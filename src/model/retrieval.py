from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from src.config.mongo_db import client
import os
from dotenv import load_dotenv
from src.model.preprocessing.indexing import IndexingDocuments
from langchain import hub
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from src.model.llm_model import llm,pipe_runnable

load_dotenv()
#cac mo hinh can tai ve tu hugging face
huggingface_model_name = "meta-llama/Llama-3.2-1B-Instruct"
embedding_model_name = "all-MPNet-base-v2"
database_name = os.getenv("MONGODB_DATABASE_NAME")
collection_name = os.getenv("MONGODB_COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_search_index"
langchain_api_key = os.getenv("LANGSMITH_API_KEY")

prompt = hub.pull("rlm/rag-prompt",api_key=langchain_api_key)

embeddings = HuggingFaceEmbeddings(model_name = embedding_model_name)
text_splitter = SemanticChunker(embeddings=embeddings,buffer_size=3)
indexing = IndexingDocuments(model_name=huggingface_model_name,
                             embeddings=embeddings,
                             database_client=client,
                             database_collection_name=collection_name,
                             database_name=database_name,
                             database_vector_search_index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
                             text_splitter=text_splitter)


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
def retrieve(state: State):
    retrieved_docs = indexing.vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm(messages=messages,type="local")
    result =  {"answer" : response.choices[0].message.content}
    print(result)
    return result
    # response = llm.invoke(messages)
    # return {"answer": response}


