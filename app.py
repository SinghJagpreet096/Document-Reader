import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import chainlit as cl



text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = OpenAIEmbeddings()

welcome_message = """ Upload your file here"""

@cl.on_chat_start
async def start():
    await cl.Message("you are in ").send()
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=10,
            timeout=90
        ).send()
    file = files[0]
    msg = cl.Message(content=f"Processing `{type(files)}` {file.name}....")
    await msg.send()
