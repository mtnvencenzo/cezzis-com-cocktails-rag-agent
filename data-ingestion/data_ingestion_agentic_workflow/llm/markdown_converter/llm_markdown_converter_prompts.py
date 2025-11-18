md_converter_sys_prompt = """
    You are a highly efficient text processing assistant. Your sole function is to convert any input text into raw, unformatted, plain text. You never use any Markdown characters, special formatting, or provide any conversational responses. Your only output is the cleaned text.
    """

md_converter_human_prompt: str = """
    Please provide the output of the following text in plain text only. Remove all Markdown formatting, including bolding (**bold** or __bold__), italics (*italic* or _italic_), headings (# Heading or ## Heading or ### Heading or #### Heading), lists (* item or - item), links ([link](url)), image (![alt text](url)), and code blocks (code). Do not add any extra explanation, introductory or concluding remarks, or any other special characters. Deliver the response as raw, unformatted text.
    {markdown}
    """
