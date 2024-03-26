import os
from abc import ABC, abstractmethod
from typing import List

from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from rag_service.app_config import CONNECTION_STRING, COLLECTION_NAME, TOP_K
from rag_service.embeddings_model import embeddings_model_factory

embeddings_model = embeddings_model_factory(os.environ["embeddings_model_impl"])


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
