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
XPATH_GENERAL_ORDER = "splan:generalOrder/@xlink:href"
XPATH_GEOMETRY = "splan:geometry"
XPATH_GML_ID = "./@gml:id"
XPATH_LOCAL_NAME = "local-name()"
XPATH_PLANNER = "splan:planner/@xlink:href"
XPATH_PARTICIPATION_AND_EVALUTION_PLAN = "splan:participationAndEvalutionPlan/@xlink:href"
XPATH_PRODUCER_SPECIFIC_IDENTIFIER = "lud-core:producerSpecificIdentifier/text()"
XPATH_PLAN_IDENTIFIER = "splan:planIdentifier/text()"
XPATH_SPATIAL_PLAN = "splan:spatialPlan/@xlink:href"
