from langchain_mongodb import MongoDBAtlasVectorSearch
import os
from src.config.mongo_db import client
from langchain_huggingface import HuggingFaceEmbeddings

#cac field
embedding_model_name = "all-MPNet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name = embedding_model_name)
database_name = os.getenv("MONGODB_DATABASE_NAME")
collection_name = os.getenv("MONGODB_COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_search_index"
vector_store = None
try:
    vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=client[database_name][collection_name],
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)
except Exception as e:
    print(str(e))