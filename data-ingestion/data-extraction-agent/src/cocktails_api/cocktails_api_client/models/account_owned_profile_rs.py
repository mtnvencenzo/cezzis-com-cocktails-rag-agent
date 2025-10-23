from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_accessibility_settings_model import AccountAccessibilitySettingsModel
    from ..models.account_address_model import AccountAddressModel
    from ..models.account_notification_settings_model import AccountNotificationSettingsModel


T = TypeVar("T", bound="AccountOwnedProfileRs")


@_attrs_define
class AccountOwnedProfileRs:
    subject_id: str
    """ The federated subject identifier for the account """
    login_email: str
    """ The login email address for the account """
    email: str
    """ The email address for the account """
    given_name: str
    """ The given name on the account """
    family_name: str
    """ The family name on the account """
    avatar_uri: str
    """ The avatar image uri for the account """
    primary_address: "AccountAddressModel"
    """ The optional primary address listed with the account """
    display_name: str
    """ The display name for the account visible to other users """
    accessibility: "AccountAccessibilitySettingsModel"
    """ The accessibility settings for the account """
    favorite_cocktails: list[str]
    """ The list of favorite cocktails """
    notifications: "AccountNotificationSettingsModel"
    """ The notification settings for the account """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subject_id = self.subject_id

        login_email = self.login_email

        email = self.email

        given_name = self.given_name

        family_name = self.family_name

        avatar_uri = self.avatar_uri

        primary_address = self.primary_address.to_dict()

        display_name = self.display_name

        accessibility = self.accessibility.to_dict()

        favorite_cocktails = self.favorite_cocktails

        notifications = self.notifications.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subjectId": subject_id,
                "loginEmail": login_email,
                "email": email,
                "givenName": given_name,
                "familyName": family_name,
                "avatarUri": avatar_uri,
                "primaryAddress": primary_address,
                "displayName": display_name,
                "accessibility": accessibility,
                "favoriteCocktails": favorite_cocktails,
                "notifications": notifications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_accessibility_settings_model import AccountAccessibilitySettingsModel
        from ..models.account_address_model import AccountAddressModel
        from ..models.account_notification_settings_model import AccountNotificationSettingsModel

        d = dict(src_dict)
        subject_id = d.pop("subjectId")

        login_email = d.pop("loginEmail")

        email = d.pop("email")

        given_name = d.pop("givenName")

        family_name = d.pop("familyName")

        avatar_uri = d.pop("avatarUri")

        primary_address = AccountAddressModel.from_dict(d.pop("primaryAddress"))

        display_name = d.pop("displayName")

        accessibility = AccountAccessibilitySettingsModel.from_dict(d.pop("accessibility"))

        favorite_cocktails = cast(list[str], d.pop("favoriteCocktails"))

        notifications = AccountNotificationSettingsModel.from_dict(d.pop("notifications"))

        account_owned_profile_rs = cls(
            subject_id=subject_id,
            login_email=login_email,
            email=email,
            given_name=given_name,
            family_name=family_name,
            avatar_uri=avatar_uri,
            primary_address=primary_address,
            display_name=display_name,
            accessibility=accessibility,
            favorite_cocktails=favorite_cocktails,
            notifications=notifications,
        )

        account_owned_profile_rs.additional_properties = d
        return account_owned_profile_rs

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
