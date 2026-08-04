# System guide

## Why this exists

Agent demos often prove only that text appeared. This lab tests the more important system boundaries: typed output, evidence, approval, live-provider isolation, deterministic replay, bounded execution, and failure visibility.

## Flow

1. A user selects one allowlisted deployment.
2. FastAPI performs health, capability, replay, duplicate-replay, and forbidden-live probes.
3. Seven deterministic checks produce a weighted score and evidence string.
4. The browser renders the result without storing credentials or client data.

## Technology decisions

- **REST + FastAPI:** the targets already expose JSON/OpenAPI contracts, so Postman and CI can exercise the exact public boundary. GraphQL and gRPC add no value here.
- **Deterministic Python checks:** an LLM judge would make contract and security-gate checks less reproducible. LLM rubric evaluation can be added only for subjective output quality.
- **Allowlisted targets:** arbitrary URLs would create an SSRF risk in a public deployment.
- **Replay mode:** the evaluation is free, reproducible, and cannot mutate a client system.
- **Vercel:** matches the evaluated deployments and provides a zero-cost public preview. Docker remains available for local portability.

## Score

| Check | Weight |
|---|---:|
| Availability | 10 |
| Typed run contract | 20 |
| Resolvable evidence | 20 |
| Human decision gate | 20 |
| Live-provider boundary | 10 |
| Idempotent replay | 10 |
| Trace and latency bounds | 10 |

90–100 is `production-shaped`, 70–89 is `needs-work`, and below 70 is `not-ready`. The grade is deliberately not called production-ready.

## Security and limitations

The API accepts only a system identifier. It never accepts a URL, secret, prompt, or client record. The result is ephemeral. Private provider evaluation, PHI/PII handling, authorization, load, cost, and actual mutation approval remain separate acceptance gates.
