#!/usr/bin/env python
import sys
from {{folder_name}}.squad import {{squad_name}}Squad

# This main file is intended to be a way for your to run your
# squad locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the squad.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    {{squad_name}}Squad().squad().kickoff(inputs=inputs)


def train():
    """
    Train the squad for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        {{squad_name}}Squad().squad().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the squad: {e}")

def replay():
    """
    Replay the squad execution from a specific task.
    """
    try:
        {{squad_name}}Squad().squad().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the squad: {e}")

def test():
    """
    Test the squad execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        {{squad_name}}Squad().squad().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the squad: {e}")
