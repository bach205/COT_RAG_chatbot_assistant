from langchain_community.document_loaders import WebBaseLoader
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.vectorstores.utils import filter_complex_metadata
class IndexingDocuments:
    def __init__(self,
                model_name ,
                embeddings ,
                database_client,
                database_name,
                database_collection_name,
                database_vector_search_index_name,
                text_splitter,
                relevance_score_fn="cosine"):
        self.model_name = model_name
        self.embeddings = embeddings
        self.database_client = database_client
        self.database_name = database_name
        self.database_collection_name = database_collection_name
        self.database_vector_search_index_name = database_vector_search_index_name
        self.relevance_score_fn = relevance_score_fn
        self.text_splitter = text_splitter
        try:
            self.vector_store = MongoDBAtlasVectorSearch(
                embedding=self.embeddings,
                collection=self.database_client[self.database_name][self.database_collection_name],
                index_name=database_vector_search_index_name,
                relevance_score_fn=self.relevance_score_fn,
            )
        except Exception as e:
            print(e)   
    async def add_documents(self,documents : list):
        #luu cac documents duoc user input vao

        try:
            print("loading document....")
            loader = WebBaseLoader(documents)
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