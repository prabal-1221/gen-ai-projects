import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

from .nodes.comment_node import get_comment_node
from .nodes.save_py_node import save_py_agent
from .nodes.readme_node import get_readme_node
from .nodes.save_readme_node import save_readme_agent
from .nodes.summary_node import get_summary_node  # <-- new
from .nodes.save_summary_node import save_summary_agent  # <-- new
from .nodes.folder_node import create_folder_node

class FullState(TypedDict):
    messages: Annotated[list, add_messages]
    code_with_comment: str | None
    readme_file: str | None
    summary_file: str | None  # <-- new
    py_file_path: str | None
    md_file_path: str | None
    summary_file_path: str | None  # <-- new
    folder_path: str | None


def build_graph():
    load_dotenv()

    llm = init_chat_model(
        "command-r-plus",
        model_provider="cohere",
        api_key=os.getenv("COHERE_API_KEY")
    )

    graph_builder = StateGraph(FullState)

    def splitter_node(state: FullState):
        return state

    # Nodes
    graph_builder.add_node("create_folder", create_folder_node)
    graph_builder.add_node("split", splitter_node)

    graph_builder.add_node("comments_agent", get_comment_node(llm))
    graph_builder.add_node("save_py_agent", save_py_agent)

    graph_builder.add_node("readme_agent", get_readme_node(llm))
    graph_builder.add_node("save_md_agent", save_readme_agent)

    graph_builder.add_node("summary_agent", get_summary_node(llm))  # <-- new
    graph_builder.add_node("save_summary_agent", save_summary_agent)  # <-- new

    # Edges
    graph_builder.add_edge(START, "create_folder")
    graph_builder.add_edge("create_folder", "split")

    # Parallel execution
    graph_builder.add_edge("split", "comments_agent")
    graph_builder.add_edge("split", "readme_agent")
    graph_builder.add_edge("split", "summary_agent")  # <-- new

    graph_builder.add_edge("comments_agent", "save_py_agent")
    graph_builder.add_edge("readme_agent", "save_md_agent")
    graph_builder.add_edge("summary_agent", "save_summary_agent")  # <-- new

    # Merge
    graph_builder.add_edge("save_py_agent", END)
    graph_builder.add_edge("save_md_agent", END)
    graph_builder.add_edge("save_summary_agent", END)  # <-- new

    return graph_builder.compile()
