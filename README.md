# Document Reader

Don't waste time reading lengthy Terms and Conditions! Upload your files here and ask anything you want to know.

## Introduction

Welcome to Document Reader! This chatbot is designed to assist users with questions related to uploaded files. Users can upload text documents and inquire about their content.

## Features

- **File Upload:** Users can upload files (text/pdf).
- **Question and Answer:** Ask questions related to the content of the uploaded file.
- **Interactive Assistance:** Receive information and insights based on the uploaded file.

## Getting Started

Follow these steps to get started with Document Reader:

1. Clone the repository:

    ```bash
    git clone https://github.com/SinghJagpreet096/Document-Reader.git
    cd Document-Reader

    ```
2. Create Virtual Environment:
    ```bash
    python -m venv <env-name>
    ```

3. Activate venv:
    ```bash
    source <env-name>/bin/activate
    ```
4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run your app:

    ```bash
    chainlit run app.py
    ```

## Usage

1. Open Document Reader.
2. Click on the file upload button to share a document.
3. Once the file is uploaded, ask questions about its content.
4. The chatbot will provide information or insights based on the uploaded file.

Feel free to type "help" at any time for assistance.

## Configuration

The chatbot may require configuration through environment variables. Check the `.env` file for details. 

## Create an `.env` file.
    ```bash
    echo OPENAI_API_KEY = <your-openai-api-key> > .env
    ```
Create an OPENAI_API_KEY here https://platform.openai.com/api-keys


