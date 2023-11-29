# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


def xmlToMetadataElementDictFixed(xml):
    """słownik metadataElementDict na podstawie pliku XML"""
    fixedElementsDict = {}
    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'gmx': "http://www.isotc211.org/2005/gmx",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml",
          'srv': "http://www.isotc211.org/2005/srv",
          'xlink': "http://www.w3.org/1999/xlink",
          'xs': "http://www.w3.org/2001/XMLSchema",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
          }

    root = ET.parse(xml)
    # E3
    element = root.find('/gmd:hierarchyLevel/gmd:MD_ScopeCode', ns)
    if element is not None:
        fixedElementsDict['e3'] = ''

    # E8
    element = root.find('/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode', ns)
    if element is not None:
        fixedElementsDict['e8'] = ''

    # E17
    element = root.find(
        '/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode', ns)
    if element is not None:
        fixedElementsDict['e17'] = ''

    # E19
    element = root.find(
        '/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:explanation', ns)
    if element is not None:
        fixedElementsDict['e19'] = ''

    # E21
    element = root.find(
        '/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor',
        ns)
    if element is not None:
        fixedElementsDict['e21'] = ''

    # E23
    element = root.find(
        '/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode[@codeListValue="custodian"]',
        ns)
    if element is not None:
        fixedElementsDict['e23'] = ''

    # E25
    element = root.find(
        '/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:version',
        ns)
    if element is not None:
        fixedElementsDict['e25'] = ''

    # E26
    element = root.find(
        '/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode[@codeListValue="asNeeded"]',
        ns)
    if element is not None:
        fixedElementsDict['e26'] = ''

    # E28
    element = root.find(
        '/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:updateScope/gmd:MD_ScopeCode[@codeListValue="dataset"]',
        ns)
    if element is not None:
        fixedElementsDict['e28'] = ''

    # E30
    element = root.find(
        '/gmd:dateStamp/gco:Date', ns)
    if element is not None:
        fixedElementsDict['e30'] = ''

    # E31
    element = root.find(
        '/gmd:language/gmd:LanguageCode', ns)
    if element is not None:
        fixedElementsDict['e31'] = ''

    # E33
    element = root.find(
        '/gmd:metadataStandardName/gco:CharacterString', ns)
    if element is not None:
        fixedElementsDict['e33'] = ''

    # E34
    element = root.find(
        '/gmd:metadataStandardVersion/gco:CharacterString', ns)
    if element is not None:
        fixedElementsDict['e34'] = ''

    return fixedElementsDict