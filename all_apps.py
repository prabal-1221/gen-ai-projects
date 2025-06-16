import streamlit as st

st.set_page_config(page_title="Multi-App Dashboard", layout="wide")

# Sidebar navigation
app_choice = st.sidebar.radio("All the Apps", ["Home", "Basic Text Generator", "AI Story Generator", "Text to Image Generator", "Knowledge Based Chatbot"])

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

    st.markdown("---")

    st.subheader("🎨 Free Text → Image Generator")
    st.write("""
    Turn your imagination into visuals using the ClipDrop Text-to-Image API. 
    This interactive app lets you generate AI-powered images from any text prompt, 
    offering a seamless and creative experience powered by Streamlit, Pillow, and secure API integration.
    """)

    st.markdown("---")
    
    st.subheader("📄 PDF Knowledge Base (RAG-powered)")
    st.write("""
    Ask questions directly from your PDFs using a Retrieval Augmented Generation (RAG) pipeline. 
    This smart app processes any uploaded PDF and gives fact-based answers grounded strictly in the document’s content, 
    powered by Cohere embeddings, vector search, and real-time streaming with LangChain and Streamlit.
    """)



# AI Story Generator App
elif app_choice == "AI Story Generator":
    from ai_story_generator import ai_story_generator
    ai_story_generator.run()

# Basic Text Generator App
elif app_choice == "Basic Text Generator":
    from basic_text_generator import basic_text_generator
    basic_text_generator.run()

# Text to Image Generator App
elif app_choice == "Text to Image Generator":
    from text_to_image_generator import text_to_image_generator
    text_to_image_generator.run()

# Knowledge Based Chatbot App
elif app_choice == "Knowledge Based Chatbot App":
    from knowledge_based_chatbot import knowledge_based_chatbot
    knowledge_based_chatbot.run()