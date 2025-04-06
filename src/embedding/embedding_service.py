from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from pathlib import Path

class VectorService:
    def __init__(self):
        self.embedding_model = OllamaEmbeddings(model="snowflake-arctic-embed:latest")
        #the path starts from root path of the project
        self.vector_store = Chroma(collection_name="ChatBI",embedding_function=self.embedding_model,persist_directory='src/embedding_data')
        self.text_loader = TextLoader("src/documents/description_of_relations_in_chinook.text")
        #load documents
        document_of_chinook = self.text_loader.load();
        #split documents
        text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=30)
        texts = text_splitter.split_documents(document_of_chinook)
        self.vector_store.from_documents(documents=texts,embedding=self.embedding_model,collection_name="ChatBI",persist_directory='src/embedding_data')
        self.retriever = None

    def get_vector_store(self):
        self.retriever = self.vector_store.as_retriever()
        return self.retriever

    def get_knowledge_from_vector_store(self,query_question:str):
        docs = self.get_vector_store().invoke(query_question)
        return docs
