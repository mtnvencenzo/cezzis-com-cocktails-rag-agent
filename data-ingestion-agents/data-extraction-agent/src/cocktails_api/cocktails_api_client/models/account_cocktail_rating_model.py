from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountCocktailRatingModel")


@_attrs_define
class AccountCocktailRatingModel:
    """The cocktail rating values"""

    one_stars: int
    """ The number of one star ratings """
    two_stars: int
    """ The number of two star ratings """
    three_stars: int
    """ The number of three star ratings """
    four_stars: int
    """ The number of four star ratings """
    five_stars: int
    """ The number of five star ratings """
    total_stars: int
    """ The total number of stars given """
    rating: float
    """ The actual overal rating """
    rating_count: int
    """ The total number of ratings given """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        one_stars = self.one_stars

        two_stars = self.two_stars

        three_stars = self.three_stars

        four_stars = self.four_stars

        five_stars = self.five_stars

        total_stars = self.total_stars

        rating = self.rating

        rating_count = self.rating_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oneStars": one_stars,
                "twoStars": two_stars,
                "threeStars": three_stars,
                "fourStars": four_stars,
                "fiveStars": five_stars,
                "totalStars": total_stars,
                "rating": rating,
                "ratingCount": rating_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        one_stars = d.pop("oneStars")

        two_stars = d.pop("twoStars")

        three_stars = d.pop("threeStars")

        four_stars = d.pop("fourStars")

        five_stars = d.pop("fiveStars")

        total_stars = d.pop("totalStars")

        rating = d.pop("rating")

        rating_count = d.pop("ratingCount")

        account_cocktail_rating_model = cls(
            one_stars=one_stars,
            two_stars=two_stars,
            three_stars=three_stars,
            four_stars=four_stars,
            five_stars=five_stars,
            total_stars=total_stars,
            rating=rating,
            rating_count=rating_count,
        )

        account_cocktail_rating_model.additional_properties = d
        return account_cocktail_rating_model

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
