import logging

from fastapi import APIRouter, UploadFile, status
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError

from . import exceptions, models, responses

router = APIRouter()

logger = logging.getLogger("uvicorn.access")


@router.post(
    path="/store",
    response_class=responses.XMLResponse,
)
async def store(file: UploadFile):
    """Route to validate xml file."""

    try:
        feature_collection = models.LandUseFeatureCollection.from_xml_source(
            source=file.file,
        )

        feature_collection.process_feature_members()

        # All good - return xml
        return responses.XMLResponse(
            content=feature_collection.to_string(),
            status_code=status.HTTP_200_OK,
        )
    except ValidationError as err:  # pragma: no cover
        raise RequestValidationError(
            errors=err.raw_errors,
            body=err.model.__name__,
        )
    except (exceptions.ParserException, exceptions.SchemaException) as err:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": ["XML"],
                    "msg": str(err),
                    "type": err.type,
                }
            ],
        )
    except exceptions.VerifyException as err:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[
                {
                    "loc": ["XML"],
                    "msg": str(err),
                    "type": err.type,
                }
            ],
        )
    except Exception as err:  # pragma: no cover
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=[
                {
                    "loc": [],
                    "msg": "Internal server error - contact support.",
                    "type": "internal_error",
                }
            ],
        )
