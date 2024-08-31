from squadai import Agent, Squad, Process, Task
from squadai.project import SquadBase, agent, squad, task

# Uncomment the following line to use an example of a custom tool
# from demo_pipeline.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from squadai_tools import SerperDevTool


@SquadBase
class NormalSquad:
    """Normal Email Squad"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def normal_handler(self) -> Agent:
        return Agent(config=self.agents_config["normal_handler"], verbose=True)

    @task
    def urgent_task(self) -> Task:
        return Task(
            config=self.tasks_config["normal_task"],
        )

    @squad
    def squad(self) -> Squad:
        """Creates the Normal Email Squad"""
        return Squad(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
