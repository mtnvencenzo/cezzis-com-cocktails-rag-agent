import dataclasses
from dataclasses import dataclass
from typing import List

from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


@dataclass
class CocktailDescriptionChunk:
    category: str
    description: str


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
