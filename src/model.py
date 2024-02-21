
from langchain_community.chat_models import ChatOpenAI

from langchain.chains import ConversationalRetrievalChain


from src.config import Config





def load_model():
    model = ChatOpenAI(model_name=Config.model_name,
                       temperature=Config.temperature, 
                       streaming=Config.streaming)
    return model


def load_chain(docsearch):
    model = load_model()
    
    
    chain = ConversationalRetrievalChain.from_llm(load_model,
        chain_type=Config.chain_type,
        retriever=docsearch.as_retriever(),
        memory=Config.memory,
        return_source_documents=True,
    )

    return chain
