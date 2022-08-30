from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient

from kaatio_plan_validator.main import app

URL_VALIDATE = "/v1/validate"


def test_route_validate_with_broken_xml(broken_xml: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                broken_xml.name,
                broken_xml.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            "message": "Failed to parse XML!",
            "reason": ["error parsing attribute name, line 10, column 7 (<string>, line 10)"],
            "type": "parser_error",
        }


def test_route_validate_with_invalid_xml(invalid_xml: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                invalid_xml.name,
                invalid_xml.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["message"] == "Failed to validate XML against schema!"
        assert response.json()["type"] == "schema_error"


def test_route_validate_with_valid_xml_1(valid_xml_1: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                valid_xml_1.name,
                valid_xml_1.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"


def test_route_validate_with_valid_xml_2(valid_xml_2: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                valid_xml_2.name,
                valid_xml_2.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"
