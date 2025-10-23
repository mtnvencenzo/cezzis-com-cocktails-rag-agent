from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_cocktail_rating_model import AccountCocktailRatingModel
    from ..models.account_cocktail_ratings_model import AccountCocktailRatingsModel


T = TypeVar("T", bound="RateCocktailRs")


@_attrs_define
class RateCocktailRs:
    ratings: list["AccountCocktailRatingsModel"]
    """ The cocktail ratings """
    cocktail_id: str
    """ The cocktail identifier """
    cocktail_rating: "AccountCocktailRatingModel"
    """ The cocktail rating values """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ratings = []
        for ratings_item_data in self.ratings:
            ratings_item = ratings_item_data.to_dict()
            ratings.append(ratings_item)

        cocktail_id = self.cocktail_id

        cocktail_rating = self.cocktail_rating.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ratings": ratings,
                "cocktailId": cocktail_id,
                "cocktailRating": cocktail_rating,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_cocktail_rating_model import AccountCocktailRatingModel
        from ..models.account_cocktail_ratings_model import AccountCocktailRatingsModel

        d = dict(src_dict)
        ratings = []
        _ratings = d.pop("ratings")
        for ratings_item_data in _ratings:
            ratings_item = AccountCocktailRatingsModel.from_dict(ratings_item_data)

            ratings.append(ratings_item)

        cocktail_id = d.pop("cocktailId")

        cocktail_rating = AccountCocktailRatingModel.from_dict(d.pop("cocktailRating"))

        rate_cocktail_rs = cls(
            ratings=ratings,
            cocktail_id=cocktail_id,
            cocktail_rating=cocktail_rating,
        )

        rate_cocktail_rs.additional_properties = d
        return rate_cocktail_rs

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
