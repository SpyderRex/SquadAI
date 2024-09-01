import os
from typing import Optional

import click
import pkg_resources
from dotenv import load_dotenv

from squadai.cli.create_squad import create_squad
from squadai.cli.create_pipeline import create_pipeline
from squadai.memory.storage.kickoff_task_outputs_storage import (
    KickoffTaskOutputsSQLiteStorage,
)

from .evaluate_squad import evaluate_squad
from .install_squad import install_squad
from .replay_from_task import replay_task_command
from .reset_memories_command import reset_memories_command
from .run_squad import run_squad
from .train_squad import train_squad

load_dotenv()


@click.group()
def squadai():
    """Top-level command group for squadai."""


@squadai.command()
@click.argument("type", type=click.Choice(["squad", "pipeline"]))
@click.argument("name")
@click.option(
    "--router", is_flag=True, help="Create a pipeline with router functionality"
)
def create(type, name, router):
    """Create a new squad or pipeline."""
    if type == "squad":
        create_squad(name)
    elif type == "pipeline":
        create_pipeline(name, router)
    else:
        click.secho("Error: Invalid type. Must be 'squad' or 'pipeline'.", fg="red")


@squadai.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=5,
    help="Number of iterations to train the squad",
)
@click.option(
    "-f",
    "--filename",
    type=str,
    default="trained_agents_data.pkl",
    help="Path to a custom file for training",
)
def train(n_iterations: int, filename: str):
    """Train the squad."""
    click.echo(f"Training the Squad for {n_iterations} iterations")
    train_squad(n_iterations, filename)


@squadai.command()
@click.option(
    "-t",
    "--task_id",
    type=str,
    help="Replay the squad from this task ID, including all subsequent tasks.",
)
def replay(task_id: str) -> None:
    """
    Replay the squad execution from a specific task.

    Args:
        task_id (str): The ID of the task to replay from.
    """
    try:
        click.echo(f"Replaying the squad from task {task_id}")
        replay_task_command(task_id)
    except Exception as e:
        click.echo(f"An error occurred while replaying: {e}", err=True)


@squadai.command()
def log_tasks_outputs() -> None:
    """
    Retrieve your latest squad.kickoff() task outputs.
    """
    try:
        storage = KickoffTaskOutputsSQLiteStorage()
        tasks = storage.load()

        if not tasks:
            click.echo(
                "No task outputs found. Only squad kickoff task outputs are logged."
            )
            return

        for index, task in enumerate(tasks, 1):
            click.echo(f"Task {index}: {task['task_id']}")
            click.echo(f"Description: {task['expected_output']}")
            click.echo("------")

    except Exception as e:
        click.echo(f"An error occurred while logging task outputs: {e}", err=True)


@squadai.command()
@click.option("-l", "--long", is_flag=True, help="Reset LONG TERM memory")
@click.option("-s", "--short", is_flag=True, help="Reset SHORT TERM memory")
@click.option("-e", "--entities", is_flag=True, help="Reset ENTITIES memory")
@click.option(
    "-k",
    "--kickoff-outputs",
    is_flag=True,
    help="Reset LATEST KICKOFF TASK OUTPUTS",
)
@click.option("-a", "--all", is_flag=True, help="Reset ALL memories")
def reset_memories(long, short, entities, kickoff_outputs, all):
    """
    Reset the squad memories (long, short, entity, latest_squad_kickoff_ouputs). This will delete all the data saved.
    """
    try:
        if not all and not (long or short or entities or kickoff_outputs):
            click.echo(
                "Please specify at least one memory type to reset using the appropriate flags."
            )
            return
        reset_memories_command(long, short, entities, kickoff_outputs, all)
    except Exception as e:
        click.echo(f"An error occurred while resetting memories: {e}", err=True)


@squadai.command()
@click.option(
    "-n",
    "--n_iterations",
    type=int,
    default=3,
    help="Number of iterations to Test the squad",
)
@click.option(
    "-m",
    "--model",
    type=str,
    default=os.getenv("GROQ_MODEL_NAME"),
    help="LLM Model to run the tests on the Squad. For now only accepting only Llama model.",
)
def test(n_iterations: int, model: str):
    """Test the squad and evaluate the results."""
    click.echo(f"Testing the squad for {n_iterations} iterations with model {model}")
    evaluate_squad(n_iterations, model)


@squadai.command()
def install():
    """Install the Squad."""
    install_squad()


@squadai.command()
def run():
    """Run the Squad."""
    click.echo("Running the Squad")
    run_squad()


if __name__ == "__main__":
    squadai()
