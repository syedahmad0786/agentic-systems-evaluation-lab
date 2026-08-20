# Status

## 2026-08-20 — CrewAI editorial teaching trial live
- Added a four-agent evidence-to-content crew, deterministic no-key teaching model, sequential context handoffs, claims gate, and external human publish boundary.
- CrewAI AMP is online; hosted execution `d5ea70c1-762e-42eb-a87d-842ca8beed81` completed successfully with `READY_FOR_HUMAN_REVIEW` and `HUMAN DECISION REQUIRED`.
- Vercel production visual is responsive and healthy; desktop/mobile light-dark QA passed with no overflow or browser errors, and the API health endpoint returns `ok`.
- Next: connect and evaluate a provider-backed model only when open-ended content quality is in scope; keep publishing disconnected until named human approval.
