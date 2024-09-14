from squadai import Agent, Squad, Process, Task
from squadai.project import SquadBase, agent, squad, task
from pydantic import BaseModel

# Uncomment the following line to use an example of a custom tool
# from demo_pipeline.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from squadai_tools import SerperDevTool

class UrgencyScore(BaseModel):
    urgency_score: int

@SquadBase
class ClassifierSquad:
    """Email Classifier Squad"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def classifier(self) -> Agent:
        return Agent(config=self.agents_config["classifier"], verbose=True)

    @task
    def urgent_task(self) -> Task:
        return Task(
            config=self.tasks_config["classify_email"],
            output_pydantic=UrgencyScore,
        )

    @squad
    def squad(self) -> Squad:
        """Creates the Email Classifier Squad"""
        return Squad(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
