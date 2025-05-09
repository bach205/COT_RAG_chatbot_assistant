
from langgraph.graph import START, StateGraph
from src.model.retrieval import State,retrieve,generate

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()