// Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
// Licensed under the Apache License, Version 2.0
// SPDX-License-Identifier: Apache-2.0
// Project: FactCheckAI - https://github.com/BharatChandra-sys/fake-news-extension
(() => {
  console.log("[FactCheckAI] Content script v2.6.1 loaded");
  
  // Clean up any old tooltips from previous versions
  const oldTooltip = document.getElementById("__factcheck_tooltip__");
  if (oldTooltip) oldTooltip.remove();
  
  let tooltip = null;
  let floatingToolbar = null;
  let quickActionPopup = null;
  let hideTimer = null;

  // ══════════════════════════════════════════════════════════
  // 🎨 Arc-style Floating Toolbar (like Sider)
  // ══════════════════════════════════════════════════════════
  function createFloatingToolbar() {
    const toolbar = document.createElement("div");
    toolbar.id = "__factcheck_floating_toolbar__";
    toolbar.innerHTML = `
      <button data-action="truthscan" title="Truth Scan" aria-label="Truth Scan">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7v7c0 5.5 3.8 10.7 10 12 6.2-1.3 10-6.5 10-12V7l-10-5z"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
      </button>
      <button data-action="copy" title="Copy" aria-label="Copy">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
          <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
        </svg>
      </button>
      <button data-action="highlight" title="Highlight" aria-label="Highlight">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 11l-6 6v3h9l3-3"/>
          <path d="M22 2L11 13"/>
        </svg>
      </button>
      <button data-action="note" title="Add Note" aria-label="Add Note">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
          <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
        </svg>
      </button>
      <div class="divider"></div>
      <button data-action="more" title="More" aria-label="More options">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>
        </svg>
      </button>
      <button data-action="close" title="Close" aria-label="Close">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    `;
    
    Object.assign(toolbar.style, {
      position: "fixed",
      zIndex: "2147483647",
      display: "flex",
      alignItems: "center",
      gap: "4px",
      padding: "6px",
      background: "rgba(30, 34, 40, 0.95)",
      backdropFilter: "blur(20px)",
      borderRadius: "12px",
      border: "1px solid rgba(192,193,255,0.15)",
      boxShadow: "0 8px 32px rgba(0,0,0,0.6), 0 2px 8px rgba(0,0,0,0.4)",
      opacity: "0",
      transform: "translateY(-4px) scale(0.95)",
      transition: "opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
      pointerEvents: "all",
    });

    // Style buttons
    const style = document.createElement("style");
    style.textContent = `
      #__factcheck_floating_toolbar__ button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border: none;
        background: transparent;
        color: #e8eaed;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.15s ease;
        padding: 0;
      }
      #__factcheck_floating_toolbar__ button:hover {
        background: rgba(255,255,255,0.1);
        transform: scale(1.05);
      }
      #__factcheck_floating_toolbar__ button:active {
        transform: scale(0.95);
      }
      #__factcheck_floating_toolbar__ button[data-action="truthscan"] {
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        color: white;
      }
      #__factcheck_floating_toolbar__ button[data-action="truthscan"]:hover {
        background: linear-gradient(135deg, #8b70d6 0%, #7c3aed 100%);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
      }
      #__factcheck_floating_toolbar__ .divider {
        width: 1px;
        height: 20px;
        background: rgba(255,255,255,0.1);
        margin: 0 2px;
      }
    `;
    document.head.appendChild(style);

    // Event handlers
    toolbar.addEventListener("click", e => {
      const btn = e.target.closest("button");
      if (!btn) return;
      
      const action = btn.dataset.action;
      const selectedText = window.getSelection().toString().trim();

      switch(action) {
        case "truthscan":
          if (selectedText) {
            showQuickActionPopup(selectedText);
          }
          break;
        case "copy":
          if (selectedText) {
            navigator.clipboard.writeText(selectedText);
            showToast("Copied!");
          }
          break;
        case "highlight":
          highlightSelection();
          break;
        case "close":
          removeFloatingToolbar();
          break;
      }
    });

    document.body.appendChild(toolbar);
    return toolbar;
  }

  function showFloatingToolbar(x, y) {
    // Remove any old tooltip first
    removeTooltip();
    
    if (!floatingToolbar) floatingToolbar = createFloatingToolbar();

    const tw = 280;
    const left = Math.min(Math.max(x - tw / 2, 8), window.innerWidth - tw - 8);
    const top = Math.max(y - 54, 8);

    floatingToolbar.style.left = `${left}px`;
    floatingToolbar.style.top = `${top}px`;
    floatingToolbar.style.opacity = "1";
    floatingToolbar.style.transform = "translateY(0) scale(1)";
    
    console.log("[FactCheckAI] Floating toolbar shown at", left, top);
  }

  function removeFloatingToolbar() {
    if (!floatingToolbar) return;
    floatingToolbar.style.opacity = "0";
    floatingToolbar.style.transform = "translateY(-4px) scale(0.95)";
    setTimeout(() => {
      if (floatingToolbar?.parentNode) floatingToolbar.parentNode.removeChild(floatingToolbar);
      floatingToolbar = null;
    }, 200);
  }

  // ══════════════════════════════════════════════════════════
  // 💬 Arc-style Quick Action Popup
  // ══════════════════════════════════════════════════════════
  function createQuickActionPopup(text) {
    const popup = document.createElement("div");
    popup.id = "__factcheck_quick_popup__";
    popup.innerHTML = `
      <div class="popup-content">
        <div class="popup-header">
          <div class="ai-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 011 1v3a1 1 0 01-1 1h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 01-1-1v-3a1 1 0 011-1h1a7 7 0 017-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 012-2z"/>
            </svg>
          </div>
          <span>Ask AI with the above content</span>
        </div>
        <div class="selected-preview">${text.substring(0, 100)}${text.length > 100 ? '...' : ''}</div>
        <button class="action-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7v7c0 5.5 3.8 10.7 10 12 6.2-1.3 10-6.5 10-12V7l-10-5z"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
          Truth Scan
        </button>
      </div>
    `;

    const style = document.createElement("style");
    style.textContent = `
      #__factcheck_quick_popup__ {
        position: fixed;
        z-index: 2147483646;
        max-width: 380px;
        background: rgba(30, 34, 40, 0.98);
        backdrop-filter: blur(24px);
        border-radius: 12px;
        border: 1px solid rgba(192,193,255,0.15);
        box-shadow: 0 12px 48px rgba(0,0,0,0.7), 0 4px 16px rgba(0,0,0,0.5);
        opacity: 0;
        transform: translateY(-8px) scale(0.96);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        pointer-events: all;
      }
      #__factcheck_quick_popup__ .popup-content {
        padding: 16px;
      }
      #__factcheck_quick_popup__ .popup-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
        color: #e8eaed;
        font-family: -apple-system, Inter, sans-serif;
        font-size: 13px;
        font-weight: 500;
      }
      #__factcheck_quick_popup__ .ai-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        color: white;
      }
      #__factcheck_quick_popup__ .selected-preview {
        padding: 12px;
        margin-bottom: 12px;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        color: #9ca3af;
        font-size: 12px;
        line-height: 1.5;
        font-family: -apple-system, Inter, sans-serif;
        max-height: 80px;
        overflow: hidden;
      }
      #__factcheck_quick_popup__ .action-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 10px 16px;
        border: none;
        border-radius: 8px;
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        color: white;
        font-size: 14px;
        font-weight: 600;
        font-family: -apple-system, Inter, sans-serif;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      #__factcheck_quick_popup__ .action-btn:hover {
        background: linear-gradient(135deg, #8b70d6 0%, #7c3aed 100%);
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
        transform: translateY(-1px);
      }
      #__factcheck_quick_popup__ .action-btn:active {
        transform: scale(0.98);
      }
    `;
    document.head.appendChild(style);

    popup.querySelector(".action-btn").addEventListener("click", () => {
      chrome.storage.local.set({ selectedText: text, pendingAnalysis: true }, () => {
        chrome.runtime.sendMessage({ type: "OPEN_POPUP_WITH_TEXT", text });
      });
      removeQuickActionPopup();
      removeFloatingToolbar();
    });

    document.body.appendChild(popup);
    return popup;
  }

  function showQuickActionPopup(text) {
    if (quickActionPopup?.parentNode) quickActionPopup.parentNode.removeChild(quickActionPopup);
    
    quickActionPopup = createQuickActionPopup(text);
    
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    
    const left = Math.min(Math.max(rect.left, 8), window.innerWidth - 390);
    const top = rect.bottom + 8;

    quickActionPopup.style.left = `${left}px`;
    quickActionPopup.style.top = `${top}px`;
    
    setTimeout(() => {
      quickActionPopup.style.opacity = "1";
      quickActionPopup.style.transform = "translateY(0) scale(1)";
    }, 10);
  }

  function removeQuickActionPopup() {
    if (!quickActionPopup) return;
    quickActionPopup.style.opacity = "0";
    quickActionPopup.style.transform = "translateY(-8px) scale(0.96)";
    setTimeout(() => {
      if (quickActionPopup?.parentNode) quickActionPopup.parentNode.removeChild(quickActionPopup);
      quickActionPopup = null;
    }, 250);
  }

  // ══════════════════════════════════════════════════════════
  // 🛠️ Helper Functions
  // ══════════════════════════════════════════════════════════
  function showToast(message) {
    const toast = document.createElement("div");
    toast.textContent = message;
    Object.assign(toast.style, {
      position: "fixed",
      top: "20px",
      left: "50%",
      transform: "translateX(-50%)",
      zIndex: "2147483647",
      padding: "10px 20px",
      background: "rgba(30, 34, 40, 0.95)",
      color: "#e8eaed",
      borderRadius: "8px",
      fontSize: "13px",
      fontFamily: "-apple-system, Inter, sans-serif",
      boxShadow: "0 4px 16px rgba(0,0,0,0.5)",
    });
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  }

  function highlightSelection() {
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const span = document.createElement("span");
      span.style.backgroundColor = "rgba(167, 139, 250, 0.3)";
      span.style.borderRadius = "2px";
      range.surroundContents(span);
      showToast("Highlighted!");
    }
  }

  // ══════════════════════════════════════════════════════════
  // 📌 Original Tooltip (kept for compatibility)
  // ══════════════════════════════════════════════════════════
  function createTooltip() {
    const el = document.createElement("div");
    el.id = "__factcheck_tooltip__";
    el.innerHTML = `
      <span style="font-size:13px;line-height:1;">🔍</span>
      <span style="font-size:12px;font-weight:600;letter-spacing:0.01em;">TruthScan this</span>
    `;
    Object.assign(el.style, {
      position:        "fixed",
      zIndex:          "2147483647",
      display:         "flex",
      alignItems:      "center",
      gap:             "6px",
      padding:         "7px 12px",
      background:      "#1e2228",
      color:           "#e8eaed",
      borderRadius:    "8px",
      border:          "1px solid rgba(192,193,255,0.18)",
      boxShadow:       "0 4px 16px rgba(0,0,0,0.5)",
      cursor:          "pointer",
      fontFamily:      "-apple-system, 'Inter', sans-serif",
      userSelect:      "none",
      pointerEvents:   "all",
      opacity:         "0",
      transform:       "translateY(4px)",
      transition:      "opacity 0.15s ease, transform 0.15s ease",
      whiteSpace:      "nowrap",
    });

    el.addEventListener("mouseenter", () => clearTimeout(hideTimer));
    el.addEventListener("mouseleave", () => scheduleHide(800));
    el.addEventListener("mousedown", e => {
      e.preventDefault();
      e.stopPropagation();
      const text = window.getSelection().toString().trim();
      if (text) {
        chrome.storage.local.set({ selectedText: text, pendingAnalysis: true }, () => {
          chrome.runtime.sendMessage({ type: "OPEN_POPUP_WITH_TEXT", text });
        });
      }
      removeTooltip();
    });

    document.body.appendChild(el);
    return el;
  }

  function showTooltip(x, y) {
    if (!tooltip) tooltip = createTooltip();

    // Position above the selection, centered
    const tw = 160;
    const left = Math.min(Math.max(x - tw / 2, 8), window.innerWidth - tw - 8);
    const top  = Math.max(y - 44, 8);

    tooltip.style.left    = `${left}px`;
    tooltip.style.top     = `${top}px`;
    tooltip.style.opacity = "1";
    tooltip.style.transform = "translateY(0)";
  }

  function removeTooltip() {
    if (!tooltip) return;
    tooltip.style.opacity   = "0";
    tooltip.style.transform = "translateY(4px)";
    setTimeout(() => {
      if (tooltip && tooltip.parentNode) tooltip.parentNode.removeChild(tooltip);
      tooltip = null;
    }, 150);
  }

  function scheduleHide(delay = 300) {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      removeTooltip();
      removeFloatingToolbar();
      removeQuickActionPopup();
    }, delay);
  }

  // Debounce timer for TEXT_SELECTED messages — prevents firing on every
  // character of a drag selection (fires once, 300ms after mouseup settles)
  let _selectionDebounceTimer = null;

  // ══════════════════════════════════════════════════════════
  // 🎯 Event Listeners
  // ══════════════════════════════════════════════════════════
  
  // Listen for mouseup to detect selection
  document.addEventListener("mouseup", e => {
    // Small delay so selection is finalised
    setTimeout(() => {
      const selected = window.getSelection().toString().trim();

      if (selected.length > 20) {
        clearTimeout(hideTimer);
        // Show floating toolbar instead of simple tooltip
        showFloatingToolbar(e.clientX, e.clientY);

        // Debounced background notification — avoids flooding service worker
        clearTimeout(_selectionDebounceTimer);
        _selectionDebounceTimer = setTimeout(() => {
          chrome.runtime.sendMessage({
            type: "TEXT_SELECTED",
            payload: selected
          }).catch(() => {});
        }, 300);
      } else {
        scheduleHide(100);
      }
    }, 10);
  });

  // Hide on click elsewhere
  document.addEventListener("mousedown", e => {
    if (floatingToolbar && !floatingToolbar.contains(e.target) &&
        quickActionPopup && !quickActionPopup.contains(e.target)) {
      scheduleHide(100);
    }
  });

  // Hide on scroll
  document.addEventListener("scroll", () => scheduleHide(100), { passive: true });

})();
