# -*- coding: utf-8 -*-
"""
Created on Sun May 28 20:01:31 2023

@author: Marcin Lebiecki
"""

# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *
from pathlib import Path
import configparser
import re
import string
from datetime import date, datetime, timezone
from qgis.core import QgsProject, NULL, QgsSettings
from PyQt5.QtCore import QDateTime, QDate, QTime, QRegExp


def my_form_open(dialog, layer, feature):
    global atrybuty, geometria, obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
    global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
    global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
    global wylaczenieZabudowyZagrodowej, odlegloscDoSzkolyPodstawowej, odlegloscDoObszarowZieleniPublicznej
    global powierzchniaLacznaObszarowZieleniPublicznej, odlegloscDoObszaruZieleniPublicznej, powierzchniaObszaruZieleniPublicznej
    global odlegloscDoPrzedszkola, odlegloscDoZlobka, odlegloscDoAmbulatoriumPOZ, odlegloscDoBiblioteki, odlegloscDoDomuKultury
    global odlegloscDoDomuPomocySpolecznej, odlegloscDoUrzadzonegoTerenuSportu, odlegloscDoPrzystanku, odlegloscDoPlacowkiPocztowej
    global odlegloscDoApteki, odlegloscDoPosterunkuPolicji, odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej
    global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
    global czyObiektZmieniony, czyWersjaZmieniona
    
    atrybuty = feature.attributes()
    geometria = feature.geometry()
    obj = feature
    dlg = dialog
    if dlg.parent() == None:
        return
    try:
        dlg.parent().setWindowTitle("Atrybuty OSD, nazwa warstwy: " + layer.name())
        dlg.parent().setMinimumWidth(670)
        dlg.parent().setMaximumWidth(700)
        dlg.parent().setMaximumHeight(590)
    except:
        pass
    
    warstwa = layer
    warstwa.geometryOptions().setGeometryPrecision(0.01)
    warstwa.startEditing()
    qgis.utils.iface.setActiveLayer(warstwa)
    
    mainPath = Path(QgsApplication.qgisSettingsDirPath())/Path("python/plugins/wtyczka_qgis_app/")
    teryt_gminy = ''
    dataCzasTeraz = datetime.utcnow()
    
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
    numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
    jpt = s.value("qgis_app2/settings/jpt", "")
    idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
    
    placeHolders = {'przestrzenNazw':'np. PL.ZIPPZP.2393/246601-POG',
                    'lokalnyId':'np. 1OSD',
                    'oznaczenie':'np. 1OSD',
                    'symbol':'np. OSD',
                    'minimalnaOdleglosc':'wartość w metrach np. 1500',
                    'minOdlegloscOdObszaruZieleniPublicznej':'wartość w metrach np. 3000',
                    'powierzchnia obszaru':'wartość w hektarach min. 10',
                    'powierzchnia obszarow':'wartość w hektarach min. 1.5'
                    }
    
    pomoc = ['Przestrzeń nazw identyfikująca w sposób jednoznaczny źródło danych obiektu, o której mowa w § 5 ust. 1 pkt 1 rozporządzenia.\nWartość atrybutu przestrzeń nazw powinna jednoznacznie identyfikować zbiór danych przestrzennych, do którego należy instancja typu obiektu.',
             'Identyfikator lokalny obiektu, o którym mowa w § 5 ust. 1 pkt 2 oraz § 5 ust. 1a rozporządzenia, przypisany przez dostawcę danych.\nUnikalność identyfikatora w przestrzeni nazw gwarantuje dostawca zbioru danych przestrzennych.',
             'Identyfikator poszczególnej wersji obiektu przestrzennego, o którym mowa w § 5 ust. 1 pkt 3 rozporządzenia, przypisany przez dostawcę danych.\nW zestawie wszystkich wersji danego obiektu identyfikator wersji jest unikalny.',
             'Nazwa regulacji.',
             'Ciąg literowo-liczbowy, który określa regulację.',
             'Ciąg literowy stosowany do określenia rodzaju regulacji.',
             'Charakter prawny regulacji.',
             'Data, od której dana wersja obiektu przestrzennego obowiązuje.',
             'Data, do której dana wersja obiektu przestrzennego obowiązywała.',
             'Ogólne wskazanie etapu procesu planowania, na którym znajduje się wersja obiektu przestrzennego.',
             'Data i godzina, w której wersja obiektu została wprowadzona do zbioru danych przestrzennych\n lub zmieniona w tym zbiorze danych przestrzennych.',
             'Data i godzina, w której wersja obiektu została zastąpiona w zbiorze danych przestrzennych\n lub wycofana z tego zbioru danych przestrzennych.',
             'Informacja o wyłączeniu terenów zabudowy zagrodowej o którym mowa w art. 13f ust. 7 pkt 5 ustawy\n z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.',
             'Maksymalna odległość, o której mowa w art. 13f ust. 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym,\n od granicy działki ewidencyjnej do budynku szkoły podstawowej.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość, o której mowa w art. 13f ust. 3 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym,\n od granicy działki ewidencyjnej do granicy obszarów zieleni publicznej, o których mowa w art. 13f ust. 3 pkt 1 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Łączna powierzchnia obszarów zieleni publicznej, o których mowa w art. 13f ust. 3 pkt 1 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu jest wyrażona liczbą dziesiętną.',
             'Maksymalna odległość, o której mowa w art. 13f ust. 3 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym,\n od granicy działki ewidencyjnej do granicy obszaru zieleni publicznej, o którym mowa w art. 13f ust. 3 pkt 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Powierzchnia obszaru zieleni publicznej, o którym mowa w art. 13f ust. 3 pkt 2 ustawy\n z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu jest wyrażona liczbą dziesiętną.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do przedszkola.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do żłobka.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do ambulatorium podstawowej opieki zdrowotnej.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do biblioteki.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do domu kultury.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do domu pomocy społecznej.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do urządzonego terenu sportu.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do przystanku publicznego transportu zbiorowego.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do placówki pocztowej.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do apteki.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do posterunku policji.\nWartość atrybutu jest wyrażona liczbą całkowitą.',
             'Maksymalna odległość liczona jako droga dojścia ogólnodostępną\n trasą dla pieszych od granicy działki ewidencyjnej do posterunku jednostki ochrony przeciwpożarowej.\nWartość atrybutu jest wyrażona liczbą całkowitą.']
    
    atrybuty.append('geometria')
    listaBledowAtrybutow = [0 for i in range(len(atrybuty))]
    
    atrybutyPOG = odczytajAtrybutyZPOG()
    
    wersjaId = dialog.findChild(QDateTimeEdit,"wersjaId")
    wersjaId.dateTimeChanged.connect(wersjaId_kontrola)
    if obj.id() < 0: wersjaId.setDateTime(dataCzasTeraz)
    
    poczatekWersjiObiektu = dialog.findChild(QDateTimeEdit,"poczatekWersjiObiektu")
    poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)
    if obj.id() < 0: poczatekWersjiObiektu.setDateTime(dataCzasTeraz)
    
    przestrzenNazw = dialog.findChild(QLineEdit,"przestrzenNazw")
    przestrzenNazw.setToolTip('')
    przestrzenNazw.setPlaceholderText(placeHolders['przestrzenNazw'])
    przestrzenNazw.textChanged.connect(przestrzenNazw_kontrola)
    
    lokalnyId = dialog.findChild(QLineEdit,"lokalnyId")
    lokalnyId.setToolTip('')
    lokalnyId.setPlaceholderText(placeHolders['lokalnyId'])
    lokalnyId.textChanged.connect(lokalnyId_kontrola)
    if obj.id() <0: lokalnyId_kontrola('')
    
    nazwa = dialog.findChild(QLineEdit,"nazwa")
    koniecWersjiObiektu = dialog.findChild(QDateTimeEdit,"koniecWersjiObiektu")
     
    oznaczenie = dialog.findChild(QLineEdit,"oznaczenie")
    oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
    oznaczenie.textChanged.connect(oznaczenie_kontrola)
    if oznaczenie.text() == 'NULL' or oznaczenie.text() == None:
        oznaczenie.setText('')
    else:
        oznaczenie_kontrola(oznaczenie.text())
    
    symbol = dialog.findChild(QLineEdit,"symbol")
    symbol.setPlaceholderText(placeHolders['symbol'])
    symbol.textChanged.connect(symbol_kontrola)
    if symbol.text() == 'NULL': symbol.setText('')
    
    charakterUstalenia = dialog.findChild(QComboBox,"charakterUstalenia")
    charakterUstalenia.currentTextChanged.connect(charakterUstalenia_kontrola)
    if obj.id() < 0: charakterUstalenia.setCurrentIndex(0)
    
    obowiazujeOd = dialog.findChild(QDateTimeEdit,"obowiazujeOd")
    obowiazujeOd_label = dialog.findChild(QLabel,"obowiazujeOd_label")
    obowiazujeOd.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    obowiazujeDo = dialog.findChild(QDateTimeEdit,"obowiazujeDo")
    obowiazujeDo_label = dialog.findChild(QLabel,"obowiazujeDo_label")
    obowiazujeDo.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    status = dialog.findChild(QComboBox,"status")
    status.currentTextChanged.connect(status_kontrola)
    if obj.id() < 0 and atrybutyPOG != None:
        status.setCurrentText(atrybutyPOG['status'])
    status_kontrola(status.currentText())
    
    koniecWersjiObiektu.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    koniecWersjiObiektu.setMaximumDate(QDate.currentDate())
    
    wylaczenieZabudowyZagrodowej = dialog.findChild(QCheckBox,"wylaczenieZabudowyZagrodowej")
    wylaczenieZabudowyZagrodowej.stateChanged.connect(wylaczenieZabudowyZagrodowej_kontrola)
    
    odlegloscDoSzkolyPodstawowej = dialog.findChild(QLineEdit,"odlegloscDoSzkolyPodstawowej")
    odlegloscDoSzkolyPodstawowej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoSzkolyPodstawowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoSzkolyPodstawowej.textChanged.connect(odlegloscDoSzkolyPodstawowej_kontrola)
    if obj.id() < 0: odlegloscDoSzkolyPodstawowej_kontrola('')
    
    odlegloscDoObszarowZieleniPublicznej = dialog.findChild(QLineEdit,"odlegloscDoObszarowZieleniPublicznej")
    odlegloscDoObszarowZieleniPublicznej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoObszarowZieleniPublicznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoObszarowZieleniPublicznej.textChanged.connect(odlegloscDoObszarowZieleniPublicznej_kontrola)
    if obj.id() < 0: odlegloscDoObszarowZieleniPublicznej_kontrola('')
    
    powierzchniaLacznaObszarowZieleniPublicznej = dialog.findChild(QLineEdit,"powierzchniaLacznaObszarowZieleniPublicznej")
    powierzchniaLacznaObszarowZieleniPublicznej.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{0,5}\.([0-9]{1})?")))
    powierzchniaLacznaObszarowZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszarow'])
    powierzchniaLacznaObszarowZieleniPublicznej.setText(powierzchniaLacznaObszarowZieleniPublicznej.text().replace(",","."))
    powierzchniaLacznaObszarowZieleniPublicznej.textChanged.connect(powierzchniaLacznaObszarowZieleniPublicznej_kontrola)
    if obj.id() < 0: powierzchniaLacznaObszarowZieleniPublicznej_kontrola('')
    
    odlegloscDoObszaruZieleniPublicznej = dialog.findChild(QLineEdit,"odlegloscDoObszaruZieleniPublicznej")
    odlegloscDoObszaruZieleniPublicznej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoObszaruZieleniPublicznej.setPlaceholderText(placeHolders['minOdlegloscOdObszaruZieleniPublicznej'])
    odlegloscDoObszaruZieleniPublicznej.textChanged.connect(odlegloscDoObszaruZieleniPublicznej_kontrola)
    if obj.id() < 0: odlegloscDoObszaruZieleniPublicznej_kontrola('')
    
    powierzchniaObszaruZieleniPublicznej = dialog.findChild(QLineEdit,"powierzchniaObszaruZieleniPublicznej")
    powierzchniaObszaruZieleniPublicznej.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{1,5}\.([0-9]{1})?")))
    powierzchniaObszaruZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszaru'])
    powierzchniaObszaruZieleniPublicznej.setText(powierzchniaObszaruZieleniPublicznej.text().replace(",","."))
    powierzchniaObszaruZieleniPublicznej.textChanged.connect(powierzchniaObszaruZieleniPublicznej_kontrola)
    if obj.id() < 0: powierzchniaObszaruZieleniPublicznej_kontrola('')
    
    odlegloscDoPrzedszkola = dialog.findChild(QLineEdit,"odlegloscDoPrzedszkola")
    odlegloscDoPrzedszkola.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoPrzedszkola.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoPrzedszkola.textChanged.connect(odlegloscDoPrzedszkola_kontrola)
    
    odlegloscDoZlobka = dialog.findChild(QLineEdit,"odlegloscDoZlobka")
    odlegloscDoZlobka.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoZlobka.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoZlobka.textChanged.connect(odlegloscDoZlobka_kontrola)
    
    odlegloscDoAmbulatoriumPOZ = dialog.findChild(QLineEdit,"odlegloscDoAmbulatoriumPOZ")
    odlegloscDoAmbulatoriumPOZ.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoAmbulatoriumPOZ.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoAmbulatoriumPOZ.textChanged.connect(odlegloscDoAmbulatoriumPOZ_kontrola)
    
    odlegloscDoBiblioteki = dialog.findChild(QLineEdit,"odlegloscDoBiblioteki")
    odlegloscDoBiblioteki.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoBiblioteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoBiblioteki.textChanged.connect(odlegloscDoBiblioteki_kontrola)
    
    odlegloscDoDomuKultury = dialog.findChild(QLineEdit,"odlegloscDoDomuKultury")
    odlegloscDoDomuKultury.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoDomuKultury.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoDomuKultury.textChanged.connect(odlegloscDoDomuKultury_kontrola)
    
    odlegloscDoDomuPomocySpolecznej = dialog.findChild(QLineEdit,"odlegloscDoDomuPomocySpolecznej")
    odlegloscDoDomuPomocySpolecznej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoDomuPomocySpolecznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoDomuPomocySpolecznej.textChanged.connect(odlegloscDoDomuPomocySpolecznej_kontrola)
    
    odlegloscDoUrzadzonegoTerenuSportu = dialog.findChild(QLineEdit,"odlegloscDoUrzadzonegoTerenuSportu")
    odlegloscDoUrzadzonegoTerenuSportu.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoUrzadzonegoTerenuSportu.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoUrzadzonegoTerenuSportu.textChanged.connect(odlegloscDoUrzadzonegoTerenuSportu_kontrola)
    
    odlegloscDoPrzystanku = dialog.findChild(QLineEdit,"odlegloscDoPrzystanku")
    odlegloscDoPrzystanku.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoPrzystanku.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoPrzystanku.textChanged.connect(odlegloscDoPrzystanku_kontrola)
    
    odlegloscDoPlacowkiPocztowej = dialog.findChild(QLineEdit,"odlegloscDoPlacowkiPocztowej")
    try:
        odlegloscDoPlacowkiPocztowej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    except:
        pass
    odlegloscDoPlacowkiPocztowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoPlacowkiPocztowej.textChanged.connect(odlegloscDoPlacowkiPocztowej_kontrola)
    
    odlegloscDoApteki = dialog.findChild(QLineEdit,"odlegloscDoApteki")
    odlegloscDoApteki.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoApteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoApteki.textChanged.connect(odlegloscDoApteki_kontrola)
    
    odlegloscDoPosterunkuPolicji = dialog.findChild(QLineEdit,"odlegloscDoPosterunkuPolicji")
    odlegloscDoPosterunkuPolicji.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoPosterunkuPolicji.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoPosterunkuPolicji.textChanged.connect(odlegloscDoPosterunkuPolicji_kontrola)
    
    odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej = dialog.findChild(QLineEdit,"odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej")
    odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setValidator(QRegExpValidator(QRegExp("[1-9]\d{0,4}")))
    odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.textChanged.connect(odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej_kontrola)
    
    geometria_kontrola()
    poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    czyWersjaZmieniona = False
    
    zapisz = dialog.findChild(QPushButton,"zapisz")
    zapisz.clicked.connect(zapis)
    zapisz.setEnabled(False)
    zapisz.setText("Zapisz")
    
    przestrzenNazw_kontrola()
    
    labels = [None for i in range(30)]
    pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
    for i in range(30):
        labels[i] = dialog.findChild(QLabel,"label_" + str(i + 1))
        labels[i].setPixmap(pixmap)
        labels[i].setToolTip(pomoc[i])


def komunikowanieBledu(object, txt, nazwaAtrybutu):
    try:
        object.setToolTip(txt)
        if txt == '':
            listaBledowAtrybutow[obj.fieldNameIndex(nazwaAtrybutu)] = 0
            object.setStyleSheet("")
            wlaczenieZapisu()
        else:
            listaBledowAtrybutow[obj.fieldNameIndex(nazwaAtrybutu)] = 1
            object.setStyleSheet("border: 1px solid red")
            wylaczenieZapisu()
    except:
        pass


def zmianaWersjiIPoczatkuWersji():
    dataCzasTeraz = datetime.utcnow()
    if czyObiektZmieniony and koniecWersjiObiektu.dateTime().time().msec() != 0 and koniecWersjiObiektu.dateTime().date().year() != 1 and not czyWersjaZmieniona:
        wersjaId.setDateTime(dataCzasTeraz)
        poczatekWersjiObiektu.disconnect()
        poczatekWersjiObiektu.setDateTime(dataCzasTeraz)
        poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)


def wlaczenieZapisu():
    global czyObiektZmieniony
    try:
        if sum(listaBledowAtrybutow) == 0 and warstwa.isEditable():
            zapisz.setEnabled(True)
            zapisz.setText("Zapisz")
            czyObiektZmieniony = True
            zmianaWersjiIPoczatkuWersji()
    except:
        pass


def wylaczenieZapisu():
    global czyObiektZmieniony
    try:
        if sum(listaBledowAtrybutow) != 0 or not warstwa.isEditable():
            czyObiektZmieniony = False
            zapisz.setEnabled(False)
    except:
        pass


def zapis():
    try:
        dlg.save()
        warstwa.commitChanges(False)
        zapisz.setEnabled(False)
        zapisz.setText("Zapisano")
        
        if obj.id() < 0:
            dlg.parent().close()
    except:
        pass

# ----------------------------------------------------------------------------------------------------

def geometria_kontrola():
    try:
        validator = QgsGeometryValidator(obj.geometry())
        errors = validator.validateGeometry(obj.geometry())
        msg = ''
        for error in errors:
            msg = msg + error.what() + ' '
        if len(errors) != 0:
            dlg.displayWarning('Błędy w geometrii: ' + msg)
            listaBledowAtrybutow[obj.fieldNameIndex('geometria')] = 1
        else:
            listaBledowAtrybutow[obj.fieldNameIndex('geometria')] = 0
    except:
        pass


def przestrzenNazw_kontrola():
    try:
        if rodzajZbioru == '':
            komunikowanieBledu(przestrzenNazw,'Proszę w ustawieniach wybrać POG dla rodzaju zbioru i zapisać.','przestrzenNazw')
        elif numerZbioru == '':
            komunikowanieBledu(przestrzenNazw,'Proszę w ustawieniach wpisać numer zbioru i zapisać.','przestrzenNazw')
        elif jpt == '':
            komunikowanieBledu(przestrzenNazw,'Proszę w ustawieniach wpisać numer JPT i zapisać.','przestrzenNazw')
        else:
            txt = 'PL.ZIPPZP.' + numerZbioru + '/' + jpt + '-' + rodzajZbioru
            if przestrzenNazw.text() != txt:
                przestrzenNazw.setText(txt)
                komunikowanieBledu(przestrzenNazw,'','przestrzenNazw')
            teryt_gminy = przestrzenNazw.text().split("/")[1].split("-")[0]
    except:
        pass


def lokalnyId_kontrola(txt):
    try:
        if idLokalnyAPP == '':
            lokalnyId.setPlaceholderText(placeHolders['lokalnyId'])
            komunikowanieBledu(lokalnyId,'Proszę w ustawieniach wpisać identyfikator lokalny identyfikujący jednoznacznie i unikalnie akt planowania przestrzennego w zbiorze danych przestrzennych i zapisać.','lokalnyId')
        elif txt == '':
            lokalnyId.setText(idLokalnyAPP)
        elif txt != idLokalnyAPP:
            lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
        else:
            komunikowanieBledu(lokalnyId,'','lokalnyId')
    except:
        pass


def wersjaId_kontrola():
    global czyWersjaZmieniona
    try:
        if koniecWersjiObiektu.dateTime().time().msec() != 0 and koniecWersjiObiektu.dateTime().date().year() != 1:
            poczatekWersjiObiektu.disconnect()
            poczatekWersjiObiektu.setDateTime(wersjaId.dateTime())
            poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)
    except:
        pass


def poczatekWersjiObiektu_kontrola():
    global czyWersjaZmieniona
    try:
        if koniecWersjiObiektu.dateTime().time().msec() != 0 and koniecWersjiObiektu.dateTime().date().year() != 1:
            wersjaId.setDateTime(poczatekWersjiObiektu.dateTime())
            czyWersjaZmieniona = True
        poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    except:
        pass


def oznaczenie_kontrola(txt):
    try:
        if re.match('^[1-9][0-9]{0,4}$', txt) != None and symbol.text() != '':
            pozycjaKursora = len(txt)
            txt = str(txt) + symbol.text()
            oznaczenie.setText(txt)
            oznaczenie.setCursorPosition(pozycjaKursora)
            komunikowanieBledu(oznaczenie,'','oznaczenie')
            lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
        else:
            if txt == '' or re.match('^[1-9][0-9]{0,4}' + symbol.text() + '$', txt) == None:
                oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
                komunikowanieBledu(oznaczenie,'Należy wpisać liczbę naturalną. Symbol jest dodawany automatycznie.','oznaczenie')
            else:
                lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
                komunikowanieBledu(oznaczenie,'','oznaczenie')
        if not czyWartoscAtrybutuJestUnikalna('oznaczenie',txt):
            komunikowanieBledu(oznaczenie,'Oznaczenie nie jest unikalne w ramach warstwy.','oznaczenie')
    except:
        pass


def symbol_kontrola(txt):
    try:
        if txt == '':
            symbol.setPlaceholderText(placeHolders['symbol'])
            komunikowanieBledu(symbol,'Symbol jest polem obowiązkowym','symbol')
        else:
            komunikowanieBledu(symbol,'','symbol')
    except:
        pass


def charakterUstalenia_kontrola(txt):
    pass


def status_kontrola(txt):
    try:
        if txt == 'wybierz' or txt == None:
            komunikowanieBledu(status,'Należy wybrać wartość pola status','status')
        else:
            komunikowanieBledu(status,'','status')
        if txt == 'nieaktualny':
            obowiazujeDo_label.setText("obowiązuje do*")
            if obowiazujeDo.dateTime().toString("H:mm") not in ['0:00','23:59']:
                komunikowanieBledu(obowiazujeDo, 'Należy wybrać datę dla "obowiązuje do"', 'obowiazujeDo')
        else:
            poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    except:
        pass


def poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola():
    try:
        obowiazujeOdTxt = obowiazujeOd.dateTime().toString("H:mm")
        obowiazujeDoTxt = obowiazujeDo.dateTime().toString("H:mm")
        poczatekWersjiObiektuTxt = poczatekWersjiObiektu.dateTime().toString("H:mm")
        koniecWersjiObiektuTxt = koniecWersjiObiektu.dateTime().toString("H:mm")
        
        if obowiazujeOdTxt not in ['0:00','23:59']:
            komunikowanieBledu(obowiazujeOd, 'Należy wybrać datę dla "obowiązuje od"', 'obowiazujeOd')
        else:
            if obowiazujeDoTxt in ['0:00','23:59'] and obowiazujeOd.dateTime() >= obowiazujeDo.dateTime():
                komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
            else:
                komunikowanieBledu(obowiazujeOd, '', 'obowiazujeOd')
        if koniecWersjiObiektuTxt in ['0:00','23:59'] and koniecWersjiObiektu.dateTime().date().year() != 1 and poczatekWersjiObiektu.dateTime() >= koniecWersjiObiektu.dateTime():
            komunikowanieBledu(poczatekWersjiObiektu,'Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu','poczatekWersjiObiektu')
            komunikowanieBledu(koniecWersjiObiektu,'Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu','koniecWersjiObiektu')
        else:
            komunikowanieBledu(poczatekWersjiObiektu,'','poczatekWersjiObiektu')
            komunikowanieBledu(koniecWersjiObiektu,'','koniecWersjiObiektu')
            if koniecWersjiObiektu.dateTime().date().year() != 1 and koniecWersjiObiektu.dateTime().time().msec() == 0 or status.currentText() == 'nieaktualny':
                obowiazujeDo_label.setText("obowiązuje do*")
                if obowiazujeDoTxt not in ['0:00','23:59']:
                    komunikowanieBledu(obowiazujeDo, 'Należy wybrać datę dla "obowiązuje do"', 'obowiazujeDo')
                else:
                    komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
            else:
                obowiazujeDo_label.setText("obowiązuje do")
                if (obowiazujeOd.dateTime() >= obowiazujeDo.dateTime() and obowiazujeDo.dateTime().time().msec() == 0 and obowiazujeOd.dateTime().time().msec() == 0):
                    komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
                else:
                    komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
    except:
        pass


def wylaczenieZabudowyZagrodowej_kontrola(txt):
    try:
        komunikowanieBledu(wylaczenieZabudowyZagrodowej,'','wylaczenieZabudowyZagrodowej')
    except:
        pass


def odlegloscDoSzkolyPodstawowej_kontrola(txt):
    try:
        if txt == '':
            komunikowanieBledu(odlegloscDoSzkolyPodstawowej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoSzkolyPodstawowej')
            odlegloscDoSzkolyPodstawowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        else:
            komunikowanieBledu(odlegloscDoSzkolyPodstawowej,'','odlegloscDoSzkolyPodstawowej')
    except:
        pass


def odlegloscDoObszarowZieleniPublicznej_kontrola(txt):
    try:
        if txt == '':
            komunikowanieBledu(odlegloscDoObszarowZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoObszarowZieleniPublicznej')
        else:
            komunikowanieBledu(odlegloscDoObszarowZieleniPublicznej,'','odlegloscDoObszarowZieleniPublicznej')
        
        odlegloscDoObszarowZieleniPublicznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
    except:
        pass


def powierzchniaLacznaObszarowZieleniPublicznej_kontrola(txt):
    try:
        txt = txt.replace(",",".")
        if txt == '':
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','powierzchniaLacznaObszarowZieleniPublicznej')
        elif not 1.5 <= float(txt):
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'Powierzchnia musi być większa lub równa 1,5 ha.','powierzchniaLacznaObszarowZieleniPublicznej')
        else:
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'','powierzchniaLacznaObszarowZieleniPublicznej')
        
        powierzchniaLacznaObszarowZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszarow'])
    except:
        pass


def odlegloscDoObszaruZieleniPublicznej_kontrola(txt):
    try:
        if txt == '':
            komunikowanieBledu(odlegloscDoObszaruZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoObszaruZieleniPublicznej')
        else:
            komunikowanieBledu(odlegloscDoObszaruZieleniPublicznej,'','odlegloscDoObszaruZieleniPublicznej')
        
        odlegloscDoObszaruZieleniPublicznej.setPlaceholderText(placeHolders['minOdlegloscOdObszaruZieleniPublicznej'])
    except:
        pass


def powierzchniaObszaruZieleniPublicznej_kontrola(txt):
    try:
        txt = txt.replace(",",".")
        if txt == '':
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','powierzchniaObszaruZieleniPublicznej')
        elif not 10 <= float(txt):
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'Powierzchnia musi być większa lub równa 10 ha.','powierzchniaObszaruZieleniPublicznej')
        else:
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'','powierzchniaObszaruZieleniPublicznej')
        
        powierzchniaObszaruZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszaru'])
    except:
        pass


def odlegloscDoPrzedszkola_kontrola(txt):
    try:
        odlegloscDoPrzedszkola.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoPrzedszkola,'','odlegloscDoPrzedszkola')
    except:
        pass


def odlegloscDoZlobka_kontrola(txt):
    try:
        odlegloscDoZlobka.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoZlobka,'','odlegloscDoZlobka')
    except:
        pass


def odlegloscDoAmbulatoriumPOZ_kontrola(txt):
    try:
        odlegloscDoAmbulatoriumPOZ.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoAmbulatoriumPOZ,'','odlegloscDoAmbulatoriumPOZ')
    except:
        pass


def odlegloscDoBiblioteki_kontrola(txt):
    try:
        odlegloscDoBiblioteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoBiblioteki,'','odlegloscDoBiblioteki')
    except:
        pass


def odlegloscDoDomuKultury_kontrola(txt):
    try:
        odlegloscDoDomuKultury.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoDomuKultury,'','odlegloscDoDomuKultury')
    except:
        pass


def odlegloscDoDomuPomocySpolecznej_kontrola(txt):
    try:
        odlegloscDoDomuPomocySpolecznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoDomuPomocySpolecznej,'','odlegloscDoDomuPomocySpolecznej')
    except:
        pass


def odlegloscDoUrzadzonegoTerenuSportu_kontrola(txt):
    try:
        odlegloscDoUrzadzonegoTerenuSportu.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoUrzadzonegoTerenuSportu,'','odlegloscDoUrzadzonegoTerenuSportu')
    except:
        pass


def odlegloscDoPrzystanku_kontrola(txt):
    try:
        odlegloscDoPrzystanku.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoPrzystanku,'','odlegloscDoPrzystanku')
    except:
        pass


def odlegloscDoPlacowkiPocztowej_kontrola(txt):
    try:
        odlegloscDoPlacowkiPocztowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoPlacowkiPocztowej,'','odlegloscDoPlacowkiPocztowej')
    except:
        pass


def odlegloscDoApteki_kontrola(txt):
    try:
        odlegloscDoApteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoApteki,'','odlegloscDoApteki')
    except:
        pass


def odlegloscDoPosterunkuPolicji_kontrola(txt):
    try:
        odlegloscDoPosterunkuPolicji.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoPosterunkuPolicji,'','odlegloscDoPosterunkuPolicji')
    except:
        pass


def odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej_kontrola(txt):
    try:
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej,'','odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej')
    except:
        pass


def czyWartoscAtrybutuJestUnikalna(atrybut, wartosc):
    wartoscAtrybutuJestUnikalna = True
    if koniecWersjiObiektu.dateTime().time().msec() != 0:
        request = QgsFeatureRequest(QgsExpression('koniecWersjiObiektu is NULL and ' + atrybut + "='" + wartosc + "'"))
        for x in warstwa.getFeatures(request):
            if x.id() != obj.id():
                wartoscAtrybutuJestUnikalna = False
    return wartoscAtrybutuJestUnikalna


def odczytajAtrybutyZPOG():
    try:
        warstwy = QgsProject().instance().mapLayers()
        atrybutyPOG = {}
        warstwaPOG = None
        for warstwaTMP in warstwy:
            if warstwaTMP.startswith('AktPlanowaniaPrzestrzennego'):
                warstwaPOG = warstwy[warstwaTMP]
                break
        if warstwaPOG != None and warstwaPOG.featureCount() > 0:
            for POG in warstwaPOG.getFeatures():
                atrybutyPOG['status'] = POG['status']
                atrybutyPOG['obowiazujeOd'] = POG['obowiazujeOd']
                atrybutyPOG['obowiazujeDo'] = POG['obowiazujeDo']
                break
            return atrybutyPOG
        else:
            return None
    except:
        pass