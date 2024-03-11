from datetime import datetime

import psycopg2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

DB_NAME = "personal_rag_storage"
DB_HOST = "localhost"
DB_PORT = "5432"
USER_PASSWORD = "personal_rag_storage"
DB_USER = "personal_rag_storage"

TOP_K = 3
CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
COLLECTION_NAME = "mr_index"
# EMBEDDINGS_MODEL = AzureOpenAIEmbeddings(openai_api_version=os.environ["openai_api_version"],
#                                          azure_deployment=os.environ["azure_deployment"],
#                                          azure_endpoint=os.environ["azure_endpoint"],
#                                          openai_api_key=os.environ["AZURE_OPENAI_API_KEY"])

EMBEDDINGS_MODEL = OllamaEmbeddings(model="mistral")

retriever = PGVector.from_existing_index(connection_string=CONNECTION_STRING, embedding=EMBEDDINGS_MODEL,
                                         collection_name=COLLECTION_NAME).as_retriever(search_kwargs={"k": TOP_K})

db_connection = psycopg2.connect(user=DB_USER, password=USER_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME)


class InsertValue(BaseModel):
    value: str


@app.get("/rag-semantic-select")
def rag_semantic_select(sentence: str):
    print(f"new request received, asked to semantic search for sentence: {sentence}")
    documents = retriever.get_relevant_documents(sentence)
    print(f"semantic query for input {sentence} gave back following result: {documents}")
    return documents


@app.get("/rag-select-all")
def rag_semantic_select(limit: int | None = 1):
    print(f"new request received, asked to retrieve all from rag storage. Query limit: {limit}")
    with db_connection as conn:
        with conn.cursor() as cur:
            cur.arraysize = limit
            cur.execute("select uuid, document, cmetadata from langchain_pg_embedding")
            return cur.fetchmany()


@app.put("/rag-storage-insert")
def rag_semantic_select(insert_value: InsertValue):
    print(f"new request received, asked to insert value: {insert_value}")
    added_document_ids = retriever.add_documents(
        [Document(page_content=insert_value.value, metadata={"insert time": str(datetime.now())})])
    print(f"document with ids {added_document_ids} successfully added to rag storage")


@app.delete("/rag-delete-document/{document_id}")
def rag_semantic_select(document_id: str):
    print(f"new request received, asked to delete document with id: {document_id}")
    with db_connection as conn:
        with conn.cursor() as cur:
            cur.execute("delete from langchain_pg_embedding where uuid = %s", (document_id,))
    print(f"document with id: {document_id} deleted from rag storage")


uvicorn.run(app, port=9333)
