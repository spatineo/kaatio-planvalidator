from pathlib import Path

NSMAP = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink",
    "gml": "http://www.opengis.net/gml/3.2",
    "gmlexr": "http://www.opengis.net/gml/3.3/exr",
    "lsp": "http://tietomallit.ymparisto.fi/ry-yhteiset/kielituki/xml/1.0",
    "lud-core": "http://tietomallit.ymparisto.fi/mkp-ydin/xml/1.2",
    "splan": "http://tietomallit.ymparisto.fi/kaavatiedot/xml/1.2",
}
NAMESPACES = {"namespaces": NSMAP}

SCHEMA_DIR = Path(__file__).parent / "schemas"
SCHEMA_FILES = list(SCHEMA_DIR.glob("**/*.xsd"))

XPATH_XLINK_HREF = "xlink:href"
XPATH_BOUNDARY = "lud-core:boundary/*[1]"  # Pick first
XPATH_GENERAL_ORDER = "splan:generalOrder"
XPATH_GEOMETRY = "splan:geometry/*[1]"  # Pick first
XPATH_GML_ID = "./@gml:id"
XPATH_IDENTIFIER = "gml:identifier"
XPATH_LATEST_CHANGE = "lud-core:latestChange/gml:TimeInstant/gml:timePosition"
XPATH_LOCAL_NAME = "local-name()"
XPATH_OBJECT_IDENTIFIER = "lud-core:objectIdentifier"
XPATH_PLANNER = "splan:planner"
XPATH_PARTICIPATION_AND_EVALUTION_PLAN = "splan:participationAndEvalutionPlan"
XPATH_PRODUCER_SPECIFIC_IDENTIFIER = "lud-core:producerSpecificIdentifier"
XPATH_PRODUCER_SPECIFIC_IDENTIFIER_TEXT = f"{XPATH_PRODUCER_SPECIFIC_IDENTIFIER}/text()"
XPATH_PLAN_IDENTIFIER = "splan:planIdentifier"
XPATH_PLAN_IDENTIFIER_TEXT = f"{XPATH_PLAN_IDENTIFIER}/text()"
XPATH_STORAGE_TIME = "lud-core:storageTime/gml:TimeInstant/gml:timePosition"
XPATH_TARGET = "splan:target"
XPATH_SPATIAL_PLAN = "splan:spatialPlan"
