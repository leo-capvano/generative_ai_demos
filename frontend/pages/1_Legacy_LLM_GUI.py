import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.title("LLM Tool [LEGACY]")
text_input_value = st.text_input(label="Ask to the LLM")


def call_legacy_llm(query):
    legacy_ask_response = requests.post(f"{os.environ["base_llm_service_endpoint"]}/legacy-ask", json={"query": query})
    if legacy_ask_response.status_code == 200:
        return legacy_ask_response.text
    else:
        print(f"Failure legacy ask: {legacy_ask_response.status_code}")
        return False


if text_input_value:
    with st.spinner("Generating response ..."):
        legacy_ask_result = call_legacy_llm(text_input_value)
        if legacy_ask_result:
            with st.container(border=True):
                st.write(legacy_ask_result)
        else:
            st.write("Error during generation :(")
