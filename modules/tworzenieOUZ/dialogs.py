# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os

from PyQt5.QtWidgets import QMessageBox

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from ..base_dialogs import CloseMessageDialog, ButtonsDialog

title_validator = 'Tworzenie OUZ'
icon_validator = ':/plugins/wtyczka_app/img/tworzenieOUZ.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'tworzenieOUZ.ui'))


class TworzenieOUZDialog(CloseMessageDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(TworzenieOUZDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_validator)
        self.setWindowIcon(QtGui.QIcon(icon_validator))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)