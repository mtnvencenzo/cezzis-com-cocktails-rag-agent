from dataclasses import dataclass

from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


@dataclass
class CocktailExtractionModel:
    cocktail_model: CocktailModel
    extraction_text: str

    def as_serializable_json(self) -> bytes:
        from pydantic import TypeAdapter

        serializable_dict = {
            "cocktail_model": self.cocktail_model.model_dump(),
            "extraction_text": self.extraction_text,
        }
        return TypeAdapter(dict).dump_json(serializable_dict)
