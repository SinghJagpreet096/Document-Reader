from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
import logging
import os


from src.config import Config





def load_model():
    model = ChatOpenAI(temperature=Config.temperature,
                   streaming=Config.streaming)
    return model


def load_chain(docsearch):
    model = load_model()
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0, streaming=True),
        chain_type="stuff",
        retriever=docsearch.as_retriever(max_tokens_limit=4097),
    )
    return chain
