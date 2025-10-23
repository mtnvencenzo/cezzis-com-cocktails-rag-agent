from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cocktail_favorite_action_model import CocktailFavoriteActionModel


T = TypeVar("T", bound="ManageFavoriteCocktailsRq")


@_attrs_define
class ManageFavoriteCocktailsRq:
    cocktail_actions: list["CocktailFavoriteActionModel"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cocktail_actions = []
        for cocktail_actions_item_data in self.cocktail_actions:
            cocktail_actions_item = cocktail_actions_item_data.to_dict()
            cocktail_actions.append(cocktail_actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cocktailActions": cocktail_actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cocktail_favorite_action_model import CocktailFavoriteActionModel

        d = dict(src_dict)
        cocktail_actions = []
        _cocktail_actions = d.pop("cocktailActions")
        for cocktail_actions_item_data in _cocktail_actions:
            cocktail_actions_item = CocktailFavoriteActionModel.from_dict(cocktail_actions_item_data)

            cocktail_actions.append(cocktail_actions_item)

        manage_favorite_cocktails_rq = cls(
            cocktail_actions=cocktail_actions,
        )

        manage_favorite_cocktails_rq.additional_properties = d
        return manage_favorite_cocktails_rq

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
