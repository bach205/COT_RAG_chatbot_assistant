from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from src.model.llm_model import llm,pipe_runnable
from langchain_community.tools import TavilySearchResults
from src.config.vector_store import vector_store
from langchain import hub
import os

langchain_api_key = os.getenv("LANGSMITH_API_KEY")

prompt = hub.pull("rlm/rag-prompt",api_key=langchain_api_key)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    isMissingDocs : str

#tavily use to search web 
tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)

#format response when use tavily to search
def format_response_from_web_search(messages):
    result = []
    for sub_messages in messages:
        tmp = Document(page_content= "")
        for key,value in sub_messages.items():
            if(key == "content"):
                tmp.page_content=value
            else:
                tmp.metadata[key] = value
        result.append(tmp)
    return result

def retrieve(state: State):
    """
    find docs with similarity score larger than 0.8

    ------------------
    return 
    """
    # retrieved_docs = indexing.vector_store.similarity_search(state["question"])
    # return {"context": retrieved_docs}
    print("retrieving......")
    threshold = 0.8  # Ngưỡng điểm similarity
    docs_with_scores = vector_store.similarity_search_with_score(state["question"], k=10)
    # Lọc các document có điểm >= threshold
    filtered_docs = [doc for doc, score in docs_with_scores if score >= threshold]
    is_missing_docs = "false"
    print(len(filtered_docs))
    print(filtered_docs)
    if(len(filtered_docs)==0):
        is_missing_docs = "true"
    print(is_missing_docs)
    return {"context": filtered_docs,"isMissingDocs":is_missing_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    print("generating.......")
    response = pipe_runnable.invoke(messages)
    print("generated: ")
    result =  {"answer" : response}
    print(result)
    return result
    # response = llm.invoke(messages)
    # return {"answer": response}
    
def search_web(state: State):
    print("compile search_web_node")
    external_source = tool.invoke(state["question"])
    formatted_external_source = format_response_from_web_search(external_source)
    print(formatted_external_source)
    return {"context" : formatted_external_source}