from pydantic import BaseModel
from squadai import Agent, Squad, Process, Task
from squadai.project import SquadBase, agent, squad, task

# Uncomment the following line to use an example of a custom tool
# from demo_pipeline.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from squadai_tools import SerperDevTool


class ResearchReport(BaseModel):
	"""Research Report"""
	title: str
	body: str

@SquadBase
class ResearchSquad():
	"""Research Squad"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_pydantic=ResearchReport
		)

	@squad
	def squad(self) -> Squad:
		"""Creates the Research Squad"""
		return Squad(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)