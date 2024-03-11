import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.title("LLM Tool [RAG]")
text_input_value = st.text_input(label="Ask to the LLM")


def call_rag_llm(query):
    rag_ask_response = requests.post(f"{os.environ["base_llm_service_endpoint"]}/rag-ask", json={"query": query})
    if rag_ask_response.status_code == 200:
        return json.loads(rag_ask_response.text)
    else:
        print(f"Failure legacy ask: {rag_ask_response.status_code}")
        return False


if text_input_value:
    with st.spinner("Generating response ..."):
        rag_ask_result: dict = call_rag_llm(text_input_value)
        if rag_ask_result:
            with st.container(border=True):
                st.markdown(
                    f"""
                    Response: {rag_ask_result["generation_result"]} 
                    :orange[Context Documents: {rag_ask_result["source_documents"]}]
                    """)
        else:
            st.write("Error during generation :(")
