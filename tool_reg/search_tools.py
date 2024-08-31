# tool_reg/search_tools.py

from . import tool_registry  # Import the singleton instance
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def init_duckduckgo():
    return DuckDuckGoSearchRun()

def init_wikipedia():
    wikipedia_api = WikipediaAPIWrapper()
    return WikipediaQueryRun(api_wrapper=wikipedia_api)

tool_registry.register("duckduckgo", init_duckduckgo)
tool_registry.register("wikipedia", init_wikipedia)
