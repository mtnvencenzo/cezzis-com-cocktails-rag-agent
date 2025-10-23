from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cocktail_recommendation_model import CocktailRecommendationModel


T = TypeVar("T", bound="CocktailRecommendationRq")


@_attrs_define
class CocktailRecommendationRq:
    recommendation: "CocktailRecommendationModel"
    """ The cocktail recommendation model """
    verification_code: str
    """ The google recaptcha verification code returned after being valid """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recommendation = self.recommendation.to_dict()

        verification_code = self.verification_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recommendation": recommendation,
                "verificationCode": verification_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cocktail_recommendation_model import CocktailRecommendationModel

        d = dict(src_dict)
        recommendation = CocktailRecommendationModel.from_dict(d.pop("recommendation"))

        verification_code = d.pop("verificationCode")

        cocktail_recommendation_rq = cls(
            recommendation=recommendation,
            verification_code=verification_code,
        )

        cocktail_recommendation_rq.additional_properties = d
        return cocktail_recommendation_rq

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
