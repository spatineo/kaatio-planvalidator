from fastapi import APIRouter, Response, UploadFile, status

from . import exceptions, models

router = APIRouter()


@router.post("/validate")
async def validate(file: UploadFile):
    """Route to validate xml file."""

    try:
        # Parse incoming xml
        feature_collection = models.LandUseFeatureCollection.parse_xml(
            source=file.file,
        )

        spatial_plans = [
            models.SpatialPlan.from_orm(feature_member)
            for feature_member in feature_collection.get_feature_members_by_tag("SpatialPlan")
        ]
        print(spatial_plans)
        # All good - return xml
        return Response(
            content=feature_collection.to_string(),
            status_code=status.HTTP_200_OK,
        )

    except (
        exceptions.ParserException,
        exceptions.ValidatorException,
    ) as err:
        return Response(
            content=str(err),
            media_type="application/xml",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception:
        return Response(
            content="KABOOM",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
