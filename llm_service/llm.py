import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import OpenAI

load_dotenv()


class ILLM(ABC):
    @abstractmethod
    def call_llm(self, call_input: str) -> str:
        pass

    @abstractmethod
    def get_llm(self):
        pass


# class AzureOpenAILLM(ILLM):
#     def __init__(self):
#         self.__llm: BaseLanguageModel = AzureChatOpenAI(openai_api_version=os.environ["openai_api_version"],
#                                                         azure_deployment=os.environ["azure_deployment"],
#                                                         azure_endpoint=os.environ["azure_endpoint"],
#                                                         openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
#                                                         temperature=os.environ["temperature"],
#                                                         model_name=os.environ["model_name"])
#
#     def get_llm(self):
#         return self.__llm
#
#     def call_llm(self, call_input: str) -> str:
#         return self.__llm.invoke(call_input).content


class OllamaMistralLLM(ILLM):
    def __init__(self):
        self.__llm: BaseLanguageModel = Ollama(model="mistral")

    def call_llm(self, call_input: str) -> str:
        return self.__llm.invoke(call_input)

    def get_llm(self):
        return self.__llm


class OpenAILLM(ILLM):
    def __init__(self):
        self.__llm: BaseLanguageModel = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])

    def call_llm(self, call_input: str) -> str:
        return self.__llm.invoke(call_input)

    def get_llm(self):
        return self.__llm


def llm_factory(strategy: str) -> ILLM:
    return {
        # "azure_openai": AzureOpenAILLM(),
        "ollama_mistral": lambda: OllamaMistralLLM(),
        "openai": lambda: OpenAILLM()
    }.get(strategy)()
