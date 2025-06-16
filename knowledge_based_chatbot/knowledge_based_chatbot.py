import streamlit as st # Import the Streamlit library for creating web applications.
from langchain.text_splitter import RecursiveCharacterTextSplitter # For splitting documents into manageable chunks.
from langchain.embeddings import CohereEmbeddings # For converting text into numerical vector embeddings using Cohere.
from langchain.vectorstores import Chroma # For storing and querying vector embeddings (a vector database).
from langchain_cohere import ChatCohere # For interacting with Cohere's large language models.
from langchain.prompts import PromptTemplate # For defining structured prompts for the LLM.
from langchain.document_loaders import PyPDFLoader # For loading PDF documents.
import os # For interacting with the operating system, e.g., creating directories and managing file paths.
from dotenv import load_dotenv # For loading environment variables from a .env file.

# Load environment variables from the .env file.
# This is essential for securely accessing API keys without hardcoding them.
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY") # Retrieve the Cohere API key from environment variables.

# Decorator to cache the data. This ensures that the PDF loading and splitting
# process runs only once per unique PDF upload, improving performance.
# 'show_spinner' provides user feedback during this potentially long operation.
# 'max_entries' limits the cache size to prevent excessive memory usage.
@st.cache_data(show_spinner="Splitting PDF…", max_entries=10)
def load_and_split(path):
    """
    Loads a PDF document from a given path and splits it into smaller,
    manageable text chunks (documents).

    Args:
        path (str): The file path to the PDF document.

    Returns:
        list: A list of LangChain Document objects, each representing a text chunk.
    """
    loader = PyPDFLoader(path) # Initialize a PDF loader with the document path.
    docs = loader.load() # Load the entire PDF content as a list of documents (usually one per page).
    # Initialize a text splitter to break down large documents.
    # 'chunk_size' defines the maximum size of each chunk.
    # 'chunk_overlap' defines how much overlap there should be between consecutive chunks,
    # helping to maintain context across splits.
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs) # Split the loaded documents into smaller chunks.

# Decorator to cache the resource. This ensures the vector store is built
# and initialized only once per set of unique documents, saving computation.
@st.cache_resource(show_spinner="Building vectorstore…")
def get_vectorstore(_docs):
    """
    Creates and returns a Chroma vector store from a list of documents.
    The documents are converted into embeddings using Cohere's embedding model.

    Args:
        _docs (list): A list of LangChain Document objects (text chunks).

    Returns:
        Chroma: An initialized Chroma vector store.
    """
    # Initialize Cohere Embeddings model.
    # 'model' specifies the embedding model to use.
    # 'user_agent' is a custom identifier for API requests, useful for tracking.
    embeddings = CohereEmbeddings(
        model="embed-english-light-v3.0",
        user_agent="streamlit-rag-app"
    )
    # Create a Chroma vector store from the documents and the embeddings model.
    # This process embeds the text chunks and stores them in the vector database.
    return Chroma.from_documents(_docs, embeddings)

# Decorator to cache the resource. This ensures the LLM and prompt chain
# are initialized only once, improving efficiency.
@st.cache_resource(show_spinner="Initializing LLM…")
def get_chain():
    """
    Initializes and returns a LangChain processing chain for answering queries.
    The chain consists of a Cohere Chat model and a prompt template for RAG (Retrieval Augmented Generation).

    Returns:
        langchain.chains.base.Chain: A LangChain chain ready to process queries.
    """
    # Initialize the Cohere Chat model.
    # 'model' specifies the LLM to use.
    # 'temperature' controls the randomness of the output (0.1 means less creative, more factual).
    # 'streaming=True' enables streaming responses, which is good for user experience in web apps.
    llm = ChatCohere(model="command-r-plus", temperature=0.1, streaming=True)
    # Define the prompt template for RAG.
    # It explicitly includes placeholders for 'context' (retrieved from the vector store)
    # and 'query' (user's question).
    prompt = PromptTemplate.from_template("""
        Answer based only on context. If not found, say "I couldn't find the answer in the given context".

        Context: {context}
        Query: {query}
    """)
    # Create the chain by piping the prompt to the LLM.
    # This means the prompt will be formatted with context and query, then sent to the LLM.
    return prompt | llm

def run():
    """
    Main function to run the Streamlit PDF Knowledge Base application.
    Handles PDF uploading, processing, query input, and displaying answers.
    """
    st.title("📚 PDF Knowledge Base") # Set the title of the Streamlit app.

    uploaded = st.file_uploader("Upload PDF:", type="pdf") # Create a file uploader widget for PDFs.
    if not uploaded:
        return # If no PDF is uploaded, stop execution.

    # Define a temporary directory to save the uploaded PDF.
    pdf_path = os.path.join("temp", uploaded.name)
    os.makedirs("temp", exist_ok=True) # Create the 'temp' directory if it doesn't exist.

    # Save the uploaded PDF file to the temporary directory.
    with open(pdf_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Load and split the PDF into documents (chunks). This function is cached.
    docs = load_and_split(pdf_path)
    # Get or build the vector store from the document chunks. This function is cached.
    db = get_vectorstore(docs)
    # Get or initialize the LLM chain. This function is cached.
    chain = get_chain()

    query = st.text_input("Enter your query:") # Create a text input for the user's query.
    if st.button("Search"): # Create a button to trigger the search.
        with st.spinner("Searching…"): # Show a spinner while searching.
            # Perform a similarity search in the vector store to find relevant context documents.
            # 'k=3' means retrieve the top 3 most similar document chunks.
            context_docs = db.similarity_search(query, k=3)
            # Join the content of the retrieved documents into a single string to serve as context for the LLM.
            context_text = "\n\n".join([d.page_content for d in context_docs])
            # Stream the LLM's response to the Streamlit app.
            # The chain takes the user's query and the retrieved context to generate an answer.
            st.write_stream(chain.stream({"query": query, "context": context_text}))

# Entry point of the script.
if __name__ == "__main__":
    run()