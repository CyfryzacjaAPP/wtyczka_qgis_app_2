# -*- coding: utf-8 -*-
from .. import utils
from qgis.core import *
from qgis import processing
from ..utils import showPopup
from PyQt5.QtCore import QVariant



def isLayerInPoland(obrysLayer, layerName):
    crs2180 = QgsCoordinateReferenceSystem("EPSG:2180")
    granicaPolskiSHP = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/app/A00_Granice_panstwa/A00_Granice_panstwa_bufor_300m.shp"
    warstwaGranicaPolski = QgsVectorLayer(granicaPolskiSHP, 'A00_Granice_panstwa', 'ogr')
    
    # transformacja do układu granic Państwa
    reprojectlayer = processing.run("native:reprojectlayer", {
        'INPUT': obrysLayer,
        'TARGET_CRS': crs2180,
        'OUTPUT': 'memory:'
    })
    
    extractbyexpression = processing.run("qgis:extractbyexpression", {
        'INPUT': reprojectlayer['OUTPUT'],
        'EXPRESSION': '$area != 0',
        'OUTPUT': 'memory:'
    })
    
    if reprojectlayer['OUTPUT'].featureCount() - extractbyexpression['OUTPUT'].featureCount() > 0:
        showPopup("Wczytaj warstwę",f"Warstwa \"{layerName}\" posiada co najmniej jeden obiekt z pustą geometrią. Kontynuuję wczytywanie.")
    
    # geometria wychodzi poza granicę Polski
    przyciecie = processing.run("qgis:difference", {
        'INPUT': extractbyexpression['OUTPUT'],
        'OVERLAY': warstwaGranicaPolski,
        'OUTPUT': 'memory:'
    })
    
    # rozbicie multipoligon-u na poligony
    pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
        'INPUT': przyciecie['OUTPUT'],
        'OUTPUT': 'memory:'
    })
    
    # usuwanie obiektow o powierzchni < 1 m2
    pojedynczeObjekty['OUTPUT'].startEditing()
    for obj in pojedynczeObjekty['OUTPUT'].getFeatures():
        if obj.geometry().area() < 1: # 1 m2
            pojedynczeObjekty['OUTPUT'].deleteFeature(obj.id())
    pojedynczeObjekty['OUTPUT'].commitChanges(False)
    
    if pojedynczeObjekty['OUTPUT'].featureCount() > 0:
        pojedynczeObjekty['OUTPUT'].setName("Geometrie wychodzace poza granice Polski")
        QgsProject.instance().addMapLayer(pojedynczeObjekty['OUTPUT'])
        showPopup("Błąd warstwy obrysu","Niepoprawna geometria - obiekty muszą leżeć wewnątrz granicy Polski.\nDodano warstwę z geometriami wychodzącymi poza granicę Polski.")
        return False
    
    return True


def czyWarstwaMaWypelnioneObowiazkoweAtrybuty(obrysLayer):
    if obrysLayer.name().startswith("AktPlanowaniaPrzestrzennego"):
        sql = "tytul='' or typPlanu='' or poziomHierarchii='' or status='' or obowiazujeOd is null or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu=''"
    elif obrysLayer.name().startswith("StrefaPlanistyczna"):
        sql = "nazwa='' or symbol='' or oznaczenie='' or profilPodstawowy='' or status='' or obowiazujeOd is null or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu=''"
    elif obrysLayer.name().startswith("ObszarUzupelnieniaZabudowy"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd is null or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu=''"
    elif obrysLayer.name().startswith("ObszarZabudowySrodmiejskiej"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd is null or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu=''"
    elif obrysLayer.name().startswith("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd is null or charakterUstalenia='' or odlegloscDoSzkolyPodstawowej='' or odlegloscDoObszarowZieleniPublicznej='' or powierzchniaLacznaObszarowZieleniPublicznej='' or odlegloscDoObszaruZieleniPublicznej='' or powierzchniaObszaruZieleniPublicznej='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu=''"
    else:
        sql=""
    
    request = QgsFeatureRequest(QgsExpression(sql))
    requestFeatures = obrysLayer.getFeatures(request)
    for x in requestFeatures:
        return False
    return True


def kontrolaZaleznosciAtrybutow(obrysLayer):
    czyWystepujaBledy = False
    fields = QgsFields(obrysLayer.fields())
    new_field = QgsField('Opis_bledu', QVariant.String)
    fields.append(new_field)
    
    layer = QgsVectorLayer('Polygon?crs=' + obrysLayer.crs().toWkt(), obrysLayer.name() + " - bledy w atrybutach", "memory")
    layer_data_provider = layer.dataProvider()
    layer_data_provider.addAttributes(fields)
    layer.updateFields()
    
    if obrysLayer.name().startswith("AktPlanowaniaPrzestrzennego"):
        expressions = {
                       "if(typPlanu<>'plan ogólny gminy',1,0)":"Atrybut 'typ palnu' musi wynosić 'plan ogólny gminy'",
                       "if(regexp_match(lokalnyId,'\\d+POG'),0,1)":"Błędny identyfikator lokalny",
                       "if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       "if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       "if(length(tytul)<=12,1,0)":"Należy wpisać nazwę po słowach 'Plan ogólny'",
                       "if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       "if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("StrefaPlanistyczna"):
        expressions = {
                       "if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       "if(regexp_match(lokalnyId,'\\d+POG-\\d+S[CGHIJKNOPRUWZ]'),0,1)":"Błędny identyfikator lokalny",
                       "if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       "if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       "if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksNadziemnaIntensywnoscZabudowy is null,1,0)":"Należy uzupełnić maksymalną nadziemną intensywność zabudowy",
                       "if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksUdzialPowierzchniZabudowy is null,1,0)":"Należy uzupełnić maksymalny udział powierzchni zabudowy",
                       "if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksWysokoscZabudowy is null,1,0)":"Należy uzupełnić maksymalną wysokość zabudowy",
                       "if(symbol in ('SG','SO','SK') and (minUdzialPowierzchniBiologicznieCzynnej<0 or minUdzialPowierzchniBiologicznieCzynnej>150),1,0)":"Minimalny udział powierzchni biologicznie czynnej powinien być w przedziale <0; 150>%",
                       "if(nazwa='strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną',if(symbol='SW',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną',if(symbol='SJ',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa wielofunkcyjna z zabudową zagrodową',if(symbol='SZ',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa usługowa',if(symbol='SU',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa handlu wielkopowierzchniowego',if(symbol='SH',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa gospodarcza',if(symbol='SP',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa produkcji rolniczej',if(symbol='SR',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa infrastrukturalna',if(symbol='SI',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa zieleni i rekreacji',if(symbol='SN',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa cmentarzy',if(symbol='SC',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa górnictwa',if(symbol='SG',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa otwarta',if(symbol='SO',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(nazwa='strefa komunikacyjna',if(symbol='SK',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       "if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       "if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("ObszarUzupelnieniaZabudowy"):
        expressions = {
                       "if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       "if(regexp_match(lokalnyId,'\\d+POG-\\d+OUZ'),0,1)":"Błędny identyfikator lokalny",
                       "if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       "if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       "if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(symbol<>'OUZ',1,0)":"Symbol musi wynosić 'OUZ'",
                       "if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       "if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("ObszarZabudowySrodmiejskiej"):
        expressions = {
                       "if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       "if(regexp_match(lokalnyId,'\\d+POG-\\d+OZS'),0,1)":"Błędny identyfikator lokalny",
                       "if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       "if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       "if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(symbol<>'OZS',1,0)":"Symbol musi wynosić 'OZS'",
                       "if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       "if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
        expressions = {
                       "if(odlegloscDoSzkolyPodstawowej>0,0,1)":"Należy wpisać odleglość do szkoły podstawowej",
                       "if(regexp_match(lokalnyId,'\\d+POG-\\d+OSD'),0,1)":"Błędny identyfikator lokalny",
                       "if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       "if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       "if(odlegloscDoObszarowZieleniPublicznej>0,0,1)":"Należy wpisać odleglość do obszarów zieleni publicznej",
                       "if(powierzchniaLacznaObszarowZieleniPublicznej>=1.5,0,1)":"Należy wpisać łączną powierzchnię obszarów zieleni publicznej >= 1.5",
                       "if(odlegloscDoObszaruZieleniPublicznej>0,0,1)":"Należy wpisać odleglość do obszaru zieleni publicznej",
                       "if(powierzchniaObszaruZieleniPublicznej>=10,0,1)":"Należy wpisać powierzchnię obszaru zieleni publicznej >= 10",
                       "if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       "if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       "if(symbol<>'OSD',1,0)":"Symbol musi wynosić 'OSD'",
                       "if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       "if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu",
                       "if(odlegloscDoPrzedszkola>0 or odlegloscDoPrzedszkola is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoZlobka>0 or odlegloscDoZlobka is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoAmbulatoriumPOZ>0 or odlegloscDoAmbulatoriumPOZ is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoBiblioteki>0 or odlegloscDoBiblioteki is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoDomuKultury>0 or odlegloscDoDomuKultury is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoDomuPomocySpolecznej>0 or odlegloscDoDomuPomocySpolecznej is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoUrzadzonegoTerenuSportu>0 or odlegloscDoUrzadzonegoTerenuSportu is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoPrzystanku>0 or odlegloscDoPrzystanku is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoPlacowkiPocztowej>0 or odlegloscDoPlacowkiPocztowej is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoApteki>0 or odlegloscDoApteki is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoPosterunkuPolicji>0 or odlegloscDoPosterunkuPolicji is NULL,0,1)":"Wartoć musi być większa od 0",
                       "if(odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej>0 or odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej is NULL,0,1)":"Wartoć musi być większa od 0"
                      }
    else:
        expressions= {"":""}
    
    for expression in expressions:
        request = QgsFeatureRequest(QgsExpression(expression))
        requestFeatures = obrysLayer.getFeatures(request)
        
        for requestFeature in requestFeatures:
            new_feature = QgsFeature()
            new_feature.setGeometry(requestFeature.geometry())
            new_feature.setAttributes(requestFeature.attributes() + [expressions[expression]])
            layer.dataProvider().addFeature(new_feature)
    
    layer.commitChanges()
    if layer.featureCount() > 0:
        QgsProject.instance().addMapLayer(layer)
        return False
    return True

