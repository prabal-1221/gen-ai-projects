import os
from typing_extensions import TypedDict
import uuid

class FolderState(TypedDict):
    folder_path: str | None

# Node: create a unique folder
def create_folder_node(state: FolderState):
    base_dir = "temp"
    os.makedirs(base_dir, exist_ok=True)
    folder_name = f"project_{uuid.uuid4().hex[:8]}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    state["folder_path"] = folder_path
    return state