from langchain_cohere import ChatCohere # Import ChatCohere for interacting with Cohere's language models.
from langchain_core.prompts import PromptTemplate # Import PromptTemplate to define the structure of prompts.
from dotenv import load_dotenv # Import load_dotenv to load environment variables from a .env file.
import os # Import the os module to access environment variables.
import streamlit as st # Import streamlit for creating the web application UI.

# Load environment variables from the .env file.
# This is crucial for securely loading the COHERE_API_KEY without hardcoding it.
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY") # Retrieve the Cohere API key from environment variables.

# Decorator to cache the resource. This ensures that the LLM chain is initialized only once
# when the application starts, improving performance and avoiding redundant calls to Cohere.
@st.cache_resource()
def intialize_llm_chain():
    """
    Initializes and returns a LangChain LLM (Large Language Model) chain.
    The chain consists of a Cohere model and a prompt template.
    """
    # Initialize the ChatCohere model.
    # 'command-r-plus' is specified as the model.
    # 'temperature=0.5' controls the creativity of the model's responses (lower means more deterministic).
    llm = ChatCohere(model='command-r-plus', temperature=0.5)

    # Define a prompt template.
    # The '{topic}' is a placeholder that will be filled with the user's input.
    prompt = PromptTemplate.from_template("Write a joke about {topic}")

    # Create an LLM chain by piping the prompt template to the language model.
    # This means the prompt will be formatted, then sent to the LLM.
    chain = prompt | llm
    return chain

def generate_response(chain, topic):
    """
    Generates a joke using the initialized LLM chain and the provided topic.

    Args:
        chain: The LangChain LLM chain ready to invoke.
        topic: The topic for which to generate a joke.

    Returns:
        The content of the generated joke as a string.
    """
    # Invoke the LLM chain with the given topic.
    # The 'invoke' method sends the formatted prompt to the LLM and gets a response.
    output = chain.invoke({"topic": topic})
    return output.content # Return only the text content of the LLM's output.

def run():
    # Initialize the LLM chain globally when the script runs.
    # This uses the cached function, so it's efficient.
    chain = intialize_llm_chain()

    # Set the title of the Streamlit application.
    st.title("Jokes Generator")

    # Create a Streamlit form for user input.
    # Using a form helps in grouping input widgets and processing them on submission.
    with st.form("topic_form"): # Assign a unique key to the form.
        # Text input field for the user to enter a topic.
        topic = st.text_input("Enter a topic: ", key="topic_input") # Assign a unique key to the text input.

        # Submit button for the form.
        submit_btn = st.form_submit_button("Generate")

        # Check if the submit button was clicked.
        if submit_btn:
            # Use a try-except block for error handling, especially for API calls.
            try:
                # Generate the joke using the chain and the user-provided topic.
                joke = generate_response(chain, topic)
                # Display the generated joke in the Streamlit app.
                st.write(joke)
            except Exception as e:
                # If an error occurs during joke generation (e.g., API issues), display an error message.
                st.error(f"Error: {e}")

if __name__ == "__main__":
    run()