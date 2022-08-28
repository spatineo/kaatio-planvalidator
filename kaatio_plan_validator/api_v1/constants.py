from pathlib import Path

NAMESPACES = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink",
    "gml": "http://www.opengis.net/gml/3.2",
    "gmlexr": "http://www.opengis.net/gml/3.3/exr",
    "lsp": "http://tietomallit.ymparisto.fi/ry-yhteiset/kielituki/xml/1.0",
    "lud-core": "http://tietomallit.ymparisto.fi/mkp-ydin/xml/1.2",
    "splan": "http://tietomallit.ymparisto.fi/kaavatiedot/xml/1.2",
}

SCHEMA_DIR = Path(__file__).parent / "schemas"
SCHEMA_FILES = list(SCHEMA_DIR.glob("**/*.xsd"))


XPATH_BOUNDARY = "lud-core:boundary"
XPATH_GENERAL_ORDER = "splan:generalOrder"
XPATH_GENERAL_ORDER_HREF = f"{XPATH_GENERAL_ORDER}/@xlink:href"
XPATH_GEOMETRY = "splan:geometry"
XPATH_GML_ID = "./@gml:id"
XPATH_LOCAL_NAME = "local-name()"
XPATH_PLANNER = "splan:planner"
XPATH_PLANNER_HREF = f"{XPATH_PLANNER}/@xlink:href"
XPATH_PARTICIPATION_AND_EVALUTION_PLAN = "splan:participationAndEvalutionPlan"
XPATH_PARTICIPATION_AND_EVALUTION_PLAN_HREF = f"{XPATH_PARTICIPATION_AND_EVALUTION_PLAN}/@xlink:href"
XPATH_PRODUCER_SPECIFIC_IDENTIFIER = "lud-core:producerSpecificIdentifier"
XPATH_PRODUCER_SPECIFIC_IDENTIFIER_TEXT = f"{XPATH_PRODUCER_SPECIFIC_IDENTIFIER}/text()"
XPATH_PLAN_IDENTIFIER = "splan:planIdentifier"
XPATH_PLAN_IDENTIFIER_TEXT = f"{XPATH_PLAN_IDENTIFIER}/text()"
XPATH_TARGET = "splan:target"
XPATH_TARGET_HREF = f"{XPATH_TARGET}/@xlink:href"
XPATH_SPATIAL_PLAN = "splan:spatialPlan"
XPATH_SPATIAL_PLAN_HREF = f"{XPATH_SPATIAL_PLAN}/@xlink:href"
