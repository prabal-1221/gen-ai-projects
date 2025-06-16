# **Jokes Generator**

A simple Streamlit web application that uses the Cohere Command R+ large language model via LangChain to generate jokes on a user-specified topic.

## **Features**

* **Interactive UI**: Built with Streamlit for a user-friendly interface.  
* **AI-Powered Joke Generation**: Leverages Cohere's command-r-plus model to create jokes based on input.  
* **LangChain Integration**: Uses LangChain for seamless interaction with the LLM and prompt management.  
* **Environment Variable Support**: Securely loads API keys using python-dotenv.  
* **Resource Caching**: Optimizes performance by caching the LLM chain initialization.

## **Prerequisites**

Before running this application, ensure you have the following installed:

* Python 3.8+  
* A Cohere API Key

## **Installation**

1. **Clone the repository (if applicable) or save the code:**  
   git clone \<repository\_url\>  
   cd \<repository\_directory\> \# If you cloned a repo

   If you just saved the code, navigate to the directory containing your Python script (e.g., app.py).  
2. **Create a virtual environment (recommended):**  
   python \-m venv venv

3. **Activate the virtual environment:**  
   * **On Windows:**  
     .\\venv\\Scripts\\activate

   * **On macOS/Linux:**  
     source venv/bin/activate

4. **Install the required dependencies:**  
   pip install streamlit langchain-cohere python-dotenv

## **Environment Variables**

Create a file named .env in the root directory of your project (the same directory as your Python script) and add your Cohere API key:

COHERE\_API\_KEY="YOUR\_COHERE\_API\_KEY\_HERE"

**Replace YOUR\_COHERE\_API\_KEY\_HERE with your actual Cohere API key.**

## **Usage**

1. **Run the Streamlit application:**  
   streamlit run your\_script\_name.py

   (Replace your\_script\_name.py with the actual name of your Python file, e.g., app.py)  
2. This command will open the application in your default web browser.  
3. **Enter a topic** in the text input field and click the "Generate" button to get a joke\!

## **Error Handling**

The application includes basic error handling to catch exceptions during joke generation (e.g., issues with the Cohere API). If an error occurs, an error message will be displayed in the Streamlit interface.