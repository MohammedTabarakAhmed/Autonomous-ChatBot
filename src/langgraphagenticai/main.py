import streamlit as st
from src.langgraphagenticai.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graphbuilder import GraphBuilder
from src.langgraphagenticai.ui.streamlit.display_result import DisplayResultStreamlit
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph Agentic AI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model.
    Sets up the graph based on the selected use case and displays the output while
    implementing exception handling for robustness.
    """

    #LOAD UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    user_message=st.chat_input("Enter your message: ")
    if not user_message:
        return

    try:
        obj_llm_conig=GroqLLM(user_controls_input=user_input)
        model=obj_llm_conig.get_llm_model()

        if not model:
            st.error("Error: No use case selected")
            return

        usecase=user_input.get("selected_usecase")

        if not usecase:
            st.error("Error: No use case selected.")
            return

        graph_builder=GraphBuilder(model)
        try:
            graph=graph_builder.setup_graph(usecase)
            DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
        except Exception as e:
            st.error(f"Error: Graph setup failed: {e}")
            return

    except Exception as e:
        st.error(f"Error: Graph setup failed: {e}")
        return