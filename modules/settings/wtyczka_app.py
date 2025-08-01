# -*- coding: utf-8 -*-
from . import (UstawieniaDialog, PomocDialog, ustawieniaDialog, PLUGIN_VERSION)
from .. import BaseModule, dictionaries
from ..utils import showPopup, getWidgetByName, settingsValidateDatasetId, validate_IIP, validateEmailAddress, validate_ILAPP
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QVariant, QRegExp
from qgis.core import QgsSettings
import os
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime
from qgis.PyQt.QtWidgets import *
import re
import urllib.request
import urllib.parse
import json
import types


class SettingsModule(BaseModule):
    def __init__(self, iface):
        self.iface = iface
        global s, bledy, zmiany
        s = QgsSettings()
        bledy = [0, 0, 0, 0] # ścieżka, numer zbioru, JPT, lokalnyIdAPP
        zmiany = [0, 0, 0, 0, 0] # ścieżka, numer zbioru, JPT, lokalnyIdAPP, rodzaj zbioru
        
        # region okno moduł settings
        self.ustawieniaDialog = ustawieniaDialog
        # endregion
        # region okno moduł help
        self.pomocDialog = PomocDialog()
        
        # endregion
        self.add_rodzajZbioru_values()
        self.readSettings()
        self.set_field_validators()
        self.preparePrzestrzenNazw()
        
        def custom_context_menu(widget, event):
            menu = widget.createStandardContextMenu()
            menu.addSeparator()
            
            action  = QAction("Pobierz numer zbioru z Ewidencji zbiorów i usług danych przestrzennych", widget)
            action.triggered.connect(self.pobranieNumeruZbioru_z_EZiUDP)
            menu.addAction(action)
            menu.exec_(event.globalPos())
        
        self.numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit
        self.numerZbioru_lineEdit.contextMenuEvent = types.MethodType(custom_context_menu, self.numerZbioru_lineEdit)
        
        self.jpt_comboBoxWithContextMenu = self.ustawieniaDialog.jpt_comboBoxWithContextMenu.lineEdit()
        
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            self.jpt_comboBoxWithContextMenu.setPlaceholderText('np. 24')
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setValidator(QRegExpValidator(QRegExp("[0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2]")))
        else:
            self.jpt_comboBoxWithContextMenu.setPlaceholderText('np. 246601')
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setValidator(QRegExpValidator(QRegExp("([0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2])[0-9]{4}")))
        self.ustawieniaDialog.folder_btn.clicked.connect(self.folder_btn_clicked)
        self.ustawieniaDialog.save_btn.clicked.connect(self.save_btn_clicked)
        self.ustawieniaDialog.exit_btn.clicked.connect(self.exit_btn_clicked)
        
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'MPZP':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2392')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'SUIKZP':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2393')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 9878')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 9325')
        else:
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2392')
        
        self.ustawieniaDialog.numerZbioru_lineEdit.textChanged.connect(self.set_edycjaNumerZbioru)
        self.ustawieniaDialog.numerZbioru_lineEdit.setText(s.value("qgis_app2/settings/numerZbioru", ""))
        self.ustawieniaDialog.jpt_comboBoxWithContextMenu.editTextChanged.connect(self.set_edycjaJPT)
        self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentIndexChanged.connect(self.selectJPT)
        self.ustawieniaDialog.jpt_comboBoxWithContextMenu.itemRemoved.connect(self.usuniecieJPT)
        self.ustawieniaDialog.edycjaILAPP.setPlaceholderText('np. 1POG')
        self.ustawieniaDialog.edycjaILAPP.textChanged.connect(self.set_edycjaILAPP)
        self.ustawieniaDialog.edycjaILAPP.setText(s.value("qgis_app2/settings/idLokalnyAPP", ""))
        self.ustawieniaDialog.rodzajZbioru_comboBox.currentTextChanged.connect(self.set_field_validators)
        self.ustawieniaDialog.rodzajZbioru_comboBox.currentIndexChanged.connect(self.readSettings_Manual)
        self.ustawieniaDialog.save_btn.setEnabled(False)
        
        self.set_edycjaNumerZbioru()
        self.set_edycjaJPT()
        self.kontrola_folder()

    """Event handlers"""

    def set_edycjaILAPP(self):
        global bledy, zmiany
        txt = self.ustawieniaDialog.edycjaILAPP.text()
        
        if re.match('^[1-9][0-9]*$', txt) != None:
            pozycjaKursora = len(txt)
            txt = str(txt) + 'POG'
            self.ustawieniaDialog.edycjaILAPP.disconnect()
            self.ustawieniaDialog.edycjaILAPP.setText(txt)
            self.ustawieniaDialog.edycjaILAPP.setCursorPosition(pozycjaKursora)
            self.ustawieniaDialog.edycjaILAPP.textChanged.connect(self.set_edycjaILAPP)
        
        if re.match('^[1-9][0-9]*POG$', txt) == None:
            self.ustawieniaDialog.edycjaILAPP.setStyleSheet("border: 1px solid red")
            self.ustawieniaDialog.edycjaILAPP.setFixedHeight(22)
            bledy[3] = 1
        else:
            self.ustawieniaDialog.edycjaILAPP.setStyleSheet("")
            bledy[3] = 0
            if self.ustawieniaDialog.edycjaILAPP.text() != s.value("qgis_app2/settings/idLokalnyAPP", ""):
                zmiany[3] = 1
            else:
                zmiany[3] = 0
        
        self.wlaczenieZapisu()


    def set_edycjaNumerZbioru(self):
        global bledy, zmiany
        
        txt = self.ustawieniaDialog.numerZbioru_lineEdit.text()
        
        if re.match('^[1-9][0-9]*$', txt) == None:
            self.ustawieniaDialog.numerZbioru_lineEdit.setStyleSheet("border: 1px solid red")
            self.ustawieniaDialog.numerZbioru_lineEdit.setFixedHeight(22)
            bledy[1] = 1
        else:
            self.ustawieniaDialog.numerZbioru_lineEdit.setStyleSheet("")
            bledy[1] = 0
            if self.ustawieniaDialog.numerZbioru_lineEdit.text() != s.value("qgis_app2/settings/numerZbioru", ""):
                zmiany[1] = 1
            else:
                zmiany[1] = 0
        
        self.wlaczenieZapisu()


    def set_edycjaJPT(self):
        global bledy, zmiany
        
        txt = self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText()
        match = ''
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            match = '^[0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2]$'
        else:
            match = '^([0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2])[0-9]{4}$'
        
        if re.match(match, txt) == None or \
           (self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() != 'PZPW' and 
           not txt[:4] in [code for values in dictionaries.przypisaniePowiatuDoEPSGukladuPL2000.values() for code in values]):
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setStyleSheet("border: 1px solid red")
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setFixedHeight(22)
            bledy[2] = 1
        else:
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setStyleSheet("")
            bledy[2] = 0
            if self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText() != s.value("qgis_app2/settings/jpt", ""):
                zmiany[2] = 1
            else:
                zmiany[2] = 0
            
        self.wlaczenieZapisu()


    def selectJPT(self, index):
        for ustawienie_json in ustawienia_json:
            if ustawienie_json["jpt"] == self.ustawieniaDialog.jpt_comboBoxWithContextMenu.itemText(index):
                self.ustawieniaDialog.folder_lbl.setText(ustawienie_json["defaultPath"])
                self.ustawieniaDialog.numerZbioru_lineEdit.setText(ustawienie_json["numerZbioru"])
                if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
                    self.ustawieniaDialog.edycjaILAPP.setText(ustawienie_json["idLokalnyAPP"])


    def wlaczenieZapisu(self):
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() != 'POG':
            bledy[3] = 0
        if sum(bledy) == 0 and sum(zmiany) > 0:
            self.ustawieniaDialog.save_btn.setEnabled(True)
        else:
            self.ustawieniaDialog.save_btn.setEnabled(False)


    def set_field_validators(self):
        global zmiany
        self.ustawieniaDialog.numerZbioru_lineEdit.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]*")))
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.lineEdit().setPlaceholderText('np. 24')
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setValidator(QRegExpValidator(QRegExp("[0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2]")))
        else:
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.lineEdit().setPlaceholderText('np. 246601')
            self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setValidator(QRegExpValidator(QRegExp("([0][2|4|6|8]|[1-2][0|2|4|6|8]|[3][0|2])[0-9]{4}")))
        self.ustawieniaDialog.edycjaILAPP.setValidator(QRegExpValidator(QRegExp("POG|[1-9][0-9]*POG")))
        
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() != s.value("qgis_app2/settings/rodzajZbioru", ""):
            zmiany[4] = 1
        else:
            zmiany[4] = 0
        
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'MPZP':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2392')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'SUIKZP':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2393')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 9878')
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 9325')
        else:
            self.ustawieniaDialog.numerZbioru_lineEdit.setPlaceholderText('np. 2392')
        
        self.set_edycjaJPT()
        self.set_edycjaILAPP()
        self.wlaczenieZapisu()


    def add_rodzajZbioru_values(self):
        values = dictionaries.rodzajeZbiorow.keys()
        self.ustawieniaDialog.rodzajZbioru_comboBox.addItems(values)


    def folder_btn_clicked(self):
        global bledy, zmiany
        if self.ustawieniaDialog.folder_lbl != '/':
            directory = self.ustawieniaDialog.folder_lbl.text()
        else:
            directory = '/'
        path = QFileDialog.getExistingDirectory(
            self.ustawieniaDialog, "Wskaż domyślny folder zapisu", directory , QFileDialog.ShowDirsOnly)
        
        if path == '':
            showPopup('Wybór katalogu', 'Nie wskazano domyślnej ścieżki zapisu plików. Proszę wybrać katalog.', icon=QMessageBox.Warning)
            if s.value("qgis_app2/settings/defaultPath", "") == '':
                bledy[0] = 1
            return
        
        test_file = os.path.join(path, 'test_write.tmp')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            self.ustawieniaDialog.folder_lbl.setText(path)
            bledy[0] = 0
        except (OSError, IOError):
            showPopup('Brak uprawniń', 'Brak uprawnień do zapisu we wskazanym katalogu.', icon=QMessageBox.Warning)
            bledy[0] = 1
        
        self.kontrola_folder()
        self.wlaczenieZapisu()


    def kontrola_folder(self):
        global bledy, zmiany
        
        if self.ustawieniaDialog.folder_lbl.text() == '':
            bledy[0] = 1
            self.ustawieniaDialog.folder_lbl.setStyleSheet("border: 1px solid red")
            self.ustawieniaDialog.folder_lbl.setFixedHeight(22)
        else:
            bledy[0] = 0
            self.ustawieniaDialog.folder_lbl.setStyleSheet("")
            
            if self.ustawieniaDialog.folder_lbl.text() != s.value("qgis_app2/settings/defaultPath", ""):
                zmiany[0] = 1
            else:
                zmiany[0] = 0


    def validate_settings(self):
        bledy_tmp = []
        if not (self.ustawieniaDialog.przestrzenNazw_lineEdit.text() == '' or validate_IIP(self.ustawieniaDialog.przestrzenNazw_lineEdit.text())):  # walidacja idIPP
            bledy_tmp.append('- Błędna wartość dla pola Przestrzeń nazw APP.')
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG' and self.getEPSGukladPL2000() == 0:
            bledy_tmp.append('- Błędna wartość dla pola JPT.')
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG' and validate_ILAPP(self.ustawieniaDialog.edycjaILAPP.text()):
            bledy_tmp.append('- Błędna wartość dla identyfikatora lokalnego APP.')
        if bledy_tmp:
            return (False, '\n\n'.join(bledy_tmp))
        else:
            return [True]


    def save_btn_clicked(self, silently=False):
        global ustawienia_json
        
        valResult = self.validate_settings()
        if valResult[0]:
            s.setValue("qgis_app2/settings/defaultPath",
                       self.ustawieniaDialog.folder_lbl.text())
            s.setValue("qgis_app2/settings/przestrzenNazw",
                       self.ustawieniaDialog.przestrzenNazw_lineEdit.text())
            s.setValue("qgis_app2/settings/numerZbioru",
                       self.ustawieniaDialog.numerZbioru_lineEdit.text())
            s.setValue("qgis_app2/settings/jpt",
                       self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText())
            s.setValue("qgis_app2/settings/rodzajZbioru",
                       self.ustawieniaDialog.rodzajZbioru_comboBox.currentText())
            if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
                s.setValue("qgis_app2/settings/idLokalnyAPP",
                           self.ustawieniaDialog.edycjaILAPP.text())
            s.setValue("qgis_app2/settings/strefaPL2000", self.getEPSGukladPL2000())
            
            paczki = ustawienia_json
            if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() != 'POG':
                paczka = {
                    "defaultPath": self.ustawieniaDialog.folder_lbl.text(),
                    "przestrzenNazw": self.ustawieniaDialog.przestrzenNazw_lineEdit.text(),
                    "numerZbioru": self.ustawieniaDialog.numerZbioru_lineEdit.text(),
                    "jpt": self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText(),
                    "rodzajZbioru": self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()
                }
            else:
                paczka = {
                    "defaultPath": self.ustawieniaDialog.folder_lbl.text(),
                    "przestrzenNazw": self.ustawieniaDialog.przestrzenNazw_lineEdit.text(),
                    "numerZbioru": self.ustawieniaDialog.numerZbioru_lineEdit.text(),
                    "jpt": self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText(),
                    "rodzajZbioru": self.ustawieniaDialog.rodzajZbioru_comboBox.currentText(),
                    "idLokalnyAPP": self.ustawieniaDialog.edycjaILAPP.text()
                }
            
            wykorzystanaPaczka = False
            for pojedynczaPaczka in paczki:
                if pojedynczaPaczka["jpt"] == self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText():
                    indeks = paczki.index(pojedynczaPaczka)
                    paczki[indeks] = paczka
                    wykorzystanaPaczka = True
            
            if not wykorzystanaPaczka:
                paczki.append(paczka)
            
            if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
                s.setValue("qgis_app2/settings/ustawienia_json_pzpw", json.dumps(paczki))
            elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'SUIKZP':
                s.setValue("qgis_app2/settings/ustawienia_json_suikzp", json.dumps(paczki))
            elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'MPZP':
                s.setValue("qgis_app2/settings/ustawienia_json_mpzp", json.dumps(paczki))
            else:
                s.setValue("qgis_app2/settings/ustawienia_json_pog", json.dumps(paczki))
            
            self.ustawieniaDialog.save_btn.setEnabled(False)
            if not silently:
                showPopup('Ustawienia zapisane pomyślnie',
                          'Ustawienia zostały zapisane.\n\nWyłącz i włącz program QGIS lub użyj wtyczki "Plugin Reloader" w celu zastosowania zmian.',
                          icon=QMessageBox.Information)
        else:
            if not silently:
                showPopup('Błąd zapisu ustawień', 'Ustawienia nie zostały zapisane z następujących powodów:\n\n%s' % valResult[1], icon=QMessageBox.Warning)


    def exit_btn_clicked(self):
        self.readSettings()
        self.kontrola_folder()


    def preparePrzestrzenNazw(self):
        def updatePrzestrzenNazw():
            przestrzenNazw_list = []
            przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
            numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit.text()
            jpt_comboBoxWithContextMenu = self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText()
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
            if jpt_comboBoxWithContextMenu.strip():
                przestrzenNazw_list.append(jpt_comboBoxWithContextMenu.strip())
            if rodzajZbioru_comboBox.strip():
                przestrzenNazw_list.append('-'+rodzajZbioru_comboBox.strip())
            przestrzenNazw_lineEdit.setText('PL.ZIPPZP.'+"".join(przestrzenNazw_list))
            
        # pobranie dynamicznie utworzonych obiektów UI
        przestrzenNazw_lineEdit = self.ustawieniaDialog.przestrzenNazw_lineEdit
        numerZbioru_lineEdit = self.ustawieniaDialog.numerZbioru_lineEdit
        jpt_comboBoxWithContextMenu = self.ustawieniaDialog.jpt_comboBoxWithContextMenu
        rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox
        
        # definicja Eventów dynamicznych obiektów UI
        numerZbioru_lineEdit.textChanged.connect(lambda: updatePrzestrzenNazw())
        jpt_comboBoxWithContextMenu.editTextChanged.connect(lambda: updatePrzestrzenNazw())
        rodzajZbioru_comboBox.currentTextChanged.connect(lambda: updatePrzestrzenNazw())
        
        rodzajZbioru_comboBox = self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()
        if rodzajZbioru_comboBox != 'POG':
            self.ustawieniaDialog.label.hide()
            self.ustawieniaDialog.label_5.hide()
            self.ustawieniaDialog.edycjaILAPP.hide()
        else:
            self.ustawieniaDialog.edycjaILAPP.show()
            self.ustawieniaDialog.label.show()
            self.ustawieniaDialog.label_5.show()


    def readSettings(self):
        global ustawienia_json
        ustawienia_json = []
        
        try:
            self.ustawieniaDialog.rodzajZbioru_comboBox.setCurrentIndex(list(dictionaries.rodzajeZbiorow.keys()).index(s.value("qgis_app2/settings/rodzajZbioru","")))
        except:
            self.ustawieniaDialog.rodzajZbioru_comboBox.setCurrentIndex(0)
        self.ustawieniaDialog.folder_lbl.setText(s.value("qgis_app2/settings/defaultPath",""))
        self.ustawieniaDialog.przestrzenNazw_lineEdit.setText(s.value("qgis_app2/settings/przestrzenNazw","PL.ZIPPZP."))
        self.ustawieniaDialog.numerZbioru_lineEdit.setText(s.value("qgis_app2/settings/numerZbioru",""))
        
        if s.value("qgis_app2/settings/rodzajZbioru", "") == 'PZPW':
            raw_data = s.value("qgis_app2/settings/ustawienia_json_pzpw","[]")
        elif s.value("qgis_app2/settings/rodzajZbioru", "") == 'SUIKZP':
            raw_data = s.value("qgis_app2/settings/ustawienia_json_suikzp","[]")
        elif s.value("qgis_app2/settings/rodzajZbioru", "") == 'MPZP':
            raw_data = s.value("qgis_app2/settings/ustawienia_json_mpzp","[]")
        else:
            raw_data = s.value("qgis_app2/settings/ustawienia_json_pog","[]")
        
        try:
            self.data = json.loads(raw_data)
        except Exception:
            self.data = []
        
        for ustawienie_json in self.data:
            if self.ustawieniaDialog.jpt_comboBoxWithContextMenu.findText(ustawienie_json["jpt"]) == -1:
                self.ustawieniaDialog.jpt_comboBoxWithContextMenu.addItem(ustawienie_json["jpt"])
                ustawienia_json.append(ustawienie_json)
        self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setCurrentText(s.value("qgis_app2/settings/jpt",""))
        
        if s.value("qgis_app2/settings/rodzajZbioru", "") == 'POG':
            self.ustawieniaDialog.edycjaILAPP.setText(s.value("qgis_app2/settings/idLokalnyAPP",""))
        
        if self.data == []:
            self.save_btn_clicked(True)
        
        self.kontrola_folder()


    def readSettings_Manual(self):
        global ustawienia_json
        ustawienia_json = []
        
        self.ustawieniaDialog.jpt_comboBoxWithContextMenu.clear()
        
        if s.value("qgis_app2/settings/rodzajZbioru", "") != "" and s.value("qgis_app2/settings/rodzajZbioru", "") == self.ustawieniaDialog.rodzajZbioru_comboBox.currentText():
            self.readSettings()
        else:
            if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
                raw_data = s.value("qgis_app2/settings/ustawienia_json_pzpw","[]")
            elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'SUIKZP':
                raw_data = s.value("qgis_app2/settings/ustawienia_json_suikzp","[]")
            elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'MPZP':
                raw_data = s.value("qgis_app2/settings/ustawienia_json_mpzp","[]")
            else:
                raw_data = s.value("qgis_app2/settings/ustawienia_json_pog","[]")
            
            try:
                self.data = json.loads(raw_data)
            except Exception:
                self.data = []
            
            for ustawienie_json in self.data:
                if self.ustawieniaDialog.jpt_comboBoxWithContextMenu.findText(ustawienie_json["jpt"]) == -1:
                    self.ustawieniaDialog.jpt_comboBoxWithContextMenu.addItem(ustawienie_json["jpt"])
                    ustawienia_json.append(ustawienie_json)
            
            if raw_data == "[]":
                self.ustawieniaDialog.jpt_comboBoxWithContextMenu.setCurrentText("")
                self.ustawieniaDialog.numerZbioru_lineEdit.setText("")
                self.ustawieniaDialog.folder_lbl.setText("")
                if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
                    self.ustawieniaDialog.edycjaILAPP.setText("")
            else:
                self.ustawieniaDialog.folder_lbl.setText(self.data[0]["defaultPath"])
                self.ustawieniaDialog.numerZbioru_lineEdit.setText(self.data[0]["numerZbioru"])
                if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'POG':
                    self.ustawieniaDialog.edycjaILAPP.setText(self.data[0]["idLokalnyAPP"])
            
            self.kontrola_folder()


    def getEPSGukladPL2000(self):
        jpt = self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText()
        teryt = jpt[:4]
        
        for epsg in dictionaries.przypisaniePowiatuDoEPSGukladuPL2000:
            if teryt in dictionaries.przypisaniePowiatuDoEPSGukladuPL2000[epsg]:
                return epsg
        return 0


    def usuniecieJPT(self, value):
        global ustawienia_json
        
        paczki = ustawienia_json
        
        for pojedynczaPaczka in paczki:
            if pojedynczaPaczka["jpt"] == value:
                indeks = paczki.index(pojedynczaPaczka)
                del paczki[indeks]
        
        if self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'PZPW':
            s.setValue("qgis_app2/settings/ustawienia_json_pzpw", json.dumps(paczki))
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'SUIKZP':
            s.setValue("qgis_app2/settings/ustawienia_json_suikzp", json.dumps(paczki))
        elif self.ustawieniaDialog.rodzajZbioru_comboBox.currentText() == 'MPZP':
            s.setValue("qgis_app2/settings/ustawienia_json_mpzp", json.dumps(paczki))
        else:
            s.setValue("qgis_app2/settings/ustawienia_json_pog", json.dumps(paczki))
        
        showPopup('Usunięcie zapisane pomyślnie',
                  'Usunięcie zostało zapisane.\n\nWyłącz i włącz program QGIS lub użyj wtyczki "Plugin Reloader" w celu zastosowania zmian.',
                  icon=QMessageBox.Information)


    def pobranieNumeruZbioru_z_EZiUDP(self):
        teryt = self.ustawieniaDialog.jpt_comboBoxWithContextMenu.currentText()
        if teryt == "":
            showPopup('Pobranie numeru zbioru','Proszę uzupełnić JPT.',icon=QMessageBox.Information)
        else:
            showPopup('Pobranie numeru zbioru',
                      'Nastąpi pobranie numeru zbioru z Ewidencji zbiorów i usług danych przestrzennych (źródło: www.geoportal.gov.pl). Pobranie będzie trwało od 1 do ok. 10 sekund.',
                      icon=QMessageBox.Information)
            
            nazwa_zbioru = {"POG": "Zbiór danych przestrzennych dla planu ogólnego gminy",
                            "MPZP":"Zbiór danych przestrzennych dla miejscowych planów zagospodarowania przestrzennego",
                            "PZPW":"Zbiór danych przestrzennych dla planu zagospodarowania przestrzennego województwa",
                            "SUIKZP":"Studium uwarunkowań i kierunków zagospodarowania przestrzennego"
                           }
            
            params = {"teryt": teryt,
                      "rodzaj": "",
                      "nazwa": "",
                      "zbior": nazwa_zbioru[self.ustawieniaDialog.rodzajZbioru_comboBox.currentText()],
                      "temat": "",
                      "usluga": "",
                      "adres": ""
                     }
            
            base_url = "https://integracja.gugik.gov.pl/eziudp/index.php"
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read().decode("utf-8")
            except Exception as e:
                raise Exception(f"Błąd pobierania danych: {e}")
            
            matches = re.findall(r'PL\.ZIPPZP\.(\d+)', html)
            
            if not matches:
                showPopup('Pobranie numeru zbioru',
                          'Nie pobrano numeru zbioru z Ewidencji zbiorów i usług danych przestrzennych (źródło: www.geoportal.gov.pl).',
                          icon=QMessageBox.Information)
                return
            
            numeruZbioru_z_EZiUDP = matches[-1]
            
            self.ustawieniaDialog.numerZbioru_lineEdit.selectAll()
            self.ustawieniaDialog.numerZbioru_lineEdit.insert(numeruZbioru_z_EZiUDP)
            
            showPopup('Pobranie numeru zbioru',
                      'Pobrano numeru zbioru z Ewidencji zbiorów i usług danych przestrzennych (źródło: www.geoportal.gov.pl).',
                      icon=QMessageBox.Information)