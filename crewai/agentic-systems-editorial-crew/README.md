# Agentic Systems Editorial Crew

A small JSON-first CrewAI project for learning how a multi-agent content workflow is assembled and governed.

## Handoff

```text
Evidence Scout
  -> Systems Mapper
     -> Field Note Editor
        -> Claims and Release Gate
           -> HUMAN DECISION REQUIRED
```

The first three tasks pass their outputs forward through CrewAI task context. The final task uses `human_input: true`, so a hosted run can pause for feedback. No publishing or social-account tool is attached.

## Local check

```bash
uv sync
uv run crewai run
```

The default input packet is intentionally small and self-contained. Replace it with a reviewed evidence packet when testing a new topic.

## Deployment root

Deploy this directory as the CrewAI project root. It contains `pyproject.toml`, `uv.lock`, `crew.jsonc`, and `agents/` in the JSON-first layout expected by CrewAI AMP.
