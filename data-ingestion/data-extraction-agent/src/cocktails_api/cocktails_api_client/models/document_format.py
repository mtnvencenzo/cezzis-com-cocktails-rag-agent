from enum import Enum


class DocumentFormat(str, Enum):
    MARKDOWN = "markdown"

    def __str__(self) -> str:
        return str(self.value)
