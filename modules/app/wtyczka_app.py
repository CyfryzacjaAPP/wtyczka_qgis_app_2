# -*- coding: utf-8 -*-
from qgis.utils import iface
from . import (PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog, WektorInstrukcjaDialogPOG,
               WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog,
               WektorInstrukcjaDialogSPL, WektorInstrukcjaDialogOUZ, WektorInstrukcjaDialogOZS, WektorInstrukcjaDialogOSD)

from .app_utils import isLayerInPoland, czyWarstwaMaWypelnioneObowiazkoweAtrybuty, kontrolaZaleznosciAtrybutow
from .. import BaseModule, utils, Formularz
from ..utils import showPopup
from ..models import AppTableModel
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.core import *
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit
import os
import os.path
import sys
import pathlib
import time
from datetime import datetime
import xml.etree.ElementTree as ET
import random
import ntpath
from .. import dictionaries
from qgis.core import QgsSettings
from shutil import copyfile
import copy
from osgeo import ogr
from qgis import processing
from PyQt5.QtCore import QSettings
from ..tworzenieOUZ.dialogs import TworzenieOUZDialog


class AppModule(BaseModule):
    metadaneDialog = None
    
    global s, rodzajZbioru, numerZbioru, jpt, idLokalnyAPP, defaultPath, warstwaPOG
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
    numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
    jpt = s.value("qgis_app2/settings/jpt", "")
    idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
    defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
    QSettings().setValue('/Map/identifyAutoFeatureForm','true')
    warstwaPOG = None


    def __init__(self, iface):
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
    
    # endregion
    # region pytanieAppDialog
        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)
        self.pytanieAppDialog.load_btn.clicked.connect(self.pytanieAppDialog_load_btn_clicked)
    
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
        self.generowanieGMLDialog.generate_btn.clicked.connect(
            self.generateAPP)
        self.generowanieGMLDialog.addElement_btn.clicked.connect(
            self.addTableContentGML)
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(
            self.deleteTableContentGML)
    
        # rozszerzanie kolumn
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        for i in range(header_gml.count()):
            header_gml.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)
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
        self.wektorInstrukcjaDialogPOG.loadLayerEdit.clicked.connect(
            self.loadFromGMLorGPKG)
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
        self.wektorInstrukcjaDialogSPL.loadLayerEdit.clicked.connect(
            self.loadFromGMLorGPKG)
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
        self.wektorInstrukcjaDialogOUZ.loadLayerEdit.clicked.connect(
            self.loadFromGMLorGPKG)
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
        self.wektorInstrukcjaDialogOZS.loadLayerEdit.clicked.connect(
            self.loadFromGMLorGPKG)
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
        self.wektorInstrukcjaDialogOSD.loadLayerEdit.clicked.connect(
            self.loadFromGMLorGPKG)
        self.wektorInstrukcjaDialogOSD.saveLayer.clicked.connect(
            self.saveLayerToGML)
        self.wektorInstrukcjaDialogOSD.skip_btn.clicked.connect(
            self.wektorInstrukcjaDialog_skip_btn_clicked)
        self.wektorInstrukcjaDialogOSD.generateTemporaryLayer_btn.clicked.connect(
            self.newEmptyLayer)
        self.wektorInstrukcjaDialogOSD.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer)
    # endregion
    
    """Event handlers"""

    # region pytanieAppDialog

    def pytanieAppDialog_app_btn_clicked(self):
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
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)


    def pytanieAppDialog_load_btn_clicked(self):
        self.loadFromGMLorGPKG()

    # endregion

    # region rasterInstrukcjaDialog
    def rasterInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)
        self.listaOkienek.append(self.rasterInstrukcjaDialog)


    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    # endregion

    # region rasterFormularzDialog
    def rasterFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())


    def rasterFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)
        self.listaOkienek.append(self.rasterFormularzDialog)


    def rasterFormularzDialog_clear_btn_clicked(self):
        self.rasterFormularzDialog.clearForm(self.rasterFormularzDialog.form_scrollArea)
        self.rasterFormularzDialog.setDefaultValues()

    # endregion

    # region wektorInstrukcjaDialog

    def wektorInstrukcjaDialog_next_btn_clicked(self):
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
                                formItem.setCurrentIndex(value)
                        except:
                            pass
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
                                    formItem.setCurrentIndex(value)
                            except:
                                pass
            if rodzajZbioru == 'POG':
                self.listaOkienek.append(self.wektorInstrukcjaDialogPOG)
            else:
                self.listaOkienek.append(self.wektorInstrukcjaDialog)


    def wektorInstrukcjaDialogSPL_next_btn_clicked(self):
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
        self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
        if not self.obrysLayer:   # brak wybranej warstwy
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy z ObszarStandardowDostepnosciInfrastrukturySpolecznej.")
            return
        
        if self.kontrolaGeometriiWarstwy(self.obrysLayer):
            if rodzajZbioru == 'POG' and self.OSD_GML_saved == False:
                showPopup("Błąd warstwy obrysu",
                          "Warstwa nie została zapisana do GML.")
            else:
                self.openNewDialog(self.dokumentyFormularzDialog)
                self.obrysLayer = self.wektorInstrukcjaDialogOSD.layers_comboBox.currentLayer()
                self.listaOkienek.append(self.wektorInstrukcjaDialogOSD)


    def wektorInstrukcjaDialog_prev_btn_clicked(self):
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
        self.openNewDialog(self.listaOkienek.pop())


    def wektorFormularzDialog_next_btn_clicked(self):
        if rodzajZbioru == 'POG':
            self.openNewDialog(self.generowanieGMLDialog)
        else:
            self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)


    def wektorFormularzDialog_clear_btn_clicked(self):
        self.wektorFormularzDialog.clearForm(
            self.wektorFormularzDialog.form_scrollArea)
        self.wektorFormularzDialog.setDefaultValues()

    # endregion

    # region dokumentyFormularzDialog
    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())


    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)


    def dokumentyFormularzDialog_clear_btn_clicked(self):
        self.dokumentyFormularzDialog.clearForm(self.dokumentyFormularzDialog.form_scrollArea)
        self.dokumentyFormularzDialog.setDefaultValues()

    # endregion

    # region generowanieGMLDialog
    def generowanieGMLDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())


    def generowanieGMLDialog_next_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.generowanieGMLDialog)


    def makeAnotherApp_radioBtn_toggled(self, setYes):
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
        if setYes:  # finalne tworzenie zbioru app
            self.generowanieGMLDialog.next_btn.setText("Dalej")
        else:  # zakończ działanie wtyczki
            self.generowanieGMLDialog.next_btn.setText("Zakończ")

    # endregion

    # region zbiorPrzygotowanieDialog
    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())


    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)
        self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
        self.metadaneDialog.prev_btn.setEnabled(True)


    def validateAndGenerate_btn_clicked(self):
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
            self.fn = QFileDialog.getSaveFileName(
                directory=defaultPath, filter="pliki GML (*.gml)")[0]
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
        with open(file_path, 'rb') as file:
            content = file.read().decode('utf-8')
        
        old_namespace = b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0'
        new_namespace = b'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0'
        
        if old_namespace.decode('utf-8') in content:
            # Zamiana przestrzeni nazw
            updated_content = content.replace(old_namespace.decode('utf-8'), new_namespace.decode('utf-8'))
        
            # Zapisz zmienioną zawartość do nowego pliku
            dir_name, base_name = os.path.split(file_path)
            base_name = "tmp_" + base_name
            new_file_path = os.path.join(dir_name, base_name)
        
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
        else:
            new_file_path = file_path
        
        return new_file_path

    # endregion

    """Helper methods"""


    def getFormValues(self):
        plik = str(QFileDialog.getOpenFileName(filter="pliki XML/GML (*.xml *.gml)")[0])
        if plik:
            formElements = self.activeDlg.formElements
            self.activeDlg.clearForm(self.activeDlg.form_scrollArea)
            utils.loadItemsToForm(plik, formElements)


    def addTableContentGML(self):
        files = QFileDialog.getOpenFileNames(
            filter="pliki XML/GML (*.xml *.gml)")[0]
        for file in files:
            plik = str(file)
            param = True
            docNames = {
                'AktPlanowaniaPrzestrzennego': 'APP',
                'RysunekAktuPlanowaniaPrzestrzennego': 'Rysunek APP',
                'DokumentFormalny': 'Dokument Formalny',
                'StrefaPlanistyczna':'Strefa Planistyczna',
                'ObszarUzupelnieniaZabudowy':'Obszar Uzupelnienia Zabudowy',
                'ObszarZabudowySrodmiejskiej':'Obszar Zabudowy Srodmiejskiej',
                'ObszarStandardowDostepnosciInfrastrukturySpolecznej':'Obszar Standardow Dostepnosci Infrastruktury Spolecznej'
            }
            try:
                docName = utils.getDocType(plik)
            except:
                docName = ''
            if plik:
                if docName == '':
                    utils.showPopup(title='Błędny plik',text='Wczytano błędny plik: %s' % plik)
                elif docName in docNames.keys():
                    rows = self.generowanieGMLDialog.filesTable_widget.rowCount()
                    if rows > 0:
                        for i in range(rows):
                            item = self.generowanieGMLDialog.filesTable_widget.item(
                                i, 0).toolTip()
                            if plik == item:
                                param = False
                                showPopup("Błąd tabeli","Wybrany plik znajduje się już w tabeli")
                                break
                        if param:
                            self.tableContentGML(plik, rows)
                    else:
                        self.tableContentGML(plik, rows)


    def tableContentGML(self, file, rows):
        # data modyfikacji
        def path_leaf(file):
            head, tail = ntpath.split(file)
            return tail or ntpath.basename(head)
        file2 = path_leaf(file)
        flags = Qt.ItemFlags(32)
        self.generowanieGMLDialog.filesTable_widget.setRowCount(rows + 1)
        self.generowanieGMLDialog.filesTable_widget.setItem(
            rows, 0, QTableWidgetItem(file2))
        test = self.generowanieGMLDialog.filesTable_widget.item(rows, 0)
        test.setToolTip(file)
        
        t = os.path.getmtime(file)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        item = QTableWidgetItem(mtime)
        item.setFlags(flags)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 2, item)
        
        # Ustawianie rodzaju dokumentu
        docNames = {
                    'AktPlanowaniaPrzestrzennego': 'APP',
                    'RysunekAktuPlanowaniaPrzestrzennego': 'Rysunek APP',
                    'DokumentFormalny': 'Dokument Formalny',
                    'StrefaPlanistyczna':'Strefa Planistyczna',
                    'ObszarUzupelnieniaZabudowy':'Obszar Uzupelnienia Zabudowy',
                    'ObszarZabudowySrodmiejskiej':'Obszar Zabudowy Srodmiejskiej',
                    'ObszarStandardowDostepnosciInfrastrukturySpolecznej':'Obszar Standardow Dostepnosci Infrastruktury Spolecznej'
                   }
        
        docName = docNames[utils.getDocType(file)]
        
        rodzaj = ['Dokument Formalny', 'APP', 'Rysunek APP', 'Strefa Planistyczna', 'Obszar Uzupelnienia Zabudowy', 'Obszar Zabudowy Srodmiejskiej', 'Obszar Standardow Dostepnosci Infrastruktury Spolecznej']
        item2 = QTableWidgetItem(docName)
        item2.setFlags(flags)
        self.generowanieGMLDialog.filesTable_widget.setItem(rows, 1, item2)
        
        # relacja z APP
        if self.generowanieGMLDialog.filesTable_widget.item(rows, 1).text() == 'Dokument Formalny':
            c = QComboBox()
            c.addItems(dictionaries.relacjeDokumentu.keys())
            i = self.generowanieGMLDialog.filesTable_widget.model().index(rows, 3)
            self.generowanieGMLDialog.filesTable_widget.setCellWidget(
                rows, 3, c)
        else:
            empty = QTableWidgetItem('')
            empty.setFlags(flags)
            self.generowanieGMLDialog.filesTable_widget.setItem(rows, 3, empty)


    def deleteTableContentGML(self):
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.generowanieGMLDialog.filesTable_widget.currentRow()
            self.generowanieGMLDialog.filesTable_widget.removeRow(do_usuniecia)
            self.generowanieGMLDialog.filesTable_widget.setCurrentCell(-1, -1)
        else:
            pass


    def getTableContent(self):
        content = []
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        for i in range(row_num):
            item = self.generowanieGMLDialog.filesTable_widget.item(
                i, 0).toolTip()
            try:
                relation = self.generowanieGMLDialog.filesTable_widget.cellWidget(
                    i, 3).currentText()
            except:
                relation = ''
            content.append([item, relation])
        return content  # ścieżki do plików


    def generateAPP(self):  # Generowanie pliku z APP
        docList = self.getTableContent()
        if len(docList) == 0:
            utils.showPopup(title='Brak Dokumentów',text='Do tabeli nie zostały dodane żadne dokumenty.')
        else:
            uchwala_count = 0
            przystapienie_count = 0
            for doc, rel in docList:
                if rel == 'uchwala':
                    uchwala_count += 1
                    
                if rel == 'przystąpienie':
                    przystapienie_count += 1
            uchwala_przystapienie_count = przystapienie_count + uchwala_count
            if not utils.validateObjectNumber(files=docList):
                pass
            elif not utils.validatePrzestrzenNazwAppSet(files=docList):
                utils.showPopup('Błąd przestrzeni nazw','Obiekty pochodzą z różnych przestrzeni nazw.')
            elif not utils.validateDokumentFormalnyDate(files=docList):
                utils.showPopup('Błąd relacji dokumentów','Dokument z relacją uchwala nie może być starszy od dokumentu z relacją przystąpienie.')
            elif uchwala_przystapienie_count == 0:
                utils.showPopup(
                    title='Błąd relacji dokumentów', text='Wymagany jest co najmniej jeden dokument z relacją "przystąpienie" lub "uchwala".')
            elif uchwala_count > 1:
                utils.showPopup(
                    title='Błąd relacji dokumentów', text='W APP dozwolony jest tylko jeden dokument z relacją "uchwala".')
            else:
                defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
                self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="GML Files (*.gml)")[0]
                if self.fn:
                    xml_string = utils.mergeDocsToAPP(docList)
                    if xml_string != '':
                        myfile = open(self.fn, "w", encoding='utf-8')
                        myfile.write(xml_string)
                        self.showPopupApp()


    def loadSet(self):
        setPath = self.zbiorPrzygotowanieDialog.addFile_widget.filePath()
        param = True
        if setPath:
            for iip in utils.setAppId(setPath):
                rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
                if rows > 0:
                    for i in range(rows):
                        item = self.zbiorPrzygotowanieDialog.appTable_widget.item(
                            i, 0).text()
                        if iip == item:
                            param = False
                            showPopup("Błąd tabeli","Wybrany plik znajduje się już w tabeli")
                            break
                    if param:
                        self.tableContentAddSet(iip+' (Zbiór)', setPath, rows)
                else:
                    self.tableContentAddSet(iip+' (Zbiór)', setPath, rows)


    def addTableContentSet(self):
        files = QFileDialog.getOpenFileNames(
            filter="pliki XML/GML (*.xml *.gml)")[0]
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
                    utils.showPopup(
                        'Błąd wczytanego pliku', 'Wczytany plik: \n%s\nnie jest aktem planowania przestrzennego.' % plik)


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
        if rodzajZbioru == 'POG':
            pomijane = ['zmiana', 'mapaPodkladowa', 'data', 'referencja', 'lacze',
                        'dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy', 'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy']
        else:
            pomijane = ['zmiana', 'mapaPodkladowa', 'data', 'referencja', 'lacze',
                        'dokument', 'dokumentPrzystepujacy', 'dokumentUchwalajacy', 'dokumentZmieniajacy', 'dokumentUchylajacy', 'dokumentUniewazniajacy','wydzielenie']
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
        s = QgsSettings()
        epsg = s.value("qgis_app2/settings/strefaPL2000", "")
        
        layer = QgsVectorLayer(
            'multipolygon?crs=epsg:' + str(epsg) + self.fieldsDefinition(fields=fields), 'granice_app', 'memory')


    def newEmptyLayer(self):
        s = QgsSettings()
        epsg = str(s.value("qgis_app2/settings/strefaPL2000", ""))
        geomTypeEPSG = 'polygon?crs=epsg:' + epsg
        
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(int(epsg)))
        
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        if not os.access(defaultPath, os.W_OK):
            showPopup("Wygeneruj warstwę","Brak uprawnień do zapisu w katalogu "+defaultPath+". W ustawieniach wtyczki wskaż domyślną ścieżkę zapisu plików z uprawnieniami do zapisu.")
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
        showPopup("Wygeneruj warstwę","Poprawnie utworzono pustą warstwę " + popup_txt + ". Uzupełnij ją danymi przestrzennymi.")

    """Popup windows"""


    def showPopupSaveForm(self):
        if utils.isFormFilled(self.activeDlg) and utils.validate_form_dates(self.activeDlg.formElements) and utils.validate_status(self.activeDlg.formElements) and utils.validate_typPlanu(self.activeDlg.formElements):
            s = QgsSettings()
            defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
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
        alg_params = {
            'AGGREGATES': [],
            'GROUP_BY': 'NULL',
            'INPUT': layer,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        import processing
        aggregated = processing.run('qgis:aggregate', alg_params)
        aggregated['OUTPUT'].setName('granice_app_zagregowane')
        QgsProject.instance().addMapLayer(aggregated['OUTPUT'])


    def showPopupApp(self):
        # Popup generowanie APP
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
            self.listaOkienek.append(self.generowanieGMLDialog)
        elif msg.clickedButton() is no:
            self.showPopupSet()


    def showPopupSet(self):
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
            self.listaOkienek.append(self.generowanieGMLDialog)
        elif msg.clickedButton() is quit:
            self.generowanieGMLDialog.close()


    def wektorInstrukcjaDialogSPLcheckSaveForms(self):
        def findElement(formElements, name):
            for formElement in formElements:
                if formElement.name == name:
                    return formElement
                for inner in formElement.innerFormElements:
                    if inner.name == name:
                        return inner
            return None


    def checkSaveForms(self):
        def findElement(formElements, name):
            for formElement in formElements:
                if formElement.name == name:
                    return formElement
                for inner in formElement.innerFormElements:
                    if inner.name == name:
                        return inner
            return None

        def setValue(formElement1, formElement2):
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
            self.saved = False
        else:
            self.showPopupSaveForms()
        
        # Przenoszenie wartości między formularzami.
        setValue(findElement(self.rasterFormularzDialog.formElements, 'przestrzenNazw'),
                 findElement(self.wektorFormularzDialog.formElements, 'przestrzenNazw'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'przestrzenNazw'),
                 findElement(self.dokumentyFormularzDialog.formElements, 'przestrzenNazw'))
        
        setValue(findElement(self.rasterFormularzDialog.formElements, 'poczatekWersjiObiektu'),
                 findElement(self.wektorFormularzDialog.formElements, 'poczatekWersjiObiektu'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'koniecWersjiObiektu'),
                 findElement(self.wektorFormularzDialog.formElements, 'koniecWersjiObiektu'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'obowiazujeOd'),
                 findElement(self.wektorFormularzDialog.formElements, 'obowiazujeOd'))
        setValue(findElement(self.rasterFormularzDialog.formElements, 'obowiazujeDo'),
                 findElement(self.wektorFormularzDialog.formElements, 'obowiazujeDo'))
        return self.saved


    def showPopupSaveForms(self):
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


    def checkSaveSet(self):
        if self.generated:
            self.openNewDialog(self.metadaneDialog)
            self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
            self.generated = False
        else:
            self.showPopupSaveSet()
        return False


    def showPopupSaveSet(self):
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


    def loadFromGMLorGPKG(self):
        s = QgsSettings()
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        epsg_code = s.value("qgis_app2/settings/strefaPL2000", "/")
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "/")
        
        if not os.access(defaultPath, os.W_OK):
            showPopup("Wczytaj warstwę","Brak uprawnień do zapisu w katalogu " + defaultPath + ". W ustawieniach wtyczki wskaż domyślną ścieżkę zapisu plików z uprawnieniami do zapisu.")
            return
        
        file, format = QFileDialog.getOpenFileName(directory=defaultPath,filter="pliki GML (*.gml);; pliki GeoPackage (*.gpkg);")
        file = str(file)
        
        ds = ogr.Open(file)
        if ds == None:
            return
        
        warstwy = [x.GetName() for x in ds]
        activeDlgname = self.activeDlg.name
        if activeDlgname not in warstwy and activeDlgname != 'PytanieAppDialog':
            showPopup("Wczytaj warstwę","Proszę wskazać plik gml zawierający: " + activeDlgname)
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
        
        for layerName in warstwy:
            for dozwolonaWarstwa in dozwoloneWarstwy:
                if layerName.startswith(dozwolonaWarstwa):
                    layerName = dozwolonaWarstwa
            if rodzajZbioru != 'POG' and layerName == 'AktPlanowaniaPrzestrzennego':
                layer_QML_Name = 'granice_app'
            else:
                layer_QML_Name = layerName
            geomTypeEPSG = 'polygon?crs=epsg:' + epsg_code
            geomType = 'Polygon'
            if file and layerName in dozwoloneWarstwy and activeDlgname in [layerName, 'PytanieAppDialog']:
                field_edycja = utils.createEditField()
                if layerName == 'AktPlanowaniaPrzestrzennego':
                    fields = utils.createFormElements('AktPlanowaniaPrzestrzennegoType') + field_edycja
                    geomType = 'MultiPolygon'
                    geomTypeEPSG = 'multipolygon?crs=epsg:' + epsg_code
                if layerName == 'DokumentFormalny':
                    fields = utils.createFormElements('DokumentFormalnyType') + field_edycja
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
                
                layers = QgsProject.instance().mapLayers()
                i = 0
                for layer in layers.values():
                    if layer.name().startswith(layerName):
                        i += 1
                
                numerWarstwy = ''
                if i > 0:
                    numerWarstwy = '_' + str(i)
                
                pathQML = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/QML/" + layer_QML_Name + ".qml")
                if format == 'pliki GML (*.gml)':
                    pathGFS = pathlib.Path(QgsApplication.qgisSettingsDirPath())/pathlib.Path("python/plugins/wtyczka_qgis_app/GFS/")
                    copyfile(pathGFS/pathlib.Path("template.gfs"), file.replace(".xml",".gfs").replace(".XML",".gfs").replace(".gml",".gfs").replace(".GML",".gfs"))
                    layer = QgsVectorLayer(file + "|layername=" + layerName + "|option:FORCE_SRS_DETECTION=YES|option:CONSIDER_EPSG_AS_URN=YES|geometrytype=" + geomType, layerName + numerWarstwy, 'ogr')
                
                if format == 'pliki GeoPackage (*.gpkg);':
                    layer = QgsVectorLayer(file, layerName + numerWarstwy, 'ogr')
                    if geomType == 'Polygon':
                        layer = processing.run("native:multiparttosingleparts", {'INPUT': layer, 'OUTPUT': 'memory:'})['OUTPUT']
                
                if geomType != 'NoGeometry':
                    try:
                        newEPSG = layer.crs().authid().split(":")[1]
                    except:
                        return
                    if epsg_code != newEPSG:
                        odp = QMessageBox.question(None,'Wczytanie warstwy do edycji',
                                                     "Układ współrzędnych wczytywanej warstwy jest inny od układu współrzędnych przyjętego na podstawie ustawień wtyczki APP.\nCzy chcesz mimo to wczytać warstwę?", QMessageBox.Yes |
                                                     QMessageBox.No, QMessageBox.No)
                        if odp == QMessageBox.No:
                            return
                        else:
                            geomTypeEPSG = geomTypeEPSG[:-4] + newEPSG
                            epsg_code = newEPSG
                
                destlayer = QgsVectorLayer(geomTypeEPSG + self.fieldsDefinition(fields=fields), layerName + numerWarstwy, 'memory')
                destlayer.startEditing()
                for feature in layer.getFeatures():
                    new_feat = QgsFeature(destlayer.fields())
                    for index, field in enumerate(destlayer.fields()):
                        if field.name() in ('profilPodstawowy','profilDodatkowy','tytulAlternatywny') and feature.attribute(field.name()) != NULL:
                            new_feat.setAttribute(index, QVariant(",".join(feature.attribute(field.name()))))
                        else:
                            try:
                                new_feat.setAttribute(index, QVariant(feature.attribute(field.name())))
                            except:
                                pass
                    new_feat.setGeometry(feature.geometry())
                    destlayer.addFeature(new_feat)
                    destlayer.updateFeature(new_feat)
                destlayer.commitChanges()
                
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
                gkpg = QgsVectorLayer(output_path, layerName + numerWarstwy, 'ogr')
                gkpg.startEditing()
                
                gkpg.loadNamedStyle(str(pathQML))
                if activeDlgname != 'PytanieAppDialog':
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
                if activeDlgname != 'PytanieAppDialog':
                    self.activeDlg.layers_comboBox.setCurrentText(layerName)
                self.iface.messageBar().pushSuccess("Wczytanie warstwy:","Wczytano warstwę.")
                showPopup("Wczytaj warstwę","Poprawnie wczytano warstwę " + layerName + ".")


    def saveLayerToGML(self):
        s = QgsSettings()
        defaultPath = s.value("qgis_app2/settings/defaultPath", "/")
        
        namespace_map = {'wfs': 'http://www.opengis.net/wfs/2.0',
                         'app': 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0',
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
        elif isinstance(self.activeDlg, TworzenieOUZDialog):
            self.obrysLayer = layer_OUZ
        
        if self.obrysLayer == None:
            showPopup("Błąd warstwy obrysu", "Nie wskazano warstwy do zapisu.")
            return
        layerName = self.obrysLayer.name().split('_')[0]
        
        if not isinstance(self.activeDlg, TworzenieOUZDialog):
            showPopup("Zapisz warstwę","Zostaną teraz przeprowadzone kontrole warstwy " + layerName + ". Może to potrwać do kilku minut.")
            czyWynikKontroliPozytywny = True
            if not self.kontrolaWarstwy(self.obrysLayer):
                czyWynikKontroliPozytywny = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.czyObiektyUnikalne(self.obrysLayer,'oznaczenie'):
                czyWynikKontroliPozytywny = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.czyObiektyUnikalne(self.obrysLayer,'status'):
                czyWynikKontroliPozytywny = False
            if self.activeDlg != self.wektorInstrukcjaDialogPOG and not self.kontrolaGeometriiWarstwy(self.obrysLayer):
                czyWynikKontroliPozytywny = False
            if self.activeDlg == self.wektorInstrukcjaDialogOUZ and self.OUZpowyzej125procent(self.obrysLayer):
                czyWynikKontroliPozytywny = False
            
            if not czyWynikKontroliPozytywny:
                return
        
        if isinstance(self.activeDlg, TworzenieOUZDialog):
            plikGML = defaultPath + "/Dokumentacja/ObszarUzupelnieniaZabudowy-wyjsciowy.gml"
        else:
            self.fn = QFileDialog.getSaveFileName(directory=defaultPath, filter="pliki GML (*.gml)")[0]
            plikGML = str(self.fn)
        
        if plikGML:
            templateXML = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/templates/" + layerName + ".xml"
            templateFeatureCollection = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/templates/FeatureCollection.xml"
            
            with open(str(templateFeatureCollection), 'r') as input_file: xmlMain = input_file.read()
            with open(str(templateXML), 'r') as input_file: templateXML = input_file.read()
            
            ET.register_namespace('wfs', 'http://www.opengis.net/wfs/2.0')
            ET.register_namespace('app', 'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0')
            ET.register_namespace('gml', 'http://www.opengis.net/gml/3.2')
            ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
            ET.register_namespace('gco', 'http://www.isotc211.org/2005/gco')
            ET.register_namespace('gmd', 'http://www.isotc211.org/2005/gmd')
            
            tree = ET.ElementTree(ET.fromstring(xmlMain))
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
            
            swapXY = processing.run("native:swapxy", {
                'INPUT': self.obrysLayer,
                'OUTPUT': 'memory:'
            })
            
            for obj in swapXY['OUTPUT'].getFeatures():
                member = ET.fromstring(templateXML)
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
                        geom.append(ET.fromstring(geometriaGML))
                    elif geomAPP != None:
                        geomAPP.append(ET.fromstring(geometriaGML))
                
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
                                layerMember.insert(13 + liczbaWystapienProfiluPodstawowego, new_element)
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
                                layerMember.insert(12 + liczbaWystapienProfiluPodstawowego + liczbaWystapienProfiluDodatkowego, new_element)
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
        global layer_OUZ
        layer_OUZ = layer
        self.saveLayerToGML()


    def update_layer_list(self, obj):
        layers = QgsProject.instance().mapLayers()
        expected_layers = []
        for layer in layers.values():
            if not layer.name().startswith(self.activeDlg.name):
                expected_layers.append(layer)
        
        obj.layers_comboBox.setExceptedLayerList(expected_layers)


    def kontrolaGeometriiWarstwy(self, obrysLayer):
        czyGeometrieSaPoprawne = True
        
        warstwaBezKoniecWersjiObiektu = processing.run("qgis:extractbyexpression", {
            'INPUT':obrysLayer,
            'EXPRESSION':'koniecWersjiObiektu is NULL',
            'OUTPUT':'memory:'})
        self.obrysLayer = warstwaBezKoniecWersjiObiektu['OUTPUT']
        
        if self.obrysLayer.featureCount() > 0:
            # kontrola poprawnosci geometrii
            for objTMP in obrysLayer.getFeatures():
                if not objTMP.geometry().isGeosValid():
                    bledne_geometrie = processing.run("qgis:checkvalidity", {
                        'INPUT_LAYER': obrysLayer,
                        'METHOD': 2,
                        'INVALID_OUTPUT': 'memory:',
                        'ERROR_OUTPUT': 'memory:'
                    })
                    bledne_geometrie['INVALID_OUTPUT'].setName("Błędy geometrii")
                    bledne_geometrie['INVALID_OUTPUT'].startEditing()
                    bledne_geometrie['INVALID_OUTPUT'].renameAttribute(bledne_geometrie['INVALID_OUTPUT'].fields().indexFromName("_errors"), "opis_bledu")
                    bledne_geometrie['INVALID_OUTPUT'].commitChanges()
                    bledne_geometrie['ERROR_OUTPUT'].setName("Lokalizacje błędów geometrii")
                    bledne_geometrie['ERROR_OUTPUT'].startEditing()
                    bledne_geometrie['ERROR_OUTPUT'].renameAttribute(bledne_geometrie['ERROR_OUTPUT'].fields().indexFromName("message"), "opis_bledu")
                    bledne_geometrie['ERROR_OUTPUT'].commitChanges()
                    QgsProject.instance().addMapLayer(bledne_geometrie['INVALID_OUTPUT'])
                    QgsProject.instance().addMapLayer(bledne_geometrie['ERROR_OUTPUT'])
                    showPopup("Błąd warstwy obrysu", "Występuje niepoprawna geometria w warstwie. Dodano warstwę z błędnymi obiektami w zakresie geometrii oraz warstwę punktową wskazującą miejsca z błędami.")
                    return False
            
            # Sprawdzanie CRS warstwy wejściowej
            authid = str(obrysLayer.crs().authid())
            if authid == '':
                showPopup("Błąd warstwy obrysu", "Obrys nie ma zdefiniowanego układu współrzędnych")
                czyGeometrieSaPoprawne = False
            epsg = authid.split(':')[1]
            srsName = ''
            # Układ współrzędnych
            for crs in dictionaries.ukladyOdniesieniaPrzestrzennego.values():
                if epsg in crs:
                    srsName = crs
                    break
            
            if srsName == '':
                showPopup("Błąd warstwy obrysu",
                          "Obrys posiada niezgodny układ współrzędnych - EPSG:%s.\nDostępne CRS:\n    - %s" % (epsg, ',\n    - '.join(['%s : %s' % (a, b) for a, b in zip(dictionaries.ukladyOdniesieniaPrzestrzennego.keys(), dictionaries.ukladyOdniesieniaPrzestrzennego.values())])))
                czyGeometrieSaPoprawne = False
            
            # geometria wychodzi poza granicę Polski
            if not isLayerInPoland(obrysLayer):
                czyGeometrieSaPoprawne = False
            
            # geometria wychodzi poza POG
            warstwaPOG = self.wektorInstrukcjaDialogPOG.layers_comboBox.currentLayer()
            if warstwaPOG == None:
                for layer in QgsProject.instance().mapLayers().values():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name().startswith('AktPlanowaniaPrzestrzennego'):
                        warstwaPOG = layer
            
            if warstwaPOG != None:
                przyciecie = processing.run("qgis:difference", {
                    'INPUT': obrysLayer,
                    'OVERLAY': warstwaPOG,
                    'OUTPUT': 'memory:'
                })
                
                # rozbicie multipoligon-u na poligony
                pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
                    'INPUT': przyciecie['OUTPUT'],
                    'OUTPUT': 'memory:'
                })
                
                #kasowanie obiektów wychodzących poza POG o powierzchni < 1 m2
                pojedynczeObjekty['OUTPUT'].startEditing()
                for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
                    if obj.geometry().area() < 1: # 1 m2
                        pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
                pojedynczeObjekty['OUTPUT'].commitChanges(False)
                
                if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
                    pojedynczeObjekty['OUTPUT'].setName("Geometrie wychodzace poza POG")
                    QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
                    showPopup("Błąd warstwy obrysu",
                              "Niepoprawna geometria - obiekty muszą leżeć wewnątrz POG. Dodano warstwę z geometriami wychodzącymi poza POG.")
                    czyGeometrieSaPoprawne = False
            
            # sprawdzenie czy wystepują nakładające się obiekty
            if not obrysLayer.name().startswith('AktPlanowaniaPrzestrzennego'):
                union = processing.run("qgis:union", {
                    'INPUT': obrysLayer,
                    'OUTPUT': 'memory:'
                })
                
                usunDuplikaty = processing.run("native:deleteduplicategeometries", {
                    'INPUT': union['OUTPUT'],
                    'OUTPUT': 'memory:'
                })
                
                wynik = processing.run("native:detectvectorchanges", {
                    'ORIGINAL': union['OUTPUT'],
                    'REVISED': usunDuplikaty['OUTPUT'],
                    'UNCHANGED': 'memory:',
                    'ADDED': 'memory:',
                    'DELETED': 'memory:'
                })
                
                #kasowanie obiektów nakładających się o powierzchni < 1 m2
                wynik['DELETED'].startEditing()
                for obj in wynik['DELETED'].getFeatures():
                    if obj.geometry().area() < 1: # 1 m2
                        wynik['DELETED'].deleteFeature(obj.id())
                wynik['DELETED'].commitChanges(False)
                
                if wynik['DELETED'].featureCount() > 0:
                    wynik['DELETED'].setName("Nakładajace sie fragmenty geometrii")
                    QgsProject.instance().addMapLayer(wynik['DELETED'])
                    showPopup("Błąd warstwy obrysu","Niepoprawna geometria - Nakładające się fragmenty geometrii.")
                    czyGeometrieSaPoprawne = False
            
            # sprawdzenie czy wystepują dziury pomiędzy stykającymi się strefami i braki w dopełnieniu do POG
            if obrysLayer.name().startswith('StrefaPlanistyczna') and warstwaPOG != None:
                
                bufor0 = processing.run("native:buffer", {
                    'INPUT': obrysLayer,
                    'DISTANCE':0,
                    'SEGMENTS':10,
                    'DISSOLVE': True,
                    'OUTPUT': 'memory:'
                })
                difference = processing.run("qgis:difference", {
                    'INPUT': warstwaPOG,
                    'OVERLAY': bufor0['OUTPUT'],
                    'OUTPUT': 'memory:'
                })
                
                # rozbicie multipoligon-u na poligony
                pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
                    'INPUT': difference['OUTPUT'],
                    'OUTPUT': 'memory:'
                })
                
                #kasowanie dziur o powierzchni < 1 m2
                pojedynczeObjekty['OUTPUT'].startEditing()
                for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
                    if obj.geometry().area() < 1: # 1 m2
                        pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
                pojedynczeObjekty['OUTPUT'].commitChanges(False)
                
                if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
                    for objTMP in warstwaPOG.getFeatures():
                        
                        if not objTMP['modyfikacja'] or objTMP['status'] != 'w opracowaniu':
                            pojedynczeObjekty['OUTPUT'].setName("Geometrie dziur w SPL w zakresie POG")
                            QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
                            showPopup("Błąd warstwy obrysu",
                                      "Niepoprawna geometria - Występują dziury w SPL.")
                            czyGeometrieSaPoprawne = False
                            break
        else:
            showPopup("Błąd warstwy obrysu",
                      "Brak obiektu/ów na warstwie stref planistycznych.")
        return czyGeometrieSaPoprawne


    def czyObiektyUnikalne(self, obrysLayer, atrybutDoSprawdzeniaUnikalnosci):
        warstwaBezKoniecWersjiObiektu = processing.run("qgis:extractbyexpression", {
            'INPUT':obrysLayer,
            'EXPRESSION':'koniecWersjiObiektu is NULL',
            'OUTPUT':'memory:'})
        obrysLayer_tmp = warstwaBezKoniecWersjiObiektu['OUTPUT']
        
        liczbaObiektowWarstwy = obrysLayer_tmp.featureCount()
        liczbaObiektowWarstwyUnikalnych = liczbaObiektowWarstwy
        if liczbaObiektowWarstwy > 0:
            unikalnosc = processing.run("native:removeduplicatesbyattribute", {
                'INPUT': obrysLayer_tmp,
                'FIELDS':[atrybutDoSprawdzeniaUnikalnosci],
                'OUTPUT':'memory:',
                'DUPLICATES':'memory:'
            })
            liczbaObiektowWarstwyUnikalnych = unikalnosc['OUTPUT'].featureCount()
            procent = (liczbaObiektowWarstwyUnikalnych / liczbaObiektowWarstwy) * 100
            
            jestOk = True
            if procent < 100 and atrybutDoSprawdzeniaUnikalnosci == 'oznaczenie':
                showPopup("Błąd warstwy obrysu","Występują duplikaty w atrybucie " + atrybutDoSprawdzeniaUnikalnosci + " warstwy " + obrysLayer_tmp.sourceName())
                unikalnosc['DUPLICATES'].setName("Obiekty " + obrysLayer_tmp.sourceName() + " - duplikaty w atrybucie " + atrybutDoSprawdzeniaUnikalnosci)
                QgsProject.instance().addMapLayer(unikalnosc['DUPLICATES'])
                jestOk = False
            if liczbaObiektowWarstwyUnikalnych != 1 and atrybutDoSprawdzeniaUnikalnosci == 'status':
                showPopup("Błąd warstwy obrysu","Występują różne wartości w atrybucie " + atrybutDoSprawdzeniaUnikalnosci + " warstwy " + obrysLayer_tmp.sourceName())
                jestOk = False
        return jestOk


    def kontrolaWarstwy(self, obrysLayer):
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
        
        if self.obrysLayer.featureCount() > 1 and obrysLayer.name().startswith("AktPlanowaniaPrzestrzennego"):
            warstwaBezKoniecWersjiObiektu = processing.run("qgis:extractbyexpression", {
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
            showPopup("Błąd warstwy obrysu", "Wybrana warstwa nie posiada obiektu.")
            return False
        elif not isLayerInPoland(self.obrysLayer):
            showPopup("Błąd warstwy obrysu",
                      "Niepoprawna geometria - obiekt musi leżeć w Polsce, sprawdź układ współrzędnych warstwy.")
            return False
        elif not czyWarstwaMaWypelnioneObowiazkoweAtrybuty(self.obrysLayer):
            showPopup("Błąd warstwy obrysu",
                      "Występują obiekty z niewypełnionymi atrybutami obowiązkowymi.")
            return False
        elif not kontrolaZaleznosciAtrybutow(self.obrysLayer):
            showPopup("Błąd warstwy obrysu",
                      "Występują obiekty z błędnie wypełnionymi atrybutami.")
            return False
        elif srsName == '':
            showPopup("Błąd warstwy obrysu",
                      "Obrys posiada niezgodny układ współrzędnych - EPSG:%s.\nDostępne CRS:\n    - %s" % (epsg, ',\n    - '.join(['%s : %s' % (a, b) for a, b in zip(dictionaries.ukladyOdniesieniaPrzestrzennego.keys(), dictionaries.ukladyOdniesieniaPrzestrzennego.values())])))
            return False
        else:
            return True


    def OUZpowyzej125procent(self, obrysLayer):
        
        pathOUZ_wyjsciowy = os.path.join(defaultPath,"Dokumentacja/ObszarUzupelnieniaZabudowy-wyjsciowy.gml")
        powierzchnie_OUZ = os.path.join(defaultPath,"Dane pomocnicze/Powierzchnie.xml")
        
        if os.path.exists(pathOUZ_wyjsciowy) and os.path.exists(powierzchnie_OUZ):
            
            root = ET.parse(powierzchnie_OUZ).getroot()
            powierzchnia_Pp = float(root[3][2].text)
            # powierzchnia_Pu = float(root[3][0].text)
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
                return True
        
        pathOUZ_wyjsciowy_layer = QgsVectorLayer(pathOUZ_wyjsciowy + "|layername=ObszarUzupelnieniaZabudowy|option:FORCE_SRS_DETECTION=YES|option:CONSIDER_EPSG_AS_URN=YES|geometrytype=Polygon", "ObszarUzupelnieniaZabudowy", 'ogr')
        pojedynczeBufory = processing.run("native:multiparttosingleparts", {
            'INPUT': pathOUZ_wyjsciowy_layer,
            'OUTPUT': 'memory:'
        })
        
        # różnica powierzchnii
        roznica = processing.run("qgis:difference", {
            'INPUT': obrysLayer,
            'OVERLAY': pojedynczeBufory['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        # zmiana multipoligonów na poligony
        pojedynczeBufory2 = processing.run("native:multiparttosingleparts", {
            'INPUT': roznica['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        # usunięcie bardzo małych powierzchnii
        pojedynczeBufory2['OUTPUT'].startEditing()
        for tmpObj in pojedynczeBufory2['OUTPUT'].getFeatures():
            if tmpObj.geometry().area() < 0.05:
                pojedynczeBufory2['OUTPUT'].deleteFeature(tmpObj.id())
        pojedynczeBufory2['OUTPUT'].commitChanges(False)
        
        # odseparowanie obiektów, które się nie przecinają
        obiektyBledne = processing.run("qgis:extractbylocation", {
            'INPUT': pojedynczeBufory2['OUTPUT'],
            'PREDICATE': 2,
            'INTERSECT': pojedynczeBufory['OUTPUT'],
            'OUTPUT': 'memory:'
        })
        
        # przekazanie komunikatu i obiektów błędnych
        if obiektyBledne['OUTPUT'].featureCount() > 0:
            obiektyBledne['OUTPUT'].setName("Nowe obiekty OUZ")
            QgsProject.instance().addMapLayer(obiektyBledne['OUTPUT'])
            showPopup("Błąd warstwy obrysu","Warstwa ObszarUzupelnieniaZabudowy zawiera nowe obiekty.")
            return True
        
        def powierzchniaNaElipsoidzie(feature):
            d = QgsDistanceArea()
            d.setEllipsoid('WGS84')
            geom = feature.geometry()
            geom.transform(QgsCoordinateTransform(obrysLayer.crs(), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance().transformContext()))
            area = d.measureArea(geom)
            return area
        
        powierzchniaPowiekszeniaOUZ = 0
        for tmp_obj in pojedynczeBufory2['OUTPUT'].getFeatures():
            powierzchniaPowiekszeniaOUZ += powierzchniaNaElipsoidzie(tmp_obj)
        
        if powierzchniaPowiekszeniaOUZ > powierzchnia_Pp:
            showPopup("Błąd warstwy obrysu",
                      "Powierzchnia warstwy została powiększona o więcej niż maksymalną powierzchnię powiększenia obszarów uzupełnienia zabudowy wyznaczonych w sposób, o którym mowa w ust. 1 Rozporządzenia.")
            return True
        else:
            showPopup("Informacja",
                      "Kontrola maksymalnej powierzchnii powiększenia została przeprowadzona i powiększenie jest dopuszczalne.")
            return False