# -*- coding: utf-8 -*-
from PyQt5.QtCore import QDateTime
initialValues = {
    "lokalnyId": "RYS1",
    "przestrzenNazw": "PL.ZIPPZP.9999/14-PZPW"
}

placeholders = {
    "RysunekAktuPlanowaniaPrzestrzennegoType:lokalnyId": "121_Rys1 LUB np. XXVI.49.2010_Rys1",
    "RysunekAktuPlanowaniaPrzestrzennegoType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    "RysunekAktuPlanowaniaPrzestrzennegoType:wersjaId": "20200630T223418",
    "RysunekAktuPlanowaniaPrzestrzennegoType:tytul": "Plan zagospodarowania przestrzennego województwa mazowieckiego Stan zagospodarowania",
    "RysunekAktuPlanowaniaPrzestrzennegoType:lacze": "http://www.przykladowa.domena/zagospodarowanie.tif",
    "RysunekAktuPlanowaniaPrzestrzennegoType:legenda": "http://www.przykladowa.domena/legenda.png",
    "RysunekAktuPlanowaniaPrzestrzennegoType:rozdzielczoscPrzestrzenna": "2000",
    "RysunekAktuPlanowaniaPrzestrzennegoType:opis": "Zał. 2 stan zagospodarowania",
    "AktPlanowaniaPrzestrzennegoType:lokalnyId": "121_P1 LUB np. XXVI.49.2010_P1",
    "AktPlanowaniaPrzestrzennegoType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    "AktPlanowaniaPrzestrzennegoType:wersjaId": "20200630T223418",
    "AktPlanowaniaPrzestrzennegoType:tytul": "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "AktPlanowaniaPrzestrzennegoType:zmiana": "0",
    "AktPlanowaniaPrzestrzennegoType:referencja": "Plan zagospodarowania przestrzennego województwa mazowieckiego został sporządzony na podkładzie Bazy Danych Obiektów Ogólnogeograficznych (BDOO).",
    "AktPlanowaniaPrzestrzennegoType:lacze": "http://mapy.geoportal.gov.pl/wss/service/ATOM/httpauth/atom/CODGIK_BDOO",
    "DokumentFormalnyType:lokalnyId": "121_Doc1 LUB np. XXVI.49.2010_Doc1",
    "DokumentFormalnyType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    "DokumentFormalnyType:tytul": "Uchwała nr 22/18 Sejmiku Województwa Mazowieckiego z dnia 19 grudnia 2018r. w sprawie Planu zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:nazwaSkrocona": "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:numerIdentyfikacyjny": "DZ. URZ. WOJ. 2018.13180",
    "DokumentFormalnyType:organUstanawiajacy": "Sejmik Województwa Mazowieckiego",
    "DokumentFormalnyType:lacze": "http://www.przykladowa.domena/akt.pdf"
}

# listy rozwijalne combobox

nilReasons = {
    "inapplicable": "inapplicable",
    "missing": "missing",
    "template": "template",
    "unknown": "unknown",
    "withheld": "withheld"
}

ukladyOdniesieniaPrzestrzennego = {
    "PL-1992": "http://www.opengis.net/def/crs/EPSG/0/2180",
    "PL-2000(5)": "http://www.opengis.net/def/crs/EPSG/0/2176",
    "PL-2000(6)": "http://www.opengis.net/def/crs/EPSG/0/2177",
    "PL-2000(7)": "http://www.opengis.net/def/crs/EPSG/0/2178",
    "PL-2000(8)": "http://www.opengis.net/def/crs/EPSG/0/2179"
}

przypisaniePowiatuDoEPSGukladuPL2000 = {
    "2176": ['0201','0203','0205','0206','0207','0209','0210','0211','0212','0216','0219','0221','0225','0226','0261','0262','0265','0801','0802','0803','0804',\
             '0805','0806','0807','0808','0809','0810','0811','0812','0861','0862','3002','3005','3014','3015','3024','3029','3201','3202','3203','3204','3205',\
             '3206','3207','3208','3209','3210','3211','3212','3214','3216','3217','3218','3261','3262','3263'],
    "2177": ['0202','0204','0208','0213','0214','0215','0217','0218','0220','0222','0223','0224','0264','0401','0402','0403','0404','0405','0406','0407','0408',\
             '0409','0410','0411','0412','0413','0414','0415','0416','0417','0418','0419','0461','0462','0463','0464','1001','1002','1003','1004','1008','1009',\
             '1011','1014','1017','1018','1019','1020','1061','1203','1213','1601','1602','1603','1604','1605','1606','1607','1608','1609','1610','1611','1661',\
             '2201','2202','2203','2204','2205','2206','2207','2208','2209','2210','2211','2212','2213','2214','2215','2216','2261','2262','2263','2264','2401',\
             '2402','2403','2404','2405','2406','2407','2408','2409','2410','2411','2412','2413','2414','2415','2417','2461','2462','2463','2464','2465','2466',\
             '2467','2468','2469','2470','2471','2472','2473','2474','2475','2476','2477','2478','2479','3001','3003','3004','3006','3007','3008','3009','3010',\
             '3011','3012','3013','3016','3017','3018','3019','3020','3021','3022','3023','3025','3026','3027','3028','3030','3031','3061','3062','3063','3064',\
             '3213','3215'],
    "2178": ['0605','0607','0611','0612','0614','0616','1005','1006','1007','1010','1012','1013','1015','1016','1021','1062','1063','1201','1202','1204','1205',\
             '1206','1207','1208','1209','1210','1211','1212','1214','1215','1216','1217','1218','1219','1261','1262','1263','1401','1402','1403','1404','1405',\
             '1406','1407','1408','1409','1411','1412','1413','1414','1415','1416','1417','1418','1419','1420','1421','1422','1423','1424','1425','1426','1427',\
             '1428','1429','1430','1432','1433','1434','1435','1436','1437','1438','1461','1462','1463','1464','1465','1802','1803','1805','1806','1807','1808',\
             '1810','1811','1812','1815','1816','1817','1818','1819','1820','1821','1861','1863','1864','2004','2006','2007','2014','2062','2416','2601','2602',\
             '2603','2604','2605','2606','2607','2608','2609','2610','2611','2612','2613','2661','2801','2802','2803','2804','2805','2806','2807','2808','2809',\
             '2810','2811','2812','2813','2814','2815','2816','2817','2818','2819','2861','2862'],
    "2179": ['0601','0602','0603','0604','0606','0608','0609','0610','0613','0615','0617','0618','0619','0620','0661','0662','0663','0664','1410','1801','1804',\
             '1809','1813','1814','1862','2001','2002','2003','2005','2008','2009','2010','2011','2012','2013','2061','2063']
    }

typyPlanu = {
    "miejscowy plan zagospodarowania przestrzennego": "miejscowyPlanZagospodarowaniaPrzestrzennego",
    "plan zagospodarowania przestrzennego województwa": "planZagospodarowaniaPrzestrzennegoWojewodztwa",
    "studium uwarunkowań i kier. zagosp. przestrz. gminy": "studiumUwarunkowanIKierunkowZagospodarowaniaPrzestrzennegoGminy",
    "miejscowy plan odbudowy": "miejscowyPlanOdbudowy",
    "miejscowy plan rewitalizacji": "miejscowyPlanRewitalizacji"
}

poziomyHierarchii = {
    "regionalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/regional",
    "lokalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/local",
    "sublokalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/infraLocal"
}

metadataKeywordAnchors = {
    'regionalnym': "https://inspire.ec.europa.eu/metadata-codelist/SpatialScope/regional",
    'lokalne': "https://inspire.ec.europa.eu/metadata-codelist/SpatialScope/local",
    'zagospodarowanie przestrzenne': "http://inspire.ec.europa.eu/theme/lu",
    'Brak warunków dostępu i użytkowania': "http://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply"
}

zgodnoscAnchors = {
    'Zgodny (conformant)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/conformant',
    'Niezgodny (notConformant)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/notConformant',
    'Brak oceny zgodności (notEvaluated)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/notEvaluated'
}

# słownik definiujący relacje między "typPlanu", a "poziomHierarchii"
typyPlanuPoziomyHierarchii = dict(zip(typyPlanu.keys(), [
    [list(poziomyHierarchii.keys())[2], list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[0]],
    [list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[2]],
    [list(poziomyHierarchii.keys())[2]],
    [list(poziomyHierarchii.keys())[2]]
]))

statusListaKodowa = {
    "wybierz":"wybierz",
    "nieaktualny": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/obsolete",
    "prawnie wiążący lub realizowany": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/legalForce",
    "w opracowaniu": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/elaboration",
    "w trakcie przyjmowania": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/adoption"
}

dziennikUrzedowyKod = {
    "Dziennik Ustaw": "dziennikUstaw",
    "Monitor Polski": "monitorPolski",
    "Dziennik urzędowy organu władzy państwowej": "dziennikResortowy",
    "Dziennik Urzędowy Unii Europejskiej": "dziennikUrzedowyUniiEuropejskiej",
    "Dziennik Urzędowy Woj. Dolnośląskiego": "dziennikUrzedowyWojDolnoslaskiego",
    "Dziennik Urzędowy Woj. Kujawsko-Pomorskiego": "dziennikUrzedowyWojKujawskoPomorskiego",
    "Dziennik Urzędowy Woj. Lubelskiego": "dziennikUrzedowyWojLubelskiego",
    "Dziennik Urzędowy Woj. Lubuskiego": "dziennikUrzedowyWojLubuskiego",
    "Dziennik Urzędowy Woj. Łódzkiego": "dziennikUrzedowyWojLodzkiego",
    "Dziennik Urzędowy Woj. Małopolskiego": "dziennikUrzedowyWojMalopolskiego",
    "Dziennik Urzędowy Woj. Mazowieckiego": "dziennikUrzedowyWojMazowieckiego",
    "Dziennik Urzędowy Woj. Opolskiego": "dziennikUrzedowyWojOpolskiego",
    "Dziennik Urzędowy Woj. Podkarpackiego": "dziennikUrzedowyWojPodkarpackiego",
    "Dziennik Urzędowy Woj. Podlaskiego": "dziennikUrzedowyWojPodlaskiego",
    "Dziennik Urzędowy Woj. Pomorskiego": "dziennikUrzedowyWojPomorskiego",
    "Dziennik Urzędowy Woj. Śląskiego": " dziennikUrzedowyWojSlaskiego",
    "Dziennik Urzędowy Woj. Świętokrzyskiego": "dziennikUrzedowyWojSwietokrzyskiego",
    "Dziennik Urzędowy Woj. Warmińsko-Mazurskiego": "dziennikUrzedowyWojWarminskoMazurskiego",
    "Dziennik Urzędowy Woj. Wielkopolskiego": "dziennikUrzedowyWojWielkopolskiego",
    "Dziennik Urzędowy Woj. Zachodniopomorskiego": "dziennikUrzedowyWojZachodniopomorskiego"
}

cI_DateTypeCode = {
    "utworzenie": "creation",
    "publikacja": "publication",
    "przegląd": "revision"
}

languages = {
    "polski": "pol",
    "angielski": "eng"
}

licznoscMetadataFields = {
    "e1": '1',
    "e2": '1',
    "e3": '1',
    "e4": '1+',
    "e5": '1+',
    "e6": '1+',
    "e7": '0+',
    "e8": '1',
    "e9": '4+',
    "e10": '01',
    "e11": '1+',
    "e12": '1+',
    "e13": '1',
    "e14": '01',
    "e15": '1',
    "e16": '1+',
    "e17": '2',
    "e18": '4+',
    "e19": '1',
    "e20": '1+',
    "e21": '1',
    "e22": '1+',
    "e23": '1',
    "e24": '1+',
    "e25": '1',
    "e26": '1',
    "e27": '1+',
    "e28": '1',
    "e29": '1+',
    "e30": '1',
    "e31": '1',
    "e32": '1',
    "e33": '1',
    "e34": '1'
}

nazwyMetadataFields = {
    "e1": 'Tytuł zbioru danych przestrzennych',
    "e2": 'Streszczenie',
    "e3": 'Typ zbioru danych przestrzennych',
    "e4": 'Adres zbioru danych przestrzennych',
    "e5": 'Unikalny identyfikator zbioru danych przestrzennych',
    "e6": 'Język zbioru danych przestrzennych',
    "e7": 'Kodowanie znaków',
    "e8": 'Kategoria tematyczna',
    "e9": 'Wartość słowa kluczowego',
    "e10": 'Standardowy słownik źródłowy',
    "e11": 'Geograficzny prostokąt ograniczający',
    "e12": 'System odniesienia za pomocą współrzędnych',
    "e13": 'Data utworzenia',
    "e14": 'Data opublikowania',
    "e15": 'Pochodzenie',
    "e16": 'Rozdzielczość przestrzenna',
    "e17": 'Typ reprezentacji przestrzennej',
    "e18": 'Specyfikacja',
    "e19": 'Stopień',
    "e20": 'Warunki dotyczące dostępu i użytkowania',
    "e21": 'Ograniczenia w publicznym dostępie',
    "e22": 'Jednostka odpowiedzialna',
    "e23": 'Rola jednostki odpowiedzialnej',
    "e24": 'Nazwa formatu',
    "e25": 'Wersja formatu',
    "e26": 'Częstotliwość aktualizacji',
    "e27": 'Informacja o szczegółowych wymaganiach dotyczących utrzymania',
    "e28": 'Zakres danych',
    "e29": 'Punkt kontaktowy metadanych',
    "e30": 'Data metadanych',
    "e31": 'Język metadanych',
    "e32": 'Unikalny identyfikator rekordu (pliku) metadanych',
    "e33": 'Standard metadanych',
    "e34": 'Standard metadanych'
}

# domyślne zmienne wartości dla pól wielokrotnych
metadataListWidgetsDefaultItems = {
    'e6': [{'e6_cmbbx': 'polski'}],
    'e9': [
        {
            'e9_lineEdit': 'Zagospodarowanie przestrzenne',
            'e10_cmbbx': 'Data opublikowania',
            'e10_dateTimeEdit': QDateTime(2008, 6, 1, 0, 0),
            'e10_lineEdit': 'GEMET - INSPIRE themes, version 1.0',
            'xlink': "http://www.eionet.europa.eu/gemet/inspire_themes"
        },
        {
            'e9_lineEdit': 'PlannedLandUse',
            'e10_cmbbx': None,
            'e10_dateTimeEdit': None,
            'e10_lineEdit': '',
            'xlink': None
        }
    ],
    'e17': [{'e17_lineEdit': 'wektor'}, {'e17_lineEdit': 'raster'}],
    'e20': [{'e20_lineEdit': 'Brak warunków dostępu i użytkowania'}],
}

relacjeDokumentu = {
    'przystąpienie': 'przystapienie',
    'uchwala': 'uchwala',
    'zmienia': 'zmienia',
    'uchyla': 'uchyla',
    'unieważnia': 'uniewaznia',
    'inna': ''
}

relacjeDokumentuZApp = {
    'przystapienie': 'dokumentPrzystepujacy',
    'uchwala': 'dokumentUchwalajacy',
    'zmienia': 'dokumentZmieniajacy',
    'uchyla': 'dokumentUchylajacy',
    'uniewaznia': 'dokumentUniewazniajacy',
    '': 'dokument'
}

rodzajeZbiorow = {
    'PZPW': 'PZPW',
    'SUIKZP': 'SUIKZP',
    'MPZP': 'MPZP',
    'POG':'POG'
}

nameSpaces2 = {
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
    'gmd': "http://www.isotc211.org/2005/gmd",
    'gco': 'http://www.isotc211.org/2005/gco',
    'xlink': 'http://www.w3.org/1999/xlink',
    'gml': "http://www.opengis.net/gml/3.2",
    'wfs': 'http://www.opengis.net/wfs/2.0',
    'gmlexr': "http://www.opengis.net/gml/3.3/exr"
}

nameSpaces = {
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0",
    'gmd': "http://www.isotc211.org/2005/gmd",
    'gco': 'http://www.isotc211.org/2005/gco',
    'xlink': 'http://www.w3.org/1999/xlink',
    'gml': "http://www.opengis.net/gml/3.2",
    'wfs': 'http://www.opengis.net/wfs/2.0',
    'gmlexr': "http://www.opengis.net/gml/3.3/exr"
}

xmlNameSpaces = {
    'xmlns:gco': "http://www.isotc211.org/2005/gco",
    'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
    'xmlns:gml': "http://www.opengis.net/gml/3.2",
    'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
    'xmlns:xlink': "http://www.w3.org/1999/xlink",
    'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'xmlns:app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0",
    'xsi:schemaLocation': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0 https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/2.0/planowaniePrzestrzenne_2_0.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
}

charakterUstaleniaListaKodowa = {
    'NULL':"NULL",
    'niewiążące':"https://inspire.ec.europa.eu/codelist/RegulationNatureValue/nonBinding",
    'ogólnie wiążące':"https://inspire.ec.europa.eu/codelist/RegulationNatureValue/generallyBinding",
    'określone w prawodawstwie':"https://inspire.ec.europa.eu/codelist/RegulationNatureValue/definedInLegislation",
    'wiążące dla deweloperów':"https://inspire.ec.europa.eu/codelist/RegulationNatureValue/bindingForDevelopers",
    'wiążące tylko dla władz':"https://inspire.ec.europa.eu/codelist/RegulationNatureValue/bindingOnlyForAuthorities"
}

nazwaListaKodowa = {
    'NULL':"NULL",
    'strefa wielofunkcyjna z zabudową mieszkaniową wielorodzinną':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaWielofunkcyjnaZZabudowaMieszkaniowaWielorodzinna",
    'strefa wielofunkcyjna z zabudową mieszkaniową jednorodzinną':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaWielofunkcyjnaZZabudowaMieszkaniowaJednorodzinna",
    'strefa wielofunkcyjna z zabudową zagrodową':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaWielofunkcyjnaZZabudowaZagrodowa",
    'strefa usługowa':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaUslugowa",
    'strefa handlu wielkopowierzchniowego':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaHandluWielkopowierzchniowego",
    'strefa gospodarcza':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaGospodarcza",
    'strefa produkcji rolniczej':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaProdukcjiRolniczej",
    'strefa infrastrukturalna':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaInfrastrukturalna",
    'strefa zieleni i rekreacji':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaZieleniIRekreacji",
    'strefa cmentarzy':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaCmentarzy",
    'strefa górnictwa':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaGornictwa",
    'strefa otwarta':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaOtwarta",
    'strefa komunikacyjna':"https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/RodzajStrefyPlanistycznejKod/strefaKomunikacyjna"
}

profilPodstawowyLubDodatkowyListaKodowa = {
                                            "teren akwakultury i obsługi rybactwa":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-RA",
                                            "teren autostrady":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KDA",
                                            "teren biogazowni":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PEB",
                                            "teren cmentarza":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-C",
                                            "teren drogi ekspresowej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KDS",
                                            "teren drogi głównej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KDG",
                                            "teren drogi głównej ruchu przyspieszonego":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KDR",
                                            "teren drogi zbiorczej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KDZ",
                                            "teren elektrowni geotermalnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PEG",
                                            "teren elektrowni słonecznej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PEF",
                                            "teren elektrowni wiatrowej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PEW",
                                            "teren elektrowni wodnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PEO",
                                            "teren górnictwa i wydobycia":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-G",
                                            "teren handlu wielkopowierzchniowego":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-H",
                                            "teren infrastruktury technicznej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-I",
                                            "teren komunikacji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-K",
                                            "teren komunikacji kolei linowej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KKL",
                                            "teren komunikacji kolejowej i szynowej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KK",
                                            "teren komunikacji lotniczej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KL",
                                            "teren komunikacji wodnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KW",
                                            "teren lasu":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-L",
                                            "teren obsługi komunikacji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-KO",
                                            "teren ogrodów działkowych":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-ZD",
                                            "teren plaży":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-ZB",
                                            "teren produkcji w gospodarstwach rolnych":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-RZP",
                                            "teren produkcji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-P",
                                            "teren rolnictwa z zakazem zabudowy":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-RN",
                                            "teren składów i magazynów":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-PS",
                                            "teren usług biurowych i administracji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UA",
                                            "teren usług edukacji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UE",
                                            "teren usług gastronomii":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UG",
                                            "teren usług handlu detalicznego":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UHD",
                                            "teren usług handlu":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UH",
                                            "teren usług kultu religijnego":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UR",
                                            "teren usług kultury i rozrywki":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UK",
                                            "teren usług nauki":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UN",
                                            "teren usług rzemieślniczych":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UL",
                                            "teren usług sportu i rekreacji":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-US",
                                            "teren usług turystyki":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UT",
                                            "teren usług zdrowia i pomocy społecznej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-UZ",
                                            "teren usług":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-U",
                                            "teren wielkotowarowej produkcji rolnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-RZW",
                                            "teren wód":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-W",
                                            "teren zabudowy letniskowej lub rekreacji indywidualnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-ML",
                                            "teren zabudowy mieszkaniowej jednorodzinnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-MN",
                                            "teren zabudowy mieszkaniowej wielorodzinnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-MW",
                                            "teren zabudowy zagrodowej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-RZM",
                                            "teren zieleni naturalnej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-ZN",
                                            "teren zieleni urządzonej":"https://www.gov.pl/static/zagospodarowanieprzestrzenne/ontology/KPT#KPT-MPZP-ZP"
                                          }

typyPlanu = {
    "miejscowy plan zagospodarowania przestrzennego": "miejscowyPlanZagospodarowaniaPrzestrzennego",
    "plan zagospodarowania przestrzennego województwa": "planZagospodarowaniaPrzestrzennegoWojewodztwa",
    "studium uwarunkowań i kier. zagosp. przestrz. gminy": "studiumUwarunkowanIKierunkowZagospodarowaniaPrzestrzennegoGminy",
    "miejscowy plan odbudowy": "miejscowyPlanOdbudowy",
    "miejscowy plan rewitalizacji": "miejscowyPlanRewitalizacji"
}

typyPlanuListaKodowa = {
    'plan ogólny gminy':'https://www.gov.pl/static/zagospodarowanieprzestrzenne/codelist/TypAktuPlanowaniaPrzestrzennegoKod/planOgolnyGminy'
    }