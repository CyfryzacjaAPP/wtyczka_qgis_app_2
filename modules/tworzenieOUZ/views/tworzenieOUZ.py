# -*- coding: utf-8 -*-
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 152)
        font = QtGui.QFont()
        font.setKerning(True)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.chooseXML_widget = QgsFileWidget(Dialog)
        self.chooseXML_widget.setEnabled(False)
        self.chooseXML_widget.setObjectName("chooseXML_widget")
        self.gridLayout_2.addWidget(self.chooseXML_widget, 2, 2, 1, 1)
        self.chooseGMLset_widget = QgsFileWidget(Dialog)
        self.chooseGMLset_widget.setEnabled(False)
        self.chooseGMLset_widget.setObjectName("chooseGMLset_widget")
        self.gridLayout_2.addWidget(self.chooseGMLset_widget, 0, 2, 1, 1)
        self.validateGMLset_radioButton = QtWidgets.QRadioButton(Dialog)
        self.validateGMLset_radioButton.setObjectName("validateGMLset_radioButton")
        self.gridLayout_2.addWidget(self.validateGMLset_radioButton, 0, 0, 1, 1)
        self.validateXML_radioButton = QtWidgets.QRadioButton(Dialog)
        self.validateXML_radioButton.setObjectName("validateXML_radioButton")
        self.gridLayout_2.addWidget(self.validateXML_radioButton, 2, 0, 1, 1)
        self.validateGMLapp_radioButton = QtWidgets.QRadioButton(Dialog)
        self.validateGMLapp_radioButton.setObjectName("validateGMLapp_radioButton")
        self.gridLayout_2.addWidget(self.validateGMLapp_radioButton, 1, 0, 1, 1)
        self.chooseGMLapp_widget = QgsFileWidget(Dialog)
        self.chooseGMLapp_widget.setEnabled(False)
        self.chooseGMLapp_widget.setObjectName("chooseGMLapp_widget")
        self.gridLayout_2.addWidget(self.chooseGMLapp_widget, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.validate_btn = QtWidgets.QPushButton(Dialog)
        self.validate_btn.setObjectName("validate_btn")
        self.horizontalLayout_5.addWidget(self.validate_btn)
        self.close_btn = QtWidgets.QPushButton(Dialog)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout_5.addWidget(self.close_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Walidacja plików GML / XML"))
        self.validateGMLset_radioButton.setText(_translate("Dialog", "Walidacja GML dla zbioru"))
        self.validateXML_radioButton.setText(_translate("Dialog", "Walidacja XML (metadane)"))
        self.validateGMLapp_radioButton.setText(_translate("Dialog", "Walidacja GML dla APP"))
        self.validate_btn.setText(_translate("Dialog", "Waliduj"))
        self.close_btn.setToolTip(_translate("Dialog", "<html><head/><body><p>Przycisk <span style=\" font-style:italic;\">Zakończ</span> zakończy działanie wtyczki</p></body></html>"))
        self.close_btn.setText(_translate("Dialog", "Zakończ"))
from qgsfilewidget import QgsFileWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())