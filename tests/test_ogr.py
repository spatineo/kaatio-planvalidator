import pytest
from osgeo import ogr
from pytest import FixtureRequest

from kaatio_plan_validator.api_v1.ogc import gdal_err


@pytest.mark.parametrize(
    "gml_name,expected",
    [
        ("gml_curve_with_arc", True),
        ("gml_curve_with_arc_by_center_point", True),
        ("gml_curve_with_arc_string", True),
        ("gml_curve_with_linestring", True),
        ("gml_solid_with_polygon", False),
        ("gml_polyhedralsurface_with_curve", True),
    ],
)
def test_gml_with_ogr(request: FixtureRequest, gml_name: str, expected: bool):
    gml = request.getfixturevalue(gml_name)

    geometry: ogr.Geometry = ogr.CreateGeometryFromGML(gml)
    if expected:
        try:
            assert geometry.IsValid()
        except Exception:
            if gdal_err.err_msg != "SFCGAL support not enabled.":
                raise

    else:
        assert not geometry
