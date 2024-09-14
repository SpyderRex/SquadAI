import shutil
from pathlib import Path

import click


def create_pipeline(name, router=False):
    """Create a new pipeline project."""
    folder_name = name.replace(" ", "_").replace("-", "_").lower()
    class_name = name.replace("_", " ").replace("-", " ").title().replace(" ", "")

    click.secho(f"Creating pipeline {folder_name}...", fg="green", bold=True)

    project_root = Path(folder_name)
    if project_root.exists():
        click.secho(f"Error: Folder {folder_name} already exists.", fg="red")
        return

    # Create directory structure
    (project_root / "src" / folder_name).mkdir(parents=True)
    (project_root / "src" / folder_name / "pipelines").mkdir(parents=True)
    (project_root / "src" / folder_name / "squads").mkdir(parents=True)
    (project_root / "src" / folder_name / "tools").mkdir(parents=True)
    (project_root / "tests").mkdir(exist_ok=True)

    # Create .env file
    with open(project_root / ".env", "w") as file:
        file.write("GROQ_API_KEY=YOUR_API_KEY")

    package_dir = Path(__file__).parent
    template_folder = "pipeline_router" if router else "pipeline"
    templates_dir = package_dir / "templates" / template_folder

    # List of template files to copy
    root_template_files = [".gitignore", "pyproject.toml", "README.md"]
    src_template_files = ["__init__.py", "main.py"]
    tools_template_files = ["tools/__init__.py", "tools/custom_tool.py"]

    if router:
        squad_folders = [
            "classifier_squad",
            "normal_squad",
            "urgent_squad",
        ]
        pipelines_folders = [
            "pipelines/__init__.py",
            "pipelines/pipeline_classifier.py",
            "pipelines/pipeline_normal.py",
            "pipelines/pipeline_urgent.py",
        ]
    else:
        squad_folders = [
            "research_squad",
            "write_linkedin_squad",
            "write_x_squad",
        ]
        pipelines_folders = ["pipelines/__init__.py", "pipelines/pipeline.py"]

    def process_file(src_file, dst_file):
        with open(src_file, "r") as file:
            content = file.read()

        content = content.replace("{{name}}", name)
        content = content.replace("{{squad_name}}", class_name)
        content = content.replace("{{folder_name}}", folder_name)
        content = content.replace("{{pipeline_name}}", class_name)

        with open(dst_file, "w") as file:
            file.write(content)

    # Copy and process root template files
    for file_name in root_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / file_name
        process_file(src_file, dst_file)

    # Copy and process src template files
    for file_name in src_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / "src" / folder_name / file_name
        process_file(src_file, dst_file)

    # Copy tools files
    for file_name in tools_template_files:
        src_file = templates_dir / file_name
        dst_file = project_root / "src" / folder_name / file_name
        shutil.copy(src_file, dst_file)

    # Copy pipelines folders
    for file_name in pipelines_folders:
        src_file = templates_dir / file_name
        dst_file = project_root / "src" / folder_name / file_name
        process_file(src_file, dst_file)

    # Copy squad folders
    for squad_folder in squad_folders:
        src_squad_folder = templates_dir / "squads" / squad_folder
        dst_squad_folder = project_root / "src" / folder_name / "squads" / squad_folder
        if src_squad_folder.exists():
            shutil.copytree(src_squad_folder, dst_squad_folder)
        else:
            click.secho(
                f"Warning: Squad folder {squad_folder} not found in template.",
                fg="yellow",
            )

    click.secho(f"Pipeline {name} created successfully!", fg="green", bold=True)
