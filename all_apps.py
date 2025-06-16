import streamlit as st

st.set_page_config(page_title="Multi-App Dashboard", layout="wide")

# Sidebar navigation
app_choice = st.sidebar.radio("All the Apps", ["Home", "Basic Text Generator", "AI Story Generator"])

# Home Page Content
if app_choice == "Home":
    st.title("🚀 Welcome to the Multi-App Dashboard")
    st.write("Use the sidebar to navigate between different Generative AI tools built with Streamlit and LangChain.")

    st.markdown("---")
    
    st.subheader("😄 Basic Text Generator")
    st.write("""
    A fun and interactive app that uses Cohere's AI to generate creative jokes based on any topic you provide.
    Powered by LangChain and Streamlit, it delivers real-time humor with just one click.
    """)
    
    st.markdown("---")

    st.subheader("📖 AI Story Generator")
    st.write("""
    Generate creative and engaging stories from any opening sentence using Cohere's command-r-plus model with real-time streaming and adjustable creativity.
    """)

# AI Story Generator App
elif app_choice == "AI Story Generator":
    from ai_story_generator import ai_story_generator
    ai_story_generator.run()

# Basic Text Generator App (Jokes Generator)
elif app_choice == "Basic Text Generator":
    from basic_text_generator import basic_text_generator
    basic_text_generator.run()