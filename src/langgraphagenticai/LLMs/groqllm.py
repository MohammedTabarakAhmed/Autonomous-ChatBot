import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key=self.user_controls_input.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')
            selected_groq_model=self.user_controls_input['selected_groq_model']
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is missing. Enter it in the sidebar or add it to .env.")

            llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occured with Exception: {e}")
        
        return llm