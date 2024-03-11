import json
import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools.brave_search.tool import BraveSearch
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

llm = AzureChatOpenAI(openai_api_version=os.environ["openai_api_version"],
                      azure_deployment=os.environ["azure_deployment"],
                      azure_endpoint=os.environ["azure_endpoint"],
                      openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
                      temperature=os.environ["temperature"],
                      model_name=os.environ["model_name"])


# llm = OpenAI(temperature=os.environ["temperature"],
#              openai_api_key="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")

# llm = Ollama(model="mistral")


@tool
def sum_numbers(a: int, b: int):
    """Use this tool if you want to calculate the sum of two numbers"""
    return a + b


@tool
def learn(fact: str):
    """Use this tool when you have to remember or learn something"""
    learn_response = requests.put(f"{os.environ["base_rag_service_endpoint"]}/rag-storage-insert", json={"value": fact})
    if learn_response.status_code == 200:
        return "Ok, I'll remember!"
    else:
        return "Sorry, there was an error during the generation :("


tools = [BraveSearch.from_api_key(api_key=os.environ["brave_api_key"], search_kwargs={"count": 3}), sum_numbers, learn]


class AskQuery(BaseModel):
    query: str


@app.post("/legacy-ask")
def legacy_ask(ask_query: AskQuery):
    print(f"received new request, legacy ask with user query: {ask_query.query}")
    return llm.invoke(ask_query.query)


@app.get("/tools")
def get_tools():
    tools_desc = [t.description for t in tools]
    return tools_desc


@app.post("/rag-ask")
def rag_ask(ask_query: AskQuery):
    print(f"received new request, RAG ask with user query: {ask_query.query}")
    context: list = json.loads(requests.get(
        f"{os.environ["base_rag_service_endpoint"]}/rag-semantic-select?sentence={ask_query.query}").text)

    prompt_context = "----\n----".join(list(map(lambda doc: doc.get("page_content"), context)))
    prompt_template = f"""
    Given the following context:
    {prompt_context}
    Answer to the following question:
    {ask_query.query}
    """

    return {"generation_result": llm.invoke(prompt_template), "source_documents": prompt_context}


@app.post("/agent-ask")
def agent_ask(ask_query: AskQuery):
    print(f"received new request, Agent ask with user query: {ask_query.query}")
    prompt_template = hub.pull("hwchase17/openai-tools-agent")
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)
    result = agent_executor.invoke({"input": ask_query})
    return {"output": result.get("output"), "intermediate_steps": result.get("intermediate_steps")}


uvicorn.run(app, port=9334)
