import os
from typing_extensions import TypedDict

class SaveFileState(TypedDict):
    readme_file: list
    md_file_path: str | None
    folder_path: str  # Required for saving into the correct folder

def save_md_agent(state: SaveFileState):
    code = state["readme_file"][-1]["content"]

    folder_path = state["folder_path"]
    folder_name = os.path.basename(folder_path)
    file_path = os.path.join(folder_path, "README.md")

    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

    with open(file_path, "w") as f:
        f.write(code)

    return {"md_file_path": file_path}
