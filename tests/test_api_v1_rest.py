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


def test_route_validate_with_invalid_xml_no_feature_members(invalid_xml_no_feature_members: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                invalid_xml_no_feature_members.name,
                invalid_xml_no_feature_members.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_route_validate_with_valid_xml(valid_xml: Path):

    with TestClient(app) as client:
        files = {
            "file": (
                valid_xml.name,
                valid_xml.open(mode="rb").read(),
                "application/xml",
            )
        }
        response = client.post(URL_VALIDATE, files=files)
        assert response.status_code == status.HTTP_200_OK
