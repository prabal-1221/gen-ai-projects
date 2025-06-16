# Import necessary libraries
from langchain_cohere import ChatCohere  # For interacting with Cohere's chat models
from langchain_core.prompts import PromptTemplate  # For creating prompt templates
from langchain_core.runnables import ConfigurableField  # For making model parameters configurable
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For interacting with the operating system (e.g., getting environment variables)
import streamlit as st  # For building the web application UI

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Cohere API key from environment variables
# It's crucial to set this in your .env file as COHERE_API_KEY="your_api_key_here"
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def intialize_llm_chain():
    """
    Initializes and returns a LangChain LLM chain for story generation.

    The chain consists of:
    1. A PromptTemplate: Defines the structure of the input prompt for the LLM.
    2. A ChatCohere LLM: Uses Cohere's 'command-r-plus' model for text generation.
       The temperature is set to 0.5 by default and is made configurable.
    """
    # Initialize the Cohere chat model
    # 'command-r-plus' is the chosen model.
    # 'temperature' controls creativity (higher = more creative).
    # .configurable_fields() allows Streamlit users to override the temperature from the UI.
    llm = ChatCohere(model='command-r-plus', temperature=0.5, streaming=True).configurable_fields(
        temperature=ConfigurableField(
            id='cohere_temp',  # Unique ID for the configurable field
            name='cohere temperature',  # Display name in the UI (if used with Streamlit's config)
            description="override original temperature"  # Description for the field
        )
    )

    # Define the prompt template for story generation
    # The '{opening_sentence}' placeholder will be replaced by user input.
    prompt = PromptTemplate.from_template("""Based on the opening sentence given generate a creative story. Return only story No Other text.

Opening Sentence: {opening_sentence}""")

    # Create the LangChain expression language chain
    # The prompt's output is piped as input to the LLM.
    chain = prompt | llm
    return chain

def generate_response(chain, opening_sentence, temp=0.5):
    """
    Generates a story using the provided LangChain chain and opening sentence.

    Args:
        chain: The initialized LangChain chain.
        opening_sentence (str): The starting sentence for the story.
        temp (float): The creativity temperature for the LLM (0.0-1.0).

    Returns:
        A stream of responses from the LLM, allowing for real-time display.
    """
    # Use chain.stream() for streaming responses, which improves user experience
    # by showing text as it's generated.
    # The 'config' dictionary is used to pass configurable parameters to the LLM,
    # in this case, overriding the 'cohere_temp' (temperature).
    return chain.stream(
        input={"opening_sentence": opening_sentence},
        config={"configurable": {"cohere_temp": temp}}
    )

# --- Streamlit Application UI ---
def run():
    # Initialize the LLM chain once when the application starts
    # This avoids re-initializing the model on every user interaction.
    chain = intialize_llm_chain()

    # Set the title of the Streamlit application
    st.title("Story Generator")

    # Create a Streamlit form for user input
    # Using a form helps group inputs and only triggers generation on submit.
    with st.form("story"):
        # Text input field for the opening sentence
        opening_sentence = st.text_input("Give an opening sentence: ")

        # Number input for controlling creativity (temperature)
        # Allows users to select a value between 0.0 and 1.0.
        temp = st.number_input(
            "How much creativity you want (0.0 - least creative, 1.0 - most creative): ",
            min_value=0.0,
            max_value=1.0,
            value=0.5  # Default value
        )

        # Submit button for the form
        submit_btn = st.form_submit_button("Generate")

        # Check if the submit button was clicked
        if submit_btn:
            # Ensure an opening sentence is provided
            if not opening_sentence.strip():
                st.error("Please provide an opening sentence to generate a story.")
            else:
                try:
                    # Display a spinner while the story is being generated
                    with st.spinner("Generating story..."):
                        # Call the generate_response function and stream the output to Streamlit
                        st.write_stream(
                            generate_response(chain, opening_sentence, temp)
                        )
                except Exception as e:
                    # Display any errors that occur during generation
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    run()