# tool_reg/info_tools.py

from . import tool_registry  # Import the singleton instance
from langchain_community.tools import WolframAlphaQueryRun
from langchain_community.utilities import WolframAlphaAPIWrapper
from dotenv import load_dotenv

load_dotenv()

def init_wolframalpha():
    wolframalpha_api = WolframAlphaAPIWrapper()
    return WolframAlphaQueryRun(api_wrapper=wolframalpha_api)

tool_registry.register("wolframalpha", init_wolframalpha)
