import uuid
from datetime import datetime, timezone
from typing import Any

import lxml.etree as ET
import pygml
from pydantic import BaseModel, Field, validate_model, validator
from pydantic.utils import GetterDict
from shapely.geometry import shape

from .. import constants


class XMLGetterDict(GetterDict):
    """Represents getter dict for PlanOrder model."""

    _obj: ET._Element

    def get(self, key: str, default: Any) -> Any:
        """Returns value from XML element or default for given key."""

        try:
            if key == "boundary":
                element = list(self._obj.xpath(constants.XPATH_BOUNDARY, **constants.NAMESPACES)[0])[0]
                geometry = pygml.parse(element)
                return shape(geometry)
            if key == "geometry":
                element = list(self._obj.xpath(constants.XPATH_GEOMETRY, **constants.NAMESPACES)[0])[0]
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
    ref_errors: list = Field(default_factory=list)

    class Config:
        """Represents config definition for model."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        getter_dict = XMLGetterDict
        orm_mode = True

    @validator("ref_errors")
    def post_validate_ref_errors(cls, ref_errors: list):
        assert not ref_errors, f"unknown references: {ref_errors}"
        return ref_errors

    def _child_tag_names(self, xml: ET._Element) -> list[str]:
        return [
            e.xpath(
                constants.XPATH_LOCAL_NAME,
                **constants.NAMESPACES,
            )
            for e in list(xml)
            if isinstance(e, ET._Element)
        ]

    def _ns_key_to_clark_notation(self, ns_key: str) -> str:
        ns, key = ns_key.split(":")
        return f"{{{constants.NSMAP.get(ns)}}}{key}"

    def update_or_create_elements_with_id(self) -> tuple[str]:
        """Update or create elements to feature member"""

        # Update gml:id attribute
        id_old: str = self.xml.xpath(constants.XPATH_GML_ID, **constants.NAMESPACES)[0]
        # Id should always start with 'id-' prefix.
        if not id_old.startswith("id-"):
            # Id did not start with the expected prefix - create id from scratch.
            id_new = f"id-{uuid.uuid4()}.{uuid.uuid4()}"
        else:
            # Pick first part of the id.
            gml_id_uuid, *_ = id_old.removeprefix("id-").split(".")
            try:
                # Check if first is valid uuid.
                uuid.UUID(gml_id_uuid)
                # Generate second part of id.
                id_new = f"id-{gml_id_uuid}.{uuid.uuid4()}"
            except ValueError:
                # First part was not valid uuid - create id from scratch.
                id_new = f"id-{uuid.uuid4()}.{uuid.uuid4()}"

        # Find key for attribute
        attrib = self._ns_key_to_clark_notation(constants.XPATH_GML_ID.removeprefix("./@"))
        # Update attribute with key and new id
        self.xml.attrib[attrib] = id_new

        # Add or update gml:idenfifier attribute
        try:
            # Look for element
            identifier_element = self.xml.xpath(constants.XPATH_IDENTIFIER, **constants.NAMESPACES)[0]
        except IndexError:
            # Element not found - lets create it.
            identifier_element: ET._Element = ET.Element(
                self._ns_key_to_clark_notation(constants.XPATH_IDENTIFIER),
                codeSpace="http://uri.suomi.fi/object/rytj/kaava",
            )
            self.xml.insert(
                index=0,  # always the first child element.
                element=identifier_element,
            )
        # Update element value.
        identifier_element.text = f"{self.xml.xpath(constants.XPATH_LOCAL_NAME)}/{id_new}"

        # Add or update lud-core:objectIdentifier
        try:
            # Look for element
            object_identifier_element = self.xml.xpath(constants.XPATH_OBJECT_IDENTIFIER, **constants.NAMESPACES)[0]
        except IndexError:
            # Element not found - lets create it.
            object_identifier_element: ET._Element = ET.Element(
                self._ns_key_to_clark_notation(constants.XPATH_OBJECT_IDENTIFIER),
            )
            self.xml.insert(
                index=self.xml.index(identifier_element) + 1,  # always after gml:identifier
                element=object_identifier_element,
            )
        # Update element value.
        object_identifier_element.text = id_new.split(".")[0]

        # Return old and new id.
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
                self._ns_key_to_clark_notation(storage_time_ns_key),
            )
            storage_time_instant_element: ET._Element = ET.Element(
                self._ns_key_to_clark_notation(storage_time_instant_ns_key),
            )
            storage_time_position_element: ET._Element = ET.Element(
                self._ns_key_to_clark_notation(storage_time_position_ns_key),
            )
            storage_time_instant_element.append(storage_time_position_element)
            storage_time_element.append(storage_time_instant_element)
            # We need to find correct position for element
            xml_child_tag_names = self._child_tag_names(self.xml)
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

        ref_map = dict(refs)
        elements: list[ET._Element] = self.xml.xpath(xpath, **constants.NAMESPACES)

        for element in elements:
            attrib_key = self._ns_key_to_clark_notation(constants.XPATH_XLINK_HREF)
            attrib_val = str(element.attrib[attrib_key]).removeprefix("#")
            ref_val = ref_map.get(attrib_val, None)

            if ref_val:
                element.attrib[attrib_key] = f"#{ref_val}"
            else:
                self.ref_errors.append(f"{xpath} = {attrib_val}")

    def post_validate(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error
