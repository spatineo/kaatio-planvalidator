from fastapi import APIRouter, Response, UploadFile, status

from . import exceptions, models


class XMLResponse(Response):
    media_type = "application/xml"


router = APIRouter()


@router.post(
    path="/validate",
    response_class=XMLResponse,
)
async def validate(file: UploadFile):
    """Route to validate xml file."""

    try:

        # Parse incoming xml
        feature_collection = models.LandUseFeatureCollection.parse_xml(
            source=file.file,
        )

        verifier = models.FeatureCollectionVerifier.parse_feature_collection(
            feature_collection=feature_collection,
        )

        verifier.verify()

        # All good - return xml
        return XMLResponse(
            content=feature_collection.to_string(),
            status_code=status.HTTP_201_CREATED,
        )

    except exceptions.ParserException as err:
        return Response(
            content=str(err),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except exceptions.ValidatorException as err:
        return Response(
            content=str(err),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except exceptions.VerifyException as err:
        return Response(
            content=str(err),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        return Response(
            content="KABOOM",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
