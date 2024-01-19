import os
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ChatMessageHistory, ConversationBufferMemory



class Config:
    temperature = 0
    streaming = True
    max_size_mb=20
    timeout=180
    chain_type = "stuff"
    max_token_limit = 4098
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    model_name="gpt-3.5-turbo"
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True
    )