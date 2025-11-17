import asyncio
import json
from typing import List

import httpx
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langfuse.langchain import CallbackHandler

from data_ingestion_agentic_workflow.llm.content_chunking.llm_content_chunker_prompts import (
    cnt_chunker_human_prompt,
    cnt_chunker_sys_prompt,
)
from data_ingestion_agentic_workflow.llm.setup.llm_model_options import LLMModelOptions
from data_ingestion_agentic_workflow.llm.setup.llm_options import LLMOptions
from data_ingestion_agentic_workflow.llm.setup.ollama_utils import get_ollama_model_client
from data_ingestion_agentic_workflow.models.cocktail_chunking_model import CocktailDescriptionChunk


class LLMContentChunker:
    """A markdown to text converter using an LLM model."""

    def __init__(self, llm_options: LLMOptions, model_options: LLMModelOptions) -> None:
        """Initialize the LLMContentChunker with LLM options and model settings.

        Args:
            llm_options (LLMOptions): The LLM options for configuration.
            model_options (LLMModelOptions): The model settings for configuration.
        """
        self.llm = get_ollama_model_client(
            name=f"content chunking [{model_options.model}]", llm_options=llm_options, llm_model_options=model_options
        )

        self._llm_timeout = model_options.timeout_seconds or 60
        self._langfuse_handler = CallbackHandler(update_trace=True)

    async def chunk_content(self, extraction_text: str) -> List[CocktailDescriptionChunk] | None:
        """Convet exracted plain text content into chunks using LLM.

        Args:
            extraction_text (str): The extracted plain text content to chunk.

        Returns:
            List[CocktailDescriptionChunk]: The list of content chunks.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", cnt_chunker_sys_prompt),
                ("human", cnt_chunker_human_prompt),
            ]
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            result = await chain.with_config({"run_name": "data-ingestion-workflow-2"}).ainvoke(
                {"content": extraction_text}, timeout=self._llm_timeout, config={"callbacks": [self._langfuse_handler]}
            )
            self._langfuse_handler.client.flush()

            if not result:
                return None

            array_result = json.loads(result)
            return [CocktailDescriptionChunk(**item) for item in array_result]

        except asyncio.TimeoutError as e:
            raise TimeoutError(f"LLM call timed out after {self._llm_timeout} seconds") from e
        except httpx.HTTPError as e:
            raise ConnectionError(f"HTTP error during LLM call: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred during LLM call: {e}") from e
