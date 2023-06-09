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
def file_xml_valid_with_group():
    return TEST_DATA_DIR / "spatialPlan-collection-with-group.xml"


@pytest.fixture
def file_xml_valid_with_group_inlined():
    return TEST_DATA_DIR / "spatialPlan-collection-with-group-inlined.xml"


@pytest.fixture
def gml_curve_with_arc():
    return """
        <gml:Curve srsName="urn:ogc:def:crs:EPSG::4326" xmlns:gml="http://www.opengis.net/gml/3.2">
          <gml:segments>
            <gml:Arc numArc="1">
              <gml:posList>60.2893418 25.430357 60.2894259 25.4304633 60.2894444 25.4303376</gml:posList>
            </gml:Arc>
          </gml:segments>
        </gml:Curve>
    """


@pytest.fixture
def gml_curve_with_arc_by_center_point():
    return """
        <gml:Curve srsName="urn:ogc:def:crs:EPSG::4326" xmlns:gml="http://www.opengis.net/gml/3.2">
          <gml:segments>
            <gml:ArcByCenterPoint numArc="1">
              <gml:posList>60.2893418 25.430357</gml:posList>
              <gml:radius uom="m">12</gml:radius>
              <gml:startAngle uom="deg">45</gml:startAngle>
              <gml:endAngle uom="deg">90</gml:endAngle>
            </gml:ArcByCenterPoint>
          </gml:segments>
        </gml:Curve>
    """


@pytest.fixture
def gml_curve_with_arc_string():
    return """
        <gml:Curve srsName="urn:ogc:def:crs:EPSG::4326" xmlns:gml="http://www.opengis.net/gml/3.2">
          <gml:segments>
            <gml:ArcString numArc="2">
              <gml:posList>60.2893418 25.430357 60.2894259 25.4304633 60.2894444 25.4303376 60.2895416 25.4298993 60.2895686 25.4298493</gml:posList>
            </gml:ArcString>
          </gml:segments>
        </gml:Curve>
    """


@pytest.fixture
def gml_curve_with_linestring():
    return """
        <gml:Curve srsName="urn:ogc:def:crs:EPSG::4326" xmlns:gml="http://www.opengis.net/gml/3.2">
            <gml:segments>
                <gml:LineStringSegment>
                    <gml:posList>60.2893418 25.430357 60.2894259 25.4304633 60.2894444 25.4303376 60.2895416 25.4298993 60.2895686 25.4298493 60.2894865 25.4297044 60.2893418 25.430357</gml:posList>
                </gml:LineStringSegment>
            </gml:segments>
        </gml:Curve>
        """


@pytest.fixture
def gml_solid_with_polygon():
    return """
        <gml:Solid srsName="urn:ogc:def:crs:EPSG::9518" gml:id="AK_SIPOO_5_lainvoimainen_kaava_sipoo_nevasgard.geom.8" srsDimension="3" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlexr="http://www.opengis.net/gml/3.3/exr">
          <gml:exterior>
            <gml:Shell>
              <gml:surfaceMember>
                <!-- bottom -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>60 25 10 60 24 10 59 24 10 59 25 10 60 25 10</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
              <gml:surfaceMember>
                <!-- top -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>60 25 20 60 24 20 59 24 20 59 25 20 60 25 20</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
              <gml:surfaceMember>
                <!-- side 1 -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>60 24 20 59 24 20 59 24 10 60 24 10 60 24 20</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
              <gml:surfaceMember>
                <!-- side 2 -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>59 24 20 59 25 20 59 25 10 59 24 10 59 24 20</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
              <gml:surfaceMember>
                <!-- side 3 -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>60 25 20 59 25 20 59 25 10 60 25 10 60 25 20</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
              <gml:surfaceMember>
                <!-- side 4 -->
                <gml:Polygon>
                  <gml:exterior>
                    <gml:LinearRing>
                      <gml:posList>60 24 20 60 25 20 60 25 10 60 24 10 60 24 20</gml:posList>
                    </gml:LinearRing>
                  </gml:exterior>
                </gml:Polygon>
              </gml:surfaceMember>
            </gml:Shell>
          </gml:exterior>
        </gml:Solid>
    """


@pytest.fixture
def gml_polyhedralsurface_with_curve():
    return """
        <gml:PolyhedralSurface srsName="urn:ogc:def:crs:EPSG:3880" gml:id="Kaava.geom.1" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmlexr="http://www.opengis.net/gml/3.3/exr">
          <gml:polygonPatches>
            <gml:PolygonPatch>
              <gml:exterior>
                <gml:Ring>
                  <gml:curveMember>
                    <gml:Curve>
                      <gml:segments>
                        <gml:LineStringSegment>
                          <gml:pos>26478290.00000 7028885.00000</gml:pos>
                          <gml:pos>26478202.50000 7029070.00000</gml:pos>
                          <gml:pos>26478187.80894 7029242.14612</gml:pos>
                          <gml:pos>26478222.84164 7029240.15927</gml:pos>
                        </gml:LineStringSegment>
                        <gml:Arc>
                          <gml:pos>26478222.84164 7029240.15927</gml:pos>
                          <gml:pos>26478218.97206 7029160.01411</gml:pos>
                          <gml:pos>26478251.90124 7029086.84383</gml:pos>
                        </gml:Arc>
                        <gml:LineStringSegment>
                          <gml:pos>26478251.90124 7029086.84383</gml:pos>
                          <gml:pos>26478347.21675 7028891.71508</gml:pos>
                          <gml:pos>26478290.00000 7028885.00000</gml:pos>
                        </gml:LineStringSegment>
                      </gml:segments>
                    </gml:Curve>
                  </gml:curveMember>
                </gml:Ring>
              </gml:exterior>
            </gml:PolygonPatch>
          </gml:polygonPatches>
        </gml:PolyhedralSurface>
        """


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
