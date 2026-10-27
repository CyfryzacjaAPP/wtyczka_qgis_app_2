# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu APP
 ***************************************************************************/
"""

import os

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui

from .. import utils, Formularz
from ..base_dialogs import CloseMessageDialog, ButtonsDialog
from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QRegExp
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt.QtCore import QEvent
from qgis.PyQt.QtGui import QRegExpValidator, QValidator

global s, rodzajZbioru, numerZbioru, jpt, idLokalnyAPP
s = QgsSettings()

title_question = 'Praca z APP / zbiorem APP'
title_app = 'Praca z APP'
title_app_uniewaznienie = 'Praca z APP po stwierdzeniu nieważności części POG'
icon_path = ':/plugins/wtyczka_app/img/praca_z_app.png'
icon_path_po_uniewaznieniu = ':/plugins/wtyczka_app/img/praca_z_app_po_uniewaznieniu.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pytanie_dialog_base.ui'))
FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'zbior_przygotowanie_dialog_base.ui'))
FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'raster_instrukcja_dialog_base.ui'))
FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'formularz_raster_dialog_base.ui'))
if s.value("qgis_app2/settings/rodzajZbioru", "/") != 'POG':
    FORM_CLASS4, _ = uic.loadUiType(os.path.join(
        os.path.dirname(__file__), 'views', 'ui', 'formularz_dokumenty_dialog_base.ui'))
else:
    FORM_CLASS4, _ = uic.loadUiType(os.path.join(
        os.path.dirname(__file__), 'views', 'ui', 'formularz_dokumenty_dialog_base_POG.ui'))
FORM_CLASS5, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'formularz_wektor_dialog_base.ui'))
if s.value("qgis_app2/settings/rodzajZbioru", "/") != 'POG':
    FORM_CLASS6, _ = uic.loadUiType(os.path.join(
        os.path.dirname(__file__), 'views', 'ui', 'generowanie_gml_dialog_base.ui'))
else:
    FORM_CLASS6, _ = uic.loadUiType(os.path.join(
        os.path.dirname(__file__), 'views', 'ui', 'generowanie_gml_dialog_base_POG.ui'))
FORM_CLASS7, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_base.ui'))

# dla planu ogólnego gminy
FORM_CLASS8, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_SPL.ui'))
FORM_CLASS9, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_OUZ.ui'))
FORM_CLASS10, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_OZS.ui'))
FORM_CLASS11, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_OSD.ui'))
FORM_CLASS12, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'wektor_instrukcja_dialog_POG.ui'))

# dla planu ogólnego gminy w przypadku unieważnienia
FORM_CLASS13, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pytanie_dialog_base_uniewaznienie.ui'))
FORM_CLASS14, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'formularz_instrukcja_dialog_POG_po_uniewaznieniu.ui'))
FORM_CLASS15, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'formularz_dokumenty_dialog_base_POG_po_uniewaznieniu.ui'))
FORM_CLASS16, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'generowanie_gml_dialog_base_POG_po_uniewaznieniu.ui'))


class PytanieAppDialog(CloseMessageDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(PytanieAppDialog, self).__init__(parent)
        self.name = 'PytanieAppDialog'
        self.setupUi(self)
        self.setWindowTitle(title_question)
        self.setWindowIcon(QtGui.QIcon(':/plugins/wtyczka_app/img/logo.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)


class ZbiorPrzygotowanieDialog(CloseMessageDialog, FORM_CLASS1, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(ZbiorPrzygotowanieDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Tworzenie zbioru APP')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)


class RasterInstrukcjaDialog(CloseMessageDialog, FORM_CLASS2, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 1 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)


class RasterFormularzDialog(CloseMessageDialog, FORM_CLASS3, Formularz, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 2 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.removeForm(container=self.form_scrollArea)
        self.formElements = utils.createFormElementsRysunekAPP()
        self.createForm(container=self.form_scrollArea, formElements=self.formElements)
        # self.returnFormElements(self.formElements)
        
        # blokada edycji wersjaId
        self.wersjaId_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(),name="wersjaId_lineEdit")
        self.wersjaId_lineEdit.setEnabled(False)
        
        # blokada edycji przestrzenNazw
        self.przestrzenNazw_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="przestrzenNazw_lineEdit")
        self.przestrzenNazw_lineEdit.setEnabled(False)
        
        self.poczatekWersjiObiektu_dateTimeEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(),
                                                                              name="poczatekWersjiObiektu_dateTimeEdit")
        # w związku z ułomnoscią QgsDateTimeEdit muszą być oba sygnały:
        self.poczatekWersjiObiektu_dateTimeEdit.valueChanged.connect(self.updateWersjaId)
        self.poczatekWersjiObiektu_dateTimeEdit.dateTimeChanged.connect(self.updateWersjaId)
        self.przestrzenNazw_lineEdit.textChanged.connect(self.updatePrzestrzenNazw)
        ButtonsDialog.__init__(self)

    def updateWersjaId(self):
        """Aktualizuje dane obsługiwane przez operację `updateWersjaId`."""
        self.wersjaId_lineEdit.setText(self.poczatekWersjiObiektu_dateTimeEdit.dateTime().toString("yyyyMMddThhmmss"))

    def updatePrzestrzenNazw(self):
        """Aktualizuje dane obsługiwane przez operację `updatePrzestrzenNazw`."""
        self.przestrzenNazw_lineEdit.setText(s.value("qgis_app2/settings/przestrzenNazw", "/"))


class WektorInstrukcjaDialog(CloseMessageDialog, FORM_CLASS7, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 3 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)


class WektorFormularzDialog(CloseMessageDialog, FORM_CLASS5, Formularz, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 4 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.removeForm(container=self.form_scrollArea)
        self.formElements = utils.createFormElementsAktPlanowaniaPrzestrzennego()
        self.createForm(container=self.form_scrollArea,
                        formElements=self.formElements)
        
        # Ograniczenie wartości typPlanu do wartości
        # zgodnych z rodzajem zbioru wybranym w ustawieniach.
        typ_planu_dla_zbioru = {
            'PZPW': [
                'plan zagospodarowania przestrzennego województwa'
            ],
            'SUIKZP': [
                'studium uwarunkowań i kier. zagosp. przestrz. gminy'
            ],
            'MPZP': [
                'miejscowy plan zagospodarowania przestrzennego',
                'miejscowy plan odbudowy',
                'miejscowy plan rewitalizacji',
                'zintegrowany plan inwestycyjny'
            ],
            'UK': [
                'uchwała krajobrazowa'
            ],
            'AK': [
                'audyt krajobrazowy'
            ],
            'ZPI': [
                'zintegrowany plan inwestycyjny'
            ]
        }
        
        rodzaj_zbioru = s.value(
            "qgis_app2/settings/rodzajZbioru",
            ""
        )
        
        typ_planu = utils.layout_widget_by_name(
            self.form_scrollArea.widget().layout(),
            name="typPlanu_cmbbx"
        )
        
        if typ_planu and rodzaj_zbioru in typ_planu_dla_zbioru:
            typ_planu.clear()
            typ_planu.addItems(
                typ_planu_dla_zbioru[rodzaj_zbioru]
            )
        
            # Jeżeli dopuszczalna jest tylko jedna wartość,
            # użytkownik nie ma potrzeby jej zmieniać.
            typ_planu.setEnabled(
                len(typ_planu_dla_zbioru[rodzaj_zbioru]) > 1
            )
        
        # self.returnFormElements(self.formElements)
        
        # blokada edycji wersjaId
        self.wersjaId_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_lineEdit")
        self.wersjaId_lineEdit.setEnabled(False)
        
        # blokada edycji przestrzenNazw
        self.przestrzenNazw_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="przestrzenNazw_lineEdit")
        self.przestrzenNazw_lineEdit.setEnabled(False)
        
        self.poczatekWersjiObiektu_dateTimeEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(),
                                                                              name="poczatekWersjiObiektu_dateTimeEdit")
        # w związku z ułomnoscią QgsDateTimeEdit muszą być oba sygnały:
        self.poczatekWersjiObiektu_dateTimeEdit.valueChanged.connect(self.updateWersjaId)
        self.poczatekWersjiObiektu_dateTimeEdit.dateTimeChanged.connect(self.updateWersjaId)
        self.przestrzenNazw_lineEdit.textChanged.connect(self.updatePrzestrzenNazw)
        ButtonsDialog.__init__(self)

    def updateWersjaId(self):
        """Aktualizuje dane obsługiwane przez operację `updateWersjaId`."""
        self.wersjaId_lineEdit.setText(self.poczatekWersjiObiektu_dateTimeEdit.dateTime().toString("yyyyMMddThhmmss"))

    def updatePrzestrzenNazw(self):
        """Aktualizuje dane obsługiwane przez operację `updatePrzestrzenNazw`."""
        self.przestrzenNazw_lineEdit.setText(s.value("qgis_app2/settings/przestrzenNazw", "/"))


class DokumentyFormularzDialog(CloseMessageDialog, FORM_CLASS4, Formularz, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(DokumentyFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        if s.value("qgis_app2/settings/rodzajZbioru", "/") == 'POG':
            self.setWindowTitle('%s (krok 6 z 7)' % title_app)
        else:
            self.setWindowTitle('%s (krok 5 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.removeForm(container=self.form_scrollArea)
        self.formElements = utils.createFormElementsDokumentFormalny()
        
        self.createForm(container=self.form_scrollArea, formElements=self.formElements)
        
        # schowanie WersjaId dla dokumentu formalnego
        wersjaId_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_lineEdit")
        wersjaId_lineEdit.setVisible(False)
        wersjaId_lbl = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_lbl")
        wersjaId_lbl.setVisible(False)
        wersjaId_tooltip = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_tooltip")
        wersjaId_tooltip.setVisible(False)
        
        # blokada edycji przestrzenNazw
        self.przestrzenNazw_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="przestrzenNazw_lineEdit")
        self.przestrzenNazw_lineEdit.setEnabled(False)
        
        ButtonsDialog.__init__(self)


class GenerowanieGMLDialog(CloseMessageDialog, FORM_CLASS6, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerowanieGMLDialog, self).__init__(parent)
        self.setupUi(self)
        if s.value("qgis_app2/settings/rodzajZbioru", "/") == 'POG':
            self.setWindowTitle('%s (krok 7 z 7)' % title_app)
        else:
            self.setWindowTitle('%s (krok 6 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# dla planu ogólnego gminy

class WektorInstrukcjaDialogSPL(CloseMessageDialog, FORM_CLASS8, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialogSPL, self).__init__(parent)
        self.name = 'StrefaPlanistyczna'
        self.setupUi(self)
        self.setWindowTitle('%s (krok 2 z 7)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)


class WektorInstrukcjaDialogOUZ(CloseMessageDialog, FORM_CLASS9, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialogOUZ, self).__init__(parent)
        self.name = 'ObszarUzupelnieniaZabudowy'
        self.setupUi(self)
        self.setWindowTitle('%s (krok 3 z 7)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)


class WektorInstrukcjaDialogOZS(CloseMessageDialog, FORM_CLASS10, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialogOZS, self).__init__(parent)
        self.name = 'ObszarZabudowySrodmiejskiej'
        self.setupUi(self)
        self.setWindowTitle('%s (krok 4 z 7)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)


class WektorInstrukcjaDialogOSD(CloseMessageDialog, FORM_CLASS11, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialogOSD, self).__init__(parent)
        self.name = 'ObszarStandardowDostepnosciInfrastrukturySpolecznej'
        self.setupUi(self)
        self.setWindowTitle('%s (krok 5 z 7)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)


class WektorInstrukcjaDialogPOG(CloseMessageDialog, FORM_CLASS12, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialogPOG, self).__init__(parent)
        self.name = 'AktPlanowaniaPrzestrzennego'
        self.setupUi(self)
        self.setWindowTitle('%s (krok 1 z 7)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.layers_comboBox.setAllowEmptyLayer(True)
        ButtonsDialog.__init__(self)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# dla planu ogólnego gminy po unieważnieniu

class PytanieAppUniewaznienieDialog(CloseMessageDialog, FORM_CLASS13, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(PytanieAppUniewaznienieDialog, self).__init__(parent)
        self.name = 'PytanieAppUniewaznienieDialog'
        self.setupUi(self)
        self.setWindowTitle(title_app_uniewaznienie)
        self.setWindowIcon(QtGui.QIcon(':/plugins/wtyczka_app/img/praca_z_app_po_uniewaznieniu.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)


class FormularzInstrukcjaDialogPOGpoUniewaznieniu(CloseMessageDialog, FORM_CLASS14, ButtonsDialog):
    def __init__(self, parent=None):
        """Inicjalizuje obiekt klasy `FormularzInstrukcjaDialogPOGpoUniewaznieniu` i konfiguruje jego stan początkowy."""
        super(
            FormularzInstrukcjaDialogPOGpoUniewaznieniu,
            self
        ).__init__(parent)
        
        self.name = 'FormularzInstrukcjaDialogPOGpoUniewaznieniu'
        self.setupUi(self)
        
        self.oznaczenia.setPlaceholderText("np. 123SW, 5OUZ")
        
        self.oznaczenia_validator = QRegExpValidator(
            QRegExp(
                r"^[1-9]\d*(?:SW|SJ|SZ|SU|SH|SP|SR|SI|SN|SC|SG|SO|SK|OSD|OUZ|OZS)"
                r"(?:,\s*[1-9]\d*(?:SW|SJ|SZ|SU|SH|SP|SR|SI|SN|SC|SG|SO|SK|OSD|OUZ|OZS))*$"
            )
        )
        self.oznaczenia.setValidator(self.oznaczenia_validator)
        
        # Tylko warstwy powierzchniowe.
        self.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer
        )
        self.layers_comboBox.setAllowEmptyLayer(True)
        self.layers_comboBox.setCurrentIndex(0)
        
        # Pole daty może zawierać wartość NULL.
        self.obowiazujeOd_data.setAllowNull(True)
        
        # Domyślnie pole daty jest puste.
        self.obowiazujeOd_data.clear()
        
        # Oba pola wyboru obiektów są aktywne.
        self.oznaczenia.setEnabled(True)
        self.layers_comboBox.setEnabled(True)
        
        # Filtr zdarzeń.
        self.oznaczenia.installEventFilter(self)
        self.layers_comboBox.installEventFilter(self)
        
        # Sygnały.
        self.oznaczenia.textChanged.connect(
            self.sprawdz_oznaczenia
        )
        self.layers_comboBox.layerChanged.connect(
            self.sprawdz_oznaczenia
        )
        self.obowiazujeOd_data.valueChanged.connect(
            self.sprawdz_oznaczenia
        )
        
        self.next_btn.setEnabled(False)
        
        self.setWindowTitle(
            '%s (krok 1 z 3)' % title_app_uniewaznienie
        )
        self.setWindowIcon(
            QtGui.QIcon(
                ':/plugins/wtyczka_app/img/praca_z_app_po_uniewaznieniu.png'
            )
        )
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint |
            Qt.WindowSystemMenuHint |
            Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint
        )
        
        ButtonsDialog.__init__(self)
        
        self.sprawdz_oznaczenia()


    def eventFilter(self, obj, event):
        """Filtruje zdarzenia interfejsu i obsługuje zdarzenia wymagające własnej reakcji."""
        if event.type() == QEvent.MouseButtonPress:
            
            # Kliknięto pole oznaczeń -> usuń wybraną warstwę.
            if obj == self.oznaczenia:
                if self.layers_comboBox.currentLayer() is not None:
                    self.layers_comboBox.setCurrentIndex(0)
                    self.sprawdz_oznaczenia()
                    
            # Kliknięto combobox -> wyczyść oznaczenia.
            elif obj == self.layers_comboBox:
                if self.oznaczenia.text().strip():
                    self.oznaczenia.clear()
                    self.sprawdz_oznaczenia()
                    
        return super().eventFilter(obj, event)


    def sprawdz_oznaczenia(self, *args):
        """Wykonuje kontrolę danych w ramach operacji `sprawdz_oznaczenia`."""
        tekst = self.oznaczenia.text().strip()
        warstwa = self.layers_comboBox.currentLayer()
        data_obowiazuje_od = self.obowiazujeOd_data.dateTime()
        
        # Data jest obowiązkowa.
        czy_data_wybrana = (
            data_obowiazuje_od.isValid() and
            not data_obowiazuje_od.isNull()
        )
        
        if not czy_data_wybrana:
            self.next_btn.setEnabled(False)
            return
            
        # Jeżeli wpisano oznaczenia, muszą być zgodne z walidatorem.
        if tekst:
            state, _, _ = self.oznaczenia_validator.validate(
                tekst,
                0
            )
            
            self.next_btn.setEnabled(
                state == self.oznaczenia_validator.Acceptable
            )
            return
        
        # Zamiast oznaczeń można wskazać warstwę.
        if warstwa is not None:
            self.next_btn.setEnabled(True)
            return
            
        # Brak oznaczeń i brak warstwy.
        self.next_btn.setEnabled(False)


class DokumentyFormularzDialogPoUniewaznieniu(CloseMessageDialog, FORM_CLASS15, Formularz, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(DokumentyFormularzDialogPoUniewaznieniu, self).__init__(parent)
        self.setupUi(self)
        if s.value("qgis_app2/settings/rodzajZbioru", "/") == 'POG':
            self.setWindowTitle('%s (krok 2 z 3)' % title_app_uniewaznienie)
        self.setWindowIcon(QtGui.QIcon(icon_path_po_uniewaznieniu))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.removeForm(container=self.form_scrollArea)
        self.formElements = utils.createFormElementsDokumentFormalny()
        
        self.createForm(container=self.form_scrollArea, formElements=self.formElements)
        
        # schowanie WersjaId dla dokumentu formalnego
        wersjaId_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_lineEdit")
        wersjaId_lineEdit.setVisible(False)
        wersjaId_lbl = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_lbl")
        wersjaId_lbl.setVisible(False)
        wersjaId_tooltip = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="wersjaId_tooltip")
        wersjaId_tooltip.setVisible(False)
        
        # blokada edycji przestrzenNazw
        self.przestrzenNazw_lineEdit = utils.layout_widget_by_name(self.form_scrollArea.widget().layout(), name="przestrzenNazw_lineEdit")
        self.przestrzenNazw_lineEdit.setEnabled(False)
        
        self.getValues_btn.setVisible(False)
        
        ButtonsDialog.__init__(self)


class GenerowanieGMLDialogPoUniewaznieniu(CloseMessageDialog, FORM_CLASS16, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerowanieGMLDialogPoUniewaznieniu, self).__init__(parent)
        self.setupUi(self)
        if s.value("qgis_app2/settings/rodzajZbioru", "/") == 'POG':
            self.setWindowTitle('%s (krok 3 z 3)' % title_app_uniewaznienie)
        self.setWindowIcon(QtGui.QIcon(icon_path_po_uniewaznieniu))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)