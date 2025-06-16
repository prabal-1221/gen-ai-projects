This Streamlit application, the **"PDF Knowledge Base,"** serves as a powerful tool for extracting information from PDF documents using **Retrieval Augmented Generation (RAG)**. It allows users to upload a PDF and then ask questions directly related to its content, with the AI providing answers based *only* on the uploaded document.

**Core Components & Workflow:**

1. **Streamlit (streamlit):** Provides the **user interface**, handling PDF uploads, displaying loading spinners, capturing user queries, and streaming the AI-generated answers back to the user.  
2. **PDF Loading (PyPDFLoader):** Loads the user-uploaded PDF file. The file is temporarily saved to a temp directory for processing.  
3. **Text Splitting (RecursiveCharacterTextSplitter):** Breaks down the loaded PDF content into smaller, manageable **"chunks"** (e.g., 500 characters with 50 characters of overlap). This is crucial for efficient and effective RAG.  
4. **Embeddings (CohereEmbeddings):** Converts these text chunks into **numerical vector representations** (embeddings) using Cohere's embed-english-light-v3.0 model. Embeddings capture the semantic meaning of the text.  
5. **Vector Store (Chroma):** Stores these numerical embeddings in a local vector database. When a user queries, this database is searched to find the most **semantically similar text chunks** from the original PDF.  
6. **Language Model (ChatCohere):** Uses Cohere's command-r-plus model as the core AI for generating answers. It's configured for **streaming responses** (streaming=True) for a better user experience and a low temperature (0.1) for more factual, less creative output.  
7. **Prompt Template (PromptTemplate):** Defines the strict instructions for the LLM. It dictates that the LLM must **answer based *only* on the provided context** (the retrieved relevant chunks from the PDF) and explicitly states what to say if the answer isn't found in that context.  
8. **RAG Pipeline (prompt | llm):** When a user submits a query:  
   * The vectorstore performs a **similarity search** to retrieve the top 3 most relevant text chunks (context) from the uploaded PDF based on the user's query.  
   * This context and the user's query are then fed into the LLM chain (defined by prompt | llm).  
   * The LLM generates an answer, strictly adhering to the prompt's instructions.  
9. **Caching (@st.cache\_data, @st.cache\_resource):** Optimizes performance by caching the PDF loading, text splitting, vector store building, and LLM initialization steps, ensuring they only run once per unique input.  
10. **Environment Variables (python-dotenv):** Securely loads the COHERE\_API\_KEY from a .env file, preventing sensitive data from being exposed in the code.

This architecture ensures that the AI's answers are grounded in the specific content of your PDF, making it a reliable tool for knowledge extraction.