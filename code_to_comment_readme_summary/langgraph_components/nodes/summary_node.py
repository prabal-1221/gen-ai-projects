from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class SummaryState(TypedDict):
    messages: Annotated[list, add_messages]
    summary_file: str | None

def get_summary_node(llm):
    def summary_agent(state: SummaryState):
        last_message = state["messages"][-1]
        messages = [
            {
                "role": "system",
                "content": """
                    You are a technical writing AI that specializes in summarizing source code functionality for documentation purposes.

                    When provided with source code:
                    1. Analyze the code and produce a concise **summary** explaining what the code does.
                    2. The summary should include:
                    - The overall purpose of the script or project.
                    - Key components or modules and their roles.
                    - A brief explanation of the main logic or flow.
                    - Any important inputs and outputs.
                    - Notable implementation details (e.g., use of specific libraries, structure).
                    3. The summary must be written in clear, technical English suitable for developers.
                    4. Use proper Markdown formatting (`#`, `##`, bullet points, code blocks as needed).
                    5. Do not modify or paraphrase the code itself — your task is to summarize, not refactor.
                    6. Output only a single Markdown document, wrapped in triple backticks with `markdown` specified.
                """
            },
            {
                "role": "user",
                "content": last_message.content
            }
        ]

        reply = llm.invoke(messages)
        split_lines = reply.content.split("\n")[1:-1]
        summary_markdown_string = "\n".join(split_lines)
        return {"summary_file": [{"role": "assistant", "content": summary_markdown_string}]}

    return summary_agent
