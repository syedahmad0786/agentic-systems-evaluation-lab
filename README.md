# Agentic Systems Evaluation Lab

Reproducible black-box checks for three deployed creator-economy agentic systems. The evaluator verifies API availability, typed run contracts, evidence references, human approval gates, disabled live-provider access, idempotent replay, trace depth, and latency.

**Live:** https://agentic-systems-evaluation-lab.vercel.app

The live page now includes a CrewAI teaching trial for an agentic-systems content workflow. Its four-stage handoff rail is a labelled browser replay; the deployable JSON-first CrewAI source lives under [`crewai/agentic-systems-editorial-crew/`](crewai/agentic-systems-editorial-crew/).

The linked AMP automation still validates the Git repository root with CrewAI's classic scaffold rules, so an equivalent compatibility package lives under [`src/agentic_systems_evaluation_lab/`](src/agentic_systems_evaluation_lab/). Both definitions preserve the same four roles, sequential handoffs, model choice, and final human-input gate; the JSON-first folder remains the clearer teaching source.

## Run

```bash
uv sync
uv run uvicorn app:app --reload
uv run pytest
```

Open `http://127.0.0.1:8000`. API source of truth: `/openapi.json`.

## Truth boundary

This proves public replay behavior only. It does not claim real client data, production acceptance, provider quality, or authenticated mutation safety. Those require private integration tests and named human approval.

The CrewAI trial drafts and reviews content but has no publishing tool. CrewAI AMP is the authority for live deployment and execution traces; the public handoff animation exists only to explain the architecture.

See [SYSTEM-GUIDE.md](SYSTEM-GUIDE.md) and [docs/architecture.mmd](docs/architecture.mmd).
## Technical proof package

- [Full case study](CASE-STUDY.md)
- [System guide](SYSTEM-GUIDE.md)
- [Observability and evaluation protocol](docs/OBSERVABILITY-AND-EVALUATION.md)
- [System context](docs/diagrams/system-context.svg)
- [Agent collaboration](docs/diagrams/agent-collaboration.svg)
- [Runtime and observability](docs/diagrams/runtime-observability.svg)

Every architecture visual is committed as Mermaid source, editable Excalidraw, SVG, and PNG. The live page labels synthetic, replay, statistical, and human-gated behavior explicitly.

## Theme system

The product surface follows the visitor's operating-system preference on first load and provides a keyboard-accessible light and dark theme switch. The selected theme is stored only in local browser storage, updates the browser theme color, and persists after reload. Both themes are checked at 1440 pixels and 390 pixels for visibility, overflow, browser errors, and page errors.
