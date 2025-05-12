from src.model.graph import graph 

def receive_messages(messages : str):
    return graph.invoke({"question" : messages})