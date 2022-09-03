from pathlib import Path

import lxml.etree as ET
import pytest
from pydantic.error_wrappers import ValidationError

from kaatio_plan_validator.api_v1 import constants, exceptions, models


def test_model_land_use_feature_collection_from_xml_source_with_broken_xml(
    file_xml_broken: Path,
):

    with pytest.raises(exceptions.ParserException):
        models.LandUseFeatureCollection.from_xml_source(
            source=file_xml_broken,
        )


def test_model_land_use_feature_collection_from_xml_source_with_invalid_xml(
    file_xml_invalid: Path,
):

    with pytest.raises(exceptions.SchemaException):
        models.LandUseFeatureCollection.from_xml_source(
            source=file_xml_invalid,
        )


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1(
    file_xml_valid_1: Path,
    file_xml_valid_1_gen: Path,
):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=file_xml_valid_1,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(file_xml_valid_1_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1_gen(
    file_xml_valid_1_gen: Path,
    file_xml_valid_1_gen_result: Path,
):

    if file_xml_valid_1_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=file_xml_valid_1_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(file_xml_valid_1_gen_result, "w") as output:
        output.write(model.to_string())


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2(
    file_xml_valid_2: Path,
    file_xml_valid_2_gen: Path,
):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=file_xml_valid_2,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(file_xml_valid_2_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2_gen(
    file_xml_valid_2_gen: Path,
    file_xml_valid_2_gen_result: Path,
):

    if file_xml_valid_2_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=file_xml_valid_2_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(file_xml_valid_2_gen_result, "w") as output:
        output.write(model.to_string())


def test_model_spatial_plan_raises_error_when_plan_identifier_element_is_missing(
    xml_element_spatial_plan: ET._Element,
):

    plan_identifier_element: ET._Element = xml_element_spatial_plan.xpath(
        constants.XPATH_PLAN_IDENTIFIER, **constants.NAMESPACES
    )[0]
    xml_element_spatial_plan.remove(plan_identifier_element)

    with pytest.raises(ValidationError) as err:
        models.SpatialPlan.from_orm(xml_element_spatial_plan)
    assert err.value.errors() == [
        {
            "loc": ("splan:SpatialPlan/splan:planIdentifier",),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_model_spatial_plan_raises_error_when_boundary_is_not_valid(
    xml_element_spatial_plan: ET._Element,
    xml_element_polygon_invalid: ET._Element,
):

    boundary_element: ET._Element = xml_element_spatial_plan.xpath(constants.XPATH_BOUNDARY, **constants.NAMESPACES)[0]
    geometry_element_child = list(boundary_element)[0]
    boundary_element.replace(geometry_element_child, xml_element_polygon_invalid)
    with pytest.raises(ValidationError) as err:
        models.SpatialPlan.from_orm(xml_element_spatial_plan)
    assert err.value.errors() == [
        {
            "loc": ("splan:SpatialPlan/lud-core:boundary",),
            "msg": "boundary is not valid",
            "type": "assertion_error",
        }
    ]


def test_model_spatial_plan_raises_error_when_plan_identifier_element_text_is_none(
    xml_element_spatial_plan: ET._Element,
):

    plan_identifier_element: ET._Element = xml_element_spatial_plan.xpath(
        constants.XPATH_PLAN_IDENTIFIER, **constants.NAMESPACES
    )[0]
    plan_identifier_element.text = None

    with pytest.raises(ValidationError) as err:
        models.SpatialPlan.from_orm(xml_element_spatial_plan)
    assert err.value.errors() == [
        {
            "loc": ("splan:SpatialPlan/splan:planIdentifier",),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_model_plan_object_raises_error_when_geometry_is_not_valid(
    xml_element_plan_object: ET._Element,
    xml_element_polygon_invalid: ET._Element,
):

    geometry_element: ET._Element = xml_element_plan_object.xpath(constants.XPATH_GEOMETRY, **constants.NAMESPACES)[0]
    geometry_element_child = list(geometry_element)[0]
    geometry_element.replace(geometry_element_child, xml_element_polygon_invalid)
    with pytest.raises(ValidationError) as err:
        models.PlanObject.from_orm(xml_element_plan_object)
    assert err.value.errors() == [
        {
            "loc": ("splan:PlanObject/splan:geometry",),
            "msg": "geometry is not valid",
            "type": "assertion_error",
        }
    ]
