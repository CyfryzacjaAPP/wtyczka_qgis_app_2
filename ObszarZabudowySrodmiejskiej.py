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
from PyQt5.QtCore import QDateTime, QDate, QTime
import ctypes
from qgis.utils import iface


def my_form_open(dialog, layer, feature):
    try:
        global obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        global czyObiektZmieniony, czyWersjaZmieniona
        global kontrolaAtrybutu
        
        atrybuty = feature.attributes()
        geometria = feature.geometry()
        obj = feature
        dlg = dialog
        if dlg.parent() == None:
            return
        
        dlg.parent().setWindowTitle("Atrybuty OZS, nazwa warstwy: " + layer.name())
        dlg.parent().setMaximumWidth(423)
        dlg.parent().setMaximumHeight(380)
        
        warstwa = layer
        warstwa.geometryOptions().setGeometryPrecision(0.01)
        warstwa.startEditing()
        qgis.utils.iface.setActiveLayer(warstwa)
        
        mainPath = Path(QgsApplication.qgisSettingsDirPath())/Path("python/plugins/wtyczka_qgis_app/")
        teryt_gminy = ''
        dataCzasTeraz = datetime.now(timezone.utc)
        
        if warstwa.fields().indexFromName('edycja') == -1:
            warstwa.addAttribute(QgsField('edycja', QVariant.Bool, ''))
            warstwa.updateFields()
            warstwa.commitChanges(False)
            warstwa.startEditing()
        
        kontrolaAtrybutu = {'oznaczenie':2,
                            'obowiazujeOd':2,
                            'obowiazujeDo':2}
        
        s = QgsSettings()
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
        numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
        jpt = s.value("qgis_app2/settings/jpt", "")
        idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
        
        placeHolders = {'przestrzenNazw':'np. PL.ZIPPZP.2393/246601-POG',
                        'lokalnyId':'np. 1OZS',
                        'oznaczenie':'np. 1OZS',
                        'symbol':'np. OZS'
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
                 'Data i godzina, w której ta wersja obiektu została wprowadzona do zbioru danych przestrzennych\n lub zmieniona w tym zbiorze danych przestrzennych.',
                 'Data i godzina, w której wersja obiektu została zastąpiona w zbiorze danych przestrzennych\n lub wycofana z tego zbioru danych przestrzennych.',
                 'Odniesienie do aktu planowania przestrzennego, w ramach którego wyznaczone jest dane wydzielenie planistyczne.']
        
        atrybuty.append('geometria')
        listaBledowAtrybutow = [0 for i in range(len(atrybuty))]
        
        atrybutyPOG = odczytajAtrybutyZPOG()
        
        wersjaId = dialog.findChild(QDateTimeEdit,"wersjaId")
        wersjaId.dateTimeChanged.connect(wersjaId_kontrola)
        if obj.id() < 0: wersjaId.setDateTime(dataCzasTeraz)
        
        poczatekWersjiObiektu = dialog.findChild(QDateTimeEdit,"poczatekWersjiObiektu")
        poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)
        poczatekWersjiObiektu.setMaximumDate(QDate.currentDate())
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
        nazwa.setText('Obszar zabudowy śródmiejskiej')
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
        
        geometria_kontrola()
        poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
        czyWersjaZmieniona = False
        
        zapisz = dialog.findChild(QPushButton,"zapisz")
        zapisz.clicked.connect(zapis)
        zapisz.setEnabled(False)
        zapisz.setText("Zapisz")
        
        przestrzenNazw_kontrola()
        
        labels = [None for i in range(12)]
        pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
        for i in range(12):
            labels[i] = dialog.findChild(QLabel,"label_" + str(i + 1))
            labels[i].setPixmap(pixmap)
            labels[i].setToolTip(pomoc[i])
        
        operacjeNaAtrybucie('oznaczenie')
        operacjeNaAtrybucie('status')
        operacjeNaAtrybucie('obowiazujeOd')
        operacjeNaAtrybucie('obowiazujeDo')
        operacjeNaAtrybucie('koniecWersjiObiektu')
        
        dlg.parent().rejected.connect(dialogRejected)
    except:
        pass


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
        obj.setAttribute(warstwa.fields().indexFromName('edycja'),True)
        warstwa.updateFeature(obj)
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
            if (txt == '' or re.match('^[1-9][0-9]{0,4}' + symbol.text() + '$', txt) == None) and kontrolaAtrybutu['oznaczenie'] == 2:
                oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
                komunikowanieBledu(oznaczenie,'Należy wpisać liczbę naturalną. Symbol jest dodawany automatycznie.','oznaczenie')
            else:
                lokalnyId.setText(idLokalnyAPP + "-" + oznaczenie.text())
                komunikowanieBledu(oznaczenie,'','oznaczenie')
                oznaczenie.setPlaceholderText(placeHolders['oznaczenie'])
        if not czyWartoscAtrybutuJestUnikalna('oznaczenie',txt) and kontrolaAtrybutu['oznaczenie'] == 2:
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
        
        if obowiazujeOdTxt not in ['0:00','23:59'] and kontrolaAtrybutu['obowiazujeOd'] == 2:
            komunikowanieBledu(obowiazujeOd, 'Należy wybrać datę dla "obowiązuje od"', 'obowiazujeOd')
        else:
            if obowiazujeDoTxt in ['0:00','23:59'] and obowiazujeOd.dateTime() >= obowiazujeDo.dateTime() and kontrolaAtrybutu['obowiazujeOd'] == 2:
                komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
            else:
                komunikowanieBledu(obowiazujeOd, '', 'obowiazujeOd')
                if czyObiektZmieniony:
                    uspojnienieDatyObowiazujeOd()
        if koniecWersjiObiektuTxt in ['0:00','23:59'] and koniecWersjiObiektu.dateTime().date().year() != 1 and poczatekWersjiObiektu.dateTime() >= koniecWersjiObiektu.dateTime():
            komunikowanieBledu(poczatekWersjiObiektu,'Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu','poczatekWersjiObiektu')
            komunikowanieBledu(koniecWersjiObiektu,'Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu','koniecWersjiObiektu')
        else:
            komunikowanieBledu(poczatekWersjiObiektu,'','poczatekWersjiObiektu')
            komunikowanieBledu(koniecWersjiObiektu,'','koniecWersjiObiektu')
            if koniecWersjiObiektu.dateTime().date().year() != 1 and koniecWersjiObiektu.dateTime().time().msec() == 0 or status.currentText() == 'nieaktualny':
                obowiazujeDo_label.setText("obowiązuje do*")
                if obowiazujeDoTxt not in ['0:00','23:59'] and kontrolaAtrybutu['obowiazujeDo'] == 2:
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


def operacjeNaAtrybucie(nazwaAtrybutu):
    global operacja
    operacje = ['włączona kontrola wypełnienia','hurtowa zmiana atrybutu w ramach wszystkich warstw','hurtowa zmiana atrybutu w ramach warstwy','uspójnienie daty dla obiektów nowych lub zmienionych']
    atrybutOperacje = {'oznaczenie':[0],
                       'status':[1,2],
                       'obowiazujeOd':[0,1,2,3],
                       'obowiazujeDo':[0,1,2],
                       'koniecWersjiObiektu':[1,2]
                       }
    atrybutLayout = {'oznaczenie':"gridLayout",
                     'status':"gridLayout",
                     'obowiazujeOd':"gridLayout",
                     'obowiazujeDo':"gridLayout",
                     'koniecWersjiObiektu':"gridLayout"}
    atrybutRowCol = {'oznaczenie':[2,3],
                     'status':[3,3],
                     'obowiazujeOd':[4,3],
                     'obowiazujeDo':[5,3],
                     'koniecWersjiObiektu':[14,3]}
    atrybutKontrola = {'oznaczenie':"oznaczenie_kontrola",
                       'obowiazujeOd':"poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola",
                       'obowiazujeDo':"poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola"}
    atrybutOperacje_tmp = []
    for x in atrybutOperacje[nazwaAtrybutu]:
        atrybutOperacje_tmp.append(operacje[x])
    
    qWidget = QWidget()
    wyborAkcji = QgsCheckableComboBox(qWidget)
    wyborAkcji.setMaximumWidth(18)
    wyborAkcji.view().setMinimumWidth(430)
    wyborAkcji.setStyleSheet("QComboBox::down-arrow{background-image :;}")
    gridLayout = dlg.findChild(QGridLayout,atrybutLayout[nazwaAtrybutu])
    gridLayout.addWidget(wyborAkcji,atrybutRowCol[nazwaAtrybutu][0],atrybutRowCol[nazwaAtrybutu][1])
    wyborAkcji.addItems(atrybutOperacje_tmp)
    if 0 in atrybutOperacje[nazwaAtrybutu]:
        wyborAkcji.setItemCheckState(0, kontrolaAtrybutu[nazwaAtrybutu])
    operacja = {'oznaczenie':['włączona kontrola wypełnienia'],
                'status':[],
                'obowiazujeOd':['włączona kontrola wypełnienia'],
                'obowiazujeDo':['włączona kontrola wypełnienia'],
                'koniecWersjiObiektu':[]}
    
    def wlaczenieLubWylaczenieKontroli(txt):
        global kontrolaAtrybutu
        if 'włączona kontrola wypełnienia' in txt:
            kontrolaAtrybutu[nazwaAtrybutu] = 2
        else:
            kontrolaAtrybutu[nazwaAtrybutu] = 0
        if atrybutKontrola[nazwaAtrybutu] == 'poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola':
            globals().get(atrybutKontrola[nazwaAtrybutu])()
        else:
            globals().get(atrybutKontrola[nazwaAtrybutu])(oznaczenie.text())
    
    def hurtowaZmianatArybutuWRamachWarstw():
        for obj in globals():
            if obj == nazwaAtrybutu:
                if isinstance(globals().get(obj), QComboBox):
                    atrybut = globals().get(obj).currentText()
                elif isinstance(globals().get(obj), QDateTimeEdit):
                    atrybut = globals().get(obj).dateTime()
                    if atrybut.time().msec() != 0 and atrybut.time().second() != 0:
                        atrybut = None
                break
        
        if nazwaAtrybutu == "status" and status.currentText() == 'wybierz':
            QMessageBox.warning(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach wszystkich warstw nie może być wykonana dla wybranej wartości atrybutu.'.format(nazwaAtrybutu))
            return
        
        odp = QMessageBox.question(None,'Operacje na danych',
                                     "Czy rozpocząć hurtową zmianę atrybutu {} w ramach wszystkich warstw?".format(nazwaAtrybutu), QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.No:
            return
        else:
            liczbaObiektowDoZmiany = 0
            for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                   warstwa.name().startswith('ObszarUzupelnieniaZabudowy') or \
                   warstwa.name().startswith('ObszarZabudowySrodmiejskiej') or \
                   warstwa.name().startswith('AktPlanowaniaPrzestrzennego') or \
                   warstwa.name().startswith('StrefaPlanistyczna'):
                       liczbaObiektowDoZmiany += warstwa.featureCount()
            
            if liczbaObiektowDoZmiany > 0:
                progressMessageBar = iface.messageBar().createMessage("Postęp wykonania hurtowej zmiany atrybut {} w ramach wszystkich warstw.".format(nazwaAtrybutu))
                progress = QProgressBar()
                progress.setMaximum(liczbaObiektowDoZmiany)
                progressMessageBar.layout().addWidget(progress)
                iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
                y = 0
                dataCzasTeraz = datetime.now(timezone.utc)
                for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                    if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                       warstwa.name().startswith('ObszarUzupelnieniaZabudowy') or \
                       warstwa.name().startswith('ObszarZabudowySrodmiejskiej') or \
                       warstwa.name().startswith('AktPlanowaniaPrzestrzennego') or \
                       warstwa.name().startswith('StrefaPlanistyczna'):
                        warstwa.startEditing()
                        idx_Atrybut = warstwa.fields().indexFromName(nazwaAtrybutu)
                        idx_edycja = warstwa.fields().indexFromName('edycja')
                        idx_wersjaId = warstwa.fields().indexFromName('wersjaId')
                        idx_poczatekWersjiObiektu = warstwa.fields().indexFromName('poczatekWersjiObiektu')
                        for feature in warstwa.getFeatures():
                            feature.setAttribute(idx_Atrybut, atrybut)
                            feature.setAttribute(idx_edycja, True)
                            feature.setAttribute(idx_wersjaId, dataCzasTeraz.strftime("%Y%m%dT%H%M%S"))
                            feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz.isoformat())
                            warstwa.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        warstwa.commitChanges()
                        warstwa.startEditing()
                progressMessageBar.dismiss()
            dlg.changeAttribute(nazwaAtrybutu, atrybut)
            QMessageBox.information(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach wszystkich warstw została zakończona.'.format(nazwaAtrybutu))
    
    def hurtowaZmianatArybutuWRamachWarstwy():
        for obj in globals():
            if obj == nazwaAtrybutu:
                if isinstance(globals().get(obj), QComboBox):
                    atrybut = globals().get(obj).currentText()
                elif isinstance(globals().get(obj), QDateTimeEdit):
                    atrybut = globals().get(obj).dateTime()
                    if atrybut.time().msec() != 0 and atrybut.time().second() != 0:
                        atrybut = None
                break
        
        if nazwaAtrybutu == "status" and status.currentText() == 'wybierz':
            QMessageBox.warning(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach warstwy nie może być wykonana dla wybranej wartości atrybutu.'.format(nazwaAtrybutu))
            return
        
        odp = QMessageBox.question(None,'Operacje na danych',
                                     "Czy rozpocząć hurtową zmianę atrybutu {} w ramach warstwy?".format(nazwaAtrybutu), QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.No:
            return
        else:
            liczbaObiektowDoZmiany = 0
            for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                if warstwa.name().startswith('ObszarZabudowySrodmiejskiej'):
                    liczbaObiektowDoZmiany += warstwa.featureCount()
            
            if liczbaObiektowDoZmiany > 0:
                progressMessageBar = iface.messageBar().createMessage("Postęp wykonania hurtowej zmiany atrybut {} w ramach warstwy.".format(nazwaAtrybutu))
                progress = QProgressBar()
                progress.setMaximum(liczbaObiektowDoZmiany)
                progressMessageBar.layout().addWidget(progress)
                iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
                y = 0
                dataCzasTeraz = datetime.now(timezone.utc)
                for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                    if warstwa.name().startswith('ObszarZabudowySrodmiejskiej'):
                        warstwa.startEditing()
                        for feature in warstwa.getFeatures():
                            feature.setAttribute(idx_Atrybut, atrybut)
                            feature.setAttribute(idx_edycja, True)
                            feature.setAttribute(idx_wersjaId, dataCzasTeraz.strftime("%Y%m%dT%H%M%S"))
                            feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz.isoformat())
                            warstwa.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        warstwa.commitChanges()
                        warstwa.startEditing()
                        break
                progressMessageBar.dismiss()
            dlg.changeAttribute(nazwaAtrybutu, atrybut)
            QMessageBox.information(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach warstwy została zakończona.'.format(nazwaAtrybutu))
    
    def uspojnienieDatyObowiazujeOd():
        odp = QMessageBox.question(None,'Operacje na danych',
                                   'Czy uspójnić datę "obowiązuje od" dla obiektów nowych lub zmienionych w ramach wszystkich warstw?', QMessageBox.Yes |
                                   QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.No:
            return
        else:
            liczbaObiektowDoZmiany = 0
            for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                   warstwa.name().startswith('ObszarUzupelnieniaZabudowy') or \
                   warstwa.name().startswith('ObszarZabudowySrodmiejskiej') or \
                   warstwa.name().startswith('AktPlanowaniaPrzestrzennego') or \
                   warstwa.name().startswith('StrefaPlanistyczna'):
                       for obj in warstwa.getFeatures():
                           if obj['edycja']:
                               liczbaObiektowDoZmiany += 1
            
            if liczbaObiektowDoZmiany > 1:
                progressMessageBar = iface.messageBar().createMessage('Postęp wykonania uspójnienia daty "obowiązuje od" w ramach wszystkich warstw.')
                progress = QProgressBar()
                progress.setMaximum(liczbaObiektowDoZmiany)
                progressMessageBar.layout().addWidget(progress)
                iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
                y = 0
                dataCzasTeraz = datetime.now(timezone.utc)
                for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                    if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                       warstwa.name().startswith('ObszarUzupelnieniaZabudowy') or \
                       warstwa.name().startswith('ObszarZabudowySrodmiejskiej') or \
                       warstwa.name().startswith('AktPlanowaniaPrzestrzennego') or \
                       warstwa.name().startswith('StrefaPlanistyczna'):
                        warstwa.startEditing()
                        idx_obowiazujeOd = warstwa.fields().indexFromName('obowiazujeOd')
                        idx_wersjaId = warstwa.fields().indexFromName('wersjaId')
                        idx_poczatekWersjiObiektu = warstwa.fields().indexFromName('poczatekWersjiObiektu')
                        for feature in warstwa.getFeatures():
                            if feature['edycja']:
                                feature.setAttribute(idx_obowiazujeOd, obowiazujeOd.dateTime())
                                feature.setAttribute(idx_wersjaId, dataCzasTeraz.strftime("%Y%m%dT%H%M%S"))
                                feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz.isoformat())
                            warstwa.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        warstwa.commitChanges()
                        warstwa.startEditing()
                progressMessageBar.dismiss()
            dlg.changeAttribute('obowiazujeOd', obowiazujeOd.dateTime())
            QMessageBox.information(None,'Informacja','Uspójnienie daty "obowiązuje od" w ramach wszystkich warstw zostało zakończone.')
    
    def wskazanieNaOperacje(txt):
        global operacja
        if len(txt) > len(operacja[nazwaAtrybutu]):
            difference = list(set(txt) - set(operacja[nazwaAtrybutu]))
        elif len(txt) < len(operacja[nazwaAtrybutu]):
            difference = list(set(operacja[nazwaAtrybutu]) - set(txt))
        else:
            difference = operacja[nazwaAtrybutu]
        if difference[0] == 'włączona kontrola wypełnienia':
            wlaczenieLubWylaczenieKontroli(txt)
        elif difference[0] == 'hurtowa zmiana atrybutu w ramach wszystkich warstw' and txt != []:
            hurtowaZmianatArybutuWRamachWarstw()
            i = 0
            for x in atrybutOperacje[nazwaAtrybutu]:
                if operacje[x] == 'hurtowa zmiana atrybutu w ramach wszystkich warstw' and wyborAkcji.itemCheckState(i) == 2:
                    wyborAkcji.setItemCheckState(i, 0)
                    txt.remove('hurtowa zmiana atrybutu w ramach wszystkich warstw')
                i += 1
        elif difference[0] == 'hurtowa zmiana atrybutu w ramach warstwy' and txt != []:
            hurtowaZmianatArybutuWRamachWarstwy()
            i = 0
            for x in atrybutOperacje[nazwaAtrybutu]:
                if operacje[x] == 'hurtowa zmiana atrybutu w ramach warstwy' and wyborAkcji.itemCheckState(i) == 2:
                    wyborAkcji.setItemCheckState(i, 0)
                    txt.remove('hurtowa zmiana atrybutu w ramach warstwy')
                i += 1
        elif difference[0] == 'uspójnienie daty dla obiektów nowych lub zmienionych' and txt != []:
            uspojnienieDatyObowiazujeOd()
            i = 0
            for x in atrybutOperacje[nazwaAtrybutu]:
                if operacje[x] == 'uspójnienie daty dla obiektów nowych lub zmienionych' and wyborAkcji.itemCheckState(i) == 2:
                    wyborAkcji.setItemCheckState(i, 0)
                    txt.remove('uspójnienie daty dla obiektów nowych lub zmienionych')
                i += 1
        operacja[nazwaAtrybutu] = txt
    
    wyborAkcji.checkedItemsChanged.connect(wskazanieNaOperacje)


def dialogRejected():
    try:
        global obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        global czyObiektZmieniony, czyWersjaZmieniona, kontrolaAtrybutu
        
        del obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        del zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        del charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        del rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        del czyObiektZmieniony, czyWersjaZmieniona, kontrolaAtrybutu
    except:
        pass