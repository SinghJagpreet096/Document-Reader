import os
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import chainlit as cl
from src.utils import get_docSearch
from src.model import load_chain







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

    docsearch = get_docSearch(file)
    

    chain = load_chain(docsearch)

    logging.info(f"Model loaded successfully")

    
    ## let the user know when system is ready

    msg.content = f"{file.name} processed. You begin asking questions"

    await msg.update()

    cl.user_session.set("chain", chain)


