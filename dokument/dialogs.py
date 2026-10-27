# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Dokument
 ***************************************************************************/
"""

import os
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from ..base_dialogs import CloseMessageDialog, ButtonsDialog
from qgis.core import *
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout


title = 'Tworzenie pliku GML dla dokumentu Repozytorium'
icon = ':/plugins/wtyczka_app/img/dokument.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_Dokument.ui'))


class DokumentDialog(CloseMessageDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(DokumentDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)

