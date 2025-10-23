from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cocktail_updated_notification_model import CocktailUpdatedNotificationModel

T = TypeVar("T", bound="UpdateAccountOwnedNotificationSettingsRq")


@_attrs_define
class UpdateAccountOwnedNotificationSettingsRq:
    on_new_cocktail_additions: CocktailUpdatedNotificationModel
    """ The notification setting to use when new cocktail addtions are added """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        on_new_cocktail_additions = self.on_new_cocktail_additions.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "onNewCocktailAdditions": on_new_cocktail_additions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        on_new_cocktail_additions = CocktailUpdatedNotificationModel(d.pop("onNewCocktailAdditions"))

        update_account_owned_notification_settings_rq = cls(
            on_new_cocktail_additions=on_new_cocktail_additions,
        )

        update_account_owned_notification_settings_rq.additional_properties = d
        return update_account_owned_notification_settings_rq

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
