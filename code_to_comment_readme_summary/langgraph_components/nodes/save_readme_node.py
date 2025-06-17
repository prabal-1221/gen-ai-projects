import os
from typing_extensions import TypedDict

class SaveFileState(TypedDict):
    readme_file: list
    folder_path: str  # Required for saving into the correct folder

def save_readme_agent(state: SaveFileState):
    code = state["readme_file"][-1]["content"]

    folder_path = state["folder_path"]
    file_path = os.path.join(folder_path, "README.md")

    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

    with open(file_path, "w") as f:
        f.write(code)

    return {}
