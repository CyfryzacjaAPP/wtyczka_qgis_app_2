# -*- coding: utf-8 -*-
from . import (AnalizyDialog)
from .. import BaseModule
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QVariant, QRegExp
from qgis.core import QgsSettings
import os
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime
from qgis.PyQt.QtWidgets import *
from ..app.wtyczka_app import AppModule


class AnalizyModule(BaseModule):

    def __init__(self, iface):
        """Inicjalizuje obiekt klasy `AnalizyModule` i konfiguruje jego stan początkowy."""
        self.iface = iface
        self.analizyDialog = AnalizyDialog()
        self.analizyDialog.close_btn.clicked.connect(self.analizyDialog.close)
        self.analizyDialog.load_btn.clicked.connect(self.analizy_load_btn_clicked)

    """Event handlers"""
    
    def analizy_load_btn_clicked(self):
        """Obsługuje kliknięcie przycisku związanego z operacją `analizy_load`."""
        self.loadFromGMLorGPKG(True)

