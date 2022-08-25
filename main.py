import xml.etree.ElementTree as ET
import xmlschema
import pygml
import shapely
import geopandas
import uuid

from shapely.geometry import Polygon
from shapely.validation import explain_validity


def main():
    # validateXML()
    # validateSchema()
    # validatePlanIdentifier()
    validateGeometrics()
    return


def validateXML():
    message = []
    try:
        ET.parse('virallinenKaatio.xml')
        print('XML-tiedostolla on yksi root ja jokaisella avaavalla tagilla on lopetustagi')
    except ET.ParseError as err:
        message.append(err)
        return message


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


def validatePlanIdentifier():
    tree = ET.parse('virallinenKaatio.xml')
    root = tree.getroot()
    try:
        for child in root[0][0]:
            get_planIdentifier = child.tag.split('}', 1)[0] + '}planIdentifier'
            if child.tag == get_planIdentifier:
                if len(child.text) > 0:
                    print("PlanIdentifier tagissa on tekstiä")
                    return True
    except TypeError:
        print("PlanIdentifier has no text")
    return


def validateGeometrics():
    tree = ET.parse("virallinenKaatio.xml")
    root = tree.getroot()
    first_posList = []
    second_posList = []
    for index in range(0, 2):
        for child in root[index].iter():
            n = 2
            get_posList = child.tag.split('}', 1)[0] + '}posList'
            if child.tag == get_posList:
                line = child.text
                if index == 0:
                    convert_to_array = child.text.split()
                    first_posList = [(convert_to_array[i], convert_to_array[i + 1])
                                     for i in range(0, len(convert_to_array), 2)]
                else:
                    convert_to_array = child.text.split()
                    second_posList = [(convert_to_array[i], convert_to_array[i + 1])
                                      for i in range(0, len(convert_to_array), 2)]

    # TÄLLÄ HETKELLÄ NUMEROT OVAT STRING-MUODOSSA -> PITÄÄKÖ MUUTTAA DECIMAL-MUOTOON????
    # lud-core:LandUseFeatureCollection oleva esim xmlns:splan -> jos splan:jotain, niin se tulee automaattisesti xml-elementin tagiin
    print(first_posList)
    print(second_posList)

    return


if __name__ == '__main__':
    main()

# Lataa kaikki schemat ja muuta linkit -> './...' muotoon
# ID generointi Priority 2: 1. kohdan Geometriat ovat valideja kohdan jälkeen
