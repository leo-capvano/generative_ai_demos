import os
from abc import ABC, abstractmethod
from typing import List

from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from rag_service.embeddings_model import embeddings_model_factory

embeddings_model = embeddings_model_factory("openai_embeddings")

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
USER_PASSWORD = os.environ["USER_PASSWORD"]
DB_USER = os.environ["DB_USER"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
TOP_K = int(os.environ["TOP_K"])
CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class IRetriever(ABC):

    @abstractmethod
    def get_relevant_documents(self, sentence: str):
        pass

    @abstractmethod
    def add_documents(self, docs: List[Document]):
        pass


class PGVectorRetriever(IRetriever):
    def __init__(self, connection_string: str, emb_model: Embeddings, collection_name: str, top_k: int):
        self.__retriever = PGVector.from_existing_index(
            connection_string=connection_string,
            embedding=emb_model,
            collection_name=collection_name).as_retriever(search_kwargs={"k": top_k})

    def get_relevant_documents(self, sentence: str):
        return self.__retriever.get_relevant_documents(sentence)

    def add_documents(self, docs: List[Document]):
        return self.__retriever.add_documents(documents=docs)


def retriever_factory(retriever_impl: str):
    return {
        "pgvector": lambda: PGVectorRetriever(CONNECTION_STRING, embeddings_model, COLLECTION_NAME, TOP_K)
    }.get(retriever_impl)()
