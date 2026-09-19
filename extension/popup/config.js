// Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
// Licensed under the Apache License, Version 2.0
// SPDX-License-Identifier: Apache-2.0
// Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
// ── Backend API URL ───────────────────────────────────────────
// Auto-selects production vs dev based on Chrome extension context.
// Default: Production (Render) - override with FORCE_LOCAL_DEV=true for local testing
const _FORCE_LOCAL = localStorage.getItem("FORCE_LOCAL_DEV") === "true";
const _IS_PROD = !_FORCE_LOCAL;

const API = _IS_PROD
  ? "https://factcheckai-coq3.onrender.com"   // Production (Render)
  : "http://localhost:8000";                   // Local dev (set FORCE_LOCAL_DEV=true in console)

const API_TIMEOUT_MS = 20000;
const CLIENT_NAME = "edge-extension";
const CLIENT_VERSION = (chrome?.runtime?.getManifest?.().version) || "unknown";

// Debug: log which API is being used
console.log(`[FactCheckAI] API endpoint: ${API} (prod=${_IS_PROD})`);
// To switch to local dev: localStorage.setItem("FORCE_LOCAL_DEV", "true") then reload

function buildHeaders(extra = {}) {
	return {
		"X-Client": CLIENT_NAME,
		"X-Client-Version": CLIENT_VERSION,
		...extra,
	};
}

async function apiFetch(path, opts = {}, timeoutMs = API_TIMEOUT_MS) {
	const controller = new AbortController();
	const timer = setTimeout(() => controller.abort(), timeoutMs);
	const url = path.startsWith("http") ? path : `${API}${path}`;
	try {
		return await fetch(url, { ...opts, signal: controller.signal });
	} finally {
		clearTimeout(timer);
	}
}

async function readJsonSafe(res) {
	try {
		return await res.json();
	} catch (_) {
		return null;
	}
}
