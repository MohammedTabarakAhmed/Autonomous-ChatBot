from typing import list,Annotated,TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the strucutre of the state used in graph
    """
    messages:Annotated[list,add_messages] #add_messages os a "reducer" instructs LG to append new messages to exisiting list rather than overwriting to maintain history