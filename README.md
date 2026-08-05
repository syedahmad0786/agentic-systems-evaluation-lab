# Agentic Systems Evaluation Lab

Reproducible black-box checks for three deployed creator-economy agentic systems. The evaluator verifies API availability, typed run contracts, evidence references, human approval gates, disabled live-provider access, idempotent replay, trace depth, and latency.

**Live:** https://agentic-systems-evaluation-lab.vercel.app

## Run

```bash
uv sync
uv run uvicorn app:app --reload
uv run pytest
```

Open `http://127.0.0.1:8000`. API source of truth: `/openapi.json`.

## Truth boundary

This proves public replay behavior only. It does not claim real client data, production acceptance, provider quality, or authenticated mutation safety. Those require private integration tests and named human approval.

See [SYSTEM-GUIDE.md](SYSTEM-GUIDE.md) and [docs/architecture.mmd](docs/architecture.mmd).
## Technical proof package

- [Full case study](CASE-STUDY.md)
- [System guide](SYSTEM-GUIDE.md)
- [Observability and evaluation protocol](docs/OBSERVABILITY-AND-EVALUATION.md)
- [System context](docs/diagrams/system-context.svg)
- [Agent collaboration](docs/diagrams/agent-collaboration.svg)
- [Runtime and observability](docs/diagrams/runtime-observability.svg)

Every architecture visual is committed as Mermaid source, editable Excalidraw, SVG, and PNG. The live page labels synthetic, replay, statistical, and human-gated behavior explicitly.
