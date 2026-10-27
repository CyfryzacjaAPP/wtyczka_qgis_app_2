# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Settings
 ***************************************************************************/
"""
import os
from wtyczka_qgis_app import PLUGIN_VERSION
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt, QRegExp
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from .comboBoxWithContextMenu import ComboBoxWithContextMenu
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QDialog




title_settings = 'Ustawienia'
icon_settings = ':/plugins/wtyczka_app/img/ustawienia.png'

title_help = 'Pomoc'
icon_help = ':/plugins/wtyczka_app/img/info2.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'ustawienia_dialog_base.ui'))

FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pomoc_dialog_base.ui'))


class UstawieniaDialog(QtWidgets.QDialog, FORM_CLASS):
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        """Constructor."""
        super(UstawieniaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_settings)
        self.setWindowIcon(QtGui.QIcon(icon_settings))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.exit_btn.clicked.connect(self.reject)
        
        self.jpt_comboBoxWithContextMenu  = ComboBoxWithContextMenu(self)
        self.jpt_comboBoxWithContextMenu.setObjectName("jpt_comboBoxWithContextMenu")
        self.gridLayout_4.addWidget(self.jpt_comboBoxWithContextMenu ,2, 1)
    
    def closeEvent(self, event):
        """Obsługuje zamknięcie okna i wykonuje wymagane czynności porządkowe."""
        self.closed.emit()

class PomocDialog(QtWidgets.QDialog, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(PomocDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_help)
        self.setWindowIcon(QtGui.QIcon(icon_help))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.version_lbl.setText(PLUGIN_VERSION)
        self.cancel_btn.clicked.connect(self.reject)