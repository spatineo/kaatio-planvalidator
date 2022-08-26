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
