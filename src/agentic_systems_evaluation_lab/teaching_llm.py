"""Credential-free teaching model for the live CrewAI orchestration trial.

This is deliberately deterministic. It lets the deployed crew prove agent/task
handoffs and the human-input pause without presenting template output as model
quality evidence. Replace it with a provider-backed CrewAI LLM for open-ended
content generation.
"""

from __future__ import annotations

from typing import Any

from crewai.events.types.llm_events import LLMCallType
from crewai.llms.base_llm import BaseLLM, llm_call_context
from crewai.utilities.types import LLMMessage


class TeachingLLM(BaseLLM):
    """A fixed, evidence-bounded CrewAI LLM used only by this teaching trial."""

    llm_type: str = "teaching"

    def __init__(self) -> None:
        super().__init__(
            model="teaching/deterministic-v1",
            provider="teaching",
            temperature=0,
        )

    def call(
        self,
        messages: str | list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: type[Any] | None = None,
    ) -> str:
        """Return the bounded teaching artifact for the active specialist role."""
        del response_model
        with llm_call_context():
            self._emit_call_started_event(
                messages=messages,
                tools=tools,
                callbacks=callbacks,
                available_functions=available_functions,
                from_task=from_task,
                from_agent=from_agent,
            )
            role = str(getattr(from_agent, "role", "")).lower()
            prompt = self._messages_text(messages).lower()
            response = self._response_for(role=role, prompt=prompt)
            usage = {
                "prompt_tokens": max(1, len(prompt) // 4),
                "completion_tokens": max(1, len(response) // 4),
                "total_tokens": max(2, (len(prompt) + len(response)) // 4),
                "successful_requests": 1,
            }
            self._track_token_usage_internal(usage)
            self._emit_call_completed_event(
                response=response,
                call_type=LLMCallType.LLM_CALL,
                from_task=from_task,
                from_agent=from_agent,
                messages=messages,
                usage=usage,
                finish_reason="stop",
            )
            return response

    @staticmethod
    def _messages_text(messages: str | list[LLMMessage]) -> str:
        if isinstance(messages, str):
            return messages
        return "\n".join(str(message.get("content", "")) for message in messages)

    @classmethod
    def _response_for(cls, *, role: str, prompt: str) -> str:
        if "claims and release gate" in role:
            body = cls._release_review()
        elif "field note editor" in role:
            body = cls._content_pack()
        elif "systems mapper" in role:
            body = cls._systems_map()
        elif "evidence scout" in role:
            body = cls._evidence_ledger()
        elif "audit the content pack" in prompt or "release review" in prompt:
            body = cls._release_review()
        elif "channel-separated" in prompt or "three hooks" in prompt:
            body = cls._content_pack()
        elif "six-part systems map" in prompt:
            body = cls._systems_map()
        elif "claim ledger" in prompt:
            body = cls._evidence_ledger()
        else:
            body = (
                "## Teaching-model boundary\n\n"
                "This deterministic model received an unrecognized task. No content was "
                "generated, and human review is required."
            )
        return "Thought: I can complete this bounded teaching step.\nFinal Answer:\n" + body

    @staticmethod
    def _evidence_ledger() -> str:
        return """## SUPPORTED

- **S1 — Crew structure.** “CrewAI organizes specialized agents inside a crew.”
- **S2 — Task context.** “Tasks give each agent a clear assignment and may pass prior task outputs as context.”
- **S3 — Execution order.** “A sequential process runs tasks in order.”
- **S4 — Operational evidence.** “CrewAI AMP provides deployment, execution history, metrics, and traces.”
- **S5 — Release boundary.** “This demo keeps publishing outside the crew: the final task prepares a release review and pauses for a named human decision.”

## INFERENCE

- **I1.** Narrow specialist roles can make ownership and handoffs easier to inspect than one undifferentiated assistant.
- **I2.** A trace can support diagnosis, but a trace alone does not prove content quality or production acceptance.

## OPEN

- Which provider-backed model should be used for open-ended drafts?
- What source-approval standard should govern a real editorial calendar?
- Which acceptance tests are required before any publishing integration is connected?

**Evidence boundary:** this ledger uses only the supplied demonstration packet; it does not browse or add external claims."""

    @staticmethod
    def _systems_map() -> str:
        return """## Six-part systems map

1. **Signal** — A named topic, audience, channel, policy, and bounded source packet enter the crew.
2. **Specialist role** — The Evidence Scout classifies claims; the Systems Mapper explains the operating design; the Field Note Editor separates channel voices; the Claims Gate audits release readiness.
3. **Handoff** — Each completed task becomes explicit context for the next task in the sequential process.
4. **Control gate** — Unsupported claims remain labelled, publishing tools remain disconnected, and the final task requests human input.
5. **Action** — The crew may prepare a claim ledger, systems map, draft pack, and release review. It cannot publish.
6. **Evidence receipt** — AMP records the execution timeline and traces; the final output records `READY_FOR_HUMAN_REVIEW` or `REVISE`.

## Why use narrow agents?

The teaching value is separation of responsibility. Each role owns one transformation and receives named context, so an operator can inspect where a weak claim, voice error, or release decision entered the chain. This architecture does not prove that several agents are always better than one model; that remains an evaluation question."""

    @staticmethod
    def _content_pack() -> str:
        return """## Hooks

1. An agentic system becomes useful when you can see where judgment changes hands.
2. Four AI agents are not automatically safer than one. The gates between them are the real design.
3. The most important agent in this content crew cannot publish anything.

**Recommended:** Hook 2 — it creates useful tension without claiming a measured outcome.

## Ahmad Bukhari — personal LinkedIn Field Note

Four AI agents are not automatically safer than one. The gates between them are the real design.

I built this small CrewAI trial to make that idea visible.

The first agent does not write a post. It creates an evidence ledger and labels what is supported, inferred, or still open. The second turns that ledger into a systems map: signal, role, handoff, control, action, and receipt. Only then does an editor prepare two distinct drafts—one for my personal channel and another for AiXCEL.

The fourth agent is a claims gate. It checks the draft against the original ledger and can only return a release review. It has no social tool, no account access, and no authority to publish.

That separation matters because “multi-agent” can otherwise become a diagram that hides one long prompt. In this trial, each task has a named owner and each handoff carries the earlier output as context. CrewAI AMP then holds the execution history and trace.

There is also a deliberate limit: the live trial uses a deterministic teaching model. It proves the orchestration path can run and pause for human input; it does not prove provider quality, factual breadth, or production acceptance.

For me, that is the useful starting point: make the decision path inspectable before making the system more capable.

Where would you place the first non-negotiable human gate in your workflow?

## AiXCEL — company adaptation

Multi-agent architecture is most useful when responsibility is inspectable.

This CrewAI teaching trial separates an editorial workflow into four controlled stages: evidence classification, systems mapping, channel-specific drafting, and claim review. Prior outputs are passed forward as explicit task context, while the final task stops for named human input.

The crew has no publishing integration. Its current deterministic teaching model is designed to prove orchestration and governance behavior—not model quality or production readiness. AMP provides the live execution record and traces.

This is the implementation pattern AiXCEL is testing: bounded inputs, narrow roles, visible handoffs, explicit release state, and human ownership of consequential action.

## Visual brief

A horizontal relay with four specialist stations. Show the evidence ledger physically passing between agents, with the final path ending at a locked human decision gate—not a social platform icon.

## Closing question

Where would you place the first non-negotiable human gate in your workflow?"""

    @staticmethod
    def _release_review() -> str:
        return """## Release state

`READY_FOR_HUMAN_REVIEW`

## Claim audit

- Crew structure and specialist roles — **SUPPORTED** by S1 and the supplied crew definition.
- Task outputs passed as context — **SUPPORTED** by S2.
- Sequential execution — **SUPPORTED** by S3.
- AMP execution history and traces — **SUPPORTED** by S4.
- Publishing remains outside the crew — **SUPPORTED** by S5 and the stated policy.
- Narrow roles improve inspectability — **INFERENCE**, labelled as a design rationale rather than a measured result.
- No provider-quality, ROI, autonomy, or production-acceptance claim appears — **PASS**.

## Channel-separation check

**PASS.** Ahmad’s draft uses first-person learning and judgment. The AiXCEL adaptation describes the implementation pattern in company voice. Neither implies publication or customer adoption.

## Required edits

None for this bounded teaching packet. Re-run the evidence gate if the source packet or factual claims change.

## HUMAN DECISION REQUIRED

The crew is stopping here. Ahmad Bukhari must review, revise, approve, and publish outside this automation. No social account or publishing tool is connected."""
