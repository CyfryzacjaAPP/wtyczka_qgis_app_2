# -*- coding: utf-8 -*-
from . import (TworzenieOUZDialog)
from .. import BaseModule
from ..utils import showPopup
from ..app.wtyczka_app import AppModule
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
import os
import shutil
from qgis.core import *
from PyQt5.QtCore import *
from qgis import processing
import pathlib
from qgis.core import QgsSettings, QgsDistanceArea
from datetime import date, datetime, timezone
import xml.etree.ElementTree as ET


class TworzenieOUZ(BaseModule):

    def __init__(self, iface):
        self.iface = iface
        self.tworzenieOUZ = None
        self.tworzenieOUZDialog = TworzenieOUZDialog()
        self.tworzenieOUZDialog.warstwaBudynki.setShowCrs(True)
        self.tworzenieOUZDialog.warstwaPOG.setShowCrs(True)
        self.tworzenieOUZDialog.tworzenie_btn.clicked.connect(self.tworzenieOUZ_btn_clicked)

    """Event handlers"""

    def tworzenieOUZ_btn_clicked(self):
        s = QgsSettings()
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
        numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
        jpt = s.value("qgis_app2/settings/jpt", "")
        idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP", "")
        epsg = str(s.value("qgis_app2/settings/strefaPL2000", ""))
        przestrzenNazw = 'PL.ZIPPZP.' + numerZbioru + '/' + jpt + '-' + rodzajZbioru
        defaultPath = s.value("qgis_app2/settings/defaultPath", "")
        
        try:
            warstwaZBudynkami = self.tworzenieOUZDialog.warstwaBudynki.currentLayer()
            warstwaZBudynkami.dataProvider().createSpatialIndex()
            warstwaZPOG = self.tworzenieOUZDialog.warstwaPOG.currentLayer()
            warstwaZPOG.dataProvider().createSpatialIndex()
            if  warstwaZBudynkami.name() == warstwaZPOG.name():
                showPopup("Wyznaczanie OUZ","Wybrano tą samą warstwę dla budynków i POG.")
                return
        except:
            showPopup("Wyznaczanie OUZ","Nie wskazano wymaganych warstw.")
            return
        
        if warstwaZBudynkami.featureCount() < 5:
            showPopup("Wyznaczanie OUZ","Warstwa z budynkami nie zawiera obiektów (minimum 5).")
            return
        
        def powierzchniaNaElipsoidzie(self, feature):
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            geom = feature.geometry()
            geom.transform(QgsCoordinateTransform(warstwaZBudynkami.crs(), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance().transformContext()))
            area = d.measureArea(geom)
            return area
        
        self.tworzenieOUZDialog.tworzenie_btn.setEnabled(False)
        self.tworzenieOUZDialog.progressBar.reset()
        self.tworzenieOUZDialog.progressBar.setValue(0)
        
        defaultPathDokumentacja = defaultPath + "/Dokumentacja/"
        if not os.path.exists(defaultPathDokumentacja):
            os.makedirs(defaultPathDokumentacja)
        
        if warstwaZBudynkami.crs().authid().split(":")[1] != epsg:
            # reprojekcja na epsg zapisany ustawieniach
            warstwaZBudynkami = processing.run("native:reprojectlayer", {
                'INPUT': self.tworzenieOUZDialog.warstwaBudynki.currentLayer(),
                'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:' + str(epsg)),
                'OUTPUT': 'memory:'
            })
            warstwaZBudynkami = warstwaZBudynkami['OUTPUT']
        
        # bufor wokół budynków z rozpuszczeniem granic
        bufory = processing.run("native:buffer", {
            'INPUT': warstwaZBudynkami,
            'DISTANCE':50,
            'SEGMENTS':5,
            'DISSOLVE': True,
            'MITER_LIMIT': 2,
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(10)
        QCoreApplication.processEvents()
        
        # rozbicie multipoligonu na poligony
        pojedynczeBufory = processing.run("native:multiparttosingleparts", {
            'INPUT': bufory['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(30)
        QCoreApplication.processEvents()
        
        # usunięcie buforów, na których znajduje się mnieij niż 5 budynków
        pojedynczeBufory['OUTPUT'].startEditing()
        for bufor in pojedynczeBufory['OUTPUT'].getFeatures():
            budynki = []
            for budynek in warstwaZBudynkami.getFeatures(bufor.geometry().boundingBox()):
                if (bufor.geometry()).contains(budynek.geometry()):
                    budynki.append(budynek)
            if len(budynki) < 5:
                pojedynczeBufory['OUTPUT'].deleteFeature(bufor.id())
        pojedynczeBufory['OUTPUT'].commitChanges()
        self.tworzenieOUZDialog.progressBar.setValue(50)
        QCoreApplication.processEvents()
        
        if pojedynczeBufory['OUTPUT'].featureCount() == 0:
            showPopup("Wyznaczanie OUZ","Brak budynków spełniających kryteria. Tworzenie OUZ zatrzymane.")
            self.tworzenieOUZDialog.progressBar.reset()
            self.tworzenieOUZDialog.progressBar.setValue(0)
            self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
            return
        
        # usunięcie dziur o powierzchni poniżej 5 000 m2
        buforyBezDziur = processing.run("native:deleteholes", {
            'INPUT': pojedynczeBufory['OUTPUT'],
            'MIN_AREA': 5000,
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(60)
        QCoreApplication.processEvents()
        
        # do wyliczenia Pb przycięcie do POG
        if warstwaZPOG.featureCount() > 0:
            buforyBezDziurPrzycieteDoPOG = processing.run("qgis:clip", {
                'INPUT': buforyBezDziur['OUTPUT'],
                'OVERLAY': warstwaZPOG,
                'OUTPUT': 'memory:'
            })
        
        # Pb - oznacza łączną powierzchnię obszarów wyznaczonych w sposób, o którym mowa w ust. 1 pkt 1–3
        Pb = 0
        for bbd in buforyBezDziurPrzycieteDoPOG['OUTPUT'].getFeatures():
            Pb += powierzchniaNaElipsoidzie(self,bbd)
        
        # bufor -40 m
        buforMinus40m = processing.run("native:buffer", {
            'INPUT': buforyBezDziur['OUTPUT'],
            'DISTANCE': -40,
            'SEGMENTS': 10,
            'DISSOLVE': True,
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(80)
        QCoreApplication.processEvents()
        
        # rozbicie multipoligon na poligony
        pojedynczeBufory40m = processing.run("native:multiparttosingleparts", {
            'INPUT': buforMinus40m['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        self.tworzenieOUZDialog.progressBar.setValue(90)
        QCoreApplication.processEvents()
        
        # jeżeli jest obiekt POG to przecięcie z OUZ
        if warstwaZPOG.featureCount() > 0:
            przyciecie = processing.run("qgis:clip", {
                'INPUT': pojedynczeBufory40m['OUTPUT'],
                'OVERLAY': warstwaZPOG,
                'OUTPUT': 'memory:'
            })
            
            if przyciecie['OUTPUT'].featureCount() == 0:
                showPopup("Wyznaczanie OUZ","Budynki nie leżą w obszarze objętym POG. Tworzenie OUZ zatrzymane.")
                self.tworzenieOUZDialog.progressBar.reset()
                self.tworzenieOUZDialog.progressBar.setValue(0)
                self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
                return
            
            # Pu - oznacza łączną powierzchnię obszarów uzupełnienia zabudowy wyznaczonych w sposób, o którym mowa w ust. 1
            Pu = 0
            for p in przyciecie['OUTPUT'].getFeatures():
                Pu += powierzchniaNaElipsoidzie(self,p)
            
            # Pp - oznacza łączną maksymalną powierzchnię powiększenia obszarów uzupełnienia
            # zabudowy wyznaczonych w sposób, o którym mowa w ust. 1, w wyniku rozszerzenia ich granic
            Pp = 0.25 * (Pb - Pu)
            
            # rozbicie multipoligon na poligony
            pojedynczeBufory = processing.run("native:multiparttosingleparts", {
                'INPUT': przyciecie['OUTPUT'],
                'OUTPUT': 'memory:'
            })
        else:
            # rozbicie multipoligon na poligony
            pojedynczeBufory = processing.run("native:multiparttosingleparts", {
                'INPUT': multipoligon['OUTPUT'],
                'OUTPUT': 'memory:'
            })
        
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        pathQML = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/QML/ObszarUzupelnieniaZabudowy.qml")
        
        newFields = QgsFields()
        newFields.append(QgsField('przestrzenNazw', QVariant.String, '', 255))
        newFields.append(QgsField('lokalnyId', QVariant.String, '', 255))
        newFields.append(QgsField('wersjaId', QVariant.String, '', 255))
        newFields.append(QgsField('nazwa', QVariant.String, '', 500))
        newFields.append(QgsField('oznaczenie', QVariant.String, '', 500))
        newFields.append(QgsField('symbol', QVariant.String, '', 500))
        newFields.append(QgsField('charakterUstalenia', QVariant.String, '', 255))
        newFields.append(QgsField('obowiazujeOd', QVariant.Date, ''))
        newFields.append(QgsField('obowiazujeDo', QVariant.Date, ''))
        newFields.append(QgsField('status', QVariant.String, '', 255))
        newFields.append(QgsField('poczatekWersjiObiektu', QVariant.DateTime, ''))
        newFields.append(QgsField('koniecWersjiObiektu', QVariant.DateTime, ''))
        newFields.append(QgsField('edycja', QVariant.Bool, ''))
        
        layers = QgsProject.instance().mapLayers()
        i = 0
        nazwyWarstw = []
        for l in layers.values():
            if l.name().startswith('ObszarUzupelnieniaZabudowy'):
                nazwyWarstw.append(l.name())
        for n in range(100):
            if n == 0:
                layerName = 'ObszarUzupelnieniaZabudowy'
            else:
                layerName = 'ObszarUzupelnieniaZabudowy' + "_" + str(n)
            if not layerName in nazwyWarstw and not os.path.exists(pathlib.Path(str(defaultPath + '/' + layerName + '.gpkg'))):
                i = n
                break
        
        if i > 0:
            layerName = 'ObszarUzupelnieniaZabudowy_' + str(i)
        
        layer = pojedynczeBufory['OUTPUT']
        layer.startEditing()
        
        provider = layer.dataProvider()
        fields = provider.fields()
        provider.deleteAttributes(list(range(len(fields))))
        provider.addAttributes(newFields)
        
        layer.commitChanges()
        
        if layer.featureCount() > 0:
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = 'GPKG'
            options.layerName = layerName
            options.fileEncoding = 'UTF-8'
            options.destCRS = QgsCoordinateReferenceSystem('EPSG:' + epsg)
            
            error =  QgsVectorFileWriter.writeAsVectorFormatV3(layer, defaultPath + "/" + layerName, QgsCoordinateTransformContext(), options)
            
            # Sprawdzenie wyniku zapisu
            if error[0] == QgsVectorFileWriter.NoError:
                output_path = str(pathlib.Path(str(defaultPath + '/' + layerName + '.gpkg')))
                gkpg = QgsVectorLayer(output_path, layerName, 'ogr')
                gkpg.startEditing()
                nrOUZ = 0
                dataTime = QDateTime.currentDateTimeUtc()
                for ouz in gkpg.getFeatures():
                    nrOUZ += 1
                    ouz.setAttribute(1,przestrzenNazw)
                    ouz.setAttribute(2,idLokalnyAPP.replace("-","") + "-" + str(nrOUZ) + "OUZ")
                    ouz.setAttribute(3,dataTime.toString("yyyyMMddTHHmmss"))
                    ouz.setAttribute(4,'Obszar uzupełnienia zabudowy')
                    ouz.setAttribute(5,str(nrOUZ)+"OUZ")
                    ouz.setAttribute(6,'OUZ')
                    ouz.setAttribute(7,'ogólnie wiążące')
                    ouz.setAttribute(8,dataTime)
                    ouz.setAttribute(10,'w opracowaniu')
                    ouz.setAttribute(11,dataTime)
                    ouz.setAttribute(13,True)
                    ouz.setGeometry(ouz.geometry().snappedToGrid(0.01,0.01))
                    
                    if warstwaZPOG.featureCount() > 0:
                        for pog in warstwaZPOG.getFeatures():
                            ouz.setAttribute(8,pog['OBOWIAZUJEOD'])
                            ouz.setAttribute(10,pog['STATUS'])
                    
                    gkpg.updateFeature(ouz)
                    gkpg.commitChanges(False)
                
                gkpg.loadNamedStyle(str(pathQML))
                
                editFormConfig = gkpg.editFormConfig()
                pathUI = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/ObszarUzupelnieniaZabudowy.ui")
                editFormConfig.setUiForm(str(pathUI))
                pathPy = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/ObszarUzupelnieniaZabudowy.py")
                editFormConfig.setInitFilePath(str(pathPy))
                editFormConfig.setInitFunction("my_form_open")
                gkpg.setEditFormConfig(editFormConfig)
                
                # Zapis OUZ do GML
                AppModule.saveLayerToGML_OUZ(self, gkpg)
                
                # Zapis budynków do GML
                target_path = os.path.join(defaultPathDokumentacja, "Budynki.gml")
                if warstwaZBudynkami.dataProvider().storageType() == 'GML':
                    warstwaZBudynkamiPath = str(warstwaZBudynkami.dataProvider().dataSourceUri()).split("|")[0]
                    try:
                        shutil.copy2(warstwaZBudynkamiPath, target_path)
                    except:
                        pass
                else:
                    try:
                        kolDoUsuniecia = []
                        for field in warstwaZBudynkami.fields():
                            if field.type() == QVariant.String and field.length() > 254:
                                for f in warstwaZBudynkami.getFeatures():
                                    try:
                                        max_length = len(f[field.name()])
                                    except:
                                        kolDoUsuniecia.append(field.name())
                                        break
                                    if max_length > 255:
                                        kolDoUsuniecia.append(field.name())
                                        break
                        if kolDoUsuniecia != None and len(kolDoUsuniecia) > 0:
                            warstwaZBudynkamiBezKolumny = processing.run("native:deletecolumn", {
                                'COLUMN': kolDoUsuniecia,
                                'INPUT': warstwaZBudynkami,
                                'OUTPUT': 'memory:'
                            })
                            warstwaWynikowa = warstwaZBudynkamiBezKolumny['OUTPUT']
                        else:
                            warstwaWynikowa = warstwaZBudynkami
                        wynik = processing.run("native:savefeatures", {
                            'DATASOURCE_OPTIONS': '',
                            'INPUT': warstwaWynikowa,
                            'LAYER_NAME': 'Budynki',
                            'LAYER_OPTIONS': '',
                            'OUTPUT': target_path
                        })
                        
                        defaultPathDanePomocnicze = defaultPath + "/Dane pomocnicze/"
                        if not os.path.exists(defaultPathDanePomocnicze):
                            os.makedirs(defaultPathDanePomocnicze)
                        shutil.move(defaultPathDokumentacja + '/Budynki.xsd', defaultPathDanePomocnicze + '/Budynki.xsd')
                        
                    except Exception as errorMsg:
                        print(errorMsg)
                
                # zapisanie Pp, Pu, Pb do pliku Powierzchnie.xml
                root = ET.Element("Dane")
                komentarz = ET.Comment(f'Podane wartości Pu, Pb, Pp podane są w metrach kwadratowych. Zostały obliczone na elipsoidzie WGS84.')
                root.insert(1, komentarz)
                jpt_element = ET.SubElement(root, "JPT")
                jpt_element.text = str(jpt)
                numerZbioru_element = ET.SubElement(root, "Numer_zbioru")
                numerZbioru_element.text = str(numerZbioru)
                path_element = ET.SubElement(root, "Plik_OUZ")
                path_element.text = os.path.join(defaultPathDokumentacja, "ObszarUzupelnieniaZabudowy-wyjsciowy.gml")
                powierzchnie = ET.SubElement(root, "Powierzchnie")
                informacja_Pu = ET.SubElement(powierzchnie, "Pu")
                informacja_Pb = ET.SubElement(powierzchnie, "Pb")
                informacja_Pp = ET.SubElement(powierzchnie, "Pp")
                informacja_Pu.text = str(round(Pu, 2))
                informacja_Pb.text = str(round(Pb, 2))
                informacja_Pp.text = str(round(Pp, 2))
                tree = ET.ElementTree(root)
                ET.indent(tree, space="    ", level=0)
                tree.write(defaultPathDanePomocnicze + "/Powierzchnie.xml", encoding="utf-8", xml_declaration=True)
                
                QgsProject.instance().addMapLayer(gkpg)
                QgsProject.instance().removeMapLayer(layer)
        
        self.tworzenieOUZDialog.progressBar.setValue(100)
        self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
        
        showPopup("Wyznaczanie OUZ",'Utworzono warstwę OUZ i uzupełniono atrybuty.\nUtworzono w folderze „Dokumentacja”\
plik o nazwie „ObszarUzupelnieniaZabudowy-wyjsciowy.gml” oraz plik o nazwie „Budynki.gml”.\nUtworzono w folderze \
„Dane pomocnicze” plik o nazwie „Budynki.xsd”.')
        
        self.tworzenieOUZDialog.progressBar.reset()
        self.tworzenieOUZDialog.progressBar.setValue(0)