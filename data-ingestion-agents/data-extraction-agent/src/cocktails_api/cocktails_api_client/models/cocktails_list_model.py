from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.glassware_type_model import GlasswareTypeModel

if TYPE_CHECKING:
    from ..models.ingredient_model import IngredientModel


T = TypeVar("T", bound="CocktailsListModel")


@_attrs_define
class CocktailsListModel:
    id: str
    """ The cocktail recipe unique identifier """
    title: str
    """ The name of the cocktail recipe """
    descriptive_title: str
    """ A more descriptive title for the cocktail recipe, generally used as an editorial title """
    rating: float
    """ The overral rating for the recipe """
    ingredients: list["IngredientModel"]
    """ The list of ingredients that make up the cocktail recipe """
    is_iba: bool
    """ Whether or not the cocktail represented by this recipe is recognized by the International Bartenders
    Association """
    serves: int
    """ The number of people the cocktail recipe serves """
    prep_time_minutes: int
    """ The average number of minutes to build the cocktail using this recipe """
    main_images: list[str]
    """ A list of primary image uris for the cocktail recipe """
    search_tiles: list[str]
    """ A list of secondary, smaller sized image uris for the cocktail recipe """
    glassware: list[GlasswareTypeModel]
    """ The recommended glassware to use when serving the cocktail """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        descriptive_title = self.descriptive_title

        rating = self.rating

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        is_iba = self.is_iba

        serves = self.serves

        prep_time_minutes = self.prep_time_minutes

        main_images = self.main_images

        search_tiles = self.search_tiles

        glassware = []
        for glassware_item_data in self.glassware:
            glassware_item = glassware_item_data.value
            glassware.append(glassware_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "descriptiveTitle": descriptive_title,
                "rating": rating,
                "ingredients": ingredients,
                "isIba": is_iba,
                "serves": serves,
                "prepTimeMinutes": prep_time_minutes,
                "mainImages": main_images,
                "searchTiles": search_tiles,
                "glassware": glassware,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_model import IngredientModel

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        descriptive_title = d.pop("descriptiveTitle")

        rating = d.pop("rating")

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = IngredientModel.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        is_iba = d.pop("isIba")

        serves = d.pop("serves")

        prep_time_minutes = d.pop("prepTimeMinutes")

        main_images = cast(list[str], d.pop("mainImages"))

        search_tiles = cast(list[str], d.pop("searchTiles"))

        glassware = []
        _glassware = d.pop("glassware")
        for glassware_item_data in _glassware:
            glassware_item = GlasswareTypeModel(glassware_item_data)

            glassware.append(glassware_item)

        cocktails_list_model = cls(
            id=id,
            title=title,
            descriptive_title=descriptive_title,
            rating=rating,
            ingredients=ingredients,
            is_iba=is_iba,
            serves=serves,
            prep_time_minutes=prep_time_minutes,
            main_images=main_images,
            search_tiles=search_tiles,
            glassware=glassware,
        )

        cocktails_list_model.additional_properties = d
        return cocktails_list_model

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
