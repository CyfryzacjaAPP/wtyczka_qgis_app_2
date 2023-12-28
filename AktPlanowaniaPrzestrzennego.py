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
from PyQt5.QtCore import QDateTime, QDate, QTime


def my_form_open(dialog, layer, feature):
    global atrybuty, geometria, obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy, tytulAlternatywny_QLE
    global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, listaTytulowAlternatywnych
    global status, obowiazujeOd, obowiazujeDo, tytul, tytulAlternatywny, typPlanu, poziomHierarchii, tytulyAlternatywne, dodaj, usun
    global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP, obowiazujeOd_label, obowiazujeDo_label
    global czyObiektZmieniony, modyfikacja, czyWersjaZmieniona
    
    atrybuty = feature.attributes()
    geometria = feature.geometry()
    obj = feature
    dlg = dialog
    if dlg.parent() == None:
        return
    try:
        dlg.parent().setWindowTitle("Atrybuty POG, nazwa warstwy: " + layer.name())
        dlg.parent().setMaximumWidth(520)
        dlg.parent().setMaximumHeight(520)
    except:
        pass
    
    warstwa = layer
    warstwa.geometryOptions().setGeometryPrecision(0.01)
    warstwa.startEditing()
    qgis.utils.iface.setActiveLayer(warstwa)
    
    mainPath = Path(QgsApplication.qgisSettingsDirPath())/Path("python/plugins/wtyczka_qgis_app/")
    teryt_gminy = ''
    dataCzasTeraz = datetime.now()
    
    s = QgsSettings()
    rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
    numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
    jpt = s.value("qgis_app2/settings/jpt", "")
    idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
    
    placeHolders = {'przestrzenNazw':'np. PL.ZIPPZP.2393/246601-POG',
                    'lokalnyId':'np. 1POG',
                    'tytul':'np. Plan ogólny gminy …',
                    'tytulAlternatywny':'np. POG nazwa gminy'
                    }
    
    pomoc = ['Przestrzeń nazw identyfikująca w sposób jednoznaczny źródło danych obiektu, o której mowa w § 5 ust. 1 pkt 1 rozporządzenia.\nWartość atrybutu przestrzeń nazw powinna jednoznacznie identyfikować zbiór danych przestrzennych, do którego należy instancja typu obiektu.',
             'Identyfikator lokalny obiektu, o którym mowa w § 5 ust. 1 pkt 2 oraz § 5 ust. 1a rozporządzenia, przypisany przez dostawcę danych.\nUnikalność identyfikatora w przestrzeni nazw gwarantuje dostawca zbioru danych przestrzennych.',
             'Identyfikator poszczególnej wersji obiektu przestrzennego, o którym mowa w § 5 ust. 1 pkt 3 rozporządzenia, przypisany przez dostawcę danych.\nW zestawie wszystkich wersji danego obiektu identyfikator wersji jest unikalny.',
             'Data i godzina, w której wersja obiektu została wprowadzona do zbioru danych przestrzennych lub zmieniona w tym zbiorze danych przestrzennych.',
             'Data i godzina, w której wersja obiektu została zastąpiona w zbiorze danych przestrzennych lub wycofana z tego zbioru danych przestrzennych.',
             'Oficjalny tytuł aktu planowania przestrzennego lub jego projektu.',
             'Alternatywny (nieoficjalny) tytuł aktu planowania przestrzennego lub jego projektu.',
             'Formalna nazwa typu aktu planowania przestrzennego lub jego projektu.',
             'Poziom aktu planowania przestrzennego w hierarchii terytorialnej. \n Dla poszczególnych typów aktu planowania przestrzennego atrybut przyjmuje następujące wartości: \n 1)	Plan zagospodarowania przestrzennego województwa – regionalny; \n 2)	Plan ogólny gminy – lokalny; \n 3)	Miejscowy plan zagospodarowania przestrzennego – sublokalny; \n 4)	Zintegrowany plan inwestycyjny – sublokalny; \n 5)	Miejscowy plan odbudowy – sublokalny; \n 6)	Miejscowy plan rewitalizacji – sublokalny',
             'Data, od której dana wersja obiektu przestrzennego obowiązuje.',
             'Data, do której dana wersja obiektu przestrzennego obowiązywała.',
             'Ogólne wskazanie etapu procesu planowania, na którym znajduje się wersja aktu planowania przestrzennego lub jego projektu.',
             'Informacja, czy dana wersja aktu planowania przestrzennego obowiązuje w części – nie obejmuje całego obszaru, który jest objęty aktem planowania przestrzennego lub jego projektem (np. w wyniku uchylenia, unieważnienia).']
    
    atrybuty.append('geometria')
    listaBledowAtrybutow = [0 for i in range(len(atrybuty))]
    listaTytulowAlternatywnych = []
    
    wersjaId = dialog.findChild(QDateTimeEdit,"wersjaId")
    wersjaId.dateTimeChanged.connect(wersjaId_kontrola)
    if obj.id() < 0: wersjaId.setDateTime(dataCzasTeraz)
    
    przestrzenNazw = dialog.findChild(QLineEdit,"przestrzenNazw")
    przestrzenNazw.setToolTip('')
    przestrzenNazw.setPlaceholderText(placeHolders['przestrzenNazw'])
    przestrzenNazw.textChanged.connect(przestrzenNazw_kontrola)
    
    lokalnyId = dialog.findChild(QLineEdit,"lokalnyId")
    lokalnyId.setToolTip('')
    lokalnyId.setPlaceholderText(placeHolders['lokalnyId'])
    lokalnyId.textChanged.connect(lokalnyId_kontrola)
    if lokalnyId.text() == 'NULL': lokalnyId.setText(idLokalnyAPP)
    
    obowiazujeOd = dialog.findChild(QDateTimeEdit,"obowiazujeOd")
    obowiazujeOd_label = dialog.findChild(QLabel,"obowiazujeOd_label")
    obowiazujeOd.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    obowiazujeDo = dialog.findChild(QDateTimeEdit,"obowiazujeDo")
    obowiazujeDo_label = dialog.findChild(QLabel,"obowiazujeDo_label")
    obowiazujeDo.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    
    modyfikacja = dialog.findChild(QCheckBox,"modyfikacja")
    modyfikacja.stateChanged.connect(modyfikacja_kontrola)
    
    status = dialog.findChild(QComboBox,"status")
    status.currentTextChanged.connect(status_kontrola)
    if obj.id() < 0: status_kontrola(status.currentText())
    
    poczatekWersjiObiektu = dialog.findChild(QDateTimeEdit,"poczatekWersjiObiektu")
    poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)
    if obj.id() < 0: poczatekWersjiObiektu.setDateTime(dataCzasTeraz)
    
    koniecWersjiObiektu = dialog.findChild(QDateTimeEdit,"koniecWersjiObiektu")
    koniecWersjiObiektu.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
    koniecWersjiObiektu.setMaximumDate(QDate.currentDate())
    
    tytul = dialog.findChild(QLineEdit,"tytul")
    tytul.setPlaceholderText(placeHolders['tytul'])
    tytul.textChanged.connect(tytul_kontrola)
    if obj.id() < 0: tytul.setText('Plan ogólny gminy ')
    tytul_kontrola(tytul.text())
    
    tytulAlternatywny = dialog.findChild(QLineEdit,"tytulAlternatywny")
    tytulAlternatywny_QLE = dialog.findChild(QLineEdit,"tytulAlternatywny_QLE")
    tytulAlternatywny_QLE.setPlaceholderText(placeHolders['tytulAlternatywny'])
    if tytulAlternatywny_QLE.text() == 'NULL': tytulAlternatywny_QLE.setText('')
    
    try:
        tytulyAlternatywne = dialog.findChild(QListWidget,"tytulyAlternatywne")
        read_tytulAlternatywny()
        tytulyAlternatywne.itemClicked.connect(zaznacz_tytulyAlternatywne)
    except:
        pass
    
    dodaj = dialog.findChild(QPushButton,"dodaj")
    dodaj.clicked.connect(dodaj_tytulAlternatywny)
    
    usun = dialog.findChild(QPushButton,"usun")
    usun.clicked.connect(usun_tytulAlternatywny)
    
    geometria_kontrola()
    poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    czyWersjaZmieniona = False
    
    zapisz = dialog.findChild(QPushButton,"zapisz")
    zapisz.clicked.connect(zapis)
    zapisz.setEnabled(False)
    zapisz.setText("Zapisz")
    
    przestrzenNazw_kontrola()
    
    labels = [None for i in range(13)]
    pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
    for i in range(13):
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
        
        for obiekty_bliskie in warstwa.getFeatures(geometria.boundingBox()): # wybiera obiekty w zasiegu opracowywanego obiektu
            if geometria.intersects(obiekty_bliskie.geometry()) == True and \
                not geometria.touches(obiekty_bliskie.geometry()) == True and \
                (obj.id() != obiekty_bliskie.id() and (obiekty_bliskie.id() >= 0 or obiekty_bliskie.id()< -100000)):
                msg = 'Obiekty wewnątrz warstwy przecinają się.'
                listaBledowAtrybutow[obj.fieldNameIndex('geometria')] = 1
                dlg.displayWarning(msg)
                break
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


def lokalnyId_kontrola():
    try:
        if lokalnyId.text() == '':
            komunikowanieBledu(lokalnyId,'Identyfikator lokalny jest obligatoryjny.','lokalnyId')
        elif idLokalnyAPP == '':
            lokalnyId.setPlaceholderText(placeHolders['lokalnyId'])
            komunikowanieBledu(lokalnyId,'Proszę w ustawieniach wpisać identyfikator lokalny identyfikujący jednoznacznie i unikalnie akt planowania przestrzennego w zbiorze danych przestrzennych i zapisać.','lokalnyId')
        else:
            lokalnyId.setText(idLokalnyAPP)
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


def tytul_kontrola(txt):
    try:
        if re.match('^Plan ogólny gminy [A-Z,a-z,ĄŚĘŁÓŻŹĆŃąśęłóżźćń ()-]{2,}$', txt) == None:
            tytul.setPlaceholderText(placeHolders['tytul'])
            komunikowanieBledu(tytul,'Tytuł jest polem obowiązkowym i musi zaczynać się od Plan ogólny gminy','tytul')
        else:
            komunikowanieBledu(tytul,'','tytul')
    except:
        pass


def dodaj_tytulAlternatywny():
    try:
        global listaTytulowAlternatywnych
        if listaTytulowAlternatywnych == ['NULL']:
            listaTytulowAlternatywnych = []
        txt = tytulAlternatywny_QLE.text()
        if txt != '' and txt != 'NULL' and txt not in listaTytulowAlternatywnych:
            tytulyAlternatywne.addItem(txt)
            listaTytulowAlternatywnych.append(txt)
            tytulAlternatywny.setText(','.join(listaTytulowAlternatywnych))
            komunikowanieBledu(tytulAlternatywny,'','tytulAlternatywny')
            tytulAlternatywny_QLE.setText('')
    except:
        pass


def usun_tytulAlternatywny():
    try:
        global listaTytulowAlternatywnych
        nr = tytulyAlternatywne.currentRow()
        if nr != -1:
            tytulyAlternatywne.takeItem(nr)
            listaTytulowAlternatywnych.pop(nr)
            tytulAlternatywny.setText(','.join(listaTytulowAlternatywnych))
            komunikowanieBledu(tytulAlternatywny,'','tytulAlternatywny')
    except:
        pass


def read_tytulAlternatywny():
    try:
        global listaTytulowAlternatywnych
        lista = tytulAlternatywny.text()
        listaTytulowAlternatywnych = lista.split(",")
        tytulyAlternatywne.clear()
        for item in listaTytulowAlternatywnych:
            if item != 'NULL':
                tytulyAlternatywne.addItem(item)
    except:
        pass


def modyfikacja_kontrola():
    try:
        komunikowanieBledu(modyfikacja,'','modyfikacja')
        if modyfikacja.checkState() == 2 and tytul.text() != '':
            tytul.setText('')
        else:
            tytul.setText('Plan ogólny gminy ')
    except:
        pass