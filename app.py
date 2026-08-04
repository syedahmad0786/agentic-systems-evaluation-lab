from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from evaluator import SYSTEMS, evaluate_system


class EvaluationRequest(BaseModel):
    system: Literal["campaign-command", "language-mix", "proof-lab"]


app = FastAPI(title="Agentic Systems Evaluation Lab API", version="1.0.0")


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
        return evaluate_system(payload.system)
    except Exception as exc:
        raise HTTPException(502, f"Evaluation target unavailable: {type(exc).__name__}") from exc


PUBLIC = Path(__file__).with_name("public")
if PUBLIC.exists():
    app.mount("/assets", StaticFiles(directory=PUBLIC), name="assets")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(PUBLIC / "index.html")

