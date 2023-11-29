# -*- coding: utf-8 -*-
from .. import utils
from qgis.core import *
from qgis import processing
from ..utils import showPopup


def isLayerInPoland(obrysLayer):
    """sprawdza czy geometria obrysu jest poprawna"""
    # definicja transformacji układu
    layerCrs = obrysLayer.sourceCrs()  # z warstwy
    crs4258 = QgsCoordinateReferenceSystem(4258)  # ETRS89
    transform = QgsCoordinateTransform(crs4258, layerCrs, QgsProject.instance())
    czyGeometrieSaPoprawne = True
    granicaPolskiSHP = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/app/A00_Granice_panstwa/A00_Granice_panstwa.shp"
    warstwaGranicaPolski = QgsVectorLayer(granicaPolskiSHP, 'A00_Granice_panstwa', 'ogr')
    geom_poland = next(warstwaGranicaPolski.getFeatures()).geometry().transform(transform)
    
    # geometria wychodzi poza granicę Polski
    przyciecie = processing.run("qgis:difference", {
        'INPUT': obrysLayer,
        'OVERLAY': warstwaGranicaPolski,
        'OUTPUT': 'memory:'
    })
    
    # rozbicie multipoligon-u na poligony
    pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
        'INPUT': przyciecie['OUTPUT'],
        'OUTPUT': 'memory:'
    })
    
    #kasowanie obiektów wychodzących poza POG o powierzchni < 1m2
    pojedynczeObjekty['OUTPUT'].startEditing()
    for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
        if obj.geometry().area() < 1:
            pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
    pojedynczeObjekty['OUTPUT'].commitChanges(False)
    
    if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
        pojedynczeObjekty['OUTPUT'].setName("Geometrie wychodzace poza granice Polski")
        QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
        showPopup("Błąd warstwy obrysu",
                  "Niepoprawna geometria - obiekty muszą leżeć wewnątrz granicy Polski. Dodano warstwę z geometriami wychodzącymi poza granicę Polski.")
        czyGeometrieSaPoprawne = False
    
    return czyGeometrieSaPoprawne

