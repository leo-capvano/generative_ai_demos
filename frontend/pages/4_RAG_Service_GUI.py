import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from requests import Response

load_dotenv()


def call_semantic_search():
    resp: Response = requests.get(
        f"{os.environ["base_rag_service_endpoint"]}/rag-semantic-select?sentence={st.session_state.semantic_query_input}")
    documents = json.loads(resp.text)
    return list(map(lambda d: d.get("page_content"), documents))


def get_all(limit: int):
    resp = requests.get(
        f"{os.environ["base_rag_service_endpoint"]}/rag-select-all?limit={str(limit)}")
    documents = json.loads(resp.text)
    return list(map(lambda d: {"document": d[1], "uuid": d[0]}, documents))


def insert():
    return requests.put(f"{os.environ["base_rag_service_endpoint"]}/rag-storage-insert",
                        json={"value": st.session_state.insert_text_input})


def delete_rag_rows():
    if ("get_all_view" in st.session_state and "deleted_rows" in st.session_state["get_all_view"]
            and "get_all_query_result" in st.session_state):
        for row_id in st.session_state.get_all_view["deleted_rows"]:
            uuid = st.session_state.get_all_query_result[row_id]["uuid"]
            print(f"deleting object {st.session_state.get_all_query_result[row_id]}")
            delete_response = requests.delete(f"{os.environ["base_rag_service_endpoint"]}/rag-delete-document/{uuid}")
            print(delete_response)


delete_rag_rows()

col1, col2 = st.columns(spec=[0.7, 0.3], gap="medium")
with col1:
    with st.container(border=True):
        st.title("Rag Semantic Query Tool")
        st.text_input(label="Semantic search query input text below ...", key="semantic_query_input")
        semantic_search_button = st.button(label="semantic search")
        get_all_button = st.button("get all")

        if semantic_search_button:
            with st.spinner("Semantic query running .."):
                query_result: list = call_semantic_search()
            with st.container(border=True):
                st.write("Semantic Query Result\n")
                st.dataframe(query_result)

        if get_all_button:
            with st.spinner("Getting all from vector store ..."):
                get_all_query_result: list = get_all(100)
                st.session_state["get_all_query_result"] = get_all_query_result
            with st.container(border=True):
                st.write("Get All Query Results\n")
                st.data_editor(get_all_query_result, num_rows="dynamic", key="get_all_view")

with col2:
    with st.container(border=True):
        st.title("Rag Insert Tool")
        st.text_area(label="Insert into rag storage", key="insert_text_input")
        insert_button = st.button("Insert")
        if insert_button:
            with st.spinner("Inserting value ..."):
                response = insert()
                if response.status_code == 200:
                    st.write("Tutt'appost")
                else:
                    st.write("Error occurred, check the logs please")
