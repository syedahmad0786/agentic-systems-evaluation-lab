from agentic_systems_evaluation_lab.crew import AgenticSystemsEditorialCrew


DEFAULT_INPUTS = {
    "topic": "Why agentic systems need evidence gates before they act",
    "audience": "Founders and operations leaders evaluating practical AI systems",
    "channel": "Ahmad Bukhari personal LinkedIn, with a separate AiXCEL company adaptation",
    "source_packet": (
        "CrewAI organizes specialized agents inside a crew. Tasks give each agent a clear "
        "assignment and may pass prior task outputs as context. A sequential process runs tasks "
        "in order. CrewAI AMP provides deployment, execution history, metrics, and traces. This "
        "demo keeps publishing outside the crew: the final task prepares a release review and "
        "pauses for a named human decision."
    ),
    "human_review_policy": (
        "Draft and review only. Ahmad Bukhari owns the final publish decision. "
        "No social account or publishing tool is connected in this trial."
    ),
}


def run():
    """Run the teaching crew with its safe default evidence packet."""
    return AgenticSystemsEditorialCrew().crew().kickoff(inputs=DEFAULT_INPUTS)
