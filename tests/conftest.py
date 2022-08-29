from pathlib import Path

import pytest

from kaatio_plan_validator.api_v1 import models

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def broken_xml():
    return DATA_DIR / "virallinen_kaatio_broken.xml"


@pytest.fixture
def invalid_xml():
    return DATA_DIR / "virallinen_kaatio_invalid.xml"


@pytest.fixture
def invalid_xml_no_feature_members():
    return DATA_DIR / "virallinen_kaatio_invalid_no_feature_members.xml"


@pytest.fixture
def invalid_xml_plan_object_unknown_spatialplan():
    return DATA_DIR / "virallinen_kaatio_invalid_plan_object_unkown_spatialplan.xml"


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
