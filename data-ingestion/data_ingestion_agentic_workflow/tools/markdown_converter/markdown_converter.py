import asyncio

from langchain.tools import tool
from strip_markdown import strip_markdown


@tool
async def convert_markdown(markdown_text: str) -> str | None:
    """Strips markdown formatting from the given markdown_text.
    Args:
        markdown_text (str): The markdown formatted text that needs to be cleaned of any markdown syntax.
    Returns:
        str: The cleaned text without markdown formatting.
    """

    try:
        result = strip_markdown(md=markdown_text)
        await asyncio.sleep(0)  # Yield control to the event loop
        return result

    except Exception as e:
        raise RuntimeError(f"An error occurred during markdown conversion process: {e}") from e
