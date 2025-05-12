
from langgraph.graph import START, StateGraph, END
from utils.graph_utils import retrieve,generate,search_web,State


def route_is_missing_docs(state:State):
    return state["isMissingDocs"]
graph_builder = StateGraph(State)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)
graph_builder.add_node("search_web", search_web)
graph_builder.add_edge(START, "retrieve")
graph_builder.add_conditional_edges(
    source="retrieve",
    path=route_is_missing_docs,
    path_map={
        "true": "search_web",
        "false": "generate"
    }
)
graph_builder.add_edge("search_web", "generate")
graph_builder.add_edge( "generate",END)
print("building")
graph = graph_builder.compile()