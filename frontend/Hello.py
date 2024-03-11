import streamlit as st

st.title("GenAI Tool")
st.sidebar.success("Select one of the demos above.")

st.markdown('''
    ## Hi, this is a tool to run demo LLM queries.
    There are 2 pages dedicated to the LLM queries:
    - Legacy LLM
        > :green[ask LLM questions without context and obtain general purpose responses]
    - Retrieval Augmented Generation (RAG) LLM 
        > :green[ask LLM questions with a context. The response you get depends on the RAG storage informations]
        
    There is one page dedicated to the RAG storage administration in which you can:
    - see what's inside your rag storage
    - add basic informations to the rag storage
    - delete informations
''')
