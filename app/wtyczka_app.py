# -*- coding: utf-8 -*-
from qgis.utils import iface
from . import (PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog, WektorInstrukcjaDialogPOG,
               WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog,
               WektorInstrukcjaDialogSPL, WektorInstrukcjaDialogOUZ, WektorInstrukcjaDialogOZS, WektorInstrukcjaDialogOSD,
               PytanieAppUniewaznienieDialog, FormularzInstrukcjaDialogPOGpoUniewaznieniu, DokumentyFormularzDialogPoUniewaznieniu,
               GenerowanieGMLDialogPoUniewaznieniu)

from .app_utils import isLayerInPoland, czyWarstwaMaWypelnioneObowiazkoweAtrybuty, kontrolaZaleznosciAtrybutow, isJPTinLayer, kontrolaProfiliDodatkowych
from .. import BaseModule, utils, Formularz
from ..utils import showPopup
from ..models import AppTableModel
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
from datetime import datetime
from .. import dictionaries
from qgis.core import QgsSettings
from shutil import copyfile
from osgeo import ogr
from processing.core.Processing import Processing
from PyQt5.QtCore import QSettings, QDateTime, QDate
from ..tworzenieOUZ.dialogs import TworzenieOUZDialog
from PyQt5.QtGui import QColor
from matplotlib import cm
from matplotlib.colors import to_hex
from shapely.wkb import loads
from shapely.geometry import LineString
from datetime import datetime, timezone
import numpy as np
import os
import os.path
import sys
import pathlib
import re
import time
import lxml
import xml.etree.ElementTree as ET  # nosec B405
import ntpath
import copy
import hashlib
import math
import processing



class AppModule(BaseModule):
    metadaneDialog = None
    
    global s, rodzajZbioru, numerZbioru, jpt, idLokalnyAPP, defaultPath, warstwaPOG, checksums, informacjaOgolna
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
    numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
    jpt = s.value("qgis_app2/settings/jpt", "")
    idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
    defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
    QSettings().setValue('/Map/identifyAutoFeatureForm','true')
    warstwaPOG = None
    checksums = set()
    informacjaOgolna = False


    def __init__(self, iface):
        """Inicjalizuje obiekt klasy `AppModule` i konfiguruje jego stan początkowy."""
        Processing.initialize()
        
        self.tableView = None
        self.iface = iface
        self.dataValidator = None  # inicjacja w głównym skrypcie wtyczki
        
        self.saved = False
        self.generated = False
        self.savedxml = False
        
        self.POG_GML_saved = False
        self.SPL_GML_saved = False
        self.OUZ_GML_saved = False
        self.OZS_GML_saved = False
        self.OSD_GML_saved = False
        
    # region okna moduł app
        self.pytanieAppDialog = PytanieAppDialog()
        self.zbiorPrzygotowanieDialog = ZbiorPrzygotowanieDialog()
        self.rasterInstrukcjaDialog = RasterInstrukcjaDialog()
        self.rasterFormularzDialog = RasterFormularzDialog()
        self.wektorInstrukcjaDialog = WektorInstrukcjaDialog()
        self.wektorFormularzDialog = WektorFormularzDialog()
        self.dokumentyFormularzDialog = DokumentyFormularzDialog()
        self.generowanieGMLDialog = GenerowanieGMLDialog()
    
        # dla plnu ogólnego gminy
        self.wektorInstrukcjaDialogPOG = WektorInstrukcjaDialogPOG()
        self.wektorInstrukcjaDialogSPL = WektorInstrukcjaDialogSPL()
        self.wektorInstrukcjaDialogOUZ = WektorInstrukcjaDialogOUZ()
        self.wektorInstrukcjaDialogOZS = WektorInstrukcjaDialogOZS()
        self.wektorInstrukcjaDialogOSD = WektorInstrukcjaDialogOSD()
        
        # dla plnu ogólnego gminy po unieważnieniu
        self.pytanieAppUniewaznienieDialog = PytanieAppUniewaznienieDialog()
        self.formularzInstrukcjaDialogPOGpoUniewaznieniu = FormularzInstrukcjaDialogPOGpoUniewaznieniu()
        self.dokumentyFormularzDialogPoUniewaznieniu = DokumentyFormularzDialogPoUniewaznieniu()
        self.generowanieGMLDialogPoUniewaznieniu = GenerowanieGMLDialogPoUniewaznieniu()
    # endregion
    
    # region pytanieAppDialog
        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)
        self.pytanieAppDialog.load_btn.clicked.connect(self.pytanieAppDialog_load_btn_clicked)
        self.pytanieAppDialog.projekt_qgs_btn.clicked.connect(self.pytanieAppDialog_projekt_qgs_btn_clicked)
    # endregion
    
    # region rasterInstrukcjaDialog
        self.rasterInstrukcjaDialog.next_btn.clicked.connect(self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(self.rasterInstrukcjaDialog_prev_btn_clicked)
    # endregion
    
    # region rasterFormularzDialog
        self.rasterFormularzDialog.prev_btn.clicked.connect(self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(self.checkSaveForms)
        self.rasterFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)
        self.prepareIdIPP(formularz=self.rasterFormularzDialog)
        self.rasterFormularzDialog.setDefaultValues()
        self.rasterFormularzDialog.skip_btn.clicked.connect(self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.rasterFormularzDialog.clear_btn.clicked.connect(self.rasterFormularzDialog_clear_btn_clicked)
        self.rasterFormularzDialog.getValues_btn.clicked.connect(self.getFormValues)
    # endregion
    
    # region wektorInstrukcjaDialog
        self.wektorInstrukcjaDialog.next_btn.clicked.connect(
            self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialog.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialog.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
        self.wektorInstrukcjaDialog.layers_comboBox.setShowCrs(True)
    # endregion
    
    # region wektorFormularzDialog
        self.wektorFormularzDialog.prev_btn.clicked.connect(
            self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(
            self.checkSaveForms)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        self.wektorFormularzDialog.clear_btn.clicked.connect(
            self.wektorFormularzDialog_clear_btn_clicked)
        self.wektorFormularzDialog.getValues_btn.clicked.connect(
            self.getFormValues)
        self.prepareIdIPP(formularz=self.wektorFormularzDialog)
        self.wektorFormularzDialog.setDefaultValues()
    # endregion
    
    # region dokumentyFormularzDialog
        self.dokumentyFormularzDialog.prev_btn.clicked.connect(
            self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(
            self.checkSaveForms)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        self.dokumentyFormularzDialog.clear_btn.clicked.connect(
            self.dokumentyFormularzDialog_clear_btn_clicked)
        self.dokumentyFormularzDialog.getValues_btn.clicked.connect(
            self.getFormValues)
        self.dokumentyFormularzDialog.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.prepareIdIPP(formularz=self.dokumentyFormularzDialog)
        self.dokumentyFormularzDialog.setDefaultValues()
    # endregion
    
    # region generowanieGMLDialog
        self.generowanieGMLDialog.prev_btn.clicked.connect(
            self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.generate_btn.clicked.connect(lambda:
            self.generateAPP(self.generowanieGMLDialog))
        self.generowanieGMLDialog.addElement_btn.clicked.connect(lambda:
            self.addTableContentGML(1, self.generowanieGMLDialog))
        if rodzajZbioru == 'POG':
            self.generowanieGMLDialog.addElement_btn2.clicked.connect(lambda: self.addTableContentGML(2, self.generowanieGMLDialog))
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(lambda: self.deleteTableContentGML(1, self.generowanieGMLDialog))
        if rodzajZbioru == 'POG':
            self.generowanieGMLDialog.deleteElement_btn2.clicked.connect(lambda: self.deleteTableContentGML(2, self.generowanieGMLDialog))
    
        # rozszerzanie kolumn
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        for i in range(header_gml.count()):
            header_gml.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        if rodzajZbioru == 'POG':
            header_gml2 = self.generowanieGMLDialog.filesTable_widget2.horizontalHeader()
            for i in range(header_gml2.count()):
                header_gml2.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
    # endregion
    
    # region zbiorPrzygotowanieDialog
        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(
            self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(
            self.checkSaveSet)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(
            self.validateAndGenerate_btn_clicked)
        self.zbiorPrzygotowanieDialog.addElement_btn.clicked.connect(
            self.addTableContentSet)
        self.zbiorPrzygotowanieDialog.deleteElement_btn.clicked.connect(
            self.deleteTableContentSet)
        header_zbior = self.zbiorPrzygotowanieDialog.appTable_widget.horizontalHeader()
        for i in range(header_zbior.count()):
            header_zbior.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
    
    # endregion
    
    # dla plnu ogólnego gminy ---------------------------------------------------------
    
    # region wektorInstrukcjaDialogPOG
        self.wektorInstrukcjaDialogPOG.next_btn.clicked.connect(
            self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialogPOG.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialogPOG.loadLayerEdit.clicked.connect(lambda:
            self.loadFromGMLorGPKG(False))
        self.wektorInstrukcjaDialogPOG.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogPOG.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogPOG.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogPOG.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    # region wektorInstrukcjaDialogSPL
        self.wektorInstrukcjaDialogSPL.next_btn.clicked.connect(
            self.wektorInstrukcjaDialogSPL_next_btn_clicked)
        self.wektorInstrukcjaDialogSPL.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialogSPL.loadLayerEdit.clicked.connect(lambda:
            self.loadFromGMLorGPKG(False))
        self.wektorInstrukcjaDialogSPL.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogSPL.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogSPL.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogSPL.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    # region wektorInstrukcjaDialogOUZ
        self.wektorInstrukcjaDialogOUZ.next_btn.clicked.connect(
            self.wektorInstrukcjaDialogOUZ_next_btn_clicked)
        self.wektorInstrukcjaDialogOUZ.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialogOUZ.loadLayerEdit.clicked.connect(lambda:
            self.loadFromGMLorGPKG(False))
        self.wektorInstrukcjaDialogOUZ.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogOUZ.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogOUZ.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogOUZ.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    # region wektorInstrukcjaDialogOZS
        self.wektorInstrukcjaDialogOZS.next_btn.clicked.connect(
            self.wektorInstrukcjaDialogOZS_next_btn_clicked)
        self.wektorInstrukcjaDialogOZS.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialogOZS.loadLayerEdit.clicked.connect(lambda:
            self.loadFromGMLorGPKG(False))
        self.wektorInstrukcjaDialogOZS.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogOZS.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogOZS.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogSPL.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    # region wektorInstrukcjaDialogOSD
        self.wektorInstrukcjaDialogOSD.next_btn.clicked.connect(
            self.wektorInstrukcjaDialogOSD_next_btn_clicked)
        self.wektorInstrukcjaDialogOSD.prev_btn.clicked.connect(
            self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialogOSD.loadLayerEdit.clicked.connect(lambda:
            self.loadFromGMLorGPKG(False))
        self.wektorInstrukcjaDialogOSD.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogOSD.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogOSD.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogOSD.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    # region pytanieAppUniewaznienieDialog
        self.pytanieAppUniewaznienieDialog.load_btn.clicked.connect(self.pytanieAppDialog_load_btn_clicked)
        self.pytanieAppUniewaznienieDialog.projekt_qgs_btn.clicked.connect(self.pytanieAppDialog_projekt_qgs_btn_clicked)
        self.pytanieAppUniewaznienieDialog.skip_btn.clicked.connect(
            self.pytanieAppUniewaznienieDialog_skip_btn_clicked)
        self.pytanieAppUniewaznienieDialog.next_btn.clicked.connect(
            self.pytanieAppUniewaznienieDialog_next_btn_clicked)
    # endregion
    
    # region formularzInstrukcjaDialogPOGpoUniewaznieniu
        self.formularzInstrukcjaDialogPOGpoUniewaznieniu.prev_btn.clicked.connect(
            self.formularzInstrukcjaDialogPOGpoUniewaznieniu_prev_btn_clicked)
        self.formularzInstrukcjaDialogPOGpoUniewaznieniu.next_btn.clicked.connect(
            self.formularzInstrukcjaDialogPOGpoUniewaznieniu_next_btn_clicked)
        self.formularzInstrukcjaDialogPOGpoUniewaznieniu.skip_btn.clicked.connect(
            self.formularzInstrukcjaDialogPOGpoUniewaznieniu_skip_btn_clicked)
    # endregion
    
    # region dokumentyFormularzDialogPoUniewaznieniu
        self.dokumentyFormularzDialogPoUniewaznieniu.prev_btn.clicked.connect(
            self.dokumentyFormularzDialogPoUniewaznieniu_prev_btn_clicked)
        self.dokumentyFormularzDialogPoUniewaznieniu.next_btn.clicked.connect(
            self.checkSaveForms)
        self.dokumentyFormularzDialogPoUniewaznieniu.saveForm_btn.clicked.connect(
            self.showPopupSaveForm)
        self.dokumentyFormularzDialogPoUniewaznieniu.clear_btn.clicked.connect(
            self.dokumentyFormularzDialogPoUniewaznieniu_clear_btn_clicked)
        self.dokumentyFormularzDialogPoUniewaznieniu.getValues_btn.clicked.connect(
            self.getFormValues)
        self.dokumentyFormularzDialogPoUniewaznieniu.skip_btn.clicked.connect(
            self.dokumentyFormularzDialogPoUniewaznieniu_skip_btn_clicked)
        self.prepareIdIPP(formularz=self.dokumentyFormularzDialogPoUniewaznieniu)
        self.dokumentyFormularzDialogPoUniewaznieniu.setDefaultValues()
    # endregion
    
    # region generowanieGMLDialogPoUniewaznieniu
        self.generowanieGMLDialogPoUniewaznieniu.prev_btn.clicked.connect(
            self.generowanieGMLDialogPoUniewaznieniu_prev_btn_clicked)
        self.generowanieGMLDialogPoUniewaznieniu.generate_btn.clicked.connect(lambda:
            self.generateAPP(self.generowanieGMLDialogPoUniewaznieniu))
        self.generowanieGMLDialogPoUniewaznieniu.addElement_btn.clicked.connect(lambda:
            self.addTableContentGML(1, self.generowanieGMLDialogPoUniewaznieniu))
        self.generowanieGMLDialogPoUniewaznieniu.deleteElement_btn.clicked.connect(lambda: self.deleteTableContentGML(1, self.generowanieGMLDialogPoUniewaznieniu))
        # rozszerzanie kolumn
        header_gml = self.generowanieGMLDialogPoUniewaznieniu.filesTable_widget.horizontalHeader()
        for i in range(header_gml.count()):
            header_gml.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            
    # endregion
    
    """Event handlers"""

    # region pytanieAppDialog

    def pytanieAppDialog_app_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppDialog_app`."""
        if defaultPath == '' or rodzajZbioru == '' or numerZbioru == '' or jpt == '':
            utils.showPopup("Ustawienia wtyczki APP","Proszę uzupełnić ustawienia wtyczki APP.")
        else:
            if rodzajZbioru == 'POG':
                self.openNewDialog(self.wektorInstrukcjaDialogPOG)
                self.update_layer_list(self.wektorInstrukcjaDialogPOG)
            else:
                self.openNewDialog(self.rasterInstrukcjaDialog)
            self.listaOkienek.append(self.pytanieAppDialog)


    def pytanieAppDialog_zbior_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppDialog_zbior`."""
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)


    def pytanieAppDialog_load_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppDialog_load`."""
        self.loadFromGMLorGPKG(False)


    def pytanieAppDialog_projekt_qgs_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppDialog_projekt_qgs`."""
        self.wczytanieProjektuQGIS()

    # endregion

    # region rasterInstrukcjaDialog
    def rasterInstrukcjaDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `rasterInstrukcjaDialog_next`."""
        self.openNewDialog(self.rasterFormularzDialog)
        self.listaOkienek.append(self.rasterInstrukcjaDialog)


    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `rasterInstrukcjaDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())

    # endregion

    # region rasterFormularzDialog
    def rasterFormularzDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `rasterFormularzDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())


    def rasterFormularzDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `rasterFormularzDialog_next`."""
        self.openNewDialog(self.wektorInstrukcjaDialog)
        self.listaOkienek.append(self.rasterFormularzDialog)


    def rasterFormularzDialog_clear_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `rasterFormularzDialog_clear`."""
        self.rasterFormularzDialog.clearForm(self.rasterFormularzDialog.form_scrollArea)
        self.rasterFormularzDialog.setDefaultValues()

    # endregion

    # region wektorInstrukcjaDialog

    def wektorInstrukcjaDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialog_next`."""
        if rodzajZbioru == 'POG':
            self.obrysLayer = self.wektorInstrukcjaDialogPOG.layers_comboBox.currentLayer()
        else:
            self.obrysLayer = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
        
        if not self.kontrolaWarstwy(self.obrysLayer):
            return False
        elif rodzajZbioru == 'POG' and self.POG_GML_saved == False:
            showPopup("Błąd warstwy obrysu",
                      "Warstwa nie została zapisana do GML.")
        else:   # wszystko OK z warstwą
        
            if rodzajZbioru == 'POG':
                self.openNewDialog(self.wektorInstrukcjaDialogSPL)
                self.update_layer_list(self.wektorInstrukcjaDialogSPL)
            else:
                self.openNewDialog(self.wektorFormularzDialog)
            self.obrysLayer = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
            
            global warstwaPOG
            warstwaPOG = self.obrysLayer
            
            formElements = self.wektorFormularzDialog.formElements
            
            if rodzajZbioru != 'POG':
                obrys = next(self.obrysLayer.getFeatures())
                attrs = obrys.attributes()
                fields = self.obrysLayer.fields()
                field_names = []
                
                for field in fields:
                    field_names.append(field.name())
                
                for formElement in formElements:
                    if formElement.name in field_names:
                        idx = field_names.index(formElement.name)
                        value = attrs[idx]
                        formItem = formElement.refObject
                        try:
                            if isinstance(formItem, QLineEdit):
                                formItem.setText(value)
                            elif isinstance(formItem, QDateTimeEdit):
                                if formElement.type == 'date':
                                    formItem.setDate(value)
                                elif formElement.type == 'dateTime':
                                    formItem.setDateTime(value)
                            elif isinstance(formItem, QCheckBox):
                                formItem.setChecked(value)
                            elif isinstance(formItem, QComboBox):
                                utils.setValueToWidget(formElement, str(value))
                        except Exception as e:
                            QgsMessageLog.logMessage(f'Błąd: {str(e)}','APP2')
                    for inner in formElement.innerFormElements:
                        if inner.name in field_names:
                            idx = field_names.index(inner.name)
                            value = attrs[idx]
                            formItem = inner.refObject
                            try:
                                if isinstance(formItem, QLineEdit):
                                    formItem.setText(value)
                                elif isinstance(formItem, QDateTimeEdit):
                                    if inner.type == 'date':
                                        formItem.setDate(value)
                                    elif inner.type == 'dateTime':
                                        formItem.setDateTime(value)
                                elif isinstance(formItem, QCheckBox):
                                    formItem.setChecked(value)
                                elif isinstance(formItem, QComboBox):
                                    utils.setValueToWidget(inner, str(value))
                            except Exception as e:
                                QgsMessageLog.logMessage(f'Błąd: {str(e)}','APP2')
            if rodzajZbioru == 'POG':
                self.listaOkienek.append(self.wektorInstrukcjaDialogPOG)
            else:
                self.listaOkienek.append(self.wektorInstrukcjaDialog)


    def wektorInstrukcjaDialogSPL_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialogSPL_next`."""
        self.obrysLayer = self.wektorInstrukcjaDialogSPL.layers_comboBox.currentLayer()
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z SPL.")
            return
        
        # kontrola zdublowanych oznaczeń
        if self.kontrolaGeometriiWarstwy(self.obrysLayer):
            if rodzajZbioru == 'POG' and self.SPL_GML_saved == False:
                showPopup("Błąd warstwy obrysu",
                          "Warstwa nie została zapisana do GML.")
            else:
                self.openNewDialog(self.wektorInstrukcjaDialogOUZ)
                self.update_layer_list(self.wektorInstrukcjaDialogOUZ)
                self.listaOkienek.append(self.wektorInstrukcjaDialogSPL)


    def wektorInstrukcjaDialogOUZ_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialogOUZ_next`."""
        self.obrysLayer = self.wektorInstrukcjaDialogOUZ.layers_comboBox.currentLayer()
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z ObszarUzupelnieniaZabudowy.")
            return
        
        if self.kontrolaGeometriiWarstwy(self.obrysLayer):
            if rodzajZbioru == 'POG' and self.OUZ_GML_saved == False:
                showPopup("Błąd warstwy obrysu",
                          "Warstwa nie została zapisana do GML.")
            else:
                self.openNewDialog(self.wektorInstrukcjaDialogOZS)
                self.update_layer_list(self.wektorInstrukcjaDialogOZS)
                self.obrysLayer = self.wektorInstrukcjaDialogOUZ.layers_comboBox.currentLayer()
                self.listaOkienek.append(self.wektorInstrukcjaDialogOUZ)


    def wektorInstrukcjaDialogOZS_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialogOZS_next`."""
        self.obrysLayer = self.wektorInstrukcjaDialogOZS.layers_comboBox.currentLayer()
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z ObszarZabudowySrodmiejskiej.")
            return
        
        if self.kontrolaGeometriiWarstwy(self.obrysLayer):
            if rodzajZbioru == 'POG' and self.OZS_GML_saved == False:
                showPopup("Błąd warstwy obrysu",
                          "Warstwa nie została zapisana do GML.")
            else:
                self.openNewDialog(self.wektorInstrukcjaDialogOSD)
                self.update_layer_list(self.wektorInstrukcjaDialogOSD)
                self.obrysLayer = self.wektorInstrukcjaDialogOUZ.layers_comboBox.currentLayer()
                self.listaOkienek.append(self.wektorInstrukcjaDialogOZS)


    def wektorInstrukcjaDialogOSD_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialogOSD_next`."""
        self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z ObszarStandardowDostepnosciInfrastrukturySpolecznej.")
            return
        
        if self.kontrolaGeometriiWarstwy(self.obrysLayer):
            if rodzajZbioru == 'POG' and self.OSD_GML_saved == False:
                showPopup("Błąd warstwy obrysu", "Warstwa nie została zapisana do GML.")
            else:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
                self.listaOkienek.append(self.wektorInstrukcjaDialogOSD)


    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())
        if self.activeDlg == self.wektorInstrukcjaDialogPOG:
            self.update_layer_list(self.wektorInstrukcjaDialogPOG)
        elif self.activeDlg == self.wektorInstrukcjaDialogSPL:
            self.update_layer_list(self.wektorInstrukcjaDialogSPL)
        elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
            self.update_layer_list(self.wektorInstrukcjaDialogOUZ)
        elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
            self.update_layer_list(self.wektorInstrukcjaDialogOZS)


    def wektorInstrukcjaDialog_skip_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorInstrukcjaDialog_skip`."""
        if rodzajZbioru == 'POG':
            if self.activeDlg == self.wektorInstrukcjaDialogPOG:
                self.openNewDialog(self.wektorInstrukcjaDialogSPL)
                self.update_layer_list(self.wektorInstrukcjaDialogSPL)
                self.listaOkienek.append(self.wektorInstrukcjaDialogPOG)
            elif self.activeDlg == self.wektorInstrukcjaDialogSPL:
                self.openNewDialog(self.wektorInstrukcjaDialogOUZ)
                self.update_layer_list(self.wektorInstrukcjaDialogOUZ)
                self.listaOkienek.append(self.wektorInstrukcjaDialogSPL)
            elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
                self.openNewDialog(self.wektorInstrukcjaDialogOZS)
                self.update_layer_list(self.wektorInstrukcjaDialogOZS)
                self.listaOkienek.append(self.wektorInstrukcjaDialogOUZ)
            elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
                self.openNewDialog(self.wektorInstrukcjaDialogOSD)
                self.update_layer_list(self.wektorInstrukcjaDialogOSD)
                self.listaOkienek.append(self.wektorInstrukcjaDialogOZS)
            elif self.activeDlg == self.wektorInstrukcjaDialogOSD:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorInstrukcjaDialogOSD)
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
            
            global warstwaPOG
            warstwaPOG = self.wektorInstrukcjaDialogPOG.layers_comboBox.currentLayer()
        else:
            if self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
            elif self.activeDlg == self.rasterFormularzDialog:
                self.openNewDialog(self.wektorInstrukcjaDialog)
                self.listaOkienek.append(self.rasterFormularzDialog)
            else:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorInstrukcjaDialog)

    # endregion

    # region wektorFormularzDialog
    def wektorFormularzDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorFormularzDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())


    def wektorFormularzDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorFormularzDialog_next`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.generowanieGMLDialog)
        else:
            self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)


    def wektorFormularzDialog_clear_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `wektorFormularzDialog_clear`."""
        self.wektorFormularzDialog.clearForm(
            self.wektorFormularzDialog.form_scrollArea)
        self.wektorFormularzDialog.setDefaultValues()

    # endregion

    # region dokumentyFormularzDialog
    def dokumentyFormularzDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())


    def dokumentyFormularzDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialog_next`."""
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)


    def dokumentyFormularzDialog_clear_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialog_clear`."""
        self.dokumentyFormularzDialog.clearForm(self.dokumentyFormularzDialog.form_scrollArea)
        self.dokumentyFormularzDialog.setDefaultValues()

    # endregion

    # region generowanieGMLDialog
    def generowanieGMLDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `generowanieGMLDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())


    def generowanieGMLDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `generowanieGMLDialog_next`."""
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.generowanieGMLDialog)


    def makeAnotherApp_radioBtn_toggled(self, setYes):
        """Realizuje operację `makeAnotherApp_radioBtn_toggled` w bieżącym module."""
        if setYes:  # tak - utworzenie kolejnego APP
            self.generowanieGMLDialog.next_btn.setText("Dalej")
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(False)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(False)
        else:  # nie
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(True)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(True)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(True)
            if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
                self.generowanieGMLDialog.next_btn.setText("Zakończ")


    def makeSet_radioBtn_toggled(self, setYes):
        """Realizuje operację `makeSet_radioBtn_toggled` w bieżącym module."""
        if setYes:  # finalne tworzenie zbioru app
            self.generowanieGMLDialog.next_btn.setText("Dalej")
        else:  # zakończ działanie wtyczki
            self.generowanieGMLDialog.next_btn.setText("Zakończ")

    # endregion

    # region zbiorPrzygotowanieDialog
    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `zbiorPrzygotowanieDialog_prev`."""
        self.openNewDialog(self.listaOkienek.pop())


    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `zbiorPrzygotowanieDialog_next`."""
        self.openNewDialog(self.metadaneDialog)
        self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
        self.metadaneDialog.prev_btn.setEnabled(True)


    def validateAndGenerate_btn_clicked(self, fileName=None):
        """Obsługuje kliknięcie przycisku związanego z operacją `validateAndGenerate`."""
        files = []
        gmlPaths = []
        appTable_widget = utils.getWidgetByName(
            layout=self.zbiorPrzygotowanieDialog,
            searchObjectType=QTableWidget,
            name="appTable_widget")
        
        xmlIip_list = []
        for rowId in range(appTable_widget.rowCount()):
            xmlIpp = appTable_widget.item(rowId, 0).text()
            if xmlIpp not in xmlIip_list:
                xmlIip_list.append(xmlIpp)
            xmlPath = os.path.join(appTable_widget.item(rowId, 1).toolTip())
            xmlDate = appTable_widget.item(rowId, 2).text()
            files.append(AppTableModel(rowId, xmlPath, xmlDate))
            gmlPaths.append(xmlPath)
        
        if not utils.validatePrzestrzenNazwAppSet(files=files):
            utils.showPopup('Błąd przestrzeni nazw','Obiekty posiadają różne przestrzenie nazw w idIIP.')
        elif len(xmlIip_list) != appTable_widget.rowCount():
            utils.showPopup('Błąd liczności obiektów',
                            'W zbiorze mogą występować tylko obiekty AktPlanowaniaPrzestrzennego o unikalnym idIIP.')
        else:
            # Sprawdzenie poprawności każdego z plików składowych
            for file in files:
                file.path = self.changeNamespaceInFile(file.path)
                # nie zwalidowano poprawnie
                if not self.validateFile(path=file.path, validator=self.dataValidator, type='app', muted=True):
                    return False
            
            # Sprawdzenie zależności geometrycznych miedzy GMLami
            result = utils.checkZbiorGeometryValidityBeforeCreation(gmlPaths)
            if not result[0]:  # niepoprawne zależności geometryczne
                trescBledu = result[1]
                self.iface.messageBar().pushCritical("Błąd geometrii zbioru:", trescBledu)
                return False
            
            defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
            
            if fileName:
                self.fn = fileName
            else:
                self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="pliki GML (*.gml)")[0]
            if self.fn:
                xml_string = utils.mergeAppToCollection(files, set={})
                if xml_string != '':
                    myfile = open(self.fn, "w", encoding='utf-8')
                    myfile.write(xml_string)
                    self.iface.messageBar().pushSuccess("Generowanie zbioru:","Pomyślnie wygenerowano zbiór APP.")
                    utils.showPopup("Wygeneruj plik GML dla zbioru APP","Poprawnie wygenerowano plik GML.")
                    self.generated = True
        return True


    def changeNamespaceInFile(self, file_path):
        """Zmienia przestrzeń nazw APP 1.0 lub 2.0 na APP 3.0."""
        
        with open(file_path, 'rb') as file:
            content = file.read()
            
        old_namespaces = (
            b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0',
            b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0',
        )
        
        new_namespace = b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0'
        
        updated_content = content
        
        for old_namespace in old_namespaces:
            updated_content = updated_content.replace(old_namespace, new_namespace)
            
        # Jeżeli zawartość została zmieniona, zapisz plik tymczasowy.
        if updated_content != content:
            dir_name, base_name = os.path.split(file_path)
            new_file_path = os.path.join(dir_name, f"tmp_{base_name}")
            
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
                
            return new_file_path
            
        # Plik korzysta już z APP 3.0 albo nie zawiera obsługiwanej przestrzeni.
        return file_path

    # endregion

    # region po unieważnieniu
    def pytanieAppUniewaznienieDialog_next_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppUniewaznienieDialog_next`."""
        if rodzajZbioru == 'POG' and self.checkRequiredLayers():
            self.openNewDialog(self.formularzInstrukcjaDialogPOGpoUniewaznieniu)

    def pytanieAppUniewaznienieDialog_skip_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `pytanieAppUniewaznienieDialog_skip`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.formularzInstrukcjaDialogPOGpoUniewaznieniu)

    def formularzInstrukcjaDialogPOGpoUniewaznieniu_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `formularzInstrukcjaDialogPOGpoUniewaznieniu_prev`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.pytanieAppUniewaznienieDialog)

    def formularzInstrukcjaDialogPOGpoUniewaznieniu_next_btn_clicked(self):
        
        """Obsługuje kliknięcie przycisku związanego z operacją `formularzInstrukcjaDialogPOGpoUniewaznieniu_next`."""
        dialog = self.formularzInstrukcjaDialogPOGpoUniewaznieniu
        przycisk = dialog.next_btn
    
        if rodzajZbioru != "POG":
            return
    
        # Zablokowanie przycisku zapobiega ponownemu uruchomieniu operacji.
        przycisk.setEnabled(False)
    
        # Informacja wizualna, że wtyczka wykonuje operację.
        QApplication.setOverrideCursor(Qt.WaitCursor)
    
        # Wymuszenie natychmiastowego odświeżenia GUI.
        QApplication.processEvents()
        
        try:
            oznaczenia = (self.formularzInstrukcjaDialogPOGpoUniewaznieniu.oznaczenia.text().strip())
            warstwa = (self.formularzInstrukcjaDialogPOGpoUniewaznieniu.layers_comboBox.currentLayer())
            
            if rodzajZbioru != "POG":
                return
            
            # Wariant 1: użytkownik wpisał oznaczenia.
            if oznaczenia:
                if not self.checkLayersAndOznaczenia(oznaczenia):
                    return
                
                obowiazuje_od = self.pobierzDateObowiazujeOdZOkna()
                
                if obowiazuje_od is None:
                    return
                
                if self.removeObjectsByOznaczenia(oznaczenia, obowiazuje_od):
                    self.openNewDialog(self.dokumentyFormularzDialogPoUniewaznieniu)
                    
                return
            
            # Wariant 2: użytkownik wybrał warstwę w layers_comboBox.
            if warstwa is not None:
                obowiazuje_od = self.pobierzDateObowiazujeOdZOkna()
                
                if obowiazuje_od is None:
                    return
                    
                if self.removeObjectsByLayer(obowiazuje_od):
                    self.openNewDialog(self.dokumentyFormularzDialogPoUniewaznieniu)
        finally:
            # Kursor musi zostać przywrócony niezależnie od:
            # - wyniku operacji,
            # - wcześniejszego return,
            # - wystąpienia wyjątku.
            QApplication.restoreOverrideCursor()
            
            # Przywrócenie przycisku.
            przycisk.setEnabled(True)
            
            QApplication.processEvents()

    def formularzInstrukcjaDialogPOGpoUniewaznieniu_skip_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `formularzInstrukcjaDialogPOGpoUniewaznieniu_skip`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.dokumentyFormularzDialogPoUniewaznieniu)


    def dokumentyFormularzDialogPoUniewaznieniu_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialogPoUniewaznieniu_prev`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.formularzInstrukcjaDialogPOGpoUniewaznieniu)


    def dokumentyFormularzDialogPoUniewaznieniu_clear_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialogPoUniewaznieniu_clear`."""
        self.dokumentyFormularzDialogPoUniewaznieniu.clearForm(self.dokumentyFormularzDialogPoUniewaznieniu.form_scrollArea)
        self.dokumentyFormularzDialogPoUniewaznieniu.setDefaultValues()


    def dokumentyFormularzDialogPoUniewaznieniu_skip_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `dokumentyFormularzDialogPoUniewaznieniu_skip`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.generowanieGMLDialogPoUniewaznieniu)


    def generowanieGMLDialogPoUniewaznieniu_prev_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `generowanieGMLDialogPoUniewaznieniu_prev`."""
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.dokumentyFormularzDialogPoUniewaznieniu)

    """Helper methods"""


    def getFormValues(self, fileName=None):
        """Pobiera dane wymagane przez operację `getFormValues`."""
        if fileName:
            plik = fileName
        else:
            plik = str(QFileDialog.getOpenFileName(filter="pliki XML/GML (*.xml *.gml)")[0])
        if plik:
            formElements = self.activeDlg.formElements
            self.activeDlg.clearForm(self.activeDlg.form_scrollArea)
            self.activeDlg.setDefaultValues()
            utils.loadItemsToForm(plik, formElements, self.activeDlg, rodzajZbioru)


    def getDocTypesFromGML(self, file):
        """Pobiera dane wymagane przez operację `getDocTypesFromGML`."""
        docNames = {
            'AktPlanowaniaPrzestrzennego':
                'Akt planowania przestrzennego',
            'RysunekAktuPlanowaniaPrzestrzennego':
                'Rysunek APP',
            'DokumentFormalny':
                'Dokument formalny',
            'StrefaPlanistyczna':
                'Strefa planistyczna',
            'ObszarUzupelnieniaZabudowy':
                'Obszar uzupełnienia zabudowy',
            'ObszarZabudowySrodmiejskiej':
                'Obszar zabudowy śródmiejskiej',
            'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                'Obszar standardów dostępności infrastruktury społecznej'
        }
        
        foundDocTypes = set()
        
        try:
            tree = ET.parse(file)  # nosec B314
            root = tree.getroot()
            
            for elem in root.iter():
                localName = elem.tag.split('}')[-1]
                
                if localName in docNames:
                    foundDocTypes.add(localName)
                    
        except Exception:
            foundDocTypes = set()
            
        if not foundDocTypes:
            docType = utils.getDocType(file)
            if docType in docNames:
                foundDocTypes.add(docType)
                
        return foundDocTypes


    def addTableContentGML(self, nr_tabeli, obj, fileNames=None):
        """Dodaje dane lub elementy obsługiwane przez operację `addTableContentGML`."""
        global checksums
        
        if fileNames:
            files = fileNames
        else:
            files = QFileDialog.getOpenFileNames(
                filter="pliki XML/GML (*.xml *.gml)"
            )[0]
        
        docNames = {
            'AktPlanowaniaPrzestrzennego':
                'Akt planowania przestrzennego',
            'RysunekAktuPlanowaniaPrzestrzennego':
                'Rysunek APP',
            'DokumentFormalny':
                'Dokument formalny',
            'StrefaPlanistyczna':
                'Strefa planistyczna',
            'ObszarUzupelnieniaZabudowy':
                'Obszar uzupełnienia zabudowy',
            'ObszarZabudowySrodmiejskiej':
                'Obszar zabudowy śródmiejskiej',
            'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                'Obszar standardów dostępności infrastruktury społecznej'
        }
        
        docNamesReverse = {
            value: key
            for key, value in docNames.items()
        }
        
        for file in files:
            plik = str(file)
            
            if not plik:
                continue
            
            normalizedFilePath = os.path.normcase(
                os.path.abspath(plik)
            )
            
            foundDocTypes = self.getDocTypesFromGML(plik)
            
            if not foundDocTypes:
                utils.showPopup(
                    title='Błędny plik',
                    text=(
                        'Wskazano błędny plik albo plik nie zawiera '
                        'obsługiwanych klas GML:\n%s'
                        % plik
                    )
                )
                continue
                
            # Dla drugiej tabeli nie wolno wczytać pliku,
            # który jest już w pierwszej albo drugiej tabeli.
            if nr_tabeli == 2:
                fileExistsInFirstTable = False
                fileExistsInSecondTable = False
                
                for row in range(obj.filesTable_widget.rowCount()):
                    fileItem = obj.filesTable_widget.item(row, 0)
                    
                    if fileItem is None:
                        continue
                        
                    existingFilePath = fileItem.toolTip()
                    
                    if not existingFilePath:
                        continue
                    
                    normalizedExistingPath = os.path.normcase(
                        os.path.abspath(existingFilePath)
                    )
                    
                    if normalizedExistingPath == normalizedFilePath:
                        fileExistsInFirstTable = True
                        break
                        
                if fileExistsInFirstTable:
                    utils.showPopup(
                        title='Dodawanie pliku do tabeli',
                        text=(
                            'Nie można wczytać pliku do drugiej tabeli, '
                            'ponieważ został już wczytany do pierwszej tabeli:\n'
                            '%s'
                            % plik
                        )
                    )
                    continue
                    
                for row in range(obj.filesTable_widget2.rowCount()):
                    fileItem = obj.filesTable_widget2.item(row, 0)
                    
                    if fileItem is None:
                        continue
                    
                    existingFilePath = fileItem.toolTip()
                    
                    if not existingFilePath:
                        continue
                    
                    normalizedExistingPath = os.path.normcase(
                        os.path.abspath(existingFilePath)
                    )
                    
                    if normalizedExistingPath == normalizedFilePath:
                        fileExistsInSecondTable = True
                        break
                        
                if fileExistsInSecondTable:
                    utils.showPopup(
                        title='Dodawanie pliku do tabeli',
                        text=(
                            'Plik został już wczytany do drugiej tabeli:\n%s'
                            % plik
                        )
                    )
                    continue
                    
            # Dla pierwszej tabeli sprawdzamy, czy typ obiektu
            # już istnieje. Wyjątkiem jest Dokument formalny i rysunek.
            if nr_tabeli == 1:
                existingDocTypes = set()
                
                for row in range(obj.filesTable_widget.rowCount()):
                    typeItem = obj.filesTable_widget.item(row, 1)
                    
                    if typeItem is None:
                        continue
                        
                    existingDocName = typeItem.text().strip()
                    
                    # Zgodność z ewentualnym starszym zapisem
                    if existingDocName == 'Dokument Formalny':
                        existingDocName = 'Dokument formalny'
                        
                    if existingDocName in ('Dokument formalny', 'Rysunek APP'):
                        continue
                        
                    if existingDocName in docNamesReverse:
                        existingDocTypes.add(
                            docNamesReverse[existingDocName]
                        )
                        
                duplicateDocTypes = set()
                
                for docType in foundDocTypes:
                    if docType in ('DokumentFormalny', 'RysunekAktuPlanowaniaPrzestrzennego'):
                        continue
                        
                    if docType in existingDocTypes:
                        duplicateDocTypes.add(docType)
                        
                if duplicateDocTypes:
                    duplicateNames = [
                        docNames[docType]
                        for docType in duplicateDocTypes
                        if docType in docNames
                    ]
                    
                    duplicateText = '\n'.join(
                        '• %s' % name
                        for name in duplicateNames
                    )
                    
                    utils.showPopup(
                        title='Dodawanie pliku do tabeli',
                        text=(
                            'Niektóre typy obiektów z wybranego pliku '
                            'występują już w pierwszej tabeli i nie zostaną '
                            'dodane ponownie:\n\n%s\n\nPlik:\n%s'
                            % (duplicateText, plik)
                        )
                    )
                    
                    allowedDocTypes = (
                        foundDocTypes - duplicateDocTypes
                    )
                    
                    if not allowedDocTypes:
                        continue
                        
            try:
                checksum = self.calculate_checksum(plik)
                
            except Exception as e:
                utils.showPopup(
                    title='Błąd odczytu pliku',
                    text=(
                        'Nie udało się obliczyć sumy kontrolnej pliku:\n'
                        '%s\n\n'
                        'Szczegóły błędu:\n%s'
                        % (plik, e)
                    )
                )
                continue
                
            if nr_tabeli == 1:
                rowsBefore = obj.filesTable_widget.rowCount()
                
                rowsAfter = self.tableContentGML(
                    plik,
                    obj,
                    rowsBefore
                )
                
                if rowsAfter > rowsBefore:
                    checksums.add(checksum)
                    
                else:
                    utils.showPopup(
                        title='Dodawanie pliku do tabeli',
                        text=(
                            'Nie dodano żadnego nowego typu obiektu '
                            'z pliku:\n%s'
                            % plik
                        )
                    )
                    
            elif nr_tabeli == 2:
                rowsBefore = obj.filesTable_widget2.rowCount()
                
                self.tableContentGML2(
                    plik,
                    obj,
                    rowsBefore
                )
                
                rowsAfter = obj.filesTable_widget2.rowCount()
                
                if rowsAfter > rowsBefore:
                    checksums.add(checksum)
                    
                else:
                    utils.showPopup(
                        title='Dodawanie pliku do tabeli',
                        text=(
                            'Nie znaleziono klas możliwych do dodania '
                            'z pliku:\n%s'
                            % plik
                        )
                    )
                    
            else:
                utils.showPopup(
                    title='Błąd',
                    text='Nieznany numer tabeli: %s' % nr_tabeli
                )


    def tableContentGML(self, file, obj, rows):
        """Zwraca wynik operacji `tableContentGML` wykonywanej w bieżącym module."""
        docNames = {
            'AktPlanowaniaPrzestrzennego':
                'Akt planowania przestrzennego',
            'RysunekAktuPlanowaniaPrzestrzennego':
                'Rysunek APP',
            'DokumentFormalny':
                'Dokument formalny',
            'StrefaPlanistyczna':
                'Strefa planistyczna',
            'ObszarUzupelnieniaZabudowy':
                'Obszar uzupełnienia zabudowy',
            'ObszarZabudowySrodmiejskiej':
                'Obszar zabudowy śródmiejskiej',
            'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                'Obszar standardów dostępności infrastruktury społecznej'
        }
        
        docNamesOrder = [
            'AktPlanowaniaPrzestrzennego',
            'RysunekAktuPlanowaniaPrzestrzennego',
            'DokumentFormalny',
            'StrefaPlanistyczna',
            'ObszarUzupelnieniaZabudowy',
            'ObszarZabudowySrodmiejskiej',
            'ObszarStandardowDostepnosciInfrastrukturySpolecznej'
        ]
        
        docNamesReverse = {
            value: key
            for key, value in docNames.items()
        }
        
        foundDocTypes = self.getDocTypesFromGML(file)
        
        if not foundDocTypes:
            utils.showPopup(
                title='Błędny plik',
                text=(
                    'W pliku nie znaleziono obsługiwanych klas GML:\n%s'
                    % file
                )
            )
            return obj.filesTable_widget.rowCount()
        
        head, tail = ntpath.split(file)
        fileName = tail or ntpath.basename(head)
        
        normalizedFilePath = os.path.normcase(
            os.path.abspath(file)
        )
        
        modificationTime = os.path.getmtime(file)
        modificationDate = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(modificationTime)
        )
        
        flags = Qt.ItemFlags(32)
        
        existingGlobalDocTypes = set()
        existingFileDocNames = set()
        
        for tableRow in range(obj.filesTable_widget.rowCount()):
            fileItem = obj.filesTable_widget.item(tableRow, 0)
            typeItem = obj.filesTable_widget.item(tableRow, 1)
            
            if typeItem is None:
                continue
            
            existingDocName = typeItem.text().strip()
            
            if existingDocName == 'Dokument Formalny':
                existingDocName = 'Dokument formalny'
                
            if (
                existingDocName not in ('Dokument formalny', 'Rysunek APP')
                and existingDocName in docNamesReverse
            ):
                existingGlobalDocTypes.add(
                    docNamesReverse[existingDocName]
                )
                
            if fileItem is None:
                continue
            
            existingFilePath = fileItem.toolTip()
            
            if not existingFilePath:
                continue
                
            normalizedExistingPath = os.path.normcase(
                os.path.abspath(existingFilePath)
            )
            
            if normalizedExistingPath == normalizedFilePath:
                existingFileDocNames.add(existingDocName)
                
        for docType in docNamesOrder:
            if docType not in foundDocTypes:
                continue
            
            docName = docNames[docType]
            
            # Tego samego typu z tego samego pliku nie dodajemy ponownie.
            # Dotyczy również dokumentu formalnego.
            if docName in existingFileDocNames:
                continue
                
            # Każdy typ poza dokumentem formalnym
            # może wystąpić w pierwszej tabeli tylko raz.
            if (
                docType != 'DokumentFormalny'
                and docType in existingGlobalDocTypes
            ):
                continue
                
            currentRow = obj.filesTable_widget.rowCount()
            
            obj.filesTable_widget.setRowCount(
                currentRow + 1
            )
            
            fileItem = QTableWidgetItem(fileName)
            fileItem.setToolTip(file)
            
            obj.filesTable_widget.setItem(
                currentRow,
                0,
                fileItem
            )
            
            typeItem = QTableWidgetItem(docName)
            typeItem.setFlags(flags)
            
            obj.filesTable_widget.setItem(
                currentRow,
                1,
                typeItem
            )
            
            dateItem = QTableWidgetItem(modificationDate)
            dateItem.setFlags(flags)
            
            obj.filesTable_widget.setItem(
                currentRow,
                2,
                dateItem
            )
            
            if docType == 'DokumentFormalny':
                relationComboBox = QComboBox()
                
                relationComboBox.addItems(
                    list(dictionaries.relacjeDokumentu.keys())
                )
                
                obj.filesTable_widget.setCellWidget(
                    currentRow,
                    3,
                    relationComboBox
                )
                
            else:
                emptyItem = QTableWidgetItem('')
                emptyItem.setFlags(flags)
                
                obj.filesTable_widget.setItem(
                    currentRow,
                    3,
                    emptyItem
                )
                
            existingFileDocNames.add(docName)
            
            if docType != 'DokumentFormalny':
                existingGlobalDocTypes.add(docType)
                
        return obj.filesTable_widget.rowCount()


    def tableContentGML2(self, file, obj, rows):
        # Ustawianie rodzaju dokumentu
        """Zwraca wynik operacji `tableContentGML2` wykonywanej w bieżącym module."""
        docNames = {
                    'AktPlanowaniaPrzestrzennego': 'Akt planowania przestrzennego',
                    'RysunekAktuPlanowaniaPrzestrzennego': 'Rysunek APP',
                    'DokumentFormalny': 'Dokument formalny',
                    'StrefaPlanistyczna':'Strefa planistyczna',
                    'ObszarUzupelnieniaZabudowy':'Obszar uzupełnienia zabudowy',
                    'ObszarZabudowySrodmiejskiej':'Obszar zabudowy śródmiejskiej',
                    'ObszarStandardowDostepnosciInfrastrukturySpolecznej':'Obszar standardów dostępności infrastruktury społecznej'
                   }
        
        docNamesGML = set()
        
        try:
            tree = ET.parse(file)  # nosec B314
            root = tree.getroot()
            
            elemList = set()
            for elem in root.iter():
                elemList.add(elem.tag)
                
            # usuwanie duplikatów
            elemList = list(elemList)
            
            for elem in elemList:
                for docName in docNames:
                    if docName in elem:
                        docNamesGML.add(docNames[docName])
        except:
            return ''
        
        for docName in docNamesGML:
            # data modyfikacji
            def path_leaf(file):
                """Zwraca końcowy element wskazanej ścieżki."""
                head, tail = ntpath.split(file)
                return tail or ntpath.basename(head)
            file2 = path_leaf(file)
            flags = Qt.ItemFlags(32)
            obj.filesTable_widget2.setRowCount(rows + 1)
            obj.filesTable_widget2.setItem(rows, 0, QTableWidgetItem(file2))
            txt = obj.filesTable_widget2.item(rows, 0)
            txt.setToolTip(file)
            
            t = os.path.getmtime(file)
            mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            item = QTableWidgetItem(mtime)
            item.setFlags(flags)
            obj.filesTable_widget2.setItem(rows, 2, item)
            
            rodzaj = ['Dokument formalny', 'Akt planowania przestrzennego', 'Rysunek APP', 'Strefa planistyczna', 'Obszar uzupełnienia zabudowy', 'Obszar zabudowy śródmiejskiej', 'Obszar standardów dostępności infrastruktury społecznej']
            item2 = QTableWidgetItem(docName)
            item2.setFlags(flags)
            
            obj.filesTable_widget2.setItem(rows, 1, item2)
            
            rows += 1


    def deleteTableContentGML(self, nr_tabeli, obj):
        """Usuwa dane lub elementy obsługiwane przez operację `deleteTableContentGML`."""
        global checksums
        if nr_tabeli == 1:
            row_num = obj.filesTable_widget.rowCount()
        else:
            row_num = obj.filesTable_widget2.rowCount()
        if row_num > 0:
            if nr_tabeli == 1:
                do_usuniecia = obj.filesTable_widget.currentRow()
                if do_usuniecia != -1:
                    txt = obj.filesTable_widget.item(do_usuniecia, 0)
                    checksum = self.calculate_checksum(txt.toolTip())
                    obj.filesTable_widget.removeRow(do_usuniecia)
                    obj.filesTable_widget.setCurrentCell(-1, -1)
            else:
                do_usuniecia = obj.filesTable_widget2.currentRow()
                if do_usuniecia != -1:
                    txt = obj.filesTable_widget2.item(do_usuniecia, 0)
                    checksum = self.calculate_checksum(txt.toolTip())
                    obj.filesTable_widget2.removeRow(do_usuniecia)
                    obj.filesTable_widget2.setCurrentCell(-1, -1)
            if do_usuniecia != -1 and checksum in checksums:
                checksums.remove(checksum)
        else:
            pass


    def deteteChecksum(self, checksum):
        """Usuwa dane lub elementy obsługiwane przez operację `deteteChecksum`."""
        global checksums
        if checksum in checksums:
            checksums.remove(checksum)



    def hasTableSP(self):
        """Sprawdza warunek określony przez operację `hasTableSP` i zwraca jego wynik."""
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        for i in range(row_num):
            if 'Strefa planistyczna' in self.generowanieGMLDialog.filesTable_widget.item(i, 1).text():
                return True
        return False


    def app_status_PWLR(self,docList):
        """Zwraca wynik operacji `app_status_PWLR` wykonywanej w bieżącym module."""
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        for i in range(row_num):
            if 'Akt planowania przestrzennego' in self.generowanieGMLDialog.filesTable_widget.item(i, 1).text():
                for doc in docList:
                    if self.generowanieGMLDialog.filesTable_widget.item(i, 0).text() in doc[0]:
                        root = ET.parse(doc[0]).getroot()  # nosec B314
                        namespaces = {'app': 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0'}
                        for status in root.findall('.//app:status', namespaces):
                            for attr_name, attr_value in status.attrib.items():
                                if attr_name == '{http://www.w3.org/1999/xlink}title' and attr_value == 'prawnie wiążący lub realizowany':
                                    return True
                        return False


    def getTableContent(self, table_num, obj):
        """Pobiera dane wymagane przez operację `getTableContent`."""
        content = []
        if table_num == 1:
            row_num = obj.filesTable_widget.rowCount()
        else:
            row_num = obj.filesTable_widget2.rowCount()
        for i in range(row_num):
            if table_num == 1:
                item = obj.filesTable_widget.item(i, 0).toolTip()
                typObiektu = obj.filesTable_widget.item(i, 1).text()
                try:
                    relation = obj.filesTable_widget.cellWidget(i, 3).currentText()
                except:
                    relation = ''
                content.append([item, typObiektu, relation])
            else:
                item = obj.filesTable_widget2.item(i, 0).toolTip()
                typObiektu = obj.filesTable_widget2.item(i, 1).text()
                content.append([item, typObiektu])
        return content  # ścieżki do plików


    def get_app_status(self, docList):
        """Pobiera dane wymagane przez operację `get_app_status`."""
        namespaces = {
            'app': (
                'https://www.gov.pl/static/'
                'zagospodarowanieprzestrzenne/schemas/app/3.0'
            )
        }
        
        xlink_title = (
            '{http://www.w3.org/1999/xlink}title'
        )
        
        for file_path, doc_type, relation in docList:
            if doc_type != 'Akt planowania przestrzennego':
                continue
            
            root = ET.parse(file_path).getroot()  # nosec B314
            status = root.find('.//app:status', namespaces)
            
            if status is not None:
                return status.attrib.get(xlink_title)
            
        return None


    def generateAPP(self, obj, fileName=None, param=None):
        """Generowanie pliku z APP"""
        docList1 = self.getTableContent(1, obj)
        if len(docList1) == 0:
            utils.showPopup(title='Brak Dokumentów',text='Do tabeli nie zostały dodane żadne dokumenty.')
        else:
            uchwala_count = 0
            przystapienie_count = 0
            for file, doc, rel in docList1:
                if rel == 'uchwala':
                    uchwala_count += 1
                if rel == 'przystąpienie':
                    przystapienie_count += 1
            uchwala_przystapienie_count = przystapienie_count + uchwala_count
            app_status = self.get_app_status(docList1)
            przestrzenNazw_list = utils.validatePrzestrzenNazwAppSet(files=docList1)
            if not utils.validateObjectNumber(files=docList1):
                pass
            elif len(przestrzenNazw_list) != 1:
                utils.showPopup('Błąd przestrzeni nazw',f'Obiekty pochodzą z różnych przestrzeni nazw tj.: {przestrzenNazw_list}.\nSprawdź czy wszystkie obiekty posiadają taką samą wartość w polu przestrzeń nazw. Upewnij się, że w ustawieniach wszystkie pola są poprawnie wypełnione.')
            elif not utils.validateDokumentFormalnyDate(files=docList1):
                utils.showPopup('Błąd relacji dokumentów','Dokument z relacją uchwala nie może być starszy od dokumentu z relacją przystąpienie.')
            elif (app_status in ('prawnie wiążący lub realizowany', 'nieaktualny') and uchwala_count != 1):
                utils.showPopup(title='Błąd relacji dokumentów', text='Dla APP o statusie "%s" wymagany jest dokładnie jeden dokument z relacją "uchwala".' % app_status)
            elif uchwala_przystapienie_count == 0:
                utils.showPopup(title='Błąd relacji dokumentów', text='Wymagany jest co najmniej jeden dokument z relacją "przystąpienie" lub "uchwala".')
            elif uchwala_count > 1:
                utils.showPopup(title='Błąd relacji dokumentów', text='W APP dozwolony jest tylko jeden dokument z relacją "uchwala".')
            elif rodzajZbioru == 'POG' and not self.hasTableSP() and self.app_status_PWLR(docList1):
                utils.showPopup(title='Błąd APP', text='Dla APP o statusie "prawnie wiążący lub realizowany" wymagany jest plik "Strefa Planistyczna".')
            else:
                if rodzajZbioru == 'POG' and self.activeDlg != self.generowanieGMLDialogPoUniewaznieniu:
                    docList1 = sorted(docList1, key=lambda x: x[1], reverse=True)
                    docList2 = self.getTableContent(2, obj)
                    if len(docList2) > 0:
                        podanoDateObowiazujeOd = False
                        anulowanoUspojnienieDaty = False
                        dataObowiazujeOd = None
                        dataCzasTeraz = QDateTime.currentDateTimeUtc()
                        for doc1 in docList1:
                            for doc2 in docList2:
                                if doc1[1] == doc2[1]:
                                    lokalnyids_to_update = list(self.kontrolaZmianAtrybutowWzgledemWersji(doc1[0],doc2[0]))
                                    if len(lokalnyids_to_update) > 0:
                                        if not podanoDateObowiazujeOd:
                                            dataObowiazujeOd = self.pobierzDateObowiazujeOd()
                                            if dataObowiazujeOd == None:
                                                utils.showPopup(title='Pobieranie daty obowiązuje od', text='Ponieważ anulowano wskazanie daty obowiązuje od, nie nastąpi jej uspójnienie.')
                                                anulowanoUspojnienieDaty = True
                                                break
                                            else:
                                                podanoDateObowiazujeOd = True
                                        doc1[0] = self.updateObowiazujeOd(doc1[0], lokalnyids_to_update, dataObowiazujeOd, dataCzasTeraz)
                                    break
                            # Jeżeli użytkownik anulował podanie daty,
                            # kończymy całe uspójnianie, a nie tylko pętlę doc2.
                            if anulowanoUspojnienieDaty:
                                break
                            if podanoDateObowiazujeOd and doc1[1] == 'Akt planowania przestrzennego':
                                lokalnyids_to_update = list(self.lokalnyId_APP(doc1[0]))
                                doc1[0] = self.updateObowiazujeOd(doc1[0], lokalnyids_to_update, dataObowiazujeOd, dataCzasTeraz)
                                continue
                
                defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
                if fileName:
                    self.fn = defaultPath + "/" + fileName
                else:
                    self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="GML Files (*.gml)")[0]
                
                if self.fn:
                    xml_string = utils.mergeDocsToAPP(docList1)
                    if xml_string != '':
                        myfile = open(self.fn, "w", encoding='utf-8')
                        myfile.write(xml_string)
                        
                        if param:
                            self.showPopupApp(obj, param)
                        else:
                            self.showPopupApp(obj)


    def loadSet(self):
        """Wczytuje dane obsługiwane przez operację `loadSet`."""
        setPath = self.zbiorPrzygotowanieDialog.addFile_widget.filePath()
        param = True
        if setPath:
            for iip in utils.setAppId(setPath):
                rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
                if rows > 0:
                    for i in range(rows):
                        item = self.zbiorPrzygotowanieDialog.appTable_widget.item(i, 0).text()
                        if iip == item:
                            param = False
                            showPopup("Błąd tabeli","Wybrany plik znajduje się już w tabeli")
                            break
                    if param:
                        self.tableContentAddSet(iip + ' (Zbiór)', setPath, rows)
                else:
                    self.tableContentAddSet(iip + ' (Zbiór)', setPath, rows)


    def addTableContentSet(self, fileNames=None):
        """Dodaje dane lub elementy obsługiwane przez operację `addTableContentSet`."""
        if fileNames:
            files = fileNames
        else:
            files = QFileDialog.getOpenFileNames(filter = "pliki XML/GML (*.xml *.gml)")[0]
        for file in files:
            plik = str(file)
            param = True
            if plik:
                rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
                if utils.checkIfAPP(plik):
                    if rows > 0:
                        for i in range(rows):
                            item = self.zbiorPrzygotowanieDialog.appTable_widget.item(
                                i, 1).toolTip()
                            if plik == item:
                                param = False
                                showPopup("Błąd tabeli","Wybrany plik znajduje się już w tabeli")
                                break
                        if param:
                            self.tableContentSet(plik, rows)
                    else:
                        self.tableContentSet(plik, rows)
                else:
                    utils.showPopup('Błąd wczytanego pliku', 'Wczytany plik: \n%s\nnie jest aktem planowania przestrzennego.' % plik)


    def tableContentAddSet(self, iip, file, rows):
        """Dodanie zbioru do tabeli zbioru"""
        flags = Qt.ItemFlags(32)
        self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows + 1)
        
        # pierwsza kolumna
        idIIP = iip
        itemIIP = QTableWidgetItem(idIIP)
        itemIIP.setFlags(flags)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(
            rows, 0, itemIIP)
        # druga kolumna
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(
            rows, 1, QTableWidgetItem(file))
        # trzecia kolumna
        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        # dodanie do tabeli
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 2, item)


    def tableContentSet(self, file, rows):
        """Dodanie APP do tabeli zbioru"""
        def path_leaf(file):
            """Zwraca końcowy element wskazanej ścieżki."""
            head, tail = ntpath.split(file)
            return tail or ntpath.basename(head)
        file2 = path_leaf(file)
        flags = Qt.ItemFlags(32)
        self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows + 1)
        
        # pierwsza kolumna
        idIIP = utils.getIPPapp(file)
        itemIIP = QTableWidgetItem(idIIP)
        itemIIP.setFlags(flags)
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(
            rows, 0, itemIIP)
        # druga kolumna
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(
            rows, 1, QTableWidgetItem(file2))
        test = self.zbiorPrzygotowanieDialog.appTable_widget.item(rows, 1)
        test.setToolTip(file)
        # trzecia kolumna
        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        # dodanie do tabeli
        self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 2, item)


    def deleteTableContentSet(self):
        """Usuwa dane lub elementy obsługiwane przez operację `deleteTableContentSet`."""
        row_num = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.zbiorPrzygotowanieDialog.appTable_widget.currentRow()
            self.zbiorPrzygotowanieDialog.appTable_widget.removeRow(
                do_usuniecia)
            self.zbiorPrzygotowanieDialog.appTable_widget.setCurrentCell(
                -1, -1)
        else:
            pass


    def fieldsDefinition(self, fields):
        """Zwraca wynik operacji `fieldsDefinition` wykonywanej w bieżącym module."""
        if rodzajZbioru == 'POG':
            pomijane = ['zmiana', 'mapaPodkladowa', 'data', 'referencja',
                        'dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy', 'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy','zmienianyPlan']
        else:
            pomijane = ['zmiana', 'mapaPodkladowa', 'data', 'referencja', 'lacze',
                        'dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy', 'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy','wydzielenie','zmienianyPlan']
            # pomijane = ['tytulAlternatywny', 'typPlanu', 'poziomHierarchii', 'status', 'zmiana', 'mapaPodkladowa', 'data', 'referencja', 'lacze',
            #             'dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy', 'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy','wydzielenie']
        fieldDef = ''
        for field in fields:
            if field.name in pomijane:
                continue
            form = Formularz()
            if field.isComplex():  # zawiera podrzędne elementy typu complex
                for fieldElements in field.innerFormElements:
                    fieldDef += '&field=%s:%s' % (
                        fieldElements.name, fieldElements.type.replace('gml:ReferenceType', 'string').replace('anyURI', 'string'))
                continue
            if 'gml' not in field.type or 'gml:ReferenceType' in field.type:
                if field.type == 'string':
                    fieldDef += '&field=%s:%s' % (field.name, field.type + '(500)')
                else:
                    if field.name in ('profilPodstawowy','profilDodatkowy'):
                        fieldDef += '&field=%s:%s' % (field.name, field.type.replace('gml:ReferenceType', 'string(350)'))
                    else:
                        fieldDef += '&field=%s:%s' % (field.name, field.type.replace('gml:ReferenceType', 'string').replace('anyURI', 'string'))
            else:
                if field.type == 'gml:LengthType':
                    fieldDef += '&field=%s:%s' % (field.name, field.type.replace('gml:LengthType', 'real'))
                elif field.type == 'gml:AreaType':
                    fieldDef += '&field=%s:%s' % (field.name, field.type.replace('gml:AreaType', 'real'))
        return(fieldDef)


    def newEmptyLayer(self):
        """Tworzy dane lub obiekt wymagany przez operację `newEmptyLayer`."""
        s = QgsSettings()
        epsg = str(s.value("qgis_app2/settings/strefaPL2000", ""))
        geomTypeEPSG = 'polygon?crs=epsg:' + epsg
        
        if epsg in (0, NULL, ''):
            showPopup("Wygeneruj warstwę","Proszę uzupełnić ustawienia wtyczki APP.")
            return
        
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(int(epsg)))
        
        # włączenie snapowania i edycji topologicznej
        new_conf = QgsSnappingConfig(QgsProject.instance().snappingConfig())
        new_conf.setEnabled(True)
        QgsProject.instance().setSnappingConfig(new_conf)
        QgsProject.instance().setTopologicalEditing(True)
        
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        if not os.access(defaultPath, os.W_OK):
            showPopup("Wygeneruj warstwę","Brak uprawnień do zapisu w katalogu " + defaultPath+". W ustawieniach wtyczki wskaż domyślną ścieżkę zapisu plików z uprawnieniami do zapisu.")
            return
        
        field_edycja = utils.createEditField()
        if self.activeDlg == self.wektorInstrukcjaDialog or self.activeDlg == self.wektorInstrukcjaDialogPOG:
            fields = utils.createFormElements('AktPlanowaniaPrzestrzennegoType') + field_edycja
            if rodzajZbioru == 'POG':
                layerName = 'AktPlanowaniaPrzestrzennego'
                qml = 'AktPlanowaniaPrzestrzennego'
                popup_txt = 'granic planu ogólnego gminy'
                geomTypeEPSG = 'multipolygon?crs=epsg:' + epsg
            else:
                layerName = 'granice_app'
                popup_txt = 'app'
                geomTypeEPSG = 'multipolygon?crs=epsg:' + epsg
        elif self.activeDlg == self.wektorInstrukcjaDialogSPL:
            fieldsWP = utils.createFormElements('WydzieleniePlanistyczneType')
            fieldsSPL = utils.createFormElements('StrefaPlanistycznaType')
            fields = fieldsWP + fieldsSPL + field_edycja
            layerName ='StrefaPlanistyczna'
            popup_txt = 'stref planistycznych'
        elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
            fields = utils.createFormElements('RegulacjaType') + field_edycja
            layerName ='ObszarUzupelnieniaZabudowy'
            popup_txt = 'granic obszarów uzupełnienia zabudowy'
        elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
            fields = utils.createFormElements('RegulacjaType') + field_edycja
            layerName ='ObszarZabudowySrodmiejskiej'
            popup_txt = 'granic obszarów zabudowy śródmiejskiej'
        elif self.activeDlg == self.wektorInstrukcjaDialogOSD:
            fieldsRegulacja = utils.createFormElements('RegulacjaType')
            fieldsOSD = utils.createFormElements('ObszarStandardowDostepnosciInfrastrukturySpolecznejType')
            fields = fieldsRegulacja + fieldsOSD + field_edycja
            layerName ='ObszarStandardowDostepnosciInfrastrukturySpolecznej'
            popup_txt = 'granic obszarów standardów dostępności infrastruktury społecznej'
        
        layers = QgsProject.instance().mapLayers()
        i = 0
        nazwyWarstw = []
        for layer in layers.values():
            if layer.name().startswith(layerName):
                nazwyWarstw.append(layer.name())
        for n in range(100):
            if n == 0:
                nazwaWarstwy = layerName
            else:
                nazwaWarstwy = layerName + "_" + str(n)
            if not nazwaWarstwy in nazwyWarstw and not os.path.exists(pathlib.Path(str(defaultPath + '/' + nazwaWarstwy + '.gpkg'))):
                i = n
                break
        
        numerWarstwy = ''
        if i > 0:
            numerWarstwy = '_' + str(i)
        
        layer = QgsVectorLayer(geomTypeEPSG + self.fieldsDefinition(fields=fields), layerName + numerWarstwy, 'memory')
        
        output_path = str(pathlib.Path(str(defaultPath + '/' + layerName + numerWarstwy + '.gpkg')))
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = 'GPKG'
        options.layerName = layerName + numerWarstwy
        options.fileEncoding = 'UTF-8'
        options.destCRS = QgsCoordinateReferenceSystem('EPSG:' + epsg)
        error =  QgsVectorFileWriter.writeAsVectorFormatV3(layer, output_path, QgsCoordinateTransformContext(), options)
        if rodzajZbioru == 'POG':
            # Sprawdzenie wyniku zapisu
            if error[0] == QgsVectorFileWriter.NoError:
                gkpg = QgsVectorLayer(output_path, layerName + numerWarstwy, 'ogr')
                gkpg.startEditing()
                editFormConfig = gkpg.editFormConfig()
                pathUI = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".ui")
                editFormConfig.setUiForm(str(pathUI))
                pathPy = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".py")
                editFormConfig.setInitFilePath(str(pathPy))
                editFormConfig.setInitFunction("my_form_open")
                gkpg.setEditFormConfig(editFormConfig)
                layer = gkpg
        
        pathQML = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/QML/" + layerName + ".qml")
        layer.startEditing()
        layer.loadNamedStyle(str(pathQML))
        
        QgsProject.instance().addMapLayer(layer)
        
        self.iface.messageBar().pushSuccess("Utworzenie warstwy:","Stworzono warstwę do wektoryzacji.")
        
        def on_geometry_changed(fid, geom, warstwa_tmp):
            """Obsługuje zmianę geometrii obiektu i aktualizuje zależne dane."""
            changed_feature = warstwa_tmp.getFeature(fid)
            dataCzasTeraz = QDateTime.currentDateTimeUtc()
            try:
                changed_feature.setAttribute("wersjaId", dataCzasTeraz.toString("yyyyMMddThhmmss"))
                changed_feature.setAttribute("poczatekWersjiObiektu", dataCzasTeraz)
                changed_feature.setAttribute("edycja", True)
            except Exception as e:
                print(e)
            warstwa_tmp.updateFeature(changed_feature)
        
        layer.geometryChanged.connect(lambda fid, geom, lyr=layer: on_geometry_changed(fid, geom, lyr))
        
        showPopup("Wygeneruj warstwę","Poprawnie utworzono pustą warstwę " + popup_txt + ". Uzupełnij ją danymi przestrzennymi.")
        
    """Popup windows"""


    def showPopupSaveForm(self, fileName=None):
        """Wyświetla komunikat związany z operacją `showPopupSaveForm`."""
        if utils.isFormFilled(self.activeDlg) and utils.validate_form_dates(self.activeDlg.formElements) and utils.validate_status(self.activeDlg.formElements) and utils.validate_typPlanu(self.activeDlg.formElements):
            s = QgsSettings()
            defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
            
            if fileName:
                self.fn = defaultPath + "/" + fileName
            else:
                self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="GML Files (*.gml)")[0]
            if self.fn:
                self.saved = True
                try:
                    if self.activeDlg == self.wektorInstrukcjaDialogSPL:
                        self.obrysLayer = self.wektorInstrukcjaDialogSPL.layers_comboBox.currentLayer()
                    elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
                        self.obrysLayer = self.wektorInstrukcjaDialogOUZ.layers_comboBox.currentLayer()
                    elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
                        self.obrysLayer = self.wektorInstrukcjaDialogOZS.layers_comboBox.currentLayer()
                    elif self.activeDlg == self.wektorInstrukcjaDialogOSD:
                        self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
                    else:
                        self.obrysLayer = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
                except:
                    self.obrysLayer = None
                data = utils.createXmlData(self.activeDlg, self.obrysLayer)
                
                ET.indent(data, space="    ", level=0)
                xml_string = ET.tostring(data, 'unicode')
                
                myfile = open(self.fn, "w", encoding='utf-8')
                myfile.write(xml_string)
                
                if self.activeDlg == self.wektorFormularzDialog:
                    showPopup("Zapisz aktualny formularz",
                              "Poprawnie zapisano formularz.")
                else:
                    showPopup("Zapisz aktualny formularz",
                              "Poprawnie zapisano formularz. W razie potrzeby wygenerowania kolejnego formularza, należy zmodyfikować dane oraz zapisać formularz ponownie.")
        return self.saved


    def showPopupAggregate(self, title, text, layer):
        """Wyświetla komunikat związany z operacją `showPopupAggregate`."""
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            self.aggregateLayer(layer)


    def aggregateLayer(self, layer):
        # Aggregate
        """Realizuje operację `aggregateLayer` w bieżącym module."""
        alg_params = {
            'AGGREGATES': [],
            'GROUP_BY': 'NULL',
            'INPUT': layer,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        aggregated = processing.run('native:aggregate', alg_params)
        aggregated['OUTPUT'].setName('granice_app_zagregowane')
        QgsProject.instance().addMapLayer(aggregated['OUTPUT'])


    def showPopupApp(self, obj, param=None):
        # Popup generowanie APP
        """Wyświetla komunikat związany z operacją `showPopupApp`."""
        if param == None:
            msg = QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setWindowTitle('Czy chcesz utworzyć kolejne dane dla APP?')
            msg.setText(
                'Wygenerowano plik GML dla APP. Czy chcesz utworzyć kolejne dane dla APP?')
            yes = msg.addButton(
                'Tak', QtWidgets.QMessageBox.AcceptRole)
            no = msg.addButton(
                'Nie', QtWidgets.QMessageBox.AcceptRole)
            cancel = msg.addButton(
                'Anuluj', QtWidgets.QMessageBox.RejectRole)
            msg.setDefaultButton(yes)
            msg.exec_()
            msg.deleteLater()
            if msg.clickedButton() is yes:
                if rodzajZbioru != 'POG':
                    self.openNewDialog(self.rasterInstrukcjaDialog)
                else:
                    self.openNewDialog(self.wektorInstrukcjaDialogPOG)
                self.listaOkienek.append(obj)
            elif msg.clickedButton() is no:
                self.showPopupSet(obj)


    def showPopupSet(self, obj):
        """Wyświetla komunikat związany z operacją `showPopupSet`."""
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Czy chcesz utworzyć zbiór APP?')
        msg.setText(
            'Czy chcesz przejść do tworzenia zbioru czy zakończyć pracę?')
        set = msg.addButton(
            'Tworzenie zbioru', QtWidgets.QMessageBox.AcceptRole)
        cancel = msg.addButton(
            'Anuluj', QtWidgets.QMessageBox.RejectRole)
        quit = msg.addButton(
            'Zakończ', QtWidgets.QMessageBox.AcceptRole)
        
        msg.setDefaultButton(set)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is set:
            self.openNewDialog(self.zbiorPrzygotowanieDialog)
            self.listaOkienek.append(obj)
        elif msg.clickedButton() is quit:
            obj.close()


    def wektorInstrukcjaDialogSPLcheckSaveForms(self):
        """Zwraca wynik operacji `wektorInstrukcjaDialogSPLcheckSaveForms` wykonywanej w bieżącym module."""
        def findElement(formElements, name):
            """Wyszukuje elementy wymagane przez operację `findElement`."""
            for formElement in formElements:
                if formElement.name == name:
                    return formElement
                for inner in formElement.innerFormElements:
                    if inner.name == name:
                        return inner
            return None


    def checkSaveForms(self):
        """Wykonuje kontrolę danych w ramach operacji `checkSaveForms`."""
        def findElement(formElements, name):
            """Wyszukuje elementy wymagane przez operację `findElement`."""
            for formElement in formElements:
                if formElement.name == name:
                    return formElement
                for inner in formElement.innerFormElements:
                    if inner.name == name:
                        return inner
            return None
        
        def setValue(formElement1, formElement2):
            """Ustawia dane lub stan wymagany przez operację `setValue`."""
            if formElement1 is None or formElement2 is None:
                return
            if formElement1.type == 'string':
                utils.setValueToWidget(
                    formElement2, formElement1.refObject.text())
            elif formElement1.type == 'date':
                if utils.checkForNoDateValue(formElement1.refObject):
                    return
                dateValue = formElement1.refObject.text()
                try:
                    date_time_obj = datetime.strptime(dateValue, '%d.%m.%Y')
                except:
                    date_time_obj = datetime.strptime(dateValue, '%Y-%m-%d')
                str_date = date_time_obj.strftime("%Y-%m-%d")
                utils.setValueToWidget(formElement2, str_date)
            elif formElement1.type == 'dateTime':
                if utils.checkForNoDateValue(formElement1.refObject):
                    return
                dateValue = formElement1.refObject.text()
                try:
                    date_time_obj = datetime.strptime(dateValue, '%d.%m.%Y %H:%M:%S')
                except:
                    date_time_obj = datetime.strptime(dateValue, '%Y-%m-%d %H:%M:%S')
                str_date = date_time_obj.strftime("%Y-%m-%dT%H:%M:%S")
                utils.setValueToWidget(formElement2, str_date)
        
        if self.saved:
            if self.activeDlg == self.rasterFormularzDialog:
                self.openNewDialog(self.wektorInstrukcjaDialog)
                self.listaOkienek.append(self.rasterFormularzDialog)
            elif self.activeDlg == self.wektorFormularzDialog:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorFormularzDialog)
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
            elif self.activeDlg == self.dokumentyFormularzDialogPoUniewaznieniu:
                self.openNewDialog(self.generowanieGMLDialogPoUniewaznieniu)
                self.listaOkienek.append(self.dokumentyFormularzDialogPoUniewaznieniu)
            self.saved = False
        else:
            self.showPopupSaveForms()
        
        # Przenoszenie wartości między formularzami.
        setValue(findElement(self.rasterFormularzDialog.formElements, 'przestrzenNazw'),
                 findElement(self.wektorFormularzDialog.formElements, 'przestrzenNazw'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'przestrzenNazw'),
                 findElement(self.dokumentyFormularzDialog.formElements, 'przestrzenNazw'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'koniecWersjiObiektu'),
                 findElement(self.wektorFormularzDialog.formElements, 'koniecWersjiObiektu'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'obowiazujeOd'),
                 findElement(self.wektorFormularzDialog.formElements, 'obowiazujeOd'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'obowiazujeDo'),
                 findElement(self.wektorFormularzDialog.formElements, 'obowiazujeDo'))
        return self.saved


    def showPopupSaveForms(self):
        """Wyświetla komunikat związany z operacją `showPopupSaveForms`."""
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niezapisany formularz')
        msg.setText(
            'Formularz nie został zapisany. Czy na pewno chcesz przejść dalej?')
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(no)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            if self.activeDlg == self.rasterFormularzDialog:
                self.openNewDialog(self.wektorInstrukcjaDialog)
                self.listaOkienek.append(self.rasterFormularzDialog)
            elif self.activeDlg == self.wektorFormularzDialog:
                if rodzajZbioru == 'POG':
                    self.openNewDialog(self.generowanieGMLDialog)
                else:
                    self.openNewDialog(self.dokumentyFormularzDialog)
                self.listaOkienek.append(self.wektorFormularzDialog)
            elif self.activeDlg == self.dokumentyFormularzDialog:
                self.openNewDialog(self.generowanieGMLDialog)
                self.listaOkienek.append(self.dokumentyFormularzDialog)
            elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
                self.openNewDialog(self.wektorFormularzDialogOUZ)
                self.listaOkienek.append(self.wektorInstrukcjaDialogOUZ)
            elif self.activeDlg == self.dokumentyFormularzDialogPoUniewaznieniu:
                self.openNewDialog(self.generowanieGMLDialogPoUniewaznieniu)


    def checkSaveSet(self):
        """Wykonuje kontrolę danych w ramach operacji `checkSaveSet`."""
        if self.generated:
            self.openNewDialog(self.metadaneDialog)
            self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
            self.generated = False
        else:
            self.showPopupSaveSet()
        return False


    def showPopupSaveSet(self):
        """Wyświetla komunikat związany z operacją `showPopupSaveSet`."""
        msg = QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle('Niewygenerowany GML dla zbioru')
        msg.setText(
            'GML nie został jeszcze wygenerowany. Czy na pewno chcesz przejść do tworzenia metadanych?')
        yes = msg.addButton(
            'Tak', QtWidgets.QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QtWidgets.QMessageBox.RejectRole)
        msg.setDefaultButton(no)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            self.openNewDialog(self.metadaneDialog)
            self.listaOkienek.append(self.zbiorPrzygotowanieDialog)


    def prepareIdIPP(self, formularz):
        """definuje autouzupełnianie idIPP na podstawie zagnieżdzonych pól"""
        def updateIdIPP():
            """Aktualizuje dane obsługiwane przez operację `updateIdIPP`."""
            idIPP_list = []
            przestrzenNazw = przestrzenNazw_lineEdit.text().replace("/", "_")
            lokalnyId = lokalnyId_lineEdit.text()
            if self.activeDlg == self.dokumentyFormularzDialog:
                wersjaId_lineEdit.setText('')
            wersjaId = wersjaId_lineEdit.text()
            
            if przestrzenNazw.strip():
                idIPP_list.append(przestrzenNazw.strip())
            if lokalnyId.strip():
                idIPP_list.append(lokalnyId.strip())
            if wersjaId.strip():
                if self.activeDlg != self.dokumentyFormularzDialog:
                    idIPP_list.append(wersjaId.strip())
                    
            idIIP_lineEdit.setText("_".join(idIPP_list))
            
        # pobranie dynamicznie utworzonych obiektów UI
        idIIP_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="idIIP_lineEdit")
        lokalnyId_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="lokalnyId_lineEdit")
        przestrzenNazw_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="przestrzenNazw_lineEdit")
        wersjaId_lineEdit = utils.getWidgetByName(
            layout=formularz,
            searchObjectType=QgsFilterLineEdit,
            name="wersjaId_lineEdit")
        
        # definicja Eventów dynamicznych obiektów UI
        lokalnyId_lineEdit.textChanged.connect(lambda: updateIdIPP())
        przestrzenNazw_lineEdit.textChanged.connect(lambda: updateIdIPP())
        wersjaId_lineEdit.textChanged.connect(lambda: updateIdIPP())


    def loadFromGMLorGPKG(self, analizy, fileName=None, formatPliku=None):
        """Wczytuje dane obsługiwane przez operację `loadFromGMLorGPKG`."""
        global informacjaOgolna
        
        s = QgsSettings()
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        epsg_code = s.value("qgis_app2/settings/strefaPL2000", "/")
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
        
        if rodzajZbioru in ('AK', 'PZPW'):
            epsg_code = '2180'
        
        jpt = s.value("qgis_app2/settings/jpt", "/")
        dataCzasTeraz = QDateTime.currentDateTimeUtc()
        profile_msg = False
        profile_podstawowe_msg = False
        raport_poprawionych_profili = []
        raport_nierozpoznanych_profili = []
        ileRazyPowielicWarstwe = 1
        
        def popraw_wartosci_profili(wartosci, feature, nazwa_pola):
            """Zwraca wynik operacji `popraw_wartosci_profili` wykonywanej w bieżącym module."""
            from difflib import SequenceMatcher
            
            dozwolone_wartosci = list(
                dictionaries.profilPodstawowyLubDodatkowyListaKodowa.keys()
            )
            mapa_znormalizowanych = {
                " ".join(wartosc.split()).casefold(): wartosc
                for wartosc in dozwolone_wartosci
            }
            
            if isinstance(wartosci, str):
                lista_wartosci = [
                    wartosc.strip()
                    for wartosc in wartosci.split(",")
                    if wartosc.strip()
                ]
            elif isinstance(wartosci, (list, tuple)):
                lista_wartosci = [
                    str(wartosc).strip()
                    for wartosc in wartosci
                    if str(wartosc).strip()
                ]
            else:
                lista_wartosci = [str(wartosci).strip()]
                
            oznaczenie = feature.attribute("oznaczenie")
            if oznaczenie in (NULL, None, ""):
                oznaczenie = feature.attribute("symbol")
            if oznaczenie in (NULL, None, ""):
                oznaczenie = "brak oznaczenia"
                
            poprawione_wartosci = []
            czy_poprawiono = False
            
            for wartosc_pierwotna in lista_wartosci:
                wartosc_znormalizowana = " ".join(
                    wartosc_pierwotna.split()
                ).casefold()
                
                if wartosc_znormalizowana in mapa_znormalizowanych:
                    wartosc_poprawiona = mapa_znormalizowanych[
                        wartosc_znormalizowana
                    ]
                    
                    if wartosc_poprawiona != wartosc_pierwotna:
                        czy_poprawiono = True
                        raport_poprawionych_profili.append(
                            (
                                str(oznaczenie),
                                nazwa_pola,
                                wartosc_pierwotna,
                                wartosc_poprawiona
                            )
                        )
                        
                    poprawione_wartosci.append(wartosc_poprawiona)
                    continue
                
                dopasowania = []
                
                for dozwolona_wartosc in dozwolone_wartosci:
                    podobienstwo = SequenceMatcher(
                        None,
                        wartosc_znormalizowana,
                        dozwolona_wartosc.casefold()
                    ).ratio()
                    dopasowania.append((podobienstwo, dozwolona_wartosc))
                    
                dopasowania.sort(reverse=True)
                najlepsze_podobienstwo, najlepsza_wartosc = dopasowania[0]
                drugie_podobienstwo = (
                    dopasowania[1][0]
                    if len(dopasowania) > 1
                    else 0.0
                )
                
                if (
                    najlepsze_podobienstwo >= 0.88
                    and najlepsze_podobienstwo - drugie_podobienstwo >= 0.03
                ):
                    poprawione_wartosci.append(najlepsza_wartosc)
                    czy_poprawiono = True
                    raport_poprawionych_profili.append(
                        (
                            str(oznaczenie),
                            nazwa_pola,
                            wartosc_pierwotna,
                            najlepsza_wartosc
                        )
                    )
                else:
                    poprawione_wartosci.append(wartosc_pierwotna)
                    raport_nierozpoznanych_profili.append(
                        (
                            str(oznaczenie),
                            nazwa_pola,
                            wartosc_pierwotna
                        )
                    )
                    
            return poprawione_wartosci, czy_poprawiono
        subNamesSPL = ['maksNadziemnaIntensywnoscZabudowy','maksWysokoscZabudowy','maksUdzialPowierzchniZabudowy',
                       'minUdzialPowierzchniBiologicznieCzynnej','profileDodatkowe','obowiazujeOd']
        subNamesOSD = ['odleglosciIPowierzchnie','obowiazujeOd']
        subNamesOUZ = ['obowiazujeOd']
        subNamesOZS = ['obowiazujeOd']
        
        # włączenie snapowania i edycji topologicznej
        new_conf = QgsSnappingConfig(QgsProject.instance().snappingConfig())
        new_conf.setEnabled(True)
        QgsProject.instance().setSnappingConfig(new_conf)
        QgsProject.instance().setTopologicalEditing(True)
        
        if not os.access(defaultPath, os.W_OK):
            showPopup("Wczytaj warstwę","Brak uprawnień do zapisu w katalogu " + defaultPath + ". W ustawieniach wtyczki wskaż domyślną ścieżkę zapisu plików z uprawnieniami do zapisu.")
            return
        
        if epsg_code in (0, NULL, '') and rodzajZbioru == 'POG':
            showPopup("Wczytaj warstwę","Proszę uzupełnić w ustawieniach wtyczki APP wartość JPT dla rodzaju zbioru POG.")
            return
        
        if not informacjaOgolna:
            showPopup("Informacja",
                      "Wtyczka umożliwia wczytanie także niepoprawnych danych, aby umożliwić ich naprawienie. Rekomendujemy, aby plik sprawdzić w Przeglądarce danych planistycznych.")
            informacjaOgolna = True
        
        if fileName and formatPliku:
            file, format = fileName, formatPliku
        else:
            file, format = QFileDialog.getOpenFileName(directory=defaultPath,filter = "pliki GML (*.gml);; pliki GeoPackage (*.gpkg);")
            file = str(file)
        
        if not file:
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        
        try:
            while file.lower().endswith('.gml.gml'):
                nowa_nazwa = file[:-4]
                os.rename(file, nowa_nazwa)
                file = nowa_nazwa
            
            if format == 'pliki GML (*.gml)':
                gfsfile = str(pathlib.Path(file).with_suffix(".gfs"))
                if os.path.exists(gfsfile):
                    os.remove(gfsfile)
            
            ds = ogr.Open(file)
            warstwy = [x.GetName() for x in ds]
            
            activeDlgname = self.activeDlg.name
            if not any(activeDlgname.upper() in element.upper() for element in warstwy) and activeDlgname not in ['PytanieAppDialog','PytanieAppUniewaznienieDialog']:
                showPopup("Wczytaj warstwę","Proszę wskazać plik gml lub gpkg zawierający: " + activeDlgname)
                return
            
            
            if format == 'pliki GeoPackage (*.gpkg);':
                definicja_warstwy = ds.GetLayer().GetLayerDefn()
                ilosc_pol = definicja_warstwy.GetFieldCount()
                
                if ilosc_pol == 0:
                    showPopup("Wczytaj warstwę","Warstwa nie zawiera pól.")
                    return
                    
                for i in range(ilosc_pol):
                    nazwa_pola = definicja_warstwy.GetFieldDefn(i).GetName()
                    if nazwa_pola == 'profilPodstawowy':
                        warstwy = ['StrefaPlanistyczna']
                        break
                    if nazwa_pola == 'modyfikacja':
                        warstwy = ['AktPlanowaniaPrzestrzennego']
                        break
                    if nazwa_pola == 'wylaczenieZabudowyZagrodowej':
                        warstwy = ['ObszarStandardowDostepnosciInfrastrukturySpolecznej']
                        break
                    if nazwa_pola == 'symbol':
                        warstwa = ds.GetLayer()
                        for obiekt in warstwa:
                            wartosc_pola = obiekt.GetField('symbol')
                            if wartosc_pola == 'OUZ':
                                warstwy = ['ObszarUzupelnieniaZabudowy']
                            elif wartosc_pola == 'OZS':
                                warstwy = ['ObszarZabudowySrodmiejskiej']
                            break
                    break
            
            dozwoloneWarstwy = ['AktPlanowaniaPrzestrzennego','StrefaPlanistyczna','ObszarUzupelnieniaZabudowy','ObszarZabudowySrodmiejskiej','ObszarStandardowDostepnosciInfrastrukturySpolecznej','DokumentFormalny','RysunekAktuPlanowaniaPrzestrzennego']
            warstwy.sort(reverse=True)
            isJPTinLayer_msg = False
            
            for layerName in warstwy:
                
                # poprawa nazwy warstwy jeżeli to kwestia tylko wielkości liter
                nazwa = layerName.lower()
                for warstwa in dozwoloneWarstwy:
                    if warstwa.lower() in nazwa:
                        layerName = warstwa
                
                if layerName not in dozwoloneWarstwy:
                    showPopup("Wczytaj warstwę",f"Wskazany plik zawiera warstwę \"{layerName}\", która nie występuje w modelu planowania przestrzennego.")
                    continue
                
                if rodzajZbioru == 'POG' and layerName == 'RysunekAktuPlanowaniaPrzestrzennego':
                    showPopup("Wczytaj warstwę", "Dla rodzaju zbioru POG nie można wczytać warstwy RysunekAktuPlanowaniaPrzestrzennego.\n\nZmień rodzaj zbioru w ustawieniach wtyczki APP i ponownie wczytaj dane.")
                    return
                
                geomTypeEPSG = 'polygon?crs=epsg:' + str(epsg_code)
                geomType = 'Polygon'
                
                if file and layerName in dozwoloneWarstwy and activeDlgname in [layerName, 'PytanieAppDialog', 'PytanieAppUniewaznienieDialog']:
                    field_edycja = utils.createEditField()
                    if layerName == 'AktPlanowaniaPrzestrzennego':
                        fields = utils.createFormElements('AktPlanowaniaPrzestrzennegoType') + field_edycja
                        geomType = 'MultiPolygon'
                        geomTypeEPSG = 'multipolygon?crs=epsg:' + str(epsg_code)
                    if layerName == 'DokumentFormalny':
                        fields_DateCI_DateTypeCode = utils.createDateCI_DateTypeCodeFields()
                        fields = utils.createFormElements('DokumentFormalnyType') + fields_DateCI_DateTypeCode
                        # brudne rozwiazanie usuniecia wersjaId dla DokumentFormalnyType
                        for x in fields:
                            if x.name == 'idIIP':
                                for y in x.innerFormElements:
                                    if y.name == 'wersjaId':
                                        x.innerFormElements.remove(y)
                        geomType = 'NoGeometry'
                    if layerName == 'RysunekAktuPlanowaniaPrzestrzennego':
                        fields = utils.createFormElements('RysunekAktuPlanowaniaPrzestrzennegoType') + field_edycja
                        geomType = 'NoGeometry'
                    if layerName== 'StrefaPlanistyczna':
                        fieldsWP = utils.createFormElements('WydzieleniePlanistyczneType')
                        fieldsSPL = utils.createFormElements('StrefaPlanistycznaType')
                        fields = fieldsWP + fieldsSPL + field_edycja
                    elif layerName == 'ObszarUzupelnieniaZabudowy':
                        fields = utils.createFormElements('RegulacjaType') + field_edycja
                    elif layerName == 'ObszarZabudowySrodmiejskiej':
                        fields = utils.createFormElements('RegulacjaType') + field_edycja
                    elif layerName == 'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                        fieldsRegulacja = utils.createFormElements('RegulacjaType')
                        fieldsOSD = utils.createFormElements('ObszarStandardowDostepnosciInfrastrukturySpolecznejType')
                        fields = fieldsRegulacja + fieldsOSD + field_edycja
                    
                    def czyIstniejeWarstwaIPlik(layerName):
                        """Sprawdza warunek określony przez operację `czyIstniejeWarstwaIPlik` i zwraca jego wynik."""
                        for layer in QgsProject.instance().mapLayers().values():
                            if layer.name() == layerName:
                                return True
                        if os.path.exists(os.path.join(defaultPath, layerName + '.gpkg')):
                            return True
                        return False
                        
                    i = 0
                    numerWarstwy = ''
                    while czyIstniejeWarstwaIPlik(layerName + numerWarstwy):
                        i += 1
                        numerWarstwy = '_' + str(i)
                    
                    if format == 'pliki GML (*.gml)':
                        try:
                            tree = ET.parse(file)  # nosec B314
                        except Exception as e:
                            showPopup("Wczytaj warstwę",f"Dane GML dla \"{layerName}\" mają błąd składni.\n{e}")
                            return
                        
                        root = tree.getroot()
                        for elem in root.iter():
                            if elem.tag.endswith('featureMember') or elem.tag.endswith('member'):
                                namespace = elem.tag.split('}')[0].strip('{')
                                if namespace == 'http://www.opengis.net/wfs/2.0' or namespace == 'http://www.opengis.net/gml/3.2':
                                    pathGFS = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/GFS/")
                                    copyfile(pathGFS/pathlib.Path("template.gfs"), gfsfile)
                                break
                        layer = QgsVectorLayer(file + "|layername=" + layerName + "|option:FORCE_SRS_DETECTION=YES|option:CONSIDER_EPSG_AS_URN=YES|geometrytype=" + geomType, layerName + numerWarstwy, 'ogr')
                        if layer.featureCount() == 0:
                            continue
                    
                    if format == 'pliki GeoPackage (*.gpkg);':
                        layer = QgsVectorLayer(file, layerName + numerWarstwy, 'ogr')
                        if geomType == 'Polygon':
                            layer = processing.run("native:multiparttosingleparts", {'INPUT': layer, 'OUTPUT': 'memory:'})['OUTPUT']
                    
                    # sprawdzenie czy wczytywany APP jest zgodny z rodzajem zbioru w ustawieniach
                    if layerName == 'AktPlanowaniaPrzestrzennego' and 'typPlanu' in [field.name() for field in layer.fields()]:
                        for feature in layer.getFeatures():
                            typPlanu_value = feature.attribute('typPlanu')
                            if typPlanu_value not in (NULL, None, '') and not utils.validate_typPlanu(typPlanu_value=str(typPlanu_value), rodzajZbioru_value=rodzajZbioru, showMessage=False):
                                showPopup("Wczytaj warstwę", 'Wczytywane dane nie są zgodne z rodzajem zbioru "%s" wybranym w ustawieniach wtyczki APP.\n\nAtrybut typPlanu wczytywanych danych ma wartość:\n"%s"\n\nZmień rodzaj zbioru w ustawieniach wtyczki APP i ponownie wczytaj dane.' % (rodzajZbioru, typPlanu_value))
                                return
                    
                    if geomType != 'NoGeometry':
                        try:
                            newEPSG = layer.crs().authid().split(":")[1]
                        except:
                            return
                        
                        # czy warstwa posiada atrybut przestrzenNazw
                        if not 'przestrzenNazw' in [field.name() for field in layer.fields()]:
                            showPopup("Wczytaj warstwę",f"Warstwa \"{layerName}\" nie posiada atrybutu przestrzenNazw.")
                            continue
                        
                        checkvalidity = processing.run("qgis:checkvalidity", {
                            'INPUT_LAYER': layer,
                            'METHOD': 2, # GEOS
                            'INVALID_OUTPUT': 'memory:',
                            'ERROR_OUTPUT': 'memory:'
                        })
                        if checkvalidity['INVALID_OUTPUT'].featureCount() > 0:
                            showPopup("Wczytaj warstwę",f"Warstwa \"{layerName}\" posiada co najmniej jeden obiekt z błędną geometrią.\nNastąpi próba wczytania warstwy.")
                            self.kontrolaGeometriiWarstwy(layer)
                            # continue
                        
                        isLayerInPoland(layer, layerName)
                        
                        newEPSG = str(layer.crs().authid().split(":")[-1])
                        
                        if str(epsg_code) != newEPSG:
                            odp = QMessageBox.question(None,'Wczytanie warstwy do edycji',
                                                         "Układ współrzędnych wczytywanej warstwy jest inny od układu współrzędnych przyjętego na podstawie ustawień wtyczki APP.\nCzy chcesz mimo to wczytać warstwę?", QMessageBox.Yes |
                                                         QMessageBox.No, QMessageBox.No)
                            if odp == QMessageBox.No:
                                return
                            else:
                                geomTypeEPSG = geomTypeEPSG[:-4] + newEPSG
                                epsg_code = newEPSG
                        else:
                            if not isJPTinLayer_msg and not isJPTinLayer(layer, jpt):
                                showPopup("Wczytaj warstwę",f"Warstwa \"{layerName}\" posiada co najmniej jeden obiekt z JPT niezgodnym z ustawieniami.")
                                isJPTinLayer_msg = True
                    
                    destlayer = QgsVectorLayer(geomTypeEPSG + self.fieldsDefinition(fields=fields), layerName + numerWarstwy, 'memory')
                    destlayer.startEditing()
                    poczatekKoniecWersjiObiektu_msg = False
                    obowiazujeOdDo_msg = False
                    for feature in layer.getFeatures():
                        new_feat = QgsFeature(destlayer.fields())
                        for index, field in enumerate(destlayer.fields()):
                            if field.name() == 'wersjaId' and layerName == 'DokumentFormalny':
                                continue
                            if field.name() == 'zmienianyPlan' and layerName == 'AktPlanowaniaPrzestrzennego':
                                continue
                            if field.name() in ('profilPodstawowy','profilDodatkowy','tytulAlternatywny') and feature.attribute(field.name()) != NULL and format != 'pliki GeoPackage (*.gpkg);':
                                wartosci = feature.attribute(field.name())
                                if field.name() in ('profilPodstawowy','profilDodatkowy'):
                                    wartosci, czy_poprawiono_profil = popraw_wartosci_profili(
                                        wartosci,
                                        feature,
                                        field.name()
                                    )
                                    
                                    if field.name() == 'profilPodstawowy' and not 'teren ogrodów działkowych' in wartosci:
                                        if wartosci[-1] == 'teren infrastruktury technicznej':
                                            wartosci.insert(-1, 'teren ogrodów działkowych')
                                        elif wartosci[-1] == 'teren komunikacji':
                                            wartosci.append('teren ogrodów działkowych')
                                        new_feat.setAttribute('wersjaId', dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                        new_feat.setAttribute('poczatekWersjiObiektu', dataCzasTeraz)
                                        new_feat.setAttribute('obowiazujeOd', None)
                                        new_feat.setAttribute('edycja', True)
                                        if not profile_msg:
                                            profile_msg = True
                                            showPopup("Wczytaj warstwę","Podczas wczytywania warstw, zgodnie ze zmianą rozporządzenia zmienił się profil funkcjonalny w strefach planistycznych związany z terenami ogrodów działkowych.")
                                    if field.name() == 'profilPodstawowy' and 'teren ogrodów działkowych' in wartosci:
                                        # Odwrotna mapa: opis → kod
                                        opis_na_kod = {v: k for k, v in dictionaries.klasaPrzeznaczeniaTerenuKod.items()}
                                        
                                        # Kody z wejściowej listy
                                        kody_wejsciowe = [opis_na_kod[o] for o in wartosci if o in opis_na_kod]
                                        liczba_kodow_wejsciowych = len(kody_wejsciowe)
                                        
                                        # Znajdź pasujący symbol strefy
                                        dopasowany_symbol = None
                                        for symbol, lista_kolejnosci in dictionaries.mapaSymbolProfilPodstawowy.items():
                                            liczba_lista_kolejnosci = len(lista_kolejnosci)
                                            if all(kod in lista_kolejnosci for kod in kody_wejsciowe) and liczba_lista_kolejnosci == liczba_kodow_wejsciowych:
                                                dopasowany_symbol = symbol
                                                break
                                            
                                        # Jeśli nie znaleziono – zwróć oryginał
                                        if not dopasowany_symbol:
                                            if not profile_podstawowe_msg:
                                                profile_podstawowe_msg = True
                                                showPopup("Wczytaj warstwę","Podczas wczytywania warstwy stref planistycznych, został poprawiony profil podstawowy zgodnie z rozporządzeniem.")
                                            dopasowany_symbol = feature.attribute("symbol")
                                        
                                        # Posortuj według tego symbolu
                                        wartosci = [
                                            dictionaries.klasaPrzeznaczeniaTerenuKod[kod]
                                            for kod in dictionaries.mapaSymbolProfilPodstawowy[dopasowany_symbol]
                                        ]
                                    
                                    if field.name() == 'profilDodatkowy' and 'teren ogrodów działkowych' in wartosci:
                                        wartosci.remove('teren ogrodów działkowych')
                                        new_feat.setAttribute('wersjaId', dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                        new_feat.setAttribute('poczatekWersjiObiektu', dataCzasTeraz)
                                        new_feat.setAttribute('obowiazujeOd', None)
                                        new_feat.setAttribute('edycja', True)
                                        if not profile_msg:
                                            profile_msg = True
                                            showPopup("Wczytaj warstwę","Podczas wczytywania warstw, zgodnie ze zmianą rozporządzenia zmienił się profil funkcjonalny w strefach planistycznych związany z terenami ogrodów działkowych.")
                                if isinstance(wartosci, list):
                                    tekst = ",".join(map(str, wartosci))
                                else:
                                    tekst = str(wartosci)
                                new_feat.setAttribute(index, QVariant(tekst))
                            
                            elif field.name() in ('profilPodstawowy','profilDodatkowy') and feature.attribute(field.name()) != NULL and format == 'pliki GeoPackage (*.gpkg);':
                                wartosci = feature.attribute(field.name()).split(",")
                                wartosci, czy_poprawiono_profil = popraw_wartosci_profili(
                                    wartosci,
                                    feature,
                                    field.name()
                                )
                                
                                if field.name() == 'profilPodstawowy' and not 'teren ogrodów działkowych' in wartosci:
                                    if wartosci[-1] == 'teren infrastruktury technicznej':
                                        wartosci.insert(-1, 'teren ogrodów działkowych')
                                    elif wartosci[-1] == 'teren komunikacji':
                                        wartosci.append('teren ogrodów działkowych')
                                    new_feat.setAttribute('wersjaId', dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                    new_feat.setAttribute('poczatekWersjiObiektu', dataCzasTeraz)
                                    new_feat.setAttribute('obowiazujeOd', None)
                                    new_feat.setAttribute('profilPodstawowy', ",".join(wartosci))
                                    new_feat.setAttribute('edycja', True)
                                    if not profile_msg:
                                        profile_msg = True
                                        showPopup("Wczytaj warstwę","Podczas wczytywania warstw, zgodnie ze zmianą rozporządzenia zmienił się profil funkcjonalny w strefach planistycznych związany z terenami ogrodów działkowych.")
                                elif field.name() == 'profilDodatkowy' and 'teren ogrodów działkowych' in wartosci:
                                    wartosci.remove('teren ogrodów działkowych')
                                    new_feat.setAttribute('wersjaId', dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                    new_feat.setAttribute('poczatekWersjiObiektu', dataCzasTeraz)
                                    new_feat.setAttribute('obowiazujeOd', None)
                                    new_feat.setAttribute('profilDodatkowy', ",".join(wartosci))
                                    new_feat.setAttribute('edycja', True)
                                    if not profile_msg:
                                        profile_msg = True
                                        showPopup("Wczytaj warstwę","Podczas wczytywania warstw, zgodnie ze zmianą rozporządzenia zmienił się profil funkcjonalny w strefach planistycznych związany z terenami ogrodów działkowych.")
                                else:
                                    tekst = feature.attribute(field.name())
                                    new_feat.setAttribute(index, QVariant(tekst))
                            else:
                                try:
                                    if not (field.name() == 'edycja' and profile_msg):
                                        if format == 'pliki GeoPackage (*.gpkg);' and field.name() in ['poczatekWersjiObiektu','koniecWersjiObiektu'] and not feature.fields().field(feature.fieldNameIndex(field.name())).typeName() in ['datetime','DateTime']:
                                            if not poczatekKoniecWersjiObiektu_msg:
                                                field_type = feature.fields().field(feature.fieldNameIndex(field.name())).typeName()
                                                showPopup("Wczytaj warstwę",f"Atrybut {field.name()} jest typu {field_type} a powinien być typu DateTime.")
                                                poczatekKoniecWersjiObiektu_msg = True
                                        else:
                                            new_feat.setAttribute(index, QVariant(feature.attribute(field.name())))
                                except Exception as e:
                                    print(e)
                            if layerName == 'AktPlanowaniaPrzestrzennego' and profile_msg and field.name() == 'obowiazujeOd':
                                new_feat.setAttribute('wersjaId', dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                new_feat.setAttribute('poczatekWersjiObiektu', dataCzasTeraz)
                                new_feat.setAttribute('obowiazujeOd', None)
                        
                        new_feat.setGeometry(feature.geometry())
                        destlayer.addFeature(new_feat)
                        destlayer.updateFeature(new_feat)
                    destlayer.commitChanges()
                    
                    if (poczatekKoniecWersjiObiektu_msg or obowiazujeOdDo_msg) and format == 'pliki GML (*.gml)':
                        continue
                    
                    output_path = str(pathlib.Path(str(defaultPath + '/' + layerName + numerWarstwy + '.gpkg')))
                    options = QgsVectorFileWriter.SaveVectorOptions()
                    options.driverName = 'GPKG'
                    options.layerName = layerName + numerWarstwy
                    options.fileEncoding = 'UTF-8'
                    epsg = 'EPSG:' + str(epsg_code)
                    options.destCRS = QgsCoordinateReferenceSystem(epsg)
                    crs = QgsCoordinateReferenceSystem(epsg)
                    if layerName in ['DokumentFormalny','RysunekAktuPlanowaniaPrzestrzennego']:
                        options.overrideGeometryType = QgsWkbTypes.NoGeometry
                    elif layerName in ['AktPlanowaniaPrzestrzennego']:
                        options.overrideGeometryType = QgsWkbTypes.MultiPolygon
                    else:
                        options.overrideGeometryType = QgsWkbTypes.Polygon
                    try:
                        error =  QgsVectorFileWriter.writeAsVectorFormatV3(destlayer, output_path, QgsCoordinateTransformContext(), options)
                    except:
                        self.iface.messageBar().pushCritical("Wczytanie warstwy:","Wystąpił błąd podczas wczytania warstwy.")
                        showPopup("Wczytaj warstwę","Wystąpił błąd podczas wczytania warstwy " + layerName + ": " + error[1])
                    
                    QgsProject.instance().removeMapLayer(destlayer)
                    QgsProject.instance().removeMapLayer(layer)
                    
                    # Usunięcie pomocniczego GFS po zakończeniu odczytu GML.
                    # Plik nie może pozostać obok GML, ponieważ przy późniejszym
                    # drag & drop QGIS/OGR odczyta z niego również klasy niewystępujące
                    # w danym rodzaju aktu.
                    if format == 'pliki GML (*.gml)':
                        if os.path.exists(gfsfile):
                            os.remove(gfsfile)
                    
                    if analizy and 'StrefaPlanistyczna' in layerName:
                        ileRazyPowielicWarstwe = 6
                    elif analizy and 'ObszarStandardowDostepnosciInfrastrukturySpolecznej' in layerName:
                        ileRazyPowielicWarstwe = 2
                    else:
                        ileRazyPowielicWarstwe = 1
                    
                    for n in range(ileRazyPowielicWarstwe):
                        gkpg = QgsVectorLayer(output_path, layerName + numerWarstwy, 'ogr')
                        
                        if not analizy:
                            if rodzajZbioru != 'POG' and layerName == 'AktPlanowaniaPrzestrzennego':
                                layer_QML_Name = 'granice_app'
                            else:
                                layer_QML_Name = layerName
                        elif layerName in ['StrefaPlanistyczna',
                                           'ObszarStandardowDostepnosciInfrastrukturySpolecznej',
                                           'ObszarUzupelnieniaZabudowy',
                                           'ObszarZabudowySrodmiejskiej'] and rodzajZbioru == 'POG':
                            if layerName == 'StrefaPlanistyczna':
                                layer_QML_Name = 'SPL_' + subNamesSPL[n]
                            if layerName == 'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                                layer_QML_Name = 'OSD_' + subNamesOSD[n]
                            if layerName == 'ObszarUzupelnieniaZabudowy':
                                layer_QML_Name = 'OUZ_' + subNamesOUZ[n]
                            if layerName == 'ObszarZabudowySrodmiejskiej':
                                layer_QML_Name = 'OZS_' + subNamesOZS[n]
                            gkpg.setName(layer_QML_Name)
                        else:
                            layer_QML_Name = layerName
                        
                        pathQML = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/QML/" + layer_QML_Name + ".qml")
                        gkpg.startEditing()
                        gkpg.loadNamedStyle(str(pathQML))
                        if activeDlgname not in ['PytanieAppDialog', 'PytanieAppUniewaznienieDialog']:
                            gkpg.startEditing()
                        else:
                            gkpg.commitChanges()
                        
                        editFormConfig = gkpg.editFormConfig()
                        pathUI = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".ui")
                        editFormConfig.setUiForm(str(pathUI))
                        pathPy = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + layerName + ".py")
                        editFormConfig.setInitFilePath(str(pathPy))
                        editFormConfig.setInitFunction("my_form_open")
                        gkpg.setEditFormConfig(editFormConfig)
                        gkpg.setCrs(crs)
                        
                        QgsProject.instance().addMapLayer(gkpg)
                        
                        if analizy:
                            if layerName == 'StrefaPlanistyczna' and not subNamesSPL[n] == 'profileDodatkowe':
                                self.dodajStylOpartyORegulach(gkpg, subNamesSPL[n])
                            if layerName == 'ObszarStandardowDostepnosciInfrastrukturySpolecznej':
                                self.dodajStylOpartyORegulach(gkpg, subNamesOSD[n])
                            if layerName == 'ObszarUzupelnieniaZabudowy':
                                self.dodajStylOpartyORegulach(gkpg, subNamesOUZ[n])
                            if layerName == 'ObszarZabudowySrodmiejskiej':
                                self.dodajStylOpartyORegulach(gkpg, subNamesOZS[n])
                    if activeDlgname not in ['PytanieAppDialog', 'PytanieAppUniewaznienieDialog']:
                        self.activeDlg.layers_comboBox.setCurrentText(layerName)
                    self.iface.messageBar().pushSuccess("Wczytanie warstwy:","Wczytano warstwę.")
                    
                    def on_geometry_changed(fid, geom, warstwa_tmp):
                        """Obsługuje zmianę geometrii obiektu i aktualizuje zależne dane."""
                        changed_feature = warstwa_tmp.getFeature(fid)
                        dataCzasTeraz = QDateTime.currentDateTimeUtc()
                        try:
                            changed_feature.setAttribute("wersjaId", dataCzasTeraz.toString("yyyyMMddThhmmss"))
                            changed_feature.setAttribute("poczatekWersjiObiektu", dataCzasTeraz)
                            changed_feature.setAttribute("edycja", True)
                        except Exception as e:
                            print(e)
                        warstwa_tmp.updateFeature(changed_feature)
                    
                    gkpg.geometryChanged.connect(lambda fid, geom, lyr=gkpg: on_geometry_changed(fid, geom, lyr))
                    showPopup("Wczytaj warstwę","Poprawnie wczytano warstwę " + layerName + ".")
                    
            if raport_poprawionych_profili or raport_nierozpoznanych_profili:
                komunikat = []
                
                if raport_poprawionych_profili:
                    komunikat.append(
                        "Automatycznie poprawiono wartości profili:"
                    )
                    
                    for (
                        oznaczenie,
                        nazwa_pola,
                        wartosc_pierwotna,
                        wartosc_poprawiona
                    ) in raport_poprawionych_profili:
                        komunikat.append(
                            f'• {oznaczenie}, {nazwa_pola}: '
                            f'"{wartosc_pierwotna}" → "{wartosc_poprawiona}"'
                        )
                        
                if raport_nierozpoznanych_profili:
                    if komunikat:
                        komunikat.append("")
                        
                    komunikat.append(
                        "Nie poprawiono automatycznie wartości "
                        "niejednoznacznych:"
                    )
                    
                    for (
                        oznaczenie,
                        nazwa_pola,
                        wartosc_pierwotna
                    ) in raport_nierozpoznanych_profili:
                        komunikat.append(
                            f'• {oznaczenie}, {nazwa_pola}: '
                            f'"{wartosc_pierwotna}"'
                        )
                        
                showPopup(
                    "Wczytaj warstwę",
                    "\n".join(komunikat)
                )
        finally:
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()


    def saveLayerToGML(self, fileName=None):
        """Zapisuje dane obsługiwane przez operację `saveLayerToGML`."""
        s = QgsSettings()
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        
        namespace_map = {'wfs': 'http://www.opengis.net/wfs/2.0',
                         'app': 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0',
                         'gml': 'http://www.opengis.net/gml/3.2',
                         'xlink':'http://www.w3.org/1999/xlink'}
        
        if self.activeDlg == self.wektorInstrukcjaDialogPOG:
            self.obrysLayer = self.wektorInstrukcjaDialogPOG.layers_comboBox.currentLayer()
        if self.activeDlg == self.wektorInstrukcjaDialogSPL:
            self.obrysLayer = self.wektorInstrukcjaDialogSPL.layers_comboBox.currentLayer()
        elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
            self.obrysLayer = self.wektorInstrukcjaDialogOUZ.layers_comboBox.currentLayer()
        elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
            self.obrysLayer = self.wektorInstrukcjaDialogOZS.layers_comboBox.currentLayer()
        elif self.activeDlg == self.wektorInstrukcjaDialogOSD:
            self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
        elif self.activeDlg == self.formularzInstrukcjaDialogPOGpoUniewaznieniu:
            nazwa_warstwy = os.path.splitext(fileName)[0]
            self.obrysLayer = None
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name().startswith(nazwa_warstwy):
                    self.obrysLayer = layer
                    break
        elif isinstance(self.activeDlg, TworzenieOUZDialog):
            self.obrysLayer = layer_OUZ
        if self.obrysLayer == None:
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy do zapisu.")
            return
        
        name_list = ["AktPlanowaniaPrzestrzennego",
                     "dokument_formalny",
                     "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
                     "ObszarUzupelnieniaZabudowy",
                     "ObszarZabudowySrodmiejskiej",
                     "rysunek_aktu_planowania_przestrzennego",
                     "StrefaPlanistyczna"]
        
        layerName = None
        
        for name in name_list:
            if name in self.obrysLayer.name():
                layerName = name
                break
        
        if layerName == None:
            showPopup("Błąd warstwy obrysu", "Niepoprawna nazwa warstwy: " + self.obrysLayer.name())
            return
        
        if not isinstance(self.activeDlg, TworzenieOUZDialog):
            showPopup("Zapisz warstwę","Zostaną teraz przeprowadzone kontrole warstwy " + layerName + ". Może to potrwać do kilku minut.")
            czyWynikKontroliPozytywny = True
            czyGeometrieSaPoprawne = True
            
            if not self.kontrolaWarstwy(self.obrysLayer):
                czyWynikKontroliPozytywny = False
            if not self.kontrolaGeometriiWarstwy(self.obrysLayer):
                czyWynikKontroliPozytywny = False
                czyGeometrieSaPoprawne = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.czyObiektyUnikalne(self.obrysLayer,'oznaczenie'):
                czyWynikKontroliPozytywny = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.czyObiektyUnikalne(self.obrysLayer,'status'):
                czyWynikKontroliPozytywny = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.czyObiektyUnikalne(self.obrysLayer,'lokalnyId'):
                czyWynikKontroliPozytywny = False
            if self.activeDlg == self.wektorInstrukcjaDialogOUZ and czyGeometrieSaPoprawne and self.OUZpowyzej125procent(self.obrysLayer, fileName):
                czyWynikKontroliPozytywny = False
            
            if not czyWynikKontroliPozytywny:
                return
        
        if isinstance(self.activeDlg, TworzenieOUZDialog):
            plikGML = defaultPath + "/Dokumentacja/ObszarUzupelnieniaZabudowy-wyjsciowy.gml"
        else:
            if fileName:
                plikGML = defaultPath + "/" + fileName
            else:
                self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="pliki GML (*.gml)")[0]
                plikGML = str(self.fn)
        
        if plikGML:
            templateXML = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/templates/" + layerName + ".xml"
            templateFeatureCollection = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/templates/FeatureCollection.xml"
            
            with open(str(templateFeatureCollection), 'r') as input_file: xmlMain = input_file.read()
            with open(str(templateXML), 'r') as input_file: templateXML = input_file.read()
            
            ET.register_namespace('wfs', 'http://www.opengis.net/wfs/2.0')
            ET.register_namespace('app', 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0')
            ET.register_namespace('gml', 'http://www.opengis.net/gml/3.2')
            ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
            ET.register_namespace('gco', 'http://www.isotc211.org/2005/gco')
            ET.register_namespace('gmd', 'http://www.isotc211.org/2005/gmd')
            
            tree = ET.ElementTree(ET.fromstring(xmlMain))  # nosec B314
            timeStamp = tree.find('[@timeStamp]', namespaces=namespace_map)
            numberReturned = tree.find('[@numberReturned]', namespaces=namespace_map)
            timeStamp.attrib['timeStamp'] = str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")+'Z')
            numberReturned.attrib['numberReturned'] = str(self.obrysLayer.featureCount())
            root = tree.getroot()
            
            attrs2Dic = {'charakterUstalenia':dictionaries.charakterUstaleniaListaKodowa,
                         'nazwa':dictionaries.nazwaListaKodowa,
                         'status':dictionaries.statusListaKodowa,
                         'typPlanu':dictionaries.typyPlanuListaKodowa,
                         'poziomHierarchii':dictionaries.poziomyHierarchii,
                         'profilPodstawowy':dictionaries.profilPodstawowyLubDodatkowyListaKodowa,
                         'profilDodatkowy':dictionaries.profilPodstawowyLubDodatkowyListaKodowa}
            
            crs_authid = self.obrysLayer.crs().authid()
            epsg_code = int(crs_authid.split(':')[1])
            
            wynik = processing.run("native:swapxy", {
                'INPUT': self.obrysLayer,
                'OUTPUT': 'memory:'
            })
            
            if layerName != 'AktPlanowaniaPrzestrzennego':
                wynik = processing.run("native:multiparttosingleparts", {
                    'INPUT': wynik['OUTPUT'],
                    'OUTPUT': 'memory:'
                })
            
            for obj in wynik['OUTPUT'].getFeatures():
                member = ET.fromstring(templateXML)  # nosec B314
                przestrzenNazw = ''
                lokalnyId = ''
                wersjaId = ''
                elementyDoUsuniecia = []
                
                geom = member.find('.//app:geometria', namespaces=namespace_map)
                geomAPP = member.find('.//app:zasiegPrzestrzenny', namespaces=namespace_map)
                if geom != None or geomAPP != None:
                    geomWkt = obj.geometry().asWkt()
                    options = ['FORMAT=GML3']
                    geometryWkt = ogr.CreateGeometryFromWkt(geomWkt)
                    
                    if geometryWkt.GetGeometryType() == 3:
                        geometriaGML = str(geometryWkt.ExportToGML(options=options)).replace("<gml:Polygon>",f'<gml:Polygon srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/{epsg_code}" xmlns:gml="http://www.opengis.net/gml/3.2">')
                    elif geometryWkt.GetGeometryType() == 6:
                        geometriaGML = str(geometryWkt.ExportToGML(options=options)).replace("<gml:MultiSurface>",f'<gml:MultiSurface srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/{epsg_code}" xmlns:gml="http://www.opengis.net/gml/3.2">')
                    
                    if geom != None:
                        geom.append(ET.fromstring(geometriaGML))  # nosec B314
                    elif geomAPP != None:
                        geomAPP.append(ET.fromstring(geometriaGML))  # nosec B314
                for attr in obj.fields():
                    attr_name = attr.name()
                    attr_value = str(obj.attribute(attr_name))
                    if attr_name == 'przestrzenNazw':
                        przestrzenNazw = attr_value
                    elif attr_name == 'lokalnyId':
                        lokalnyId = attr_value
                    elif attr_name == 'wersjaId':
                        wersjaId = attr_value
                    if przestrzenNazw != '' and lokalnyId != '' and wersjaId != '':
                        layerMember = member.find('.//app:' + layerName + '[@gml:id]', namespaces=namespace_map)
                        layerMember.attrib['{http://www.opengis.net/gml/3.2}id'] = przestrzenNazw.replace("/","_") + "_" + lokalnyId + "_" + wersjaId
                        element = member.find('.//gml:identifier', namespaces=namespace_map)
                        element.text = "https://www.gov.pl/zagospodarowanieprzestrzenne/app/" + layerName + "/" + przestrzenNazw + "/" + lokalnyId + "/" + wersjaId
                    atrybutTitle = member.find('.//app:' + attr.name() + '[@xlink:title]', namespaces=namespace_map)
                    atrybutHref = member.find('.//app:' + attr.name() + '[@xlink:href]', namespaces=namespace_map)
                    if atrybutTitle != None and atrybutHref != None and attr.name() not in ('profilPodstawowy','profilDodatkowy','tytulAlternatywny'):
                        atrybutTitle.attrib['{http://www.w3.org/1999/xlink}title'] = str(obj.attribute(attr.name()))
                        atrybutHref.attrib['{http://www.w3.org/1999/xlink}href'] = attrs2Dic[attr.name()][str(obj.attribute(attr.name()))]
                    elif atrybutTitle == None and atrybutHref != None and attr.name() not in ('plan'):
                        atrybutHref.attrib['{http://www.w3.org/1999/xlink}href'] = attrs2Dic[attr.name()][str(obj.attribute(attr.name()))]
                    elif atrybutTitle == None and atrybutHref != None and attr.name() in ('plan'):
                        if obj.attribute(attr.name()) == NULL:
                            atrybutHref.attrib['{http://www.w3.org/1999/xlink}href'] = ''
                        else:
                            atrybutHref.attrib['{http://www.w3.org/1999/xlink}href'] = str(obj.attribute(attr.name()))
                    elif attr.name() == 'profilPodstawowy':
                        profile = str(obj.attribute(attr.name()))
                        profileLista = profile.split(",")
                        liczbaWystapienProfiluPodstawowego = 0
                        element = member.find('.//app:' + attr.name(), namespaces=namespace_map)
                        for profil in profileLista:
                            if attr.name() == 'profilPodstawowy' and liczbaWystapienProfiluPodstawowego == 0:
                                liczbaWystapienProfiluPodstawowego += 1
                                element.set('{http://www.w3.org/1999/xlink}href', dictionaries.profilPodstawowyLubDodatkowyListaKodowa[profil])
                                element.set('{http://www.w3.org/1999/xlink}title', profil)
                            elif attr.name() == 'profilPodstawowy' and liczbaWystapienProfiluPodstawowego > 0:
                                new_element = ET.Element('app:profilPodstawowy')
                                new_element.attrib['{http://www.w3.org/1999/xlink}href'] = dictionaries.profilPodstawowyLubDodatkowyListaKodowa[profil]
                                new_element.attrib['{http://www.w3.org/1999/xlink}title'] = profil
                                layerMember.insert(14 + liczbaWystapienProfiluPodstawowego, new_element)
                                liczbaWystapienProfiluPodstawowego += 1
                    elif attr.name() == 'profilDodatkowy':
                        profile = str(obj.attribute(attr.name()))
                        profileLista = profile.split(",")
                        liczbaWystapienProfiluDodatkowego = 0
                        element = member.find('.//app:' + attr.name(), namespaces=namespace_map)
                        for profil in profileLista:
                            if attr.name() == 'profilDodatkowy' and liczbaWystapienProfiluDodatkowego == 0:
                                if profil != 'NULL' and profil != '':
                                    liczbaWystapienProfiluDodatkowego += 1
                                    element.set('{http://www.w3.org/1999/xlink}href', dictionaries.profilPodstawowyLubDodatkowyListaKodowa[profil])
                                    element.set('{http://www.w3.org/1999/xlink}title', profil)
                                else:
                                    elementyDoUsuniecia.append(element)
                            elif attr.name() == 'profilDodatkowy' and liczbaWystapienProfiluDodatkowego > 0:
                                liczbaWystapienProfiluDodatkowego += 1
                                new_element = ET.Element('app:profilDodatkowy')
                                new_element.attrib['{http://www.w3.org/1999/xlink}href'] = dictionaries.profilPodstawowyLubDodatkowyListaKodowa[profil]
                                new_element.attrib['{http://www.w3.org/1999/xlink}title'] = profil
                                layerMember.insert(13 + liczbaWystapienProfiluPodstawowego + liczbaWystapienProfiluDodatkowego, new_element)
                    elif attr.name() == 'tytulAlternatywny':
                        tytulyAlternatywne = str(obj.attribute(attr.name()))
                        tytulyAlternatywneLista = tytulyAlternatywne.split(",")
                        liczbaWystapienTytulyAlternatywne = 0
                        
                        if tytulyAlternatywneLista != ['NULL'] and tytulyAlternatywneLista != ['']:
                            for tytulAlternatywny in tytulyAlternatywneLista:
                                element = member.find('.//app:' + attr.name(), namespaces=namespace_map)
                                
                                if liczbaWystapienTytulyAlternatywne == 0:
                                    liczbaWystapienTytulyAlternatywne += 1
                                    element.text = tytulAlternatywny
                                elif liczbaWystapienTytulyAlternatywne > 0:
                                    liczbaWystapienTytulyAlternatywne += 1
                                    new_element = ET.Element('app:tytulAlternatywny')
                                    new_element.text = tytulAlternatywny
                                    layerMember.insert(4 + liczbaWystapienTytulyAlternatywne, new_element)
                        else:
                            element = member.find('.//app:' + attr.name(), namespaces=namespace_map)
                            elementyDoUsuniecia.append(element)
                    else:
                        element = member.find('.//app:' + attr.name(), namespaces=namespace_map)
                        if element != None:
                            if str(obj.attribute(attr.name())) == 'NULL' or str(obj.attribute(attr.name())) == '':
                                elementyDoUsuniecia.append(element)
                            elif attr.name() == 'poczatekWersjiObiektu' or attr.name() == 'koniecWersjiObiektu':
                                try:
                                    element.text = obj.attribute(attr.name()).toString("yyyy-MM-ddTHH:mm:ss") + "Z"
                                except:
                                    element.text = obj.attribute(attr.name())
                            elif attr.name() == 'obowiazujeOd' or attr.name() == 'obowiazujeDo':
                                try:
                                    element.text = obj.attribute(attr.name()).toString("yyyy-MM-dd")
                                except:
                                    element.text = obj.attribute(attr.name())
                            elif attr.name() == 'wylaczenieZabudowyZagrodowej' or 'modyfikacja':
                                element.text = str(obj.attribute(attr.name())).replace("True","true").replace("False","false")
                            else:
                                element.text = str(obj.attribute(attr.name()))
                
                for el2del in elementyDoUsuniecia:
                    layerMember.remove(el2del)
                
                root.append(copy.deepcopy(member))
            
            ET.indent(tree, space="    ", level=0)
            tree.write(plikGML, encoding='utf-8', xml_declaration=True)
            
            if self.activeDlg == self.wektorInstrukcjaDialogPOG:
                self.POG_GML_saved = True
            if self.activeDlg == self.wektorInstrukcjaDialogSPL:
                self.SPL_GML_saved = True
            elif self.activeDlg == self.wektorInstrukcjaDialogOUZ:
                self.OUZ_GML_saved = True
            elif self.activeDlg == self.wektorInstrukcjaDialogOZS:
                self.OZS_GML_saved = True
            elif self.activeDlg == self.wektorInstrukcjaDialogOSD:
                self.OSD_GML_saved = True
            
            if not isinstance(self.activeDlg, TworzenieOUZDialog):
                self.iface.messageBar().pushSuccess("Zapisanie warstwy:","Zapisano warstwę do formatu GML.")
                showPopup("Zapisz warstwę","Poprawnie zapisano warstwę " + layerName + " do formatu GML.")


    def saveLayerToGML_OUZ(self, layer):
        """Zapisuje dane obsługiwane przez operację `saveLayerToGML_OUZ`."""
        global layer_OUZ
        layer_OUZ = layer
        self.saveLayerToGML()


    def update_layer_list(self, obj):
        """Aktualizuje dane obsługiwane przez operację `update_layer_list`."""
        layers = QgsProject.instance().mapLayers()
        expected_layers = []
        
        for layer in layers.values():
            if not layer.name().startswith(obj.name):
                expected_layers.append(layer)
        
        obj.layers_comboBox.setExceptedLayerList(expected_layers)
        if obj.layers_comboBox.currentIndex() == 0:
            obj.layers_comboBox.setCurrentIndex(1)


    def kontrolaGeometriiWarstwy(self, obrysLayer):
        """Wykonuje kontrolę danych w ramach operacji `kontrolaGeometriiWarstwy`."""
        czyGeometrieSaPoprawne = True
        obrysLayerName = obrysLayer.name()
        
        try:
            warstwaBezKoniecWersjiObiektu = processing.run("native:extractbyexpression", {
                'INPUT':obrysLayer,
                'EXPRESSION':'koniecWersjiObiektu is NULL',
                'OUTPUT':'memory:'})
            obrysLayer = warstwaBezKoniecWersjiObiektu['OUTPUT']
        except Exception as e:
            print(e)
        
        if obrysLayer.featureCount() > 0:
            if not self.kontrolaPoprawnosciGeometrii(obrysLayer):
                return False
            
            # usuwanie pustych geometrii
            removenullgeometries = processing.run("native:removenullgeometries", {
                'INPUT': obrysLayer,
                'REMOVE_EMPTY': True,
                'OUTPUT': 'memory:',
                'NULL_OUTPUT': 'memory:'
            })
            
            if obrysLayer.featureCount()-removenullgeometries['OUTPUT'].featureCount() > 0:
                showPopup("Błąd warstwy obrysu", "Obrys posiada obiekty bez geometrii. Utworzono warstwę 'Obiekty bez geometrii'.")
                removenullgeometries['NULL_OUTPUT'].setName("Obiekty bez geometrii")
                QgsProject.instance().addMapLayer(removenullgeometries['NULL_OUTPUT'])
            obrysLayer = removenullgeometries['OUTPUT']
            
            # Sprawdzanie CRS warstwy wejściowej
            authid = str(obrysLayer.crs().authid())
            if authid == '':
                showPopup("Błąd warstwy obrysu", "Obrys nie ma zdefiniowanego układu współrzędnych")
                czyGeometrieSaPoprawne = False
                return False
            epsg = authid.split(':')[1]
            srsName = ''
            # Układ współrzędnych
            for crs in dictionaries.ukladyOdniesieniaPrzestrzennego.values():
                if epsg in crs:
                    srsName = crs
                    break
            
            # Kontrola układu współrzędnych
            if srsName == '':
                showPopup("Błąd warstwy obrysu",
                          "Obrys posiada niezgodny układ współrzędnych - EPSG:%s.\nDostępne CRS:\n    - %s" % (epsg, ',\n    - '.join(['%s : %s' % (a, b) for a, b in zip(dictionaries.ukladyOdniesieniaPrzestrzennego.keys(), dictionaries.ukladyOdniesieniaPrzestrzennego.values())])))
                czyGeometrieSaPoprawne = False
            
            # Czy geometria wychodzi poza granicę Polski
            if not isLayerInPoland(obrysLayer, obrysLayerName):
                czyGeometrieSaPoprawne = False
            
            # Kontrole obiektów innych niż POG
            if self.activeDlg not in (self.wektorInstrukcjaDialogPOG, self.formularzInstrukcjaDialogPOGpoUniewaznieniu):
                warstwaPOG = self.wektorInstrukcjaDialogPOG.layers_comboBox.currentLayer()
                
                # Czy geometria wychodzi poza POG
                if warstwaPOG != None:
                    czyGeometrieSaPoprawne = self.kontrolaWychodzeniaPozaPOG(obrysLayer, warstwaPOG, czyGeometrieSaPoprawne)
                
                # Czy strefy planistyczne posiadają dziury
                if obrysLayerName.startswith('StrefaPlanistyczna'):
                    czyGeometrieSaPoprawne = self.kontrolaDziurWSPL(obrysLayer, warstwaPOG, czyGeometrieSaPoprawne)
                
                # Czy wystepują nakładające się obiekty
                if not obrysLayerName.startswith('AktPlanowaniaPrzestrzennego'):
                    czyGeometrieSaPoprawne = self.kontrolaNakladania(obrysLayer, czyGeometrieSaPoprawne)
                
                # Czy wystepują dziury pomiędzy stykającymi się strefami i braki w dopełnieniu do POG
                if obrysLayerName.startswith('StrefaPlanistyczna') and warstwaPOG != None:
                    czyGeometrieSaPoprawne = self.kontrolaDziurSPL(obrysLayer, warstwaPOG, czyGeometrieSaPoprawne)
                
                # Czy występują obiekty o wspolnych bokach (styczne) w OUZ lub OZS
                if obrysLayerName.startswith('ObszarUzupelnieniaZabudowy') or obrysLayerName.startswith('ObszarZabudowySrodmiejskiej'):
                    czyGeometrieSaPoprawne = self.kontrolaObiektowOWspolnychBokach(obrysLayer, obrysLayerName, czyGeometrieSaPoprawne)
        else:
            showPopup("Błąd warstwy obrysu", "Brak obiektów na warstwie lub obiekty mają uzupełniony koniec wersji obiektu.")
            return False
        
        return czyGeometrieSaPoprawne


    def kontrolaPoprawnosciGeometrii(self, obrysLayer) -> bool:
        # kontrola poprawnosci geometrii
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaPoprawnosciGeometrii`."""
        for nr_metody in range(1, 3):
            bledne_geometrie = processing.run("qgis:checkvalidity", {
                'INPUT_LAYER': obrysLayer,
                'METHOD': nr_metody,
                'INVALID_OUTPUT': 'memory:',
                'ERROR_OUTPUT': 'memory:'
            })
            if bledne_geometrie['INVALID_OUTPUT'].featureCount() > 0:
                break
        
        if bledne_geometrie['ERROR_OUTPUT'].featureCount() > 0:
            bledne_geometrie['ERROR_OUTPUT'].setName("Lokalizacje błędów geometrii")
            bledne_geometrie['ERROR_OUTPUT'].startEditing()
            bledne_geometrie['ERROR_OUTPUT'].renameAttribute(bledne_geometrie['ERROR_OUTPUT'].fields().indexFromName("message"), "opis_bledu")
            
            # usuwanie błędów typu Poligon 7 leży wewnątrz poligonu 2
            for bledna_geometria in bledne_geometrie['ERROR_OUTPUT'].getFeatures():
                if re.search(r'Poligon \d+ leży wewnątrz poligonu \d+', bledna_geometria['opis_bledu'], re.IGNORECASE) or \
                   re.search(r'Polygon \d+ inside polygon \d+', bledna_geometria['opis_bledu'], re.IGNORECASE):
                    bledne_geometrie['ERROR_OUTPUT'].deleteFeature(bledna_geometria.id())
            
            bledne_geometrie['ERROR_OUTPUT'].commitChanges()
            
            if bledne_geometrie['INVALID_OUTPUT'].featureCount() > 0:
                bledne_geometrie['INVALID_OUTPUT'].setName("Błędy geometrii")
                bledne_geometrie['INVALID_OUTPUT'].startEditing()
                bledne_geometrie['INVALID_OUTPUT'].renameAttribute(bledne_geometrie['INVALID_OUTPUT'].fields().indexFromName("_errors"), "opis_bledu")
                
                # usuwanie błędów typu Poligon 7 leży wewnątrz poligonu 2
                for bledna_geometria in bledne_geometrie['INVALID_OUTPUT'].getFeatures():
                    if re.search(r'Poligon \d+ leży wewnątrz poligonu \d+', bledna_geometria['opis_bledu'], re.IGNORECASE) or \
                       re.search(r'Polygon \d+ inside polygon \d+', bledna_geometria['opis_bledu'], re.IGNORECASE):
                        bledne_geometrie['INVALID_OUTPUT'].deleteFeature(bledna_geometria.id())
                
                bledne_geometrie['INVALID_OUTPUT'].commitChanges()
                
            if bledne_geometrie['INVALID_OUTPUT'].featureCount() > 0 or bledne_geometrie['ERROR_OUTPUT'].featureCount() > 0:
                showPopup("Błąd warstwy obrysu", "Występuje niepoprawna geometria w warstwie.\nDodano warstwę z błędnymi obiektami w zakresie geometrii oraz warstwę punktową wskazującą miejsca z błędami.\nDalsza kontrola została wstrzymana z uwagi na błędy geometrii.")
                QgsProject.instance().addMapLayer(bledne_geometrie['ERROR_OUTPUT'])
                QgsProject.instance().addMapLayer(bledne_geometrie['INVALID_OUTPUT'])
                return False
        return True


    def kontrolaWychodzeniaPozaPOG(self, obrysLayer, warstwaPOG, czyGeometrieSaPoprawne) -> bool:
        # Czy geometria wychodzi poza POG
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaWychodzeniaPozaPOG`."""
        if warstwaPOG == None:
            return None
        else:
            # Sprawdzenie czy warstwa POG nie ma błędów geometrii
            checkvalidity = processing.run("qgis:checkvalidity", {
                'INPUT_LAYER': warstwaPOG,
                'METHOD': 2, # GEOS
                'INVALID_OUTPUT': 'memory:',
                'ERROR_OUTPUT': 'memory:'
            })
            if checkvalidity['INVALID_OUTPUT'].featureCount() > 0:
                showPopup("Kontrola wychodzenia poza POG",f"Warstwa POG posiada błąd geometrii. Nie jest możliwe wykonanie kontroli wychodzenia poza POG.")
                return False
            
            # Zamiana POG na linie
            POG_polygonstolines = processing.run("native:polygonstolines", {
                'INPUT': warstwaPOG,
                'OUTPUT': 'memory:'
            })
            
            bufor_POG_lines = processing.run("native:buffer", {
                'INPUT': POG_polygonstolines['OUTPUT'],
                'DISTANCE': 0.01,
                'SEGMENTS': 10,
                'DISSOLVE': True,
                'OUTPUT': 'memory:'
            })
            
            przyciecie = processing.run("native:difference", {
                'INPUT': obrysLayer,
                'OVERLAY': warstwaPOG,
                'OUTPUT': 'memory:'
            })
            
            difference = processing.run("native:difference", {
                'INPUT': przyciecie['OUTPUT'],
                'OVERLAY': bufor_POG_lines['OUTPUT'],
                'OUTPUT': 'memory:'
            })
            
            # Rozbicie multipoligon-u na poligony
            pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
                'INPUT': difference['OUTPUT'],
                'OUTPUT': 'memory:'
            })
            
            # Kasowanie obiektów wychodzących poza POG o powierzchni < 1 m2 oraz których smuklosc > 10 000
            pojedynczeObjekty['OUTPUT'].startEditing()
            for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
                geom = obj.geometry()
                if geom.area() < 1: # 1 m2
                    pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
                else:
                    smuklosc = (geom.length() ** 2) / geom.area()
                    if smuklosc > 10000:
                        pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
            pojedynczeObjekty['OUTPUT'].commitChanges(False)
            
            if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
                pojedynczeObjekty['OUTPUT'].setName("Geometrie wychodzace poza POG")
                QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
                showPopup("Błąd warstwy obrysu",
                          "Niepoprawna geometria - obiekty muszą leżeć wewnątrz POG. Dodano warstwę z geometriami wychodzącymi poza POG.")
                czyGeometrieSaPoprawne = False
        
        return czyGeometrieSaPoprawne


    def kontrolaObiektowOWspolnychBokach(self, obrysLayer, obrysLayerName, czyGeometrieSaPoprawne) -> bool:
        # Czy występują obiekty o wspolnych bokach (styczne) w OUZ lub OZS
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaObiektowOWspolnychBokach`."""
        features = list(obrysLayer.getFeatures())
        geoms = {f.id(): loads(bytes(f.geometry().asWkb())) for f in features}
        
        def get_segments(geom):
            """Zwraca segmenty składające się na analizowaną geometrię."""
            coords = list(geom.exterior.coords)
            return [LineString([coords[i], coords[i+1]]) for i in range(len(coords) - 1)]
        
        shared_edge_ids = set()
        
        for i, feat in enumerate(obrysLayer.getFeatures()):
            geom1 = feat.geometry()
            for j, other_feat in enumerate(obrysLayer.getFeatures()):
                if feat.id() == other_feat.id():
                    continue
                
                geom2 = other_feat.geometry()
                
                # Sprawdź czy geometrie się stykają
                if geom1.touches(geom2):
                    intersection = geom1.intersection(geom2)
                    
                    # Jeżeli część wspólna jest linią, to mają wspólny bok
                    if intersection and intersection.type() == QgsWkbTypes.LineGeometry:
                        shared_edge_ids.add(feat.id())
                        break  # Wystarczy jeden wspólny bok
        
        if len(shared_edge_ids) > 0:
            warstwa_wynikowa = QgsVectorLayer(f'Polygon?crs={obrysLayer.crs().authid()}', 'Obiekty o wspolnych bokach', 'memory')
            warstwa_wynikowa.dataProvider().addAttributes(obrysLayer.fields())
            warstwa_wynikowa.updateFields()
            warstwa_wynikowa.dataProvider().addFeatures([f for f in obrysLayer.getFeatures() if f.id() in shared_edge_ids])
            warstwa_wynikowa.updateExtents()
            QgsProject.instance().addMapLayer(warstwa_wynikowa)
            showPopup("Błąd warstwy obrysu",f"Niepoprawna geometria - Obiekty o wspólnych bokach w {obrysLayerName}.")
            czyGeometrieSaPoprawne = False
        
        return czyGeometrieSaPoprawne


    def kontrolaDziurSPL(self, obrysLayer, warstwaPOG, czyGeometrieSaPoprawne) -> bool:
        # Czy wystepują dziury pomiędzy stykającymi się strefami i braki w dopełnieniu do POG
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaDziurSPL`."""
        bufor0 = processing.run("native:buffer", {
            'INPUT': obrysLayer,
            'DISTANCE': 0,
            'SEGMENTS': 10,
            'DISSOLVE': True,
            'OUTPUT': 'memory:'
        })
        
        # Sprawdzenie czy warstwa POG nie ma błędów geometrii
        checkvalidity = processing.run("qgis:checkvalidity", {
            'INPUT_LAYER': warstwaPOG,
            'METHOD': 2, # GEOS
            'INVALID_OUTPUT': 'memory:',
            'ERROR_OUTPUT': 'memory:'
        })
        if checkvalidity['INVALID_OUTPUT'].featureCount() > 0:
            showPopup("Kontrola dziur w SPL",f"Warstwa POG posiada błąd geometrii. Nie jest możliwe wykonanie kontroli dziur w Strefach Planistycznych.")
            return False
        else:
            difference = processing.run("native:difference", {
                'INPUT': warstwaPOG,
                'OVERLAY': bufor0['OUTPUT'],
                'OUTPUT': 'memory:'
            })
        
            # Rozbicie multipoligon-u na poligony
            pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
                'INPUT': difference['OUTPUT'],
                'OUTPUT': 'memory:'
            })
            
            # Kasowanie dziur o powierzchni < 1 m2 oraz których smuklosc > 10 000
            pojedynczeObjekty['OUTPUT'].startEditing()
            for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
                geom = obj.geometry()
                if geom.area() < 1: # 1 m2
                    pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
                else:
                    smuklosc = (geom.length() ** 2) / geom.area()
                    if smuklosc > 10000:
                        pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
            pojedynczeObjekty['OUTPUT'].commitChanges(False)
            
            if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
                for objTMP in warstwaPOG.getFeatures():
                    
                    field_names = [field.name() for field in warstwaPOG.fields()]
                    if 'modyfikacja' in field_names and 'status' in field_names:
                        if (
                            not objTMP['modyfikacja']
                            and self.activeDlg != self.formularzInstrukcjaDialogPOGpoUniewaznieniu
                        ):
                            pojedynczeObjekty['OUTPUT'].setName("Geometrie dziur w SPL w zakresie POG")
                            QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
                            showPopup("Błąd warstwy obrysu", "Niepoprawna geometria - Występują dziury w SPL.")
                            czyGeometrieSaPoprawne = False
                            break
        
        return czyGeometrieSaPoprawne


    def kontrolaDziurWSPL(self, obrysLayer, warstwaPOG, czyGeometrieSaPoprawne) -> bool:
        # Czy strefy planistyczne posiadają dziury
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaDziurWSPL`."""
        deleteholes = processing.run("native:deleteholes", {
            'INPUT': obrysLayer,
            'OUTPUT': 'memory:'
        })
        
        difference = processing.run("native:difference", {
            'INPUT': deleteholes['OUTPUT'],
            'OVERLAY': obrysLayer,
            'OUTPUT': 'memory:'
        })
        
        pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
            'INPUT': difference['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        polygonstolines = processing.run("native:polygonstolines", {
            'INPUT': deleteholes['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        extractbylocation = processing.run("native:extractbylocation", {
            'INPUT': pojedynczeObjekty['OUTPUT'],
            'PREDICATE': [0],
            'INTERSECT': polygonstolines['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        try:
            difference2 = processing.run("native:difference", {
                'INPUT': pojedynczeObjekty['OUTPUT'],
                'OVERLAY': extractbylocation['OUTPUT'],
                'OUTPUT': 'memory:'
            })['OUTPUT']
        except:
            difference2 = pojedynczeObjekty['OUTPUT']
        
        pojedynczeObjekty2 = processing.run("native:multiparttosingleparts", {
            'INPUT': difference2,
            'OUTPUT': 'memory:'
        })
        
        # Wykluczenie dziur spowodowanych przez dziury w POG
        if warstwaPOG != None:
            pojedynczeObjekty2 = processing.run("native:extractbylocation", {
                'INPUT': pojedynczeObjekty2['OUTPUT'],
                'PREDICATE': [6],
                'INTERSECT': warstwaPOG,
                'OUTPUT': 'memory:'
            })
        
            obiektPOG = next(warstwaPOG.getFeatures(), None)
            modyfikacjaObiektuPOG = False
            if "modyfikacja" in obiektPOG.fields().names():
                modyfikacjaObiektuPOG = obiektPOG["modyfikacja"]
            
            if pojedynczeObjekty2['OUTPUT'].featureCount() > 0 and not modyfikacjaObiektuPOG:
                pojedynczeObjekty2['OUTPUT'].setName("Dziury w strefach planistycznych")
                QgsProject.instance().addMapLayer(pojedynczeObjekty2['OUTPUT'])
                showPopup("Błąd warstwy obrysu","Niepoprawna geometria - Dziury w strefach planistycznych.")
                czyGeometrieSaPoprawne = False
        
        return czyGeometrieSaPoprawne


    def kontrolaNakladania(self, obrysLayer, czyGeometrieSaPoprawne) -> bool:
        # Czy wystepują nakładające się obiekty
        
        """Wykonuje kontrolę danych w ramach operacji `kontrolaNakladania`."""
        try:
            union = processing.run("native:union", {
                'INPUT': obrysLayer,
                'OUTPUT': 'memory:'
            })['OUTPUT']
            
            usunDuplikaty = processing.run("native:deleteduplicategeometries", {
                'INPUT': union,
                'OUTPUT': 'memory:'
            })
            
            wynik = processing.run("native:detectvectorchanges", {
                'ORIGINAL': union,
                'REVISED': usunDuplikaty['OUTPUT'],
                'UNCHANGED': 'memory:',
                'ADDED': 'memory:',
                'DELETED': 'memory:'
            })['DELETED']
        except:
            # Rozwiazanie alternatywne gdy nie zadziala union
            geom_dict = {f.id(): f.geometry() for f in obrysLayer.getFeatures()}
            
            # Spatial index
            spatial_index = QgsSpatialIndex()
            for f in obrysLayer.getFeatures():
                spatial_index.addFeature(f)
            
            crs = obrysLayer.crs().toWkt()
            results_layer = QgsVectorLayer("Polygon?crs=" + crs, "wyniki", "memory")
            results_provider = results_layer.dataProvider()
            
            # Przetwarzanie unikalnych par
            checked_pairs = set()
            
            for i, f1 in enumerate(obrysLayer.getFeatures()):
                fid1 = f1.id()
                geom1 = geom_dict[fid1]
                candidate_ids = spatial_index.intersects(geom1.boundingBox())
                
                for fid2 in candidate_ids:
                    if fid1 >= fid2 or (fid1, fid2) in checked_pairs:
                        continue
                        
                    geom2 = geom_dict[fid2]
                    
                    if geom1.intersects(geom2):
                        intersection = geom1.intersection(geom2)
                        if not intersection.isEmpty() and intersection.isGeosValid():
                            result = QgsFeature()
                            result.setGeometry(intersection)
                            results_provider.addFeatures([result])
                            
                    checked_pairs.add((fid1, fid2))
                    
            wynik = results_layer
            
        # Kasowanie obiektów nakładających się o powierzchni < 1 m2 oraz których smuklosc > 10 000
        wynik.startEditing()
        for obj in wynik.getFeatures():
            geom = obj.geometry()
            if geom.area() < 1: # 1 m2
                wynik.deleteFeature(obj.id())
            else:
                smuklosc = (geom.length() ** 2) / geom.area()
                if smuklosc > 10000:
                    wynik.deleteFeature(obj.id())
        wynik.commitChanges(False)
        
        if wynik.featureCount() > 0:
            wynik.setName("Nakładajace sie fragmenty geometrii")
            QgsProject.instance().addMapLayer(wynik)
            showPopup("Błąd warstwy obrysu","Niepoprawna geometria - Nakładające się fragmenty geometrii.")
            czyGeometrieSaPoprawne = False
        
        return czyGeometrieSaPoprawne


    def czyObiektyUnikalne(self, obrysLayer, atrybutDoSprawdzeniaUnikalnosci):
        """Sprawdza warunek określony przez operację `czyObiektyUnikalne` i zwraca jego wynik."""
        warstwaBezKoniecWersjiObiektu = processing.run("native:extractbyexpression", {
            'INPUT':obrysLayer,
            'EXPRESSION':'koniecWersjiObiektu is NULL',
            'OUTPUT':'memory:'})
        obrysLayer_tmp = warstwaBezKoniecWersjiObiektu['OUTPUT']
        
        liczbaObiektowWarstwy = obrysLayer_tmp.featureCount()
        liczbaObiektowWarstwyUnikalnych = liczbaObiektowWarstwy
        jestOk = True
        
        field_names = [field.name() for field in obrysLayer.fields()]
        if atrybutDoSprawdzeniaUnikalnosci not in field_names:
            return False
        
        if liczbaObiektowWarstwy > 0:
            unikalnosc = processing.run("native:removeduplicatesbyattribute", {
                'INPUT': obrysLayer_tmp,
                'FIELDS':[atrybutDoSprawdzeniaUnikalnosci],
                'OUTPUT':'memory:',
                'DUPLICATES':'memory:'
            })
            liczbaObiektowWarstwyUnikalnych = unikalnosc['OUTPUT'].featureCount()
            procent = (liczbaObiektowWarstwyUnikalnych / liczbaObiektowWarstwy) * 100
            
            if procent < 100 and atrybutDoSprawdzeniaUnikalnosci == 'oznaczenie':
                showPopup("Błąd warstwy obrysu","Występują duplikaty w atrybucie \'oznaczenie\' warstwy " + obrysLayer.sourceName())
                unikalnosc['DUPLICATES'].setName("Obiekty " + obrysLayer.sourceName() + " - duplikaty w atrybucie \'oznaczenie\'")
                QgsProject.instance().addMapLayer(unikalnosc['DUPLICATES'])
                jestOk = False
            if procent < 100 and atrybutDoSprawdzeniaUnikalnosci == 'lokalnyId':
                showPopup("Błąd warstwy obrysu","Występują duplikaty w atrybucie \'lokalnyId\' warstwy " + obrysLayer.sourceName())
                unikalnosc['DUPLICATES'].setName("Obiekty " + obrysLayer.sourceName() + " - duplikaty w atrybucie \'lokalnyId\'")
                QgsProject.instance().addMapLayer(unikalnosc['DUPLICATES'])
                jestOk = False
            if liczbaObiektowWarstwyUnikalnych != 1 and atrybutDoSprawdzeniaUnikalnosci == 'status':
                showPopup("Ostrzeżenie do warstwy obrysu","Występują różne wartości w atrybucie \'status\' warstwy " + obrysLayer.sourceName())
        return jestOk


    def kontrolaWarstwy(self, obrysLayer):
        """Wykonuje kontrolę danych w ramach operacji `kontrolaWarstwy`."""
        s = QgsSettings()
        jpt = s.value("qgis_app2/settings/jpt", "/")
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
        wynikKontroli = True
        
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z obrysem.")
            return False
        else:
            # Sprawdzanie CRS warstwy wejściowej
            authid = str(self.obrysLayer.crs().authid())
            if authid == '':
                showPopup("Błąd warstwy obrysu", "Obrys nie ma zdefiniowanego układu współrzędnych")
                return False
            epsg = authid.split(':')[1]
            srsName = ''
            # Układ współrzędnych
            for crs in dictionaries.ukladyOdniesieniaPrzestrzennego.values():
                if epsg in crs:
                    srsName = crs
                    break
        
        if self.obrysLayer.featureCount() > 1 and self.obrysLayer.name().startswith("AktPlanowaniaPrzestrzennego"):
            warstwaBezKoniecWersjiObiektu = processing.run("native:extractbyexpression", {
                'INPUT':obrysLayer,
                'EXPRESSION':'koniecWersjiObiektu is NULL',
                'OUTPUT':'memory:'})
            if warstwaBezKoniecWersjiObiektu['OUTPUT'].featureCount() > 1:
                showPopup(title="Błąd warstwy obrysu", text="Wybrana warstwa posiada obiekty w liczbie: %d.\nObrys może składać się wyłącznie z jednego obiektu z niewypełnionym atrybutem koniecWersjiObiektu." % (
                    self.obrysLayer.featureCount()))
                return False
        
        for objx in self.obrysLayer.getFeatures():
            objxgeom = objx.geometry()
            if not objxgeom.isGeosValid():
                return False
        
        if self.obrysLayer.featureCount() == 0:
            return False
        
        if not czyWarstwaMaWypelnioneObowiazkoweAtrybuty(self.obrysLayer):
            showPopup("Błąd warstwy obrysu",
                      "Występują obiekty z niewypełnionymi atrybutami obowiązkowymi.\nWygenerowano warstwę z błędnymi obiektami.")
            wynikKontroli = False
        
        if not kontrolaZaleznosciAtrybutow(self.obrysLayer, rodzajZbioru):
            showPopup("Błąd warstwy obrysu",
                      "Występują obiekty z błędnie wypełnionymi atrybutami.")
            wynikKontroli = False
        
        if obrysLayer.name().startswith("StrefaPlanistyczna") and not kontrolaProfiliDodatkowych(self.obrysLayer):
            showPopup("Błąd warstwy obrysu",
                      "Występują obiekty z błędnie wypełnionymi profilami dodatkowymi.")
            wynikKontroli = False
            
        if srsName == '':
            showPopup("Błąd warstwy obrysu",
                      "Obrys posiada niezgodny układ współrzędnych - EPSG:%s.\nDostępne CRS:\n    - %s" % (epsg, ',\n    - '.join(['%s : %s' % (a, b) for a, b in zip(dictionaries.ukladyOdniesieniaPrzestrzennego.keys(), dictionaries.ukladyOdniesieniaPrzestrzennego.values())])))
            wynikKontroli = False
        
        if rodzajZbioru not in ('PZPW','SUIKZP','MPZP','AK','UK'):
            if not isJPTinLayer(self.obrysLayer, jpt):
                showPopup("Błąd warstwy obrysu",
                          "Warstwa posiada co najmniej jeden obiekt z JPT niezgodnym z ustawieniami.")
                wynikKontroli = False
        
        return wynikKontroli


    def OUZpowyzej125procent(self, obrysLayer, fileName=None):
        """Zwraca wynik operacji `OUZpowyzej125procent` wykonywanej w bieżącym module."""
        pathOUZ_wyjsciowy = os.path.join(defaultPath,"Dokumentacja/ObszarUzupelnieniaZabudowy-wyjsciowy.gml")
        powierzchnie_OUZ = os.path.join(defaultPath,"Dane_pomocnicze/Powierzchnie.xml")
        
        if fileName: # na potrzeby testów - brak kontroli
            return False
        
        if os.path.exists(pathOUZ_wyjsciowy) and os.path.exists(powierzchnie_OUZ):
            root = ET.parse(powierzchnie_OUZ).getroot()  # nosec B314
            powierzchnia_Pp = float(root[3][2].text)
            jpt_xml = int(root[0].text)
            
            if jpt_xml != int(jpt):
                showPopup("Informacja", "JPT w pliku Powierzchnie.xml jest różne od JPT ustawieniach wtyczki.")
            
        else:
            odp = QMessageBox.question(None,'Kontrola warstwy OUZ',
                                         "Wtyczka umożliwia sprawdzenie poprawności wybranej warstwy z wymaganiem, o którym mowa w § 1. ust 5 rozporządzenia.\nDo tej weryfikacji potrzebna jest wyjściowa warstwa OUZ powstała w komponencie „Tworzenie OUZ”, czy chcesz ją teraz wykonać?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if odp == QMessageBox.No:
                return False
            else:
                if self.activeDlg:
                    self.activeDlg.close()
                ouz_dlg = self.tworzenieOUZDialog
                self.activeDlg = ouz_dlg
                ouz_dlg.wlaczenieKonektorow()
                ouz_dlg.show()
                ouz_dlg.warstwa_POG()
                ouz_dlg.warstwa_Budynki()
                ouz_dlg.wylaczenieKonektorow()
                return True
        
        pathOUZ_wyjsciowy_layer = QgsVectorLayer(pathOUZ_wyjsciowy + "|layername=ObszarUzupelnieniaZabudowy|option:FORCE_SRS_DETECTION=YES|option:CONSIDER_EPSG_AS_URN=YES|geometrytype=Polygon", "ObszarUzupelnieniaZabudowy", 'ogr')
        
        try:
            pojedynczeOUZ = processing.run("native:multiparttosingleparts", {
                'INPUT': pathOUZ_wyjsciowy_layer,
                'OUTPUT': 'memory:'
            })['OUTPUT']
        except:
            pojedynczeOUZ = pathOUZ_wyjsciowy_layer
        
        wynik = QgsVectorLayer(
            f"Polygon?crs={obrysLayer.crs().authid()}",
            "wynik",
            "memory"
        )
        
        provider = wynik.dataProvider()
        provider.addAttributes(obrysLayer.fields())
        wynik.updateFields()
        
        # połącz wszystkie geometrie OUZ
        geom_ouz = None
        for f in pojedynczeOUZ.getFeatures():
            if geom_ouz is None:
                geom_ouz = QgsGeometry(f.geometry())
            else:
                geom_ouz = geom_ouz.combine(f.geometry())
        
        for feat in obrysLayer.getFeatures():
            nowy = QgsFeature(wynik.fields())
            nowy.setAttributes(feat.attributes())
        
            geom = QgsGeometry(feat.geometry())
        
            if geom_ouz:
                geom = geom.difference(geom_ouz)
        
            if not geom.isEmpty():
                nowy.setGeometry(geom)
                provider.addFeature(nowy)
        
        wynik.updateExtents()
        wynik_roznica = wynik
        
        # zmiana multipoligonów na poligony
        try:
            pojedynczeRoznice = processing.run("native:multiparttosingleparts", {
                'INPUT': wynik_roznica,
                'OUTPUT': 'memory:'
            })['OUTPUT']
        except:
            pojedynczeRoznice = wynik_roznica
        
        def powierzchniaNaElipsoidzie(feature):
            """Oblicza powierzchnię geometrii na elipsoidzie."""
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            geom = feature.geometry()
            geom.transform(QgsCoordinateTransform(obrysLayer.crs(), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance().transformContext()))
            area = d.measureArea(geom)
            return area
        
        powierzchniaPowiekszeniaOUZ = 0
        for tmp_obj in pojedynczeRoznice.getFeatures():
            powierzchniaPowiekszeniaOUZ += powierzchniaNaElipsoidzie(tmp_obj)
        
        # usunięcie bardzo małych powierzchnii
        pojedynczeRoznice.startEditing()
        for tmpObj in pojedynczeRoznice.getFeatures():
            if tmpObj.geometry().area() < 10:
                pojedynczeRoznice.deleteFeature(tmpObj.id())
        pojedynczeRoznice.commitChanges(False)
        
        # odseparowanie obiektów, które się nie przecinają
        obiektyBledne = processing.run("native:extractbylocation", {
            'INPUT': pojedynczeRoznice,
            'PREDICATE': 2, # Disjoint
            'INTERSECT': pojedynczeOUZ,
            'OUTPUT': 'memory:'
        })
        
        # dodatkowa kontrola sprawdzająca czy native:extractbylocation dla Disjoint dało poprawny wynik
        if obiektyBledne['OUTPUT'].featureCount() > 0:
            # --- kasowanie obiektów, które nie są nowe ---
            obiektyBledne['OUTPUT'].startEditing()
            
            for diff_feat in obiektyBledne['OUTPUT'].getFeatures():
                geomD = diff_feat.geometry()
                diff_vertices = [v for v in geomD.vertices()]
            
                max_common = 0
                for featA in pojedynczeOUZ.getFeatures():
                    geomA = featA.geometry()
                    verticesA = [v for v in geomA.vertices()]
                    common = sum(1 for v in diff_vertices if v in verticesA)
                    if common > max_common:
                        max_common = common
            
                if max_common > 1:  # dwa lub więcej wspólne wierzchołki
                    obiektyBledne['OUTPUT'].deleteFeature(diff_feat.id())
            
            obiektyBledne['OUTPUT'].commitChanges(False)
        
        # przekazanie komunikatu i obiektów błędnych
        if obiektyBledne['OUTPUT'].featureCount() > 0:
            obiektyBledne['OUTPUT'].setName("Nowe obiekty OUZ")
            QgsProject.instance().addMapLayer(obiektyBledne['OUTPUT'])
            showPopup("Błąd warstwy obrysu","Warstwa ObszarUzupelnieniaZabudowy zawiera nowe obiekty.")
            return True
        
        if powierzchniaPowiekszeniaOUZ > powierzchnia_Pp:
            roznica_pow = powierzchniaPowiekszeniaOUZ - powierzchnia_Pp
            showPopup("Błąd warstwy obrysu",
                      f"Powierzchnia warstwy została powiększona o {powierzchniaPowiekszeniaOUZ:.2f} m2,\
 tj. więcej niż o maksymalną powierzchnię powiększenia obszarów uzupełnienia zabudowy wyznaczonych w sposób,\
 o którym mowa w ust. 1 Rozporządzenia tj. {powierzchnia_Pp:.2f} m2. Róznica wynosi {roznica_pow:.2f} m2.")
            return True
        else:
            showPopup("Informacja",
                      "Kontrola maksymalnej powierzchnii powiększenia została przeprowadzona i powiększenie jest dopuszczalne.")
            return False


    def wczytanieProjektuQGIS(self, fileName=None):
        """Wczytuje dane obsługiwane przez operację `wczytanieProjektuQGIS`."""
        if fileName:
            file = fileName
        else:
            file, format = QFileDialog.getOpenFileName(directory=defaultPath,filter="Wszystkie pliki projektów (*.qgs *.QGS *.qgz *QGZ)")
            file = str(file)
        if file == '':
            return
        
        showPopup("Informacja",
                  "Wtyczka umożliwia wczytanie także projektu zawierającego niepoprawne dane, aby umożliwić ich naprawienie. Rekomendujemy, aby plik sprawdzić w Przeglądarce danych planistycznych.")
        
        QgsProject.instance().read(file)
        warstwy = ['StrefaPlanistyczna','ObszarZabudowySrodmiejskiej','ObszarUzupelnieniaZabudowy','ObszarStandardowDostepnosciInfrastrukturySpolecznej','AktPlanowaniaPrzestrzennego']
        for layer in QgsProject.instance().mapLayers().values():
            for warstwa in warstwy:
                if layer.name().startswith(warstwa):
                    break
            
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QgsWkbTypes.PolygonGeometry and layer.name().startswith(warstwa):
                # wczytanie stylu z QML
                if layer.loadNamedStyle(QgsApplication.qgisSettingsDirPath() + "python/plugins/wtyczka_qgis_app/qml/" + warstwa + ".qml"):
                    layer.triggerRepaint()
                    editFormConfig = layer.editFormConfig()
                    # aktualizacja cieżek do ui i py
                    pathUI = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + warstwa + ".ui")
                    editFormConfig.setUiForm(str(pathUI))
                    pathPy = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/" + warstwa + ".py")
                    editFormConfig.setInitFilePath(str(pathPy))
                    editFormConfig.setInitFunction("my_form_open")
                    layer.setEditFormConfig(editFormConfig)
                    # zapisanie zmian w projekcie
                    QgsProject.instance().write()


    def calculate_checksum(self, file_path):
        """Oblicza sumę kontrolną wskazanego pliku lub danych."""
        hash_function = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Odczytaj plik w blokach
            for chunk in iter(lambda: f.read(4096), b""):
                hash_function.update(chunk)
        return hash_function.hexdigest()


    def dodajStylOpartyORegulach(self, layer, field_name):
        """Dodaje dane lub elementy obsługiwane przez operację `dodajStylOpartyORegulach`."""
        if layer.fields().indexOf(field_name) == -1:
            return
        
        unique_values = set()
        for feature in layer.getFeatures():
            value = feature[field_name]
            if isinstance(value, QDate):
                year = value.year()
                month = value.month()
                day = value.day()
                value = int(f"{year:04d}{month:02d}{day:02d}")
            if value != NULL:
                unique_values.add(value)
        
        unique_values = list(unique_values)
        unique_values.sort()
        
        jednostki = {'maksWysokoscZabudowy':'m',
                     'maksUdzialPowierzchniZabudowy':'%',
                     'minUdzialPowierzchniBiologicznieCzynnej':'%',
                     'maksNadziemnaIntensywnoscZabudowy':'',
                     'obowiazujeOd':''}
        
        if 0 in unique_values:
            unique_values_count = len(unique_values)
        else:
            unique_values_count = len(unique_values) + 1 # +1 dla pozycji zero
        if unique_values_count > 9:
            unique_values_count = 10
        
        if len(unique_values) > 0:
            min_value = min(unique_values)
            max_value = max(unique_values)
            if unique_values_count > 1:
                step = round((max_value - min_value) / (unique_values_count - 1), 2)
            else:
                step = round((max_value - min_value) / unique_values_count, 2)
        else:
            unique_values_count = 0
        root_rule = QgsRuleBasedRenderer.Rule(None)
        
        # Reguła dla NULL
        null_symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        null_color = QColor(230, 230, 230)  # Kolor szary dla wartości NULL
        null_symbol.setColor(null_color)
        null_rule = QgsRuleBasedRenderer.Rule(null_symbol)
        null_rule.setFilterExpression(f'"{field_name}" IS NULL')
        null_rule.setLabel('Brak danych')
        root_rule.appendChild(null_rule)
        
        for layer_renderer in null_symbol.symbolLayers():
            if hasattr(layer_renderer, 'setStrokeColor'):
                layer_renderer.setStrokeColor(null_color)
        
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
        
        # Definiowanie niestandardowej palety brązowej
        custom_browns = LinearSegmentedColormap.from_list("CustomBrowns", ["#ffffff", "#8B4513"], N=9)
        
        # Definiowanie niestandardowej palety czerwonej
        custom_reds = LinearSegmentedColormap.from_list("CustomBrowns", ["#ffffff", "#da0000"], N=9)
        
        if len(unique_values) > 0:
            n_colors = unique_values_count  # Liczba kolorów w palecie
            if field_name == 'maksWysokoscZabudowy':
                colors = cm.Blues(np.linspace(0.2, 0.8, n_colors))
            elif field_name == 'minUdzialPowierzchniBiologicznieCzynnej':
                colors = cm.Greens(np.linspace(0.2, 0.8, n_colors))
            elif field_name == 'maksNadziemnaIntensywnoscZabudowy':
                colors = cm.Purples(np.linspace(0.2, 0.8, n_colors))
            elif field_name == 'maksUdzialPowierzchniZabudowy':
                colors = custom_browns(np.linspace(0.2, 0.8, n_colors))
            elif field_name == 'obowiazujeOd':
                colors = custom_reds(np.linspace(0.2, 0.8, n_colors))
            qcolors = [QColor.fromRgbF(color[0], color[1], color[2]) for color in colors]
        
        # Reguły dla przedziałów
        for i in range(unique_values_count):
            if i == 0:
                if field_name == 'obowiazujeOd':
                    continue
                lower_bound = 0.0
                upper_bound = 0.0
                rule_expression = f'"{field_name}" = {lower_bound:.1f}'
                rule_label = f'{lower_bound:.1f}{jednostki[field_name]}'
            else:
                if i == 1:
                    if field_name == 'obowiazujeOd':
                        lower_bound = min_value
                    else:
                        lower_bound = 0.1
                else:
                    if field_name == 'obowiazujeOd':
                        if unique_values_count < 10:
                            lower_bound = unique_values[i - 1]
                        else:
                            lower_bound = upper_bound + 1
                    else:
                        if unique_values_count < 10:
                            lower_bound = unique_values[i - 1]
                        else:
                            lower_bound = upper_bound + 0.1
                if unique_values_count < 10:
                    upper_bound = unique_values[i - 1]
                else:
                    upper_bound = min_value + i * step
                
                # Zaokrąglanie granic
                if field_name == 'obowiazujeOd':
                    lower_bound = int(lower_bound)
                    upper_bound = int(upper_bound)
                else:
                    lower_bound = round(lower_bound, 1)
                    upper_bound = round(upper_bound, 1)
                
                if field_name == 'obowiazujeOd':
                    if i < unique_values_count - 1:
                        rule_expression = f'year(obowiazujeOd)*10000+ month(obowiazujeOd)*100+ day(obowiazujeOd) >= {lower_bound} AND year(obowiazujeOd)*10000+ month(obowiazujeOd)*100+ day(obowiazujeOd) <= {upper_bound}'
                    else:
                        rule_expression = f'year(obowiazujeOd)*10000+ month(obowiazujeOd)*100+ day(obowiazujeOd) >= {lower_bound} AND year(obowiazujeOd)*10000+ month(obowiazujeOd)*100+ day(obowiazujeOd) <= {upper_bound}'
                    if unique_values_count < 10:
                        rule_label = f'{lower_bound}'
                    else:
                        rule_label = f'{lower_bound} - {upper_bound}'
                else:
                    if i < unique_values_count - 1:
                        rule_expression = f'"{field_name}" >= {lower_bound:.1f} AND "{field_name}" <= {upper_bound:.1f}'
                    else:
                        rule_expression = f'"{field_name}" >= {lower_bound:.1f} AND "{field_name}" <= {upper_bound:.1f}'
                    if unique_values_count < 10:
                        rule_label = f'{upper_bound:.1f}{jednostki[field_name]}'
                    else:
                        rule_label = f'{lower_bound:.1f}{jednostki[field_name]} - {upper_bound:.1f}{jednostki[field_name]}'
            
            # Tworzenie symbolu
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(qcolors[i])  # Kolor z palety
        
            for layer_renderer in symbol.symbolLayers():
                if hasattr(layer_renderer, 'setStrokeColor'):
                    layer_renderer.setStrokeColor(QColor(0, 0, 0))
                    layer_renderer.setStrokeWidth(0.03)
        
            # Dodaj regułę
            rule = QgsRuleBasedRenderer.Rule(symbol)
            rule.setFilterExpression(rule_expression)
            rule.setLabel(rule_label)
            rule.setDescription(f'Zakres {i + 1}')
            root_rule.appendChild(rule)
            
        # Stwórz renderer oparty na regułach
        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)
        
        # Włączenie pokazywania liczby obiektów w warstwie
        QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setCustomProperty("showFeatureCount", True)
        iface.layerTreeView().refreshLayerSymbology(layer.id())


    def kontrolaZmianAtrybutowWzgledemWersji(self, plikGMLzrodlowy, plikGML):
        """Wykonuje kontrolę danych w ramach operacji `kontrolaZmianAtrybutowWzgledemWersji`."""
        parser = lxml.etree.XMLParser(remove_blank_text=True)
        
        def parse_for_comparison(file_path):
            """Przetwarza wartość do postaci używanej podczas porównywania danych."""
            with open(file_path, 'rb') as file:
                content = file.read()
        
            target_namespace = (b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0')
            
            for old_namespace in (
                b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0',
                b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0',
            ):
                content = content.replace(old_namespace, target_namespace)
                
            return lxml.etree.fromstring(content, parser=parser)
        
        k = parse_for_comparison(plikGML)
        z = parse_for_comparison(plikGMLzrodlowy)
        
        # usuwanie gml:id
        for elem in k.xpath('//*[@gml:id]', namespaces={'gml': 'http://www.opengis.net/gml/3.2'}):
            del elem.attrib['{http://www.opengis.net/gml/3.2}id']
        for elem in z.xpath('//*[@gml:id]', namespaces={'gml': 'http://www.opengis.net/gml/3.2'}):
            del elem.attrib['{http://www.opengis.net/gml/3.2}id']
        
        # usuwanie zbędnych spacji z gml:posList
        for posList_elem in k.xpath('//gml:posList', namespaces={'gml': 'http://www.opengis.net/gml/3.2'}):
            if posList_elem.text:
                posList_elem.text = posList_elem.text.strip()
        for posList_elem in z.xpath('//gml:posList', namespaces={'gml': 'http://www.opengis.net/gml/3.2'}):
            if posList_elem.text:
                posList_elem.text = posList_elem.text.strip()
        
        ns = {'gml': 'http://www.opengis.net/gml/3.2',
              'wfs': 'http://www.opengis.net/wfs/2.0',
              'app': 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0'
             }
        
        fMembers_K = k.findall('.//wfs:member', namespaces=ns)
        fMembers_Z = z.findall('.//wfs:member', namespaces=ns)
        
        fMembers_K_dic = {}
        fMembers_Z_dic = {}
        obiektyNoweLubZmienione = set()
        
        for fMember in fMembers_K:
            fMembers_K_dic[fMember.find('.//app:lokalnyId', namespaces=ns).text] = fMember
        fMembers_K_dic = dict(sorted(fMembers_K_dic.items()))
        for fMember in fMembers_Z:
            fMembers_Z_dic[fMember.find('.//app:lokalnyId', namespaces=ns).text] = fMember
        fMembers_Z_dic = dict(sorted(fMembers_Z_dic.items()))
        del fMembers_K, fMembers_Z
        
        for fMember_Z_dic in fMembers_Z_dic:
            # wyszukanie i dodanie obiektów nowych
            if not fMember_Z_dic in fMembers_K_dic:
               obiektyNoweLubZmienione.add(fMember_Z_dic)
            
            # wyszukanie i dodanie obiektów zmienionych
            if fMember_Z_dic in fMembers_K_dic and lxml.etree.tostring(fMembers_K_dic[fMember_Z_dic], method="c14n", exclusive=True) != lxml.etree.tostring(fMembers_Z_dic[fMember_Z_dic], method="c14n", exclusive=True):
                    atrybutyZRoznica = set()
                    for element in fMembers_Z_dic[fMember_Z_dic].iter():
                        elementyIdentyczne = False
                        for fM_K_dic_element in fMembers_K_dic[fMember_Z_dic].findall('.//' + element.tag):
                            if fM_K_dic_element.text == element.text:
                                elementyIdentyczne = True
                        if not elementyIdentyczne and element.tag != '{http://www.opengis.net/wfs/2.0}member':
                            if element.tag.split("}")[1] in ['posList','LinearRing','LineString','exterior','interior','Polygon','segments','LineStringSegment','Curve','pos','Point']:
                                atrybutyZRoznica.add('geometria')
                            else:
                                atrybutyZRoznica.add(element.tag.split("}")[1])
                    
                    for element in fMembers_K_dic[fMember_Z_dic].iter():
                        elementyIdentyczne = False
                        
                        if callable(element.tag): # usuwanie komentarzy w GML
                            continue
                        
                        for fM_Z_dic_element in fMembers_Z_dic[fMember_Z_dic].findall('.//' + element.tag):
                            if fM_Z_dic_element.text == element.text:
                                elementyIdentyczne = True
                        if not elementyIdentyczne and element.tag != '{http://www.opengis.net/wfs/2.0}member':
                            if element.tag.split("}")[1] in ['posList','LinearRing','LineString','exterior','interior','Polygon','segments','LineStringSegment','Curve','pos','Point']:
                                atrybutyZRoznica.add('geometria')
                            else:
                                atrybutyZRoznica.add(element.tag.split("}")[1])
                    if len(atrybutyZRoznica) > 1:
                        if 'wersjaId' in atrybutyZRoznica and 'poczatekWersjiObiektu' in atrybutyZRoznica:
                            obiektyNoweLubZmienione.add(fMember_Z_dic)
        return obiektyNoweLubZmienione


    def lokalnyId_APP(self, plikGMLzrodlowy):
        """Zwraca wynik operacji `lokalnyId_APP` wykonywanej w bieżącym module."""
        parser = lxml.etree.XMLParser(remove_blank_text=True)
        z = lxml.etree.parse(plikGMLzrodlowy, parser).getroot()
        unikalnyLokalnyId = set()
        
        ns = {'gml': 'http://www.opengis.net/gml/3.2',
              'wfs': 'http://www.opengis.net/wfs/2.0',
              'app': 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/3.0'
             }
        
        fMembers_Z = z.findall('.//app:lokalnyId', namespaces=ns)
        for fMember_Z in fMembers_Z:
            unikalnyLokalnyId.add(fMember_Z.text)
        
        return unikalnyLokalnyId


    def updateObowiazujeOd(self, input_file, lokalnyids_to_update, data_obowiazujeOd, dataCzasTerazUTC):
        """Aktualizuje dane obsługiwane przez operację `updateObowiazujeOd`."""
        parser = lxml.etree.XMLParser(remove_blank_text=True)
        tree = lxml.etree.parse(input_file, parser)
        root = tree.getroot()
        ns = root.nsmap
        
        # Jeżeli plik zawiera app:DokumentFormalny, nie wykonuj aktualizacji
        if root.xpath(".//app:DokumentFormalny", namespaces=ns):
            return input_file
        
        wersjaId = dataCzasTerazUTC.toString("yyyyMMddThhmmss")
        poczatekWersjiObiektu = dataCzasTerazUTC.toString("yyyy-MM-ddThh:mm:ssZ")
        for lokalnyid in lokalnyids_to_update:
            gmlid = root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../../@gml:id", namespaces=ns)[0]
            identifier = root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../../gml:identifier", namespaces=ns)[0].text
            werjaId_tmp = root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../app:wersjaId", namespaces=ns)[0].text
            gmlid = gmlid.replace(werjaId_tmp, wersjaId)
            identifier = identifier.replace(werjaId_tmp, wersjaId)
            
            root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../..", namespaces=ns)[0].set(f"{{{ns['gml']}}}id", gmlid)
            root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../../gml:identifier", namespaces=ns)[0].text = identifier
            root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../app:wersjaId", namespaces=ns)[0].text = wersjaId
            root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../../app:poczatekWersjiObiektu", namespaces=ns)[0].text = poczatekWersjiObiektu
            root.xpath(f".//app:lokalnyId[text()='{lokalnyid}']/../../../app:obowiazujeOd", namespaces=ns)[0].text = data_obowiazujeOd
            
        # Generowanie nowej nazwy pliku
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_tmp{ext}"
        
        # Zapis zmodyfikowanego XML do nowego pliku z zachowaniem przestrzeni nazw
        tree.write(output_file, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return output_file


    def pobierzDateObowiazujeOd(self):
        """Pobiera dane wymagane przez operację `pobierzDateObowiazujeOd`."""
        dialog = QDialog()
        dialog.setWindowTitle("Wybierz datę obowiązuje od")
        layout = QVBoxLayout(dialog)
        label = QLabel('Wybierz datę "obowiązuje od" dla obiektów nowych i zmienionych, a następnie naciśnij ok:')
        layout.addWidget(label)
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        layout.addWidget(date_edit)
        
        ok_button = QPushButton("OK")
        ok_button.setObjectName("ok_button")
        layout.addWidget(ok_button)
        selected_date_str = None
        
        def on_ok():
            """Realizuje operację `on_ok` w bieżącym module."""
            nonlocal selected_date_str
            selected_date = date_edit.date()
            selected_date_str = selected_date.toString("yyyy-MM-dd")
            dialog.accept()
        
        ok_button.clicked.connect(on_ok)
        dialog.exec_()
        
        return selected_date_str


    def checkRequiredLayers(self):
        """Sprawdza, czy w projekcie QGIS znajduje się co najmniej jedna warstwa POG."""
        
        wymagane_warstwy = [
            "StrefaPlanistyczna",
            "ObszarUzupelnieniaZabudowy",
            "ObszarZabudowySrodmiejskiej",
            "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
        ]
        
        warstwy_w_projekcie = [
            layer.name()
            for layer in QgsProject.instance().mapLayers().values()
        ]
        
        znalezione = []
        
        for wymagana in wymagane_warstwy:
            if any(nazwa.startswith(wymagana) for nazwa in warstwy_w_projekcie):
                znalezione.append(wymagana)
                
        if not znalezione:
            QMessageBox.warning(
                None,
                "Brak wymaganych warstw",
                "W projekcie QGIS nie znaleziono żadnej z warstw POG. Wykorzystaj funkcję 'Wczytaj warstwy'."
            )
            return False
            
        return True


    def checkLayersAndOznaczenia(self, text):
        """Sprawdza wymagane warstwy oraz występowanie oznaczeń w odpowiednich warstwach QGIS."""
        
        import re
        from qgis.core import QgsProject
        from qgis.PyQt.QtWidgets import QMessageBox
        
        pole_oznaczenia = "oznaczenie"
        
        strefy = {
            "SW", "SJ", "SZ", "SU", "SH", "SP", "SR",
            "SI", "SN", "SC", "SG", "SO", "SK"
        }
        
        warstwa_dla_skrotu = {
            "OUZ": "ObszarUzupelnieniaZabudowy",
            "OZS": "ObszarZabudowySrodmiejskiej",
            "OSD": "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
        }
        
        def find_layer_by_prefix(prefix):
            """Zwraca pierwszą warstwę, której nazwa zaczyna się od wskazanego tekstu."""
            for layer in QgsProject.instance().mapLayers().values():
                if layer.name().startswith(prefix):
                    return layer
            return None
        
        znalezione = re.findall(
            r"\b([1-9]\d*)\s*(SW|SJ|SZ|SU|SH|SP|SR|SI|SN|SC|SG|SO|SK|OUZ|OZS|OSD)\b",
            text.upper()
        )
        
        if not znalezione:
            return True
        
        oznaczenia_dla_warstw = {}
        wymagane_warstwy = set()
        
        for numer, skrot in znalezione:
            oznaczenie = f"{numer}{skrot}"
            
            if skrot in strefy:
                nazwa_warstwy = "StrefaPlanistyczna"
            else:
                nazwa_warstwy = warstwa_dla_skrotu[skrot]
                
            wymagane_warstwy.add(nazwa_warstwy)
            oznaczenia_dla_warstw.setdefault(nazwa_warstwy, set()).add(oznaczenie)
            
        brakujace_warstwy = []
        
        for nazwa_warstwy in sorted(wymagane_warstwy):
            if find_layer_by_prefix(nazwa_warstwy) is None:
                brakujace_warstwy.append(nazwa_warstwy)
                
        if brakujace_warstwy:
            QMessageBox.warning(
                None,
                "Brak wymaganych warstw",
                "Brakuje wymaganych warstw:\n\n" + "\n".join(brakujace_warstwy)
            )
            return False
        
        brakujace_oznaczenia = {}
        
        for nazwa_warstwy, wymagane_oznaczenia in oznaczenia_dla_warstw.items():
            layer = find_layer_by_prefix(nazwa_warstwy)
            
            if layer is None:
                brakujace_oznaczenia[nazwa_warstwy] = sorted(wymagane_oznaczenia)
                continue
            
            if pole_oznaczenia not in [field.name() for field in layer.fields()]:
                QMessageBox.warning(
                    None,
                    "Brak pola w warstwie",
                    f"W warstwie {layer.name()} nie znaleziono pola '{pole_oznaczenia}'."
                )
                return False
            
            oznaczenia_w_warstwie = {
                str(feature[pole_oznaczenia]).replace(" ", "").upper()
                for feature in layer.getFeatures()
                if feature[pole_oznaczenia] is not None
            }
            
            nieznalezione = sorted(wymagane_oznaczenia - oznaczenia_w_warstwie)
            
            if nieznalezione:
                brakujace_oznaczenia[layer.name()] = nieznalezione
                
        if brakujace_oznaczenia:
            komunikat = "Nie znaleziono poniższych oznaczeń w odpowiednich warstwach:\n"
            
            for nazwa_warstwy, oznaczenia in sorted(brakujace_oznaczenia.items()):
                komunikat += f"\n{nazwa_warstwy}:\n"
                komunikat += "\n".join(f" • {o}" for o in oznaczenia)
                komunikat += "\n"
                
            QMessageBox.warning(
                None,
                "Brak oznaczeń w warstwach",
                komunikat
            )
            return False
        
        return True


    def obliczPowierzchnieM2PoUniewaznieniu(
        self,
        geometry,
        crs
    ):
        """
        Zwraca powierzchnię geometrii w metrach kwadratowych.
        """
        
        if geometry is None or geometry.isEmpty():
            return 0.0
        
        miernik = QgsDistanceArea()
        miernik.setSourceCrs(
            crs,
            QgsProject.instance().transformContext()
        )
        
        elipsoida = QgsProject.instance().ellipsoid()
        
        if not elipsoida or str(elipsoida).upper() == "NONE":
            elipsoida = crs.ellipsoidAcronym()
            
        if elipsoida and str(elipsoida).upper() != "NONE":
            miernik.setEllipsoid(elipsoida)
            
        powierzchnia = abs(
            miernik.measureArea(geometry)
        )
        
        return abs(
            miernik.convertAreaMeasurement(
                powierzchnia,
                QgsUnitTypes.AreaSquareMeters
            )
        )


    def czyPowierzchniaMniejszaNizJedenCm2PoUniewaznieniu(self, geometry, crs):
        """Sprawdza warunek określony przez operację `czyPowierzchniaMniejszaNizJedenCm2PoUniewaznieniu` i zwraca jego wynik."""
        prog_powierzchni_m2 = 0.0001
        
        return (
            self.obliczPowierzchnieM2PoUniewaznieniu(
                geometry,
                crs
            )
            < prog_powierzchni_m2
        )


    def pobierzPoligonyZGeometriiPoUniewaznieniu(
        self,
        geometry,
        crs
    ):
        
        """Pobiera dane wymagane przez operację `pobierzPoligonyZGeometriiPoUniewaznieniu`."""
        if geometry is None or geometry.isEmpty():
            return [], 0
        
        geometrie_do_sprawdzenia = [
            QgsGeometry(geometry)
        ]
        poligony = []
        liczba_usunietych_malych_czesci = 0
        
        while geometrie_do_sprawdzenia:
            geometria = geometrie_do_sprawdzenia.pop(0)
            
            if geometria is None or geometria.isEmpty():
                continue
            
            if geometria.isMultipart():
                czesci = geometria.asGeometryCollection()
                
                if czesci:
                    geometrie_do_sprawdzenia.extend(
                        QgsGeometry(czesc)
                        for czesc in czesci
                    )
                    continue
                
            if (
                QgsWkbTypes.geometryType(
                    geometria.wkbType()
                )
                == QgsWkbTypes.PolygonGeometry
            ):
                poligon = QgsGeometry(geometria)
                
                if (
                    self.czyPowierzchniaMniejszaNizJedenCm2PoUniewaznieniu(
                        poligon,
                        crs
                    )
                ):
                    liczba_usunietych_malych_czesci += 1
                    continue
                
                poligony.append(poligon)
                
        return poligony, liczba_usunietych_malych_czesci


    def oczyscGeometriePoUniewaznieniu(self, geometry):
        """Czyści dane lub stan obsługiwany przez operację `oczyscGeometriePoUniewaznieniu`."""
        if geometry is None or geometry.isEmpty():
            return geometry
            
        temp_layer = QgsVectorLayer(QgsWkbTypes.displayString(geometry.wkbType()), "geometria_do_oczyszczenia", "memory")
        temp_provider = temp_layer.dataProvider()
        
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry(geometry))
        temp_provider.addFeature(feature)
        temp_layer.updateExtents()
        
        wynik_processing = processing.run("native:removeduplicatevertices", {'INPUT': temp_layer, 'TOLERANCE': 1e-06, 'USE_Z_VALUE': False, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        
        output_layer = wynik_processing['OUTPUT']
        
        for output_feature in output_layer.getFeatures():
            wynik = QgsGeometry(output_feature.geometry())
            
            if not wynik.isGeosValid():
                wynik = wynik.makeValid()
                
            return wynik
        
        return geometry


    def zastapMultipoligonPoligonamiPoUniewaznieniu(
        self,
        layer,
        feature,
        nowa_geometria,
        stare_oznaczenie,
        wersja_id,
        poczatek_wersji,
        obowiazuje_od,
        pole_oznaczenia="oznaczenie",
        pole_lokalny_id="lokalnyId"
    ):
        """Usuwa obiekt multipoligonowy i dodaje pojedyncze poligony bez oznaczeń."""
        
        indeks_oznaczenia = layer.fields().indexFromName(
            pole_oznaczenia
        )
        indeks_lokalny_id = layer.fields().indexFromName(
            pole_lokalny_id
        )
        
        if indeks_oznaczenia == -1:
            return (
                False,
                0,
                0,
                f"Warstwa '{layer.name()}' nie zawiera pola "
                f"'{pole_oznaczenia}'."
            )
        
        if indeks_lokalny_id == -1:
            return (
                False,
                0,
                0,
                f"Warstwa '{layer.name()}' nie zawiera pola "
                f"'{pole_lokalny_id}'."
            )
        
        (
            poligony,
            liczba_usunietych_malych_czesci
        ) = self.pobierzPoligonyZGeometriiPoUniewaznieniu(
            nowa_geometria,
            layer.crs()
        )
            
        if not poligony and liczba_usunietych_malych_czesci == 0:
            return (
                False,
                0,
                0,
                f"Nie udało się pobrać części poligonowych z geometrii "
                f"obiektu '{stare_oznaczenie}' w warstwie "
                f"'{layer.name()}'."
            )
        
        atrybuty_zrodlowe = list(
            feature.attributes()
        )
        indeksy_klucza_glownego = set(
            layer.dataProvider().pkAttributeIndexes()
        )
        nowe_obiekty = []
        
        for poligon in poligony:
            nowy_feature = QgsFeature(
                layer.fields()
            )
            nowy_feature.setAttributes(
                list(atrybuty_zrodlowe)
            )
            nowy_feature.setGeometry(
                poligon
            )
            
            for indeks_pola in indeksy_klucza_glownego:
                nowy_feature.setAttribute(
                    indeks_pola,
                    None
                )
                
            # Nowe obiekty nie otrzymują automatycznie oznaczenia.
            # lokalnyId również jest zerowany, ponieważ zostanie
            # wyliczony przez formularz po wpisaniu nowego oznaczenia.
            nowy_feature.setAttribute(
                indeks_oznaczenia,
                None
            )
            nowy_feature.setAttribute(
                indeks_lokalny_id,
                None
            )
            
            nowe_obiekty.append(
                nowy_feature
            )
            
        layer.beginEditCommand(
            "Rozbicie multipoligonu po wycięciu"
        )
        
        try:
            if not layer.deleteFeature(feature.id()):
                raise RuntimeError(
                    f"Nie udało się usunąć obiektu "
                    f"'{stare_oznaczenie}'."
                )
                
            for nowy_feature in nowe_obiekty:
                if not layer.addFeature(nowy_feature):
                    raise RuntimeError(
                        f"Nie udało się dodać poligonu powstałego "
                        f"z obiektu '{stare_oznaczenie}'."
                    )
                    
                self.ustawAtrybutyZmianyObiektuPoUniewaznieniu(
                    layer=layer,
                    feature_id=nowy_feature.id(),
                    wersja_id=wersja_id,
                    poczatek_wersji=poczatek_wersji,
                    obowiazuje_od=obowiazuje_od
                )
                
            layer.endEditCommand()
            
        except Exception as blad:
            layer.destroyEditCommand()
            return (
                False,
                0,
                liczba_usunietych_malych_czesci,
                str(blad)
            )
        
        return (
            True,
            len(nowe_obiekty),
            liczba_usunietych_malych_czesci,
            None
        )


    def removeObjectsByOznaczenia(self, text, obowiazuje_od):
        """Usuwa wskazane obiekty, aktualizuje APP i zapisuje wszystkie warstwy POG."""
        
        pole_oznaczenia = "oznaczenie"
        pole_wersja_id = "wersjaId"
        pole_poczatek = "poczatekWersjiObiektu"
        pole_obowiazuje_od = "obowiazujeOd"
        pole_lokalny_id = "lokalnyId"
        
        warstwa_app = (
            self.pobierzWarstweAktPlanowaniaPrzestrzennegoDoAktualizacji()
        )
        
        if warstwa_app is None:
            return False
        
        now = QDateTime.currentDateTimeUtc().toPyDateTime()
        wersja_id = now.strftime("%Y%m%dT%H%M%S")
        poczatek_wersji = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        obowiazuje_od_txt = obowiazuje_od.toString("yyyy-MM-dd")
        
        strefy = {
            "SW", "SJ", "SZ", "SU", "SH", "SP", "SR",
            "SI", "SN", "SC", "SG", "SO", "SK"
        }
        
        warstwa_dla_skrotu = {
            "OUZ": "ObszarUzupelnieniaZabudowy",
            "OZS": "ObszarZabudowySrodmiejskiej",
            "OSD": "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
        }
        
        warstwy_do_wycinania = [
            "ObszarUzupelnieniaZabudowy",
            "ObszarZabudowySrodmiejskiej",
            "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
        ]
        
        raport = {}
        edytowane_warstwy = set()
        warstwy_do_recznego_zapisu = set()
        
        def init_raport(nazwa_warstwy):
            """Inicjalizuje dane wymagane przez operację `init_raport`."""
            if nazwa_warstwy not in raport:
                raport[nazwa_warstwy] = {
                    "usuniete_wskazane": [],
                    "zmodyfikowane_po_wycieciu": [],
                    "usuniete_po_wycieciu": [],
                    "usuniete_ponizej_1_cm2": [],
                    "usuniete_czesci_ponizej_1_cm2": [],
                    "rozbite_multipoligony": [],
                }
                
        def dodaj_do_raportu(nazwa_warstwy, klucz, oznaczenie):
            """Dodaje dane lub elementy obsługiwane przez operację `dodaj_do_raportu`."""
            init_raport(nazwa_warstwy)
            
            if oznaczenie not in raport[nazwa_warstwy][klucz]:
                raport[nazwa_warstwy][klucz].append(oznaczenie)
                
        def oznaczenie_feature(feature):
            """Zwraca wynik operacji `oznaczenie_feature` wykonywanej w bieżącym module."""
            return str(
                feature[pole_oznaczenia]
            ).replace(" ", "").upper()
        
        znalezione = re.findall(
            r"\b([1-9]\d*)\s*"
            r"(SW|SJ|SZ|SU|SH|SP|SR|SI|SN|SC|SG|SO|SK|OUZ|OZS|OSD)\b",
            text.upper()
        )
        
        if not znalezione:
            QMessageBox.information(
                None,
                "Raport",
                "Nie znaleziono oznaczeń do przetworzenia."
            )
            return False
        
        oznaczenia_dla_warstw = {}
        oznaczenia_stref = set()
        
        for numer, skrot in znalezione:
            oznaczenie = f"{numer}{skrot}"
            
            if skrot in strefy:
                nazwa_warstwy = "StrefaPlanistyczna"
                oznaczenia_stref.add(oznaczenie)
            else:
                nazwa_warstwy = warstwa_dla_skrotu[skrot]
                
            oznaczenia_dla_warstw.setdefault(
                nazwa_warstwy,
                set()
            ).add(oznaczenie)
            
        geometrie_stref_do_wyciecia = []
        
        if oznaczenia_stref:
            layer_stref = self.znajdzWarstwePoPrefiksie(
                "StrefaPlanistyczna"
            )
            
            if layer_stref is None:
                QMessageBox.warning(
                    None,
                    "Brak warstwy",
                    "Nie znaleziono warstwy StrefaPlanistyczna."
                )
                return False
            
            for feature in layer_stref.getFeatures():
                ozn = oznaczenie_feature(feature)
                
                if ozn in oznaczenia_stref:
                    geometrie_stref_do_wyciecia.append(
                        QgsGeometry(feature.geometry())
                    )
                    
        for nazwa_warstwy, oznaczenia in oznaczenia_dla_warstw.items():
            layer = self.znajdzWarstwePoPrefiksie(nazwa_warstwy)
            
            if layer is None:
                continue
            
            init_raport(layer.name())
            
            if layer.fields().indexFromName(pole_oznaczenia) == -1:
                QMessageBox.warning(
                    None,
                    "Brak pola oznaczenie",
                    f"Warstwa '{layer.name()}' nie zawiera pola "
                    f"'{pole_oznaczenia}'."
                )
                return False
            
            if not self.rozpocznijEdycjeWarstwyPoUniewaznieniu(
                layer,
                edytowane_warstwy
            ):
                return False
            
            ids_do_usuniecia = []
            
            for feature in layer.getFeatures():
                ozn = oznaczenie_feature(feature)
                
                if ozn in oznaczenia:
                    ids_do_usuniecia.append(feature.id())
                    dodaj_do_raportu(
                        layer.name(),
                        "usuniete_wskazane",
                        ozn
                    )
                    
            if ids_do_usuniecia:
                layer.deleteFeatures(ids_do_usuniecia)
                
        if geometrie_stref_do_wyciecia:
            geometria_wycinajaca = QgsGeometry.unaryUnion(
                geometrie_stref_do_wyciecia
            )
            
            for nazwa_warstwy in warstwy_do_wycinania:
                layer = self.znajdzWarstwePoPrefiksie(nazwa_warstwy)
                
                if layer is None:
                    continue
                
                init_raport(layer.name())
                
                if layer.fields().indexFromName(pole_oznaczenia) == -1:
                    QMessageBox.warning(
                        None,
                        "Brak pola oznaczenie",
                        f"Warstwa '{layer.name()}' nie zawiera pola "
                        f"'{pole_oznaczenia}'."
                    )
                    return False
                
                if not self.rozpocznijEdycjeWarstwyPoUniewaznieniu(
                    layer,
                    edytowane_warstwy
                ):
                    return False
                
                for feature in list(layer.getFeatures()):
                    geom = feature.geometry()
                    
                    if geom is None or geom.isEmpty():
                        continue
                    
                    if not geom.intersects(geometria_wycinajaca):
                        continue
                    
                    ozn = oznaczenie_feature(feature)
                    nowa_geom = geom.difference(geometria_wycinajaca)
                    nowa_geom = self.oczyscGeometriePoUniewaznieniu(nowa_geom)
                    
                    if nowa_geom is None or nowa_geom.isEmpty():
                        layer.deleteFeature(feature.id())
                        dodaj_do_raportu(
                            layer.name(),
                            "usuniete_po_wycieciu",
                            ozn
                        )
                        continue
                    
                    if (
                        self.czyPowierzchniaMniejszaNizJedenCm2PoUniewaznieniu(
                            nowa_geom,
                            layer.crs()
                        )
                    ):
                        layer.deleteFeature(feature.id())
                        dodaj_do_raportu(
                            layer.name(),
                            "usuniete_ponizej_1_cm2",
                            ozn
                        )
                        continue
                    
                    if nowa_geom.isMultipart():
                        (
                            sukces,
                            liczba_nowych_poligonow,
                            liczba_usunietych_malych_czesci,
                            blad_rozbicia
                        ) = self.zastapMultipoligonPoligonamiPoUniewaznieniu(
                            layer=layer,
                            feature=feature,
                            nowa_geometria=nowa_geom,
                            stare_oznaczenie=ozn,
                            wersja_id=wersja_id,
                            poczatek_wersji=poczatek_wersji,
                            obowiazuje_od=obowiazuje_od,
                            pole_oznaczenia=pole_oznaczenia,
                            pole_lokalny_id=pole_lokalny_id
                        )
                            
                        if not sukces:
                            QMessageBox.critical(
                                None,
                                "Błąd rozbijania multipoligonu",
                                blad_rozbicia
                            )
                            return False
                        
                        if liczba_usunietych_malych_czesci:
                            raport[layer.name()][
                                "usuniete_czesci_ponizej_1_cm2"
                            ].append(
                                f"{ozn}: usunięto "
                                f"{liczba_usunietych_malych_czesci} "
                                f"część/części"
                            )
                                
                        if liczba_nowych_poligonow == 0:
                            dodaj_do_raportu(
                                layer.name(),
                                "usuniete_ponizej_1_cm2",
                                ozn
                            )
                            continue
                        
                        warstwy_do_recznego_zapisu.add(
                            layer.id()
                        )
                        
                        raport[layer.name()][
                            "rozbite_multipoligony"
                        ].append(
                            f"{ozn} - rozbito na "
                            f"{liczba_nowych_poligonow} poligonów"
                        )
                        continue
                    
                    layer.changeGeometry(
                        feature.id(),
                        nowa_geom
                    )
                    
                    self.ustawAtrybutyZmianyObiektuPoUniewaznieniu(
                        layer=layer,
                        feature_id=feature.id(),
                        wersja_id=wersja_id,
                        poczatek_wersji=poczatek_wersji,
                        obowiazuje_od=obowiazuje_od
                    )
                    
                    dodaj_do_raportu(
                        layer.name(),
                        "zmodyfikowane_po_wycieciu",
                        ozn
                    )
                    
        if not self.aktualizujAktPlanowaniaPrzestrzennegoPoUniewaznieniu(
            layer=warstwa_app,
            wersja_id=wersja_id,
            poczatek_wersji=poczatek_wersji,
            obowiazuje_od=obowiazuje_od,
            edytowane_warstwy=edytowane_warstwy
        ):
            return False
        
        zapisane_warstwy, bledy_zapisu = (
            self.zapiszWszystkieWarstwyPOGDoGML(
                edytowane_warstwy,
                warstwy_do_recznego_zapisu
            )
        )
        
        data_generowania_raportu = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        komunikat = (
            "Raport z unieważnienia\n"
            f"Data i godzina wygenerowania raportu: "
            f"{data_generowania_raportu}\n\n"
            "Raport według warstw:\n"
        )
        
        for nazwa_warstwy in sorted(raport.keys()):
            dane = raport[nazwa_warstwy]
            
            usuniete_wskazane = sorted(
                dane["usuniete_wskazane"]
            )
            zmodyfikowane = sorted(
                dane["zmodyfikowane_po_wycieciu"]
            )
            usuniete_po_wycieciu = sorted(
                dane["usuniete_po_wycieciu"]
            )
            usuniete_ponizej_1_cm2 = sorted(
                dane["usuniete_ponizej_1_cm2"]
            )
            usuniete_czesci_ponizej_1_cm2 = sorted(
                dane["usuniete_czesci_ponizej_1_cm2"]
            )
            rozbite_multipoligony = sorted(
                dane["rozbite_multipoligony"]
            )
            
            komunikat += f"\n{nazwa_warstwy}:\n"
            komunikat += (
                "• Usunięto wskazane obiekty: "
                f"{len(usuniete_wskazane)}\n"
            )
            
            if usuniete_wskazane:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in usuniete_wskazane
                ) + "\n"
                
            komunikat += (
                "• Zmieniono geometrię po wycięciu stref: "
                f"{len(zmodyfikowane)}\n"
            )
            
            if zmodyfikowane:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in zmodyfikowane
                ) + "\n"
                
            komunikat += (
                "• Usunięto po wycięciu całej geometrii: "
                f"{len(usuniete_po_wycieciu)}\n"
            )
            
            if usuniete_po_wycieciu:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in usuniete_po_wycieciu
                ) + "\n"
                
            komunikat += (
                "• Rozbito multipoligony na poligony: "
                f"{len(rozbite_multipoligony)}\n"
            )
            
            if rozbite_multipoligony:
                komunikat += "\n".join(
                    f"  • {opis}"
                    for opis in rozbite_multipoligony
                ) + "\n"
                
        if warstwy_do_recznego_zapisu:
            komunikat += (
                "\nNależy uzupełnić formularz atrybutów dla nowo "
                "powstałych obiektów, a następnie zapisać warstwę "
                "do pliku GML.\n"
            )
            
        komunikat += (
            "\nUstawiono wartości atrybutów dla obiektów zmienionych:"
        )
        komunikat += f"\n• {pole_wersja_id}: {wersja_id}"
        komunikat += f"\n• {pole_poczatek}: {poczatek_wersji}"
        komunikat += (
            f"\n• {pole_obowiazuje_od}: {obowiazuje_od_txt}"
        )
        
        komunikat += self.przygotujRaportAktPlanowaniaPrzestrzennego(
            warstwa_app=warstwa_app,
            wersja_id=wersja_id,
            poczatek_wersji=poczatek_wersji,
            obowiazuje_od=obowiazuje_od
        )
        
        if zapisane_warstwy:
            komunikat += "\n\nZapisano warstwy do GML:\n"
            komunikat += "\n".join(
                f"• {nazwa}"
                for nazwa in sorted(zapisane_warstwy)
            )
            
        if bledy_zapisu:
            komunikat += (
                "\n\nNie udało się zapisać zmian lub GML:\n"
            )
            komunikat += "\n".join(
                f"• {blad}"
                for blad in sorted(bledy_zapisu)
            )
            
        self.pokazRaportUniewaznienia(komunikat)
        return True


    def removeObjectsByLayer(self, obowiazuje_od):
        """Przycina obiekty, aktualizuje APP i zapisuje wszystkie warstwy POG."""
        
        pole_oznaczenia = "oznaczenie"
        pole_wersja_id = "wersjaId"
        pole_poczatek = "poczatekWersjiObiektu"
        pole_obowiazuje_od = "obowiazujeOd"
        pole_lokalny_id = "lokalnyId"
        
        warstwa_wejsciowa = (
            self.formularzInstrukcjaDialogPOGpoUniewaznieniu
            .layers_comboBox.currentLayer()
        )
        
        if warstwa_wejsciowa is None:
            QMessageBox.warning(
                None,
                "Brak warstwy wejściowej",
                "Nie wskazano warstwy służącej do wycinania geometrii."
            )
            return False
        
        warstwa_app = (
            self.pobierzWarstweAktPlanowaniaPrzestrzennegoDoAktualizacji()
        )
        
        if warstwa_app is None:
            return False
        
        now = QDateTime.currentDateTimeUtc().toPyDateTime()
        wersja_id = now.strftime("%Y%m%dT%H%M%S")
        poczatek_wersji = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        obowiazuje_od_txt = obowiazuje_od.toString("yyyy-MM-dd")
        
        warstwy_do_przetworzenia = [
            "StrefaPlanistyczna",
            "ObszarUzupelnieniaZabudowy",
            "ObszarZabudowySrodmiejskiej",
            "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
        ]
        
        raport = {}
        edytowane_warstwy = set()
        warstwy_do_recznego_zapisu = set()
        
        def init_raport(nazwa_warstwy):
            """Inicjalizuje dane wymagane przez operację `init_raport`."""
            if nazwa_warstwy not in raport:
                raport[nazwa_warstwy] = {
                    "usuniete_wskazane": [],
                    "zmodyfikowane_po_wycieciu": [],
                    "usuniete_po_wycieciu": [],
                    "usuniete_ponizej_1_cm2": [],
                    "usuniete_czesci_ponizej_1_cm2": [],
                    "rozbite_multipoligony": [],
                }
                
        def dodaj_do_raportu(nazwa_warstwy, klucz, oznaczenie):
            """Dodaje dane lub elementy obsługiwane przez operację `dodaj_do_raportu`."""
            init_raport(nazwa_warstwy)
            
            if oznaczenie not in raport[nazwa_warstwy][klucz]:
                raport[nazwa_warstwy][klucz].append(oznaczenie)
                
        def oznaczenie_feature(feature, layer):
            """Zwraca wynik operacji `oznaczenie_feature` wykonywanej w bieżącym module."""
            indeks_oznaczenia = layer.fields().indexFromName(
                pole_oznaczenia
            )
            
            if indeks_oznaczenia != -1:
                wartosc = feature[pole_oznaczenia]
                
                if wartosc is not None:
                    return str(wartosc).replace(" ", "").upper()
                
            return f"fid:{feature.id()}"
        
        geometrie_wejsciowe = []
        
        for feature in warstwa_wejsciowa.getFeatures():
            geom = feature.geometry()
            
            if geom is None or geom.isEmpty():
                continue
                
            geometrie_wejsciowe.append(
                QgsGeometry(geom)
            )
            
        if not geometrie_wejsciowe:
            QMessageBox.information(
                None,
                "Raport",
                "Wybrana warstwa wejściowa nie zawiera geometrii "
                "do przetworzenia."
            )
            return False
            
        geometria_wycinajaca = QgsGeometry.unaryUnion(
            geometrie_wejsciowe
        )
        
        if geometria_wycinajaca is None or geometria_wycinajaca.isEmpty():
            QMessageBox.warning(
                None,
                "Błąd geometrii",
                "Nie udało się utworzyć geometrii wycinającej "
                "z wybranej warstwy."
            )
            return False
            
        for nazwa_warstwy in warstwy_do_przetworzenia:
            layer = self.znajdzWarstwePoPrefiksie(
                nazwa_warstwy
            )
            
            if layer is None:
                continue
                
            init_raport(layer.name())
            
            if layer.fields().indexFromName(pole_oznaczenia) == -1:
                QMessageBox.warning(
                    None,
                    "Brak pola oznaczenie",
                    f"Warstwa '{layer.name()}' nie zawiera pola "
                    f"'{pole_oznaczenia}'."
                )
                return False
            
            if not self.rozpocznijEdycjeWarstwyPoUniewaznieniu(
                layer,
                edytowane_warstwy
            ):
                return False
                
            for feature in list(layer.getFeatures()):
                geom = feature.geometry()
                
                if geom is None or geom.isEmpty():
                    continue
                
                if not geom.intersects(geometria_wycinajaca):
                    continue
                
                # Samo zetknięcie granic nie oznacza zmiany geometrii obiektu.
                if geom.touches(geometria_wycinajaca):
                    continue
                
                ozn = oznaczenie_feature(
                    feature,
                    layer
                )
                nowa_geom = geom.difference(geometria_wycinajaca)
                nowa_geom = self.oczyscGeometriePoUniewaznieniu(nowa_geom)
                
                if nowa_geom is None or nowa_geom.isEmpty():
                    layer.deleteFeature(
                        feature.id()
                    )
                    dodaj_do_raportu(
                        layer.name(),
                        "usuniete_po_wycieciu",
                        ozn
                    )
                    continue
                
                # Dodatkowe zabezpieczenie. Operacja difference może zwrócić
                # geometrię zapisaną w innej kolejności wierzchołków/pierścieni,
                # mimo że topologicznie jest to dokładnie ten sam obiekt.
                if geom.isGeosEqual(nowa_geom):
                    continue
                
                if (
                    self.czyPowierzchniaMniejszaNizJedenCm2PoUniewaznieniu(
                        nowa_geom,
                        layer.crs()
                    )
                ):
                    layer.deleteFeature(
                        feature.id()
                    )
                    dodaj_do_raportu(
                        layer.name(),
                        "usuniete_ponizej_1_cm2",
                        ozn
                    )
                    continue
                
                if nowa_geom.isMultipart():
                    (
                        sukces,
                        liczba_nowych_poligonow,
                        liczba_usunietych_malych_czesci,
                        blad_rozbicia
                    ) = self.zastapMultipoligonPoligonamiPoUniewaznieniu(
                        layer=layer,
                        feature=feature,
                        nowa_geometria=nowa_geom,
                        stare_oznaczenie=ozn,
                        wersja_id=wersja_id,
                        poczatek_wersji=poczatek_wersji,
                        obowiazuje_od=obowiazuje_od,
                        pole_oznaczenia=pole_oznaczenia,
                        pole_lokalny_id=pole_lokalny_id
                    )
                        
                    if not sukces:
                        QMessageBox.critical(
                            None,
                            "Błąd rozbijania multipoligonu",
                            blad_rozbicia
                        )
                        return False
                    
                    if liczba_usunietych_malych_czesci:
                        raport[layer.name()][
                            "usuniete_czesci_ponizej_1_cm2"
                        ].append(
                            f"{ozn}: usunięto "
                            f"{liczba_usunietych_malych_czesci} "
                            f"część/części"
                        )
                            
                    if liczba_nowych_poligonow == 0:
                        dodaj_do_raportu(
                            layer.name(),
                            "usuniete_ponizej_1_cm2",
                            ozn
                        )
                        continue
                    
                    warstwy_do_recznego_zapisu.add(
                        layer.id()
                    )
                    
                    raport[layer.name()][
                        "rozbite_multipoligony"
                    ].append(
                        f"{ozn} - rozbito na "
                        f"{liczba_nowych_poligonow} poligonów"
                    )
                    continue
                
                layer.changeGeometry(
                    feature.id(),
                    nowa_geom
                )
                
                self.ustawAtrybutyZmianyObiektuPoUniewaznieniu(
                    layer=layer,
                    feature_id=feature.id(),
                    wersja_id=wersja_id,
                    poczatek_wersji=poczatek_wersji,
                    obowiazuje_od=obowiazuje_od
                )
                
                dodaj_do_raportu(
                    layer.name(),
                    "zmodyfikowane_po_wycieciu",
                    ozn
                )
                
        if not self.aktualizujAktPlanowaniaPrzestrzennegoPoUniewaznieniu(
            layer=warstwa_app,
            wersja_id=wersja_id,
            poczatek_wersji=poczatek_wersji,
            obowiazuje_od=obowiazuje_od,
            edytowane_warstwy=edytowane_warstwy
        ):
            return False
        
        zapisane_warstwy, bledy_zapisu = (
            self.zapiszWszystkieWarstwyPOGDoGML(
                edytowane_warstwy,
                warstwy_do_recznego_zapisu
            )
        )
        
        data_generowania_raportu = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        komunikat = (
            "Raport z unieważnienia\n"
            f"Data i godzina wygenerowania raportu: "
            f"{data_generowania_raportu}\n\n"
            "Raport według warstw:\n"
        )
        
        for nazwa_warstwy in sorted(raport.keys()):
            dane = raport[nazwa_warstwy]
            
            usuniete_wskazane = sorted(
                dane["usuniete_wskazane"]
            )
            zmodyfikowane = sorted(
                dane["zmodyfikowane_po_wycieciu"]
            )
            usuniete_po_wycieciu = sorted(
                dane["usuniete_po_wycieciu"]
            )
            usuniete_ponizej_1_cm2 = sorted(
                dane["usuniete_ponizej_1_cm2"]
            )
            usuniete_czesci_ponizej_1_cm2 = sorted(
                dane["usuniete_czesci_ponizej_1_cm2"]
            )
            rozbite_multipoligony = sorted(
                dane["rozbite_multipoligony"]
            )
            
            komunikat += f"\n{nazwa_warstwy}:\n"
            komunikat += (
                "• Usunięto wskazane obiekty: "
                f"{len(usuniete_wskazane)}\n"
            )
            
            if usuniete_wskazane:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in usuniete_wskazane
                ) + "\n"
                
            komunikat += (
                "• Zmieniono geometrię po wycięciu: "
                f"{len(zmodyfikowane)}\n"
            )
            
            if zmodyfikowane:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in zmodyfikowane
                ) + "\n"
                
            komunikat += (
                "• Usunięto po wycięciu całej geometrii: "
                f"{len(usuniete_po_wycieciu)}\n"
            )
            
            if usuniete_po_wycieciu:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in usuniete_po_wycieciu
                ) + "\n"
                
            if usuniete_ponizej_1_cm2:
                komunikat += "\n".join(
                    f"  • {oznaczenie}"
                    for oznaczenie in usuniete_ponizej_1_cm2
                ) + "\n"
                
            if usuniete_czesci_ponizej_1_cm2:
                komunikat += "\n".join(
                    f"  • {opis}"
                    for opis in usuniete_czesci_ponizej_1_cm2
                ) + "\n"
                
            komunikat += (
                "• Rozbito multipoligony na poligony: "
                f"{len(rozbite_multipoligony)}\n"
            )
            
            if rozbite_multipoligony:
                komunikat += "\n".join(
                    f"  • {opis}"
                    for opis in rozbite_multipoligony
                ) + "\n"
                
        if warstwy_do_recznego_zapisu:
            komunikat += (
                "\nNależy uzupełnić formularz atrybutów dla nowo "
                "powstałych obiektów, a następnie zapisać warstwę "
                "do pliku GML.\n"
            )
            
        komunikat += (
            "\nUstawiono wartości atrybutów dla obiektów zmienionych:"
        )
        komunikat += f"\n• {pole_wersja_id}: {wersja_id}"
        komunikat += f"\n• {pole_poczatek}: {poczatek_wersji}"
        komunikat += (
            f"\n• {pole_obowiazuje_od}: {obowiazuje_od_txt}"
        )
        
        komunikat += self.przygotujRaportAktPlanowaniaPrzestrzennego(
            warstwa_app=warstwa_app,
            wersja_id=wersja_id,
            poczatek_wersji=poczatek_wersji,
            obowiazuje_od=obowiazuje_od
        )
        
        if zapisane_warstwy:
            komunikat += "\n\nZapisano warstwy do GML:\n"
            komunikat += "\n".join(
                f"• {nazwa}"
                for nazwa in sorted(zapisane_warstwy)
            )
            
        if bledy_zapisu:
            komunikat += (
                "\n\nNie udało się zapisać zmian lub GML:\n"
            )
            komunikat += "\n".join(
                f"• {blad}"
                for blad in sorted(bledy_zapisu)
            )
            
        self.pokazRaportUniewaznienia(komunikat)
        return True


    def pobierzDateObowiazujeOdZOkna(self):
        """Pobiera prawidłową datę z pola obowiazujeOd_data jako QDate."""
        
        widget = self.formularzInstrukcjaDialogPOGpoUniewaznieniu.obowiazujeOd_data
        
        try:
            if hasattr(widget, "isNull") and widget.isNull():
                QMessageBox.warning(
                    None,
                    "Brak daty obowiązuje od",
                    "Proszę wskazać datę w polu 'obowiązuje od'."
                )
                return None
        except Exception as e:
            print(e)
        
        data = None
        
        try:
            data = widget.date()
        except Exception:
            try:
                data = widget.dateTime().date()
            except Exception:
                data = None
                
        if data is None or not data.isValid():
            QMessageBox.warning(
                None,
                "Brak daty obowiązuje od",
                "Nie udało się odczytać prawidłowej daty z pola 'obowiązuje od'."
            )
            return None
        
        return QDate(data)


    def znajdzWarstwePoPrefiksie(self, prefiks):
        """Zwraca pierwszą warstwę projektu, której nazwa rozpoczyna się od prefiksu."""
        
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().startswith(prefiks):
                return layer
            
        return None


    def pobierzWarstweAktPlanowaniaPrzestrzennegoDoAktualizacji(self):
        """Pobiera warstwę APP i sprawdza pola wymagane do aktualizacji."""
        
        warstwa_app = None
        
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().startswith("AktPlanowaniaPrzestrzennego"):
                warstwa_app = layer
                break
                
        if warstwa_app is None:
            QMessageBox.warning(
                None,
                "Brak warstwy AktPlanowaniaPrzestrzennego",
                "Nie znaleziono warstwy, której nazwa rozpoczyna się od "
                "'AktPlanowaniaPrzestrzennego'."
            )
            return None
            
        wymagane_pola = {
            "obowiazujeOd",
            "wersjaId",
            "modyfikacja",
            "poczatekWersjiObiektu",
        }
        pola_warstwy = {
            field.name()
            for field in warstwa_app.fields()
        }
        brakujace_pola = sorted(wymagane_pola - pola_warstwy)
        
        if brakujace_pola:
            QMessageBox.warning(
                None,
                "Brak wymaganych pól",
                "Warstwa AktPlanowaniaPrzestrzennego nie zawiera pól:\n"
                + "\n".join(
                    f"• {nazwa_pola}"
                    for nazwa_pola in brakujace_pola
                )
            )
            return None
            
        return warstwa_app



    def rozpocznijEdycjeWarstwyPoUniewaznieniu(self, layer, edytowane_warstwy):
        """Uruchamia edycję warstwy i rejestruje ją do późniejszego zatwierdzenia."""
        
        if layer is None:
            return False
        
        if not layer.isEditable() and not layer.startEditing():
            QMessageBox.warning(
                None,
                "Błąd edycji warstwy",
                f"Nie udało się rozpocząć edycji warstwy {layer.name()}."
            )
            return False
        
        edytowane_warstwy.add(layer)
        return True


    def ustawAtrybutyZmianyObiektuPoUniewaznieniu(self, layer, feature_id, wersja_id, poczatek_wersji, obowiazuje_od, ustaw_modyfikacje=False):
        """Ustawia wspólne atrybuty wersjonowania dla zmienionego obiektu."""
        
        wartosci = {
            "wersjaId": wersja_id,
            "poczatekWersjiObiektu": poczatek_wersji,
            "obowiazujeOd": obowiazuje_od,
        }
        
        if ustaw_modyfikacje:
            wartosci["modyfikacja"] = True
            
        for nazwa_pola, wartosc in wartosci.items():
            indeks_pola = layer.fields().indexFromName(nazwa_pola)
            
            if indeks_pola != -1:
                layer.changeAttributeValue(
                    feature_id,
                    indeks_pola,
                    wartosc
                )


    def aktualizujAktPlanowaniaPrzestrzennegoPoUniewaznieniu(self, layer, wersja_id, poczatek_wersji, obowiazuje_od, edytowane_warstwy):
        """Aktualizuje atrybuty obiektów warstwy AktPlanowaniaPrzestrzennego."""
        
        if layer is None:
            return False
            
        if not layer.isEditable() and not layer.startEditing():
            QMessageBox.warning(
                None,
                "Błąd edycji warstwy",
                "Nie udało się rozpocząć edycji warstwy "
                f"{layer.name()}."
            )
            return False
            
        indeks_wersja_id = layer.fields().indexFromName("wersjaId")
        indeks_poczatek = layer.fields().indexFromName(
            "poczatekWersjiObiektu"
        )
        indeks_obowiazuje_od = layer.fields().indexFromName(
            "obowiazujeOd"
        )
        indeks_modyfikacja = layer.fields().indexFromName(
            "modyfikacja"
        )
        
        for feature in layer.getFeatures():
            layer.changeAttributeValue(
                feature.id(),
                indeks_wersja_id,
                wersja_id
            )
            layer.changeAttributeValue(
                feature.id(),
                indeks_poczatek,
                poczatek_wersji
            )
            layer.changeAttributeValue(
                feature.id(),
                indeks_obowiazuje_od,
                obowiazuje_od
            )
            layer.changeAttributeValue(
                feature.id(),
                indeks_modyfikacja,
                True
            )
            
        edytowane_warstwy.add(layer)
        return True


    def zapiszWszystkieWarstwyPOGDoGML(
        self,
        edytowane_warstwy,
        warstwy_do_recznego_zapisu=None
    ):
        """
        Zatwierdza zmiany i zapisuje warstwy POG do podkatalogu unieważnienia.

        Warstwy zawierające nowe obiekty bez oznaczenia są pomijane zarówno
        podczas commitChanges(), jak i podczas automatycznego zapisu GML.
        Pozostają w trybie edycji do ręcznego uzupełnienia przez użytkownika.
        """
        
        zapisane_warstwy = []
        bledy_zapisu = []
        warstwy_z_bledem_commit = set()
        warstwy_do_recznego_zapisu = set(
            warstwy_do_recznego_zapisu or []
        )
        
        for layer in edytowane_warstwy:
            if layer.id() in warstwy_do_recznego_zapisu:
                continue
            
            try:
                if layer.isEditable() and not layer.commitChanges():
                    bledy_zapisu.append(
                        f"{layer.name()} - błąd commitChanges()"
                    )
                    warstwy_z_bledem_commit.add(layer.id())
            except Exception as e:
                bledy_zapisu.append(
                    f"{layer.name()} - błąd zatwierdzania zmian: {e}"
                )
                warstwy_z_bledem_commit.add(layer.id())
                
        ustawienia = QgsSettings()
        katalog_nadrzedny = ustawienia.value(
            "qgis_app2/settings/defaultPath",
            "/"
        )
        
        if not katalog_nadrzedny:
            katalog_nadrzedny = "/"
            
        if not os.path.isdir(katalog_nadrzedny):
            katalog_z_pliku = os.path.dirname(katalog_nadrzedny)
            
            if katalog_z_pliku and os.path.isdir(katalog_z_pliku):
                katalog_nadrzedny = katalog_z_pliku
            else:
                katalog_nadrzedny = "/"
                
        znacznik_czasu = QDateTime.currentDateTimeUtc().toPyDateTime().strftime(
            "%Y%m%d_%H%M%S"
        )
        
        nazwa_podkatalogu = (
            "unieważnienie_"
            + znacznik_czasu
        )
        
        katalog_uniewaznienia = os.path.join(
            katalog_nadrzedny,
            nazwa_podkatalogu
        )
        
        numer_katalogu = 2
        bazowy_katalog_uniewaznienia = katalog_uniewaznienia
        
        while os.path.exists(katalog_uniewaznienia):
            katalog_uniewaznienia = (
                bazowy_katalog_uniewaznienia
                + "_"
                + str(numer_katalogu)
            )
            numer_katalogu += 1
            
        try:
            os.makedirs(
                katalog_uniewaznienia,
                exist_ok=False
            )
        except Exception as e:
            bledy_zapisu.append(
                "Nie udało się utworzyć katalogu zapisu: "
                f"{katalog_uniewaznienia} - {e}"
            )
            return zapisane_warstwy, bledy_zapisu
        
        # Zapamiętanie katalogu, aby raport został zapisany
        # dokładnie obok plików GML.
        self.katalog_uniewaznienia = katalog_uniewaznienia
        
        konfiguracja_zapisu = [
            (
                "AktPlanowaniaPrzestrzennego",
                "AktPlanowaniaPrzestrzennego.gml",
                self.wektorInstrukcjaDialogPOG
            ),
            (
                "StrefaPlanistyczna",
                "StrefaPlanistyczna.gml",
                self.wektorInstrukcjaDialogSPL
            ),
            (
                "ObszarUzupelnieniaZabudowy",
                "ObszarUzupelnieniaZabudowy.gml",
                self.wektorInstrukcjaDialogOUZ
            ),
            (
                "ObszarZabudowySrodmiejskiej",
                "ObszarZabudowySrodmiejskiej.gml",
                self.wektorInstrukcjaDialogOZS
            ),
            (
                "ObszarStandardowDostepnosciInfrastrukturySpolecznej",
                "ObszarStandardowDostepnosciInfrastrukturySpolecznej.gml",
                self.wektorInstrukcjaDialogOSD
            ),
        ]
        
        poprzedni_katalog_zapisu = ustawienia.value(
            "qgis_app2/settings/defaultPath",
            "/"
        )
        
        poprzednie_okno = self.activeDlg
        
        poprzednia_warstwa_obrysu = getattr(
            self,
            "obrysLayer",
            None
        )
        
        # Zapamiętanie warstwy wskazanej wcześniej w formularzu POG.
        poprzednia_warstwa_pog = (
            self.wektorInstrukcjaDialogPOG
            .layers_comboBox.currentLayer()
        )
        
        # Pobranie dokładnie tej warstwy APP, która została
        # zaktualizowana podczas bieżącej operacji unieważnienia.
        warstwa_pog_do_kontroli = next(
            (
                layer
                for layer in edytowane_warstwy
                if layer.name().startswith(
                    "AktPlanowaniaPrzestrzennego"
                )
            ),
            None
        )
        
        try:
            # saveLayerToGML pobiera katalog z ustawień,
            # dlatego na czas zapisu wskazujemy podkatalog unieważnienia.
            ustawienia.setValue(
                "qgis_app2/settings/defaultPath",
                katalog_uniewaznienia
            )
            
            # Wszystkie kontrole SPL, OUZ, OZS i OSD muszą być
            # wykonywane względem granicy APP z bieżącego POG,
            # a nie względem warstwy wcześniej wskazanej w formularzu.
            if warstwa_pog_do_kontroli is not None:
                self.wektorInstrukcjaDialogPOG.layers_comboBox.setLayer(
                    warstwa_pog_do_kontroli
                )
                
            for prefiks, nazwa_pliku, dialog in konfiguracja_zapisu:
                layer = self.znajdzWarstwePoPrefiksie(
                    prefiks
                )
                
                if layer is None:
                    continue
                
                # Warstwa zawiera nowo utworzone obiekty bez oznaczenia.
                # Nie zatwierdzamy jej zmian i nie zapisujemy automatycznie
                # do GML. Użytkownik zrobi to po uzupełnieniu formularzy.
                if layer.id() in warstwy_do_recznego_zapisu:
                    continue
                
                if layer.id() in warstwy_z_bledem_commit:
                    continue
                
                poprzednia_warstwa_dialogu = (
                    dialog.layers_comboBox.currentLayer()
                )
                
                try:
                    dialog.layers_comboBox.setLayer(
                        layer
                    )
                    
                    self.activeDlg = dialog
                    self.obrysLayer = layer
                    
                    self.saveLayerToGML(
                        nazwa_pliku
                    )
                    
                    sciezka_pliku = os.path.join(
                        katalog_uniewaznienia,
                        nazwa_pliku
                    )
                    
                    if os.path.isfile(sciezka_pliku):
                        zapisane_warstwy.append(
                            nazwa_pliku
                        )
                    else:
                        bledy_zapisu.append(
                            f"{layer.name()} - nie utworzono pliku "
                            f"{sciezka_pliku}"
                        )
                        
                except Exception as e:
                    bledy_zapisu.append(
                        f"{layer.name()} - {e}"
                    )
                    
                finally:
                    try:
                        dialog.layers_comboBox.setLayer(
                            poprzednia_warstwa_dialogu
                        )
                    except Exception as e:
                        print(e)
                        
        finally:
            # Przywrócenie poprzedniego katalogu domyślnego,
            # aby nie zmieniać ustawień użytkownika.
            ustawienia.setValue(
                "qgis_app2/settings/defaultPath",
                poprzedni_katalog_zapisu
            )
            
            try:
                self.wektorInstrukcjaDialogPOG.layers_comboBox.setLayer(
                    poprzednia_warstwa_pog
                )
            except Exception as e:
                print(e)
                
            self.activeDlg = poprzednie_okno
            self.obrysLayer = poprzednia_warstwa_obrysu
            
        return zapisane_warstwy, bledy_zapisu


    def zapiszRaportUniewaznieniaJako(self, raport, parent=None):
        """Zapisuje raport w podkatalogu zawierającym pliki GML unieważnienia."""
        
        katalog_uniewaznienia = getattr(
            self,
            "katalog_uniewaznienia",
            None
        )
        
        if not katalog_uniewaznienia:
            QMessageBox.warning(
                parent,
                "Brak katalogu unieważnienia",
                "Nie znaleziono katalogu, do którego zapisano pliki GML."
            )
            return
        
        if not os.path.isdir(katalog_uniewaznienia):
            QMessageBox.warning(
                parent,
                "Brak katalogu unieważnienia",
                "Katalog zapisu plików GML nie istnieje:\n"
                f"{katalog_uniewaznienia}"
            )
            return
        
        sciezka_raportu = os.path.join(
            katalog_uniewaznienia,
            "raport_uniewaznienia.txt"
        )
        
        try:
            with open(
                sciezka_raportu,
                "w",
                encoding="utf-8"
            ) as plik:
                plik.write(raport)
            
            QMessageBox.information(
                parent,
                "Zapis raportu",
                "Zapisano raport oraz pliki GML w podkatalogu:\n"
                f"{katalog_uniewaznienia}\n\n"
                "Plik raportu:\n"
                f"{sciezka_raportu}"
            )
        
        except Exception as e:
            QMessageBox.critical(
                parent,
                "Błąd zapisu raportu",
                "Nie udało się zapisać raportu.\n\n"
                f"Szczegóły błędu:\n{e}"
            )


    def pokazRaportUniewaznienia(self, raport):
        """Wyświetla raport w oknie z przyciskiem Zapisz jako."""
        
        dialog = QDialog(
            self.formularzInstrukcjaDialogPOGpoUniewaznieniu
        )
        dialog.setWindowTitle("Raport z unieważnienia")
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        pole_raportu = QPlainTextEdit(dialog)
        pole_raportu.setReadOnly(True)
        pole_raportu.setPlainText(raport)
        layout.addWidget(pole_raportu)
        
        przyciski = QDialogButtonBox(dialog)
        zapisz_jako_btn = przyciski.addButton(
            "Zapisz jako",
            QDialogButtonBox.ActionRole
        )
        zamknij_btn = przyciski.addButton(
            "Zamknij",
            QDialogButtonBox.RejectRole
        )
        layout.addWidget(przyciski)
        
        zapisz_jako_btn.clicked.connect(
            lambda: self.zapiszRaportUniewaznieniaJako(
                raport,
                dialog
            )
        )
        zamknij_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()


    def przygotujRaportAktPlanowaniaPrzestrzennego(self, warstwa_app, wersja_id, poczatek_wersji, obowiazuje_od):
        """Zwraca sekcję raportu dotyczącą warstwy APP."""
        
        obowiazuje_od_txt = obowiazuje_od.toString("yyyy-MM-dd")
        
        return (
            f"\n\nWarstwa {warstwa_app.name()}:"
            f"\n• Wartość atrybutu wersjaId: {wersja_id}"
            f"\n• Wartość atrybutu poczatekWersjiObiektu: "
            f"{poczatek_wersji}"
            f"\n• Wartość atrybutu obowiazujeOd: "
            f"{obowiazuje_od_txt}"
            "\n• Wartość atrybutu modyfikacja: prawda"
        )