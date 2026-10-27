# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)
from qgis.core import (
    QgsCoordinateTransformContext,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsProject,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsWkbTypes,
)


class DokumentDialog(QDialog):
    """Okno tworzenia / aktualizacji GML dla dokumentu do repozytorium."""

    def __init__(self, iface, parent=None):
        """Inicjalizuje obiekt klasy `DokumentDialog` i konfiguruje jego stan początkowy."""
        super().__init__(parent)
        self.iface = iface
        self.loaded_layer = None
        
        self.setWindowTitle("Tworzenie / aktualizacja GML dla dokumentu do repozytorium")
        self.resize(720, 360)
        
        self._connect_signals()
        self.refresh_layers()
        self._update_mode()

    def _connect_signals(self):
        """Realizuje operację `_connect_signals` w bieżącym module."""
        self.refresh_btn.clicked.connect(self.refresh_layers)
        self.browse_file_btn.clicked.connect(self.load_layer_from_file)
        self.output_btn.clicked.connect(self.choose_output_file)
        self.save_btn.clicked.connect(self.save_gml)
        self.close_btn.clicked.connect(self.close)

        self.project_layer_radio.toggled.connect(self._update_mode)
        self.load_file_radio.toggled.connect(self._update_mode)
        self.empty_layer_radio.toggled.connect(self._update_mode)

    def _update_mode(self):
        """Realizuje operację `_update_mode` w bieżącym module."""
        project_mode = self.project_layer_radio.isChecked()
        file_mode = self.load_file_radio.isChecked()

        self.layer_combo.setEnabled(project_mode)
        self.refresh_btn.setEnabled(project_mode)
        self.file_path_edit.setEnabled(file_mode)
        self.browse_file_btn.setEnabled(file_mode)

    def refresh_layers(self):
        """Realizuje operację `refresh_layers` w bieżącym module."""
        self.layer_combo.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsVectorLayer) and layer.isValid():
                self.layer_combo.addItem(layer.name(), layer.id())

    def load_layer_from_file(self):
        """Wczytuje dane obsługiwane przez operację `load_layer_from_file`."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Wczytaj warstwę dokumentu APP",
            "",
            "Pliki wektorowe (*.gml *.xml *.gpkg *.shp);;Wszystkie pliki (*.*)",
        )
        if not path:
            return

        layer = QgsVectorLayer(path, os.path.basename(path), "ogr")
        if not layer.isValid():
            QMessageBox.warning(self, "Wczytywanie warstwy", "Nie udało się wczytać wybranego pliku jako warstwy wektorowej.")
            return

        self.loaded_layer = layer
        QgsProject.instance().addMapLayer(layer)
        self.file_path_edit.setText(path)

    def choose_output_file(self):
        """Realizuje operację `choose_output_file` w bieżącym module."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz dokument do repozytorium do GML",
            "dokument_zbioru_app.gml",
            "GML (*.gml)",
        )
        if not path:
            return
        if not path.lower().endswith(".gml"):
            path += ".gml"
        self.output_path_edit.setText(path)

    def _selected_layer(self):
        """Zwraca wynik operacji `_selected_layer` wykonywanej w bieżącym module."""
        if self.project_layer_radio.isChecked():
            layer_id = self.layer_combo.currentData()
            return QgsProject.instance().mapLayer(layer_id) if layer_id else None

        if self.load_file_radio.isChecked():
            return self.loaded_layer

        if self.empty_layer_radio.isChecked():
            return self._create_empty_document_layer()

        return None

    def _create_empty_document_layer(self):
        """Zwraca wynik operacji `_create_empty_document_layer` wykonywanej w bieżącym module."""
        layer = QgsVectorLayer("NoGeometry?crs=EPSG:2180", "Dokument_zbioru_APP", "memory")
        provider = layer.dataProvider()
        provider.addAttributes([
            QgsField("identyfikatorDokumentu", QVariant.String, len=255),
        ])
        layer.updateFields()
        return layer

    def _ensure_document_id(self, layer, document_id):
        """Dopisuje/aktualizuje pole identyfikatorDokumentu w wybranej warstwie."""
        if layer is None or not layer.isValid():
            return None

        # Pracujemy na kopii pamięciowej, aby nie modyfikować oryginalnej warstwy użytkownika.
        geometry_name = QgsWkbTypes.displayString(layer.wkbType())
        if layer.wkbType() == QgsWkbTypes.NoGeometry:
            uri = "NoGeometry?crs={}".format(layer.crs().authid() or "EPSG:2180")
        else:
            uri = "{}?crs={}".format(geometry_name, layer.crs().authid() or "EPSG:2180")

        out_layer = QgsVectorLayer(uri, "Dokument_zbioru_APP_GML", "memory")
        out_provider = out_layer.dataProvider()

        fields = QgsFields(layer.fields())
        if fields.indexFromName("identyfikatorDokumentu") == -1:
            fields.append(QgsField("identyfikatorDokumentu", QVariant.String, len=255))

        out_provider.addAttributes(list(fields))
        out_layer.updateFields()

        source_features = list(layer.getFeatures())
        if not source_features:
            source_features = [QgsFeature(layer.fields())]

        id_index = out_layer.fields().indexFromName("identyfikatorDokumentu")
        new_features = []
        for source_feature in source_features:
            new_feature = QgsFeature(out_layer.fields())
            if layer.wkbType() != QgsWkbTypes.NoGeometry and source_feature.hasGeometry():
                new_feature.setGeometry(source_feature.geometry())

            attrs = []
            for field in out_layer.fields():
                name = field.name()
                if name == "identyfikatorDokumentu":
                    attrs.append(document_id)
                elif layer.fields().indexFromName(name) != -1:
                    attrs.append(source_feature[name])
                else:
                    attrs.append(None)
            new_feature.setAttributes(attrs)
            new_features.append(new_feature)

        out_provider.addFeatures(new_features)
        out_layer.updateExtents()
        return out_layer

    def save_gml(self):
        """Zapisuje przygotowane dane dokumentu do pliku GML."""
        document_id = self.document_id_edit.text().strip()
        output_path = self.output_path_edit.text().strip()

        if not document_id:
            QMessageBox.warning(self, "Brak danych", "Podaj identyfikator dokumentu.")
            return

        if not output_path:
            QMessageBox.warning(self, "Brak pliku", "Wybierz plik wynikowy GML.")
            return

        layer = self._selected_layer()
        if layer is None or not layer.isValid():
            QMessageBox.warning(self, "Brak warstwy", "Wybierz, wczytaj albo utwórz warstwę dokumentu.")
            return

        out_layer = self._ensure_document_id(layer, document_id)
        if out_layer is None or not out_layer.isValid():
            QMessageBox.critical(self, "Błąd", "Nie udało się przygotować warstwy do zapisu.")
            return

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GML"
        options.fileEncoding = "UTF-8"
        options.layerName = "DokumentZbioruAPP"
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

        result = QgsVectorFileWriter.writeAsVectorFormatV3(
            out_layer,
            output_path,
            QgsCoordinateTransformContext(),
            options,
        )

        # QGIS 3.34+ zwraca krotkę: (error_code, error_message, new_file, new_layer)
        error_code = result[0] if isinstance(result, tuple) else result
        error_message = result[1] if isinstance(result, tuple) and len(result) > 1 else ""

        if error_code == QgsVectorFileWriter.NoError:
            QMessageBox.information(self, "Zapis GML", "Zapisano plik GML:\n{}".format(output_path))
        else:
            QMessageBox.critical(self, "Błąd zapisu GML", "Nie udało się zapisać pliku GML.\n{}".format(error_message))
