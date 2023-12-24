from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
import logging
import os


from src.config import Config





def load_model():
    model = ChatOpenAI(temperature=Config.temperature,
                   streaming=Config.streaming,api_key=os.getenv('OPENAI_API_KEY'))
    return model


def load_chain(docsearch):
    model = load_model()
    chain = RetrievalQAWithSourcesChain.from_chain_type(model,
                                                        chain_type=Config.chain_type,
                                                        retriever=docsearch.as_retriever(max_tokens_limit=Config.max_token_limit))
    return chain
