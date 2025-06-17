from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class ReadmeState(TypedDict):
    messages: Annotated[list, add_messages]
    readme_file: str | None

def get_readme_node(llm):
    def readme_agent(state: ReadmeState):
        last_message = state["messages"][-1]
        messages = [
            {
                "role": "system",
                "content": """
                    You are a technical writer AI tasked with generating a professional and concise `README.md` file for a given codebase.

                    When provided with source code:
                    1. Start with a short **project title** and a **one-line summary** of what the code does.
                    2. Include the following standard sections:
                    - **Overview**: A brief explanation of the code’s purpose and context.
                    - **Features**: Key functionalities or highlights of the script or project.
                    - **Usage**: A clear example or description of how the code can be run or used.
                    - **Inputs / Outputs**: Explain any required inputs (e.g., arguments, files) and what outputs it generates.
                    - **Requirements**: Mention any dependencies, libraries, or environment setup.
                    - **Notes**: Any limitations, edge cases, or areas for improvement (if identifiable).
                    3. Write in a clear and neutral tone suitable for developers.
                    4. Use proper Markdown formatting (e.g., `#`, `##`, backticks for code blocks).
                    5. Do not change or rewrite the code itself — just explain it.
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
        markdown_string = "\n".join(split_lines)
        return {"readme_file": [{"role": "assistant", "content": markdown_string}]}

    return readme_agent
