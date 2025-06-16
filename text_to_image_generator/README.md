# **🖼️ Free Text→Image with ClipDrop**

A simple Streamlit web application that allows users to generate images from text prompts using the ClipDrop Text-to-Image API. This application provides a straightforward interface to leverage AI for creative image generation.

## **Features**

* **Interactive UI**: Built with Streamlit for a responsive and easy-to-use interface.  
* **AI-Powered Image Generation**: Connects to the ClipDrop Text-to-Image API to convert text prompts into visual art.  
* **Secure API Key Handling**: Utilizes python-dotenv to manage API keys securely via environment variables.  
* **User Feedback**: Provides a loading spinner during image generation and displays error messages for API issues.

## **Prerequisites**

Before running this application, ensure you have the following:

* Python 3.8+  
* A ClipDrop API Key (You can get one from the [ClipDrop website](https://clipdrop.co/apis/docs/text-to-image))

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
   pip install streamlit requests Pillow python-dotenv

## **Environment Variables**

Create a file named .env in the root directory of your project (the same directory as your Python script) and add your ClipDrop API key:

CLIPDROP\_KEY="YOUR\_CLIPDROP\_API\_KEY\_HERE"

**Replace YOUR\_CLIPDROP\_API\_KEY\_HERE with your actual ClipDrop API key.**

## **Usage**

1. **Run the Streamlit application:**  
   streamlit run your\_script\_name.py

   (Replace your\_script\_name.py with the actual name of your Python file, e.g., app.py)  
2. This command will open the application in your default web browser.  
3. **Enter a text prompt** in the input field describing the image you want to generate.  
4. Click the **"Generate"** button. The application will then display the generated image. Note that each generation typically consumes one free credit on the ClipDrop API.

## **Error Handling**

The application includes robust error handling to catch common issues such as network problems, API errors (e.g., invalid API key, rate limits), and other exceptions during image generation, providing informative messages to the user.