# -*- coding: utf-8 -*-
from . import (TworzenieOUZDialog)
from .. import BaseModule
from ..utils import showPopup

from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5.QtCore import Qt
import os
from qgis.core import *
from PyQt5.QtCore import *
from qgis import processing
import pathlib
from qgis.core import QgsSettings
import datetime


class TworzenieOUZ(BaseModule):

    def __init__(self, iface):
        self.iface = iface
        self.tworzenieOUZ = None
        self.tworzenieOUZDialog = TworzenieOUZDialog()
        self.tworzenieOUZDialog.tworzenie_btn.clicked.connect(self.tworzenieOUZ_btn_clicked)

    """Event handlers"""

    def tworzenieOUZ_btn_clicked(self):
        start = datetime.datetime.now()
        s = QgsSettings()
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
        numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
        jpt = s.value("qgis_app2/settings/jpt", "")
        idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
        epsg = str(s.value("qgis_app2/settings/strefaPL2000",""))
        przestrzenNazw = 'PL.ZIPPZP.' + numerZbioru + '/' + jpt + '-' + rodzajZbioru
        
        try:
            warstwaZBudynkami = self.tworzenieOUZDialog.warstwaBudynki.currentLayer()
            warstwaZPOG = self.tworzenieOUZDialog.warstwaPOG.currentLayer()
            if  warstwaZBudynkami.name() == warstwaZPOG.name():
                showPopup("Tworzenie OUZ","Wybrano tą samą warstwę dla budynków i POG.")
                return
        except:
            showPopup("Tworzenie OUZ","Nie wskazano wymaganych warstw.")
            return
        
        if warstwaZBudynkami.featureCount() < 5:
            showPopup("Tworzenie OUZ","Warstwa z budynkami nie zawiera obiektów.")
            return
        
        self.tworzenieOUZDialog.tworzenie_btn.setEnabled(False)
        self.tworzenieOUZDialog.progressBar.reset()
        self.tworzenieOUZDialog.progressBar.setValue(0)
        
        # bufor wokół budynków z rozpuszczeniem granic
        bufory = processing.run("native:buffer", {
            'INPUT': warstwaZBudynkami,
            'DISTANCE':50,
            'SEGMENTS':10,
            'DISSOLVE': True,
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(10)
        QCoreApplication.processEvents()
        
        # rozbicie multipoligon na poligony
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
            showPopup("Utworzenie OUZ","Brak budynków spełniających kryteria. Tworzenie OUZ zatrzymane.")
            self.tworzenieOUZDialog.progressBar.reset()
            self.tworzenieOUZDialog.progressBar.setValue(0)
            self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
            return
        
        # usunięcie dziur o powierzchni poniżej 5 000 m2
        buforyBezDziur = processing.run("native:deleteholes", {
            'INPUT': pojedynczeBufory['OUTPUT'],
            'MIN_AREA':5000,
            'OUTPUT': 'memory:'
        })
        self.tworzenieOUZDialog.progressBar.setValue(60)
        QCoreApplication.processEvents()
        
        # bufor -40 m
        buforMinus40m = processing.run("native:buffer", {
            'INPUT': buforyBezDziur['OUTPUT'],
            'DISTANCE':-40,
            'SEGMENTS':10,
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
                'OVERLAY':warstwaZPOG,
                'OUTPUT': 'memory:'
            })
            
            if przyciecie['OUTPUT'].featureCount() == 0:
                showPopup("Utworzenie OUZ","Budynki nie leżą w obszarze objętym POG. Tworzenie OUZ zatrzymane.")
                self.tworzenieOUZDialog.progressBar.reset()
                self.tworzenieOUZDialog.progressBar.setValue(0)
                self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
                return
            
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
        newFields.append(QgsField('przestrzenNazw', QVariant.String, '', 30))
        newFields.append(QgsField('lokalnyId', QVariant.String, '', 50))
        newFields.append(QgsField('wersjaId', QVariant.String, '', 15))
        newFields.append(QgsField('nazwa', QVariant.String, '', 255))
        newFields.append(QgsField('oznaczenie', QVariant.String, '', 10))
        newFields.append(QgsField('symbol', QVariant.String, '', 3))
        newFields.append(QgsField('charakterUstalenia', QVariant.String, '', 255))
        newFields.append(QgsField('obowiazujeOd', QVariant.Date, ''))
        newFields.append(QgsField('obowiazujeDo', QVariant.Date, ''))
        newFields.append(QgsField('status', QVariant.String, '', 255))
        newFields.append(QgsField('poczatekWersjiObiektu', QVariant.DateTime, ''))
        newFields.append(QgsField('koniecWersjiObiektu', QVariant.DateTime, ''))
        
        layerName = 'ObszarUzupelnieniaZabudowy'
        layers = QgsProject.instance().mapLayers()
        i = 0
        for layer in layers.values():
            if layer.name().startswith(layerName):
                i += 1

        numerWarstwy = ''
        if i > 0:
            numerWarstwy = '_' + str(i)
        
        layer = pojedynczeBufory['OUTPUT']
        
        layer.startEditing()
        layer.geometryOptions().setGeometryPrecision(0.01)
        
        provider = layer.dataProvider()
        fields = provider.fields()
        provider.deleteAttributes(list(range(len(fields))))
        provider.addAttributes(newFields)
        
        layer.commitChanges()
        
        if layer.featureCount() > 0:
            output_path = str(pathlib.Path(str(defaultPath + '/' + layerName + numerWarstwy + '.gpkg')))
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = 'GPKG'
            options.layerName = layerName + numerWarstwy
            options.fileEncoding = 'UTF-8'
            options.destCRS = QgsCoordinateReferenceSystem('EPSG:' + epsg)
            
            error =  QgsVectorFileWriter.writeAsVectorFormatV3(layer, output_path, QgsCoordinateTransformContext(), options)
            
            # Sprawdzenie wyniku zapisu
            if error[0] == QgsVectorFileWriter.NoError:
                gkpg = QgsVectorLayer(output_path, layerName + numerWarstwy, 'ogr')
                gkpg.startEditing()
                nrOUZ = 0
                dataTime = QDateTime.currentDateTime()
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
                    
                    if warstwaZPOG.featureCount() > 0:
                        for pog in warstwaZPOG.getFeatures():
                            ouz.setAttribute(8,pog['OBOWIAZUJEOD'])
                            ouz.setAttribute(10,pog['STATUS'])
                    
                    gkpg.updateFeature(ouz)
                    gkpg.commitChanges(False)
                
                gkpg.loadNamedStyle(str(pathQML))
                
                editFormConfig = gkpg.editFormConfig()
                pathUI = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".ui")
                editFormConfig.setUiForm(str(pathUI))
                pathPy = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".py")
                editFormConfig.setInitFilePath(str(pathPy))
                editFormConfig.setInitFunction("my_form_open")
                gkpg.setEditFormConfig(editFormConfig)
                
                QgsProject.instance().addMapLayer(gkpg)
        
        self.tworzenieOUZDialog.progressBar.setValue(100)
        self.tworzenieOUZDialog.tworzenie_btn.setEnabled(True)
        
        # ts = datetime.datetime.now() - start
        # print('Tworzenie OUZ zajęło: ', ts.seconds)
        
        showPopup("Utworzenie OUZ","Utworzono warstwę OUZ i uzupełniono atrybuty.")
        self.tworzenieOUZDialog.progressBar.reset()
        self.tworzenieOUZDialog.progressBar.setValue(0)