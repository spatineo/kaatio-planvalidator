from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from kaatio_plan_validator.main import app

URL_VALIDATE = "/v1/store"


def test_route_validate_with_broken_xml(
    file_xml_broken: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_broken.name,
                file_xml_broken.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            "detail": [
                {
                    "loc": ["XML"],
                    "msg": "Failed to parse XML! Reason: error parsing attribute name, line 10, column 7 (<string>, line 10)",
                    "type": "parser_error",
                }
            ]
        }


def test_route_validate_with_invalid_xml(
    file_xml_invalid: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_invalid.name,
                file_xml_invalid.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["XML"]
        assert response.json()["detail"][0]["type"] == "schema_error"


def test_route_validate_with_valid_xml_1(
    file_xml_valid_1: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_valid_1.name,
                file_xml_valid_1.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"


@pytest.mark.skip(reason="Debug stuff")
def test_route_validate_with_valid_xml_1_gen(
    file_xml_valid_1_gen: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_valid_1_gen.name,
                file_xml_valid_1_gen.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"


def test_route_validate_with_valid_xml_2(
    file_xml_valid_2: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_valid_2.name,
                file_xml_valid_2.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"


@pytest.mark.skip(reason="Debug stuff")
def test_route_validate_with_valid_xml_2_gen(
    file_xml_valid_2_gen: Path,
):

    with TestClient(app) as client:
        files = {
            "file": (
                file_xml_valid_2_gen.name,
                file_xml_valid_2_gen.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"
