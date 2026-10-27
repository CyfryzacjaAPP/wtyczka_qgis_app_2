# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timezone

from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
    QgsMapLayerProxyModel,
    QgsGeometry,
    QgsVectorFileWriter,
    QgsSettings
)

from .. import BaseModule
from ..app.app_utils import isLayerInPoland
from .dialogs import DokumentDialog

import os
import tempfile
import xml.etree.ElementTree as ET  # nosec B405
from html import escape as xml_escape



class DokumentModule(BaseModule):
    """Moduł: Tworzenie pliku GML dla dokumentu Repozytorium"""
    
    def __init__(self, iface):
        """Inicjalizuje obiekt klasy `DokumentModule` i konfiguruje jego stan początkowy."""
        self.iface = iface
        self.dokumentDialog = DokumentDialog()
        
        self.dokumentDialog.localId.setPlaceholderText("np. VII.123.2024")
        
        self.dokumentDialog.layers_comboBox.setFilters(
            QgsMapLayerProxyModel.PolygonLayer
        )
        
        self.dokumentDialog.generateTemporaryLayer_btn.clicked.connect(
            self.generateTemporaryLayer_btn_clicked
        )
        self.dokumentDialog.loadLayerEdit.clicked.connect(
            self.loadLayerEdit_clicked
        )
        self.dokumentDialog.saveLayer.clicked.connect(
            self.saveLayer_clicked
        )
        
        s = QgsSettings()
        self.defaultPath = s.value("qgis_app2/settings/defaultPath", "/")


    def generateTemporaryLayer_btn_clicked(self):
        """Tworzy pustą warstwę GPKG do geometrii dokumentu."""
            
        try:
            os.makedirs(self.defaultPath, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            gpkg_path = os.path.join(
                self.defaultPath,
                f"geometria_dokumentu_APP_{timestamp}.gpkg"
            )
            
            layer_name = "Geometria_dokumentu_APP"
            
            layer = QgsVectorLayer(
                "MultiPolygon?crs=EPSG:2180",
                layer_name,
                "memory"
            )
            
            if not layer.isValid():
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd",
                    "Nie udało się utworzyć pustej warstwy."
                )
                return
            
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "GPKG"
            options.layerName = layer_name
            options.fileEncoding = "UTF-8"
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            
            result = QgsVectorFileWriter.writeAsVectorFormatV3(
                layer,
                gpkg_path,
                QgsProject.instance().transformContext(),
                options
            )
            
            if result[0] != QgsVectorFileWriter.NoError:
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd zapisu GPKG",
                    f"Nie udało się zapisać warstwy GPKG:\n{result[1]}"
                )
                return
            
            gpkg_layer = QgsVectorLayer(
                f"{gpkg_path}|layername={layer_name}",
                layer_name,
                "ogr"
            )
            
            if not gpkg_layer.isValid():
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd wczytania GPKG",
                    "Plik GPKG został utworzony, ale nie udało się go wczytać do QGIS."
                )
                return
            
            QgsProject.instance().addMapLayer(gpkg_layer)
            self.dokumentDialog.layers_comboBox.setLayer(gpkg_layer)
            
            QMessageBox.information(
                self.dokumentDialog,
                "Utworzono warstwę",
                f"Utworzono warstwę 'Geometria_dokumentu_APP' do edycji przestrzennej reprezentacji (zasięgu) dokumentu."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.dokumentDialog,
                "Błąd",
                str(e)
            )


    def loadLayerEdit_clicked(self):
        """Wczytuje GML, pobiera lokalnyIdDokumentu i konwertuje warstwę do GPKG."""
        
        gml_path, _ = QFileDialog.getOpenFileName(
            self.dokumentDialog,
            "Wskaż plik GML dokumentu",
            self.defaultPath,
            "GML (*.gml *.xml)"
        )
        
        if not gml_path:
            return
                
        try:
            tree = ET.parse(gml_path)  # nosec B314
            root = tree.getroot()
            
            local_id = None
            
            for elem in root.iter():
                if elem.tag.endswith("lokalnyIdDokumentu"):
                    local_id = elem.text
                    break
                    
            if local_id:
                self.dokumentDialog.localId.setText(local_id.strip())
            else:
                QMessageBox.warning(
                    self.dokumentDialog,
                    "Brak identyfikatora",
                    "Nie znaleziono elementu lokalnyIdDokumentu w pliku GML."
                )
            
            # 2. Wczytanie GML jako warstwa QGIS
            layer_name = os.path.splitext(os.path.basename(gml_path))[0]
            
            gml_layer = QgsVectorLayer(
                gml_path,
                layer_name,
                "ogr"
            )
            
            if not gml_layer.isValid():
                gml_layer = QgsVectorLayer(
                    gml_path + "|layername=LokalizacjaDokumentu",
                    layer_name,
                    "ogr"
                )
            
            if not gml_layer.isValid():
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd wczytania",
                    "Nie udało się wczytać pliku GML jako warstwy."
                )
                return
            
            if QgsWkbTypes.geometryType(gml_layer.wkbType()) != QgsWkbTypes.PolygonGeometry:
                QMessageBox.warning(
                    self.dokumentDialog,
                    "Nieprawidłowa geometria",
                    "Wczytany plik GML nie zawiera warstwy poligonowej."
                )
                return
            
            # 3. Zapis do tymczasowego GPKG
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            gpkg_path = os.path.join(
                tempfile.gettempdir(),
                f"{layer_name}_{timestamp}.gpkg"
            )
            
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "GPKG"
            options.layerName = "LokalizacjaDokumentu"
            options.fileEncoding = "UTF-8"
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
            
            result = QgsVectorFileWriter.writeAsVectorFormatV3(
                gml_layer,
                gpkg_path,
                QgsProject.instance().transformContext(),
                options
            )
            
            if result[0] != QgsVectorFileWriter.NoError:
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd zapisu GPKG",
                    f"Nie udało się zapisać warstwy do GPKG:\n{result[1]}"
                )
                return
            
            # 4. Wczytanie GPKG do projektu QGIS
            gpkg_layer = QgsVectorLayer(
                f"{gpkg_path}|layername=LokalizacjaDokumentu",
                layer_name,
                "ogr"
            )
            
            if not gpkg_layer.isValid():
                QMessageBox.critical(
                    self.dokumentDialog,
                    "Błąd wczytania GPKG",
                    "Plik GPKG został utworzony, ale nie udało się go wczytać do QGIS."
                )
                return
            
            QgsProject.instance().addMapLayer(gpkg_layer)
            
            # ustaw warstwę jako wybraną w QgsMapLayerComboBox
            self.dokumentDialog.layers_comboBox.setLayer(gpkg_layer)
            
            QMessageBox.information(
                self.dokumentDialog,
                "Wczytano GML",
                "Plik GML został wczytany, przekonwertowany do GPKG i dodany do projektu."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.dokumentDialog,
                "Błąd",
                str(e)
            )


    def saveLayer_clicked(self):
        """Zapisuje dane obsługiwane przez operację `saveLayer_clicked`."""
        lokalny_id = self.dokumentDialog.localId.text().strip()
        
        if not lokalny_id:
            QMessageBox.warning(
                self.dokumentDialog,
                "Brak identyfikatora",
                "Wpisz identyfikator lokalny dokumentu."
            )
            self.dokumentDialog.localId.setFocus()
            return
        
        layer = self.dokumentDialog.layers_comboBox.currentLayer()
        
        if layer is None:
            QMessageBox.warning(
                self.dokumentDialog,
                "Brak warstwy",
                "Wybierz warstwę z geometrią dokumentu."
            )
            self.dokumentDialog.layers_comboBox.setFocus()
            return
            
        if not layer.isValid():
            QMessageBox.warning(
                self.dokumentDialog,
                "Nieprawidłowa warstwa",
                "Wybrana warstwa jest nieprawidłowa."
            )
            return
            
        if QgsWkbTypes.geometryType(layer.wkbType()) != QgsWkbTypes.PolygonGeometry:
            QMessageBox.warning(
                self.dokumentDialog,
                "Nieprawidłowa geometria",
                "Warstwa musi być warstwą poligonową."
            )
            return
            
        polygon_features = []
        
        for feat in layer.getFeatures():
            geom = feat.geometry()
            
            if geom and not geom.isEmpty():
                if QgsWkbTypes.geometryType(geom.wkbType()) == QgsWkbTypes.PolygonGeometry:
                    polygon_features.append(feat)
                    
        if len(polygon_features) == 0:
            QMessageBox.warning(
                self.dokumentDialog,
                "Brak geometrii",
                "Warstwa musi zawierać co najmniej jeden obiekt poligonowy lub multipoligonowy."
            )
            return
        
        # Czy geometria wychodzi poza granicę Polski
        if not isLayerInPoland(layer, layer.name()):
            return
        
        path, _ = QFileDialog.getSaveFileName(
            self.dokumentDialog,
            "Zapisz dokument GML",
            self.defaultPath,
            "",
            "GML (*.gml)"
        )
        
        if not path:
            return
            
        if not path.lower().endswith(".gml"):
            path += ".gml"
            
        try:
            gml = self.build_gml(
                lokalny_id=lokalny_id,
                layer=layer,
                features=polygon_features
            )
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(gml)
                
            QMessageBox.information(
                self.dokumentDialog,
                "Zapisano",
                "Dokument GML został zapisany poprawnie."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.dokumentDialog,
                "Błąd zapisu",
                str(e)
            )


    def build_gml(self, lokalny_id, layer, features):
        """Buduje dokument GML na podstawie przekazanych danych i geometrii."""
        epsg = layer.crs().postgisSrid()
    
        if not epsg or epsg <= 0:
            epsg = 2180
    
        srs_name = f"http://www.opengis.net/def/crs/EPSG/0/{epsg}"
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        surface_members = []
    
        for feat in features:
            geom = QgsGeometry(feat.geometry())
    
            surface_member = self.geometry_to_surface_member(
                geom
            )
    
            if surface_member:
                surface_members.append(
                    self.indent_xml_block(
                        surface_member,
                        4
                    )
                )
    
        surface_members_xml = "\n".join(surface_members)
    
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<wfs:FeatureCollection '
            'xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:ru="https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/ru/1.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'numberMatched="unknown" '
            'numberReturned="1" '
            f'timeStamp="{timestamp}" '
            'xsi:schemaLocation="'
            'http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd '
            'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/ru/1.0 '
            'https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/ru/1.0/rejestrUrbanistyczny.xsd'
            '">\n'
            '\t<wfs:member>\n'
            '\t\t<ru:LokalizacjaDokumentu gml:id="ID-1">\n'
            f'\t\t\t<ru:lokalnyIdDokumentu>'
            f'{xml_escape(str(lokalny_id), quote=False)}'
            f'</ru:lokalnyIdDokumentu>\n'
            '\t\t\t<ru:geometria>\n'
            f'\t\t\t\t<gml:MultiSurface '
            f'srsName="{srs_name}" '
            f'srsDimension="2">\n'
            f'{surface_members_xml}\n'
            '\t\t\t\t</gml:MultiSurface>\n'
            '\t\t\t</ru:geometria>\n'
            '\t\t</ru:LokalizacjaDokumentu>\n'
            '\t</wfs:member>\n'
            '</wfs:FeatureCollection>\n'
        )


    def indent_xml_block(self, xml, level):
        """Formatuje blok XML przez ustawienie odpowiednich wcięć."""
        indent = "\t" * level
    
        return "\n".join(
            f"{indent}{line}"
            for line in xml.splitlines()
            if line.strip()
        )


    def geometry_to_surface_member(self, geom):
        """Konwertuje geometrię do elementu `surfaceMember` zapisywanego w GML."""
        if geom.isMultipart():
            polygons = geom.asMultiPolygon()
        else:
            polygons = [geom.asPolygon()]
    
        result = []
    
        for polygon in polygons:
            if not polygon:
                continue
    
            polygon_id = f"ID_{uuid4().hex}"
    
            exterior_ring = polygon[0]
            interior_rings = polygon[1:]
    
            lines = [
                "<gml:surfaceMember>",
                f'\t<gml:Polygon gml:id="{polygon_id}">',
                "\t\t<gml:exterior>",
                "\t\t\t<gml:LinearRing>",
                (
                    "\t\t\t\t<gml:posList>"
                    f"{self.ring_to_poslist(exterior_ring)}"
                    "</gml:posList>"
                ),
                "\t\t\t</gml:LinearRing>",
                "\t\t</gml:exterior>",
            ]
    
            for ring in interior_rings:
                lines.extend([
                    "\t\t<gml:interior>",
                    "\t\t\t<gml:LinearRing>",
                    (
                        "\t\t\t\t<gml:posList>"
                        f"{self.ring_to_poslist(ring)}"
                        "</gml:posList>"
                    ),
                    "\t\t\t</gml:LinearRing>",
                    "\t\t</gml:interior>",
                ])
    
            lines.extend([
                "\t</gml:Polygon>",
                "</gml:surfaceMember>",
            ])
    
            result.append(
                "\n".join(lines)
            )
    
        return "\n".join(result)


    def ring_to_poslist(self, ring):
        """Konwertuje pierścień geometrii do listy współrzędnych `posList`."""
        coords = []
        
        for point in ring:
            coords.append(f"{point.y()} {point.x()}")
            
        return " ".join(coords)