"""
LangGraph Workflow — FactCheck Graph

Stateful orchestration of the fact-checking pipeline.
Nodes are connected with conditional edges so the graph can:
  - Skip live search if memory retrieval was sufficient
  - Re-route to live search if evidence is insufficient
  - Write memory only when verdict is confident

Graph:
  START
    ↓
  normalize_claim
    ↓
  run_ml  ──────── (parallel) ──── retrieve_memory
    ↓                                    ↓
  retrieve_live ◄──── (if needed) ───────┘
    ↓
  rag_reason
    ↓
  detect_conflicts
    ↓
  analyze_manipulation
    ↓
  meta_decide
    ↓
  write_memory
    ↓
  END
"""
from __future__ import annotations

import logging
from functools import partial

logger = logging.getLogger(__name__)

try:
    from langgraph.graph import StateGraph, END
    _LANGGRAPH_AVAILABLE = True
except ImportError:
    _LANGGRAPH_AVAILABLE = False
    logger.info("LangGraph not installed — workflow will run in sequential fallback mode")

from app.graph.state  import FactCheckState
from app.graph import nodes


# ── Routing functions ─────────────────────────────────────────

def _route_after_conflicts(state: FactCheckState) -> str:
    """
    If evidence is insufficient AND live search hasn't been done yet,
    route back to retrieve_live. Otherwise continue.
    """
    if state.get("needs_live_search") and not state.get("live_evidence"):
        return "retrieve_live"
    return "analyze_manipulation"


# ── Build LangGraph workflow ──────────────────────────────────

def build_graph(db=None):
    """
    Build and compile the LangGraph StateGraph.

    db is injected so nodes can access the database session.
    Returns a compiled graph with an .invoke() method.
    """
    if not _LANGGRAPH_AVAILABLE:
        return None

    graph = StateGraph(FactCheckState)

    # Bind db to nodes that need it
    retrieve_memory_node = partial(nodes.retrieve_memory, db=db)
    write_memory_node    = partial(nodes.write_memory,    db=db)

    # Add nodes
    graph.add_node("normalize_claim",      nodes.normalize_claim)
    graph.add_node("run_ml",               nodes.run_ml)
    graph.add_node("retrieve_memory",      retrieve_memory_node)
    graph.add_node("retrieve_live",        nodes.retrieve_live)
    graph.add_node("rag_reason",           nodes.rag_reason)
    graph.add_node("detect_conflicts",     nodes.detect_conflicts)
    graph.add_node("analyze_manipulation", nodes.analyze_manipulation)
    graph.add_node("meta_decide",          nodes.meta_decide)
    graph.add_node("write_memory",         write_memory_node)

    # Edges
    graph.set_entry_point("normalize_claim")
    graph.add_edge("normalize_claim",  "run_ml")
    graph.add_edge("normalize_claim",  "retrieve_memory")   # parallel
    graph.add_edge("run_ml",           "retrieve_live")
    graph.add_edge("retrieve_memory",  "retrieve_live")     # wait for both
    graph.add_edge("retrieve_live",    "rag_reason")
    graph.add_edge("rag_reason",       "detect_conflicts")

    # Conditional: re-search if insufficient evidence
    graph.add_conditional_edges(
        "detect_conflicts",
        _route_after_conflicts,
        {
            "retrieve_live":        "retrieve_live",
            "analyze_manipulation": "analyze_manipulation",
        },
    )

    graph.add_edge("analyze_manipulation", "meta_decide")
    graph.add_edge("meta_decide",          "write_memory")
    graph.add_edge("write_memory",         END)

    return graph.compile()


# ── Sequential fallback (no LangGraph) ───────────────────────

def run_sequential(claim: str, db=None) -> FactCheckState:
    """
    Fallback sequential execution when LangGraph is not installed.
    Runs the same nodes in order without the graph framework.
    """
    state: FactCheckState = {"claim": claim, "node_trace": []}

    state.update(nodes.normalize_claim(state))
    state.update(nodes.run_ml(state))
    state.update(nodes.retrieve_memory(state, db=db))
    state.update(nodes.retrieve_live(state))
    state.update(nodes.rag_reason(state))
    state.update(nodes.detect_conflicts(state))

    # One re-search if insufficient evidence
    if state.get("needs_live_search") and not state.get("live_evidence"):
        state.update(nodes.retrieve_live(state))

    state.update(nodes.analyze_manipulation(state))
    state.update(nodes.meta_decide(state))
    state.update(nodes.write_memory(state, db=db))

    return state


# ── Public API ────────────────────────────────────────────────

def run_fact_check(claim: str, db=None) -> FactCheckState:
    """
    Run the full fact-checking workflow.

    Uses LangGraph if available, falls back to sequential execution.

    Args:
        claim: The claim text to fact-check.
        db:    SQLAlchemy session for memory read/write.

    Returns:
        Final FactCheckState with all signals and verdict populated.
    """
    if _LANGGRAPH_AVAILABLE:
        try:
            graph  = build_graph(db=db)
            result = graph.invoke({"claim": claim, "node_trace": []})
            return result
        except Exception as e:
            logger.warning("LangGraph execution failed, falling back to sequential: %s", e)

    return run_sequential(claim, db=db)
