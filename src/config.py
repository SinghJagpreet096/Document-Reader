import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



class Config:
    temperature = 0
    streaming = True
    chain_type = "stuff"
    max_token_limit = 4098
    embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)