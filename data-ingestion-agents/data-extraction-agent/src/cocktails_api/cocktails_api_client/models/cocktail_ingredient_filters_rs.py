from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ingredient_filter_model import IngredientFilterModel
    from ..models.ingredient_filter_model_2 import IngredientFilterModel2
    from ..models.ingredient_filter_model_3 import IngredientFilterModel3
    from ..models.ingredient_filter_model_4 import IngredientFilterModel4
    from ..models.ingredient_filter_model_5 import IngredientFilterModel5
    from ..models.ingredient_filter_model_6 import IngredientFilterModel6
    from ..models.ingredient_filter_model_7 import IngredientFilterModel7
    from ..models.ingredient_filter_model_8 import IngredientFilterModel8
    from ..models.ingredient_filter_model_9 import IngredientFilterModel9
    from ..models.ingredient_filter_model_10 import IngredientFilterModel10
    from ..models.ingredient_filter_model_11 import IngredientFilterModel11
    from ..models.ingredient_filter_model_12 import IngredientFilterModel12
    from ..models.ingredient_filter_model_13 import IngredientFilterModel13


T = TypeVar("T", bound="CocktailIngredientFiltersRs")


@_attrs_define
class CocktailIngredientFiltersRs:
    glassware: list["IngredientFilterModel"]
    """ The cocktail ingredient filters for searching against recommended glassware """
    spirits: list["IngredientFilterModel2"]
    """ The cocktail ingredient filters for searching against spirits """
    liqueurs: list["IngredientFilterModel3"]
    """ The cocktail ingredient filters for searching against liqueurs """
    fruits: list["IngredientFilterModel4"]
    """ The cocktail ingredient filters for searching against friuts """
    vegetables: list["IngredientFilterModel5"]
    """ The cocktail ingredient filters for searching against vegetables """
    herbs_and_flowers: list["IngredientFilterModel6"]
    """ The cocktail ingredient filters for searching against herbs and flowers """
    syrups_and_sauces: list["IngredientFilterModel7"]
    """ The cocktail ingredient filters for searching against syrups and sauces """
    bitters: list["IngredientFilterModel8"]
    """ The cocktail ingredient filters for searching against bitters """
    proteins: list["IngredientFilterModel9"]
    """ The cocktail ingredient filters for searching against proteins """
    juices: list["IngredientFilterModel10"]
    """ The cocktail ingredient filters for searching against juices """
    dilutions: list["IngredientFilterModel11"]
    """ The cocktail ingredient filters for searching against dilutions """
    beer_wine_champagne: list["IngredientFilterModel12"]
    """ The cocktail ingredient filters for searching against beers, wines and champagnes """
    eras: list["IngredientFilterModel13"]
    """ The cocktail ingredient filters for searching against eras when cocktails were established """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        glassware = []
        for glassware_item_data in self.glassware:
            glassware_item = glassware_item_data.to_dict()
            glassware.append(glassware_item)

        spirits = []
        for spirits_item_data in self.spirits:
            spirits_item = spirits_item_data.to_dict()
            spirits.append(spirits_item)

        liqueurs = []
        for liqueurs_item_data in self.liqueurs:
            liqueurs_item = liqueurs_item_data.to_dict()
            liqueurs.append(liqueurs_item)

        fruits = []
        for fruits_item_data in self.fruits:
            fruits_item = fruits_item_data.to_dict()
            fruits.append(fruits_item)

        vegetables = []
        for vegetables_item_data in self.vegetables:
            vegetables_item = vegetables_item_data.to_dict()
            vegetables.append(vegetables_item)

        herbs_and_flowers = []
        for herbs_and_flowers_item_data in self.herbs_and_flowers:
            herbs_and_flowers_item = herbs_and_flowers_item_data.to_dict()
            herbs_and_flowers.append(herbs_and_flowers_item)

        syrups_and_sauces = []
        for syrups_and_sauces_item_data in self.syrups_and_sauces:
            syrups_and_sauces_item = syrups_and_sauces_item_data.to_dict()
            syrups_and_sauces.append(syrups_and_sauces_item)

        bitters = []
        for bitters_item_data in self.bitters:
            bitters_item = bitters_item_data.to_dict()
            bitters.append(bitters_item)

        proteins = []
        for proteins_item_data in self.proteins:
            proteins_item = proteins_item_data.to_dict()
            proteins.append(proteins_item)

        juices = []
        for juices_item_data in self.juices:
            juices_item = juices_item_data.to_dict()
            juices.append(juices_item)

        dilutions = []
        for dilutions_item_data in self.dilutions:
            dilutions_item = dilutions_item_data.to_dict()
            dilutions.append(dilutions_item)

        beer_wine_champagne = []
        for beer_wine_champagne_item_data in self.beer_wine_champagne:
            beer_wine_champagne_item = beer_wine_champagne_item_data.to_dict()
            beer_wine_champagne.append(beer_wine_champagne_item)

        eras = []
        for eras_item_data in self.eras:
            eras_item = eras_item_data.to_dict()
            eras.append(eras_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "glassware": glassware,
                "spirits": spirits,
                "liqueurs": liqueurs,
                "fruits": fruits,
                "vegetables": vegetables,
                "herbsAndFlowers": herbs_and_flowers,
                "syrupsAndSauces": syrups_and_sauces,
                "bitters": bitters,
                "proteins": proteins,
                "juices": juices,
                "dilutions": dilutions,
                "beerWineChampagne": beer_wine_champagne,
                "eras": eras,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_filter_model import IngredientFilterModel
        from ..models.ingredient_filter_model_2 import IngredientFilterModel2
        from ..models.ingredient_filter_model_3 import IngredientFilterModel3
        from ..models.ingredient_filter_model_4 import IngredientFilterModel4
        from ..models.ingredient_filter_model_5 import IngredientFilterModel5
        from ..models.ingredient_filter_model_6 import IngredientFilterModel6
        from ..models.ingredient_filter_model_7 import IngredientFilterModel7
        from ..models.ingredient_filter_model_8 import IngredientFilterModel8
        from ..models.ingredient_filter_model_9 import IngredientFilterModel9
        from ..models.ingredient_filter_model_10 import IngredientFilterModel10
        from ..models.ingredient_filter_model_11 import IngredientFilterModel11
        from ..models.ingredient_filter_model_12 import IngredientFilterModel12
        from ..models.ingredient_filter_model_13 import IngredientFilterModel13

        d = dict(src_dict)
        glassware = []
        _glassware = d.pop("glassware")
        for glassware_item_data in _glassware:
            glassware_item = IngredientFilterModel.from_dict(glassware_item_data)

            glassware.append(glassware_item)

        spirits = []
        _spirits = d.pop("spirits")
        for spirits_item_data in _spirits:
            spirits_item = IngredientFilterModel2.from_dict(spirits_item_data)

            spirits.append(spirits_item)

        liqueurs = []
        _liqueurs = d.pop("liqueurs")
        for liqueurs_item_data in _liqueurs:
            liqueurs_item = IngredientFilterModel3.from_dict(liqueurs_item_data)

            liqueurs.append(liqueurs_item)

        fruits = []
        _fruits = d.pop("fruits")
        for fruits_item_data in _fruits:
            fruits_item = IngredientFilterModel4.from_dict(fruits_item_data)

            fruits.append(fruits_item)

        vegetables = []
        _vegetables = d.pop("vegetables")
        for vegetables_item_data in _vegetables:
            vegetables_item = IngredientFilterModel5.from_dict(vegetables_item_data)

            vegetables.append(vegetables_item)

        herbs_and_flowers = []
        _herbs_and_flowers = d.pop("herbsAndFlowers")
        for herbs_and_flowers_item_data in _herbs_and_flowers:
            herbs_and_flowers_item = IngredientFilterModel6.from_dict(herbs_and_flowers_item_data)

            herbs_and_flowers.append(herbs_and_flowers_item)

        syrups_and_sauces = []
        _syrups_and_sauces = d.pop("syrupsAndSauces")
        for syrups_and_sauces_item_data in _syrups_and_sauces:
            syrups_and_sauces_item = IngredientFilterModel7.from_dict(syrups_and_sauces_item_data)

            syrups_and_sauces.append(syrups_and_sauces_item)

        bitters = []
        _bitters = d.pop("bitters")
        for bitters_item_data in _bitters:
            bitters_item = IngredientFilterModel8.from_dict(bitters_item_data)

            bitters.append(bitters_item)

        proteins = []
        _proteins = d.pop("proteins")
        for proteins_item_data in _proteins:
            proteins_item = IngredientFilterModel9.from_dict(proteins_item_data)

            proteins.append(proteins_item)

        juices = []
        _juices = d.pop("juices")
        for juices_item_data in _juices:
            juices_item = IngredientFilterModel10.from_dict(juices_item_data)

            juices.append(juices_item)

        dilutions = []
        _dilutions = d.pop("dilutions")
        for dilutions_item_data in _dilutions:
            dilutions_item = IngredientFilterModel11.from_dict(dilutions_item_data)

            dilutions.append(dilutions_item)

        beer_wine_champagne = []
        _beer_wine_champagne = d.pop("beerWineChampagne")
        for beer_wine_champagne_item_data in _beer_wine_champagne:
            beer_wine_champagne_item = IngredientFilterModel12.from_dict(beer_wine_champagne_item_data)

            beer_wine_champagne.append(beer_wine_champagne_item)

        eras = []
        _eras = d.pop("eras")
        for eras_item_data in _eras:
            eras_item = IngredientFilterModel13.from_dict(eras_item_data)

            eras.append(eras_item)

        cocktail_ingredient_filters_rs = cls(
            glassware=glassware,
            spirits=spirits,
            liqueurs=liqueurs,
            fruits=fruits,
            vegetables=vegetables,
            herbs_and_flowers=herbs_and_flowers,
            syrups_and_sauces=syrups_and_sauces,
            bitters=bitters,
            proteins=proteins,
            juices=juices,
            dilutions=dilutions,
            beer_wine_champagne=beer_wine_champagne,
            eras=eras,
        )

        cocktail_ingredient_filters_rs.additional_properties = d
        return cocktail_ingredient_filters_rs

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
