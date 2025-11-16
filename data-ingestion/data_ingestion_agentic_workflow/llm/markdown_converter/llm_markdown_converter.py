import asyncio

import httpx
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langfuse.langchain import CallbackHandler

from data_ingestion_agentic_workflow.llm.markdown_converter.llm_markdown_converter_prompts import (
    md_converter_human_prompt,
    md_converter_sys_prompt,
)
from data_ingestion_agentic_workflow.llm.setup.llm_model_options import LLMModelOptions
from data_ingestion_agentic_workflow.llm.setup.llm_options import LLMOptions
from data_ingestion_agentic_workflow.llm.setup.ollama_utils import get_ollama_model_client


class LLMMarkdownConverter:
    """A markdown to text converter using an LLM model."""

    def __init__(self, llm_options: LLMOptions, model_options: LLMModelOptions) -> None:
        """Initialize the LLMMarkdownConverter with LLM options and model settings.

        Args:
            llm_options (LLMOptions): The LLM options for configuration.
            model_options (LLMModelOptions): The model settings for configuration.
        """
        self.llm = get_ollama_model_client(
            name=f"convert_markdown [{model_options.model}]", llm_options=llm_options, llm_model_options=model_options
        )

        self._llm_timeout = model_options.timeout_seconds or 60
        self._langfuse_handler = CallbackHandler(update_trace=True)

    async def convert_markdown(self, markdown_text: str) -> str:
        """Convert markdown text to plain text using the LLM.

        Args:
            markdown_text (str): The markdown text to convert.

        Returns:
            str: The converted plain text.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", md_converter_sys_prompt),
                ("human", md_converter_human_prompt),
            ]
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            result = await chain.with_config({"run_name": "data-ingestion-workflow"}).ainvoke(
                {"markdown": markdown_text}, timeout=self._llm_timeout, config={"callbacks": [self._langfuse_handler]}
            )
            self._langfuse_handler.client.flush()

            return result

        except asyncio.TimeoutError:
            raise TimeoutError(f"LLM call timed out after {self._llm_timeout} seconds")
        except httpx.HTTPError as e:
            raise ConnectionError(f"HTTP error during LLM call: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during LLM call: {e}")
