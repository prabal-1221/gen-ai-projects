from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class CommentState(TypedDict):
    messages: Annotated[list, add_messages]
    code_with_comment: str | None

def get_comment_node(llm):
    def comments_agent(state: CommentState):
        last_message = state["messages"][-1]
        messages = [
            {
                "role": "system",
                "content": """
                    You are a skilled coding assistant whose job is to review the provided source code and insert clear, precise comments that explain its purpose, logic, and any non-trivial sections.

                    When you receive code input from the user:
                    1. Add a comment header outlining:
                       - Purpose
                       - Inputs / Outputs
                    2. Inline comment complex logic
                    3. Use # for Python comments
                    4. Maintain clean formatting
                    5. Do not change logic
                    6. Wrap your response in triple backticks
                """
            },
            {
                "role": "user",
                "content": last_message.content
            }
        ]

        reply = llm.invoke(messages)
        split_lines = reply.content.split("\n")[1:-1]
        code = "\n".join(split_lines)
        return {"code_with_comment": [{"role": "assistant", "content": code}]}

    return comments_agent
