import os
from typing_extensions import TypedDict

class SaveFileState(TypedDict):
    code_with_comment: list
    py_file_path: str | None
    folder_path: str  # Required for saving into the correct folder

def save_py_agent(state: SaveFileState):
    code = state["code_with_comment"][-1]["content"]

    folder_path = state["folder_path"]
    folder_name = os.path.basename(folder_path)
    file_path = os.path.join(folder_path, f"{folder_name}.py")

    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

    with open(file_path, "w") as f:
        f.write(code)

    return {"py_file_path": file_path}
