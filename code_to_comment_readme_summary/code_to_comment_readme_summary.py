import streamlit as st
import os
from langgraph_components.graph_builder import build_graph

@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

st.title("🧠 Python Code Comment & README Generator")

if "py_file_path" not in st.session_state:
    st.session_state["py_file_path"] = None
if "md_file_path" not in st.session_state:
    st.session_state["md_file_path"] = None

# Form section
with st.form("code_form"):
    uploaded = st.file_uploader("Upload .py file", type="py", key="code_file_uploader")
    submitted = st.form_submit_button("Generate")

    if submitted and uploaded:
        os.makedirs("temp", exist_ok=True)
        temp_path = os.path.join("temp", uploaded.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())
        with open(temp_path, "r") as f:
            code = f.read()

        state = {"messages": [{"role": "user", "content": code}]}

        with st.spinner("Generating comments and README..."):
            result = graph.invoke(state)

        st.session_state["commented_code"] = result["code_with_comment"][-1]["content"]
        st.session_state["readme_md"] = result["readme_file"][-1]["content"]
        st.session_state["py_file_path"] = result["py_file_path"]
        st.session_state["md_file_path"] = result["md_file_path"]


# Display commented code
if st.session_state.get("py_file_path"):
    with st.expander("🔍 View Commented Code", expanded=False):
        st.subheader("📝 Commented Code")
        st.code(st.session_state["commented_code"], language="python")

# Display README
if st.session_state.get("md_file_path"):
    with st.expander("📘 View Generated README", expanded=False):
        st.subheader("📄 Generated README")
        st.markdown(st.session_state["readme_md"])

# Download buttons at the bottom
if st.session_state.get("py_file_path") or st.session_state.get("md_file_path"):
    st.markdown("---")  # separator line
    st.subheader("📥 Download Your Files")

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.get("py_file_path"):
            with open(st.session_state["py_file_path"], "rb") as f:
                st.download_button(
                    label="Download Commented Code (.py)",
                    data=f,
                    file_name=os.path.basename(st.session_state["py_file_path"]),
                    mime="text/x-python"
                )

    with col2:
        if st.session_state.get("md_file_path"):
            with open(st.session_state["md_file_path"], "rb") as f:
                st.download_button(
                    label="Download README (.md)",
                    data=f,
                    file_name=os.path.basename(st.session_state["md_file_path"]),
                    mime="text/markdown"
                )
