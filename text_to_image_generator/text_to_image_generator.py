import streamlit as st # Import the Streamlit library for creating web applications.
import requests, io # Import requests for making HTTP requests and io for handling byte streams.
from PIL import Image # Import Image from Pillow (PIL) to open and manipulate images.
from dotenv import load_dotenv # Import load_dotenv to load environment variables from a .env file.
import os # Import the os module to interact with the operating system, specifically for environment variables.

# Load environment variables from the .env file.
# This ensures that sensitive information like API keys are not hardcoded directly into the script.
load_dotenv()
CLIP_KEY = os.getenv("CLIPDROP_KEY") # Retrieve the ClipDrop API key from the loaded environment variables.

# Set the title of the Streamlit application that will be displayed on the web page.
st.title("🖼️ Free Text→Image with ClipDrop")

def generate_clipdrop(prompt):
    """
    Makes a POST request to the ClipDrop Text-to-Image API to generate an image.

    Args:
        prompt (str): The text description (prompt) for the image to be generated.

    Returns:
        PIL.Image.Image: An image object loaded from the API response content.

    Raises:
        requests.exceptions.HTTPError: If the API response indicates an error (e.g., bad status code).
        Exception: For other potential errors during the request or image processing.
    """
    resp = requests.post(
        "https://clipdrop-api.co/text-to-image/v1", # The API endpoint for text-to-image generation.
        headers={"x-api-key": CLIP_KEY}, # Set the API key in the request headers for authentication.
        # 'files' is used because the API expects the prompt as a file-like object,
        # even though it's just text. (None, prompt) means no filename and just the prompt string.
        files={"prompt": (None, prompt)},
        timeout=60 # Set a timeout for the request to prevent it from hanging indefinitely.
    )
    resp.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx status codes).
    # Open the image from the raw byte content of the response.
    # io.BytesIO creates an in-memory binary stream from the response content.
    return Image.open(io.BytesIO(resp.content))

def run():
    # Create a text input field in the Streamlit application for the user to enter their prompt.
    prompt = st.text_input("Prompt:")

    # Create a button in the Streamlit application.
    # The code inside the 'if' block will execute only when this button is clicked.
    if st.button("Generate"):
        # Display a spinner with a message while the image is being generated.
        # This provides visual feedback to the user during the potentially long API call.
        with st.spinner("Generating... (uses 1 free credit)"):
            try:
                # Call the function to generate the image using the user's prompt.
                img = generate_clipdrop(prompt)
                # Display the generated image in the Streamlit application.
                # 'caption' adds text below the image, and 'use_container_width=True' makes the image responsive.
                st.image(img, caption=prompt, use_container_width=True)
            except requests.exceptions.HTTPError as e:
                # Catch specific HTTP errors from the API and display a user-friendly error message
                # including the status code and response text from the API.
                st.error(f"API Error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                # Catch any other general exceptions that might occur and display a generic error message.
                st.error(f"Error: {e}")

if __name__=="__main__":
    run()