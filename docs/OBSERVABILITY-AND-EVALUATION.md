# Observability and Evaluation Protocol

## What is connected now

The public system uses the smallest truthful monitoring stack that works at zero recurring cost:

1. FastAPI middleware creates an X-Trace-ID for every request.
2. The same trace ID is written to structured JSON request and error logs.
3. Vercel captures stdout and stderr for the deployed function.
4. Run responses expose run ID, ordered steps, evidence, usage, approval state, and errors when the project supports runs.
5. GET /api/v1/health provides availability and runtime mode.
6. GET /api/v1/capabilities exposes supported behavior and hard boundaries.
7. GitHub Actions runs the automated contract and regression tests.
8. Postman collections exercise the generated API contract.
9. The Agentic Systems Evaluation Lab runs independent black-box checks where applicable.

Langfuse, LangSmith, Sentry, and a hosted OpenTelemetry collector are not connected to this public version. They are production integration options, not current portfolio claims.

## Trace tags

The standard production trace vocabulary is:

- service
- environment
- trace_id
- run_id
- scenario
- graph_version
- agent
- step
- status
- latency_ms
- approval_state
- evidence_count
- model
- tokens
- cost_usd
- error_type
- idempotency_key_hash

Raw idempotency keys, prompts containing client data, credentials, and personal data are never log tags.

## Where monitoring happens

| Signal | Current location | Reviewer action |
|---|---|---|
| Availability | /api/v1/health and Vercel deployment checks | Confirm status and declared mode. |
| Request failure | Vercel runtime logs filtered by trace_id and error_type | Open the matching request and reproduce against preview. |
| Contract drift | GitHub Actions and OpenAPI assertion | Block the release until consumers and collection tests pass. |
| Run quality | Response traces, evidence, usage, and project golden tests | Compare the failure to the accepted fixture. |
| Approval control | Proposal and decision state plus evaluator check | Treat any bypass as a release blocker. |
| Public boundary | Forbidden live-mode probe | Treat any accepted live request as a security failure. |
| Browser behavior | Desktop and 390 pixel Playwright journeys | Block promotion on runtime or console errors. |

## Project evaluation gates

- Availability: health and capabilities return HTTP 200.
- Contract and evidence: required fields exist and evidence references resolve.
- Gate and live boundary: the expected approval state is present and forbidden live mode returns HTTP 403.
- Idempotency: two runs with the same key return the same run ID.
- Latency: the slowest black-box call stays below 12 seconds.
- Evaluator sensitivity: each explicit fault scenario must lower the baseline score.

## Error protocol

1. Capture the trace ID, route, status, duration, and error type.
2. Reproduce against the exact Vercel preview artifact.
3. Classify the failure as contract, input, provider, policy, data, timeout, or internal.
4. Confirm whether a proposal or external action could have escaped its gate.
5. Add the smallest regression test that would have caught the failure.
6. Fix and rerun unit, API, Postman, and browser checks.
7. Promote the already verified artifact. Do not rebuild a different commit.
8. Record production acceptance separately from code, CI, preview, and HTTP availability.

## Evaluation layers

- Deterministic controls: schemas, budgets, evidence presence, permissions, idempotency, and approval gates.
- Golden scenarios: expected status, output changes, evidence state, and failure handling.
- Black-box deployment checks: health, capabilities, live boundaries, latency, and repeat behavior.
- Human review: language quality, strategic usefulness, claim interpretation, and stakeholder acceptance.
- Model-based judges: allowed only for qualitative comparisons after calibration against human labels. They never replace deterministic security or approval checks.

## Production monitoring upgrade

When a private pilot has real traffic and an approved budget, add OpenTelemetry export to Langfuse or LangSmith for agent traces, Sentry for application errors, and a durable audit store for decisions. Alerts should be based on error rate, latency, evidence failures, approval bypasses, token and cost ceilings, and quality-regression samples. No paid service is enabled for the public portfolio.

