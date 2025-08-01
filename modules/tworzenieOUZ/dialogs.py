# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu Metadata
 ***************************************************************************/
"""

import os
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from qgis.PyQt import QtWidgets
from ..base_dialogs import CloseMessageDialog, ButtonsDialog
from qgis.core import *
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout


title = 'Wyznaczanie OUZ'
icon = ':/plugins/wtyczka_app/img/tworzenieOUZ.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'views', 'ui', 'tworzenieOUZ.ui'))


class TworzenieOUZDialog(CloseMessageDialog, FORM_CLASS, ButtonsDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(TworzenieOUZDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        ButtonsDialog.__init__(self)
        self.closed.connect(self.wylaczenieKonektorow)
        self.cancel.rejected.connect(self.wylaczenieKonektorow)
        global pierwszyKomunikat_Bud, pierwszyKomunikat_POG

    def wlaczenieKonektorow(self):
        global pierwszyKomunikat_Bud, pierwszyKomunikat_POG
        pierwszyKomunikat_Bud = True
        pierwszyKomunikat_POG = True
        self.warstwaBudynki.currentTextChanged.connect(self.warstwa_Budynki)
        self.warstwaPOG.currentTextChanged.connect(self.warstwa_POG)

    def wylaczenieKonektorow(self):
        try:
            self.warstwaBudynki.currentTextChanged.disconnect()
            self.warstwaPOG.currentTextChanged.disconnect()
        except Exception as e:
            QgsMessageLog.logMessage(f"Błąd:{str(e)}", 'APP2')

    def warstwa_Budynki(self):
        global pierwszyKomunikat_Bud
        self.tworzenie_btn.setEnabled(False)
        cl_Bud = self.warstwaBudynki.currentLayer()
        try:
            if isinstance(cl_Bud, QgsVectorLayer):
                if cl_Bud != None and \
                    not cl_Bud.name().__contains__("AktPlanowaniaPrzestrzennego") and \
                    not cl_Bud.name().__contains__("StrefaPlanistyczna") and \
                    not cl_Bud.name().__contains__("ObszarZabudowySrodmiejskiej") and \
                    not cl_Bud.name().__contains__("ObszarStandardowDostepnosciInfrastrukturySpolecznej") and \
                    not cl_Bud.name().__contains__("ObszarUzupelnieniaZabudowy") and \
                    cl_Bud.geometryType() == QgsWkbTypes.PolygonGeometry and \
                    cl_Bud.featureCount() >= 5 and \
                    cl_Bud.crs().authid() != "":
                    if self.warstwaPOG.currentLayer() != None:
                        self.tworzenie_btn.setEnabled(True)
                    pierwszyKomunikat_Bud = False
                    return
                else:
                    vectorLayers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.type() == QgsMapLayer.VectorLayer]
                    # komunikaty bledów
                    if not pierwszyKomunikat_Bud:
                        if cl_Bud.name().__contains__("AktPlanowaniaPrzestrzennego"):
                            l_b = False
                            for vl in vectorLayers:
                                if not vl.name().__contains__("AktPlanowaniaPrzestrzennego"):
                                    l_b = True
                                    break
                            if not l_b:
                                QMessageBox.critical(None,'Informacja','Wybrano warstwę AktPlanowaniaPrzestrzennego. Należy wybrać warstwę z budynkami.')
                        elif cl_Bud.name().__contains__("StrefaPlanistyczna"):
                            l_b = False
                            for vl in vectorLayers:
                                if not vl.name().__contains__("StrefaPlanistyczna"):
                                    l_b = True
                                    break
                            if not l_b:
                                QMessageBox.critical(None,'Informacja','Wybrano warstwę StrefaPlanistyczna. Należy wybrać warstwę z budynkami.')
                        elif cl_Bud.name().__contains__("ObszarZabudowySrodmiejskiej"):
                            l_b = False
                            for vl in vectorLayers:
                                if not vl.name().__contains__("ObszarZabudowySrodmiejskiej"):
                                    l_b = True
                                    break
                            if not l_b:
                                QMessageBox.critical(None,'Informacja','Wybrano warstwę ObszarZabudowySrodmiejskiej. Należy wybrać warstwę z budynkami.')
                        elif cl_Bud.name().__contains__("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
                            l_b = False
                            for vl in vectorLayers:
                                if not vl.name().__contains__("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
                                    l_b = True
                                    break
                            if not l_b:
                                QMessageBox.critical(None,'Informacja','Wybrano warstwę ObszarStandardowDostepnosciInfrastrukturySpolecznej. Należy wybrać warstwę z budynkami.')
                        elif cl_Bud.name().__contains__("ObszarUzupelnieniaZabudowy"):
                            l_b = False
                            for vl in vectorLayers:
                                if not vl.name().__contains__("ObszarUzupelnieniaZabudowy"):
                                    l_b = True
                                    break
                            if not l_b:
                                QMessageBox.critical(None,'Informacja','Wybrano warstwę ObszarUzupelnieniaZabudowy. Należy wybrać warstwę z budynkami.')
                        elif cl_Bud.geometryType() != QgsWkbTypes.PolygonGeometry:
                            QMessageBox.critical(None,'Informacja','Warstwa musi przechowywać obiekty typu poligon.')
                        elif cl_Bud.featureCount() < 5:
                            QMessageBox.critical(None,'Informacja','Warstwa musi zawierać co najmniej 5 obiektów.')
                        elif cl_Bud.crs().authid():
                            QMessageBox.critical(None,'Informacja','Warstwa musi mieć zdefiniowany układ współrzędnych.')
                    
                    for layer in vectorLayers:
                        if not layer.name().__contains__("AktPlanowaniaPrzestrzennego") and \
                            not layer.name().__contains__("StrefaPlanistyczna") and \
                            not layer.name().__contains__("ObszarZabudowySrodmiejskiej") and \
                            not layer.name().__contains__("ObszarStandardowDostepnosciInfrastrukturySpolecznej") and \
                            not layer.name().__contains__("ObszarUzupelnieniaZabudowy") and \
                            layer.geometryType() == QgsWkbTypes.PolygonGeometry and \
                            layer.featureCount() >= 5 and \
                            layer.crs().authid() != "":
                            self.warstwaBudynki.setLayer(layer)
                            break
                        else:
                            self.warstwaBudynki.setLayer(None)
            else:
                self.warstwaBudynki.setLayer(None)
        except Exception as e:
            QgsMessageLog.logMessage(f"Błąd:{str(e)}", 'APP2')


    def warstwa_POG(self):
        global pierwszyKomunikat_POG
        cl_POG = self.warstwaPOG.currentLayer()
        if isinstance(cl_POG, QgsVectorLayer):
            if cl_POG != None and \
               cl_POG.name().__contains__("AktPlanowaniaPrzestrzennego") and \
               cl_POG.geometryType() == QgsWkbTypes.PolygonGeometry and \
               cl_POG.featureCount() == 1 and \
               cl_POG.crs().authid() != "" and \
               cl_POG.fields().names().__contains__("obowiazujeOd"):
                pierwszyKomunikat_POG = False
                return
            else:
                vectorLayers = [layer for layer in QgsProject.instance().mapLayers().values() if layer.type() == QgsMapLayer.VectorLayer]
                # komunikaty bledów
                if not pierwszyKomunikat_POG:
                    if not cl_POG.name().__contains__("AktPlanowaniaPrzestrzennego"):
                        l_b = False
                        for vl in vectorLayers:
                            if vl.name().__contains__("AktPlanowaniaPrzestrzennego"):
                                l_b = True
                                break
                        if not l_b:
                            QMessageBox.critical(None,'Informacja','Warstwa wejściowa ma nieodpowiednią nazwę. Prawidłowa nazwa powinna zaczynać się od „AktPlanowaniaPrzestrzennego”.')
                    elif cl_POG.geometryType() != QgsWkbTypes.PolygonGeometry:
                        QMessageBox.critical(None,'Informacja','Warstwa musi przechowywać obiekt typu multipoligon.')
                    elif cl_POG.featureCount() == 0:
                        QMessageBox.critical(None,'Informacja','Warstwa musi posiadać jeden obiekt.')
                    elif cl_POG.crs().authid() == "":
                        QMessageBox.critical(None,'Informacja','Warstwa musi mieć zdefiniowany układ współrzędnych.')
                    elif not (cl_POG.fields().names().__contains__("status") and cl_POG.fields().names().__contains__("obowiazujeOd")):
                        QMessageBox.critical(None,'Informacja','Warstwa wejściowa ma nieodpowiednią strukturę.')
                
                pierwszyKomunikat_POG = False
                for layer in vectorLayers:
                    if layer.name().__contains__("AktPlanowaniaPrzestrzennego") and \
                       layer.geometryType() == QgsWkbTypes.PolygonGeometry and \
                       layer.featureCount() == 1 and \
                       layer.crs().authid() != "" and \
                       layer.fields().names().__contains__("obowiazujeOd"):
                        self.warstwaPOG.setLayer(layer)
                        break
                    else:
                        self.warstwaPOG.setLayer(None)
        else:
            self.warstwaPOG.setLayer(None)