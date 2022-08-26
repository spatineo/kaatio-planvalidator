import xml.etree.ElementTree as ET
import xmlschema
import pygml
import shapely
import geopandas
import uuid

from shapely.geometry import Polygon
from shapely.validation import explain_validity

namespaces = {'lud-core': "http://tietomallit.ymparisto.fi/mkp-ydin/xml/1.2",
              'splan': "http://tietomallit.ymparisto.fi/kaavatiedot/xml/1.2"}


def main():
    message = []
    try:
        tree = ET.parse('virallinenKaatio.xml')
        print('XML-tiedostolla on yksi root ja jokaisella avaavalla tagilla on lopetustagi')
    except ET.ParseError as err:
        message.append(err)
        return message
    root = tree.getroot()

    # validateSchema()
    # validatePlanIdentifier(root)
    # validateBoundary(root)
    # validateGeom_b(root)
    # findGmlIds(root)
    # createObjectIdentifier(root, tree)

    return


def validateSchema():
    my_schema = xmlschema.XMLSchema('spatialplan-1.2.xsd', 
        base_url='schema/', 
        namespace='http://tietomallit.ymparisto.fi/kaavatiedot/xml/1.2',
        locations=[
            ('http://tietomallit.ymparisto.fi/ry-yhteiset/kielituki/xml/1.0', 'localization-1.0.xsd'),
            ('http://tietomallit.ymparisto.fi/mkp-ydin/xml/1.2', 'land-use-decision-core-1.2.xsd'),
            ('http://www.w3.org/1999/xlink', 'xlink.xsd'),
            ('http://www.opengis.net/gml/3.3/exr', 'extdEncRule.xsd'),
            ('http://www.opengis.net/gml/3.2', 'gml/gml.xsd'),
            ('http://www.isotc211.org/2005/gmd', 'gmd/gmd.xsd'), 
            ('http://www.isotc211.org/2005/gss', 'gss/gss.xsd'),
            ('http://www.isotc211.org/2005/gco', 'gco/gco.xsd'),
            ('http://www.isotc211.org/2005/gts', 'gts/gts.xsd'),
            ('http://www.isotc211.org/2005/gsr', 'gsr/gsr.xsd')
        ],
        build=True)
    
    my_schema.validate('virallinenKaatio.xml')

    is_valid = my_schema.is_valid('virallinenKaatio.xml')
    if is_valid:
        print('True')
    else:
        print('False')


def validatePlanIdentifier(xml_root):

    try:
        first_featureMember: ET.Element = xml_root.find(
            'lud-core:featureMember', namespaces)
        first_spatialPlan = first_featureMember.find(
            'splan:SpatialPlan', namespaces)
        planIdentifier = first_spatialPlan.find(
            'splan:planIdentifier', namespaces)
        if len(planIdentifier.text) > 0:
            print("PlanIdentifier tagissa on tekstiä")
            return True
    except TypeError:
        print("No text in planIdentifier")


def createObjectIdentifier(xml_root, xml_tree):
    new_id = f"id-{uuid.uuid4()}"
    first_featureMember = xml_root.find(
        'lud-core:featureMember', namespaces)
    first_spatialPlan = first_featureMember.find(
        'splan:SpatialPlan', namespaces)
    spatial_plan = ET.Element(first_spatialPlan)
    objectIdentifier = ET.SubElement(
        spatial_plan, '{http://tietomallit.ymparisto.fi/mkp-ydin/xml/1.2}objectIdentifier')
    objectIdentifier.text = new_id
    first_spatialPlan.insert(0, objectIdentifier)
    xml_tree.write(open('output.xml', 'wb'), encoding="UTF-8")

    # objectIdentifier = first_spatialPlan.find(
    #     'lud-core:objectIdentifier', namespaces)
    # if objectIdentifier:
    #     print("True")
    # else:
    #     print("false")


def findGmlIds(xml_root):
    gml_id_dict = {}
    for child in xml_root.iter():
        for key, value in child.attrib.items():
            if "id" in key:
                gml_id_dict[value] = {"old_gml_id": value}
    checkAllLinks(gml_id_dict, xml_root)


def checkAllLinks(gmlDict, xml_root):
    for child in xml_root.iter():
        for key, value in child.attrib.items():
            if "href" in key and "#" in value:
                get_link_value = value.split('#', 1)[1]
                if gmlDict.get(get_link_value) == None:
                    print(f"{get_link_value} Does not exist as a gml_id")
                else:
                    print(f"{get_link_value} is a gml_id")

    return


def validateBoundary(xml_root):
    first_featureMember = xml_root.find('lud-core:featureMember', namespaces)
    first_spatialPlan = first_featureMember.find(
        "splan:SpatialPlan", namespaces)
    first_boundary = first_spatialPlan.find("lud-core:boundary", namespaces)
    gml_geometry = first_boundary.find("*")
    result = ET.tostring(gml_geometry, encoding='utf8', method='xml')

    pygml_result = pygml.parse(result)


def validateGeom_b(xml_root):
    second_featureMember_planObject = xml_root[1].find(
        'splan:PlanObject', namespaces)
    second_featureMember_geometry = second_featureMember_planObject.find(
        'splan:geometry', namespaces)
    gml_geometry_b = second_featureMember_geometry.find('*')
    result = ET.tostring(gml_geometry_b, encoding='utf8', method='xml')
    pygml_result = pygml.parse(result)
    return


if __name__ == '__main__':
    main()

# Lataa kaikki schemat ja muuta linkit -> './...' muotoon
# ID generointi Priority 2: 1. kohdan Geometriat ovat valideja kohdan jälkeen
# found_jotain = root.find(
#     './lud-core:featureMember/splan:SpatialPlan', namespaces)
######################
# for-loopissa child.set("updated", "yes") asettaa attribuutin elementille
# jos pistää for child in root.iter("{...}featureMember") niin käy läpi kaikki featurememberit
