from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RateCocktailRq")


@_attrs_define
class RateCocktailRq:
    cocktail_id: str
    """ The cocktail identifier """
    stars: int
    """ The rating for the cocktail (1-5) """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cocktail_id = self.cocktail_id

        stars = self.stars

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cocktailId": cocktail_id,
                "stars": stars,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cocktail_id = d.pop("cocktailId")

        stars = d.pop("stars")

        rate_cocktail_rq = cls(
            cocktail_id=cocktail_id,
            stars=stars,
        )

        rate_cocktail_rq.additional_properties = d
        return rate_cocktail_rq

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
