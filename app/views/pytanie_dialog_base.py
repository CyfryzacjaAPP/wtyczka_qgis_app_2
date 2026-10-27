# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/app/views/ui/pytanie_dialog_base.ui'
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
        Dialog.setMinimumSize(QtCore.QSize(0, 196))
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.empty2_lbl = QtWidgets.QLabel(Dialog)
        self.empty2_lbl.setText("")
        self.empty2_lbl.setObjectName("empty2_lbl")
        self.verticalLayout.addWidget(self.empty2_lbl)
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 573, 435))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.verticalLayout_2.addWidget(self.instruction_lbl)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/plugins/wtyczka_app/img/baner_wtyczka.png"))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.zbior_btn = QtWidgets.QPushButton(Dialog)
        self.zbior_btn.setObjectName("zbior_btn")
        self.horizontalLayout.addWidget(self.zbior_btn)
        self.app_btn = QtWidgets.QPushButton(Dialog)
        self.app_btn.setDefault(True)
        self.app_btn.setObjectName("app_btn")
        self.horizontalLayout.addWidget(self.app_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Czy będziesz pracować ze zbiorem danych przestrzennych aktów planowania przestrzennego (zbiór APP), czy z danymi przestrzennymi dla pojedynczego aktu planowania przestrzennego (APP)?"))
        self.instruction_lbl.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">APP</span> – obejmuje dane przestrzenne dla jednego aktu planowania przestrzennego np. dla wybranego miejscowego planu zagospodarowania przestrzennego. </p><p><span style=\" font-weight:600;\">Zbiór APP</span> – obejmuje zestaw danych przestrzennych dla wielu (co najmniej jednego) aktów planowania przestrzennego tego samego rodzaju, występujących w danej jednostce podziału terytorialnego np. miejscowe plany zagospodarowania przestrzennego danej gminy. </p><p>Aby utworzyć zbiór APP, należy wcześniej przygotować pojedyncze pliki GML dla każdego APP, który zostanie włączony do tego zbioru. </p><p>Dane przestrzenne dla jednego APP obejmują: </p><p><span style=\" font-family:&quot;\'Symbol\'&quot;;\">- </span>rysunek lub rysunki APP, w postaci plików rastrowych z nadaną georeferencją, w formacie GeoTIFF, wraz z informacją o łączu pod którym są one opublikowane (co najmniej jeden rysunek jest wymagany w przypadku obowiązującego APP); </p><p><span style=\" font-family:&quot;\'Symbol\'&quot;;\">- </span>granicę obszaru objętego APP określoną w układzie PL-1992 (EPSG:2180) lub PL-2000 (EPSG:2176, 2177, 2178, 2179), posiadającą reprezentację geometryczną w postaci jednego poligonu lub jednego multipoligonu (w przypadku obiektów wieloczęściowych);</p><p><span style=\" font-family:&quot;\'Symbol\'&quot;;\">- </span>informacje nt. dokumentów powiązanych z danym APP (np. uchwała o przystąpieniu do sporządzenia APP, uchwała uchwalająca APP, czy opracowanie ekofizjograficzne, prognoza oddziaływania na środowisko, prognoza skutków finansowych, decyzja o zmianie przeznaczenia gruntów rolnych na cele nierolnicze lub leśnych na cele nieleśne wraz ze złożonymi wnioskami).</p></body></html>"))
        self.zbior_btn.setText(_translate("Dialog", "Zbiór APP"))
        self.app_btn.setText(_translate("Dialog", "APP"))

