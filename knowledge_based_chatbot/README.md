# **📚 PDF Knowledge Base**

A Streamlit web application that transforms your PDF documents into an interactive knowledge base. Upload a PDF, ask questions about its content, and get AI-powered answers based *only* on the provided document. This application leverages advanced Retrieval Augmented Generation (RAG) techniques using LangChain and Cohere.

## **Features**

* **PDF Upload & Processing**: Easily upload PDF documents for analysis.  
* **Intelligent Document Chunking**: Automatically splits large PDFs into manageable text chunks for efficient processing.  
* **Vector Database Integration**: Builds a vector store (Chroma DB) from your PDF content, enabling semantic search.  
* **AI-Powered Question Answering (RAG)**: Uses Cohere's command-r-plus Large Language Model to answer queries based on the context retrieved from your uploaded PDF.  
* **Context-Aware Responses**: Ensures answers are strictly derived from the document's content, with a clear indication if information is not found.  
* **Performance Optimization**: Utilizes Streamlit's caching mechanisms for fast PDF processing and LLM initialization.  
* **Secure API Key Handling**: Manages API keys securely via environment variables.

## **Prerequisites**

Before running this application, ensure you have the following:

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
   pip install streamlit langchain langchain-cohere pypdf chromadb python-dotenv

## **Environment Variables**

Create a file named .env in the root directory of your project (the same directory as your Python script) and add your Cohere API key:

COHERE\_API\_KEY="YOUR\_COHERE\_API\_KEY\_HERE"

**Replace YOUR\_COHERE\_API\_KEY\_HERE with your actual Cohere API key.**

## **Usage**

1. **Run the Streamlit application:**  
   streamlit run your\_script\_name.py

   (Replace your\_script\_name.py with the actual name of your Python file, e.g., app.py)  
2. This command will open the application in your default web browser.  
3. **Upload a PDF file** using the "Upload PDF:" file uploader.  
4. Once the PDF is processed (spinners will indicate progress), **enter your query** in the text input field.  
5. Click the **"Search"** button to get an answer generated from the content of your uploaded PDF.

## **How it Works (Retrieval Augmented Generation \- RAG)**

This application implements a basic RAG pipeline:

1. **Loading & Splitting**: The uploaded PDF is loaded and broken down into smaller, overlapping text chunks.  
2. **Embedding & Vector Store**: These text chunks are converted into numerical representations (embeddings) using Cohere's embed-english-light-v3.0 model and stored in a local vector database (Chroma DB).  
3. **Retrieval**: When a user asks a query, the most semantically similar chunks from the vector store are retrieved. These chunks form the "context."  
4. **Generation**: The retrieved context and the user's query are then passed to a Cohere command-r-plus Large Language Model. The LLM generates an answer, instructed to rely *only* on the provided context.

## **Error Handling**

The application includes basic error handling for file operations and API interactions, displaying messages to the user if issues occur during the process.