import lxml.etree as ET

from . import constants


def child_tag_names(xml: ET._Element) -> list[str]:
    return [
        e.xpath(
            constants.XPATH_LOCAL_NAME,
            **constants.NAMESPACES,
        )
        for e in list(xml)
        if isinstance(e, ET._Element)
    ]


def ns_key_to_clark_notation(ns_key: str) -> str:
    ns, key = ns_key.split(":")
    return f"{{{constants.NSMAP.get(ns)}}}{key}"
