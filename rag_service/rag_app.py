import os
from datetime import datetime

import psycopg2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.documents import Document
from pydantic import BaseModel

from rag_service.retriever import retriever_factory

load_dotenv()

app = FastAPI()

db_connection = psycopg2.connect(user=os.environ["DB_USER"], password=os.environ["USER_PASSWORD"],
                                 host=os.environ["DB_HOST"],
                                 port=os.environ["DB_PORT"], database=os.environ["DB_NAME"])
retriever = retriever_factory("pgvector")


class InsertValue(BaseModel):
    value: str


@app.get("/rag-semantic-select")
def rag_semantic_select(sentence: str):
    print(f"new request received, asked to semantic search for sentence: {sentence}")
    documents = retriever.get_relevant_documents(sentence)
    print(f"semantic query for input {sentence} gave back following result: {documents}")
    return documents


@app.get("/rag-select-all")
def rag_select_all(limit: int | None = 1):
    print(f"new request received, asked to retrieve all from rag storage. Query limit: {limit}")
    with db_connection as conn:
        with conn.cursor() as cur:
            cur.arraysize = limit
            cur.execute("select uuid, document, cmetadata from langchain_pg_embedding")
            return cur.fetchmany()


@app.put("/rag-storage-insert")
def rag_insert(insert_value: InsertValue):
    print(f"new request received, asked to insert value: {insert_value}")
    added_document_ids = retriever.add_documents(
        [Document(page_content=insert_value.value, metadata={"insert time": str(datetime.now())})])
    print(f"document with ids {added_document_ids} successfully added to rag storage")


@app.delete("/rag-delete-document/{document_id}")
def rag_delete(document_id: str):
    print(f"new request received, asked to delete document with id: {document_id}")
    with db_connection as conn:
        with conn.cursor() as cur:
            cur.execute("delete from langchain_pg_embedding where uuid = %s", (document_id,))
    print(f"document with id: {document_id} deleted from rag storage")


uvicorn.run(app, port=9333)
