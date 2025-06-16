# **Story Generator**

This is a simple web application built with Streamlit and LangChain, powered by Cohere's command-r-plus model, to generate creative stories based on an opening sentence provided by the user.

## **Features**

* **Custom Opening Sentence**: Users can provide any starting sentence.  
* **Creativity Control**: Adjust the story's creativity using a temperature slider (0.0 to 1.0).  
* **Streaming Output**: Watch the story unfold in real-time as it's generated.  
* **User-Friendly Interface**: Built with Streamlit for a simple and intuitive experience.

## **Technologies Used**

* **Python 3.x**  
* **Streamlit**: For building the interactive web UI.  
* **LangChain**: For orchestrating the LLM calls and prompt management.  
* **Cohere API**: As the underlying Large Language Model (command-r-plus).  
* **python-dotenv**: For managing environment variables securely.

## **Setup Instructions**

Follow these steps to get the Story Generator running on your local machine.

### **1\. Clone the Repository (or create the files)**

If you have a repository, clone it:

git clone \<your-repo-url\>  
cd story-generator

If you are creating files manually, create a folder named story-generator and navigate into it.

### **2\. Create a Virtual Environment**

It's recommended to use a virtual environment to manage dependencies:

python \-m venv venv  
source venv/bin/activate  \# On macOS/Linux  
\# venv\\Scripts\\activate   \# On Windows

### **3\. Install Dependencies**

Install the required Python packages:

pip install streamlit langchain-cohere python-dotenv

### **4\. Obtain Cohere API Key**

You will need a Cohere API key.

1. Go to the [Cohere website](https://cohere.com/) and sign up or log in.  
2. Navigate to your API keys section and generate a new API key.

### **5\. Configure Environment Variable**

Create a file named .env in the root directory of your project (the same directory as your Python script) and add your Cohere API key to it:

COHERE\_API\_KEY="your\_cohere\_api\_key\_here"

**Important**: Replace "your\_cohere\_api\_key\_here" with the actual API key you obtained from Cohere. Make sure to keep this file out of version control (e.g., add .env to your .gitignore file).

### **6\. Run the Application**

Now you can run the Streamlit application:

streamlit run your\_script\_name.py

(Replace your\_script\_name.py with the actual name of your Python script, e.g., app.py or story\_generator.py).

The application will open in your web browser, usually at http://localhost:8501.

## **Usage**

1. Enter an **opening sentence** in the provided text box.  
2. Adjust the **creativity slider** to control how imaginative the story should be (0.0 for least creative, 1.0 for most creative).  
3. Click the **"Generate"** button.  
4. Watch as your story is streamed live on the screen\!

## **Troubleshooting**

* **COHERE\_API\_KEY not found error**: Ensure you have created the .env file correctly and placed your API key inside it. Also, verify that load\_dotenv() is called at the beginning of your script.  
* **Network issues**: Check your internet connection, as the application needs to communicate with the Cohere API.  
* **Other errors**: Review the error messages in your terminal for more specific guidance.