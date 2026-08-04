from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Literal

SystemName = Literal["campaign-command", "language-mix", "proof-lab"]


@dataclass(frozen=True)
class SystemContract:
    label: str
    base_url: str
    start_path: str
    payload: dict[str, Any]
    expected_status: str
    min_traces: int


SYSTEMS: dict[SystemName, SystemContract] = {
    "campaign-command": SystemContract(
        "Creator Campaign Command",
        "https://creator-campaign-command.vercel.app",
        "/api/v1/campaigns/plan",
        {"scenario": "launch", "objective": "Qualified trial sign-ups", "budget": 18000, "idempotency_key": "agent-eval-command-001"},
        "awaiting_approval",
        5,
    ),
    "language-mix": SystemContract(
        "LanguageMix Studio",
        "https://language-mix-studio.vercel.app",
        "/api/v1/localizations/review",
        {"scenario": "wellness", "target_locale": "ar-AE", "tone": "conversational", "idempotency_key": "agent-eval-language-001"},
        "awaiting_language_review",
        5,
    ),
    "proof-lab": SystemContract(
        "Creator Campaign Proof Lab",
        "https://creator-campaign-proof-lab.vercel.app",
        "/api/v1/campaigns/prove",
        {"scenario": "commerce", "attribution_window_days": 7, "idempotency_key": "agent-eval-proof-001"},
        "awaiting_approval",
        5,
    ),
}

Fetcher = Callable[[str, str, dict[str, Any] | None, dict[str, str] | None], tuple[int, dict[str, Any], float]]


def http_fetch(method: str, url: str, payload: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any], float]:
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={"Accept": "application/json", "Content-Type": "application/json", **(headers or {})})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            raw = response.read(1_000_000)
            return response.status, json.loads(raw), round((time.perf_counter() - started) * 1000, 1)
    except urllib.error.HTTPError as exc:
        raw = exc.read(50_000)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"error": raw.decode(errors="replace")[:500]}
        return exc.code, parsed, round((time.perf_counter() - started) * 1000, 1)


def _evidence_valid(items: Any) -> bool:
    return bool(items) and all(isinstance(item, dict) and item.get("source") and item.get("locator") and item.get("content_hash") for item in items)


def _check(name: str, passed: bool, weight: int, evidence: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "weight": weight, "earned": weight if passed else 0, "evidence": evidence}


def evaluate_system(name: SystemName, fetcher: Fetcher = http_fetch) -> dict[str, Any]:
    contract = SYSTEMS[name]
    health_code, health, health_ms = fetcher("GET", f"{contract.base_url}/api/v1/health", None, None)
    cap_code, capabilities, cap_ms = fetcher("GET", f"{contract.base_url}/api/v1/capabilities", None, None)
    first_code, first, first_ms = fetcher("POST", f"{contract.base_url}{contract.start_path}", contract.payload, {"x-demo-mode": "replay"})
    second_code, second, second_ms = fetcher("POST", f"{contract.base_url}{contract.start_path}", contract.payload, {"x-demo-mode": "replay"})
    live_code, _, live_ms = fetcher("POST", f"{contract.base_url}{contract.start_path}", contract.payload, {"x-demo-mode": "live"})

    required = {"run_id", "status", "mode", "created_at", "traces", "proposal", "evidence", "usage"}
    checks = [
        _check("Availability", health_code == 200 and health.get("status") == "ok" and cap_code == 200, 10, f"health={health_code}; capabilities={cap_code}"),
        _check("Typed run contract", first_code == 200 and required.issubset(first), 20, f"missing={sorted(required - set(first))}"),
        _check("Resolvable evidence", _evidence_valid(first.get("evidence")), 20, f"evidence_refs={len(first.get('evidence') or [])}"),
        _check("Human decision gate", first.get("status") == contract.expected_status and bool(first.get("proposal")), 20, f"status={first.get('status')}"),
        _check("Live-provider boundary", live_code == 403, 10, f"live_probe_http={live_code}"),
        _check("Idempotent replay", first.get("run_id") and first.get("run_id") == second.get("run_id"), 10, f"run_ids={first.get('run_id')},{second.get('run_id')}"),
        _check("Bounded trace and latency", len(first.get("traces") or []) >= contract.min_traces and max(health_ms, cap_ms, first_ms, second_ms, live_ms) < 12_000, 10, f"traces={len(first.get('traces') or [])}; max_ms={max(health_ms, cap_ms, first_ms, second_ms, live_ms)}"),
    ]
    score = sum(item["earned"] for item in checks)
    return {
        "system": name,
        "label": contract.label,
        "score": score,
        "grade": "production-shaped" if score >= 90 else "needs-work" if score >= 70 else "not-ready",
        "checks": checks,
        "run_id": first.get("run_id"),
        "mode": first.get("mode"),
        "evaluated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "limitations": [
            "This is black-box replay evaluation, not client production acceptance.",
            "Provider quality, real-data privacy, and external mutation controls require separate authenticated tests.",
        ],
    }

