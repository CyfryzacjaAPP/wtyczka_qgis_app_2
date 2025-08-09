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
from qgis.core import QgsProject, NULL, QgsSettings, QgsMessageLog
from PyQt5.QtCore import QDateTime, QDate, QTime, QRegExp
from qgis.utils import iface
import wtyczka_qgis_app.resources


def my_form_open(dialog, layer, feature):
    try:
        global obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        global wylaczenieZabudowyZagrodowej, odlegloscDoSzkolyPodstawowej, odlegloscDoObszarowZieleniPublicznej
        global powierzchniaLacznaObszarowZieleniPublicznej, odlegloscDoObszaruZieleniPublicznej, powierzchniaObszaruZieleniPublicznej
        global odlegloscDoPrzedszkola, odlegloscDoZlobka, odlegloscDoAmbulatoriumPOZ, odlegloscDoBiblioteki, odlegloscDoDomuKultury
        global odlegloscDoDomuPomocySpolecznej, odlegloscDoUrzadzonegoTerenuSportu, odlegloscDoPrzystanku, odlegloscDoPlacowkiPocztowej
        global odlegloscDoApteki, odlegloscDoPosterunkuPolicji, odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej
        global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        global tablicaZmian, czyZmianaJestDopuszczalna
        global kontrolaAtrybutu, kontrolaAtrybutu_CB, fid
        
        atrybuty = feature.attributes()
        geometria = feature.geometry()
        obj = feature
        fid = obj.id()
        dlg = dialog
        if not isinstance(dialog.parent(), QDialog) or dlg.parent() == None:
            return
        
        dlg.parent().setWindowTitle("Atrybuty OSD, nazwa warstwy: " + layer.name())
        dlg.parent().setMinimumWidth(750)
        dlg.parent().setMaximumWidth(800)
        dlg.parent().setMaximumHeight(590)
        
        warstwa = layer
        warstwa.startEditing()
        qgis.utils.iface.setActiveLayer(warstwa)
        
        mainPath = Path(QgsApplication.qgisSettingsDirPath())/Path("python/plugins/wtyczka_qgis_app/")
        teryt_gminy = ''
        czyZmianaJestDopuszczalna = False
        dataCzasTeraz = QDateTime.currentDateTimeUtc()
        kontrolaAtrybutu_CB = []
        
        if warstwa.fields().indexFromName('edycja') == -1:
            warstwa.addAttribute(QgsField('edycja', QVariant.Bool, ''))
            warstwa.updateFields()
            warstwa.commitChanges(False)
            warstwa.startEditing()
        
        kontrolaAtrybutu = {'oznaczenie':2,
                            'odlegloscDoSzkolyPodstawowej':2,
                            'odlegloscDoObszarowZieleniPublicznej':2,
                            'powierzchniaLacznaObszarowZieleniPublicznej':2,
                            'odlegloscDoObszaruZieleniPublicznej':2,
                            'powierzchniaObszaruZieleniPublicznej':2,
                            'obowiazujeOd':2,
                            'obowiazujeDo':2}
        
        s = QgsSettings()
        rodzajZbioru = s.value("qgis_app2/settings/rodzajZbioru", "")
        numerZbioru = s.value("qgis_app2/settings/numerZbioru", "")
        jpt = s.value("qgis_app2/settings/jpt", "")
        idLokalnyAPP = s.value("qgis_app2/settings/idLokalnyAPP","")
        
        placeHolders = {'przestrzenNazw':'np. PL.ZIPPZP.2393/246601-POG',
                        'lokalnyId':'np. 1OSD',
                        'oznaczenie':'np. 1OSD',
                        'symbol':'np. OSD',
                        'minimalnaOdleglosc':'wartość w metrach np. 1500 m',
                        'minOdlegloscOdObszaruZieleniPublicznej':'wartość w metrach np. 3000 m',
                        'powierzchnia obszaru':'wartość w hektarach min. 10 ha',
                        'powierzchnia obszarow':'wartość w hektarach min. 1.5 ha'
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
        
        zapisz = dialog.findChild(QPushButton,"zapisz")
        
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
        
        if obj.id() < 0 and atrybutyPOG not in [None,{}]:
            status.setCurrentText(atrybutyPOG['status'])
        status_kontrola(status.currentText())
        
        koniecWersjiObiektu.valueChanged.connect(poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola)
        
        wylaczenieZabudowyZagrodowej = dialog.findChild(QCheckBox,"wylaczenieZabudowyZagrodowej")
        wylaczenieZabudowyZagrodowej.stateChanged.connect(wylaczenieZabudowyZagrodowej_kontrola)
        
        odlegloscDoSzkolyPodstawowej = dialog.findChild(QLineEdit,"odlegloscDoSzkolyPodstawowej")
        odlegloscDoSzkolyPodstawowej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoSzkolyPodstawowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoSzkolyPodstawowej.textChanged.connect(odlegloscDoSzkolyPodstawowej_kontrola)
        odlegloscDoSzkolyPodstawowej_kontrola(odlegloscDoSzkolyPodstawowej.text())
        
        odlegloscDoObszarowZieleniPublicznej = dialog.findChild(QLineEdit,"odlegloscDoObszarowZieleniPublicznej")
        odlegloscDoObszarowZieleniPublicznej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoObszarowZieleniPublicznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoObszarowZieleniPublicznej.textChanged.connect(odlegloscDoObszarowZieleniPublicznej_kontrola)
        odlegloscDoObszarowZieleniPublicznej_kontrola(odlegloscDoObszarowZieleniPublicznej.text())
        
        powierzchniaLacznaObszarowZieleniPublicznej = dialog.findChild(QLineEdit,"powierzchniaLacznaObszarowZieleniPublicznej")
        powierzchniaLacznaObszarowZieleniPublicznej.setValidator(QRegExpValidator(QRegExp(r"[1-9][0-9]{0,5}\.([0-9]{1})?")))
        powierzchniaLacznaObszarowZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszarow'])
        powierzchniaLacznaObszarowZieleniPublicznej.setText(powierzchniaLacznaObszarowZieleniPublicznej.text().replace(",","."))
        powierzchniaLacznaObszarowZieleniPublicznej.textChanged.connect(powierzchniaLacznaObszarowZieleniPublicznej_kontrola)
        powierzchniaLacznaObszarowZieleniPublicznej_kontrola(powierzchniaLacznaObszarowZieleniPublicznej.text())
        
        odlegloscDoObszaruZieleniPublicznej = dialog.findChild(QLineEdit,"odlegloscDoObszaruZieleniPublicznej")
        odlegloscDoObszaruZieleniPublicznej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoObszaruZieleniPublicznej.setPlaceholderText(placeHolders['minOdlegloscOdObszaruZieleniPublicznej'])
        odlegloscDoObszaruZieleniPublicznej.textChanged.connect(odlegloscDoObszaruZieleniPublicznej_kontrola)
        odlegloscDoObszaruZieleniPublicznej_kontrola(odlegloscDoObszaruZieleniPublicznej.text())
        
        powierzchniaObszaruZieleniPublicznej = dialog.findChild(QLineEdit,"powierzchniaObszaruZieleniPublicznej")
        powierzchniaObszaruZieleniPublicznej.setValidator(QRegExpValidator(QRegExp(r"[1-9][0-9]{1,5}\.([0-9]{1})?")))
        powierzchniaObszaruZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszaru'])
        powierzchniaObszaruZieleniPublicznej.setText(powierzchniaObszaruZieleniPublicznej.text().replace(",","."))
        powierzchniaObszaruZieleniPublicznej.textChanged.connect(powierzchniaObszaruZieleniPublicznej_kontrola)
        powierzchniaObszaruZieleniPublicznej_kontrola(powierzchniaObszaruZieleniPublicznej.text())
        
        odlegloscDoPrzedszkola = dialog.findChild(QLineEdit,"odlegloscDoPrzedszkola")
        odlegloscDoPrzedszkola.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoPrzedszkola.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoPrzedszkola.textChanged.connect(odlegloscDoPrzedszkola_kontrola)
        
        odlegloscDoZlobka = dialog.findChild(QLineEdit,"odlegloscDoZlobka")
        odlegloscDoZlobka.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoZlobka.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoZlobka.textChanged.connect(odlegloscDoZlobka_kontrola)
        
        odlegloscDoAmbulatoriumPOZ = dialog.findChild(QLineEdit,"odlegloscDoAmbulatoriumPOZ")
        odlegloscDoAmbulatoriumPOZ.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoAmbulatoriumPOZ.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoAmbulatoriumPOZ.textChanged.connect(odlegloscDoAmbulatoriumPOZ_kontrola)
        
        odlegloscDoBiblioteki = dialog.findChild(QLineEdit,"odlegloscDoBiblioteki")
        odlegloscDoBiblioteki.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoBiblioteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoBiblioteki.textChanged.connect(odlegloscDoBiblioteki_kontrola)
        
        odlegloscDoDomuKultury = dialog.findChild(QLineEdit,"odlegloscDoDomuKultury")
        odlegloscDoDomuKultury.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoDomuKultury.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoDomuKultury.textChanged.connect(odlegloscDoDomuKultury_kontrola)
        
        odlegloscDoDomuPomocySpolecznej = dialog.findChild(QLineEdit,"odlegloscDoDomuPomocySpolecznej")
        odlegloscDoDomuPomocySpolecznej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoDomuPomocySpolecznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoDomuPomocySpolecznej.textChanged.connect(odlegloscDoDomuPomocySpolecznej_kontrola)
        
        odlegloscDoUrzadzonegoTerenuSportu = dialog.findChild(QLineEdit,"odlegloscDoUrzadzonegoTerenuSportu")
        odlegloscDoUrzadzonegoTerenuSportu.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoUrzadzonegoTerenuSportu.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoUrzadzonegoTerenuSportu.textChanged.connect(odlegloscDoUrzadzonegoTerenuSportu_kontrola)
        
        odlegloscDoPrzystanku = dialog.findChild(QLineEdit,"odlegloscDoPrzystanku")
        odlegloscDoPrzystanku.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoPrzystanku.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoPrzystanku.textChanged.connect(odlegloscDoPrzystanku_kontrola)
        
        odlegloscDoPlacowkiPocztowej = dialog.findChild(QLineEdit,"odlegloscDoPlacowkiPocztowej")
        odlegloscDoPlacowkiPocztowej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoPlacowkiPocztowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoPlacowkiPocztowej.textChanged.connect(odlegloscDoPlacowkiPocztowej_kontrola)
        
        odlegloscDoApteki = dialog.findChild(QLineEdit,"odlegloscDoApteki")
        odlegloscDoApteki.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoApteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoApteki.textChanged.connect(odlegloscDoApteki_kontrola)
        
        odlegloscDoPosterunkuPolicji = dialog.findChild(QLineEdit,"odlegloscDoPosterunkuPolicji")
        odlegloscDoPosterunkuPolicji.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoPosterunkuPolicji.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoPosterunkuPolicji.textChanged.connect(odlegloscDoPosterunkuPolicji_kontrola)
        
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej = dialog.findChild(QLineEdit,"odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej")
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setValidator(QRegExpValidator(QRegExp(r"[1-9]\d{0,4}")))
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.textChanged.connect(odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej_kontrola)
        
        geometria_kontrola()
        poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
        
        tablicaZmian = [0] * len(warstwa.fields())
        
        zapisz.clicked.connect(zapis)
        zapisz.setEnabled(False)
        zapisz.setText("Zapisz")
        
        labels = [None for i in range(30)]
        pixmap = QPixmap(':/plugins/wtyczka_app/img/info2.png')
        for i in range(30):
            labels[i] = dialog.findChild(QLabel,"label_" + str(i + 1))
            labels[i].setPixmap(pixmap)
            labels[i].setToolTip(pomoc[i])
        
        operacjeNaAtrybucie('oznaczenie')
        operacjeNaAtrybucie('odlegloscDoSzkolyPodstawowej')
        operacjeNaAtrybucie('odlegloscDoObszarowZieleniPublicznej')
        operacjeNaAtrybucie('powierzchniaLacznaObszarowZieleniPublicznej')
        operacjeNaAtrybucie('odlegloscDoObszaruZieleniPublicznej')
        operacjeNaAtrybucie('powierzchniaObszaruZieleniPublicznej')
        operacjeNaAtrybucie('status')
        operacjeNaAtrybucie('obowiazujeOd')
        operacjeNaAtrybucie('obowiazujeDo')
        operacjeNaAtrybucie('koniecWersjiObiektu')
        
        dlg.parent().rejected.connect(dialogRejected)
        
        def on_geometry_changed(fid):
            changed_feature = layer.getFeature(fid)
            field_names = [field.name() for field in layer.fields()]
            dataCzasTeraz = QDateTime.currentDateTimeUtc()
            
            if 'wersjaId' in field_names:
                changed_feature.setAttribute("wersjaId", dataCzasTeraz.toString("yyyyMMddThhmmss"))
            if 'poczatekWersjiObiektu' in field_names:
                changed_feature.setAttribute("poczatekWersjiObiektu", dataCzasTeraz)
            if 'edycja' in field_names:
                changed_feature.setAttribute("edycja", True)
                
            layer.updateFeature(changed_feature)
        
        warstwa.geometryChanged.connect(on_geometry_changed)
        czyZmianaJestDopuszczalna = True
        przestrzenNazw_kontrola()
    except Exception as e:
        pass


def komunikowanieBledu(object, txt, nazwaAtrybutu):
    try:
        object.setToolTip(txt)
        if txt == '':
            listaBledowAtrybutow[warstwa.fields().indexFromName(nazwaAtrybutu)] = 0
            object.setStyleSheet("")
        else:
            listaBledowAtrybutow[warstwa.fields().indexFromName(nazwaAtrybutu)] = 1
            object.setStyleSheet("border: 1px solid red")
    except Exception as e:
        pass


def zmianaWersjiIPoczatkuWersji():
    try:
        if czyZmianaJestDopuszczalna:
            if sum(listaBledowAtrybutow) > 0 or sum(tablicaZmian) == 1:
                wersjaId.setDateTime(datetime.strptime(obj['wersjaId'], "%Y%m%dT%H%M%S"))
            
            KWO_dateTime = koniecWersjiObiektu.dateTime()
            dataCzasTeraz = QDateTime.currentDateTimeUtc()
            
            if KWO_dateTime.time().msec() != 0 and KWO_dateTime.date().year() != 1 and sum(tablicaZmian) > 0:
                wersjaId.setDateTime(dataCzasTeraz)
            else:
                wlaczenieLubWylaczenieZapisu()
    except Exception as e:
        pass


def wlaczenieLubWylaczenieZapisu():
    global zapisz
    try:
        if sum(listaBledowAtrybutow) == 0 and warstwa.isEditable() and czyZmianaJestDopuszczalna and sum(tablicaZmian) > 0:
            zapisz.setEnabled(True)
            zapisz.setText("Zapisz")
        else:
            zapisz.setEnabled(False)
    except Exception as e:
        pass


def zapis():
    global zapisz
    try:
        obj.setAttribute(warstwa.fields().indexFromName('edycja'),True)
        if obj.id() > 0:
            obj.setGeometry(warstwa.getFeature(obj.id()).geometry())
        warstwa.updateFeature(obj)
        dlg.save()
        warstwa.commitChanges(False)
        zapisz.setEnabled(False)
        zapisz.setText("Zapisano")
        
        if obj.id() < 0:
            dlg.parent().close()
    except Exception as e:
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
    except Exception as e:
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
                zmianaWTablicyZmian(txt, 'przestrzenNazw')
                komunikowanieBledu(przestrzenNazw,'','przestrzenNazw')
            teryt_gminy = przestrzenNazw.text().split("/")[1].split("-")[0]
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
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
    except Exception as e:
        pass


def wersjaId_kontrola():
    try:
        zmianaWTablicyZmian(wersjaId.dateTime().toString("yyyyMMdd'T'hhmmss"), 'wersjaId')
        if koniecWersjiObiektu.dateTime().time().msec() != 0 and koniecWersjiObiektu.dateTime().date().year() != 1:
            poczatekWersjiObiektu.disconnect()
            poczatekWersjiObiektu.setDateTime(wersjaId.dateTime())
            poczatekWersjiObiektu.dateTimeChanged.connect(poczatekWersjiObiektu_kontrola)
        wlaczenieLubWylaczenieZapisu()
    except Exception as e:
        pass


def poczatekWersjiObiektu_kontrola():
    try:
        if koniecWersjiObiektu.dateTime().time().msec() != 0 and koniecWersjiObiektu.dateTime().date().year() != 1:
            wersjaId.setDateTime(poczatekWersjiObiektu.dateTime())
        poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola()
    except Exception as e:
        pass


def oznaczenie_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'oznaczenie')
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
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def symbol_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'symbol')
        if txt == '':
            symbol.setPlaceholderText(placeHolders['symbol'])
            komunikowanieBledu(symbol,'Symbol jest polem obowiązkowym','symbol')
        else:
            komunikowanieBledu(symbol,'','symbol')
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def charakterUstalenia_kontrola(txt):
    pass


def status_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'status')
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
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola():
    try:
        obowiazujeOdTxt = obowiazujeOd.dateTime().toString("H:mm")
        obowiazujeDoTxt = obowiazujeDo.dateTime().toString("H:mm")
        koniecWersjiObiektuTxt = koniecWersjiObiektu.dateTime().toString("H:mm")
        
        if obowiazujeOdTxt in ['0:00','23:59']:
            zmianaWTablicyZmian(obowiazujeOd.date(), 'obowiazujeOd')
        else:
            zmianaWTablicyZmian(NULL, 'obowiazujeOd')
        
        if obowiazujeDoTxt in ['0:00','23:59']:
            zmianaWTablicyZmian(obowiazujeDo.date(), 'obowiazujeDo')
        else:
            zmianaWTablicyZmian(NULL, 'obowiazujeDo')
        
        if obowiazujeOdTxt not in ['0:00','23:59'] and kontrolaAtrybutu['obowiazujeOd'] == 2:
            komunikowanieBledu(obowiazujeOd, 'Należy wybrać datę dla "obowiązuje od"', 'obowiazujeOd')
        else:
            if obowiazujeDoTxt in ['0:00','23:59'] and obowiazujeOd.dateTime() >= obowiazujeDo.dateTime() and kontrolaAtrybutu['obowiazujeOd'] == 2:
                komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
            else:
                komunikowanieBledu(obowiazujeOd, '', 'obowiazujeOd')
        if koniecWersjiObiektu.dateTime().time().msec() == 0 and koniecWersjiObiektu.dateTime().date().year() != 1 and poczatekWersjiObiektu.dateTime() >= koniecWersjiObiektu.dateTime():
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
                if obowiazujeOd.dateTime() >= obowiazujeDo.dateTime() and obowiazujeDo.dateTime().time().msec() == 0 and obowiazujeOd.dateTime().time().msec() == 0 and kontrolaAtrybutu['obowiazujeOd'] == 2:
                    komunikowanieBledu(obowiazujeOd, 'Atrybut "obowiązuje od" nie może być większy lub równy od "obowiązuje do".', 'obowiazujeOd')
                else:
                    komunikowanieBledu(obowiazujeDo, '', 'obowiazujeDo')
        
        if koniecWersjiObiektu.dateTime().toString("zzz") == '000' and koniecWersjiObiektu.dateTime().toString("H:mm:ss") != '0:00:00':
            zmianaWTablicyZmian(koniecWersjiObiektu.dateTime(), 'koniecWersjiObiektu')
        else:
            zmianaWTablicyZmian(NULL, 'koniecWersjiObiektu')
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def wylaczenieZabudowyZagrodowej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'wylaczenieZabudowyZagrodowej')
        komunikowanieBledu(wylaczenieZabudowyZagrodowej,'','wylaczenieZabudowyZagrodowej')
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoSzkolyPodstawowej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoSzkolyPodstawowej')
        if txt == '' and kontrolaAtrybutu['odlegloscDoSzkolyPodstawowej'] == 2:
            komunikowanieBledu(odlegloscDoSzkolyPodstawowej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoSzkolyPodstawowej')
        else:
            komunikowanieBledu(odlegloscDoSzkolyPodstawowej,'','odlegloscDoSzkolyPodstawowej')
        odlegloscDoSzkolyPodstawowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoObszarowZieleniPublicznej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoObszarowZieleniPublicznej')
        if txt == '' and kontrolaAtrybutu['odlegloscDoObszarowZieleniPublicznej'] == 2:
            komunikowanieBledu(odlegloscDoObszarowZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoObszarowZieleniPublicznej')
        else:
            komunikowanieBledu(odlegloscDoObszarowZieleniPublicznej,'','odlegloscDoObszarowZieleniPublicznej')
        odlegloscDoObszarowZieleniPublicznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def powierzchniaLacznaObszarowZieleniPublicznej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'powierzchniaLacznaObszarowZieleniPublicznej')
        txt = txt.replace(",",".")
        if txt == '' and kontrolaAtrybutu['powierzchniaLacznaObszarowZieleniPublicznej'] == 2:
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','powierzchniaLacznaObszarowZieleniPublicznej')
        elif kontrolaAtrybutu['powierzchniaLacznaObszarowZieleniPublicznej'] == 2 and not 1.5 <= float(txt):
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'Powierzchnia musi być większa lub równa 1,5 ha.','powierzchniaLacznaObszarowZieleniPublicznej')
        else:
            komunikowanieBledu(powierzchniaLacznaObszarowZieleniPublicznej,'','powierzchniaLacznaObszarowZieleniPublicznej')
        powierzchniaLacznaObszarowZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszarow'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoObszaruZieleniPublicznej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoObszaruZieleniPublicznej')
        if txt == '' and kontrolaAtrybutu['odlegloscDoObszaruZieleniPublicznej'] == 2:
            komunikowanieBledu(odlegloscDoObszaruZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','odlegloscDoObszaruZieleniPublicznej')
        else:
            komunikowanieBledu(odlegloscDoObszaruZieleniPublicznej,'','odlegloscDoObszaruZieleniPublicznej')
        odlegloscDoObszaruZieleniPublicznej.setPlaceholderText(placeHolders['minOdlegloscOdObszaruZieleniPublicznej'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def powierzchniaObszaruZieleniPublicznej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'powierzchniaObszaruZieleniPublicznej')
        txt = txt.replace(",",".")
        if txt == '' and kontrolaAtrybutu['powierzchniaObszaruZieleniPublicznej'] == 2:
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'Wartość atrybutu jest obligatoryjna.','powierzchniaObszaruZieleniPublicznej')
        elif kontrolaAtrybutu['powierzchniaObszaruZieleniPublicznej'] == 2 and not 10 <= float(txt):
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'Powierzchnia musi być większa lub równa 10 ha.','powierzchniaObszaruZieleniPublicznej')
        else:
            komunikowanieBledu(powierzchniaObszaruZieleniPublicznej,'','powierzchniaObszaruZieleniPublicznej')
        powierzchniaObszaruZieleniPublicznej.setPlaceholderText(placeHolders['powierzchnia obszaru'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoPrzedszkola_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoPrzedszkola')
        odlegloscDoPrzedszkola.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoZlobka_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoZlobka')
        odlegloscDoZlobka.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoAmbulatoriumPOZ_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoAmbulatoriumPOZ')
        odlegloscDoAmbulatoriumPOZ.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoBiblioteki_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoBiblioteki')
        odlegloscDoBiblioteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        komunikowanieBledu(odlegloscDoBiblioteki,'','odlegloscDoBiblioteki')
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoDomuKultury_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoDomuKultury')
        odlegloscDoDomuKultury.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoDomuPomocySpolecznej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoDomuPomocySpolecznej')
        odlegloscDoDomuPomocySpolecznej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoUrzadzonegoTerenuSportu_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoUrzadzonegoTerenuSportu')
        odlegloscDoUrzadzonegoTerenuSportu.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoPrzystanku_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoPrzystanku')
        odlegloscDoPrzystanku.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoPlacowkiPocztowej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoPlacowkiPocztowej')
        odlegloscDoPlacowkiPocztowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoApteki_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoApteki')
        odlegloscDoApteki.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoPosterunkuPolicji_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoPosterunkuPolicji')
        odlegloscDoPosterunkuPolicji.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej_kontrola(txt):
    try:
        zmianaWTablicyZmian(txt, 'odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej')
        odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej.setPlaceholderText(placeHolders['minimalnaOdleglosc'])
        
        zmianaWersjiIPoczatkuWersji()
    except Exception as e:
        pass


def czyWartoscAtrybutuJestUnikalna(atrybut, wartosc):
    wartoscAtrybutuJestUnikalna = True
    if koniecWersjiObiektu.dateTime().time().msec() != 0:
        request = QgsFeatureRequest(QgsExpression('koniecWersjiObiektu is NULL and ' + atrybut + "='" + wartosc + "'"))
        for x in warstwa.getFeatures(request):
            if x.id() != fid:
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
    except Exception as e:
        pass


def operacjeNaAtrybucie(nazwaAtrybutu):
    global operacja, kontrolaAtrybutu_CB
    
    operacje = ['włączona kontrola wypełnienia',
                'włączona kontrola wypełnienia wymaganych atrybutów',
                'hurtowa zmiana atrybutu w ramach wszystkich warstw',
                'hurtowa zmiana atrybutu w ramach warstwy',
                'uspójnienie daty dla obiektów nowych lub zmienionych'
               ]
    atrybutOperacje = {'oznaczenie':[0,1],
                       'odlegloscDoSzkolyPodstawowej':[0,1],
                       'odlegloscDoObszarowZieleniPublicznej':[0,1],
                       'powierzchniaLacznaObszarowZieleniPublicznej':[0,1],
                       'odlegloscDoObszaruZieleniPublicznej':[0,1],
                       'powierzchniaObszaruZieleniPublicznej':[0,1],
                       'status':[2,3],
                       'obowiazujeOd':[0,1,2,3,4],
                       'obowiazujeDo':[0,1,2,3],
                       'koniecWersjiObiektu':[2,3],
                       }
    atrybutLayout = {'oznaczenie':"gridLayout_2",
                     'odlegloscDoSzkolyPodstawowej':"gridLayout_2",
                     'odlegloscDoObszarowZieleniPublicznej':"gridLayout_2",
                     'powierzchniaLacznaObszarowZieleniPublicznej':"gridLayout_2",
                     'odlegloscDoObszaruZieleniPublicznej':"gridLayout_2",
                     'powierzchniaObszaruZieleniPublicznej':"gridLayout_2",
                     'status':"gridLayout_2",
                     'obowiazujeOd':"gridLayout_2",
                     'obowiazujeDo':"gridLayout_2",
                     'koniecWersjiObiektu':"gridLayout_2"}
    atrybutRowCol = {'oznaczenie':[2,3],
                     'odlegloscDoSzkolyPodstawowej':[8,3],
                     'odlegloscDoObszarowZieleniPublicznej':[9,3],
                     'powierzchniaLacznaObszarowZieleniPublicznej':[10,3],
                     'odlegloscDoObszaruZieleniPublicznej':[11,3],
                     'powierzchniaObszaruZieleniPublicznej':[12,3],
                     'status':[25,3],
                     'obowiazujeOd':[26,3],
                     'obowiazujeDo':[27,3],
                     'koniecWersjiObiektu':[33,3]}
    atrybutKontrola = {'oznaczenie':"oznaczenie_kontrola",
                       'odlegloscDoSzkolyPodstawowej':"odlegloscDoSzkolyPodstawowej_kontrola",
                       'odlegloscDoObszarowZieleniPublicznej':"odlegloscDoObszarowZieleniPublicznej_kontrola",
                       'powierzchniaLacznaObszarowZieleniPublicznej':"powierzchniaLacznaObszarowZieleniPublicznej_kontrola",
                       'odlegloscDoObszaruZieleniPublicznej':"odlegloscDoObszaruZieleniPublicznej_kontrola",
                       'powierzchniaObszaruZieleniPublicznej':"powierzchniaObszaruZieleniPublicznej_kontrola",
                       'obowiazujeOd':"poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola",
                       'obowiazujeDo':"poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola"}
    atrybutOperacje_tmp = []
    for x in atrybutOperacje[nazwaAtrybutu]:
        atrybutOperacje_tmp.append(operacje[x])
    
    qWidget = QWidget()
    wyborAkcji = QToolButton(qWidget)
    wyborAkcji.setFixedSize(18, 18)
    wyborAkcji.setIcon(QIcon(":/plugins/wtyczka_app/img/rectangle.png"))
    wyborAkcji.setPopupMode(QToolButton.InstantPopup)
    wyborAkcji.setStyleSheet("QToolButton::menu-indicator { image: none; }")
    menu = QMenu(wyborAkcji)
    
    for item in atrybutOperacje_tmp:
        action = QAction(item, wyborAkcji)
        if item == 'włączona kontrola wypełnienia':
            action.setCheckable(True)
            if 0 in atrybutOperacje[nazwaAtrybutu]:
                action.setChecked(kontrolaAtrybutu[nazwaAtrybutu])
            action.triggered.connect(lambda checked, text=item: wlaczenieLubWylaczenieKontroli(nazwaAtrybutu,checked))
            kontrolaAtrybutu_CB.append(action)
        elif item == 'włączona kontrola wypełnienia wymaganych atrybutów':
            action.setCheckable(True)
            if 0 in atrybutOperacje[nazwaAtrybutu]:
                action.setChecked(kontrolaAtrybutu[nazwaAtrybutu])
            action.triggered.connect(lambda checked, text=item: wlaczenieLubWylaczenieKontroliWszystkichWymaganychAtrybutow(checked))
            kontrolaAtrybutu_CB.append(action)
        else:
            if item == 'hurtowa zmiana atrybutu w ramach wszystkich warstw':
                action.setIcon(QIcon(":/plugins/wtyczka_app/img/hurtowa_zmiana_atrybutu_ikona.png"))
            elif item == 'hurtowa zmiana atrybutu w ramach warstwy':
                action.setIcon(QIcon(":/plugins/wtyczka_app/img/hurtowa_zmiana_atrybutu_warstwa_ikona.png"))
            elif item == 'uspójnienie daty dla obiektów nowych lub zmienionych':
                action.setIcon(QIcon(":/plugins/wtyczka_app/img/uspojnienie_daty_ikona.png"))
            action.triggered.connect(lambda checked, text=item: wskazanieNaOperacje(nazwaAtrybutu,text))
        menu.addAction(action)
    wyborAkcji.setMenu(menu)
    gridLayout = dlg.findChild(QGridLayout,atrybutLayout[nazwaAtrybutu])
    gridLayout.addWidget(wyborAkcji,atrybutRowCol[nazwaAtrybutu][0],atrybutRowCol[nazwaAtrybutu][1])
    
    operacja = {'oznaczenie':['włączona kontrola wypełnienia'],
                'odlegloscDoSzkolyPodstawowej':['włączona kontrola wypełnienia'],
                'odlegloscDoObszarowZieleniPublicznej':['włączona kontrola wypełnienia'],
                'powierzchniaLacznaObszarowZieleniPublicznej':['włączona kontrola wypełnienia'],
                'odlegloscDoObszaruZieleniPublicznej':['włączona kontrola wypełnienia'],
                'powierzchniaObszaruZieleniPublicznej':['włączona kontrola wypełnienia'],
                'status':[],
                'obowiazujeOd':['włączona kontrola wypełnienia'],
                'obowiazujeDo':['włączona kontrola wypełnienia'],
                'koniecWersjiObiektu':[]}
    
    def wlaczenieLubWylaczenieKontroliWszystkichWymaganychAtrybutow(isChecked):
        global czyZmianaJestDopuszczalna
        czyZmianaJestDopuszczalna = False
        if isChecked:
            for atrybut, operacje in atrybutOperacje.items():
                if 1 in operacje:
                    wlaczenieLubWylaczenieKontroli(atrybut,2)
            for ka in kontrolaAtrybutu_CB:
                ka.setChecked(True)
        else:
            for atrybut, operacje in atrybutOperacje.items():
                if 1 in operacje:
                    wlaczenieLubWylaczenieKontroli(atrybut,0)
            for ka in kontrolaAtrybutu_CB:
                ka.setChecked(False)
        czyZmianaJestDopuszczalna = True
    
    def wlaczenieLubWylaczenieKontroli(atrybut,isChecked):
        global kontrolaAtrybutu, czyZmianaJestDopuszczalna
        czyZmianaJestDopuszczalna = False
        if isChecked:
            kontrolaAtrybutu[atrybut] = 2
        else:
            kontrolaAtrybutu[atrybut] = 0
        if atrybutKontrola[atrybut] == 'poczatekKoniecWersjiObiektuObowiazujeOdDo_kontrola':
            globals().get(atrybutKontrola[atrybut])()
        else:
            if atrybut == 'oznaczenie':
                globals().get(atrybutKontrola[atrybut])(oznaczenie.text())
            elif atrybut == 'odlegloscDoSzkolyPodstawowej':
                globals().get(atrybutKontrola[atrybut])(odlegloscDoSzkolyPodstawowej.text())
            elif atrybut == 'odlegloscDoObszarowZieleniPublicznej':
                globals().get(atrybutKontrola[atrybut])(odlegloscDoObszarowZieleniPublicznej.text())
            elif atrybut == 'powierzchniaLacznaObszarowZieleniPublicznej':
                globals().get(atrybutKontrola[atrybut])(powierzchniaLacznaObszarowZieleniPublicznej.text())
            elif atrybut == 'odlegloscDoObszaruZieleniPublicznej':
                globals().get(atrybutKontrola[atrybut])(odlegloscDoObszaruZieleniPublicznej.text())
            elif atrybut == 'powierzchniaObszaruZieleniPublicznej':
                globals().get(atrybutKontrola[atrybut])(powierzchniaObszaruZieleniPublicznej.text())
        czyZmianaJestDopuszczalna = True
        wlaczenieLubWylaczenieZapisu()
    
    def hurtowaZmianaArybutuWRamachWarstw():
        if obj.id() < 0:
            QMessageBox.warning(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach wszystkich warstw nie może być wykonana dla obiektu, który nie został zapisany.'.format(nazwaAtrybutu))
            return
        
        for o in globals():
            if o == nazwaAtrybutu:
                if isinstance(globals().get(o), QComboBox):
                    atrybut = globals().get(o).currentText()
                elif isinstance(globals().get(o), QDateTimeEdit):
                    atrybut = globals().get(o).dateTime()
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
                   warstwa.name().startswith('OSD_') or \
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
                dataCzasTeraz = QDateTime.currentDateTimeUtc()
                for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                    if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                       warstwa.name().startswith('OSD_') or \
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
                            feature.setAttribute(idx_wersjaId, dataCzasTeraz.toString("yyyyMMddThhmmss"))
                            feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz)
                            warstwa.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        warstwa.commitChanges()
                        warstwa.startEditing()
                progressMessageBar.dismiss()
                dlg.changeAttribute(nazwaAtrybutu, atrybut)
                dlg.changeAttribute('wersjaId', dataCzasTeraz)
                zapis()
            QMessageBox.information(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach wszystkich warstw została zakończona.'.format(nazwaAtrybutu))
    
    def hurtowaZmianaArybutuWRamachWarstwy():
        if obj.id() < 0:
            QMessageBox.warning(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach warstwy nie może być wykonana dla obiektu, który nie został zapisany.'.format(nazwaAtrybutu))
            return
        
        for o in globals():
            if o == nazwaAtrybutu:
                if isinstance(globals().get(o), QComboBox):
                    atrybut = globals().get(o).currentText()
                elif isinstance(globals().get(o), QDateTimeEdit):
                    atrybut = globals().get(o).dateTime()
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
                if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej'):
                    liczbaObiektowDoZmiany += warstwa.featureCount()
            
            if liczbaObiektowDoZmiany > 0:
                progressMessageBar = iface.messageBar().createMessage("Postęp wykonania hurtowej zmiany atrybut {} w ramach warstwy.".format(nazwaAtrybutu))
                progress = QProgressBar()
                progress.setMaximum(liczbaObiektowDoZmiany)
                progressMessageBar.layout().addWidget(progress)
                iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
                y = 0
                dataCzasTeraz = QDateTime.currentDateTimeUtc()
                for warstwa_id, warstwa in QgsProject.instance().mapLayers().items():
                    if warstwa.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or warstwa.name().startswith('OSD_'):
                        warstwa.startEditing()
                        idx_Atrybut = warstwa.fields().indexFromName(nazwaAtrybutu)
                        idx_edycja = warstwa.fields().indexFromName('edycja')
                        idx_wersjaId = warstwa.fields().indexFromName('wersjaId')
                        idx_poczatekWersjiObiektu = warstwa.fields().indexFromName('poczatekWersjiObiektu')
                        for feature in warstwa.getFeatures():
                            feature.setAttribute(idx_Atrybut, atrybut)
                            feature.setAttribute(idx_edycja, True)
                            feature.setAttribute(idx_wersjaId, dataCzasTeraz.toString("yyyyMMddThhmmss"))
                            feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz)
                            warstwa.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        warstwa.commitChanges()
                        warstwa.startEditing()
                        break
                progressMessageBar.dismiss()
                dlg.changeAttribute(nazwaAtrybutu, atrybut)
                dlg.changeAttribute('wersjaId', dataCzasTeraz)
                zapis()
            QMessageBox.information(None,'Informacja','Hurtowa zmiana atrybutu {} w ramach warstwy została zakończona.'.format(nazwaAtrybutu))
    
    def uspojnienieDatyObowiazujeOd():
        if obj.id() < 0:
            QMessageBox.warning(None,'Informacja','Uspójnienie daty "obowiązuje od" nie może być wykonane dla obiektu, który nie został zapisany.')
            return
        
        odp = QMessageBox.question(None,'Operacje na danych', 'UWAGA: Jeśli w trakcie edycji danych użyta została wcześniej funkcja hurtowej zmiany atrybutu, \
wówczas funkcja uspójnienia zostanie zastosowana we wszystkich obiektach, w których zaszła zmiana hurtowa.\n\
Czy uspójnić "obowiązuje od" dla obiektów nowych lub zmienionych w ramach wszystkich warstw?', QMessageBox.Yes |
                                   QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.No:
            return
        else:
            liczbaObiektowDoZmiany = 0
            for warstwa_id, lyr in QgsProject.instance().mapLayers().items():
                if lyr.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                   lyr.name().startswith('OSD_') or \
                   lyr.name().startswith('ObszarUzupelnieniaZabudowy') or \
                   lyr.name().startswith('ObszarZabudowySrodmiejskiej') or \
                   lyr.name().startswith('StrefaPlanistyczna'):
                       for f in lyr.getFeatures():
                           if f['edycja']:
                               liczbaObiektowDoZmiany += 1
            
            if liczbaObiektowDoZmiany > 0:
                istniejeAktPlanowaniaPrzestrzennego = False
                for warstwa_id, lyr in QgsProject.instance().mapLayers().items():
                    if lyr.name().startswith('AktPlanowaniaPrzestrzennego'):
                        liczbaObiektowDoZmiany += 1
                        istniejeAktPlanowaniaPrzestrzennego = True
            
                if not istniejeAktPlanowaniaPrzestrzennego:
                    QMessageBox.warning(None,'Informacja','Brak warstwy AktPlanowaniaPrzestrzennego.\nUspójnienie daty "obowiązuje od" zostało zatrzymane.')
                    return
            
            if liczbaObiektowDoZmiany > 1:
                progressMessageBar = iface.messageBar().createMessage('Postęp wykonania uspójnienia daty "obowiązuje od" w ramach wszystkich warstw.')
                progress = QProgressBar()
                progress.setMaximum(liczbaObiektowDoZmiany)
                progressMessageBar.layout().addWidget(progress)
                iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
                y = 0
                dataCzasTeraz = QDateTime.currentDateTimeUtc()
                for warstwa_id, lyr in QgsProject.instance().mapLayers().items():
                    if lyr.name().startswith('ObszarStandardowDostepnosciInfrastrukturySpolecznej') or \
                       lyr.name().startswith('OSD_') or \
                       lyr.name().startswith('ObszarUzupelnieniaZabudowy') or \
                       lyr.name().startswith('ObszarZabudowySrodmiejskiej') or \
                       lyr.name().startswith('AktPlanowaniaPrzestrzennego') or \
                       lyr.name().startswith('StrefaPlanistyczna'):
                        lyr.startEditing()
                        idx_obowiazujeOd = lyr.fields().indexFromName('obowiazujeOd')
                        idx_wersjaId = lyr.fields().indexFromName('wersjaId')
                        idx_poczatekWersjiObiektu = lyr.fields().indexFromName('poczatekWersjiObiektu')
                        for feature in lyr.getFeatures():
                            if feature['edycja'] or lyr.name().startswith('AktPlanowaniaPrzestrzennego'):
                                feature.setAttribute(idx_obowiazujeOd, obowiazujeOd.dateTime())
                                feature.setAttribute(idx_wersjaId, dataCzasTeraz.toString("yyyyMMddThhmmss"))
                                feature.setAttribute(idx_poczatekWersjiObiektu, dataCzasTeraz)
                            lyr.updateFeature(feature)
                            y += 1
                            progress.setValue(y)
                        lyr.commitChanges()
                        lyr.startEditing()
                progressMessageBar.dismiss()
                dlg.changeAttribute('obowiazujeOd', obowiazujeOd.dateTime())
                dlg.changeAttribute('wersjaId', dataCzasTeraz)
                zapis()
            QMessageBox.information(None,'Informacja','Uspójnienie daty "obowiązuje od" w ramach wszystkich warstw zostało zakończone.')
    
    def wskazanieNaOperacje(atrybut,txt):
        nazwaAtrybutu = atrybut
        if txt == 'hurtowa zmiana atrybutu w ramach wszystkich warstw':
            hurtowaZmianaArybutuWRamachWarstw()
        elif txt == 'hurtowa zmiana atrybutu w ramach warstwy':
            hurtowaZmianaArybutuWRamachWarstwy()
        elif txt == 'uspójnienie daty dla obiektów nowych lub zmienionych':
            uspojnienieDatyObowiazujeOd()


def zmianaWTablicyZmian(txt, nazwaAtrybutu):
    global tablicaZmian
    if czyZmianaJestDopuszczalna:
        if txt == '':
            txt = NULL
        
        if obj[nazwaAtrybutu] == '':
            attr = NULL
        else:
            attr = obj[nazwaAtrybutu]
        
        if txt != NULL and isinstance(obj[nazwaAtrybutu], float):
            txt = float(txt)
        
        if txt == attr:
            tablicaZmian[warstwa.fields().indexFromName(nazwaAtrybutu)] = 0
        else:
            tablicaZmian[warstwa.fields().indexFromName(nazwaAtrybutu)] = 1


def dialogRejected():
    try:
        global obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        global zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        global charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        global wylaczenieZabudowyZagrodowej, odlegloscDoSzkolyPodstawowej, odlegloscDoObszarowZieleniPublicznej
        global powierzchniaLacznaObszarowZieleniPublicznej, odlegloscDoObszaruZieleniPublicznej, powierzchniaObszaruZieleniPublicznej
        global odlegloscDoPrzedszkola, odlegloscDoZlobka, odlegloscDoAmbulatoriumPOZ, odlegloscDoBiblioteki, odlegloscDoDomuKultury
        global odlegloscDoDomuPomocySpolecznej, odlegloscDoUrzadzonegoTerenuSportu, odlegloscDoPrzystanku, odlegloscDoPlacowkiPocztowej
        global odlegloscDoApteki, odlegloscDoPosterunkuPolicji, odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej
        global rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        global tablicaZmian, kontrolaAtrybutu, kontrolaAtrybutu_CB, fid
        
        del obj, dlg, warstwa, listaBledowAtrybutow, placeHolders, teryt_gminy
        del zapisz, przestrzenNazw, koniecWersjiObiektu, lokalnyId, wersjaId, poczatekWersjiObiektu, nazwa, oznaczenie, symbol
        del charakterUstalenia, status, obowiazujeOd, obowiazujeDo, obowiazujeOd_label, obowiazujeDo_label
        del wylaczenieZabudowyZagrodowej, odlegloscDoSzkolyPodstawowej, odlegloscDoObszarowZieleniPublicznej
        del powierzchniaLacznaObszarowZieleniPublicznej, odlegloscDoObszaruZieleniPublicznej, powierzchniaObszaruZieleniPublicznej
        del odlegloscDoPrzedszkola, odlegloscDoZlobka, odlegloscDoAmbulatoriumPOZ, odlegloscDoBiblioteki, odlegloscDoDomuKultury
        del odlegloscDoDomuPomocySpolecznej, odlegloscDoUrzadzonegoTerenuSportu, odlegloscDoPrzystanku, odlegloscDoPlacowkiPocztowej
        del odlegloscDoApteki, odlegloscDoPosterunkuPolicji, odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej
        del rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
        del tablicaZmian, kontrolaAtrybutu, kontrolaAtrybutu_CB, fid
    except Exception as e:
        pass