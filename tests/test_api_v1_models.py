import uuid
from pathlib import Path

import lxml.etree as ET
import pytest
from pydantic.error_wrappers import ValidationError
from pytest import FixtureRequest

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


@pytest.mark.parametrize(
    "input,output,gml_id_reset",
    [
        ("file_xml_valid_1", "file_xml_valid_1_gen", True),
        ("file_xml_valid_1_gen", "file_xml_valid_1_gen_result", False),
        ("file_xml_valid_2", "file_xml_valid_2_gen", True),
        ("file_xml_valid_2_gen", "file_xml_valid_2_gen_result", False),
    ],
)
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml(
    request: FixtureRequest,
    input: str,
    output: str,
    gml_id_reset: bool,
):
    file_xml_input: Path = request.getfixturevalue(input)
    file_xml_output: Path = request.getfixturevalue(output)

    assert file_xml_input.exists()

    model = models.LandUseFeatureCollection.from_xml_source(
        source=file_xml_input,
    )
    assert model
    before_spatial_plan_gml_id = str(
        model.spatial_plan.xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    before_pe_plan_gml_id = str(model.pe_plans[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]).split(
        "."
    )
    before_plan_object_gml_id = str(
        model.plan_objects[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    before_plan_order_gml_id = str(
        model.plan_orders[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    before_planner_gml_id = str(model.planners[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]).split(
        "."
    )
    model.update_ids_and_refs()
    after_spatial_plan_gml_id = str(
        model.spatial_plan.xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    after_pe_plan_gml_id = str(model.pe_plans[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]).split(
        "."
    )
    after_plan_object_gml_id = str(
        model.plan_objects[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    after_plan_order_gml_id = str(
        model.plan_orders[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
    ).split(".")
    after_planner_gml_id = str(model.planners[0].xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]).split(
        "."
    )
    if gml_id_reset:
        # Received gml:id values did not follow format: 'id-uuid.uuid' - new gml:id created
        assert uuid.UUID(after_spatial_plan_gml_id[0].removeprefix("id-"))
        assert uuid.UUID(after_spatial_plan_gml_id[1])
        assert uuid.UUID(after_pe_plan_gml_id[0].removeprefix("id-"))
        assert uuid.UUID(after_pe_plan_gml_id[1])
        assert uuid.UUID(after_plan_object_gml_id[0].removeprefix("id-"))
        assert uuid.UUID(after_plan_object_gml_id[1])
        assert uuid.UUID(after_plan_order_gml_id[0].removeprefix("id-"))
        assert uuid.UUID(after_plan_order_gml_id[1])
        assert uuid.UUID(after_planner_gml_id[0].removeprefix("id-"))
        assert uuid.UUID(after_planner_gml_id[1])
    else:
        # Received gml:id values did follow format: 'id-uuid.uuid' - latter uuid updated
        assert before_spatial_plan_gml_id[0] == after_spatial_plan_gml_id[0]
        assert before_spatial_plan_gml_id[1] != after_spatial_plan_gml_id[1]
        assert before_pe_plan_gml_id[0] == after_pe_plan_gml_id[0]
        assert before_pe_plan_gml_id[1] != after_pe_plan_gml_id[1]
        assert before_plan_object_gml_id[0] == after_plan_object_gml_id[0]
        assert before_plan_object_gml_id[1] != after_plan_object_gml_id[1]
        assert before_plan_order_gml_id[0] == after_plan_order_gml_id[0]
        assert before_plan_order_gml_id[1] != after_plan_order_gml_id[1]
        assert before_planner_gml_id[0] == after_planner_gml_id[0]
        assert before_planner_gml_id[1] != after_planner_gml_id[1]

    with open(file_xml_output, "w") as output:
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
