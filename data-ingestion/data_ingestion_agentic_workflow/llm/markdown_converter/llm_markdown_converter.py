import asyncio
import os

import httpx
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langfuse import Langfuse, get_client, observe
from langfuse.langchain import CallbackHandler

from .llm_markdown_converter_prompts import md_converter_human_prompt, md_converter_sys_prompt


class LLMMarkdownConverter:
    def __init__(self, ollama_host: str, langfuse_host: str, langfuse_public_key: str, langfuse_secret_key: str):
        self.llm = OllamaLLM(model="llama3.2:3b", base_url=ollama_host, temperature=0.1, num_predict=2024, verbose=True)
        self._llm_timeout = 180.0

        os.environ["LANGFUSE_BASE_URL"] = langfuse_host
        os.environ["LANGFUSE_HOST"] = langfuse_host
        os.environ["LANGFUSE_PUBLIC_KEY"] = langfuse_public_key
        os.environ["LANGFUSE_SECRET_KEY"] = langfuse_secret_key

        #_ = get_client()
        _ = Langfuse(
            secret_key=langfuse_secret_key,
            public_key=langfuse_public_key,
            host=langfuse_host,
            debug=True,
        )

        # self._langfuse_handler = CallbackHandler(
        #     # host=langfuse_host,
        #     public_key=langfuse_public_key,
        #     update_trace=True,
        #     # secret_key=langfuse_secret_key,
        # )

    @observe
    async def convert_markdown(self, markdown_text: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", md_converter_sys_prompt),
                ("human", md_converter_human_prompt),
            ]
        )
        chain = prompt | self.llm

        try:
            #result = await chain.ainvoke({"markdown": markdown_text}, config={"callbacks": [self._langfuse_handler]})
            result = await chain.ainvoke(
                {"markdown": markdown_text},
                timeout=self._llm_timeout)

            return result

        except asyncio.TimeoutError:
            raise TimeoutError(f"LLM call timed out after {self._llm_timeout} seconds")
        except httpx.HTTPError as e:
            raise ConnectionError(f"HTTP error during LLM call: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during LLM call: {e}")
