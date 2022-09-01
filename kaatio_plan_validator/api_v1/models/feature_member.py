import uuid
from datetime import datetime, timezone
from typing import Any

import lxml.etree as ET
import pygml
from pydantic import BaseModel
from pydantic.utils import GetterDict
from shapely.geometry import shape

from .. import constants, utils


class XMLGetterDict(GetterDict):
    """Represents getter dict for PlanOrder model."""

    _obj: ET._Element

    def get(self, key: str, default: Any) -> Any:
        """Returns value from XML element or default for given key."""

        try:
            if key == "boundary":
                element = self._obj.xpath(constants.XPATH_BOUNDARY, **constants.NAMESPACES)[0]
                geometry = pygml.parse(element)
                return shape(geometry)
            if key == "geometry":
                element = self._obj.xpath(constants.XPATH_GEOMETRY, **constants.NAMESPACES)[0]
                geometry = pygml.parse(element)
                return shape(geometry)
            if key == "plan_identifier":
                return self._obj.xpath(constants.XPATH_PLAN_IDENTIFIER_TEXT, **constants.NAMESPACES)[0]
            if key == "producer_specific_identifier":
                return self._obj.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER_TEXT, **constants.NAMESPACES)[0]

        except IndexError:  # pragma: no cover
            pass
        if key == "xml":
            return self._obj

        return default


class FeatureMember(BaseModel):

    xml: ET._Element

    class Config:
        """Represents config definition for model."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        getter_dict = XMLGetterDict
        orm_mode = True

    def update_or_create_elements_with_id(self) -> tuple[str]:

        # Update gml:id attribute
        id_old: str = self.xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
        if not id_old.startswith("id-"):
            id_new = f"id-{uuid.uuid4()}.{uuid.uuid4()}"
        else:
            gml_id_uuid, *_ = id_old.removeprefix("id-").split(".")
            try:
                uuid.UUID(gml_id_uuid)
                id_new = f"id-{gml_id_uuid}.{uuid.uuid4()}"
            except ValueError:
                id_new = f"id-{uuid.uuid4()}.{uuid.uuid4()}"

        attrib = utils.ns_key_to_clark_notation(constants.XPATH_GML_ID.removeprefix("./@"))
        self.xml.attrib[attrib] = id_new

        # Add or update gml:idenfifier attribute
        try:
            identifier_element = self.xml.xpath(constants.XPATH_IDENTIFIER, **constants.NAMESPACES)[0]
        except IndexError:
            identifier_element: ET._Element = ET.Element(
                utils.ns_key_to_clark_notation(constants.XPATH_IDENTIFIER),
                codeSpace="http://uri.suomi.fi/object/rytj/kaava",
            )
            self.xml.insert(
                index=0,
                element=identifier_element,
            )
        identifier_element.text = f"{self.xml.xpath(constants.XPATH_LOCAL_NAME)}/{id_new}"

        # Add or update lud-core:objectIdentifier
        try:
            object_identifier_element = self.xml.xpath(constants.XPATH_OBJECT_IDENTIFIER, **constants.NAMESPACES)[0]
        except IndexError:
            object_identifier_element: ET._Element = ET.Element(
                utils.ns_key_to_clark_notation(constants.XPATH_OBJECT_IDENTIFIER),
            )
            self.xml.insert(
                index=self.xml.index(identifier_element) + 1,
                element=object_identifier_element,
            )
        object_identifier_element.text = id_new.split(".")[0]

        return (id_old, id_new)

    def update_or_create_storage_time(self):

        # Add or update lud-core:storageTime/gml:TimeInstant/gml:timePosition
        dt = datetime.now()
        ts = dt.replace(tzinfo=timezone.utc)

        try:
            storage_time_position_element = self.xml.xpath(constants.XPATH_STORAGE_TIME, **constants.NAMESPACES)[0]
        except IndexError:
            (
                storage_time_ns_key,
                storage_time_instant_ns_key,
                storage_time_position_ns_key,
            ) = constants.XPATH_STORAGE_TIME.split("/")
            storage_time_element: ET._Element = ET.Element(
                utils.ns_key_to_clark_notation(storage_time_ns_key),
            )
            storage_time_instant_element: ET._Element = ET.Element(
                utils.ns_key_to_clark_notation(storage_time_instant_ns_key),
            )
            storage_time_position_element: ET._Element = ET.Element(
                utils.ns_key_to_clark_notation(storage_time_position_ns_key),
            )
            storage_time_instant_element.append(storage_time_position_element)
            storage_time_element.append(storage_time_instant_element)
            # We need to find correct position for element
            xml_child_tag_names = utils.child_tag_names(self.xml)
            if "latestChange" in xml_child_tag_names:
                pos_element = self.xml.xpath(constants.XPATH_LATEST_CHANGE, **constants.NAMESPACES)[0]
            elif "producerSpecificIdentifier" in xml_child_tag_names:
                pos_element = self.xml.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, **constants.NAMESPACES)[0]
            elif "objectIdentifier" in xml_child_tag_names:
                pos_element = self.xml.xpath(constants.XPATH_OBJECT_IDENTIFIER, **constants.NAMESPACES)[0]
            else:
                pos_element = self.xml.xpath(constants.XPATH_IDENTIFIER, **constants.NAMESPACES)[0]
            self.xml.insert(
                index=self.xml.index(pos_element) + 1,
                element=storage_time_element,
            )
        storage_time_position_element.text = ts.isoformat(timespec="seconds")

    def update_feature_member_id_references(self, xpath: str, refs: list[tuple[str]]):

        elements: list[ET._Element] = self.xml.xpath(xpath, **constants.NAMESPACES)
        for old, new in refs:
            for element in elements:
                attrib = utils.ns_key_to_clark_notation(constants.XPATH_XLINK_HREF)
                if str(element.attrib[attrib]).removeprefix("#") == old:
                    element.attrib[attrib] = f"#{new}"