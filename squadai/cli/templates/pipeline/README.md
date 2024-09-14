# {{squad_name}} Squad

Welcome to the {{squad_name}} Squad project, powered by [squadAI](https://squadai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by squadAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:

```bash
squadai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/{{folder_name}}/config/agents.yaml` to define your agents
- Modify `src/{{folder_name}}/config/tasks.yaml` to define your tasks
- Modify `src/{{folder_name}}/squad.py` to add your own logic, tools and specific args
- Modify `src/{{folder_name}}/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your squad of AI agents and begin task execution, run this from the root folder of your project:

```bash
squadai run
```

This command initializes the {{name}} Squad, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Squad

The {{name}} Squad is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your squad.

## Support

For support, questions, or feedback regarding the {{squad_name}} Squad or squadAI.

- Visit our [documentation](https://docs.squadai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/squadai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of squadAI.
