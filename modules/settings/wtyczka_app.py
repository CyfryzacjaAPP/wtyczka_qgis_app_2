# -*- coding: utf-8 -*-
from . import (UstawieniaDialog, PomocDialog, ustawieniaDialog, PLUGIN_VERSION)
from .. import BaseModule, dictionaries
from ..utils import showPopup, getWidgetByName, settingsValidateDatasetId, validate_IIP, validateEmailAddress
from ..metadata import SmtpDialog, CswDialog
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QVariant, QRegExp
from qgis.core import QgsSettings
import os
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime
from qgis.PyQt.QtWidgets import *

class SettingsModule(BaseModule):

    def __init__(self, iface):
        self.iface = iface
        global s
        s = QgsSettings()
        
        # region okno moduł settings
        self.ustawieniaDialog = ustawieniaDialog
        # endregion
        self.settingsSmtpDialog = SmtpDialog(self.iface)
        self.settingsCswDialog = CswDialog(self.iface)
        # region okno moduł help
        self.pomocDialog = PomocDialog()

        # endregion
        self.set_field_validators()
        self.add_rodzajZbioru_values()
        self.readSettings()

        self.preparePrzestrzenNazw()

        self.ustawieniaDialog.folder_btn.clicked.connect(
            self.folder_btn_clicked)
        self.ustawieniaDialog.save_btn.clicked.connect(self.save_btn_clicked)
        self.ustawieniaDialog.smtp_btn.clicked.connect(self.smtp_btn_clicked)
        self.ustawieniaDialog.csw_btn.clicked.connect(self.csw_btn_clicked)
        self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2393')
        self.ustawieniaDialog.jpt_lineEdit.setPlaceholderText('np. 246601')
        self.ustawieniaDialog.edycjaILAPP.setPlaceholderText('np. 1POG')


    """Event handlers"""

    def set_field_validators(self):
        self.ustawieniaDialog.numerZbioru_lineEdit.setValidator(
            QRegExpValidator(QRegExp("[1-9][0-9]*")))
        self.ustawieniaDialog.jpt_lineEdit.setValidator(
            QRegExpValidator(QRegExp("[0-3][0|2|4|6|8][0-9]{4}")))
        self.ustawieniaDialog.edycjaILAPP.setValidator(
            QRegExpValidator(QRegExp("[1-9][0-9]*POG")))


    def add_rodzajZbioru_values(self):
        values = dictionaries.rodzajeZbiorow.keys()
        self.ustawieniaDialog.rodzajZbioru_comboBox.addItems(values)


    def folder_btn_clicked(self):
        if self.ustawieniaDialog.folder_lbl != '/':
            directory = self.ustawieniaDialog.folder_lbl.text()
        else:
            directory = '/'
        path = QFileDialog.getExistingDirectory(
            self.ustawieniaDialog, "Wskaż domyślny folder zapisu", directory , QFileDialog.ShowDirsOnly)
        if path:
            self.ustawieniaDialog.folder_lbl.setText(path)


    def validate_settings(self):
        bledy = []
        if not (self.ustawieniaDialog.przestrzenNazw_lineEdit.text() == '' or validate_IIP(self.ustawieniaDialog.przestrzenNazw_lineEdit.text())):  # walidacja idIPP
            bledy.append('- Błędna wartość dla pola przestrzenNazw.')
        if not (self.ustawieniaDialog.contactMail_lineEdit.text() == '' or validateEmailAddress(self.ustawieniaDialog.contactMail_lineEdit.text())):
            bledy.append('- Błędna wartość dla adresu email domyślnego punktu kontaktowego.')
        if not (self.ustawieniaDialog.adminMail_lineEdit.text() == '' or validateEmailAddress(self.ustawieniaDialog.adminMail_lineEdit.text())):
            bledy.append('- Błędna wartość dla adresu email administratora danych.')
        if self.getEPSGukladPL2000() == 0:
            bledy.append('- Błędna wartość dla teryt powiatu w jpt.')
        if bledy:
            return (False, '\n\n'.join(bledy))
        else:
            return [True]


    def save_btn_clicked(self):
        valResult = self.validate_settings()
        if valResult[0]:
            
            s.setValue("qgis_app2/settings/defaultPath",
                       self.ustawieniaDialog.folder_lbl.text())
            s.setValue("qgis_app2/settings/contactName",
                       self.ustawieniaDialog.contactName_lineEdit.text())
            s.setValue("qgis_app2/settings/contactMail",
                       self.ustawieniaDialog.contactMail_lineEdit.text())
            s.setValue("qgis_app2/settings/adminName",
                       self.ustawieniaDialog.adminName_lineEdit.text())
            s.setValue("qgis_app2/settings/adminMail",
                       self.ustawieniaDialog.adminMail_lineEdit.text())
            s.setValue("qgis_app2/settings/przestrzenNazw",
                       self.ustawieniaDialog.przestrzenNazw_lineEdit.text())
            s.setValue("qgis_app2/settings/numerZbioru",
                       self.ustawieniaDialog.numerZbioru_lineEdit.text())
            s.setValue("qgis_app2/settings/jpt",
                       self.ustawieniaDialog.jpt_lineEdit.text())
            s.setValue("qgis_app2/settings/rodzajZbioru",
                       self.ustawieniaDialog.rodzajZbioru_comboBox.currentText())
            if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
                s.setValue("qgis_app2/settings/idLokalnyAPP",
                           self.ustawieniaDialog.edycjaILAPP.text())
            s.setValue("qgis_app2/settings/strefaPL2000",
                       self.getEPSGukladPL2000())
            
            showPopup('Ustawienia zapisane pomyślnie',
                      'Ustawienia zostały zapisane.\n\nWyłącz i włącz program QGIS lub użyj wtyczki "Plugin Reloader" w celu zastosowania zmian.',
                      icon=QMessageBox.Information)
        else:   # błędy walidacji
            showPopup('Błąd zapisu ustawień', 'Ustawienia nie zostały zapisane z następujących powodów:\n\n%s' % valResult[1], icon=QMessageBox.Warning)


    def preparePrzestrzenNazw(self):
        def updatePrzestrzenNazw():
            przestrzenNazw_list = []
            przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
            numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit.text()
            jpt_lineEdit = self.ustawieniaDialog.jpt_lineEdit.text()
            rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()
            if rodzajZbioru_comboBox != 'POG':
                self.ustawieniaDialog.label.hide()
                self.ustawieniaDialog.label_5.hide()
                self.ustawieniaDialog.edycjaILAPP.hide()
            else:
                self.ustawieniaDialog.edycjaILAPP.show()
                self.ustawieniaDialog.label.show()
                self.ustawieniaDialog.label_5.show()
            
            if numerZbioru_lineEdit.strip():
                przestrzenNazw_list.append(numerZbioru_lineEdit.strip()+'/')
            if jpt_lineEdit.strip():
                przestrzenNazw_list.append(jpt_lineEdit.strip())
            if rodzajZbioru_comboBox.strip():
                przestrzenNazw_list.append('-'+rodzajZbioru_comboBox.strip())
            przestrzenNazw_lineEdit.setText('PL.ZIPPZP.'+"".join(przestrzenNazw_list))

        # pobranie dynamicznie utworzonych obiektów UI
        przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
        numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit
        jpt_lineEdit = self.ustawieniaDialog.jpt_lineEdit
        rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox

        # definicja Eventów dynamicznych obiektów UI
        numerZbioru_lineEdit.textChanged.connect(
            lambda: updatePrzestrzenNazw())
        jpt_lineEdit.textChanged.connect(
            lambda: updatePrzestrzenNazw())
        rodzajZbioru_comboBox.currentTextChanged.connect(
            lambda: updatePrzestrzenNazw())
        
        rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()
        if rodzajZbioru_comboBox != 'POG':
            self.ustawieniaDialog.label.hide()
            self.ustawieniaDialog.label_5.hide()
            self.ustawieniaDialog.edycjaILAPP.hide()
        else:
            self.ustawieniaDialog.edycjaILAPP.show()
            self.ustawieniaDialog.label.show()
            self.ustawieniaDialog.label_5.show()


    def smtp_btn_clicked(self):
        self.settingsSmtpDialog.show()
        self.settingsSmtpDialog.send_btn.setVisible(False)


    def csw_btn_clicked(self):
        self.settingsCswDialog.show()
        self.settingsCswDialog.send_btn.setVisible(False)


    def readSettings(self):
        # s = QgsSettings()
        self.ustawieniaDialog.folder_lbl.setText(
            s.value("qgis_app2/settings/defaultPath", ""))
        self.ustawieniaDialog.contactName_lineEdit.setText(
            s.value("qgis_app2/settings/contactName", ""))
        self.ustawieniaDialog.contactMail_lineEdit.setText(
            s.value("qgis_app2/settings/contactMail", ""))
        self.ustawieniaDialog.adminName_lineEdit.setText(
            s.value("qgis_app2/settings/adminName", ""))
        self.ustawieniaDialog.adminMail_lineEdit.setText(
            s.value("qgis_app2/settings/adminMail", ""))
        self.ustawieniaDialog.przestrzenNazw_lineEdit.setText(
            s.value("qgis_app2/settings/przestrzenNazw", "PL.ZIPPZP."))
        self.ustawieniaDialog.numerZbioru_lineEdit.setText(
            s.value("qgis_app2/settings/numerZbioru", ""))
        self.ustawieniaDialog.jpt_lineEdit.setText(
            s.value("qgis_app2/settings/jpt", ""))
        try:
            self.ustawieniaDialog.rodzajZbioru_comboBox.setCurrentIndex(
                list(dictionaries.rodzajeZbiorow.keys()).index(s.value("qgis_app2/settings/rodzajZbioru", "")))
        except:
            pass
        if s.value("qgis_app2/settings/rodzajZbioru", "") == 'POG':
            self.ustawieniaDialog.edycjaILAPP.setText(s.value("qgis_app2/settings/idLokalnyAPP",""))
    """Helper methods"""
    """Popup windows"""


    def getEPSGukladPL2000(self):
        jpt = self.ustawieniaDialog.jpt_lineEdit.text()
        teryt = jpt[:4]
        
        for epsg in dictionaries.przypisaniePowiatuDoEPSGukladuPL2000:
            if teryt in dictionaries.przypisaniePowiatuDoEPSGukladuPL2000[epsg]:
                return epsg
        return 0
