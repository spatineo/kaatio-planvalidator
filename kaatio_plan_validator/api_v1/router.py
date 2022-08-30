from fastapi import APIRouter, UploadFile, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from . import exception_handlers, models, responses

router = APIRouter()


@router.post(
    path="/validate",
    response_class=responses.XMLResponse,
    responses={
        422: {
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ErrorResponse",
                    }
                }
            },
            "default_response_class": exception_handlers.JSONResponse,
            "description": "Validation Error",
            "model": exception_handlers.ErrorResponse,
        },
    },
)
async def validate(file: UploadFile):
    """Route to validate xml file."""

    # Parse incoming xml
    try:
        feature_collection = models.LandUseFeatureCollection.parse_xml(
            source=file.file,
        )

        verifier = models.FeatureCollectionVerifier(
            participation_and_evaluation_plans=[
                models.ParticipationAndEvaluationPlan.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("ParticipationAndEvaluationPlan")
            ],
            plan_objects=[
                models.PlanObject.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("PlanObject")
            ],
            plan_orders=[
                models.PlanOrder.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("PlanOrder")
            ],
            planners=[
                models.Planner.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("Planner")
            ],
            spatial_plans=[
                models.SpatialPlan.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("SpatialPlan")
            ],
        )

        verifier.verify()

    except ValidationError as err:  # pragma: no cover
        raise RequestValidationError(errors=err.raw_errors, body=err.model.__name__)

    # All good - return xml
    return responses.XMLResponse(
        content=feature_collection.to_string(),
        status_code=status.HTTP_200_OK,
    )
