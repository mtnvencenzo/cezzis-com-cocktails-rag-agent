import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.glassware_type_model import GlasswareTypeModel

if TYPE_CHECKING:
    from ..models.cocktail_image_model import CocktailImageModel
    from ..models.cocktail_image_model_2 import CocktailImageModel2
    from ..models.cocktail_rating_model import CocktailRatingModel
    from ..models.ingredient_model import IngredientModel
    from ..models.instruction_step_model import InstructionStepModel


T = TypeVar("T", bound="CocktailModel")


@_attrs_define
class CocktailModel:
    """The cocktail recipe model"""

    id: str
    """ The cocktail recipe unique identifier """
    title: str
    """ The name of the cocktail recipe """
    descriptive_title: str
    """ A more descriptive title for the cocktail recipe, generally used as an editorial title """
    description: str
    """ A brief editorial description for the cocktail recipe """
    content: str
    """ The complete descriptive cocktail recipe including ingredients, directions and historical information in
    markdown format """
    published_on: datetime.datetime
    """ The date this cocktail recipe was published on Cezzis.Com """
    modified_on: datetime.datetime
    """ The date this cocktail recipe was last modified on Cezzis.Com """
    serves: int
    """ The number of people the cocktail recipe serves """
    prep_time_minutes: int
    """ The average number of minutes to build the cocktail using this recipe """
    is_iba: bool
    """ Whether or not the cocktail represented by this recipe is recognized by the International Bartenders
    Association """
    main_images: list["CocktailImageModel"]
    """ A list of primary images for the cocktail recipe """
    search_tiles: list["CocktailImageModel2"]
    """ A list of secondary, smaller sized images for the cocktail recipe """
    glassware: list[GlasswareTypeModel]
    """ The recommended glassware to use when serving the cocktail """
    rating: "CocktailRatingModel"
    """ A ratings for this cocktail """
    searchable_titles: list[str]
    """ A list of titles that are queried against when issuing cocktail recipe search queries """
    tags: list[str]
    """ A list of taxonomy tags defining the cocktail recipe """
    ingredients: list["IngredientModel"]
    """ The list of ingredients that make up the cocktail recipe """
    instructions: list["InstructionStepModel"]
    """ The list of instructions to make the cocktail recipe """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        descriptive_title = self.descriptive_title

        description = self.description

        content = self.content

        published_on = self.published_on.isoformat()

        modified_on = self.modified_on.isoformat()

        serves = self.serves

        prep_time_minutes = self.prep_time_minutes

        is_iba = self.is_iba

        main_images = []
        for main_images_item_data in self.main_images:
            main_images_item = main_images_item_data.to_dict()
            main_images.append(main_images_item)

        search_tiles = []
        for search_tiles_item_data in self.search_tiles:
            search_tiles_item = search_tiles_item_data.to_dict()
            search_tiles.append(search_tiles_item)

        glassware = []
        for glassware_item_data in self.glassware:
            glassware_item = glassware_item_data.value
            glassware.append(glassware_item)

        rating = self.rating.to_dict()

        searchable_titles = self.searchable_titles

        tags = self.tags

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        instructions = []
        for instructions_item_data in self.instructions:
            instructions_item = instructions_item_data.to_dict()
            instructions.append(instructions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "descriptiveTitle": descriptive_title,
                "description": description,
                "content": content,
                "publishedOn": published_on,
                "modifiedOn": modified_on,
                "serves": serves,
                "prepTimeMinutes": prep_time_minutes,
                "isIba": is_iba,
                "mainImages": main_images,
                "searchTiles": search_tiles,
                "glassware": glassware,
                "rating": rating,
                "searchableTitles": searchable_titles,
                "tags": tags,
                "ingredients": ingredients,
                "instructions": instructions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cocktail_image_model import CocktailImageModel
        from ..models.cocktail_image_model_2 import CocktailImageModel2
        from ..models.cocktail_rating_model import CocktailRatingModel
        from ..models.ingredient_model import IngredientModel
        from ..models.instruction_step_model import InstructionStepModel

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        descriptive_title = d.pop("descriptiveTitle")

        description = d.pop("description")

        content = d.pop("content")

        published_on = isoparse(d.pop("publishedOn"))

        modified_on = isoparse(d.pop("modifiedOn"))

        serves = d.pop("serves")

        prep_time_minutes = d.pop("prepTimeMinutes")

        is_iba = d.pop("isIba")

        main_images = []
        _main_images = d.pop("mainImages")
        for main_images_item_data in _main_images:
            main_images_item = CocktailImageModel.from_dict(main_images_item_data)

            main_images.append(main_images_item)

        search_tiles = []
        _search_tiles = d.pop("searchTiles")
        for search_tiles_item_data in _search_tiles:
            search_tiles_item = CocktailImageModel2.from_dict(search_tiles_item_data)

            search_tiles.append(search_tiles_item)

        glassware = []
        _glassware = d.pop("glassware")
        for glassware_item_data in _glassware:
            glassware_item = GlasswareTypeModel(glassware_item_data)

            glassware.append(glassware_item)

        rating = CocktailRatingModel.from_dict(d.pop("rating"))

        searchable_titles = cast(list[str], d.pop("searchableTitles"))

        tags = cast(list[str], d.pop("tags"))

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = IngredientModel.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        instructions = []
        _instructions = d.pop("instructions")
        for instructions_item_data in _instructions:
            instructions_item = InstructionStepModel.from_dict(instructions_item_data)

            instructions.append(instructions_item)

        cocktail_model = cls(
            id=id,
            title=title,
            descriptive_title=descriptive_title,
            description=description,
            content=content,
            published_on=published_on,
            modified_on=modified_on,
            serves=serves,
            prep_time_minutes=prep_time_minutes,
            is_iba=is_iba,
            main_images=main_images,
            search_tiles=search_tiles,
            glassware=glassware,
            rating=rating,
            searchable_titles=searchable_titles,
            tags=tags,
            ingredients=ingredients,
            instructions=instructions,
        )

        cocktail_model.additional_properties = d
        return cocktail_model

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
