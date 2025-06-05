# -*- coding: utf-8 -*-
# from . import (UstawieniaDialog, PomocDialog, ustawieniaDialog, PLUGIN_VERSION)
# from .. import BaseModule, dictionaries
# from ..utils import showPopup, getWidgetByName, settingsValidateDatasetId, validate_IIP, validateEmailAddress, validate_ILAPP
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QVariant, QRegExp, pyqtSignal
from qgis.core import QgsSettings
import os
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime
from qgis.PyQt.QtWidgets import *
# import re



class ComboBoxWithContextMenu(QComboBox):
    
    itemRemoved = pyqtSignal(str)
    pobierzNumerZbioru_z_EZiUDP = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        
        # Ustawiamy listView, który będzie zawierał itemy
        view = QListView()
        view.setMouseTracking(True)
        view.setEditTriggers(QListView.NoEditTriggers)
        self.setView(view)
        self.view().viewport().installEventFilter(self)
    
    def eventFilter(self, source, event):
        # Zdarzenie, gdy klikniemy prawym przyciskiem myszy na elemencie ComboBox
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.RightButton:
            index = self.view().indexAt(event.pos())
            if index.isValid():
                # Tworzymy menu kontekstowe
                menu = QMenu(self)
                
                delete_action = QAction("Usuń", self)
                delete_action.triggered.connect(lambda: self.usuniecie(index.row()))
                menu.addAction(delete_action)
                
                # Wyświetlamy menu kontekstowe w miejscu kliknięcia
                menu.exec_(event.globalPos())  # Pokaż menu
                return True
        return super().eventFilter(source, event)
    
    def focusOutEvent(self, event):
        # Kiedy ComboBox traci fokus, sprawdzamy czy pole edycji zawiera wartość
        text = self.lineEdit().text()
        super().focusOutEvent(event)
    
    def usuniecie(self, index):
        value = self.itemText(index)
        self.removeItem(index)
        self.itemRemoved.emit(value)