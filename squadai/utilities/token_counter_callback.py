from typing import Any, Dict, List

import tiktoken
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from squadai.agents.agent_builder.utilities.base_token_process import TokenProcess


class TokenCalcHandler(BaseCallbackHandler):
    model_name: str = ""
    token_cost_process: TokenProcess
    encoding: tiktoken.Encoding

    def __init__(self, model_name, token_cost_process):
        self.model_name = model_name
        self.token_cost_process = token_cost_process
        try:
            self.encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        if self.token_cost_process is None:
            return

        for prompt in prompts:
            self.token_cost_process.sum_prompt_tokens(len(self.encoding.encode(prompt)))

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.token_cost_process.sum_completion_tokens(1)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.token_cost_process.sum_successful_requests(1)
