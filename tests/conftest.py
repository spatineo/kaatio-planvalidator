from pathlib import Path

import pytest

TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def broken_xml():
    return TEST_DATA_DIR / "virallinen_kaatio_broken.xml"


@pytest.fixture
def invalid_xml():
    return TEST_DATA_DIR / "virallinen_kaatio_invalid.xml"


@pytest.fixture
def valid_xml_1():
    return TEST_DATA_DIR / "virallinen_kaatio_valid_1.xml"


@pytest.fixture
def valid_xml_1_gen():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_1.xml"


@pytest.fixture
def valid_xml_1_gen_result():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_1_result.xml"


@pytest.fixture
def valid_xml_2():
    return TEST_DATA_DIR / "virallinen_kaatio_valid_2.xml"


@pytest.fixture
def valid_xml_2_gen():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_2.xml"


@pytest.fixture
def valid_xml_2_gen_result():
    return TEST_DATA_DIR / "generated-virallinen_kaatio_valid_2_result.xml"
