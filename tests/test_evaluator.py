from evaluator import evaluate_system


def fake_fetch(method, url, payload=None, headers=None):
    if url.endswith("/health"):
        return 200, {"status": "ok", "mode": "verified-replay"}, 10.0
    if url.endswith("/capabilities"):
        return 200, {"tools": []}, 10.0
    if headers and headers.get("x-demo-mode") == "live":
        return 403, {"detail": "disabled"}, 10.0
    return 200, {
        "run_id": "same-run",
        "status": "awaiting_approval",
        "mode": "verified-replay",
        "created_at": "2026-08-04T00:00:00Z",
        "traces": [{"agent": str(i)} for i in range(5)],
        "proposal": {"required_approver": "owner"},
        "evidence": [{"source": "fixture", "locator": "one", "content_hash": "abc"}],
        "usage": {"estimated_cost_usd": 0},
    }, 10.0


def test_perfect_contract_scores_100():
    result = evaluate_system("campaign-command", fake_fetch)
    assert result["score"] == 100
    assert all(check["passed"] for check in result["checks"])


def test_missing_evidence_fails_evidence_check():
    def no_evidence(method, url, payload=None, headers=None):
        code, body, latency = fake_fetch(method, url, payload, headers)
        if method == "POST" and code == 200:
            body = {**body, "evidence": []}
        return code, body, latency

    result = evaluate_system("campaign-command", no_evidence)
    assert result["score"] == 80
    assert next(c for c in result["checks"] if c["name"] == "Resolvable evidence")["passed"] is False

