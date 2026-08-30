// Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
// Licensed under the Apache License, Version 2.0
// SPDX-License-Identifier: Apache-2.0
// Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
// ── Backend API URL ───────────────────────────────────────────
// Auto-selects production vs dev based on Chrome extension context.
// In production: packaged extension has no update_url pointing to localhost.
// In dev: load unpacked from localhost.
const _IS_PROD = !!(chrome?.runtime?.getManifest?.().update_url);
const API = _IS_PROD
  ? "https://fake-news-analyzer-j6ka.onrender.com"   // Production (Render)
  : "http://localhost:8000";                           // Local dev

const API_TIMEOUT_MS = 20000;
const CLIENT_NAME = "edge-extension";
const CLIENT_VERSION = (chrome?.runtime?.getManifest?.().version) || "unknown";

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
