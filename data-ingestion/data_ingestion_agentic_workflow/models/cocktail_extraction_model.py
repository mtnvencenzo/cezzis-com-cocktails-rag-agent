from dataclasses import dataclass

from data_ingestion_agentic_workflow.models.cocktail_models import CocktailModel


@dataclass
class CocktailExtractionModel:
    cocktail_model: CocktailModel
    extraction_text: str
