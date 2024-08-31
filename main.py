import os
import json
import asyncio
from typing import List, Dict, Any
from squadai import Agent, Task, Squad, Process, Pipeline
from squadai.squadai_tools import FileWriterTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from groq import Groq
from dotenv import load_dotenv
from tool_reg import tool_registry
import tool_reg.search_tools
import tool_reg.file_tools
import tool_reg.info_tools

load_dotenv()

# Initialize tools
duckduckgo_tool = tool_registry.get("duckduckgo")
wikipedia_tool = tool_registry.get("wikipedia")
wolframalpha_tool = tool_registry.get("wolframalpha")
write_file_tool = tool_registry.get("write_file")
read_file_tool = tool_registry.get("read_file")
list_directory_tool = tool_registry.get("list_directory")
copy_file_tool = tool_registry.get("copy_file")
delete_file_tool = tool_registry.get("delete_file")
file_search_tool = tool_registry.get("file_search")
move_file_tool = tool_registry.get("move_file")



# Set up Groq API (make sure to set your API key in the environment variables)
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def get_squad_config(user_prompt: str) -> Dict[str, Any]:
    """
    Use Groq's API to generate a SquadAI configuration based on the user's prompt.
    """
    with open("system_message.txt", "r") as f:
        system_message = f.read()

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Create a SquadAI configuration for the following goal: {user_prompt}"}
        ]
    )

    llm_response = response.choices[0].message.content
    print("Raw LLM response:", llm_response)

    # Remove backticks if present
    llm_response = llm_response.strip('`')
    if llm_response.startswith('json'):
        llm_response = llm_response[4:].strip()

    try:
        config = json.loads(llm_response)
    except json.JSONDecodeError:
        print("Error: Invalid JSON. Attempting to fix...")
        config = fix_json(llm_response)

    return config

def fix_json(invalid_json: str) -> Dict[str, Any]:
    """
    Attempt to fix invalid JSON by sending it back to the LLM for correction.
    """
    system_message = """
    The following JSON is invalid. Please correct any syntax errors and return a valid JSON object.
    Only respond with the corrected JSON, nothing else.
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": invalid_json}
        ]
    )

    corrected_json = response.choices[0].message.content
    corrected_json = corrected_json.strip('`')
    if corrected_json.startswith('json'):
        corrected_json = corrected_json[4:].strip()

    try:
        return json.loads(corrected_json)
    except json.JSONDecodeError:
        raise ValueError("Unable to generate valid JSON configuration. Please try again with a different prompt.")

def create_agent(agent_config: Dict[str, Any]) -> Agent:
    """
    Create an Agent instance from a configuration dictionary.
    """
    tools = []
    if "search_tool" in agent_config["tools"]:
        tools.append(duckduckgo_tool)
    if "wikipedia_tool" in agent_config["tools"]:
        tools.append(wikipedia_tool)
    if "wolframalpha_tool" in agent_config["tools"]:
        tools.append(wolframalpha_tool)
    if "write_file_tool" in agent_config["tools"]:
        tools.append(write_file_tool)

    return Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        verbose=agent_config["verbose"],
        allow_delegation=agent_config["allow_delegation"],
        tools=tools
    )

def create_task(task_config: Dict[str,Any], agents: List[Agent]) -> Task:
    """
    Create a Task instance from a configuration dictionary and a list of available agents.
    """
    agent = next(agent for agent in agents if agent.role == task_config["agent"])
    return Task(
        description=task_config["description"],
        expected_output=task_config["expected_output"],
        agent=agent
    )

def create_squad(squad_config: Dict[str, Any], agents: List[Agent], tasks: List[Task]) -> Squad:
    """
    Create a Squad instace from configuration dictionary, a list of available agents, and a list of tasks.
    """
    squad_agents = [next(agent for agent in agents if agent.role == role) for role in squad_config["agents"]]
    squad_tasks = [next(task for task in tasks if task.description == desc) for desc in squad_config["tasks"]]

    manager = None
    if squad_config["process"] == "hierarchical":
        manager = Agent(
            role="Project Manager",
            goal="Efficiently manage the squad and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the squad members, ensuring that each task is completed on time and to the highest standard.",
            allow_delegation=True,
            verbose=True
        )

    return Squad(
        name=squad_config["name"],
        agents=squad_agents,
        tasks=squad_tasks,
        process=Process.sequential if squad_config["process"] == "sequential" else Process.hierarchical,
        verbose=squad_config["verbose"],
        manager_agent=manager
    )

def create_pipeline(pipeline_config: List[str], squads: List[Squad]) -> Pipeline:
    """
    Create a Pipeline instance from a configuration list and a list of available squads.
    """
    pipeline_squads = [next(squad for squad in squads if squad.name == squad_name) for squad_name in pipeline_config]
    return Pipeline(stages=pipeline_squads)

def needs_wolframalpha(config: Dict[str, Any]) -> bool:
    """
    Check if any agent in the configuration uses the Wolfram Alpha tool.
    """
    for agent in config["agents"]:
        if "wolframalpha_tool" in agent["tools"]:
            return True
    return False

def run_sync_squad(config: Dict[str, Any], user_prompt: str) -> str:
    """
    Run the squad synchronously when Wolfram Alpha is needed or there's no pipeline.
    """
    agents = [create_agent(agent_config) for agent_config in config["agents"]]
    tasks = [create_task(task_config, agents) for task_config in config["tasks"]]
    squads = [create_squad(squad_config, agents, tasks) for squad_config in config["squads"]]

    if "pipeline" in config:
        inputs = [{"initial query": user_prompt}]
        pipeline = create_pipeline(config["pipeline"], squads)
        result = pipeline.kickoff(inputs=inputs)
        return result[0].raw
    else:
        result = "Running squads individually (sync mode):\n"
        for squad in squads:
            squad_result = squad.kickoff()
            result += f"\n{squad.name}: {squad_result}"
        return result

async def run_async_squad(config: Dict[str, Any], user_prompt: str) -> str:
    """
    Run the squad asynchronously when a pipeline is used and Wolfram Alpha is not needed.
    """
    agents = [create_agent(agent_config) for agent_config in config["agents"]]
    tasks = [create_task(task_config, agents) for task_config in config["tasks"]]
    squads = [create_squad(squad_config, agents, tasks) for squad_config in config["squads"]]

    if "pipeline" in config:
        inputs = [{"initial query": user_prompt}]
        pipeline = create_pipeline(config["pipeline"], squads)
        result = await pipeline.kickoff(inputs=inputs)
        return result[0].raw
    else:
        result = "No pipeline defined. Running squads individually (async mode):\n"
        for squad in squads:
            squad_result = await squad.kickoff()
            result += f"\n{squad.name}: {squad_result}"
        return result

def run_dynamic_squad(user_prompt: str) -> str:
    """
    Run a dynamically created squadAI based on the user's prompt.
    """
    config = get_squad_config(user_prompt)
    
    if needs_wolframalpha(config) or "pipeline" not in config:
        return run_sync_squad(config, user_prompt)
    else:
        return asyncio.run(run_async_squad(config, user_prompt))

def main():
    user_prompt = input("Enter your goal for squadAI: ")
    try:
        result = run_dynamic_squad(user_prompt)

        print("-----------------------------")
        print("SquadAI Result:")
        print(result)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again with a different prompt or check your configuration.")

if __name__ == "__main__":
    main()
