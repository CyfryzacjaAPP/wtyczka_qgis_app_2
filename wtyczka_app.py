# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WtyczkaAPP
                                 A QGIS plugin
 Wtyczka QGIS wspomagająca przygotowanie aktów planowania przestrzennego zgodnych z rozporządzeniem Ministra Rozwoju.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by EnviroSolutions Sp. z o.o.
        email                : office@envirosolutions.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtWidgets import QDialog, QFileDialog
import os
from . import PLUGIN_VERSION
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.core import QgsTask, QgsApplication, QgsMessageLog
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modules.app.wtyczka_app import AppModule
from .modules.metadata.wtyczka_app import MetadataModule
from .modules.validator.wtyczka_app import ValidatorModule
from .modules.tworzenieOUZ.wtyczka_app import TworzenieOUZModule
from .modules.settings.wtyczka_app import SettingsModule
from .modules.analizy.wtyczka_app import AnalizyModule
from .modules.utils import showPopup
from .modules.validator import validator
from .modules import utils
from .modules.base_dialogs import CloseMessageDialog
from qgis.core import qgsfunction
from qgis.core import QgsExpression


PLUGIN_NAME = 'Wtyczka APP 2'


class WtyczkaAPP(AppModule, MetadataModule, ValidatorModule, TworzenieOUZModule, SettingsModule, AnalizyModule):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # wczytanie modułów
        AppModule.__init__(self, iface)
        MetadataModule.__init__(self, iface)
        ValidatorModule.__init__(self, iface)
        TworzenieOUZModule.__init__(self, iface)
        SettingsModule.__init__(self, iface)
        AnalizyModule.__init__(self, iface)
        
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # zamykane okna do czyszczenia
        self.closableWindows = []
        for dialogObject in vars(self).values():
            if isinstance(dialogObject, CloseMessageDialog):
                self.closableWindows.append(dialogObject)
        for dialogObject in self.closableWindows:
            dialogObject.closed.connect(self.clearFormsOnClose)
        
        # Declare instance attributes
        self.actions = []
        
        self.listaPlikow = []
        
        # definicja walidatora
        self.dataValidator = None


    def clearFormsOnClose(self):
        """czyści formularze przy zamknięciu"""
        for dialogObject in self.closableWindows:
            # czyszczenie formularzy danych (APP)
            try:
                dialogObject.clearForm(dialogObject.form_scrollArea)
                dialogObject.setDefaultValues()
            except AttributeError:
                pass


    def createValidator(self):
        self.iface.messageBar().pushSuccess("Informacja:","Schemat jest importowany. Proszę nie podejmować żadnych akcji w programie QGIS.")
        QCoreApplication.processEvents()
        self.dataValidator = validator.ValidatorLxml(schema_path=os.path.join(os.path.dirname(__file__), 'modules/validator', 'schematTechniczny.xsd'))
        QCoreApplication.processEvents()
        if self.dataValidator.isXSDLoaded:
            showPopup("Informacja", "Schemat został zaimportowany.")
        else:
            showPopup("Informacja", "Schemat nie został zaimportowany.")


    def createMetadataValidator(self):
        self.iface.messageBar().pushSuccess("Informacja:","Schemat metadanych jest importowany. Proszę nie podejmować żadnych akcji w programie QGIS.")
        QCoreApplication.processEvents()
        self.metadataValidator = validator.ValidatorLxml(schema_path=os.path.join(os.path.dirname(__file__), 'modules/validator', 'metadane.xsd'))
        QCoreApplication.processEvents()
        showPopup("Informacja", "Schemat metadanych został zaimportowany.")


    def prepareXsdForApp(self):
        self.createValidator()


    def prepareXsdForMetadata(self):
        self.createMetadataValidator()


    def addAction(self, icon_path, text, callback):
        m = self.toolButton.menu()
        action = QAction(
            icon=QIcon(icon_path),
            text=text,
            parent=self.iface.mainWindow()
        )
        action.triggered.connect(callback)
        self.actions.append(action)
        m.addAction(action)
        self.iface.addPluginToMenu(u'&' + PLUGIN_NAME, action)
        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        self.toolButton = QToolButton()
        self.toolButton.setDefaultAction(QAction(
            icon=QIcon(':/plugins/wtyczka_app/img/logo.png'),
            text=u'&' + PLUGIN_NAME,
            parent=self.iface.mainWindow()
        ))
        self.toolButton.clicked.connect(self.run_app)
        
        self.toolButton.setMenu(QMenu())
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolBtnAction = self.iface.addToolBarWidget(self.toolButton)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/praca_z_app.png',
                       text=u'Praca z APP / zbiorem APP',
                       callback=self.run_app)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/tworzenie.png',
                       text=u'Tworzenie / aktualizacja metadanych dla zbioru APP',
                       callback=self.run_metadata)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/walidacja.png',
                       text=u'Walidacja danych planistycznych',
                       callback=self.run_validator)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/tworzenieOUZ.png',
                       text=u'Wyznaczanie OUZ',
                       callback=self.run_OUZ)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/analizy.png',
                       text=u'Ustalenia POG - widoki',
                       callback=self.run_analizy)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/ustawienia.png',
                       text=u'Ustawienia',
                       callback=self.run_settings)
        
        self.addAction(icon_path=':/plugins/wtyczka_app/img/info2.png',
                       text=u'Pomoc',
                       callback=self.run_help)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&' + PLUGIN_NAME, action)
            self.iface.removeToolBarIcon(action)
            
        self.iface.removeToolBarIcon(self.toolBtnAction)
        
        try:
            QgsExpression.unregisterFunction('zamien_nazwy_na_skroty')
        except Exception:
            pass


    """Action handlers"""
    # region action handlers
    def run_app(self):
        self.openNewDialog(self.pytanieAppDialog)


    def run_metadata(self):
        self.openNewDialog(self.metadaneDialog)
        self.metadaneDialog.prev_btn.setEnabled(False)


    def run_settings(self):
        self.openNewDialog(self.ustawieniaDialog)


    def run_help(self):
        self.openNewDialog(self.pomocDialog)


    def run_validator(self):
        self.openNewDialog(self.walidacjaDialog)


    def run_analizy(self):
        self.openNewDialog(self.analizyDialog)


    def run_OUZ(self):
        ouz_dlg = self.tworzenieOUZDialog
        self.openNewDialog(ouz_dlg)
        ouz_dlg.wlaczenieKonektorow()
        ouz_dlg.warstwa_POG()
        ouz_dlg.warstwa_Budynki()
    # endregion


    @qgsfunction(group='Custom')
    def zamien_nazwy_na_skroty(input_text, feature):
        """
        Funkcja do wtyczki APP 2.
        <br>
        Funkcja zamienia pełne nazwy terenów na skróty zgodnie z mapowaniem.
        <br>
        :param input_text: Tekst wejściowy do zamiany
        :param feature: Obiekt, na którym działa funkcja
        :param parent: Rodzic (domyślnie wymagane)
        :return: Zmieniony tekst
        <br>
        <h2>Przykłady</h2>
        <br>
        <ul>
        <li>zamien_nazwy_na_skroty() -> 13</li>
        <li>zamien_nazwy_na_skroty("field2") -> 42</li>
        </ul>
        """
    
        # Mapowanie pełnych nazw na skróty
        mapping = {
            "teren zabudowy mieszkaniowej jednorodzinnej": "MN",
            "teren handlu wielkopowierzchniowego": "H",
            "teren zieleni naturalnej": "ZN",
            "teren lasu": "L",
            "teren wód": "W",
            "teren zabudowy letniskowej lub rekreacji indywidualnej": "ML",
            "teren wielkotowarowej produkcji rolnej": "RZW",
            "teren rolnictwa z zakazem zabudowy": "RN",
            "teren biogazowni": "PEB",
            "teren usług sportu i rekreacji": "US",
            "teren usług kultury i rozrywki": "UK",
            "teren usług handlu detalicznego": "UHD",
            "teren usług gastronomii": "UG",
            "teren usług turystyki": "UT",
            "teren usług nauki": "UN",
            "teren usług edukacji": "UE",
            "teren usług zdrowia i pomocy społecznej": "UZ",
            "teren usług kultu religijnego": "UR",
            "teren usług handlu": "UH",
            "teren usług rzemieślniczych": "UL",
            "teren usług biurowych i administracji": "UA",
            "teren usług": "U",
            "teren elektrowni geotermalnej": "PEG",
            "teren drogi zbiorczej": "KDZ",
            "teren składów i magazynów": "PS",
            "teren produkcji": "P",
            "teren elektrowni słonecznej": "PEF",
            "teren elektrowni wiatrowej": "PEW",
            "teren elektrowni wodnej": "PEO",
            "teren zieleni urządzonej": "ZP"
        }
        
        if not input_text:  # Jeśli tekst pusty, zwróć bez zmian
            return input_text
            
        # Zamiana tekstów
        for full_text, short_text in mapping.items():
            input_text = input_text.replace(full_text, short_text)
        return input_text