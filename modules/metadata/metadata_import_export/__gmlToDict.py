# -*- coding: utf-8 -*-
from .. import dictionaries, utils
import xml.etree.ElementTree as ET
import re
from PyQt5.QtCore import QDateTime
from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsRectangle
from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsSettings


def appGmlToMetadataElementDict(gmlPath):
    """słownik metadataElementDict na podstawie pliku zbioru APP"""
    metadataElementDict = {}
    
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
    root = ET.parse(gmlPath)
    
    ns = {'gco': "http://www.isotc211.org/2005/gco",
          'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0",
          'gmd': "http://www.isotc211.org/2005/gmd",
          'gml': "http://www.opengis.net/gml/3.2",
          'wfs': "http://www.opengis.net/wfs/2.0",
          'xlink': "http://www.w3.org/1999/xlink",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance"
         }
    
    if rodzajZbioru != 'POG' and root.find('//app:AktPlanowaniaPrzestrzennego/app:idIIP/app:Identyfikator/app:przestrzenNazw', ns) is None:
        ns = {'gco': "http://www.isotc211.org/2005/gco",
              'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
              'gmd': "http://www.isotc211.org/2005/gmd",
              'gml': "http://www.opengis.net/gml/3.2",
              'wfs': "http://www.opengis.net/wfs/2.0",
              'xlink': "http://www.w3.org/1999/xlink",
              'xsi': "http://www.w3.org/2001/XMLSchema-instance"
             }
    
    # E1
    element = root.find('//app:AktPlanowaniaPrzestrzennego/app:typPlanu', ns)
    if element is not None:
        typPlanu = element.attrib['{%s}title' %
                                  ns['xlink']].replace('miejscowy', 'miejscowych').replace('plan', 'planów').replace('kier.', 'kierunków').replace('zagosp.', 'zagospodarowania').replace('przestrz.', 'przestrzennego')
        metadataElementDict['e1'] = {
            'e1_lineEdit': "Zbiór danych przestrzennych dla %s <typ_jednostki> <nazwa_jednostki>" % typPlanu}
    
    # E5
    date = root.find('//app:AktPlanowaniaPrzestrzennego/app:idIIP/app:Identyfikator/app:przestrzenNazw', ns)
    if date is None:
        utils.showPopup("Błąd pliku", "wczytany plik nie jest poprawną definicją GML dla zbioru APP. Zwaliduj plik przed wczytaniem do formularza metadanych", QMessageBox.Warning)
        return False
    metadataElementDict['e5'] = [{'e5_lineEdit': date.text}]
    
    # E7 - kodowanie z nagłówka GML
    with open(gmlPath, 'r') as file:
        line = file.readlines(1)[0]
        line.replace("'", '"')
        encoding = re.search('encoding="[a-zA-Z0-9\\-]{3,10}"', line)[0].split(
            "=")[-1].strip('"').replace(' ', '').replace('-', '').lower()
        if encoding == 'usascii':
            encoding = 'usAscii'
        metadataElementDict['e7'] = [{'e7_cmbbx': encoding}]

    # E9, E10 - słowa kluczowe
    itemsList = []
    date = root.find('//app:AktPlanowaniaPrzestrzennego/app:poziomHierarchii', ns)
    if date is not None:
        atrybut_title = date.attrib['{%s}title' % ns['xlink']]
        atrybut_href = date.attrib['{%s}href' % ns['xlink']]

    tekst = 'Regionalnym' if atrybut_title == 'regionalny' else 'Lokalne'

    # poziom administracyjny
    itemsList.append({
        'e9_lineEdit': tekst,
        'e10_cmbbx': 'Data opublikowania',
        'e10_dateTimeEdit': QDateTime(2019, 5, 22, 0, 0),
        'e10_lineEdit': 'Zakres przestrzenny',
        'xlink': "http://inspire.ec.europa.eu/metadata-codelist/SpatialScope"
    })

    # poziom jednostki
    itemsList.append({
        'e9_lineEdit': atrybut_title,
        'e10_cmbbx': 'Data opublikowania',
        'e10_dateTimeEdit': QDateTime(2013, 12, 10, 0, 0),
        'e10_lineEdit': 'Poziom planu zagospodarowania przestrzennego',
        'xlink': "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue"
    })

    # dodanie domyslnych wartosci kluczowych
    itemsList.extend(dictionaries.metadataListWidgetsDefaultItems['e9'])
    metadataElementDict['e9'] = itemsList

    # E11
    layer = QgsVectorLayer(
        gmlPath + '|layername=AktPlanowaniaPrzestrzennego', "gml",  'ogr')
    # if not layer.isValid(): # sprawdzanie czy AktPlanowaniaPrzestrzennego jest w wfs:member lub gml:featureMember (bezpośrednio)
    #     layer = QgsVectorLayer(gmlPath + '|layername=featureMember', "gml", 'ogr')
    if layer.isValid():

        sourceCrs = layer.crs()
        extent = layer.extent()
        # w zwiazku z niepoprawnym zaczytywaniem zasiegu GML przez QGIS - odwrocenie osi
        '''
        Dla wersji QGIS <= 3.14 przy wczytywaniu GML
        # z definicją układu
        # jako uri do opengis.net np. http://www.opengis.net/def/crs/EPSG/0/2177
        # QGIS wczytuje zasięg z odwróconymi X i Y
        # TODO: do wykomentowania gdy błąd zostanie naprawiony w nowej wersji programu
        # dla starych - pozostaje
        '''
        extentInverted = QgsRectangle(extent.yMinimum(), extent.xMinimum(), extent.yMaximum(), extent.xMaximum())
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS84
        xform = QgsCoordinateTransform(
            sourceCrs, crsDest, QgsProject.instance())
        extent84 = xform.transform(extentInverted)
        metadataElementDict['e11'] = [{'e11_lineEdit': '%s,%s,%s,%s' % (extent84.xMinimum(), extent84.xMaximum(), extent84.yMinimum(), extent84.yMaximum())}]

    # E12
    itemsList = []
    # szukaj w rysunkach APP
    for uklad in root.findall('//*/app:ukladOdniesieniaPrzestrzennego', ns):
        if {'e12_cmbbx': uklad.text} not in itemsList:
            itemsList.append({'e12_cmbbx': uklad.text})
    # szukaj w zasięgach APP
    for multiSurface in root.findall('//*/app:zasiegPrzestrzenny/gml:MultiSurface', ns):
        if {'e12_cmbbx': multiSurface.attrib['srsName']} not in itemsList:
            itemsList.append({'e12_cmbbx': multiSurface.attrib['srsName']})
    metadataElementDict['e12'] = itemsList

    # E13
    dates = []
    for date in root.findall('//app:AktPlanowaniaPrzestrzennego/app:poczatekWersjiObiektu', ns):
        dates.append(QDateTime.fromString(date.text, "yyyy-MM-dd'T'hh:mm:ss"))
    oldestDate = utils.oldestQDateTime(dates)
    if oldestDate is not None:
        metadataElementDict['e13'] = {'e13_dateTimeEdit': oldestDate}

    # E16
    itemsList = []
    for rozdzielczosc in root.findall('//*/app:rozdzielczoscPrzestrzenna', ns):
        if {'e16_lineEdit': rozdzielczosc.text} not in itemsList:
            itemsList.append({'e16_lineEdit': rozdzielczosc.text})
    metadataElementDict['e16'] = itemsList

    # E18 i E19 i E24 i E25
    itemsList = []
    inspire1 = "Rozporządzenie Komisji (UE) Nr 1089/2010 z dnia 23 listopada 2010 r. w sprawie wykonania dyrektywy 2007/2/WE Parlamentu Europejskiego i Rady w zakresie interoperacyjności zbiorów i usług danych przestrzennych"
    inspire2 = "D2.8.III.4 Data Specification on Land Use – Technical Guidelines"
    krajowy1 = "Rozporządzenie Ministra Rozwoju, Pracy i Technologii z dnia 26 października 2020 r. w sprawie zbiorów danych przestrzennych oraz metadanych w zakresie zagospodarowania przestrzennego"
    krajowy2 = "Planowanie przestrzenne: Specyfikacja danych"

    ifKrajowy = False
    ifInspire = False
    namespaces = dict(
        [node for _, node in ET.iterparse(gmlPath, events=['start-ns'])])
    for v in namespaces.values():
        if 'https://www.gov.pl/static/zagospodarowanieprzestrzenne' in v:
            ifKrajowy = True
            # ifInspire = False
            break
        if 'http://inspire.ec.europa.eu/schemas/plu/4.0/PlannedLandUse.xsd' in v:
            # ifKrajowy = False
            ifInspire = True
            break

    # E18 i E19 inspire1
    itemsList.append({
        'e18_lineEdit': inspire1,
        'e18_dateTimeEdit': QDateTime(2010, 12, 8, 0, 0),
        'e18_cmbbx': 'Data opublikowania',
        'e19_cmbbx': 'Zgodny (conformant)' if ifInspire else 'Niezgodny (notConformant)',
        'xlink': "http://data.europa.eu/eli/reg/2010/1089"
    })
    # E18 i E19 inspire2
    itemsList.append({
        'e18_lineEdit': inspire2,
        'e18_dateTimeEdit': QDateTime(2013, 12, 10, 0, 0),
        'e18_cmbbx': 'Data opublikowania',
        'e19_cmbbx': 'Zgodny (conformant)' if ifInspire else 'Niezgodny (notConformant)'
    })
    # E18 i E19 krajowy1
    itemsList.append({
        'e18_lineEdit': krajowy1,
        'e18_dateTimeEdit': QDateTime(2020, 10, 31, 0, 0),
        'e18_cmbbx': 'Data opublikowania',
        'e19_cmbbx': 'Zgodny (conformant)' if ifKrajowy else 'Niezgodny (notConformant)',
        'xlink': "https://dziennikustaw.gov.pl/DU/2020/1916"
    })
    # E18 i E19 krajowy2
    itemsList.append({
        'e18_lineEdit': krajowy2,
        'e18_dateTimeEdit': QDateTime(2020, 10, 31, 0, 0),
        'e18_cmbbx': 'Data opublikowania',
        'e19_cmbbx': 'Zgodny (conformant)' if ifKrajowy else 'Niezgodny (notConformant)',
        'xlink': ""   # TODO: uaktualnić po publikacji
    })
    metadataElementDict['e18'] = itemsList

    # E24 i E25 krajowy
    itemsList = []
    if ifKrajowy:
        itemsList.append({
            'e24_lineEdit': "Schemat aplikacyjny GML Planowanie przestrzenne",
            'e25_lineEdit': "1.0"
        })
    if ifInspire:
        itemsList.append({
            'e24_lineEdit': "Planned Land Use GML Application Schema",
            'e25_lineEdit': "4.0"
        })
    metadataElementDict['e24'] = itemsList

    return metadataElementDict
