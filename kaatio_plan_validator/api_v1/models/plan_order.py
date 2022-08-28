from typing import Optional, cast

import lxml.etree as ET
from pydantic import validator

from .. import constants
from . import common


class PlanOrder(common.XmlOrmModel):
    """Represents model definition for PlanOrder class."""

    spatial_plan: str
    target: Optional[str]

    @validator("target", always=True)
    def target_must_be_defined(cls, target: Optional[str], values: dict):
        if not target:
            root = cast(
                ET._Element,
                values.get("xml"),
            )
            target = "FILLED"
            target_element_ns = constants.NAMESPACES.get("splan")
            target_element_attribute_ns = constants.NAMESPACES.get("xlink")
            target_element = ET.Element(
                f"{{{target_element_ns}}}target",
                attrib={
                    f"{{{target_element_attribute_ns}}}href": target,
                },
                nsmap=root.nsmap,
            )
            index = root.index(child=root.xpath(constants.XPATH_SPATIAL_PLAN, namespaces=constants.NAMESPACES)[0]) + 1
            root.insert(
                index=index,
                element=target_element,
            )
        return target
