import streamlit as st
import os
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated

# Load environment variables
load_dotenv()

# Initialize LLM
llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai"
)

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    code: str | None
    readme: str | None
    summary: str | None

# Define the main node
def generate_all_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
        "content":
        """
            You are a technical assistant AI tasked with generating structured documentation and annotated code from a given Python codebase.
            When provided with source code, you MUST generate an output in the exact format described below. Any deviation from this structure will cause parsing failures in downstream systems. You are NOT allowed to add extra commentary, headers, or content outside the strictly defined sections.
            Your response MUST contain exactly three sections, clearly separated by the delimiters below, and in the exact order shown:
            ```
            ===START_CODE_WITH_COMMENTS===
            [Insert the original code with helpful inline comments. Use block or inline comments where appropriate. DO NOT rewrite or modify the code logic.]
            ===END_CODE_WITH_COMMENTS===

            ===START_README===
            [Insert a well-formatted README.md document.]
            ===END_README===

            ===START_SUMMARY===
            [Insert a concise summary of the code’s purpose, functionality, and design approach.]
            ===END_SUMMARY===
            ```
            CRITICAL FORMAT RULES:
            - Do NOT include anything before or after the three sections.
            - Use only the delimiter lines shown above — no extra spacing, indentation, or variation.
            - Do NOT hallucinate or fabricate functionality not present in the code.
            - Output must be deterministic and consistently structured for reliable parsing.

            README GENERATION SPECIFICATIONS:
            - Start with a clear **project title** and a **one-line summary**.
            - Include the following sections, in this order:
            - **Overview**
                - **Features**
                - **Usage**
                - **Inputs / Outputs**
                - **Requirements**
                - **Notes**
                - Use proper Markdown formatting (e.g., `#`, `##`, backticks).
                - Maintain a clear, concise, developer-friendly tone.
                This formatting is mandatory. Non-compliance will break integration pipelines.
        """
        },
        {
            "role": "user",
            "content": last_message.content
        }
    ]

    reply = llm.invoke(messages)
    split_lines = reply.content.split('\n')

    idx_start_code = split_lines.index("===START_CODE_WITH_COMMENTS===")
    idx_end_code = split_lines.index("===END_CODE_WITH_COMMENTS===")
    idx_start_readme = split_lines.index("===START_README===")
    idx_end_readme = split_lines.index("===END_README===")
    idx_start_summary = split_lines.index("===START_SUMMARY===")
    idx_end_summary = split_lines.index("===END_SUMMARY===") or -1

    code = "\n".join(split_lines[idx_start_code+1: idx_end_code])
    readme = "\n".join(split_lines[idx_start_readme+1: idx_end_readme])
    summary = "\n".join(split_lines[idx_start_summary+1: idx_end_summary])

    return {"code": [{"role": "assistant", "content": code}], "readme": [{"role": "assistant", "content": readme}], "summary": [{"role": "assistant", "content": summary}]}

# Build the LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("generate_all_agent", generate_all_agent)
graph_builder.add_edge(START, "generate_all_agent")
graph_builder.add_edge("generate_all_agent", END)
graph = graph_builder.compile()

# Streamlit UI
st.title("📄 Python Code Documentation Assistant")

uploaded_file = st.file_uploader("Upload a Python (.py) file", type=["py"])

if uploaded_file:
    code_text = uploaded_file.read().decode("utf-8")
    with st.expander("🧾 Oriiginal Code", expanded=False):
        st.code(code_text, language="python")

    # Only invoke the LLM if it's a new upload or not cached
    if "doc_result" not in st.session_state or st.session_state.get("last_code") != code_text:
        with st.spinner("Generating documentation..."):
            state = {"messages": [{"role": "user", "content": code_text}]}
            result = graph.invoke(state)
            st.session_state.doc_result = result
            st.session_state.last_code = code_text
    else:
        result = st.session_state.doc_result

    st.success("Documentation generated!")

    with st.expander("🧠 Code with Comments", expanded=False):
        st.code(result['code'][-1]["content"], language='python')

    with st.expander("📘 README.md", expanded=False):
        st.markdown(result['readme'][-1]["content"])

    with st.expander("📝 Summary", expanded=False):
        st.markdown(result['summary'][-1]["content"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="⬇️ Commented Code",
            data=result['code'][-1]["content"],
            file_name="commented_code.py",
            mime="text/x-python"
        )

    with col2:
        st.download_button(
            label="⬇️ README.md",
            data=result['readme'][-1]["content"],
            file_name="README.md",
            mime="text/markdown"
        )

    with col3:
        st.download_button(
            label="⬇️ Summary",
            data=result['summary'][-1]["content"],
            file_name="summary.md",
            mime="text/markdown"
        )
