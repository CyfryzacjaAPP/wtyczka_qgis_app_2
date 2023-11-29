# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.dom import minidom
from . import translation
from .. import dictionaries, utils


def metadataElementDictToXml(metadataElementDict):
    """tworzy XML na podstawie słownika metadataElementDict"""

    # Przestrzenie nazw ustawione na sztywno
    namespaces = {
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:gmx': "http://www.isotc211.org/2005/gmx",
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:gml': "http://www.opengis.net/gml",
        'xmlns:srv': "http://www.isotc211.org/2005/srv",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20070417/gmd/gmd.xsd http://www.isotc211.org/2005/gmx http://schemas.opengis.net/iso/19139/20070417/gmx/gmx.xsd http://www.isotc211.org/2005/srv http://schemas.opengis.net/iso/19139/20070417/srv/1.0/srv.xsd"
    }

    """gmd:MD_Metadata"""
    root = ET.Element('gmd:MD_Metadata')
    for ns in namespaces.keys():
        root.set(ns, namespaces[ns])

    """gmd:fileIdentifier"""
    fileIdentifier = ET.SubElement(root, 'gmd:fileIdentifier')
    characterString = ET.SubElement(fileIdentifier, 'gco:CharacterString')
    characterString.text = metadataElementDict['e32']['e32_lineEdit']

    """gmd:language"""
    language = ET.SubElement(root, 'gmd:language')
    lang = metadataElementDict['e31']['e31_lineEdit']
    languageCode = ET.SubElement(language, 'gmd:LanguageCode', {
                                 'codeList': "http://www.loc.gov/standards/iso639-2/", 'codeListValue': dictionaries.languages[lang]})
    languageCode.text = lang

    """gmd:characterSet"""
    for listItem in metadataElementDict['e7']:
        characterSet = ET.SubElement(root, 'gmd:characterSet')
        ET.SubElement(characterSet, 'gmd:MD_CharacterSetCode',
                      {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_CharacterSetCode", 'codeListValue': listItem['e7_cmbbx']})

    """gmd:hierarchyLevel"""
    hierarchyLevel = ET.SubElement(root, 'gmd:hierarchyLevel')
    ET.SubElement(hierarchyLevel, 'gmd:MD_ScopeCode',
                  {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode", 'codeListValue': metadataElementDict['e3']['e3_lineEdit']})

    """gmd:contact"""
    for listItem in metadataElementDict['e29']:
        contact = ET.SubElement(root, 'gmd:contact')
        cI_ResponsibleParty = ET.SubElement(contact, 'gmd:CI_ResponsibleParty')
        """gmd:organisationName"""
        organisationName = ET.SubElement(
            cI_ResponsibleParty, 'gmd:organisationName')
        characterString = ET.SubElement(
            organisationName, 'gco:CharacterString')
        characterString.text = listItem['e29_name_lineEdit']
        """gmd:contactInfo"""
        contactInfo = ET.SubElement(cI_ResponsibleParty, 'gmd:contactInfo')
        cI_Contact = ET.SubElement(contactInfo, 'gmd:CI_Contact')
        address = ET.SubElement(cI_Contact, 'gmd:address')
        cI_Address = ET.SubElement(address, 'gmd:CI_Address')
        electronicMailAddress = ET.SubElement(
            cI_Address, 'gmd:electronicMailAddress')
        characterString = ET.SubElement(
            electronicMailAddress, 'gco:CharacterString')
        characterString.text = listItem['e29_mail_lineEdit']
        """gmd:role"""
        role = ET.SubElement(cI_ResponsibleParty, 'gmd:role')
        ET.SubElement(role, 'gmd:CI_RoleCode', {
                      'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode", 'codeListValue': translation[listItem['e29_cmbbx']]})

    """gmd:dateStamp"""
    dateStamp = ET.SubElement(root, 'gmd:dateStamp')
    date = ET.SubElement(dateStamp, 'gco:Date')
    date.text = metadataElementDict['e30']['e30_dateTimeEdit'].toString(
        "yyyy-MM-dd")

    """gmd:metadataStandardName"""
    metadataStandardName = ET.SubElement(root, 'gmd:metadataStandardName')
    characterString = ET.SubElement(
        metadataStandardName, 'gco:CharacterString')
    characterString.text = metadataElementDict['e33']['e33_lineEdit']

    """gmd:metadataStandardVersion"""
    metadataStandardVersion = ET.SubElement(
        root, 'gmd:metadataStandardVersion')
    characterString = ET.SubElement(
        metadataStandardVersion, 'gco:CharacterString')
    characterString.text = metadataElementDict['e34']['e34_lineEdit']

    """gmd:referenceSystemInfo"""
    for listItem in metadataElementDict['e12']:
        referenceSystemInfo = ET.SubElement(root, 'gmd:referenceSystemInfo')
        mD_ReferenceSystem = ET.SubElement(
            referenceSystemInfo, 'gmd:MD_ReferenceSystem')
        referenceSystemIdentifier = ET.SubElement(
            mD_ReferenceSystem, 'gmd:referenceSystemIdentifier')
        rS_Identifier = ET.SubElement(
            referenceSystemIdentifier, 'gmd:RS_Identifier')
        code = ET.SubElement(rS_Identifier, 'gmd:code')
        characterString = ET.SubElement(code, 'gco:CharacterString')
        characterString.text = listItem['e12_cmbbx']

    """gmd:identificationInfo"""
    identificationInfo = ET.SubElement(root, 'gmd:identificationInfo')
    # id na podstawie E5
    typZbioru = ''
    for listItem in metadataElementDict['e5']:
        if utils.validateDatasetId(listItem['e5_lineEdit']):
            typZbioru = listItem['e5_lineEdit'].strip(
                '/').split("/")[-1].split('-')[-1]
            break
    mD_DataIdentification = ET.SubElement(
        identificationInfo, 'gmd:MD_DataIdentification', {'id': typZbioru})

    """gmd:citation"""
    citation = ET.SubElement(mD_DataIdentification, 'gmd:citation')
    cI_Citation = ET.SubElement(citation, 'gmd:CI_Citation')
    title = ET.SubElement(cI_Citation, 'gmd:title')
    characterString = ET.SubElement(title, 'gco:CharacterString')
    characterString.text = metadataElementDict['e1']['e1_lineEdit']
    date = ET.SubElement(cI_Citation, 'gmd:date')
    cI_Date = ET.SubElement(date, 'gmd:CI_Date')
    date2 = ET.SubElement(cI_Date, 'gmd:date')
    date3 = ET.SubElement(date2, 'gco:Date')
    date3.text = metadataElementDict['e13']['e13_dateTimeEdit'].toString(
        "yyyy-MM-dd")
    dateType = ET.SubElement(cI_Date, 'gmd:dateType')
    ET.SubElement(dateType, 'gmd:CI_DateTypeCode', {'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode',
                                                    'codeListValue': translation[metadataElementDict['e13']['e13_cmbbx']]})
    if metadataElementDict['e14']['e14_dateTimeEdit']:
        date = ET.SubElement(cI_Citation, 'gmd:date')
        cI_Date = ET.SubElement(date, 'gmd:CI_Date')
        date2 = ET.SubElement(cI_Date, 'gmd:date')
        date3 = ET.SubElement(date2, 'gco:Date')
        date3.text = metadataElementDict['e14']['e14_dateTimeEdit'].toString(
            "yyyy-MM-dd")
        dateType = ET.SubElement(cI_Date, 'gmd:dateType')
        ET.SubElement(dateType, 'gmd:CI_DateTypeCode',
                      {'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode',
                       'codeListValue': translation[metadataElementDict['e14']['e14_cmbbx']]})

    for listItem in metadataElementDict['e5']:
        identifier = ET.SubElement(cI_Citation, 'gmd:identifier')
        mD_Identifier = ET.SubElement(identifier, 'gmd:MD_Identifier')
        code = ET.SubElement(mD_Identifier, 'gmd:code')
        characterString = ET.SubElement(code, 'gco:CharacterString')
        idIpp = listItem['e5_lineEdit']
        idIppUri = 'https://www.gov.pl/zagospodarowanieprzestrzenne/app/AktPlanowaniaPrzestrzennego/%s/' % idIpp
        characterString.text = idIppUri

    """gmd:abstract"""
    abstract = ET.SubElement(mD_DataIdentification, 'gmd:abstract')
    characterString = ET.SubElement(abstract, 'gco:CharacterString')
    characterString.text = metadataElementDict['e2']['e2_lineEdit']

    """gmd:pointOfContact"""
    for listItem in metadataElementDict['e22']:
        pointOfContact = ET.SubElement(
            mD_DataIdentification, 'gmd:pointOfContact')
        cI_ResponsibleParty = ET.SubElement(
            pointOfContact, 'gmd:CI_ResponsibleParty')
        """gmd:organisationName"""
        organisationName = ET.SubElement(
            cI_ResponsibleParty, 'gmd:organisationName')
        characterString = ET.SubElement(
            organisationName, 'gco:CharacterString')
        characterString.text = listItem['e22_name_lineEdit']
        """gmd:contactInfo"""
        contactInfo = ET.SubElement(cI_ResponsibleParty, 'gmd:contactInfo')
        cI_Contact = ET.SubElement(contactInfo, 'gmd:CI_Contact')
        address = ET.SubElement(cI_Contact, 'gmd:address')
        cI_Address = ET.SubElement(address, 'gmd:CI_Address')
        electronicMailAddress = ET.SubElement(
            cI_Address, 'gmd:electronicMailAddress')
        characterString = ET.SubElement(
            electronicMailAddress, 'gco:CharacterString')
        characterString.text = listItem['e22_mail_lineEdit']
        """gmd:role"""
        role = ET.SubElement(cI_ResponsibleParty, 'gmd:role')
        ET.SubElement(role, 'gmd:CI_RoleCode',
                      {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode",
                       'codeListValue': translation[listItem['e23_cmbbx']]})

    """gmd:resourceMaintenance"""
    resourceMaintenance = ET.SubElement(
        mD_DataIdentification, 'gmd:resourceMaintenance')
    mD_MaintenanceInformation = ET.SubElement(
        resourceMaintenance, 'gmd:MD_MaintenanceInformation')
    maintenanceAndUpdateFrequency = ET.SubElement(
        mD_MaintenanceInformation, 'gmd:maintenanceAndUpdateFrequency')
    ET.SubElement(maintenanceAndUpdateFrequency, 'gmd:MD_MaintenanceFrequencyCode', {'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_MaintenanceFrequencyCode",
                                                                                     'codeListValue': translation[metadataElementDict['e26']['e26_lineEdit']]})
    updateScope = ET.SubElement(mD_MaintenanceInformation, 'gmd:updateScope')
    ET.SubElement(updateScope, 'gmd:MD_ScopeCode', {
        'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode",
        'codeListValue': translation[metadataElementDict['e28']['e28_lineEdit']]})

    for listItem in metadataElementDict['e27']:
        maintenanceNote = ET.SubElement(
            mD_MaintenanceInformation, 'gmd:maintenanceNote')
        characterString = ET.SubElement(maintenanceNote, 'gco:CharacterString')
        characterString.text = listItem['e27_lineEdit']

    """gmd:descriptiveKeywords"""
    for listItem in metadataElementDict['e9']:
        descriptiveKeywords = ET.SubElement(
            mD_DataIdentification, 'gmd:descriptiveKeywords')
        mD_Keywords = ET.SubElement(descriptiveKeywords, 'gmd:MD_Keywords')
        keyword = ET.SubElement(mD_Keywords, 'gmd:keyword')
        keywordValue = listItem['e9_lineEdit']
        keywordValueLower = keywordValue[:].lower()
        slownikRoboczy = {**dictionaries.metadataKeywordAnchors,
                          **dictionaries.poziomyHierarchii}
        if keywordValueLower in slownikRoboczy:  # jest anchor w slowniku
            anchor = ET.SubElement(keyword,
                                   'gmx:Anchor',
                                   {'xlink:href': slownikRoboczy[keywordValueLower]})
            anchor.text = keywordValue
        else:  # zwykly tekst
            characterString = ET.SubElement(keyword, 'gco:CharacterString')
            characterString.text = keywordValue

        if 'e10_lineEdit' in listItem and listItem['e10_lineEdit']:
            """gmd:thesaurusName"""
            thesaurusName = ET.SubElement(mD_Keywords, 'gmd:thesaurusName')
            cI_Citation = ET.SubElement(thesaurusName, 'gmd:CI_Citation')
            title = ET.SubElement(cI_Citation, 'gmd:title')
            # if listItem['xlink']:
            if 'xlink' in listItem and listItem['xlink']:
                # xlink jeżeli istnieje
                anchor = ET.SubElement(title, 'gmx:Anchor', {
                                       'xlink:href': listItem['xlink']})
                anchor.text = listItem['e10_lineEdit']
            else:
                characterString = ET.SubElement(title, 'gco:CharacterString')
                characterString.text = listItem['e10_lineEdit']

            date = ET.SubElement(cI_Citation, 'gmd:date')
            cI_Date = ET.SubElement(date, 'gmd:CI_Date')
            date2 = ET.SubElement(cI_Date, 'gmd:date')
            date3 = ET.SubElement(date2, 'gco:Date')
            date3.text = listItem['e10_dateTimeEdit'].toString("yyyy-MM-dd")
            dateType = ET.SubElement(cI_Date, 'gmd:dateType')
            ET.SubElement(dateType, 'gmd:CI_DateTypeCode',
                          {'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode',
                           'codeListValue': translation[listItem['e10_cmbbx']]})

    """gmd:resourceConstraints E21"""
    resourceConstraints = ET.SubElement(
        mD_DataIdentification, 'gmd:resourceConstraints')
    mD_LegalConstraints = ET.SubElement(
        resourceConstraints, 'gmd:MD_LegalConstraints')
    accessConstraints = ET.SubElement(
        mD_LegalConstraints, 'gmd:accessConstraints')
    ET.SubElement(accessConstraints, 'gmd:MD_RestrictionCode',
                  {'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_RestrictionCode',
                   'codeListValue': 'otherRestrictions'})
    otherConstraints = ET.SubElement(
        mD_LegalConstraints, 'gmd:otherConstraints')
    anchor = ET.SubElement(otherConstraints, 'gmx:Anchor',
                           {'xlink:href': "http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/noLimitations"})  # xlink jeżeli istnieje
    anchor.text = metadataElementDict['e21']['e21_lineEdit']

    """gmd:resourceConstraints E20"""
    for listItem in metadataElementDict['e20']:
        resourceConstraints = ET.SubElement(
            mD_DataIdentification, 'gmd:resourceConstraints')
        mD_LegalConstraints = ET.SubElement(
            resourceConstraints, 'gmd:MD_LegalConstraints')
        useConstraints = ET.SubElement(
            mD_LegalConstraints, 'gmd:useConstraints')
        ET.SubElement(useConstraints, 'gmd:MD_RestrictionCode',
                      {
                          'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_RestrictionCode',
                          'codeListValue': 'otherRestrictions'})
        otherConstraints = ET.SubElement(
            mD_LegalConstraints, 'gmd:otherConstraints')

        if 'e20_lineEdit' in listItem and listItem['e20_lineEdit'] in dictionaries.metadataKeywordAnchors:
            xlink = dictionaries.metadataKeywordAnchors[listItem['e20_lineEdit']]
        else:
            xlink = ""
        anchor = ET.SubElement(otherConstraints, 'gmx:Anchor', {
                               'xlink:href': xlink})
        anchor.text = listItem['e20_lineEdit']

    """gmd:spatialRepresentationType"""
    for listItem in metadataElementDict['e17']:
        spatialRepresentationType = ET.SubElement(
            mD_DataIdentification, 'gmd:spatialRepresentationType')
        ET.SubElement(spatialRepresentationType, 'gmd:MD_SpatialRepresentationTypeCode', {
            'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_SpatialRepresentationTypeCode',
            'codeListValue': translation[listItem['e17_lineEdit']]})

    """gmd:spatialResolution"""
    for listItem in metadataElementDict['e16']:
        spatialResolution = ET.SubElement(
            mD_DataIdentification, 'gmd:spatialResolution')
        mD_Resolution = ET.SubElement(spatialResolution, 'gmd:MD_Resolution')
        equivalentScale = ET.SubElement(mD_Resolution, 'gmd:equivalentScale')
        mD_RepresentativeFraction = ET.SubElement(
            equivalentScale, 'gmd:MD_RepresentativeFraction')
        denominator = ET.SubElement(
            mD_RepresentativeFraction, 'gmd:denominator')
        integer = ET.SubElement(denominator, 'gco:Integer')
        integer.text = listItem['e16_lineEdit']

    """gmd:language"""
    for listItem in metadataElementDict['e6']:
        language = ET.SubElement(mD_DataIdentification, 'gmd:language')
        languageCode = ET.SubElement(language, 'gmd:LanguageCode', {
            'codeList': "http://www.loc.gov/standards/iso639-2/",
            'codeListValue': dictionaries.languages[listItem['e6_cmbbx']]
        })
        languageCode.text = listItem['e6_cmbbx']

    """gmd:topicCategory"""
    topicCategory = ET.SubElement(mD_DataIdentification, 'gmd:topicCategory')
    mD_TopicCategoryCode = ET.SubElement(
        topicCategory, 'gmd:MD_TopicCategoryCode')
    mD_TopicCategoryCode.text = translation[metadataElementDict['e8']['e8_lineEdit']]

    """gmd:extent"""
    for listItem in metadataElementDict['e11']:
        bbox = listItem['e11_lineEdit']
        bboxList = bbox.strip().split(',')
        if len(bboxList) == 4:
            xmin = bboxList[0]
            xmax = bboxList[1]
            ymin = bboxList[2]
            ymax = bboxList[3]
            extent = ET.SubElement(mD_DataIdentification, 'gmd:extent')
            eX_Extent = ET.SubElement(extent, 'gmd:EX_Extent')
            geographicElement = ET.SubElement(
                eX_Extent, 'gmd:geographicElement')
            eX_GeographicBoundingBox = ET.SubElement(
                geographicElement, 'gmd:EX_GeographicBoundingBox')
            westBoundLongitude = ET.SubElement(
                eX_GeographicBoundingBox, 'gmd:westBoundLongitude')
            decimal = ET.SubElement(westBoundLongitude, 'gco:Decimal')
            decimal.text = xmin
            eastBoundLongitude = ET.SubElement(
                eX_GeographicBoundingBox, 'gmd:eastBoundLongitude')
            decimal = ET.SubElement(eastBoundLongitude, 'gco:Decimal')
            decimal.text = xmax
            southBoundLatitude = ET.SubElement(
                eX_GeographicBoundingBox, 'gmd:southBoundLatitude')
            decimal = ET.SubElement(southBoundLatitude, 'gco:Decimal')
            decimal.text = ymin
            northBoundLatitude = ET.SubElement(
                eX_GeographicBoundingBox, 'gmd:northBoundLatitude')
            decimal = ET.SubElement(northBoundLatitude, 'gco:Decimal')
            decimal.text = ymax

    """gmd:distributionInfo"""
    distributionInfo = ET.SubElement(root, 'gmd:distributionInfo')
    mD_Distribution = ET.SubElement(distributionInfo, 'gmd:MD_Distribution')
    """gmd:distributionFormat"""
    for listItem in metadataElementDict['e24']:

        distributionFormat = ET.SubElement(
            mD_Distribution, 'gmd:distributionFormat')
        mD_Format = ET.SubElement(distributionFormat, 'gmd:MD_Format')
        name = ET.SubElement(mD_Format, 'gmd:name')
        characterString = ET.SubElement(name, 'gco:CharacterString')
        characterString.text = listItem['e24_lineEdit']
        version = ET.SubElement(mD_Format, 'gmd:version')
        characterString = ET.SubElement(version, 'gco:CharacterString')
        characterString.text = listItem['e25_lineEdit']

        if (listItem['e24_lineEdit'].split() == 'Schemat aplikacyjny GML Planowanie przestrzenne' and
            listItem['e25_lineEdit'].split() == '1.0'
            ):
            specification = ET.SubElement(mD_Format, 'gmd:specification')
            characterString = ET.SubElement(
                specification, 'gco:CharacterString')
            characterString.text = 'Specyfikacja danych: Planowanie przestrzenne v1.0'
        if (listItem['e24_lineEdit'].split() == 'Planned Land Use GML Application Schema' and
            listItem['e25_lineEdit'].split() == '4.0'
            ):
            specification = ET.SubElement(mD_Format, 'gmd:specification')
            characterString = ET.SubElement(
                specification, 'gco:CharacterString')
            characterString.text = 'D2.8.III.4 Data Specification on Land Use – Technical Guidelines'

    """gmd:transferOptions"""
    for listItem in metadataElementDict['e4']:
        transferOptions = ET.SubElement(mD_Distribution, 'gmd:transferOptions')
        mD_DigitalTransferOptions = ET.SubElement(
            transferOptions, 'gmd:MD_DigitalTransferOptions')
        onLine = ET.SubElement(mD_DigitalTransferOptions, 'gmd:onLine')
        cI_OnlineResource = ET.SubElement(onLine, 'gmd:CI_OnlineResource')
        linkage = ET.SubElement(cI_OnlineResource, 'gmd:linkage')
        uRL = ET.SubElement(linkage, 'gmd:URL')
        uRL.text = listItem['e4_lineEdit']

    """gmd:dataQualityInfo"""
    dataQualityInfo = ET.SubElement(root, 'gmd:dataQualityInfo')
    dQ_DataQuality = ET.SubElement(dataQualityInfo, 'gmd:DQ_DataQuality')
    """gmd:scope"""
    scope = ET.SubElement(dQ_DataQuality, 'gmd:scope')
    dQ_Scope = ET.SubElement(scope, 'gmd:DQ_Scope')
    level = ET.SubElement(dQ_Scope, 'gmd:level')
    mD_ScopeCode = ET.SubElement(level, 'gmd:MD_ScopeCode', {
        'codeList': "http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode",
        'codeListValue': translation[metadataElementDict['e28']['e28_lineEdit']]})
    mD_ScopeCode.text = translation[metadataElementDict['e28']['e28_lineEdit']]

    for listItem in metadataElementDict['e18']:
        """gmd:report"""
        report = ET.SubElement(dQ_DataQuality, 'gmd:report')
        dQ_DomainConsistency = ET.SubElement(
            report, 'gmd:DQ_DomainConsistency')
        result = ET.SubElement(dQ_DomainConsistency, 'gmd:result')
        dQ_ConformanceResult = ET.SubElement(
            result, 'gmd:DQ_ConformanceResult')
        specification = ET.SubElement(
            dQ_ConformanceResult, 'gmd:specification')
        cI_Citation = ET.SubElement(specification, 'gmd:CI_Citation')
        title = ET.SubElement(cI_Citation, 'gmd:title')

        if 'xlink' in listItem and listItem['xlink']:
            anchor = ET.SubElement(title, 'gmx:Anchor', {
                                   'xlink:href': listItem['xlink']})
            anchor.text = listItem['e18_lineEdit']
        else:
            characterString = ET.SubElement(title, 'gco:CharacterString')
            characterString.text = listItem['e18_lineEdit']

        date = ET.SubElement(cI_Citation, 'gmd:date')
        cI_Date = ET.SubElement(date, 'gmd:CI_Date')
        date2 = ET.SubElement(cI_Date, 'gmd:date')
        date3 = ET.SubElement(date2, 'gco:Date')
        date3.text = listItem['e18_dateTimeEdit'].toString("yyyy-MM-dd")
        dateType = ET.SubElement(cI_Date, 'gmd:dateType')
        ET.SubElement(dateType, 'gmd:CI_DateTypeCode',
                      {'codeList': 'http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode',
                       'codeListValue': translation[listItem['e18_cmbbx']]})
        explanation = ET.SubElement(dQ_ConformanceResult, 'gmd:explanation')
        exp_anchor = ET.SubElement(explanation, 'gmx:Anchor', {
                                   'xlink:href': dictionaries.zgodnoscAnchors[listItem['e19_cmbbx']]})
        exp_anchor.text = listItem['e19_cmbbx']

        conformancyLevel = listItem['e19_cmbbx']

        if conformancyLevel == 'Zgodny (conformant)':
            _pass = ET.SubElement(dQ_ConformanceResult, 'gmd:pass')
            boolean = ET.SubElement(_pass, 'gco:Boolean')
            boolean.text = 'true'
        elif conformancyLevel == 'Niezgodny (notConformant)':
            _pass = ET.SubElement(dQ_ConformanceResult, 'gmd:pass')
            boolean = ET.SubElement(_pass, 'gco:Boolean')
            boolean.text = 'false'
        elif conformancyLevel == 'Brak oceny zgodności (notEvaluated)':
            _pass = ET.SubElement(dQ_ConformanceResult, 'gmd:pass', {
                                  'gco:nilReason': "unknown"})

    """gmd:lineage"""
    lineage = ET.SubElement(dQ_DataQuality, 'gmd:lineage')
    lI_Lineage = ET.SubElement(lineage, 'gmd:LI_Lineage')
    statement = ET.SubElement(lI_Lineage, 'gmd:statement')
    characterString = ET.SubElement(statement, 'gco:CharacterString')
    characterString.text = metadataElementDict['e15']['e15_lineEdit']

    return minidom.parseString(ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')).toprettyxml(encoding='utf-8').decode('UTF-8')
