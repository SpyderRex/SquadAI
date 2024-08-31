import json
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from squadai.tasks.output_format import OutputFormat
from squadai.tasks.task_output import TaskOutput
from squadai.types.usage_metrics import UsageMetrics


class SquadOutput(BaseModel):
    """Class that represents the result of a squad."""

    raw: str = Field(description="Raw output of squad", default="")
    pydantic: Optional[BaseModel] = Field(
        description="Pydantic output of Squad", default=None
    )
    json_dict: Optional[Dict[str, Any]] = Field(
        description="JSON dict output of Squad", default=None
    )
    tasks_output: list[TaskOutput] = Field(
        description="Output of each task", default=[]
    )
    token_usage: UsageMetrics = Field(description="Processed token summary", default={})

    @property
    def json(self) -> Optional[str]:
        if self.tasks_output[-1].output_format != OutputFormat.JSON:
            raise ValueError(
                "No JSON output found in the final task. Please make sure to set the output_json property in the final task in your squad."
            )

        return json.dumps(self.json_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert json_output and pydantic_output to a dictionary."""
        output_dict = {}
        if self.json_dict:
            output_dict.update(self.json_dict)
        elif self.pydantic:
            output_dict.update(self.pydantic.model_dump())
        return output_dict

    def __str__(self):
        if self.pydantic:
            return str(self.pydantic)
        if self.json_dict:
            return str(self.json_dict)
        return self.raw
