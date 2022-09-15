from pathlib import Path

import lxml.etree as ET
import pytest

from kaatio_plan_validator.api_v1 import constants

TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def file_xml_broken():
    return TEST_DATA_DIR / "virallinen_kaatio_broken.xml"


@pytest.fixture
def file_xml_invalid():
    return TEST_DATA_DIR / "virallinen_kaatio_invalid.xml"


@pytest.fixture
def file_xml_valid_1():
    return TEST_DATA_DIR / "virallinen_kaatio_valid_1.xml"


@pytest.fixture
def file_xml_valid_1_gen():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_1.xml"


@pytest.fixture
def file_xml_valid_1_gen_result():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_1_result.xml"


@pytest.fixture
def file_xml_valid_2():
    return TEST_DATA_DIR / "virallinen_kaatio_valid_2.xml"


@pytest.fixture
def file_xml_valid_2_gen():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_2.xml"


@pytest.fixture
def file_xml_valid_2_gen_result():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_2_result.xml"


@pytest.fixture
def file_xml_valid_example():
    return TEST_DATA_DIR / "spatialPlan-collection-simple.xml"


@pytest.fixture
def xml_element_feature_member_pe_plan(xml_valid_1: ET._ElementTree):
    return xml_valid_1.xpath("lud-core:featureMember/splan:ParticipationAndEvaluationPlan", **constants.NAMESPACES)[0]


@pytest.fixture
def xml_element_feature_member_plan_object(xml_valid_1: ET._ElementTree):
    return xml_valid_1.xpath("lud-core:featureMember/splan:PlanObject", **constants.NAMESPACES)[0]


@pytest.fixture
def xml_element_feature_member_plan_order(xml_valid_1: ET._ElementTree):
    return xml_valid_1.xpath("lud-core:featureMember/splan:PlanOrder", **constants.NAMESPACES)[0]


@pytest.fixture
def xml_element_feature_member_planner(xml_valid_1: ET._ElementTree):
    return xml_valid_1.xpath("lud-core:featureMember/splan:Planner", **constants.NAMESPACES)[0]


@pytest.fixture
def xml_element_feature_member_spatial_plan(xml_valid_1: ET._ElementTree):
    return xml_valid_1.xpath("lud-core:featureMember/splan:SpatialPlan", **constants.NAMESPACES)[0]


@pytest.fixture
def xml_element_polygon_invalid():
    return ET.fromstring(
        """
        <gml:Polygon srsName="urn:ogc:def:crs:EPSG::4326" gml:id="AK_SIPOO_5_lainvoimainen_kaava_sipoo_nevasgard.geom.2" xmlns:gml="http://www.opengis.net/gml/3.2">
            <gml:exterior>
                <gml:LinearRing>
                    <gml:posList>60.2866853 25.4095811 60.2866968 25.4092981 60.286163 25.409723 60.285766 25.409760 60.285861 25.409401</gml:posList>
                </gml:LinearRing>
            </gml:exterior>
        </gml:Polygon>
        """
    )


@pytest.fixture
def xml_valid_1(file_xml_valid_1: Path):
    return ET.parse(file_xml_valid_1)
