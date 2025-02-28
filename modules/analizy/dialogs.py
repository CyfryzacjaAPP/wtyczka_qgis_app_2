# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Analizy
 ***************************************************************************/
"""

import os
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from ..base_dialogs import CloseMessageDialog, ButtonsDialog

title_analizy = 'Ustalenia POG – widoki'
icon_analizy = ':/plugins/wtyczka_app/img/analizy.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'analizy_dialog_base.ui'))


class AnalizyDialog(QtWidgets.QDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(AnalizyDialog, self).__init__(parent)
        self.setupUi(self)
        self.name = 'PytanieAppDialog'
        self.setWindowTitle(title_analizy)
        self.setWindowIcon(QtGui.QIcon(icon_analizy))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)