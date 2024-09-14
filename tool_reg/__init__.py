# tool_reg/__init__.py
from typing import Dict, Callable
from langchain_community.tools import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[[], BaseTool]] = {}
        self._initialized_tools: Dict[str, BaseTool] = {}

    def register(self, name: str, initializer: Callable[[], BaseTool]):
        self._tools[name] = initializer

    def get(self, name: str) -> BaseTool:
        if name not in self._initialized_tools:
            if name not in self._tools:
                raise KeyError(f"Tool '{name}' not found in registry")
            self._initialized_tools[name] = self._tools[name]()
        return self._initialized_tools[name]

    def get_all(self) -> Dict[str, BaseTool]:
        for name in self._tools:
            if name not in self._initialized_tools:
                self._initialized_tools[name] = self._tools[name]()
        return self._initialized_tools

# Create a singleton instance of ToolRegistry
tool_registry = ToolRegistry()
