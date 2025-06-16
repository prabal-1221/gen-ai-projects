# Jokes Generator

A simple Streamlit web application that uses the Cohere Command R+ large language model via LangChain to generate jokes on a user-specified topic.

## Features

- **Interactive UI**: Built with Streamlit for a user-friendly interface.
- **AI-Powered Joke Generation**: Leverages Cohere's command-r-plus model to create jokes based on input.
- **LangChain Integration**: Uses LangChain for seamless interaction with the LLM and prompt management.
- **Environment Variable Support**: Securely loads API keys using python-dotenv.
- **Resource Caching**: Optimizes performance by caching the LLM chain initialization.

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.8+
- A Cohere API Key

## Installation

Clone the repository (if applicable) or save the code:

```bash
git clone <repository_url>
cd <repository_directory> # If you cloned a repo
