from typing import Any

import lxml.etree as ET
import pygml
from pydantic import BaseModel
from pydantic.utils import GetterDict
from shapely.geometry import shape

from .. import constants


class XmlGetterDict(GetterDict):

    _obj: ET._Element

    def get(self, key: str, default: Any) -> Any:

        if key == "boundary":
            geometry = list(self.xpath(constants.XPATH_BOUNDARY, default))[0]
            return shape(pygml.parse(geometry))
        if key == "general_order":
            return self.xpath(constants.XPATH_GENERAL_ORDER_HREF, default)
        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "geometry":
            geometry = list(self.xpath(constants.XPATH_GEOMETRY, default))[0]
            return shape(pygml.parse(geometry))
        if key == "planner":
            return self.xpath(constants.XPATH_PLANNER_HREF, default)
        if key == "participation_and_evalution_plan":
            return self.xpath(constants.XPATH_PARTICIPATION_AND_EVALUTION_PLAN_HREF, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER_TEXT, default)
        if key == "plan_identifier":
            return self.xpath(constants.XPATH_PLAN_IDENTIFIER_TEXT, default)
        if key == "target":
            return self.xpath(constants.XPATH_TARGET_HREF, default)
        if key == "spatial_plan":
            return self.xpath(constants.XPATH_SPATIAL_PLAN_HREF, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover

    def xpath(self, xpath: str, default: Any) -> Any:
        try:
            return self._obj.xpath(xpath, namespaces=constants.NAMESPACES)[0]
        except IndexError:  # pragma: no cover
            return default


class XmlModel(BaseModel):

    skip: dict = {}
    xml: ET._Element | ET._ElementTree

    class Config:
        arbitrary_types_allowed = True


class XmlOrmModel(XmlModel):

    gml_id: str
    producer_specific_identifier: str

    class Config(XmlModel.Config):
        getter_dict = XmlGetterDict
        orm_mode = True
