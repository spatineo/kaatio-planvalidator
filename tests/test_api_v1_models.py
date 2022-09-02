from pathlib import Path

import lxml.etree as ET
import pytest
from pydantic.error_wrappers import ValidationError

from kaatio_plan_validator.api_v1 import constants, exceptions, models


def test_model_land_use_feature_collection_from_xml_source_with_broken_xml(broken_xml: Path):

    with pytest.raises(exceptions.ParserException):
        models.LandUseFeatureCollection.from_xml_source(
            source=broken_xml,
        )


def test_model_land_use_feature_collection_from_xml_source_with_invalid_xml(invalid_xml: Path):

    with pytest.raises(exceptions.SchemaException):
        models.LandUseFeatureCollection.from_xml_source(
            source=invalid_xml,
        )


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1(valid_xml_1: Path, valid_xml_1_gen: Path):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=valid_xml_1,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(valid_xml_1_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1_gen(
    valid_xml_1_gen: Path,
    valid_xml_1_gen_result: Path,
):

    if valid_xml_1_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=valid_xml_1_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(valid_xml_1_gen_result, "w") as output:
        output.write(model.to_string())


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2(valid_xml_2: Path, valid_xml_2_gen: Path):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=valid_xml_2,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(valid_xml_2_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2_gen(
    valid_xml_2_gen: Path,
    valid_xml_2_gen_result: Path,
):

    if valid_xml_2_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=valid_xml_2_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(valid_xml_2_gen_result, "w") as output:
        output.write(model.to_string())


def test_model_spatial_plan_raises_error_when_plan_identifier_element_is_missing(xml_spatial_plan: ET._Element):

    plan_identifier_element: ET._Element = xml_spatial_plan.xpath(
        constants.XPATH_PLAN_IDENTIFIER, **constants.NAMESPACES
    )[0]
    xml_spatial_plan.remove(plan_identifier_element)

    with pytest.raises(ValidationError) as err:
        models.SpatialPlan.from_orm(xml_spatial_plan)
    assert err.value.errors() == [
        {
            "loc": ("splan:SpatialPlan/splan:planIdentifier",),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_model_spatial_plan_raises_error_when_plan_identifier_element_text_is_none(xml_spatial_plan: ET._Element):

    plan_identifier_element: ET._Element = xml_spatial_plan.xpath(
        constants.XPATH_PLAN_IDENTIFIER, **constants.NAMESPACES
    )[0]
    plan_identifier_element.text = None

    with pytest.raises(ValidationError) as err:
        models.SpatialPlan.from_orm(xml_spatial_plan)
    assert err.value.errors() == [
        {
            "loc": ("splan:SpatialPlan/splan:planIdentifier",),
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_model_plan_object_raises_error_when_geometry_is_not_valid(xml_plan_object: ET._Element):

    geometry = """
    <gml:Polygon srsName="urn:ogc:def:crs:EPSG::4326" gml:id="AK_SIPOO_5_lainvoimainen_kaava_sipoo_nevasgard.geom.2" xmlns:gml="http://www.opengis.net/gml/3.2">
	    <gml:exterior>
		    <gml:LinearRing>
			    <gml:posList>60.2866853 25.4095811 60.2866968 25.4092981 60.286163 25.409723 60.285766 25.409760 60.285861 25.409401</gml:posList>
		    </gml:LinearRing>
	    </gml:exterior>
    </gml:Polygon>
    """
    geometry_element: ET._Element = xml_plan_object.xpath(constants.XPATH_GEOMETRY, **constants.NAMESPACES)[0]
    new_element = ET.fromstring(geometry)
    old_element = list(geometry_element)[0]
    geometry_element.replace(old_element, new_element)
    with pytest.raises(ValidationError) as err:
        models.PlanObject.from_orm(xml_plan_object)
    assert err.value.errors() == [
        {
            "loc": ("splan:PlanObject/splan:geometry",),
            "msg": "geometry is not valid",
            "type": "assertion_error",
        }
    ]
