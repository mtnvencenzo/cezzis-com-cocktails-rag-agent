import dataclasses
from dataclasses import dataclass
from typing import List
from uuid import NAMESPACE_DNS, uuid5

from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


@dataclass
class CocktailDescriptionChunk:
    category: str
    description: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class CocktailChunkingModel:
    cocktail_model: CocktailModel
    chunks: List[CocktailDescriptionChunk]

    def as_serializable_json(self) -> bytes:
        from pydantic import TypeAdapter

        serializable_dict = {
            "cocktail_model": self.cocktail_model.model_dump(),
            "chunks": [dataclasses.asdict(chunk) for chunk in self.chunks],
        }
        return TypeAdapter(dict).dump_json(serializable_dict)

    def get_chunk_uuids(self) -> List[str]:
        return [
            str(uuid5(NAMESPACE_DNS, f"{self.cocktail_model.id}-{chunk.category.replace(' ', '-')}"))
            for chunk in self.chunks
        ]
