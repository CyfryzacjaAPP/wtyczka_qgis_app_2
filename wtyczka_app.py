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
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu
from qgis.core import QgsTask, QgsApplication, QgsMessageLog
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modules.app.wtyczka_app import AppModule
from .modules.metadata.wtyczka_app import MetadataModule
from .modules.validator.wtyczka_app import ValidatorModule
from .modules.tworzenieOUZ.wtyczka_app import TworzenieOUZ
from .modules.settings.wtyczka_app import SettingsModule
from .modules.utils import showPopup
from .modules.validator import validator
from .modules import utils
from .modules.base_dialogs import CloseMessageDialog


PLUGIN_NAME = 'Wtyczka APP'


class WtyczkaAPP(AppModule, MetadataModule, ValidatorModule, TworzenieOUZ, SettingsModule):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        # wczytanie modułów
        AppModule.__init__(self, iface)
        MetadataModule.__init__(self, iface)
        ValidatorModule.__init__(self, iface)
        TworzenieOUZ.__init__(self, iface)
        SettingsModule.__init__(self, iface)

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
        # for el in utils.all_layout_widgets(self.wektorFormularzDialog.layout()):
        #     print(el.objectName())

        # definicja walidatora
        self.dataValidator = None


        # inicjacja walidatorów
        self.prepareXsdForApp()
        self.prepareXsdForMetadata()

    def clearFormsOnClose(self):
        """czyści formularze przy zamknięciu"""
        for dialogObject in self.closableWindows:
            # czyszczenie formularzy danych (APP)
            try:
                dialogObject.clearForm(dialogObject.form_scrollArea)
                dialogObject.setDefaultValues()
            except AttributeError:
                pass

    def createValidator(self, task):
        QgsMessageLog.logMessage('walidator start')
        self.dataValidator = validator.ValidatorLxml()
        QgsMessageLog.logMessage('walidator gotowy')

    def createMetadataValidator(self, task):
        QgsMessageLog.logMessage('walidator start')
        self.metadataValidator = validator.ValidatorLxml(schema_path=os.path.join(os.path.dirname(__file__), 'modules/validator', 'metadane.xsd'))
        QgsMessageLog.logMessage('walidator gotowy')


    def prepareXsdForApp(self):
        task = QgsTask.fromFunction('Wczytywanie schematu XSD dla APP', self.createValidator)
        if task.description() not in [task.description() for task in QgsApplication.taskManager().activeTasks()]:
            QgsApplication.taskManager().addTask(task)
            QgsMessageLog.logMessage('starting XSD reading task')

    def prepareXsdForMetadata(self):
        task = QgsTask.fromFunction('Wczytywanie schematu XSD dla metadanych', self.createMetadataValidator)
        if task.description() not in [task.description() for task in QgsApplication.taskManager().activeTasks()]:
            QgsApplication.taskManager().addTask(task)
            QgsMessageLog.logMessage('starting XSD reading task')


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
                       text=u'Tworzenie / aktualizacja metadanych',
                       callback=self.run_metadata)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/walidacja.png',
                       text=u'Walidacja GML',
                       callback=self.run_validator)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/tworzenieOUZ.png',
                       text=u'Tworzenie OUZ',
                       callback=self.run_OUZ)

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

    def run_OUZ(self):
        self.openNewDialog(self.tworzenieOUZDialog)
    # endregion