from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_address_model import AccountAddressModel


T = TypeVar("T", bound="UpdateAccountOwnedProfileRq")


@_attrs_define
class UpdateAccountOwnedProfileRq:
    given_name: str
    """ The given name on the account """
    family_name: str
    """ The family name on the account """
    display_name: str
    """ The display for the account visible to other users """
    primary_address: "AccountAddressModel"
    """ The optional primary address listed with the account """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        given_name = self.given_name

        family_name = self.family_name

        display_name = self.display_name

        primary_address = self.primary_address.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "givenName": given_name,
                "familyName": family_name,
                "displayName": display_name,
                "primaryAddress": primary_address,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_address_model import AccountAddressModel

        d = dict(src_dict)
        given_name = d.pop("givenName")

        family_name = d.pop("familyName")

        display_name = d.pop("displayName")

        primary_address = AccountAddressModel.from_dict(d.pop("primaryAddress"))

        update_account_owned_profile_rq = cls(
            given_name=given_name,
            family_name=family_name,
            display_name=display_name,
            primary_address=primary_address,
        )

        update_account_owned_profile_rq.additional_properties = d
        return update_account_owned_profile_rq

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
