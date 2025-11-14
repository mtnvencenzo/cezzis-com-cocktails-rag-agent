from langchain_ollama import OllamaLLM


class ExtractionDataValidator:
    def __init__(self):
        self.llm = OllamaLLM(model="mistral:7b", temperature=0.2)
