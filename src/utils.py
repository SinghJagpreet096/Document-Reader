from chainlit.types import AskFileResponse
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = OpenAIEmbeddings()

def process_file(file: AskFileResponse):
    import tempfile 

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFDirectoryLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        loader = Loader(tempfile.name)
        documents = loader.load()
        # text_splitter = text_splitter()
        docs = text_splitter.split_documents(documents)

        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs

def get_docSearch(file: AskFileResponse):
    docs = process_file(file)

    ## save data in user session 
    
    docsearch = Chroma.from_documents(docs, embeddings)

    return docsearch