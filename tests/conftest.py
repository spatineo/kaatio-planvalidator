from pathlib import Path

import lxml.etree as ET
import pytest

from kaatio_plan_validator.api_v1 import constants, models

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def broken_xml():
    return DATA_DIR / "virallinen_kaatio_broken.xml"


@pytest.fixture
def invalid_xml():
    return DATA_DIR / "virallinen_kaatio_invalid.xml"


@pytest.fixture
def valid_xml_1():
    return DATA_DIR / "virallinen_kaatio_valid_1.xml"


@pytest.fixture
def valid_xml_2():
    return DATA_DIR / "virallinen_kaatio_valid_2.xml"


@pytest.fixture
def land_use_feature_collection(valid_xml_1: Path):
    return models.LandUseFeatureCollection.parse_xml(
        skip={"no_xsd_validation": True},
        source=valid_xml_1,
    )


@pytest.fixture
def plan_object_valid_element(land_use_feature_collection: models.LandUseFeatureCollection):

    return land_use_feature_collection.find_feature_members_by_tag("PlanObject")[0]


@pytest.fixture
def plan_object_invalid_element_without_spatialplan(plan_object_valid_element: ET._Element):
    plan_object_valid_element.remove(
        plan_object_valid_element.xpath(constants.XPATH_SPATIAL_PLAN, namespaces=constants.NAMESPACES)[0],
    )
    return plan_object_valid_element


@pytest.fixture
def spatial_plan_valid_element(land_use_feature_collection: models.LandUseFeatureCollection):
    return land_use_feature_collection.find_feature_members_by_tag("SpatialPlan")[0]
