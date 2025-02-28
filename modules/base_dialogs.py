# -*- coding: utf-8 -*-
from . import utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from .utils import showPopup
from qgis.core import QgsApplication
from .settings import ustawieniaDialog, pomocDialog


class ButtonsDialog:
    """Okno z klawiszami - przejścia do ustawień"""
    def __init__(self):
        vLayout = self.layout().itemAt(0)
        
        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/ustawienia.png'))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.setToolTip("Ustawienia")
        self.settings_btn.setAutoDefault(False)
        self.settings_btn.clicked.connect(self.settings_btn_clicked)
        hbox.addWidget(self.settings_btn)
        self.help_btn = QPushButton()
        self.help_btn.setIcon(QIcon(':/plugins/wtyczka_app/img/info2.png'))
        self.help_btn.setIconSize(QSize(20, 20))
        self.help_btn.setObjectName("help_btn")
        self.help_btn.setToolTip("Pomoc")
        self.help_btn.setAutoDefault(False)
        self.help_btn.clicked.connect(self.help_btn_clicked)
        hbox.addWidget(self.help_btn)
        vLayout.insertLayout(0, hbox)
    
    def settings_btn_clicked(self):
        ustawieniaDialog.show()
    
    def help_btn_clicked(self):
        pomocDialog.show()


class CloseMessageDialog(QDialog):
    """Klasa bazowa definiująca zamykanie okna wtyczki"""
    closed = pyqtSignal()

    def closeEvent(self, event):
        if self.sender() is None:
            reply = QMessageBox.question(self, 'Opuszczanie wtyczki APP',
                                         "Jesteś pewien, że chcesz opuścić wtyczkę?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # emituje sygnał zamknięcia
                self.closed.emit()
                event.accept()
            else:
                event.ignore()


class BaseModule:
    """Klasa bazowa dla wszystkich modułów wtyczka_app.py"""
    listaOkienek = []
    activeDlg = None
    iface = None

    """Helper methods"""

    def validateFile(self, path, validator, type, muted=False):
        """walidacja pliku z danymi lub metadanymi"""
        taskDescriptions = [task.description() for task in QgsApplication.taskManager().activeTasks()]
        if validator:  # walidator gotowy do dzialania
            if type == 'metadane':
                validationResult = validator.validateMetadataXml(xmlPath=path)
            elif type == 'zbior':
                validationResult = validator.validateZbiorXml(xmlPath=path)
            elif type == 'app':
                validationResult = validator.validateAppXml(xmlPath=path)
            else:
                raise NotImplementedError
            if validationResult[0]:  # poprawnie zwalidowano
                if not muted:
                    self.iface.messageBar().pushSuccess(
                        "Sukces:", "Pomyślnie zwalidowano plik. Nie wykryto błędów.")
                    showPopup("Waliduj pliki", "Poprawnie zwalidowano plik.")
                return True
            else:   # błędy walidacji
                self.iface.messageBar().pushCritical(
                    "Błąd walidacji:", "Wykryto błędy walidacji.")
                self.showPopupValidationErrors(
                    "Błąd walidacji", "Wystąpiły błędy walidacji pliku %s :\n\n%s" % (path, validationResult[1]))
                return False
        elif type == 'metadane':
            if 'Wczytywanie schematu XSD dla metadanych' in taskDescriptions:
                # walidator metadanych niegotowy do dzialania - nadal wczytuje XSD
                self.iface.messageBar().pushWarning("Ostrzeżenie:","Schemat metadanych nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")
                return False
            else:  # blad przy wczytywaniu - wczytac jeszcze raz
                self.showPopupYesNo("Ostrzeżenie:","Schemat metadanych musi zostać zaimportowany, co może potrwać kilka minut.\nNiezbędne jest połączenie z internetem.\nProszę nie podejmować żadnych akcji w programie QGIS. Po zakończeniu wczytywania zostanie wyświetlony komunikat.\nCzy chcesz go zaimportować?",lambda: self.prepareXsdForMetadata())
                return False
        elif type == 'zbior' or type == 'app':
            if 'Wczytywanie schematu XSD dla APP' in taskDescriptions:
                # walidator danych niegotowy do dzialania - nadal wczytuje XSD
                self.iface.messageBar().pushWarning("Ostrzeżenie:","Schemat APP i zbioru APP nie został jeszcze zaimportowany, spróbuj ponownie za chwilę.")
                return False
            else:  # blad przy wczytywaniu - wczytac jeszcze raz
                self.showPopupYesNo("Ostrzeżenie:","Schemat musi zostać zaimportowany, co może potrwać kilka minut.\nNiezbędne jest połączenie z internetem.\nProszę nie podejmować żadnych akcji w programie QGIS. Po zakończeniu wczytywania zostanie wyświetlony komunikat.\nCzy chcesz go zaimportować?",lambda: self.prepareXsdForApp())
                return False
        else:
            raise NotImplementedError


    def openNewDialog(self, dlg):
        if self.activeDlg:
            self.activeDlg.close()
        self.activeDlg = dlg
        self.activeDlg.show()


    def showPopupYesNo(self, title, text, functionIfYes):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        yes = msg.addButton(
            'Tak', QMessageBox.AcceptRole)
        no = msg.addButton(
            'Nie', QMessageBox.RejectRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            functionIfYes()


    def showPopupValidationErrors(self, title, text, icon=QMessageBox.Warning):
        def saveErrorsFile(outputFile):
            with open(outputFile, 'w') as plik:
                plik.write(text)
        
        def saveErrors():
            plik = QFileDialog.getSaveFileName(
                filter="Pliki tekstowe (*.txt)")[0]
            if plik:
                try:
                    saveErrorsFile(plik)
                    self.iface.messageBar().pushSuccess("Eksport błędów:", "Zapisano plik z błędami.")
                except Exception as e:
                    self.iface.messageBar().pushCritical(
                        "Eksport błędów:", "Nie udało się zapisać pliku z błędami:" + str(e))
        
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setEscapeButton(QMessageBox.Ok)
        msg.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        raport = msg.addButton('Eksport błędów do pliku', QMessageBox.AcceptRole)
        raport.clicked.connect(saveErrors)
        return msg.exec_()