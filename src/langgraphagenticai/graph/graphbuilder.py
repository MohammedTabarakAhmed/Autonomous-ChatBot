from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tool,create_tool_node
from src.langgraphagenticai.nodes.chabot_with_tool_node import ChabotWithToolNode

class GraphBuilder:
   def __init__(self,model):
      self.llm=model
      self.graph_builder=StateGraph(State)

   def chatbot_with_tools_build_graph(self):
      """
      Builds an advanced chatot grpah wiht tool integration.
      this methos creates a chatbot graph that includes both a chatbot node
      and a tool node. It defines tools, intialies the chatbot with tool
      capabilities, and sets up conditiona; and direct edges between nodes.
      The chatbot node is set as the entry point.
      """
      ##Define the tool and tool nodes
      tools=get_tool()
      tool_node=create_tool_node(tools)

      ## define llm
      llm=self.llm

      #Define the chatbot node
      obj_chatbot_with_node=ChabotWithToolNode(llm)
      chatbot_node=obj_chatbot_with_node.create_chatbot(tools)

      ## Add nodes
      self.graph_builder.add_node("chatbot",chatbot_node)
      self.graph_builder.add_node("tools",tool_node)
      ## add edges
      self.graph_builder.add_edge(START,"chatbot")
      self.graph_builder.add_conditional_edges("chatbot",tools_condition)
      self.graph_builder.add_edge("tools","chatbot")
      self.graph_builder.add_edge("chatbot",END)


   def basic_chatbot_build_graph(self):
      """
      Builds a absic chatbot graph using LangGraph.
      This method initializes a chatbot node using the 'BasicChatbotNode' class
      and inegrates it into the graph. the chatbot node is set as both the 
      entry and exit point of the graph.
      """

      self.basic_chatbot_node=BasicChatbotNode(self.llm)

      self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
      self.graph_builder.add_edge(START,"chatbot")
      self.graph_builder.add_edge("chatbot",END)

   def setup_graph(self,usecase:str):
      """
      Sets up the graph for the selected use case

      """
      if usecase=="Basic Chatbot":
         self.basic_chatbot_build_graph()
         return self.graph_builder.compile()
      if usecase=="Chatbot Web Search":
         self.chatbot_with_tools_build_graph()
         return self.graph_builder.compile()

      raise ValueError(f"Unsupported use case: {usecase}")