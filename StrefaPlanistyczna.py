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
from datetime import date, datetime
from qgis.core import QgsProject, NULL, QgsSettings
from qgis.gui import QgsCheckableComboBox
from PyQt5.QtCore import QDateTime, QDate, QTime, QRegExp
import locale
import os


def my_form_open(dialog, layer, feature):
    global atrybuty, geometria, obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy, mapaNazwaSymbol, mapaSymbolProfilDodatkowy
    global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol, symbolTXT
    global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, profilPodstawowy_QCCB, profilDodatkowy_QCCB
    global profilPodstawowy, profilDodatkowy, nazwa, nazwaAlternatywna, maksNadziemnaIntensywnoscZabudowy
    global maksUdzialPowierzchniZabudowy, maksWysokoscZabudowy, minUdzialPowierzchniBiologicznieCzynnej
    global klasaPrzeznaczeniaTerenuKod, mapaSymbolProfilPodstawowy, obowiazujeOd_label, obowiazujeDo_label
    global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
    global maksNadziemnaIntensywnoscZabudowy_label, maksWysokoscZabudowy_label, maksUdzialPowierzchniZabudowy_label
    global minUdzialPowierzchniBiologicznieCzynnej_label
    global czyObiektZmieniony, czyWersjaZmieniona
    
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    atrybuty = feature.attributes()
    geometria = feature.geometry()
    obj = feature
    dlg = dialog
    if dlg.parent() == None:
        return
    try:
        dlg.parent().setWindowTitle("Atrybuty SP, nazwa warstwy: " + layer.name())
        dlg.parent().setMaximumWidth(650)
        dlg.parent().setMaximumHeight(550)
    except:
        pass
    
    warstwa = layer
    warstwa.geometryOptions().setGeometryPrecision(0.01)
    warstwa.startEditing()
    qgis.utils.iface.setActiveLayer(warstwa)
    
    mainPath = Path(QgsApplication.qgisSettingsDirPath())/Path("python/plugins/wtyczka_qgis_app/")
    teryt_gminy = ''
    czyObiektZmieniony = False
    dataCzasTeraz = datetime.now()
    
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
    numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
    jpt = s.value("qgis_app2/settings/jpt", "")
    idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
    
    placeHolders = {'przestrzenNazw':'np. PL.ZIPPZP.2393/246601-POG',
                    'lokalnyId':'np. 1SP',
                    'nazwa':'np. strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną',
                    'oznaczenie':'np. 1SJ',
                    'nazwaAlternatywna':'np. osiedle Jantar',
                    'koniecWersjiObiektu':'np. 2023-01-31T12:34:58',
                    'maksNadziemnaIntensywnoscZabudowy':'np. 0.9',
                    'maksUdzialPowierzchniZabudowy':'wartość w procentach np. 30.1',
                    'maksWysokoscZabudowy':'wartość w metrach np. 15.5',
                    'minUdzialPowierzchniBiologicznieCzynnej':'wartość w procentach np. 30.1'
                    }
    
    mapaNazwaSymbol = {"strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną":"SW",
                       "strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną":"SJ",
                       "strefa wielofunkcyjna z zabudową zagrodową":"SZ",
                       "strefa usługowa":"SU",
                       "strefa handlu wielkopowierzchniowego":"SH",
                       "strefa gospodarcza":"SP",
                       "strefa produkcji rolniczej":"SR",
                       "strefa infrastrukturalna":"SI",
                       "strefa zieleni i rekreacji":"SN",
                       "strefa cmentarzy":"SC",
                       "strefa górnictwa":"SG",
                       "strefa otwarta":"SO",
                       "strefa komunikacyjna":"SK",
                       "wybierz":"wybierz"
                      }
    
    klasaPrzeznaczeniaTerenuKod = { "RA":"teren akwakultury i obsługi rybactwa",
                                    "KDA":"teren autostrady",
                                    "PEB":"teren biogazowni",
                                    "C":"teren cmentarza",
                                    "KDS":"teren drogi ekspresowej",
                                    "KDG":"teren drogi głównej",
                                    "KDR":"teren drogi głównej ruchu przyspieszonego",
                                    "KDZ":"teren drogi zbiorczej",
                                    "PEG":"teren elektrowni geotermalnej",
                                    "PEF":"teren elektrowni słonecznej",
                                    "PEW":"teren elektrowni wiatrowej",
                                    "PEO":"teren elektrowni wodnej",
                                    "G":"teren górnictwa i wydobycia",
                                    "H":"teren handlu wielkopowierzchniowego",
                                    "I":"teren infrastruktury technicznej",
                                    "K":"teren komunikacji",
                                    "KKL":"teren komunikacji kolei linowej",
                                    "KK":"teren komunikacji kolejowej i szynowej",
                                    "KL":"teren komunikacji lotniczej",
                                    "KW":"teren komunikacji wodnej",
                                    "L":"teren lasu",
                                    "KO":"teren obsługi komunikacji",
                                    "ZD":"teren ogrodów działkowych",
                                    "ZB":"teren plaży",
                                    "P":"teren produkcji",
                                    "RZP":"teren produkcji w gospodarstwach rolnych",
                                    "RN":"teren rolnictwa z zakazem zabudowy",
                                    "PS":"teren składów i magazynów",
                                    "U":"teren usług",
                                    "UA":"teren usług biurowych i administracji",
                                    "UE":"teren usług edukacji",
                                    "UG":"teren usług gastronomii",
                                    "UH":"teren usług handlu",
                                    "UHD":"teren usług handlu detalicznego",
                                    "UR":"teren usług kultu religijnego",
                                    "UK":"teren usług kultury i rozrywki",
                                    "UN":"teren usług nauki",
                                    "UL":"teren usług rzemieślniczych",
                                    "US":"teren usług sportu i rekreacji",
                                    "UT":"teren usług turystyki",
                                    "UZ":"teren usług zdrowia i pomocy społecznej",
                                    "RZW":"teren wielkotowarowej produkcji rolnej",
                                    "W":"teren wód",
                                    "ML":"teren zabudowy letniskowej lub rekreacji indywidualnej",
                                    "MN":"teren zabudowy mieszkaniowej jednorodzinnej",
                                    "MW":"teren zabudowy mieszkaniowej wielorodzinnej",
                                    "RZM":"teren zabudowy zagrodowej",
                                    "ZN":"teren zieleni naturalnej",
                                    "ZP":"teren zieleni urządzonej"
                                  }
    
    
    mapaSymbolProfilPodstawowy = {"SW":['MW','U','K','ZP','I'],
                                  "SJ":['MN','U','K','ZP','I'],
                                  "SZ":['RZM','RZP','RA','K','ZP','I'],
                                  "SU":['U','K','ZP','I'],
                                  "SH":['H','K','ZP','I'],
                                  "SP":['P','K','ZP','I'],
                                  "SR":['RZP','RZW','RA','K','I'],
                                  "SI":['I','K'],
                                  "SN":['ZP','ZB','W','K','I'],
                                  "SC":['C','K','ZP','I'],
                                  "SG":['G','K','I'],
                                  "SO":['RN','L','ZN','W','K','I'],
                                  "SK":['KDA','KDS','KDR','KDG','KK','KKL','KW','KL','KO','I'],
                                  "NULL":['NULL']
                                 }
    
    mapaSymbolProfilDodatkowy = {"SW":['MN','H','ZN','ZD','L','W'],
                                 "SJ":['ML','ZD','ZN','L','W'],
                                 "SZ":['RZW','RN','PEB','U','ZN','L','W'],
                                 "SU":['PS','PEF','ZN','L','W'],
                                 "SH":['U','PS','PEF','ZN','L','W'],
                                 "SP":['U','ZN','L','W'],
                                 "SR":['RN','PEB','PEF','PEW','PEO','ZP','ZN','L','W'],
                                 "SI":['U','P','ZP','ZN','L','W'],
                                 "SN":['US','UK','UHD','UG','UT','UN','UE','UZ','ZD','ZN','L'],
                                 "SC":['UR','UHD','ZN','L','W'],
                                 "SG":['P','UH','UL','UG','UA','UN','ZP','ZN','L','W'],
                                 "SO":['PEW','PEF','PEG','PEO','PEB','ZP'],
                                 "SK":['KDZ','UHD','UG','UT','ZP','L','ZN','W'],
                                 "NULL":['NULL']
                                }
    
    pomoc = ['Nazwa rodzajów stref planistycznych, o której mowa w art. 13c ust. 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.',
             'Ciąg literowy stosowany do określenia rodzaju wydzielenia planistycznego.',
             'Ciąg literowo-liczbowy, który określa wydzielenie planistyczne.',
             'Profil podstawowy będący obligatoryjnym elementem profilu funkcjonalnego strefy planistycznej, o którym mowa w art. 13e ust. 2 pkt 1 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.',
             'Profil dodatkowy będący fakultatywnym elementem profilu funkcjonalnego strefy planistycznej, o którym mowa w art. 13e ust. 2 pkt 1 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.',
             'Maksymalna nadziemna intensywność zabudowy o której mowa w art. 13e ust. 2 pkt 2 oraz ust. 3 pkt 1 i 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu podaje się z dokładnością do pierwszego miejsca po przecinku.',
             'Maksymalna wysokość zabudowy, o której mowa w art. 13e ust. 2 pkt 2 i ust. 3 pkt 1 i 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu podaje się z dokładnością do pierwszego miejsca po przecinku.',
             'Maksymalny udział powierzchni zabudowy, o którym mowa w art. 13e ust. 2 pkt 2 i ust. 3 pkt 1 i 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu jest wyrażona w % z dokładnością do pierwszego miejsca po przecinku.',
             'Minimalny udział powierzchni biologicznie czynnej, o której mowa w art. 13e ust. 2 pkt 3 i ust. 3 pkt 2 ustawy z dnia 27 marca 2003 r. o planowaniu i zagospodarowaniu przestrzennym.\nWartość atrybutu wyrażona jest w % z dokładnością do pierwszego miejsca po przecinku.',
             'Ogólne wskazanie etapu procesu planowania, na którym znajduje się wersja obiektu przestrzennego.',
             'Data, od której dana wersja obiektu przestrzennego obowiązuje.',
             'Data, do której dana wersja obiektu przestrzennego obowiązywała.',
             'Charakter prawny wydzielenia planistycznego.',
             'Nazwa alternatywna strefy planistycznej.',
             'Przestrzeń nazw identyfikująca w sposób jednoznaczny źródło danych obiektu, o której mowa w § 5 ust. 1 pkt 1 rozporządzenia.\nWartość atrybutu przestrzeń nazw powinna jednoznacznie identyfikować zbiór danych przestrzennych, do którego należy instancja typu obiektu.',
             'Identyfikator lokalny obiektu, o którym mowa w § 5 ust. 1 pkt 2 oraz § 5 ust. 1a rozporządzenia, przypisany przez dostawcę danych.\nUnikalność identyfikatora w przestrzeni nazw gwarantuje dostawca zbioru danych przestrzennych.',
             'Identyfikator poszczególnej wersji obiektu przestrzennego, o którym mowa w § 5 ust. 1 pkt 3 rozporządzenia, przypisany przez dostawcę danych.\nW zestawie wszystkich wersji danego obiektu identyfikator wersji jest unikalny.',
             'Data i godzina, w której wersja obiektu została wprowadzona do zbioru danych przestrzennych lub zmieniona w tym zbiorze danych przestrzennych.',
             'Data i godzina, w której wersja obiektu została zastąpiona w zbiorze danych przestrzennych lub wycofana z tego zbioru danych przestrzennych.'
            ]
    
    atrybuty.append('geometria')
    listaBledowAtrybutow = [0 for i in range(len(atrybuty))]
    
    try:
        warstwa.editingStarted.connect(wlaczenieWylaczenieProfiliDoEdycji)
        warstwa.editingStopped.connect(wlaczenieWylaczenieProfiliDoEdycji)
    except:
        pass
    
    atrybutyPOG = odczytajAtrybutyZPOG()
    
    profilPodstawowy = dlg.findChild(QLineEdit,"profilPodstawowy")
    qWidget = QWidget()
    profilPodstawowy_QCCB = QgsCheckableComboBox(qWidget)
    profilPodstawowy_QCCB.setMaximumHeight(20)
    profilPodstawowy_QCCB.setMinimumHeight(20)
    
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
    
    symbol = dialog.findChild(QComboBox,"symbol")
    symbol.currentTextChanged.connect(symbol_kontrola)
    symbol_kontrola(symbol.currentText())
    
    symbolTXT = symbol.currentText()
    
    oznaczenie = dialog.findChild(QLineEdit,"oznaczenie")
    oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
    oznaczenie.textChanged.connect(oznaczenie_kontrola)
    if oznaczenie.text() == 'NULL' or oznaczenie.text() == None:
        oznaczenie.setText('')
    else:
        oznaczenie_kontrola(oznaczenie.text())
    
    nazwa = dialog.findChild(QComboBox,"nazwa")
    
    charakterUstalenia = dialog.findChild(QComboBox,"charakterUstalenia")
    charakterUstalenia.currentTextChanged.connect(charakterUstalenia_kontrola)
    charakterUstalenia_kontrola(charakterUstalenia.currentText())
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
    
    koniecWersjiObiektu = dialog.findChild(QDateTimeEdit,"koniecWersjiObiektu")
    koniecWersjiObiektu.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    koniecWersjiObiektu.setMaximumDate(QDate.currentDate())
    
    nazwa.currentTextChanged.connect(nazwa_kontrola)
    if obj.id() < 0: nazwa_kontrola('wybierz')
    
    nazwaAlternatywna = dialog.findChild(QLineEdit,"nazwaAlternatywna")
    nazwaAlternatywna.setPlaceholderText(placeHolders['nazwaAlternatywna'])
    nazwaAlternatywna.textChanged.connect(nazwaAlternatywna_kontrola)
    nazwaAlternatywna.setText('')
    
    gridLayout = dlg.findChild(QGridLayout,"gridLayout")
    
    try:
        profilPodstawowy_QCCB.addItems(profilPodstawowy_createList())
    except:
        pass
    profilPodstawowy_QCCB.checkedItemsChanged.connect(profilPodstawowy_QCCB_kontrola)
    gridLayout.addWidget(profilPodstawowy_QCCB,3,1)
    profilPodstawowy_QCCB.setDefaultText('NULL')
    profilPodstawowy_reader()
    
    profilDodatkowy = dlg.findChild(QLineEdit,"profilDodatkowy")
    qWidget = QWidget()
    profilDodatkowy_QCCB = QgsCheckableComboBox(qWidget)
    try:
        profilDodatkowy_QCCB.addItems(profilDodatkowy_createList())
    except:
        pass
    
    profilDodatkowy_QCCB.checkedItemsChanged.connect(profilDodatkowy_QCCB_kontrola)
    gridLayout.addWidget(profilDodatkowy_QCCB,4,1)
    profilDodatkowy_QCCB.setDefaultText('NULL')
    profilDodatkowy_reader()
    
    wlaczenieWylaczenieProfiliDoEdycji()
    
    maksNadziemnaIntensywnoscZabudowy = dialog.findChild(QLineEdit,"maksNadziemnaIntensywnoscZabudowy")
    maksNadziemnaIntensywnoscZabudowy_label = dialog.findChild(QLabel,"maksNadziemnaIntensywnoscZabudowy_label")
    maksNadziemnaIntensywnoscZabudowy.setPlaceholderText(placeHolders['maksNadziemnaIntensywnoscZabudowy'])
    maksNadziemnaIntensywnoscZabudowy.setText(maksNadziemnaIntensywnoscZabudowy.text().replace(",","."))
    maksNadziemnaIntensywnoscZabudowy_kontrola(maksNadziemnaIntensywnoscZabudowy.text())
    maksNadziemnaIntensywnoscZabudowy.textChanged.connect(maksNadziemnaIntensywnoscZabudowy_kontrola)
    maksNadziemnaIntensywnoscZabudowy.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}\\.[0-9]?")))
    
    maksUdzialPowierzchniZabudowy = dialog.findChild(QLineEdit,"maksUdzialPowierzchniZabudowy")
    maksUdzialPowierzchniZabudowy_label = dialog.findChild(QLabel,"maksUdzialPowierzchniZabudowy_label")
    maksUdzialPowierzchniZabudowy.setPlaceholderText(placeHolders['maksUdzialPowierzchniZabudowy'])
    maksUdzialPowierzchniZabudowy.setText(maksUdzialPowierzchniZabudowy.text().replace(",","."))
    maksUdzialPowierzchniZabudowy_kontrola(maksUdzialPowierzchniZabudowy.text())
    maksUdzialPowierzchniZabudowy.textChanged.connect(maksUdzialPowierzchniZabudowy_kontrola)
    maksUdzialPowierzchniZabudowy.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}\\.[0-9]?")))
    
    maksWysokoscZabudowy = dialog.findChild(QLineEdit,"maksWysokoscZabudowy")
    maksWysokoscZabudowy_label = dialog.findChild(QLabel,"maksWysokoscZabudowy_label")
    maksWysokoscZabudowy.setPlaceholderText(placeHolders['maksWysokoscZabudowy'])
    maksWysokoscZabudowy.setText(maksWysokoscZabudowy.text().replace(",","."))
    maksWysokoscZabudowy_kontrola(maksWysokoscZabudowy.text())
    maksWysokoscZabudowy.textChanged.connect(maksWysokoscZabudowy_kontrola)
    maksWysokoscZabudowy.setValidator(QRegExpValidator(QRegExp("[0-9]{1,4}\\.[0-9]?")))
    
    minUdzialPowierzchniBiologicznieCzynnej = dialog.findChild(QLineEdit,"minUdzialPowierzchniBiologicznieCzynnej")
    minUdzialPowierzchniBiologicznieCzynnej_label = dialog.findChild(QLabel,"minUdzialPowierzchniBiologicznieCzynnej_label")
    minUdzialPowierzchniBiologicznieCzynnej.setPlaceholderText(placeHolders['minUdzialPowierzchniBiologicznieCzynnej'])
    minUdzialPowierzchniBiologicznieCzynnej.setText(minUdzialPowierzchniBiologicznieCzynnej.text().replace(",","."))
    minUdzialPowierzchniBiologicznieCzynnej_kontrola(minUdzialPowierzchniBiologicznieCzynnej.text())
    minUdzialPowierzchniBiologicznieCzynnej.textChanged.connect(minUdzialPowierzchniBiologicznieCzynnej_kontrola)
    minUdzialPowierzchniBiologicznieCzynnej.setValidator(QRegExpValidator(QRegExp("[0-9]{1,3}\\.[0-9]?")))
    
    geometria_kontrola()
    poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    czyWersjaZmieniona = False
    
    zapisz = dialog.findChild(QPushButton,"zapisz")
    zapisz.clicked.connect(zapis)
    zapisz.setEnabled(False)
    zapisz.setText("Zapisz")
    
    przestrzenNazw_kontrola()
    
    odczytajAtrybutyZPOG()
    
    labels = [None for i in range(19)]
    pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
    for i in range(19):
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
    dataCzasTeraz = datetime.now()
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
    dlg.save()
    warstwa.commitChanges(False)
    zapisz.setEnabled(False)
    zapisz.setText("Zapisano")
    
    if obj.id() < 0:
        dlg.parent().close()

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
        if re.match('^[1-9][0-9]{0,4}$', txt) != None and symbol.currentText() != 'wybierz':
            pozycjaKursora = len(txt)
            txt = str(txt) + symbol.currentText()
            oznaczenie.setText(txt)
            oznaczenie.setCursorPosition(pozycjaKursora)
            komunikowanieBledu(oznaczenie,'','oznaczenie')
            lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
        else:
            if txt == '' or re.match('^[1-9][0-9]{0,4}' + symbol.currentText() + '$', txt) == None:
                oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
                komunikowanieBledu(oznaczenie,'Należy wpisać liczbę naturalną. Symbol jest dodawany automatycznie.','oznaczenie')
            else:
                lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
                komunikowanieBledu(oznaczenie,'','oznaczenie')
        if not czyWartoscAtrybutuJestUnikalna('oznaczenie',txt):
            komunikowanieBledu(oznaczenie,'Oznaczenie nie jest unikalne w ramach warstwy.','oznaczenie')
    except:
        pass


def oznaczenie_uzupelnienie():
    try:
        if re.match('^[1-9][0-9]{0,2}S[W|J|Z|U|H|P|R|I|N|C|G|O|K]$', oznaczenie.text()) != None and oznaczenie.text() != 'wybierz':
            txt = oznaczenie.text().replace(symbolTXT, symbol.currentText())
            oznaczenie.setText(txt)
    except:
        pass


def symbol_kontrola(txt):
    global symbolTXT
    try:
        if txt == 'wybierz':
            komunikowanieBledu(symbol,'Symbol jest polem obowiązkowym','symbol')
            komunikowanieBledu(profilPodstawowy_QCCB,'Należy wybrać symbol lub nazwę','profilPodstawowy')
            nazwa.setCurrentText('wybierz')
            komunikowanieBledu(nazwa,'Należy wybrać wartość pola nazwa','nazwa')
            profilPodstawowy_QCCB.clear()
            profilDodatkowy_QCCB.clear()
        else:
            komunikowanieBledu(symbol,'','symbol')
            komunikowanieBledu(profilPodstawowy_QCCB,'','profilPodstawowy')
            nazwa.setCurrentText([k for k, v in mapaNazwaSymbol.items() if v == txt][0])
            oznaczenie_uzupelnienie()
            profilPodstawowy_QCCB.clear()
            profilDodatkowy_QCCB.clear()
            profilPodstawowy_QCCB.addItems(profilPodstawowy_createList())
            profilPodstawowy_QCCB.selectAllOptions()
            lista = []
            for l in mapaSymbolProfilPodstawowy[txt]:
                lista.append(klasaPrzeznaczeniaTerenuKod[l])
            profilPodstawowy.setText(','.join(lista))
        
            profilDodatkowy_QCCB.addItems(profilDodatkowy_createList())
            symbolTXT = symbol.currentText()
        oznaczenie_kontrola(oznaczenie.text())
        maksNadziemnaIntensywnoscZabudowy_kontrola(maksNadziemnaIntensywnoscZabudowy.text())
        maksUdzialPowierzchniZabudowy_kontrola(maksUdzialPowierzchniZabudowy.text())
        maksWysokoscZabudowy_kontrola(maksWysokoscZabudowy.text())
        minUdzialPowierzchniBiologicznieCzynnej_kontrola(minUdzialPowierzchniBiologicznieCzynnej.text())
    except:
        pass


def charakterUstalenia_kontrola(txt):
    try:
        komunikowanieBledu(charakterUstalenia,'','charakterUstalenia')
    except:
        pass


def status_kontrola(txt):
    try:
        if txt == 'wybierz' or txt == None:
            komunikowanieBledu(status,'Należy wybrać wartość pola status','status')
        else:
            komunikowanieBledu(status,'','status')
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
            if koniecWersjiObiektu.dateTime().date().year() != 1 and koniecWersjiObiektu.dateTime().time().msec() == 0:
                obowiazujeDo_label.setText("obowiązuje do*")
                if obowiazujeDoTxt not in ['0:00','23:59']:
                    komunikowanieBledu(obowiazujeDo, 'Należy wybrać datę dla "obowiązuje do"', 'obowiazujeDo')
                else:
                    komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
            else:
                obowiazujeDo_label.setText("obowiązuje do")
                if obowiazujeOdTxt not in ['0:00','23:59'] or obowiazujeOd.dateTime() < obowiazujeDo.dateTime():
                    komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
                else:
                    if obowiazujeOdTxt not in ['0:00','23:59'] or obowiazujeOd.dateTime() < obowiazujeDo.dateTime():
                        komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
                    else:
                        komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
                        komunikowanieBledu(obowiazujeDo, 'Atrybut "obowiązuje do" nie może być mniejszy lub równy od "obowiązuje od".','obowiazujeDo')
    except:
        pass


def nazwa_kontrola(txt):
    try:
        if txt == 'wybierz':
            komunikowanieBledu(nazwa,'Należy wybrać wartość pola nazwa','nazwa')
        else:
            komunikowanieBledu(nazwa,'','nazwa')
            maksWysokoscZabudowy_kontrola(maksWysokoscZabudowy.text()) 
        symbol.setCurrentText(mapaNazwaSymbol[txt])
    except:
        pass


def nazwaAlternatywna_kontrola(txt):
    try:
        nazwaAlternatywna.setPlaceholderText(placeHolders['nazwaAlternatywna'])
        komunikowanieBledu(nazwaAlternatywna,'','nazwaAlternatywna')
    except:
        pass


def profilPodstawowy_QCCB_kontrola(lista):
    try:
        if lista == [] and nazwa.currentText() == '':
            komunikowanieBledu(profilPodstawowy_QCCB,'Należy wybrać symbol lub nazwę','profilPodstawowy')
        elif len(lista) != len(profilPodstawowy_createList()):
            profilPodstawowy_QCCB.clear()
            profilPodstawowy_QCCB.addItems(profilPodstawowy_createList())
            profilPodstawowy_QCCB.selectAllOptions()
        else:
            komunikowanieBledu(profilPodstawowy_QCCB,'','profilPodstawowy')
    except:
        pass


def profilPodstawowy_reader():
    try:
        profilPodstawowy_QCCB.clear()
        listaProfiliPodstawowych = profilPodstawowy.text().split(",")
        for item in listaProfiliPodstawowych:
            profilPodstawowy_QCCB.addItem(item)
        profilPodstawowy_QCCB.selectAllOptions()
    except:
        pass


def profilPodstawowy_createList():
    try:
        lista = []
        for skrot in mapaSymbolProfilPodstawowy[symbol.currentText()]:
            lista.append(klasaPrzeznaczeniaTerenuKod[skrot])
        return lista
    except:
        pass


def profilDodatkowy_QCCB_kontrola(lista):
    try:
        if len(lista) != 0:
            profilDodatkowy.setText(','.join(lista))
        else:
            profilDodatkowy.setText('')
        komunikowanieBledu(profilDodatkowy_QCCB,'','profilDodatkowy_QCCB')
    except:
        pass


def profilDodatkowy_reader():
    try:
        lista = profilDodatkowy_createList()
        listaProfiliDodatkowych = profilDodatkowy.text().split(",")
        if listaProfiliDodatkowych != [''] and listaProfiliDodatkowych != ['NULL']:
            for item in listaProfiliDodatkowych:
                idx = lista.index(item)
                profilDodatkowy_QCCB.setItemCheckState(idx,2)
    except:
        pass


def profilDodatkowy_createList():
    try:
        lista = []
        for skrot in mapaSymbolProfilDodatkowy[symbol.currentText()]:
            lista.append(klasaPrzeznaczeniaTerenuKod[skrot])
        return lista
    except:
        pass


def maksNadziemnaIntensywnoscZabudowy_kontrola(txt):
    try:
        separator_dziesietny = locale.localeconv()['decimal_point']
        txt = txt.replace(",", separator_dziesietny)
        if txt != '' and not symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR'] and not 0 <= float(txt) <= 350:
            komunikowanieBledu(maksNadziemnaIntensywnoscZabudowy,'Wartość atrybutu podaje się z dokładnością do pierwszego miejsca po przecinku. Wartość musi być w przedziale <0;350>.','maksNadziemnaIntensywnoscZabudowy')
        elif symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR'] and (txt == '' or not 0 <= float(txt) <= 350):
            komunikowanieBledu(maksNadziemnaIntensywnoscZabudowy,'Wartość atrybutu podaje się z dokładnością do pierwszego miejsca po przecinku. Wartość musi być podana dla: ' + nazwa.currentText(),'maksNadziemnaIntensywnoscZabudowy')
        else:
            komunikowanieBledu(maksNadziemnaIntensywnoscZabudowy,'','maksNadziemnaIntensywnoscZabudowy')
        maksNadziemnaIntensywnoscZabudowy.setPlaceholderText(placeHolders['maksNadziemnaIntensywnoscZabudowy'])
        
        if symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR']:
            maksNadziemnaIntensywnoscZabudowy_label.setText("maksymalna nadziemna intensywność zabudowy*")
        else:
            maksNadziemnaIntensywnoscZabudowy_label.setText("maksymalna nadziemna intensywność zabudowy")
    except:
        pass


def maksUdzialPowierzchniZabudowy_kontrola(txt):
    try:
        separator_dziesietny = locale.localeconv()['decimal_point']
        txt = txt.replace(",", separator_dziesietny)
        if txt != '' and (not symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR'] and not 0 <= float(txt) <= 100):
            komunikowanieBledu(maksUdzialPowierzchniZabudowy,'Maksymalny udział powierzchni zabudowy powinien być w przedziale <0; 100>%.','maksUdzialPowierzchniZabudowy')
        elif symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR'] and (txt == '' or not 0 <= float(txt) <= 100):
            komunikowanieBledu(maksUdzialPowierzchniZabudowy,'Wartość atrybutu jest wyrażona w % z dokładnością do pierwszego miejsca po przecinku. \
Maksymalny udział powierzchni zabudowy wyznaczony dla strefy planistycznej nie może przekroczyć 100%.\
Wartość musi być podana dla: ' + nazwa.currentText(),'maksUdzialPowierzchniZabudowy')
        else:
            komunikowanieBledu(maksUdzialPowierzchniZabudowy,'','maksUdzialPowierzchniZabudowy')
        maksUdzialPowierzchniZabudowy.setPlaceholderText(placeHolders['maksUdzialPowierzchniZabudowy'])
        
        if symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR']:
            maksUdzialPowierzchniZabudowy_label.setText("maksymalny udział powierzchnii zabudowy*")
        else:
            maksUdzialPowierzchniZabudowy_label.setText("maksymalny udział powierzchnii zabudowy")
    except:
        pass


def maksWysokoscZabudowy_kontrola(txt):
    try:
        if symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR'] and txt == '':
            komunikowanieBledu(maksWysokoscZabudowy,'Wartość atrybutu podaje się z dokładnością do pierwszego miejsca po przecinku. Wartość musi być podana dla: ' + nazwa.currentText(),'maksWysokoscZabudowy')
        else:
            komunikowanieBledu(maksWysokoscZabudowy,'','maksWysokoscZabudowy')
        maksWysokoscZabudowy.setPlaceholderText(placeHolders['maksWysokoscZabudowy'])
        
        if symbol.currentText() in ['SW','SJ','SZ','SU','SH','SP','SR']:
            maksWysokoscZabudowy_label.setText("maksymalna wysokość zabudowy*")
        else:
            maksWysokoscZabudowy_label.setText("maksymalna wysokość zabudowy")
    except:
        pass


def minUdzialPowierzchniBiologicznieCzynnej_kontrola(txt):
    try:
        separator_dziesietny = locale.localeconv()['decimal_point']
        txt = txt.replace(",", separator_dziesietny)
        if txt != '' and (symbol.currentText() in ['SG','SO','SK','NULL'] and not 0 <= float(txt) <= 150):
            komunikowanieBledu(minUdzialPowierzchniBiologicznieCzynnej,'Minimalny udział powierzchni biologicznie czynnej powinien być w przedziale <0; 150>%.','minUdzialPowierzchniBiologicznieCzynnej')
        elif symbol.currentText() in ['SW','SJ','SZ','SU','SH','SR','SC'] and (txt == '' or not 30 <= float(txt) <= 150):
            komunikowanieBledu(minUdzialPowierzchniBiologicznieCzynnej,'Minimalny udział powierzchni biologicznie czynnej wyznaczony dla strefy planistycznej musi być równy lub większy od 30% i nie może przekroczyć 150%. \
    Wartość atrybutu wyrażona jest w % z dokładnością do pierwszego miejsca po przecinku. \
    Udział musi być podany dla: ' + nazwa.currentText(),'minUdzialPowierzchniBiologicznieCzynnej')
        elif symbol.currentText() in ['SP','SI'] and (txt == '' or not 20 <= float(txt) <= 150):
            komunikowanieBledu(minUdzialPowierzchniBiologicznieCzynnej,'Minimalny udział powierzchni biologicznie czynnej wyznaczony dla strefy planistycznej musi być równy lub większy od 20% i nie może przekroczyć 150%. \
    Wartość atrybutu wyrażona jest w % z dokładnością do pierwszego miejsca po przecinku. \
    Udział musi być podany dla: ' + nazwa.currentText(),'minUdzialPowierzchniBiologicznieCzynnej')
        elif symbol.currentText() in ['SN'] and (txt == '' or not 50 <= float(txt) <= 150):
            komunikowanieBledu(minUdzialPowierzchniBiologicznieCzynnej,'Minimalny udział powierzchni biologicznie czynnej wyznaczony dla strefy planistycznej musi być równy lub większy od 50% i nie może przekroczyć 150%. \
    Wartość atrybutu wyrażona jest w % z dokładnością do pierwszego miejsca po przecinku. \
    Udział musi być podany dla: ' + nazwa.currentText(),'minUdzialPowierzchniBiologicznieCzynnej')
        else:
            komunikowanieBledu(minUdzialPowierzchniBiologicznieCzynnej,'','minUdzialPowierzchniBiologicznieCzynnej')
        minUdzialPowierzchniBiologicznieCzynnej.setPlaceholderText(placeHolders['minUdzialPowierzchniBiologicznieCzynnej'])
        
        if not symbol.currentText() in ['SG','SO','SK','wybierz']:
            minUdzialPowierzchniBiologicznieCzynnej_label.setText("minimalny udział powierzchni biologicznie czynnej*")
        else:
            minUdzialPowierzchniBiologicznieCzynnej_label.setText("minimalny udział powierzchni biologicznie czynnej")
    except:
        pass


def wlaczenieWylaczenieProfiliDoEdycji():
    try:
        if not warstwa.isEditable():
            czyWarstwaWEdycji = False
        else:
            czyWarstwaWEdycji = True
        profilPodstawowy_QCCB.setEnabled(czyWarstwaWEdycji)
        profilDodatkowy_QCCB.setEnabled(czyWarstwaWEdycji)
    except:
        pass


def czyWartoscAtrybutuJestUnikalna(atrybut, wartosc):
    request = QgsFeatureRequest(QgsExpression(atrybut + "='" + wartosc + "'"))
    wartoscAtrybutuJestUnikalna = True
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