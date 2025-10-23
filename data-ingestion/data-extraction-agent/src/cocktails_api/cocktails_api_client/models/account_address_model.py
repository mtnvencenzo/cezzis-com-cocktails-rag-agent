from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountAddressModel")


@_attrs_define
class AccountAddressModel:
    """The optional primary address listed with the account"""

    address_line_1: str
    """ The primary street address. """
    address_line_2: str
    """ The secondary street address building sub divider """
    city: str
    """ The city the address is within """
    region: str
    """ The state or province """
    sub_region: str
    """ The state or province divered such as county """
    postal_code: str
    """ The postal or zip code """
    country: str
    """ The country """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address_line_1 = self.address_line_1

        address_line_2 = self.address_line_2

        city = self.city

        region = self.region

        sub_region = self.sub_region

        postal_code = self.postal_code

        country = self.country

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "addressLine1": address_line_1,
                "addressLine2": address_line_2,
                "city": city,
                "region": region,
                "subRegion": sub_region,
                "postalCode": postal_code,
                "country": country,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address_line_1 = d.pop("addressLine1")

        address_line_2 = d.pop("addressLine2")

        city = d.pop("city")

        region = d.pop("region")

        sub_region = d.pop("subRegion")

        postal_code = d.pop("postalCode")

        country = d.pop("country")

        account_address_model = cls(
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            region=region,
            sub_region=sub_region,
            postal_code=postal_code,
            country=country,
        )

        account_address_model.additional_properties = d
        return account_address_model

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
