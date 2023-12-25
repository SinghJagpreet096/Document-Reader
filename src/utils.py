from chainlit.types import AskFileResponse
import click
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma


from src.config import Config
import logging

from dotenv import load_dotenv

load_dotenv()




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
        # text_splitter = text_splitter()
        docs = Config.text_splitter.split_documents(documents)

        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs

def get_docSearch(file,cl):
    docs = process_file(file)

    logging.info("files loaded ")

    ## save data in user session 
    cl.user_session.set("docs",docs)

    logging.info("docs saved in active session")
    
    docsearch = Chroma.from_documents(docs, Config.embeddings)

    logging.info(f"embedding completed {type(Config.embeddings)}")

    logging.info(f"type of docsearch {type(docsearch)}")

    return docsearch

def get_source(sources,all_sources,docs,cl):
    answer = []
    source_elements = []
    if sources:
        found_sources = []

        # Add the sources to the message
        for source in sources.split(","):
            source_name = source.strip().replace(".", "")
            # Get the index of the source
            try:
                index = all_sources.index(source_name)
            except ValueError:
                continue
            text = docs[index].page_content
            found_sources.append(source_name)
            # Create the text element referenced in the message
            source_elements.append(cl.Text(content=text, name=source_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\nNo sources found"
    return source_elements,answer