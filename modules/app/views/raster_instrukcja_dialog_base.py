# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/app/views/ui/raster_instrukcja_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(580, 394)
        Dialog.setSizeGripEnabled(True)
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
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 558, 308))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.instruction_lbl.setFont(font)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setOpenExternalLinks(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.gridLayout_2.addWidget(self.instruction_lbl, 0, 0, 1, 1)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setEnabled(True)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout.addWidget(self.prev_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.next_btn = QtWidgets.QPushButton(Dialog)
        self.next_btn.setDefault(True)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout.addWidget(self.next_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Przygotowanie rysunku APP"))
        self.instruction_lbl.setText(_translate("Dialog", "<html><head/><body><p>Dane przestrzenne dla APP obejmują m.in. informacje o łączu, pod którym dostępny jest rysunek/rysunki APP z nadaną georeferencją.</p><p>Jeżeli użytkownik nie posiada opublikowanych w internecie plików w formacie GeoTIFF dla wybranego APP należy: </p><p>1. Przygotować pliki w formacie GeoTIFF, zapoznać się z instrukcją nadawania georeferencji plikom rastrowym: <a href=\"http://www.gov.pl/zagospodarowanieprzestrzenne/instrukcja-uzytkownika-wtyczka-app\"><span style=\" text-decoration: underline; color:#0000ff;\">instrukcja użytkownika</span></a>;</p><p>2. Zamieścić przygotowane pliki GeoTIFF na stronie internetowej np. na stronie BIP gminy, bądź udostępnić przy pomocy usług sieciowych. </p></body></html>"))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.next_btn.setText(_translate("Dialog", "Dalej"))

