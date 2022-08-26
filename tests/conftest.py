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
def valid_xml():
    return DATA_DIR / "virallinen_kaatio_valid.xml"


@pytest.fixture
def land_use_feature_collection(valid_xml: Path):
    return models.LandUseFeatureCollection.parse_xml(
        skip_xml_must_validate_against_xsd=True,
        source=valid_xml,
    )
