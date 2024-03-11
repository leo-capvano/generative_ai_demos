import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.title("LLM Tool [Agent]")


def call_agent_llm(query):
    rag_ask_response = requests.post(f"{os.environ["base_llm_service_endpoint"]}/agent-ask", json={"query": query})
    if rag_ask_response.status_code == 200:
        return json.loads(rag_ask_response.text)
    else:
        print(f"Failure legacy ask: {rag_ask_response.status_code}")
        return False


def get_all_registered_tools() -> dict:
    get_tools_response = requests.get(f"{os.environ["base_llm_service_endpoint"]}/tools")
    if get_tools_response.status_code == 200:
        return json.loads(get_tools_response.text)


st.markdown(""":orange[Registered Agent Tools]""")
with st.spinner("Loading tools from backend"):
    tools = get_all_registered_tools()
    for t in tools:
        st.markdown(f"""\n :green[- {t}]""")

st.divider()
text_input_value = st.text_area(label="Ask to the Agent LLM")
if text_input_value:
    with st.spinner("Generating response ..."):
        agent_ask_result: dict = call_agent_llm(text_input_value)
        if agent_ask_result:
            with st.container(border=True):
                st.markdown(f""" :red[Response: {agent_ask_result["output"]}] """)
            with st.container(border=True):
                for step in agent_ask_result.get("intermediate_steps"):
                    st.markdown(f""" Agent Step: """)
                    st.markdown(f""" -> tool used: :orange[{step[0].get("tool")}]""")
                    st.markdown(f""" -> tool output: :orange[{step[1]}]""")
        else:
            st.write("Error during generation :(")
