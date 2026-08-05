# Agentic Systems Evaluation Lab: Technical Case Study

## Status and proof boundary

This is a live public black-box evaluator for three allowlisted portfolio systems. It does not claim to certify arbitrary external agents or replace authenticated production acceptance.

Live system: https://agentic-systems-evaluation-lab.vercel.app

Repository: https://github.com/syedahmad0786/agentic-systems-evaluation-lab

## Scenario brief

Agent demos often pass one screenshot while failing the properties that matter in use: contract stability, evidence, approval enforcement, idempotency, provider boundaries, and latency. A reviewer needs a repeatable test that calls the deployed system rather than trusting its README.

The evaluator must call live public deployments, prevent arbitrary outbound requests, score fixed controls, retain evidence, repeat requests for idempotency, probe forbidden live mode, and prove that known faults lower the score.

## System design

The FastAPI evaluator accepts one of three fixed identifiers. It calls health and capabilities, runs the target scenario twice with one idempotency key, probes forbidden live mode, measures latency, and scores seven checks. A user can explicitly inject missing evidence, approval bypass, or latency breach into the evaluator record. These fault scenarios are labeled simulations and do not alter the target service.

## Technical decisions

| Decision | Choice and reason | Alternative not selected |
|---|---|---|
| Evaluation style | Black-box HTTP checks prove the deployed contract from outside the repository. | Unit tests alone cannot prove the public URL or runtime boundary. |
| Scoring | Deterministic weighted rules make control failures repeatable. | LLM-as-judge is not appropriate for binary approval or evidence controls. |
| Target access | A hard allowlist prevents server-side request forgery. | User-supplied URLs would expose an unsafe fetcher. |
| Fault testing | Explicit evaluator-side injections prove the score is sensitive to failures. | A fixed score of 100 is only a decorative dashboard. |
| HTTP client | Python standard library is enough for the small request surface. | Another client dependency adds no useful capability. |
| Runtime | A stateless Vercel function suits short bounded evaluations. | A queue or cluster is unnecessary until runs become long or scheduled. |

## Quantified implementation proof

- 3 allowlisted live systems.
- 7 weighted checks totaling 100 points.
- 4 scenarios: baseline plus 3 explicit faults.
- 2 replay runs per evaluation for idempotency.
- 1 forbidden live-provider probe.
- 12 second maximum measured-latency threshold.
- 0 user-supplied outbound URLs.
- Automated tests prove each injected fault reduces the score.

A score of 100 means the defined public checks passed at that time. It does not mean privacy, provider quality, or production data acceptance passed.

## Architecture

- [System context](docs/diagrams/system-context.svg)
- [Evaluation flow](docs/diagrams/agent-collaboration.svg)
- [Runtime and observability](docs/diagrams/runtime-observability.svg)

Each diagram is included as Mermaid, editable Excalidraw, SVG, and PNG.

## Constraints and next layer

The evaluator focuses on contracts and governance. It does not yet score semantic quality, hallucination, toxicity, retrieval relevance, or task success on private data. Those require project-specific golden sets, human labels, and controlled model comparisons.

The production path adds scheduled runs, durable results, alert thresholds, trace correlation with target services, and separate qualitative evaluators. Binary controls stay deterministic. Model-based judges are calibrated against human labels before they influence a release.

The lab tests deployed services rather than screenshots. It produces failures on demand, records evidence for every check, and separates public demo verification from production acceptance.
