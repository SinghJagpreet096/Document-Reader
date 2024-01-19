from chainlit.types import AskFileResponse
import click
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
import chainlit as cl
from src.config import Config

from src.config import Config
import logging

# text_splitter = RecursiveCharacterTextSplitter()
# embeddings = OpenAIEmbeddings()

def process_file(file: AskFileResponse):
    import tempfile

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        loader = Loader(tempfile.name)
        documents = loader.load()
        docs = Config.text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs

def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    # Save data in the user session
    cl.user_session.set("docs", docs)

    # Create a unique namespace for the file

    docsearch = Chroma.from_documents(
        docs, Config.embeddings
    )
    return docsearch

def get_source(answer,source_documents):
        text_elements = []
        if source_documents:
            for source_idx, source_doc in enumerate(source_documents):
                source_name = f"source_{source_idx}"

                text_elements.append(
                    cl.Text(content=source_doc.page_content, name=source_name)
                )
            source_names = [text_el.name for text_el in text_elements]

            if source_names:
                answer += f"\nSources: {', '.join(source_names)}"
            else:
                answer += "\nNo source found"
        return text_elements