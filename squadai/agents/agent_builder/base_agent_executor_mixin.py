import time
from typing import TYPE_CHECKING, Optional

from squadai.memory.entity.entity_memory_item import EntityMemoryItem
from squadai.memory.long_term.long_term_memory_item import LongTermMemoryItem
from squadai.utilities.converter import ConverterError
from squadai.utilities.evaluators.task_evaluator import TaskEvaluator
from squadai.utilities import I18N


if TYPE_CHECKING:
    from squadai.squad import Squad
    from squadai.task import Task
    from squadai.agents.agent_builder.base_agent import BaseAgent


class SquadAgentExecutorMixin:
    squad: Optional["Squad"]
    squad_agent: Optional["BaseAgent"]
    task: Optional["Task"]
    iterations: int
    force_answer_max_iterations: int
    have_forced_answer: bool
    _i18n: I18N

    def _should_force_answer(self) -> bool:
        """Determine if a forced answer is required based on iteration count."""
        return (
            self.iterations == self.force_answer_max_iterations
        ) and not self.have_forced_answer

    def _create_short_term_memory(self, output) -> None:
        """Create and save a short-term memory item if conditions are met."""
        if (
            self.squad
            and self.squad_agent
            and self.task
            and "Action: Delegate work to coworker" not in output.log
        ):
            try:
                if (
                    hasattr(self.squad, "_short_term_memory")
                    and self.squad._short_term_memory
                ):
                    self.squad._short_term_memory.save(
                        value=output.log,
                        metadata={
                            "observation": self.task.description,
                        },
                        agent=self.squad_agent.role,
                    )
            except Exception as e:
                print(f"Failed to add to short term memory: {e}")
                pass

    def _create_long_term_memory(self, output) -> None:
        """Create and save long-term and entity memory items based on evaluation."""
        if (
            self.squad
            and self.squad.memory
            and self.squad._long_term_memory
            and self.squad._entity_memory
            and self.task
            and self.squad_agent
        ):
            try:
                ltm_agent = TaskEvaluator(self.squad_agent)
                evaluation = ltm_agent.evaluate(self.task, output.log)

                if isinstance(evaluation, ConverterError):
                    return

                long_term_memory = LongTermMemoryItem(
                    task=self.task.description,
                    agent=self.squad_agent.role,
                    quality=evaluation.quality,
                    datetime=str(time.time()),
                    expected_output=self.task.expected_output,
                    metadata={
                        "suggestions": evaluation.suggestions,
                        "quality": evaluation.quality,
                    },
                )
                self.squad._long_term_memory.save(long_term_memory)

                for entity in evaluation.entities:
                    entity_memory = EntityMemoryItem(
                        name=entity.name,
                        type=entity.type,
                        description=entity.description,
                        relationships="\n".join(
                            [f"- {r}" for r in entity.relationships]
                        ),
                    )
                    self.squad._entity_memory.save(entity_memory)
            except AttributeError as e:
                print(f"Missing attributes for long term memory: {e}")
                pass
            except Exception as e:
                print(f"Failed to add to long term memory: {e}")
                pass

    def _ask_human_input(self, final_answer: dict) -> str:
        """Prompt human input for final decision making."""
        return input(
            self._i18n.slice("getting_input").format(final_answer=final_answer)
        )
