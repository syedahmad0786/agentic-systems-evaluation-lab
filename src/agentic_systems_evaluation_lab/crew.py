from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class AgenticSystemsEditorialCrew:
    """Evidence-led content crew with a final human release gate."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def evidence_scout(self) -> Agent:
        return Agent(config=self.agents_config["evidence_scout"], verbose=True)  # type: ignore[index]

    @agent
    def systems_mapper(self) -> Agent:
        return Agent(config=self.agents_config["systems_mapper"], verbose=True)  # type: ignore[index]

    @agent
    def field_note_editor(self) -> Agent:
        return Agent(config=self.agents_config["field_note_editor"], verbose=True)  # type: ignore[index]

    @agent
    def claims_gate(self) -> Agent:
        return Agent(config=self.agents_config["claims_gate"], verbose=True)  # type: ignore[index]

    @task
    def build_evidence_ledger(self) -> Task:
        return Task(config=self.tasks_config["build_evidence_ledger"])  # type: ignore[index]

    @task
    def map_the_system(self) -> Task:
        return Task(
            config=self.tasks_config["map_the_system"],  # type: ignore[index]
            context=[self.build_evidence_ledger()],
        )

    @task
    def draft_content_pack(self) -> Task:
        return Task(
            config=self.tasks_config["draft_content_pack"],  # type: ignore[index]
            context=[self.build_evidence_ledger(), self.map_the_system()],
        )

    @task
    def review_release_packet(self) -> Task:
        return Task(
            config=self.tasks_config["review_release_packet"],  # type: ignore[index]
            context=[
                self.build_evidence_ledger(),
                self.map_the_system(),
                self.draft_content_pack(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            tracing=True,
        )
