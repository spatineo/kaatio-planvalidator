spatialplan -> splan:generalOrder
spatialplan -> splan:participationAndEvalutionPlan
PlanObject -> splan:spatialPlan
planOrder -> splan:spatialPlan
planOrder -> splan:target (PlanObject)


gml:identifier tulee ennen objectidentifierii
objectIdentifier tulee jokaiseen featurememberiin
producerSpecificidentifier tulee viimeisenä näistä kolmesta
yllä olevat tulee jokaiseen featurememberiin
pisteen jälkeen toinen random uuid()


poista kaikki vanhat objectidentifierit ja luo uudet tilalle
#codeSpace="http://uri.suomi.fi/object/rytj/kaava"



###############################################
https://spatineo.github.io/ry-tietomallit/kehitys/kaatio/xml/esimerkit/spatialPlan-collection-simple-1st-save-with-ids.xml
