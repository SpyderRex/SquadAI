import os
import json
from typing import Dict, Any
from squadai import Agent, Task, Squad, Process
from groq import Groq
from dotenv import load_dotenv
from tool_reg import tool_registry
import tool_reg.search_tools
import tool_reg.file_tools
import tool_reg.info_tools
from tool_reg.scrape_tools import BrowserTools

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
scrape_tool = BrowserTools.scrape_and_summarize_website

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def get_squad_config(user_prompt: str) -> Dict[str, Any]:
    """Generate a SquadAI configuration based on the user's prompt."""
    with open("system_message.txt", "r") as f:
        system_message = f.read()

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Create a SquadAI configuration for the following goal: {user_prompt}"}
        ]
    )

    llm_response = response.choices[0].message.content.strip('`')
    if llm_response.startswith('json'):
        llm_response = llm_response[4:].strip()

    try:
        return json.loads(llm_response)
    except json.JSONDecodeError:
        print("Error: Invalid JSON. Attempting to fix...")
        return fix_json(llm_response)

def fix_json(invalid_json: str) -> Dict[str, Any]:
    """Attempt to fix invalid JSON using the LLM."""
    system_message = "The following JSON is invalid. Please correct any syntax errors and return a valid JSON object. Only respond with the corrected JSON, nothing else."

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": invalid_json}
        ]
    )

    corrected_json = response.choices[0].message.content.strip('`')
    if corrected_json.startswith('json'):
        corrected_json = corrected_json[4:].strip()

    try:
        return json.loads(corrected_json)
    except json.JSONDecodeError:
        raise ValueError("Unable to generate valid JSON configuration. Please try again with a different prompt.")

def create_agent(agent_config: Dict[str, Any]) -> Agent:
    """Create an Agent instance from a configuration dictionary."""
    tools = []
    if "duckduckgo_tool" in agent_config["tools"]:
        tools.append(duckduckgo_tool)
    if "wikipedia_tool" in agent_config["tools"]:
        tools.append(wikipedia_tool)
    if "wolframalpha_tool" in agent_config["tools"]:
        tools.append(wolframalpha_tool)
    if "write_file_tool" in agent_config["tools"]:
        tools.append(write_file_tool)
    if "read_file_tool" in agent_config["tools"]:
        tools.append(read_file_tool)
    if "list_directory_tool" in agent_config["tools"]:
        tools.append(list_directory_tool)
    if "copy_file_tool" in agent_config["tools"]:
        tools.append(copy_file_tool)
    if "delete_file_tool" in agent_config["tools"]:
        tools.append(delete_file_tool)
    if "file_search_tool" in agent_config["tools"]:
        tools.append(file_search_tool)
    if "move_file_tool" in agent_config["tools"]:
        tools.append(move_file_tool)
    if "scrape_tool" in agent_config["tools"]:
        tools.append(scrape_tool)
    
    return Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        verbose=agent_config["verbose"],
        allow_delegation=agent_config["allow_delegation"],
        tools=tools
    )

def create_task(task_config: Dict[str, Any], agent: Agent) -> Task:
    """Create a Task instance from a configuration dictionary and an agent."""
    return Task(
        description=task_config["description"],
        expected_output=task_config["expected_output"],
        agent=agent
    )

def create_squad(squad_config: Dict[str, Any], agents: Dict[str, Agent], tasks: list[Task]) -> Squad:
    """Create a Squad instance from a configuration dictionary, agents, and tasks."""
    squad_agents = [agents[role] for role in squad_config["agents"]]

    manager = None
    if squad_config["process"] == "hierarchical":
        manager = Agent(
            role="Project Manager",
            goal="Efficiently manage the squad and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success.",
            allow_delegation=True,
            verbose=True
        )

    return Squad(
        name=squad_config["name"],
        agents=squad_agents,
        tasks=tasks,
        process=Process.sequential if squad_config["process"] == "sequential" else Process.hierarchical,
        memory=True,
        embedder={
            "provider": "cohere",
            "config": {
                "model": "embed-english-v3.0",
                "vector_dimension": 1024
            }
        },
        verbose=squad_config["verbose"],
        manager_agent=manager
    )

def run_squad(config: Dict[str, Any], user_prompt: str) -> str:
    """Run the squad based on the configuration."""
    agents = {agent_config["role"]: create_agent(agent_config) for agent_config in config["agents"]}
    tasks = [create_task(task_config, agents[task_config["agent"]]) for task_config in config["tasks"]]
    squad = create_squad(config["squad"], agents, tasks)

    result = squad.kickoff()
    return f"Squad '{squad.name}' result: {result}"

def main():
    user_prompt = input("Enter your goal for squadAI: ")
    try:
        config = get_squad_config(user_prompt)
        result = run_squad(config, user_prompt)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again with a different prompt or check your configuration.")

if __name__ == "__main__":
    main()
