import os

from squadai import Agent, Squad, Task
from multion_tool import MultiOnTool

os.environ["GROQ_API_KEY"] = "Your Key"

multion_browse_tool = MultiOnTool(api_key="Your Key")

# Create a new agent
Browser = Agent(
    role="Browser Agent",
    goal="control web browsers using natural language ",
    backstory="An expert browsing agent.",
    tools=[multion_browse_tool],
    verbose=True,
)

# Define tasks
browse = Task(
    description="Summarize the top 3 trending AI News headlines",
    expected_output="A summary of the top 3 trending AI News headlines",
    agent=Browser,
)


squad = Squad(agents=[Browser], tasks=[browse])

squad.kickoff()
