from langchain_cohere import ChatCohere
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

@st.cache_resource()
def intialize_llm_chain():
    llm = ChatCohere(model='command-r-plus', temperature=0.5)
    prompt = PromptTemplate.from_template("Write a joke about {topic}")
    chain = prompt | llm
    return chain

def generate_response(chain, topic):
    output = chain.invoke({"topic": topic})
    return output.content

chain = intialize_llm_chain()
st.title("Jokes Generator")
with st.form("topic"):
    topic = st.text_input("Enter a topic: ")
    submit_btn = st.form_submit_button("Generate")
    if submit_btn:
        try:
            joke = generate_response(chain, topic)
            st.write(joke)
        except Exception as e:
            st.error(f"Error: {e}")