from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from evaluator import SYSTEMS, EvaluationScenario, evaluate_system


class EvaluationRequest(BaseModel):
    system: Literal["campaign-command", "language-mix", "proof-lab"]
    scenario: EvaluationScenario = "baseline"


app = FastAPI(title="Agentic Systems Evaluation Lab API", version="1.0.0")
LOGGER = logging.getLogger("portfolio.observability")
LOGGER.setLevel(logging.INFO)


@app.middleware("http")
async def observability(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID") or uuid.uuid4().hex
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        LOGGER.exception(json.dumps({"event": "http_error", "service": "agentic-systems-evaluation-lab", "trace_id": trace_id, "route": request.url.path, "method": request.method, "duration_ms": round((time.perf_counter() - started) * 1000, 1), "error_type": type(exc).__name__}))
        raise
    response.headers.update({"X-Trace-ID": trace_id, "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "strict-origin-when-cross-origin"})
    LOGGER.info(json.dumps({"event": "http_request", "service": "agentic-systems-evaluation-lab", "trace_id": trace_id, "route": request.url.path, "method": request.method, "status": response.status_code, "duration_ms": round((time.perf_counter() - started) * 1000, 1)}))
    return response


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "mode": "live-black-box", "version": app.version}


@app.get("/api/v1/capabilities")
def capabilities():
    return {
        "systems": [{"id": key, "label": value.label, "base_url": value.base_url} for key, value in SYSTEMS.items()],
        "checks": ["availability", "typed-contract", "evidence", "approval-gate", "live-boundary", "idempotency", "trace-latency"],
        "arbitrary_urls": False,
    }


@app.post("/api/v1/evaluations/run")
def run_evaluation(payload: EvaluationRequest):
    try:
        return evaluate_system(payload.system, scenario=payload.scenario)
    except Exception as exc:
        raise HTTPException(502, f"Evaluation target unavailable: {type(exc).__name__}") from exc


PUBLIC = Path(__file__).with_name("public")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(PUBLIC / "index.html")


@app.get("/styles.css", include_in_schema=False)
def styles():
    return FileResponse(PUBLIC / "styles.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def script():
    return FileResponse(PUBLIC / "app.js", media_type="text/javascript")
