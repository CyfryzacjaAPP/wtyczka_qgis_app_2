# -*- coding: utf-8 -*-
from .. import utils
from qgis.core import *
from qgis import processing
from ..utils import showPopup
from PyQt5.QtCore import QVariant
from .. import dictionaries



def isLayerInPoland(obrysLayer, layerName):
    granicaPolskiSHP = QgsApplication.qgisSettingsDirPath() + "/python/plugins/wtyczka_qgis_app/modules/app/A00_Granice_panstwa/A00_Granice_panstwa_bufor_300m.shp"
    warstwaGranicaPolski = QgsVectorLayer(granicaPolskiSHP, 'A00_Granice_panstwa', 'ogr')
    
    # transformacja do układu granic Państwa
    reprojectlayer = processing.run("native:reprojectlayer", {
        'INPUT': warstwaGranicaPolski,
        'TARGET_CRS': obrysLayer.crs(),
        'OUTPUT': 'memory:'
    })
    
    # rozbicie multipoligon-u na poligony
    pojedynczeObjekty = processing.run("native:multiparttosingleparts", {
        'INPUT': obrysLayer,
        'OUTPUT': 'memory:'
    })
    
    extractbyexpression = processing.run("qgis:extractbyexpression", {
        'INPUT': pojedynczeObjekty['OUTPUT'],
        'EXPRESSION': '$area != 0',
        'OUTPUT': 'memory:'
    })
    
    if pojedynczeObjekty['OUTPUT'].featureCount() - extractbyexpression['OUTPUT'].featureCount() > 0:
        showPopup("Wczytaj warstwę",f"Warstwa \"{layerName}\" posiada co najmniej jeden obiekt z pustą geometrią. Kontynuuję wczytywanie.")
    
    try:
        # geometria wychodzi poza granicę Polski
        przyciecie = processing.run("qgis:difference", {
            'INPUT': obrysLayer,
            'OVERLAY': reprojectlayer['OUTPUT'],
            'OUTPUT': 'memory:'
        })
    except:
        print("Problem z geometrią warstwy: ",obrysLayer.name())
        return True
    
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


def isJPTinLayer(obrysLayer, jpt):
    txt = '/' + jpt
    for obj in obrysLayer.getFeatures():
        if obj.attribute('przestrzenNazw') == None or not txt in obj.attribute('przestrzenNazw'):
            return False
    return True


def czyWarstwaMaWypelnioneObowiazkoweAtrybuty(obrysLayer):
    fields = QgsFields(obrysLayer.fields())
    layer = QgsVectorLayer('Polygon?crs=' + obrysLayer.crs().toWkt(), obrysLayer.name() + " - braki w atrybutach obowiazkowych", "memory")
    layer_data_provider = layer.dataProvider()
    layer_data_provider.addAttributes(fields)
    layer.updateFields()
    if obrysLayer.name().startswith("AktPlanowaniaPrzestrzennego"):
        sql = "tytul='' or typPlanu='' or poziomHierarchii='' or status='' or obowiazujeOd='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu='' or \
               tytul is NULL or typPlanu is NULL or poziomHierarchii is NULL or status is NULL or obowiazujeOd is null or lokalnyId is NULL or przestrzenNazw is NULL or wersjaId is NULL or poczatekWersjiObiektu is NULL"
    elif obrysLayer.name().startswith("StrefaPlanistyczna"):
        sql = "nazwa='' or symbol='' or oznaczenie='' or profilPodstawowy='' or status='' or obowiazujeOd='' or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu='' or \
               nazwa is NULL or symbol is NULL or oznaczenie is NULL or profilPodstawowy is NULL or status is NULL or obowiazujeOd is null or charakterUstalenia is NULL or lokalnyId is NULL or przestrzenNazw is NULL or wersjaId is NULL or poczatekWersjiObiektu is NULL"
    elif obrysLayer.name().startswith("ObszarUzupelnieniaZabudowy"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd='' or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu='' or \
               symbol is NULL or oznaczenie is NULL or status is NULL or obowiazujeOd is NULL or charakterUstalenia is NULL or lokalnyId is NULL or przestrzenNazw is NULL or wersjaId is NULL or poczatekWersjiObiektu is NULL"
    elif obrysLayer.name().startswith("ObszarZabudowySrodmiejskiej"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd='' or charakterUstalenia='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu='' or \
               symbol is NULL or oznaczenie is NULL or status is NULL or obowiazujeOd is NULL or charakterUstalenia is NULL or lokalnyId is NULL or przestrzenNazw is NULL or wersjaId is NULL or poczatekWersjiObiektu is NULL"
    elif obrysLayer.name().startswith("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
        sql = "symbol='' or oznaczenie='' or status='' or obowiazujeOd='' or charakterUstalenia='' or odlegloscDoSzkolyPodstawowej='' or odlegloscDoObszarowZieleniPublicznej='' or powierzchniaLacznaObszarowZieleniPublicznej='' or odlegloscDoObszaruZieleniPublicznej='' or powierzchniaObszaruZieleniPublicznej='' or lokalnyId='' or przestrzenNazw='' or wersjaId='' or poczatekWersjiObiektu='' or \
               symbol is NULL or oznaczenie is NULL or status is NULL or obowiazujeOd is NULL or charakterUstalenia is NULL or odlegloscDoSzkolyPodstawowej is NULL or odlegloscDoObszarowZieleniPublicznej is NULL or powierzchniaLacznaObszarowZieleniPublicznej is NULL or odlegloscDoObszaruZieleniPublicznej is NULL or powierzchniaObszaruZieleniPublicznej is NULL or lokalnyId is NULL or przestrzenNazw is NULL or wersjaId is NULL or poczatekWersjiObiektu is NULL"
    else:
        sql=""
    
    request = QgsFeatureRequest(QgsExpression(sql))
    requestFeatures = obrysLayer.getFeatures(request)
    
    for requestFeature in requestFeatures:
        new_feature = QgsFeature()
        new_feature.setGeometry(requestFeature.geometry())
        new_feature.setAttributes(requestFeature.attributes())
        layer.dataProvider().addFeature(new_feature)
    
    layer.commitChanges()
    if layer.featureCount() > 0:
        QgsProject.instance().addMapLayer(layer)
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
                       r"if(typPlanu<>'plan ogólny gminy',1,0)":"Atrybut 'typ palnu' musi wynosić 'plan ogólny gminy'",
                       r"if(regexp_match(lokalnyId,'\\d+POG'),0,1)":"Błędny identyfikator lokalny",
                       r"if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       r"if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       r"if(length(tytul)<=12,1,0)":"Należy wpisać nazwę po słowach 'Plan ogólny'",
                       r"if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       r"if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("StrefaPlanistyczna"):
        expressions = {
                       r"if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       r"if(regexp_match(lokalnyId,'\\d+POG-\\d+S[CGHIJKNOPRUWZ]')=0,1,0)":"Błędny identyfikator lokalny",
                       r"if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       r"if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       r"if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksNadziemnaIntensywnoscZabudowy is null,1,0)":"Należy uzupełnić maksymalną nadziemną intensywność zabudowy",
                       r"if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksUdzialPowierzchniZabudowy is null,1,0)":"Należy uzupełnić maksymalny udział powierzchni zabudowy",
                       r"if(symbol in ('SW','SJ','SZ','SU','SH','SP','SR') and maksWysokoscZabudowy is null,1,0)":"Należy uzupełnić maksymalną wysokość zabudowy",
                       r"if(symbol in ('SG','SO','SK') and (minUdzialPowierzchniBiologicznieCzynnej<0 or minUdzialPowierzchniBiologicznieCzynnej>150),1,0)":"Minimalny udział powierzchni biologicznie czynnej powinien być w przedziale <0; 150>%",
                       r"if(nazwa='strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną',if(symbol='SW',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną',if(symbol='SJ',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa wielofunkcyjna z zabudową zagrodową',if(symbol='SZ',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa usługowa',if(symbol='SU',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa handlu wielkopowierzchniowego',if(symbol='SH',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa gospodarcza',if(symbol='SP',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa produkcji rolniczej',if(symbol='SR',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa infrastrukturalna',if(symbol='SI',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa zieleni i rekreacji',if(symbol='SN',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa cmentarzy',if(symbol='SC',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa górnictwa',if(symbol='SG',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa otwarta',if(symbol='SO',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(nazwa='strefa komunikacyjna',if(symbol='SK',0,1),0)":"Symbol strefy jest niezgodny z jego nazwą",
                       r"if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Koniec wersji obiektu jest uzupełniony, należy wpisać datę dla 'obowiązuje do'",
                       r"if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       r"if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu",
                       r"if(symbol='SW' and profilPodstawowy != 'teren zabudowy mieszkaniowej wielorodzinnej,teren usług,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SJ' and profilPodstawowy != 'teren zabudowy mieszkaniowej jednorodzinnej,teren usług,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SZ' and profilPodstawowy != 'teren zabudowy zagrodowej,teren produkcji w gospodarstwach rolnych,teren akwakultury i obsługi rybactwa,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SU' and profilPodstawowy != 'teren usług,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SH' and profilPodstawowy != 'teren handlu wielkopowierzchniowego,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SP' and profilPodstawowy != 'teren produkcji,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SR' and profilPodstawowy != 'teren produkcji w gospodarstwach rolnych,teren wielkotowarowej produkcji rolnej,teren akwakultury i obsługi rybactwa,teren komunikacji,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SI' and profilPodstawowy != 'teren infrastruktury technicznej,teren komunikacji,teren ogrodów działkowych',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SN' and profilPodstawowy != 'teren zieleni urządzonej,teren plaży,teren wód,teren komunikacji,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SC' and profilPodstawowy != 'teren cmentarza,teren komunikacji,teren zieleni urządzonej,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SG' and profilPodstawowy != 'teren górnictwa i wydobycia,teren komunikacji,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SO' and profilPodstawowy != 'teren rolnictwa z zakazem zabudowy,teren lasu,teren zieleni naturalnej,teren wód,teren komunikacji,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(symbol='SK' and profilPodstawowy != 'teren autostrady,teren drogi ekspresowej,teren drogi głównej ruchu przyspieszonego,teren drogi głównej,teren komunikacji kolejowej i szynowej,teren komunikacji kolei linowej,teren komunikacji wodnej,teren komunikacji lotniczej,teren obsługi komunikacji,teren ogrodów działkowych,teren infrastruktury technicznej',1,0)":"Błędny profil podstawowy",
                       r"if(regexp_match(maksNadziemnaIntensywnoscZabudowy,'\\.\\d{2,}'),1,0)":"Wartość atrybutu maksNadziemnaIntensywnoscZabudowy musi być zapisana z precyzją jednego miejsca po przecinku",
                       r"if(regexp_match(maksUdzialPowierzchniZabudowy,'\\.\\d{2,}'),1,0)":"Wartość atrybutu maksUdzialPowierzchniZabudowy musi być zapisana z precyzją jednego miejsca po przecinku",
                       r"if(regexp_match(maksWysokoscZabudowy,'\\.\\d{2,}'),1,0)":"Wartość atrybutu maksWysokoscZabudowy musi być zapisana z precyzją jednego miejsca po przecinku",
                       r"if(regexp_match(minUdzialPowierzchniBiologicznieCzynnej,'\\.\\d{2,}'),1,0)":"Wartość atrybutu minUdzialPowierzchniBiologicznieCzynnej musi być zapisana z precyzją jednego miejsca po przecinku"
                      }
    elif obrysLayer.name().startswith("ObszarUzupelnieniaZabudowy"):
        expressions = {
                       r"if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       r"if(regexp_match(lokalnyId,'\\d+POG-\\d+OUZ'),0,1)":"Błędny identyfikator lokalny",
                       r"if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       r"if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       r"if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(symbol<>'OUZ',1,0)":"Symbol musi wynosić 'OUZ'",
                       r"if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       r"if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("ObszarZabudowySrodmiejskiej"):
        expressions = {
                       r"if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       r"if(regexp_match(lokalnyId,'\\d+POG-\\d+OZS'),0,1)":"Błędny identyfikator lokalny",
                       r"if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       r"if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       r"if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(symbol<>'OZS',1,0)":"Symbol musi wynosić 'OZS'",
                       r"if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       r"if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu"
                      }
    elif obrysLayer.name().startswith("ObszarStandardowDostepnosciInfrastrukturySpolecznej"):
        expressions = {
                       r"if(odlegloscDoSzkolyPodstawowej>0,0,1)":"Należy wpisać odleglość do szkoły podstawowej",
                       r"if(regexp_match(lokalnyId,'\\d+POG-\\d+OSD'),0,1)":"Błędny identyfikator lokalny",
                       r"if(regexp_match(przestrzenNazw,'PL.ZIPPZP\\.\\d+\\/\\d+-POG'),0,1)":"Błędna przestrzeń nazw",
                       r"if(regexp_match(wersjaId,'\\d{8}T\\d{6}'),0,1)":"Błędny identyfikator wersji",
                       r"if(odlegloscDoObszarowZieleniPublicznej>0,0,1)":"Należy wpisać odleglość do obszarów zieleni publicznej",
                       r"if(powierzchniaLacznaObszarowZieleniPublicznej>=1.5,0,1)":"Należy wpisać łączną powierzchnię obszarów zieleni publicznej >= 1.5",
                       r"if(odlegloscDoObszaruZieleniPublicznej>0,0,1)":"Należy wpisać odleglość do obszaru zieleni publicznej",
                       r"if(powierzchniaObszaruZieleniPublicznej>=10,0,1)":"Należy wpisać powierzchnię obszaru zieleni publicznej >= 10",
                       r"if(regexp_match(oznaczenie,symbol)=0,1,0)":"Oznaczenie nie jest spójne z symbolem",
                       r"if(status='nieaktualny' and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(koniecWersjiObiektu is not NULL and obowiazujeDo is NULL,1,0)":"Należy wpisać datę dla 'obowiązuje do'",
                       r"if(symbol<>'OSD',1,0)":"Symbol musi wynosić 'OSD'",
                       r"if(obowiazujeOd>=obowiazujeDo,1,0)":"Atrybut 'obowiązuje od' nie może być większy lub równy od 'obowiązuje do'",
                       r"if(koniecWersjiObiektu<=poczatekWersjiObiektu,1,0)":"Koniec wersji obiektu musi być późniejszy niż początek wersji obiektu",
                       r"if(odlegloscDoPrzedszkola>0 or odlegloscDoPrzedszkola is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoZlobka>0 or odlegloscDoZlobka is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoAmbulatoriumPOZ>0 or odlegloscDoAmbulatoriumPOZ is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoBiblioteki>0 or odlegloscDoBiblioteki is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoDomuKultury>0 or odlegloscDoDomuKultury is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoDomuPomocySpolecznej>0 or odlegloscDoDomuPomocySpolecznej is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoUrzadzonegoTerenuSportu>0 or odlegloscDoUrzadzonegoTerenuSportu is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoPrzystanku>0 or odlegloscDoPrzystanku is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoPlacowkiPocztowej>0 or odlegloscDoPlacowkiPocztowej is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoApteki>0 or odlegloscDoApteki is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoPosterunkuPolicji>0 or odlegloscDoPosterunkuPolicji is NULL,0,1)":"Wartoć musi być większa od 0",
                       r"if(odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej>0 or odlegloscDoPosterunkuJednostkiOchronyPrzeciwpozarowej is NULL,0,1)":"Wartoć musi być większa od 0"
                      }
    else:
        expressions= {"":""}
    
    for expression in expressions:
        qgs_expression = QgsExpression(expression)
        request = QgsFeatureRequest(qgs_expression)
        requestFeatures = obrysLayer.getFeatures(request)
        
        for requestFeature in requestFeatures:
            new_feature = QgsFeature()
            new_feature.setGeometry(requestFeature.geometry())
            new_feature.setAttributes(requestFeature.attributes() + [expressions[expression]])
            layer.dataProvider().addFeature(new_feature)
    
    layer.commitChanges()
    if layer.featureCount() > 0:
        QgsProject.instance().addMapLayer(layer)
        config = layer.attributeTableConfig()
        index = layer.fields().indexFromName('Opis_bledu')
        config.setColumnWidth(index, 300)
        layer.setAttributeTableConfig(config)
        return False
    return True


def kontrolaProfiliDodatkowych(obrysLayer):
    fields = QgsFields(obrysLayer.fields())
    new_field = QgsField('Opis_bledu', QVariant.String)
    fields.append(new_field)
    
    layer = QgsVectorLayer('Polygon?crs=' + obrysLayer.crs().toWkt(), obrysLayer.name() + " - bledy w profilach dodatkowych", "memory")
    layer_data_provider = layer.dataProvider()
    layer_data_provider.addAttributes(fields)
    layer.updateFields()
    
    for obj in obrysLayer.getFeatures():
        profileDodatkowe = obj['profilDodatkowy']
        
        if profileDodatkowe == NULL or profileDodatkowe == '':
            continue
        elif isinstance(profileDodatkowe, str):
            profileDodatkowe_list = [item.strip() for item in profileDodatkowe.split(",")]
        elif isinstance(profileDodatkowe, list):
            profileDodatkowe_list = profileDodatkowe
        
        for profilDodatkowy in profileDodatkowe_list:
            if not profilDodatkowy in dictionaries.profilPodstawowyLubDodatkowyListaKodowa:
                new_feature = QgsFeature()
                new_feature.setGeometry(obj.geometry())
                new_feature.setAttributes(obj.attributes() + ['Blędy w profilach dodatkowych'])
                layer.dataProvider().addFeature(new_feature)
    
    layer.commitChanges()
    if layer.featureCount() > 0:
        QgsProject.instance().addMapLayer(layer)
        config = layer.attributeTableConfig()
        index = layer.fields().indexFromName('Opis_bledu')
        config.setColumnWidth(index, 300)
        layer.setAttributeTableConfig(config)
        return False
    
    return True

