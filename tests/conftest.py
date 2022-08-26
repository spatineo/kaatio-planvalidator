from pathlib import Path

import lxml.etree as ET
import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def broken_xml():
    return DATA_DIR / "virallinen_kaatio_broken.xml"


@pytest.fixture
def invalid_xml():
    return DATA_DIR / "virallinen_kaatio_invalid.xml"


@pytest.fixture
def valid_xml_doc(valid_xml: Path) -> ET._ElementTree:
    return ET.parse(valid_xml)


@pytest.fixture
def valid_xml():
    return DATA_DIR / "virallinen_kaatio_valid.xml"
