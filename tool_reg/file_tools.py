# tool_reg/file_tools.py

import os
from . import tool_registry  # Import the singleton instance
from langchain_community.tools.file_management import (
    ReadFileTool,
    WriteFileTool,
    ListDirectoryTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    FileSearchTool
)

# Define the root directory and workspace
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from tool_reg
WORKSPACE_DIR = os.path.join(ROOT_DIR, "Workspace")

# Ensure the Workspace directory exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def init_read_file():
    return ReadFileTool(root_dir=WORKSPACE_DIR, description="Read the contents of a file in the Workspace directory.")

def init_write_file():
    return WriteFileTool(root_dir=WORKSPACE_DIR, description="Write content to a file in the Workspace directory.")

def init_list_directory():
    return ListDirectoryTool(root_dir=WORKSPACE_DIR, description="List files and directories in the Workspace directory.")

def init_copy_file():
    return CopyFileTool(root_dir=WORKSPACE_DIR, description="Copy a file within the Workspace directory.")

def init_delete_file():
    return DeleteFileTool(root_dir=WORKSPACE_DIR, description="Delete a file from the Workspace directory.")

def init_file_search():
    return FileSearchTool(root_dir=WORKSPACE_DIR, description="Search for files in the Workspace directory.")

def init_move_file():
    return MoveFileTool(root_dir=WORKSPACE_DIR, description="Move a file within the Workspace directory.")

tool_registry.register("read_file", init_read_file)
tool_registry.register("write_file", init_write_file)
tool_registry.register("list_directory", init_list_directory)
tool_registry.register("copy_file", init_copy_file)
tool_registry.register("delete_file", init_delete_file)
tool_registry.register("file_search", init_file_search)
tool_registry.register("move_file", init_move_file)
