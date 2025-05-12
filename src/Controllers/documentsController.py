from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from src.config.vector_store import v
from typing import List
from src.utils.preprocessing.indexing import IndexingDocuments
from src.utils.preprocessing.raptor import RaptorChunker
from src.config.vector_store import vector_store

#cac mo hinh can tai ve tu hugging face
huggingface_model_name = "meta-llama/Llama-3.2-1B-Instruct"
embedding_model_name = "all-MPNet-base-v2"

embeddings = HuggingFaceEmbeddings(model_name = embedding_model_name)
# text_splitter = SemanticChunker(embeddings=embeddings,buffer_size=3)
text_splitter = RaptorChunker(embd=embeddings,chunker=SemanticChunker(embeddings=embeddings,buffer_size=3))
#class that init vector_store instance

indexing = IndexingDocuments(vector_store=vector_store,
                            text_splitter=text_splitter)

def get_documents(documents : List[str]):
    try:
        indexing.add_documents(documents)
    except Exception as e:
        return {"error": str(e)}