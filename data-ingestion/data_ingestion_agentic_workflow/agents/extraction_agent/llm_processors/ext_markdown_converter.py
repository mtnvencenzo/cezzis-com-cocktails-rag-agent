import asyncio

import httpx
from langchain_ollama import OllamaLLM


class ExtractionDataMarkdownConverter:
    def __init__(self, ollama_host: str):
        self.llm = OllamaLLM(model="llama3.2:3b", base_url=ollama_host, temperature=0.2, num_predict=1024, verbose=True)

        self._llm_timeout = 90.0

    async def convert_markdown(self, markdown_text: str) -> str:
        prompt = self._prompt(markdown_text)

        try:
            return await asyncio.wait_for(self.llm.ainvoke(prompt), timeout=self._llm_timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"LLM call timed out after {self._llm_timeout} seconds")
        except httpx.HTTPError as e:
            raise ConnectionError(f"HTTP error during LLM call: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during LLM call: {e}")

    def _prompt(self, markdown: str) -> str:
        return f"""
        You are a markdown conversion agent. Your task is to convert the following markdown text into a textual structured format suitable 
        for data extraction.

        Instructions:
        1. You should not respond with anything other than the converted text.
        2. Do not include any explanations or additional commentary. 
        3. Do not include the ingredients heading and immediate section below it. This can be identified by the heading starting with '## Ingredients'.
        4. Do not include the directions heading and immediate section below it.  This can be identified by the heading starting with '## Directions'.
        5. Preserve all other headings and their content as they are.
        6. Ensure the output is clean and free from any markdown syntax.
        7. Maintain the original structure and flow of the content, excluding the specified sections.
        8. The output should be in plain text format.
        9. Retain all relevant information outside of the excluded sections.
        10. Remove any emoji characters from the text.
        11. Any characters that have been JSON escaped in the markdown should be unescaped in the output.
            For example:
            - Convert sequences like \\' to '
            - Convert sequences like \\n to a newline character
            - Convert sequences like \\t to a tab character
            - Convert sequences like \\" to "
            - Convert sequences like \\\\ to \
        12. Any characters that have been json encoded in the markdown should be decoded in the output.
        
        Here is the markdown text that needs to be converted.  Please follow the instructions above:
        {markdown}
        """
