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
from PyQt5.QtCore import QDateTime, QDate, QTime


def my_form_open(dialog, layer, feature):
    global atrybuty, geometria, obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
    global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
    global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
    global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
    global czyObiektZmieniony, czyWersjaZmieniona
    
    atrybuty = feature.attributes()
    geometria = feature.geometry()
    obj = feature
    dlg = dialog
    if dlg.parent() == None:
        return
    try:
        dlg.parent().setWindowTitle("Atrybuty OUZ, nazwa warstwy: " + layer.name())
        dlg.parent().setMaximumWidth(413)
        dlg.parent().setMaximumHeight(380)
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
                    'lokalnyId':'np. 1OUZ',
                    'oznaczenie':'np. 1OUZ',
                    'koniecWersjiObiektu':'np. 2023-01-31T12:34:58'
                    }
    
    pomoc = ['Przestrzeń nazw identyfikująca w sposób jednoznaczny źródło danych obiektu, o której mowa w § 5 ust. 1 pkt 1 rozporządzenia. KOMENTARZ 01. Wartość atrybutu przestrzeń nazw powinna jednoznacznie identyfikować zbiór danych przestrzennych, do którego należy instancja typu obiektu',
             'Lokalny identyfikator obiektu, o którym mowa w § 5 ust. 1 pkt 2 rozporządzenia,  przypisany przez dostawcę danych. KOMENTARZ 01. Unikalność identyfikatora w przestrzeni nazw gwarantuje dostawca zbioru danych przestrzennych',
             'Identyfikator poszczególnej wersji obiektu przestrzennego, o którym mowa w § 5 ust. 1 pkt 3 rozporządzenia, przypisany przez dostawcę danych. KOMENTARZ 01. W zestawie wszystkich wersji danego obiektu identyfikator wersji musi być unikalny',
             'Nazwa urzędowa regulacji dodatkowej',
             'Oznaczenia literowe lub literowo-liczbowe Regulacji umożliwiające jednoznaczne powiązanie obiektu z tekstem aktu planowania przestrzennego',
             'Symbol literowy lub literowo-liczbowy stosowany do wyświetlania identyfikacji o rodzaju Regulacji',
             'Charakter prawny regulacji w zakresie zagospodarowania przestrzennego',
             'Data, od której dana wersja aktu planowania przestrzennego obowiązuje',
             'Data, od której dana wersja aktu planowania przestrzennego przestała obowiązywać',
             'Ogólne wskazanie etapu procesu planowania, na którym znajduje się akt planowania przestrzennego',
             'Data i godzina, w której ta wersja obiektu została wprowadzona do zbioru danych przestrzennych lub zmieniona w tym zbiorze danych przestrzennych',
             'Data i godzina, w której ta wersja obiektu została zastąpiona w zbiorze danych przestrzennych lub wycofana z tego zbioru danych przestrzennych',
             'Odniesienie do aktu planowania przestrzennego, w ramach którego wyznaczone jest dane wydzielenie planistyczne']
    
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
    przestrzenNazw.setPlaceholderText(placeHolders['przestrzenNazw'])
    przestrzenNazw.textChanged.connect(przestrzenNazw_kontrola)
    
    lokalnyId = dialog.findChild(QLineEdit,"lokalnyId")
    lokalnyId.setPlaceholderText(placeHolders['lokalnyId'])
    lokalnyId.textChanged.connect(lokalnyId_kontrola)
    if obj.id() <0: lokalnyId_kontrola('')
    
    nazwa = dialog.findChild(QLineEdit,"nazwa")
    nazwa.setText('Obszar uzupełnienia zabudowy')
     
    oznaczenie = dialog.findChild(QLineEdit,"oznaczenie")
    oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
    oznaczenie.textChanged.connect(oznaczenie_kontrola)
    if oznaczenie.text() == 'NULL' or oznaczenie.text() == None:
        oznaczenie.setText('')
    else:
        oznaczenie_kontrola(oznaczenie.text())
    
    symbol = dialog.findChild(QLineEdit,"symbol")
    symbol.setText('OUZ')
    
    charakterUstalenia = dialog.findChild(QComboBox,"charakterUstalenia")
    charakterUstalenia.currentTextChanged.connect(charakterUstalenia_kontrola)
    charakterUstalenia_kontrola(charakterUstalenia.currentText())
    if obj.id() < 0: charakterUstalenia.setCurrentIndex(0)
    
    obowiazujeOd = dialog.findChild(QDateTimeEdit,"obowiazujeOd")
    obowiazujeOd_label = dialog.findChild(QLabel,"obowiazujeOd_label")
    obowiazujeOd.setMaximumDate(QDate.currentDate())
    obowiazujeOd.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    obowiazujeDo = dialog.findChild(QDateTimeEdit,"obowiazujeDo")
    obowiazujeDo_label = dialog.findChild(QLabel,"obowiazujeDo_label")
    obowiazujeDo.setMaximumDate(QDate.currentDate())
    obowiazujeDo.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    status = dialog.findChild(QComboBox,"status")
    status.currentTextChanged.connect(status_kontrola)
    if obj.id() < 0 and atrybutyPOG != None:
        status.setCurrentText(atrybutyPOG['status'])
    status_kontrola(status.currentText())
    
    koniecWersjiObiektu = dialog.findChild(QDateTimeEdit,"koniecWersjiObiektu")
    koniecWersjiObiektu.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    koniecWersjiObiektu.setMaximumDate(QDate.currentDate())
    
    geometria_kontrola()
    poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    czyWersjaZmieniona = False
    
    zapisz = dialog.findChild(QPushButton,"zapisz")
    zapisz.clicked.connect(zapis)
    zapisz.setEnabled(False)
    zapisz.setText("Zapisz")
    
    if obj.id() < 0: przestrzenNazw_kontrola()
    
    labels = [None for i in range(12)]
    pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
    for i in range(12):
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
                komunikowanieBledu(oznaczenie,'Należy wpisać liczbę naturalną i symbol','oznaczenie')
            else:
                lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
                komunikowanieBledu(oznaczenie,'','oznaczenie')
        if not czyWartoscAtrybutuJestUnikalna('oznaczenie',txt):
            komunikowanieBledu(oznaczenie,'Oznaczenie nie jest unikalne w ramach warstwy.','oznaczenie')
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
            obowiazujeOd_kontrola(obowiazujeOd.dateTime())
            obowiazujeDo_kontrola(obowiazujeDo.dateTime())
    except:
        pass


def poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola():
    try:
        obowiazujeOdTxt = obowiazujeOd.dateTime().toString("H:mm")
        obowiazujeDoTxt = obowiazujeDo.dateTime().toString("H:mm")
        poczatekWersjiObiektuTxt = poczatekWersjiObiektu.dateTime().toString("H:mm")
        koniecWersjiObiektuTxt = koniecWersjiObiektu.dateTime().toString("H:mm")
        
        if obowiazujeOdTxt not in ['0:00','23:59']:
            komunikowanieBledu(obowiazujeOd, 'Należy wybrać datę dla obowiązuje od', 'obowiazujeOd')
        else:
            if obowiazujeDoTxt in ['0:00','23:59'] and obowiazujeOd.dateTime() >= obowiazujeDo.dateTime():
                komunikowanieBledu(obowiazujeOd, 'Atrybut obowiązuje od nie może być większy lub równy od obowiązuje do.', 'obowiazujeOd')
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
                    komunikowanieBledu(obowiazujeDo, 'Należy wybrać datę dla obowiązuje do', 'obowiazujeDo')
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
                        komunikowanieBledu(obowiazujeOd, 'Atrybut obowiązuje od nie może być większy lub równy od obowiązuje do.', 'obowiazujeOd')
                        komunikowanieBledu(obowiazujeDo, 'Atrybut obowiązuje do nie może być mniejszy lub równy od obowiązuje od.','obowiazujeDo')
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