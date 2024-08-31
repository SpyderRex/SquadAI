from squadai import Agent, Squad, Process, Task
from squadai.project import SquadBase, agent, squad, task

# Uncomment the following line to use an example of a custom tool
# from demo_pipeline.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from squadai_tools import SerperDevTool


@SquadBase
class WriteXSquad:
    """Research Squad"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def x_writer_agent(self) -> Agent:
        return Agent(config=self.agents_config["x_writer_agent"], verbose=True)

    @task
    def write_x_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_x_task"],
        )

    @squad
    def squad(self) -> Squad:
        """Creates the Write X Squad"""
        return Squad(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
