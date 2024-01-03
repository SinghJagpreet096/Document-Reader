import os
import logging

# from dotenv import load_dotenv

#export HNSWLIB_NO_NATIVE = 1

from langchain.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Chroma
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import chainlit as cl
import openai
from src.config import Config
from src.utils import get_docsearch, get_source

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# embeddings = OpenAIEmbeddings()

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


welcome_message = """Welcome to Your Document Reader!

Here to assist you with any questions you have about a file. You can upload a file and ask me questions related to its content. Here's how you can get started:

1. Click on the file upload button to share a document or image.
2. Once the file is uploaded, feel free to ask me any questions about its content.
3. I'll do my best to provide information or insights based on the uploaded file.

If you need help or have any specific queries, type "help" at any time.

Let's get the conversation started! """


@cl.on_chat_start
async def start():
    await cl.Message("YOU ARE IN").send()
    files = None
    files = await cl.AskFileMessage(
        content=welcome_message,
        accept=["text/plain", "application/pdf"],
        max_size_mb=Config.max_size_mb,
        timeout=Config.timeout
    ).send()

    logging.info("file uploaded")

    file = files[0]

    msg = cl.Message(content=f"Processing {file.name}")
    await msg.send()

    logging.info("file processing")

    
    docsearch = await cl.make_async(get_docsearch)(file)

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True
    )

    ## create chain that uses chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name=Config.model_name,temperature=Config.temperature, streaming=Config.streaming),
        chain_type=Config.chain_type,
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )


    msg.content = f"Processing {file.name} completed. Start asking questions!"
    await msg.update()

    logging.info("file processed success")

    cl.user_session.set("chain",chain)

    logging.info("saved chain in currrent session")


@cl.on_message
async def main(message: cl.Message):

    ## get chain
    chain = cl.user_session.get("chain")

    logging.info("loaded chain")

    cb = cl.AsyncLangchainCallbackHandler()

    logging.info("loaded callbacks")

    res = await chain.acall(message.content, callbacks=[cb])

    answer = res["answer"]
    source_documents = res["source_documents"]
    
    text_elements = get_source(answer, source_documents)
    await cl.Message(content=answer, elements=text_elements).send()
    





