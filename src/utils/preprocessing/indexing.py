from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
class IndexingDocuments:
    def __init__(self,
                documents_loader :BaseLoader,
                text_splitter,                    # Text splitter to break documents into smaller chunks
                vector_store
    ):
        
        # Store the provided parameters as instance variables
        self.text_splitter = text_splitter
        self.vector_store = vector_store
        if(documents_loader == None):
            self.documents_loader = WebBaseLoader

    # Asynchronous method to add documents (URLs) to the vector store   
    async def add_documents(self,documents : list):
        if(self.vector_store == None and self.text_splitter == None):
            raise Exception("you need to init vector store")
        #luu cac documents duoc user input vao store
        try:
            print("loading document....")
            loader = self.documents_loader(documents)
            docs = loader.load()
            print("chunking documents....")
            chunks = self.text_splitter.split_documents(docs)
            chunks_filtered_metadatas = filter_complex_metadata(chunks)
            print("storing into mongoDB....")
            a= self.vector_store.add_documents(chunks_filtered_metadatas)
            print ("successfully")
            return a
        except Exception as e:
            print(e)            