from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from src.config.mongo_db import client
import os
from src.utils.preprocessing.indexing import IndexingDocuments
from src.utils.preprocessing.raptor import RaptorChunker

#cac mo hinh can tai ve tu hugging face
huggingface_model_name = "meta-llama/Llama-3.2-1B-Instruct"
embedding_model_name = "all-MPNet-base-v2"
database_name = os.getenv("MONGODB_DATABASE_NAME")
collection_name = os.getenv("MONGODB_COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_search_index"


embeddings = HuggingFaceEmbeddings(model_name = embedding_model_name)
# text_splitter = SemanticChunker(embeddings=embeddings,buffer_size=3)
text_splitter = RaptorChunker(embd=embeddings,chunker=SemanticChunker(embeddings=embeddings,buffer_size=3))
#class that init vector_store instance
indexing = IndexingDocuments(model_name=huggingface_model_name,
                             embeddings=embeddings,
                             database_client=client,
                             database_collection_name=collection_name,
                             database_name=database_name,
                             database_vector_search_index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
                             text_splitter=text_splitter)




