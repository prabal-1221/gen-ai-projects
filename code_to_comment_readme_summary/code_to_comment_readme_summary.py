import streamlit as st
import os
from langgraph_components.graph_builder import build_graph

st.markdown("""
    <style>
    div.stFileUploader {
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

st.title("🧠 Python Code Comment, README & Summary Generator")

if "folder_path" not in st.session_state:
    st.session_state["folder_path"] = None

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

        with st.spinner("Generating comments, README, and summary..."):
            result = graph.invoke(state)

        folder_path = result["folder_path"]
        folder_name = os.path.basename(folder_path)

        # Read and store file contents
        with open(os.path.join(folder_path, f"{folder_name}.py"), "r") as f:
            st.session_state["commented_code"] = f.read()
        with open(os.path.join(folder_path, "README.md"), "r") as f:
            st.session_state["readme_md"] = f.read()
        with open(os.path.join(folder_path, "summary.md"), "r") as f:
            st.session_state["summary_md"] = f.read()

        st.session_state["folder_path"] = folder_path


# Display Commented Code
if st.session_state.get("commented_code"):
    with st.expander("🔍 View Commented Code", expanded=False):
        st.subheader("📝 Commented Code")
        st.code(st.session_state["commented_code"], language="python")

# Display README
if st.session_state.get("readme_md"):
    with st.expander("📘 View Generated README", expanded=False):
        st.subheader("📄 Generated README")
        st.markdown(st.session_state["readme_md"])

# Display Summary
if st.session_state.get("summary_md"):
    with st.expander("🧾 View Project Summary", expanded=False):
        st.subheader("🧠 Summary")
        st.markdown(st.session_state["summary_md"])


# Download Section
# Download Section
if st.session_state.get("folder_path"):
    st.markdown("---")
    st.subheader("📥 Download Your Files")

    folder_path = st.session_state["folder_path"]
    folder_name = os.path.basename(folder_path)

    col1, col2, col3 = st.columns(3)

    with col1:
        py_path = os.path.join(folder_path, f"{folder_name}.py")
        if os.path.exists(py_path):
            with open(py_path, "rb") as f:
                st.download_button(
                    label="Code (.py)",
                    data=f,
                    file_name=f"{folder_name}.py",
                    mime="text/x-python"
                )
        else:
            st.empty()

    with col2:
        readme_path = os.path.join(folder_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "rb") as f:
                st.download_button(
                    label="README (.md)",
                    data=f,
                    file_name="README.md",
                    mime="text/markdown"
                )
        else:
            st.empty()

    with col3:
        summary_path = os.path.join(folder_path, "summary.md")
        if os.path.exists(summary_path):
            with open(summary_path, "rb") as f:
                st.download_button(
                    label="Summary (.md)",
                    data=f,
                    file_name="summary.md",
                    mime="text/markdown"
                )
        else:
            st.empty()