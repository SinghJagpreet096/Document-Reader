import os
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import chainlit as cl
from src.utils import get_docSearch, get_source
from src.model import load_chain








welcome_message = """ Upload your file here"""

@cl.on_chat_start
async def start():
    await cl.Message("you are in ").send()
    logging.info(f"app started")
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=10,
            timeout=90
        ).send()
    logging.info("uploader excecuted")
    file = files[0]
    msg = cl.Message(content=f"Processing `{type(files)}` {file.name}....")
    await msg.send()

    logging.info("processing started")

    docsearch = get_docSearch(file,cl)
    
    logging.info("document uploaded success")

    chain = load_chain(docsearch)

    logging.info(f"Model loaded successfully")

    
    ## let the user know when system is ready

    msg.content = f"{file.name} processed. You begin asking questions"

    await msg.update()

    logging.info("processing completed")

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL","ANSWER"]
    )

    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])

    answer = res["answer"]
    sources = res["sources"].strip()
    

    ## get doc from user session
    docs = cl.user_session.get("docs")
    metadatas = [doc.metadata for doc in docs]
    all_sources = [m["source"]for m in metadatas]

    source_elements,answer = get_source(sources,all_sources,docs,cl)

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=source_elements).send()

