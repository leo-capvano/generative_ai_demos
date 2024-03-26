import os
from abc import ABC

from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings

load_dotenv()


class IEmbeddingsModel(ABC):
    pass


class OpenAIEmbeddingsModel(IEmbeddingsModel):
    def __init__(self):
        self.__embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"],
                                                   model="text-embedding-3-large")

    @property
    def embeddings_model(self):
        return self.__embeddings_model


class AzureOpenAIEmbeddingsModel(IEmbeddingsModel):
    def __init__(self):
        self.__embeddings_model = AzureOpenAIEmbeddings(openai_api_version=os.environ["openai_api_version"],
                                                        azure_deployment=os.environ["azure_deployment"],
                                                        azure_endpoint=os.environ["azure_endpoint"],
                                                        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"])

    @property
    def embeddings_model(self):
        return self.__embeddings_model


class OllamaMistralEmbeddingsModel(IEmbeddingsModel):
    def __init__(self):
        self.__embeddings_model = OllamaEmbeddings(model="mistral")

    @property
    def embeddings_model(self):
        return self.__embeddings_model


def embeddings_model_factory(embeddings_model_impl: str):
    return {
        "openai_embeddings": lambda: OpenAIEmbeddingsModel(),
        "azure_openai_embeddings": lambda: AzureOpenAIEmbeddingsModel(),
        "ollama_mistral": lambda: OllamaMistralEmbeddingsModel()
    }.get(embeddings_model_impl)()
