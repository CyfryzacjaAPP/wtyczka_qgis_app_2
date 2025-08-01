# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QDateTime
from qgis.core import QgsMessageLog
from . import translation
from .. import utils, dictionaries

def xmlToMetadataElementDict(xml):
    """słownik metadataElementDict na podstawie pliku XML"""
    metadataElementDict = {}

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

    # E1
    element = root.find('//gmd:MD_DataIdentification/*/gmd:CI_Citation/gmd:title/gco:CharacterString', ns)
    if element is not None:
        data = {'e1_lineEdit': element.text}
        metadataElementDict['e1'] = data

    # E2
    element = root.find('//gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString', ns)
    if element is not None:
        data = {'e2_lineEdit': element.text}
        metadataElementDict['e2'] = data

    # E4
    itemsList = []
    for element in root.findall('//gmd:transferOptions//gmd:linkage/gmd:URL', ns):
        if element.text not in itemsList:
            itemsList.append({'e4_lineEdit': element.text})
    metadataElementDict['e4'] = itemsList

    # E5
    itemsList = []
    for element in root.findall('//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier//gco:CharacterString', ns):
        idIppUri = element.text
        idIpp = '/'.join(idIppUri.strip().strip('/').split('/')[-2:])
        if idIpp not in itemsList:
            itemsList.append({'e5_lineEdit': idIpp})
    metadataElementDict['e5'] = itemsList

    # E6
    itemsList = []
    for element in root.findall(
            '//gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode', ns):
        if element.text not in itemsList and element.text in dictionaries.languages:
            itemsList.append({'e6_cmbbx': element.text})
    metadataElementDict['e6'] = itemsList

    # E7
    itemsList = []
    for element in root.findall(
            '/gmd:characterSet/gmd:MD_CharacterSetCode', ns):
        if element.attrib['codeListValue'] not in itemsList:
            itemsList.append({'e7_cmbbx': element.attrib['codeListValue']})
    metadataElementDict['e7'] = itemsList

    # E9 E10
    itemsList = []
    for descriptiveKeywords in root.findall(
            '//gmd:MD_DataIdentification/gmd:descriptiveKeywords', ns):
        data = {}

        keyword = descriptiveKeywords.find('.//gmd:keyword/gmx:Anchor', ns) # złożony KeyWord
        keywordSimple = descriptiveKeywords.find('.//gmd:keyword/gco:CharacterString', ns)   # prosty KeyWord
        if keyword is not None and keyword.text not in data:
            data['e9_lineEdit'] = keyword.text
        elif keywordSimple is not None and keywordSimple.text not in data:
            data['e9_lineEdit'] = keywordSimple.text

        thesaurus = descriptiveKeywords.find('.//gmd:thesaurusName', ns)
        if thesaurus is not None:
            thesaurus_title = thesaurus.find('.//gmd:title/gmx:Anchor', ns)
            if thesaurus_title is None:
                thesaurus_title = thesaurus.find('.//gmd:title/gco:CharacterString', ns)
            try:
                data['e10_lineEdit'] = thesaurus_title.text
            except Exception as e:
                QgsMessageLog.logMessage(f"Błąd:{str(e)}", 'APP2')
            try:
                data['xlink'] = thesaurus_title.attrib['{%s}href' % ns['xlink']]
            except Exception as e:
                QgsMessageLog.logMessage(f"Błąd:{str(e)}", 'APP2')
            date = thesaurus.find('.//gco:Date', ns)
            data['e10_dateTimeEdit'] = QDateTime.fromString(date.text, "yyyy-MM-dd")
            dateTypeCode = thesaurus.find('.//gmd:CI_DateTypeCode', ns)
            data['e10_cmbbx'] = utils.getKeyByValue(translation, dateTypeCode.attrib['codeListValue'])

        itemsList.append(data)
    metadataElementDict['e9'] = itemsList

    # E11
    itemsList = []
    for extent in root.findall(
            '//gmd:extent', ns):
        xmin = extent.find('.//gmd:westBoundLongitude/gco:Decimal', ns)
        xmax = extent.find('.//gmd:eastBoundLongitude/gco:Decimal', ns)
        ymin = extent.find('.//gmd:southBoundLatitude/gco:Decimal', ns)
        ymax = extent.find('.//gmd:northBoundLatitude/gco:Decimal', ns)
        itemsList.append({'e11_lineEdit': "%s,%s,%s,%s" % (xmin.text, xmax.text, ymin.text, ymax.text)})
    metadataElementDict['e11'] = itemsList

    # E12
    itemsList = []
    for element in root.findall(
            '/gmd:referenceSystemInfo//gco:CharacterString', ns):
        if element.text not in itemsList:
            itemsList.append({'e12_cmbbx': element.text})
    metadataElementDict['e12'] = itemsList

    # E13 i E14
    for date in root.findall('//gmd:MD_DataIdentification/*/gmd:CI_Citation/gmd:date', ns):
        _date = date.find('.//gco:Date', ns)
        dateType = date.find('.//gmd:CI_DateTypeCode', ns)
        if dateType.attrib['codeListValue'] == "creation":  #E13
            metadataElementDict['e13'] = {'e13_dateTimeEdit': QDateTime.fromString(_date.text, "yyyy-MM-dd")}
        if dateType.attrib['codeListValue'] == "publication":  #E14
            metadataElementDict['e14'] = {'e14_dateTimeEdit': QDateTime.fromString(_date.text, "yyyy-MM-dd")}

    # E15
    element = root.find('/gmd:dataQualityInfo/*/gmd:lineage//gco:CharacterString', ns)
    if element is not None:
        data = {'e15_lineEdit': element.text}
        metadataElementDict['e15'] = data

    # E16
    itemsList = []
    for element in root.findall(
            '//gmd:MD_DataIdentification/gmd:spatialResolution//gmd:denominator/gco:Integer', ns):
        if element.text not in itemsList:
            itemsList.append({'e16_lineEdit': element.text})
    metadataElementDict['e16'] = itemsList

    # E18 i E19
    itemsList = []
    for report in root.findall(
            '/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report', ns):
        data = {}
        title = report.find('.//gmd:specification/gmd:CI_Citation/gmd:title/gco:CharacterString', ns)
        title_anchor = report.find('.//gmd:specification/gmd:CI_Citation/gmd:title/gmx:Anchor', ns)
        date = report.find('.//gmd:specification/gmd:CI_Citation/gmd:date//gco:Date', ns)
        dateType = report.find('.//gmd:specification/gmd:CI_Citation//gmd:dateType/gmd:CI_DateTypeCode', ns)
        exp_anchor = report.find('.//gmd:explanation/gmx:Anchor', ns)
        # _pass = report.find('.//gmd:pass/gco:Boolean', ns)
        if title is not None:
            data['e18_lineEdit'] = title.text
        elif title_anchor is not None:
            data['e18_lineEdit'] = title_anchor.text
            data['xlink'] = title_anchor.attrib['{%s}href' % ns['xlink']]
        else:
            data['e18_lineEdit'] = ""
        data['e18_dateTimeEdit'] = QDateTime.fromString(date.text, "yyyy-MM-dd")
        data['e18_cmbbx'] = utils.getKeyByValue(translation, dateType.attrib['codeListValue'])
        data['e19_cmbbx'] = utils.getKeyByValue(dictionaries.zgodnoscAnchors, exp_anchor.attrib['{%s}href' % ns['xlink']])
        itemsList.append(data)
    metadataElementDict['e18'] = itemsList

    # E20
    itemsList = []
    for element in root.findall(
            '//gmd:MD_DataIdentification/gmd:resourceConstraints//gmd:useConstraints/../gmd:otherConstraints/gmx:Anchor', ns):
        itemsList.append({'e20_lineEdit': element.text})
    metadataElementDict['e20'] = itemsList

    # E22 i E23
    itemsList = []
    for pointOfContact in root.findall(
            '//gmd:MD_DataIdentification/gmd:pointOfContact', ns):
        organisationName = pointOfContact.find('.//gmd:organisationName/gco:CharacterString', ns)
        mail = pointOfContact.find('.//gmd:contactInfo//gmd:electronicMailAddress/gco:CharacterString', ns)
        role = pointOfContact.find('.//gmd:CI_RoleCode', ns)
        itemsList.append({
            'e22_name_lineEdit': organisationName.text,
            'e22_mail_lineEdit': mail.text,
            'e23_cmbbx': utils.getKeyByValue(translation, role.attrib['codeListValue'])
        })
    metadataElementDict['e22'] = itemsList

    # E24/E25
    itemsList = []
    for distributionFormat in root.findall('//gmd:MD_Distribution/gmd:distributionFormat', ns):
        name = distributionFormat.find('.//gmd:name/gco:CharacterString', ns)
        version = distributionFormat.find('.//gmd:version/gco:CharacterString', ns)
        itemsList.append({
            'e24_lineEdit': name.text,
            'e25_lineEdit': version.text,
        })
    metadataElementDict['e24'] = itemsList

    # E27
    itemsList = []
    for element in root.findall(
            '//gmd:MD_DataIdentification/gmd:resourceMaintenance//gmd:maintenanceNote/gco:CharacterString',
            ns):
        itemsList.append({'e27_lineEdit': element.text})
    metadataElementDict['e27'] = itemsList

    # E29
    itemsList = []
    for contact in root.findall('/gmd:contact', ns):
        organisationName = contact.find('.//gmd:organisationName/gco:CharacterString', ns)
        mail = contact.find('.//gmd:contactInfo//gmd:electronicMailAddress/gco:CharacterString', ns)
        itemsList.append({
            'e29_name_lineEdit': organisationName.text,
            'e29_mail_lineEdit': mail.text,
            'e29_cmbbx': 'Punkt kontaktowy (pointOfContact)'
        })
    metadataElementDict['e29'] = itemsList

    # E32
    element = root.find('/gmd:fileIdentifier/gco:CharacterString', ns)
    if element is not None:
        metadataElementDict['e32'] = {'e32_lineEdit': element.text}


    return metadataElementDict