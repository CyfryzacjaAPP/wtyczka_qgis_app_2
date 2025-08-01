# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""
from .. import utils, dictionaries
from ..base_dialogs import CloseMessageDialog, ButtonsDialog
from . import metadataElementDictToForm, formToMetadataElementDict
from .metadata_form_initializer import initializeMetadataForm
import os, re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import Qt, QVariant, QRegExp, QDateTime
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from qgis.core import QgsSettings
from qgis.gui import QgisInterface, QgsFilterLineEdit




title_metadata = 'Tworzenie / aktualizacja metadanych dla zbioru APP'
icon_metadata = ':/plugins/wtyczka_app/img/tworzenie.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'metadane_dialog_base.ui'))


class SendFileDialog:
    """klasa bazowa dla formularzy wysyłki pliku metadanych"""

    def setXmlPath(self, xmlPath):
        self.xmlPath = xmlPath

    def saveSettings(self, formName):
        """Sprawdzanie Chceckboxów do zapisu ustawień"""
        s = QgsSettings()
        checked = False
        for chkbx in utils.getWidgetsByType(self, QCheckBox):
            if chkbx.isChecked():
                elementId = chkbx.objectName().split("_")[0]
                lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
                s.setValue("qgis_app/%s/%s" % (formName, elementId), lineEdit.text())
                checked = True
        if checked:
            self.iface.messageBar().pushSuccess("Zapis parametrów połączenia:", "Pomyslnie zapisano wskazane parametry połączenia")


    def readSettings(self, formName):
        """Odczyt zapisu ustawień"""
        s = QgsSettings()
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            elementId = lineEdit.objectName().split("_")[0]
            savedValue = s.value("qgis_app/%s/%s" % (formName, elementId), '')
            if savedValue:  # jeżeli była wartość zapisana w ustawieniach
                chkbx = utils.getWidgetByName(self, QCheckBox, elementId + "_chkbx")
                chkbx.setChecked(True)
            lineEdit.setText(savedValue)

    def validateForm(self):
        """walidacja formularza"""
        for lineEdit in utils.getWidgetsByType(self, QLineEdit):
            elementId = lineEdit.objectName().split("_")[0]
            label = utils.getWidgetByName(self, QLabel, elementId + "_lbl")
            if not lineEdit.text().strip():
                return (False, "Musisz wypełnić pole %s" % label.text())
            if ('user_lineEdit' == lineEdit.objectName() or 'receiver_lineEdit' == lineEdit.objectName()) and not utils.validateEmailAddress(lineEdit.text().strip()):
                return (False, "Wprowadź poprawny adres email w polu %s" % label.text())
        return [True]


class MetadaneDialog(CloseMessageDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(MetadaneDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title_metadata)
        self.setWindowIcon(QtGui.QIcon(icon_metadata))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)
        self.prepareLayout()
        # zapisanie inicjalnego formularza do słownika
        self.startFormState = formToMetadataElementDict(self)
        self.e32_btn.clicked.connect(self.e32_btn_clicked)
        self.clearForm_btn.clicked.connect(self.clearForm_btn_clicked)
        self.lockScrolls()

    def lockScrolls(self):
        """Blokuje scroll w formularzu metadanych"""
        for cmbbx in utils.getWidgetsByType(self, QComboBox):
            cmbbx.wheelEvent = lambda event: None
        for dateTimeEdit in utils.getWidgetsByType(self, QDateTimeEdit):
            dateTimeEdit.wheelEvent = lambda event: None

    def prepareLayout(self):
        """Przygotowanie layoutu metadanych"""
        for listWidget in utils.getWidgetsByType(self, QListWidget):
            self.prepareListWidgets(listWidget)

        # pola z ustawień
        # initializeMetadataForm(self)
        # pola edytowalne
        metadataElementDictToForm(metadataElementDict=dictionaries.metadataListWidgetsDefaultItems,
                                  targetForm=self)

        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')

        # Ograniczenia Pól QLineEdit
        # URI:
        for objectName in ["e4_lineEdit"]:
            input = utils.getWidgetByName(self, QLineEdit, objectName)
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))

        # mail:
        for objectName in ["e22_mail_lineEdit", "e29_mail_lineEdit"]:
            input = utils.getWidgetByName(self, QLineEdit, objectName)
            input.setValidator(QRegExpValidator(QRegExp(r"[0-9a-zA-Z.\-\_\@\+]*")))

        # unikalny identyfikator danych przestrzennych:
        input = utils.getWidgetByName(self, QLineEdit, "e5_lineEdit")
        input.setValidator(QRegExpValidator(QRegExp(r"[0-9A-Z.\-/]*")))

        # prostokat ograniczajacy
        input = utils.getWidgetByName(self, QLineEdit, "e11_lineEdit")
        input.setValidator(QRegExpValidator(QRegExp("[0-9.,]*")))

        # rozdzielczość przestrzenna
        input = utils.getWidgetByName(self, QLineEdit, "e16_lineEdit")
        input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))

        # czyszczenie QgsDateTimeEdit
        for dateTimeEdit in utils.getWidgetsByType(self, QDateTimeEdit):
            if dateTimeEdit.objectName() != 'e30_dateTimeEdit':
                dateTimeEdit.clear()

        # nadanie grafiki tooltipa
        for label in utils.getWidgetsByType(self, QLabel):
            if label.objectName().endswith("_tooltip"):
                label.setMaximumWidth(16)
                label.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))

                label.setToolTip(
                    "<FONT COLOR=black>%s</FONT>" % label.toolTip())  # dodanie tooltip z documentation 'rich text' dla zawijania

    def e32_btn_clicked(self):
        """Generowanie UUID do formularza"""
        if self.e32_lineEdit.text():
            msg = QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setWindowTitle('Generowanie UUID')
            msg.setText("Identyfikator już istnieje. Czy na pewno chcesz wygenerować nowy identyfikator dla pliku metadanych i tym samym nadpisać stary?")
            yes = msg.addButton(
                'Tak', QtWidgets.QMessageBox.AcceptRole)
            no = msg.addButton(
                'Nie', QtWidgets.QMessageBox.RejectRole)
            msg.setDefaultButton(no)
            msg.exec_()
            msg.deleteLater()
            if msg.clickedButton() is yes:
                uuid = utils.generateUUID()
                self.e32_lineEdit.setText(uuid)
        else:
            uuid = utils.generateUUID()
            self.e32_lineEdit.setText(uuid)


    def clearForm_btn_clicked(self):
        """czyszczenie formularza"""
        for lineEdit in utils.getWidgetsByType(self, QgsFilterLineEdit):
            lineEdit.clear()
        metadataElementDictToForm(self.startFormState, self)

    def prepareListWidgets(self, listWidget):
        """Przygotowanie obsługi pól wielokrotnej liczności"""
        def clearDataFromListWidget():
            if elementId == 'e22':
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx').setCurrentIndex(0)
            if elementId == 'e18':
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx').setCurrentIndex(0)
            if elementId == 'e24':
                utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit').clear()
            if elementId == 'e9':
                utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit').clear()
                utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit').clear()
                utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx').setCurrentIndex(0)
            for input in inputs:
                if isinstance(input, QComboBox):
                    input.setCurrentIndex(0)
                if isinstance(input, QLineEdit):
                    input.clear()
                if isinstance(input, QDateTimeEdit):
                    input.clear()

        def checkValidity():
            """sprawdzenie poprawności pól przed dodaniem do listWidget"""
            if elementId == 'e22' or elementId == 'e29':
                if nameLineEdit.text().strip() and mailLineEdit.text().strip():
                    return True
            elif elementId == 'e11':
                extent = lineEdit.text()
                if extent.count(',') == 3 and extent.count('.') <= 4:
                    return True
            elif elementId == 'e7' or elementId == 'e12' or elementId == 'e6':
                if cmbbx.currentText():
                    return True
            elif elementId == 'e24':
                if lineEdit.text().strip() and utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit').text().strip():
                    return True
            elif elementId == 'e18':
                if lineEdit.text().strip() and dateTimeEdit.dateTime():
                    return True
            elif elementId == 'e9':
                e10_lineEdit = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit')
                e10_dateTimeEdit = utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit')
                if lineEdit.text().strip() and not e10_lineEdit.text().strip(): # bez standardowego slownika
                    return True
                if lineEdit.text().strip() and e10_lineEdit.text().strip() and e10_dateTimeEdit.dateTime(): # standardowy słownik
                    return True
            elif lineEdit and lineEdit.text().strip():
                return True
            return False

        def getDataFromListWidget(listItem):
            data = listItem.data(Qt.UserRole)
            for input in inputs:
                if isinstance(input, QLineEdit):
                    input.setText(data[input.objectName()])
                elif isinstance(input, QDateTimeEdit):
                    input.setDateTime(data[input.objectName()])
                elif isinstance(input, QComboBox) and elementId != 'e29':
                    input.setCurrentIndex(input.findText(data[input.objectName()]))
            if elementId == 'e22':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx')
                input2.setCurrentIndex(input2.findText(data[input2.objectName()]))
            if elementId == 'e18':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx')
                input2.setCurrentIndex(input2.findText(data[input2.objectName()]))
            if elementId == 'e24':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit')
                input2.setText(data[input2.objectName()])
            if elementId == 'e9':
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit')
                if input2.objectName() in data:
                    input2.setText(data[input2.objectName()])
                else:
                    input2.clear()
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit')
                if input2.objectName() in data:
                    date = data[input2.objectName()]
                    input2.setDateTime(QDateTime() if (date is None or type(date) == QVariant) else data[input2.objectName()])
                else:
                    input2.clear()
                input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx')
                if input2.objectName() in data:
                    input2.setCurrentIndex(input2.findText(data[input2.objectName()]))
                else:
                    input2.setCurrentIndex(0)

        def addItem():
            if checkValidity():  # jeżeli pola są wypełnione
                newItem = QListWidgetItem()
                data = {}
                textList = []
                for input in inputs:
                    if isinstance(input, QLineEdit):
                        data[input.objectName()] = input.text()
                        textList.append(input.text())
                    if isinstance(input, QComboBox):
                        data[input.objectName()] = input.currentText()
                        textList.append(input.currentText())
                    if isinstance(input, QDateTimeEdit):
                        data[input.objectName()] = input.dateTime()
                        textList.append(input.dateTime().toString("dd-MM-yyyy"))

                if elementId == 'e22':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e23_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    textList.append(input2.currentText())
                if elementId == 'e18':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e19_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    textList.append(input2.currentText())
                if elementId == 'e24':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e25_lineEdit')
                    data[input2.objectName()] = input2.text()
                    textList.append(input2.text())
                if elementId == 'e9':
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QLineEdit, name='e10_lineEdit')
                    data[input2.objectName()] = input2.text()
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QDateTimeEdit, name='e10_dateTimeEdit')
                    data[input2.objectName()] = input2.dateTime()
                    input2 = utils.getWidgetByName(layout=self, searchObjectType=QComboBox, name='e10_cmbbx')
                    data[input2.objectName()] = input2.currentText()
                    data['xlink'] = None

                currentDatas = [listWidget.item(i).data(Qt.UserRole) for i in range(listWidget.count())]
                if data in currentDatas:
                    utils.showPopup("Próba ponownego wpisania istniejącej wartości",
                                    'Wprowadzana wartość już znajduje się na liście!')
                    return

                newItem.setData(Qt.UserRole, QVariant(data))
                newItem.setText(" - ".join(textList))
                listWidget.addItem(newItem)
                clearDataFromListWidget()  # czyszczenie
            else:
                utils.showPopup("Wypełnij formularz mapy podkładowej",
                                'Musisz zdefiniować poprawne wartości dla wszystkich wymaganych pól przed dodaniem do listy')
        def removeItem(listWidget):
            listWidget.takeItem(listWidget.currentRow())

        def setDefaultValues(elementId, listWidget):
            """ustawia domyślne wartości dla listWidget na podstawie słownika"""




        elementId = listWidget.objectName().split('_')[0]
        add_btn = utils.getWidgetByName(self, QPushButton, elementId + "_add_btn")
        remove_btn = utils.getWidgetByName(self, QPushButton, elementId + "_remove_btn")
        lineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_lineEdit")
        mailLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_mail_lineEdit")
        nameLineEdit = utils.getWidgetByName(self, QLineEdit, elementId + "_name_lineEdit")
        dateTimeEdit = utils.getWidgetByName(self, QDateTimeEdit, elementId + "_dateTimeEdit")
        cmbbx = utils.getWidgetByName(self, QComboBox, elementId + "_cmbbx")
        setDefaultValues(elementId, listWidget)

        inputs = [lineEdit, nameLineEdit, mailLineEdit, dateTimeEdit, cmbbx]
        add_btn.clicked.connect(addItem)
        remove_btn.clicked.connect(lambda: removeItem(listWidget))
        listWidget.itemDoubleClicked.connect(getDataFromListWidget)

