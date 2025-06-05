# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import PyQt5.QtCore
from qgis.core import QgsSettings, QgsMessageLog
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, QRegExp, QVariant
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap
from . import dictionaries, utils


class NoScrollQComboBox(QComboBox):
    """Combobox bez scrolla"""

    def wheelEvent(self, event):
        event.ignore()


class NoScrollQgsDateTimeEdit(QgsDateTimeEdit):
    """QgsDateTimeEdit bez scrolla"""

    def __init__(self, parent=None):
        super(NoScrollQgsDateTimeEdit, self).__init__()
        self.setDisplayFormat('dd.MM.yyyy hh:mm:ss')

    def wheelEvent(self, event):
        event.ignore()


class Formularz:
    """Klasa reprezentująca formularz"""

    pomijane = ["dokumentPrzystepujacy",
                "dokumentUchwalajacy",
                "dokumentZmieniajacy",
                "dokumentUchylajacy",
                "dokumentUniewazniajacy",
                "przystapienie",
                "uchwala",
                "zmienia",
                "uchyla",
                "uniewaznia",
                "plan",
                "dokument",
                "rysunek",
                "zasiegPrzestrzenny",
                "zmiana",
                "wydzielenie",
                "regulacja"]

    def returnFormElements(self, formElements):
        for fe in formElements:
            print('\t'+fe.name)
            try:
                print(fe.refObject.objectName())
            except:
                print('W pominiętych')

    def removeForm(self, container):
        """usuwa zawartość kontenera(container), żeby zrobić miejsce na formularz"""
        container.takeWidget()

    def clearForm(self, container):
        """czyści pola formularza"""
        widgets = utils.getWidgets(
            layout=container,
            types=[QgsDateTimeEdit, NoScrollQgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox, QComboBox, NoScrollQComboBox, QCheckBox, QListWidget])
        for widget in widgets[QgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[NoScrollQgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[QgsFilterLineEdit]:
            widget.clear()
        for widget in widgets[QgsMapLayerComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[QComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[NoScrollQComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[QCheckBox]:
            if widget.isChecked():
                widget.click()
        for widget in widgets[QListWidget]:
            widget.clear()

    def createForm(self, container, formElements):
        """tworzy formularz w miejscu kontenera (container), na podstawie listy obiektów klasy <FormElement>"""
        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        self.__loopFormElements(formElements, vbox)

        self.__preparePoziomHierarchii(vbox)
        container.setWidget(wgtMain)

    def __preparePoziomHierarchii(self, layout):
        """definiuje autouzupełnianie poziomHierarchii (INSPIRE)
        na podstawie typPlanu"""
        def typPlanu_cmbbx_currentTextChanged(currentText):
            if currentText.strip():
                poziomHierarchii_cmbbx.clear()
                wybor = dictionaries.typyPlanuPoziomyHierarchii[currentText]
                poziomHierarchii_cmbbx.addItems(wybor)

        # pobranie dynamicznie utworzonych obiektów UI
        poziomHierarchii_cmbbx = utils.layout_widget_by_name(
            layout, "poziomHierarchii_cmbbx")
        typPlanu_cmbbx = utils.layout_widget_by_name(layout, "typPlanu_cmbbx")
        if poziomHierarchii_cmbbx and typPlanu_cmbbx:   # jeżeli formularz zawiera te pola
            typPlanu_cmbbx.currentTextChanged.connect(
                typPlanu_cmbbx_currentTextChanged)

    def __loopFormElements(self, formElements, vbox, prefix=''):
        """Przerabia listę obiektów FormElements na GUI"""
        def createListWidget(name):
            """Tworzy listę dla pól wielokrotnej liczności"""
            def checkListFormValidity():
                if name == 'mapaPodkladowa':
                    if not referencja_lineEdit.text():
                        return False
                    if not data_dateTimeEdit.date():
                        return False
                    return True
                else:
                    if formItems[0].text().strip():
                        return True
                    else:
                        return False

            def addItem():
                if checkListFormValidity():
                    newListWidgetItem = QListWidgetItem()
                    data = {}
                    textList = []
                    for formItem in formItems:
                        if isinstance(formItem, QLineEdit):
                            data[formItem.objectName()] = formItem.text()
                            textList.append(formItem.text())
                        elif isinstance(formItem, QDateTimeEdit):
                            data[formItem.objectName()] = formItem.dateTime().date()
                            textList.append(formItem.dateTime().toString("dd-MM-yyyy"))
                        elif isinstance(formItem, QCheckBox):
                            data[formItem.objectName()] = formItem.isChecked()
                        elif isinstance(formItem, QComboBox):
                            data[formItem.objectName()] = formItem.currentIndex()
                            
                    newListWidgetItem.setData(
                        Qt.UserRole,
                        QVariant(data)
                    )
                    newListWidgetItem.setText(" - ".join(textList))
                    listWidget.addItem(newListWidgetItem)
                    clearDataFromListWidget()   # czyszczenie
                    if name == 'mapaPodkladowa':
                        referencja_lineEdit = utils.layout_widget_by_name(vbox2, name="referencja_lineEdit")
                        data_dateTimeEdit = utils.layout_widget_by_name(vbox2, name="data_dateTimeEdit")
                        referencja_lineEdit.setStyleSheet("")
                        data_dateTimeEdit.setStyleSheet("")
                else:
                    if name == 'mapaPodkladowa':
                        utils.showPopup("Wypełnij formularz mapy podkładowej",
                                        'Musisz zdefiniować wartości dla obowiązkowych pól:\n'
                                        '- referencja,\n'
                                        '- data')
                    else:
                        utils.showPopup("Wypełnij formularz",
                                        "Musisz wpisać wartość przed dodaniem")

            def removeItem():
                listWidget.takeItem(listWidget.currentRow())
                if listWidget.currentRow() == -1:
                    referencja_lineEdit = utils.layout_widget_by_name(vbox2, name="referencja_lineEdit")
                    data_dateTimeEdit = utils.layout_widget_by_name(vbox2, name="data_dateTimeEdit")
                    referencja_lineEdit.setStyleSheet("border: 1px solid red")
                    data_dateTimeEdit.setStyleSheet("border: 1px solid red")

            def clearDataFromListWidget():
                for formItem in formItems:
                    if isinstance(formItem, QCheckBox):
                        formItem.setChecked(False)
                    elif isinstance(formItem, QComboBox):
                        formItem.setCurrentIndex(0)
                    else:
                        formItem.clear()

            def setDataToListWidget(listItem):
                data = listItem.data(Qt.UserRole)
                for formItem in formItems:
                    if isinstance(formItem, QLineEdit):
                        formItem.setText(data[formItem.objectName()])
                    elif isinstance(formItem, QDateTimeEdit):
                        formItem.setDate(data[formItem.objectName()])
                    elif isinstance(formItem, QCheckBox):
                        formItem.setChecked(data[formItem.objectName()])
                    elif isinstance(formItem, QComboBox):
                        formItem.setCurrentIndex(data[formItem.objectName()])
            
            if name == 'mapaPodkladowa':
                referencja_lineEdit = utils.layout_widget_by_name(vbox2, name="referencja_lineEdit")
                data_dateTimeEdit = utils.layout_widget_by_name(vbox2, name="data_dateTimeEdit")
                lacze_lineEdit = utils.layout_widget_by_name(vbox2, name="lacze_lineEdit")
                
                formItems = [data_dateTimeEdit,
                             referencja_lineEdit,
                             lacze_lineEdit]
            elif formElement.name == 'lacze':
                lacze_lineEdit = utils.layout_widget_by_name(vbox2, name="lacze_lineEdit")
                formItems = [lacze_lineEdit]
                
            elif formElement.name == 'tytulAlternatywny':
                tytulAlternatywny_lineEdit = utils.layout_widget_by_name(vbox2, name="tytulAlternatywny_lineEdit")
                formItems = [tytulAlternatywny_lineEdit]
                
            # buttony
            btnHBox = QHBoxLayout()
            addBtn = QPushButton("Dodaj")
            addBtn.clicked.connect(addItem)
            remBtn = QPushButton("Usuń")
            remBtn.clicked.connect(removeItem)
            btnHBox.addWidget(addBtn)
            btnHBox.addWidget(remBtn)
            vbox2.addLayout(btnHBox)

            # QListWidget
            listWidget = QListWidget()
            listWidget.setObjectName(formElement.name + "_listWidget")
            listWidget.itemDoubleClicked.connect(setDataToListWidget)
            formElement.refObject = listWidget
            vbox2.addWidget(listWidget)
            
        for formElement in formElements:
            if (
                    formElement.type == 'gml:ReferenceType' or
                    formElement.type == "gml:AbstractFeatureMemberType" or
                    formElement.type == "gml:MultiSurfacePropertyType"
            ) and formElement.name in self.pomijane:
                continue  # pomiń element
            if formElement.name in ['zmiana','modyfikacja','regulacja','wydzielenie']:
                continue  # pomiń
            
            hbox = QHBoxLayout()  # wiersz formularza
            hbox.setObjectName(formElement.name + '_hbox')
            
            # label
            # zmiana nazw w formularzu
            mapowanieNazw = {'idIIP':'identyfikator',
                             'przestrzenNazw':'przestrzeń nazw',
                             'lokalnyId':'identyfikator lokalny',
                             'wersjaId':'identyfikator wersji',
                             'tytul':'tytuł',
                             'nazwaSkrocona':'nazwa skrócona',
                             'numerIdentyfikacyjny':'numer identyfikacyjny',
                             'organUstanawiajacy':'organ ustanawiający',
                             'data':'data',
                             'dataWejsciaWZycie':'data wejścia w życie',
                             'dataUchylenia':'data uchylenia',
                             'szczegoloweOdniesienie':'szczegółowe odniesienie',
                             'dziennikUrzedowy':'dziennik urzędowy',
                             'lacze':'łącze',
                             'uchwala':'uchwala',
                             'przystapienie':'przystąpienie',
                             'zmienia':'zmienia',
                             'uchyla':'uchyla',
                             'poczatekWersjiObiektu':'początek wersji obiektu',
                             'koniecWersjiObiektu':'koniec wersji obiektu',
                             'tytulAlternatywny':'tytuł alternatywny',
                             'typPlanu':'typ planu',
                             'poziomHierarchii':'poziom hierarchii',
                             'obowiazujeOd':'obowiązuje od',
                             'obowiazujeDo':'obowiązuje do',
                             'mapaPodkladowa':'mapa podkładowa',
                             'rozdzielczoscPrzestrzenna':'rozdzielczość przestrzenna',
                             'ukladOdniesieniaPrzestrzennego':'układ odniesienia przestrzennego',
                             'uniewaznia':'unieważnia'
                            }
            if formElement.name in mapowanieNazw:
                formElementName = mapowanieNazw[formElement.name]
            else:
                formElementName = formElement.name
            
            lbl = QLabel(text=prefix + formElementName + ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)
            
            input = self.__makeInput(formElement)
            formElement.refObject = input
            tooltipImg = self.__makeTooltip(formElement)
            
            if formElement.maxOccurs == "unbounded":    # pola wielokrotne np: mapaPodkladowa
                #zmiana nazwy
                if formElement.name == 'lacze':
                    groupbox = QGroupBox('łącze')
                elif formElement.name == 'mapaPodkladowa':
                    groupbox = QGroupBox('mapa podkładowa')
                elif formElement.name == 'tytulAlternatywny':
                    groupbox = QGroupBox('tytuł alternatywny')
                else:
                    groupbox = QGroupBox(formElement.name)
                
                vbox2 = QVBoxLayout()
                groupbox.setLayout(vbox2)
                vbox2.addLayout(hbox)
                
                hbox.addWidget(input)
                hbox.addWidget(tooltipImg)
                vbox.addWidget(groupbox)
                
                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    input.setVisible(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(
                        formElement.innerFormElements, vbox2, '  - ')
                        
                createListWidget(formElement.name)
                
            else:   # pola pojedyncze
                hbox.addWidget(input)
                if formElement.type == 'gmd:CI_Date_PropertyType':
                    input2 = NoScrollQComboBox()
                    input2.setObjectName(formElement.name + '_cmbbx')
                    input2.addItems(dictionaries.cI_DateTypeCode.keys())
                    formElement.refObject = [input, input2]
                    
                    hbox.addWidget(input2)
                    
                hbox.addWidget(tooltipImg)
                vbox.addLayout(hbox)
                
                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    input.setEnabled(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(formElement.innerFormElements, vbox, '  - ')


    def __makeInput(self, formElement):
        # pole wprowadzania
        if formElement.name == "ukladOdniesieniaPrzestrzennego":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.ukladyOdniesieniaPrzestrzennego.keys())
        elif formElement.name == "typPlanu":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.typyPlanu.keys())
        elif formElement.name == "poziomHierarchii":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(reversed(list(dictionaries.poziomyHierarchii.keys())[1:]))
        elif formElement.name == "status":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.statusListaKodowa.keys())
        elif formElement.name == "dziennikUrzedowy":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            dict1 = dictionaries.dziennikUrzedowyKod.keys()
            values = ['']
            values.extend(list(dict1))
            input.addItems(values)
        elif formElement.type == 'dateTime':
            input = NoScrollQgsDateTimeEdit()
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'date':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'gmd:CI_Date_PropertyType':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'integer':
            input = QgsFilterLineEdit()
            # tylko liczby calkowite
            if formElement.name == 'rozdzielczoscPrzestrzenna':
                input.setValidator(QRegExpValidator(
                    QRegExp("^[\d]{0,10}")))
            else:
                input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            # tylko ciąg znaków
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            if formElement.name == 'opis':
                input.setValidator(QRegExpValidator(QRegExp("^[\d\D\s\S\w\W]{0,1000}")))
            input.setObjectName(formElement.name + '_lineEdit')
        
        input.setMinimumHeight(20)
        
        # dodanie kontroli wypełnienia atrybutów obligatoryjnych
        name = formElement.name
        if formElement.minOccurs == 1 or name == 'obowiazujeDo':
            if not name in ['ukladOdniesieniaPrzestrzennego','poziomHierarchii','typPlanu','wersjaId','obowiazujeDo']:
                input.setStyleSheet("border: 1px solid red")
            if isinstance(input,QgsFilterLineEdit) and not name in ['wersjaId','idIIP']:
                input.textChanged.connect(lambda text: self.kontrola(text, input, name))
            elif isinstance(input,NoScrollQgsDateTimeEdit):
                input.valueChanged.connect(lambda text: self.kontrola(text, input, name))
            elif isinstance(input,NoScrollQComboBox):
                input.currentTextChanged.connect(lambda text: self.kontrola(text, input, name))
        
        # ustawienie domyślnych wartości
        fullFormElementName = formElement.form + ":" + formElement.name
        
        # ustawienie podpowiedzi
        if fullFormElementName in dictionaries.placeholders.keys():
            input.setPlaceholderText('np.: ' + dictionaries.placeholders[fullFormElementName])  # dla pól tekstowych
            
        return input


    def kontrola(self, txt, obj, name):
        if txt == '' or txt == 'wybierz' or (txt == PyQt5.QtCore.QDateTime() and name != 'obowiazujeDo'):
            obj.setStyleSheet("border: 1px solid red")
        else:
            obj.setStyleSheet("")
        
        try:
            if name == 'data' and obj.date().toString("dd-MM-yyyy") != '' and obj.parent().title() == 'mapa podkładowa':
                referencja_lineEdit = utils.layout_widget_by_name(obj.parent().children()[0], name="referencja_lineEdit")
                referencja_lineEdit.setStyleSheet("")
        except:
            pass
        
        try:
            if name == 'data' and obj.date().toString("dd-MM-yyyy") == '' and obj.parent().title() == 'mapa podkładowa':
                referencja_lineEdit = utils.layout_widget_by_name(obj.parent().children()[0], name="referencja_lineEdit")
                referencja_lineEdit.setStyleSheet("border: 1px solid red")
        except:
            pass
        
        if name == 'status':
            self.obowiazujeDo_dateTimeEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="obowiazujeDo_dateTimeEdit")
            if txt == 'nieaktualny' and self.obowiazujeDo_dateTimeEdit.dateTime() == PyQt5.QtCore.QDateTime():
                self.obowiazujeDo_dateTimeEdit.setStyleSheet("border: 1px solid red")
            else:
                self.obowiazujeDo_dateTimeEdit.setStyleSheet("")
        
        if name == 'obowiazujeDo':
            try:
                self.status_cmbbx = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="status_cmbbx")
                if self.status_cmbbx.currentText() == 'nieaktualny' and txt == PyQt5.QtCore.QDateTime():
                    self.obowiazujeDo_dateTimeEdit.setStyleSheet("border: 1px solid red")
                else:
                    self.obowiazujeDo_dateTimeEdit.setStyleSheet("")
            except:
                pass
        
        if name == 'status':
            self.obowiazujeDo_lbl = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="obowiazujeDo_lbl")
            if txt == 'nieaktualny':
                self.obowiazujeDo_lbl.setText("obowiązuje do*")
            else:
                self.obowiazujeDo_lbl.setText("obowiązuje do")


    def __makeTooltip(self, formElement):
        fullFormElementName = formElement.form + ":" + formElement.name
        tooltipImg = QLabel()
        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')
        tooltipImg.setMaximumWidth(16)
        tooltipImg.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))
        placeholder = ""
        if fullFormElementName in dictionaries.placeholders.keys():
            placeholder = '<br><br>np.: ' + \
                dictionaries.placeholders[fullFormElementName]
        tooltipImg.setToolTip(
            "<FONT COLOR=black>%s</FONT><b>%s</b>" % (formElement.documentation, placeholder))  # dodanie tooltip z documentation 'rich text' dla zawijania
        tooltipImg.setObjectName(formElement.name + '_tooltip')
        return tooltipImg


    def setDefaultValues(self):
        s = QgsSettings()
        for fe in self.formElements:
            try:
                valuePath = "qgis_app2/settings/%s" % fe.name
                feValue = s.value(valuePath, "")
                utils.setValueToWidget(fe, feValue)
            except:
                pass
            for inner in fe.innerFormElements:
                try:
                    valuePath = "qgis_app2/settings/%s" % inner.name
                    feValue = s.value(valuePath, "")
                    utils.setValueToWidget(inner, feValue)
                except:
                    pass