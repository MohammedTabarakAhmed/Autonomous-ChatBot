import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Basic Chatbot":
            for event in graph.stream({"messages": ("user", user_message)}):
                for value in event.values():
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "Chatbot Web Search":
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            result = graph.invoke(initial_state)
            for message in result["messages"]:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, ToolMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)