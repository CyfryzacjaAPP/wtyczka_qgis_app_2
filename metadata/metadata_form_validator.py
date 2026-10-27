# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re
from .. import utils, dictionaries


def validateMetadataForm(dlg):
    """Walidacja poprawności formularza metadanych"""
    # Sprawdzanie czy wymagane pola są puste:
    for label in utils.getWidgetsByType(dlg, QLabel):
        if not re.match("e\\d{1,2}_", label.objectName()):
            continue  # pomiń label, który nie jest częścią formularza

        elementId = label.objectName().split('_')[0]
        licznosc = dictionaries.licznoscMetadataFields[elementId]

        # pola pojedyncze
        if licznosc == '1' and elementId != 'e25':   # wymagane 1
            if elementId == 'e13':
                dateTimeEdit = utils.getWidgetByName(dlg, QDateTimeEdit, elementId + "_dateTimeEdit")
                if not dateTimeEdit.dateTime():
                    return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić, aby wygenerować plik metadanych." % label.text().strip('*')
            lineEdit = utils.getWidgetByName(dlg, QLineEdit, elementId + "_lineEdit")
            if lineEdit and not lineEdit.text().strip():
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić, aby wygenerować plik metadanych." % label.text().strip('*')

        # pola wielokrotne wymagane
        elif '+' in licznosc and licznosc[0] != 0:  # wielokrotnego wyboru wymagane
            listWidget = utils.getWidgetByName(dlg, QListWidget, elementId + "_listWidget")
            if listWidget.count() < int(licznosc[0]):
                return False, "Pole '%s' jest obowiązkowe. Musisz je wypełnić, aby wygenerować plik metadanych. Minimalna ilość wystąpień to %s." % (label.text().strip('*'), licznosc[0])

        # E1 tytuł zbioru i E5 Unikalny identyfikator zbioru danych przestrzennych
        if elementId == 'e1':
            lineEdit = utils.getWidgetByName(dlg, QLineEdit, elementId + "_lineEdit")
            text = lineEdit.text()
            if '<' in text or '>' in text:
                return False, "W polu '%s' musisz wprowadzić poprawną wartość w miejsce '<...>'." % (label.text().strip('*'))

        # E5 Unikalny identyfikator zbioru danych przestrzennych
        if elementId == 'e5':
            datasetIds = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                datasetIds.append(data['e5_lineEdit'])
            if len(list(filter(utils.validateDatasetId, datasetIds))) != len(datasetIds):
                return False, "W polu '%s' musisz zdefiniować wartość zgodnie z §4 rozporządzenia\n np.: 'PL.ZIPPZP.9999/146501-MPZP'." % (
                    label.text().strip('*'))

            # text = lineEdit.text().strip()
            # if '<' in text or '>' in text:
            #     return False, "W polu '%s' musisz wprowadzić poprawną wartość w miejsce <...>" % (
            #         label.text().strip('*'))
            # pattern = r'https://www.gov.pl/static/zagospodarowanieprzestrzenne/app/AktPlanowaniaPrzestrzennego/PL.ZIPPZP.\d{4}/[012]{1}[02468]{1}\d{0,4}-(PZPW)|(MPZP)|(SUIKZP)/'
            # if not utils.validateDatasetId():
            #     return False, "W polu '%s' musisz zdefiniować wartośc zgodnie z §4 rozporządzenia" % (
            #         label.text().strip('*'))

        # E9 pole słów kluczowych
        if elementId == 'e9':
            keywords = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                keywords.append(data['e9_lineEdit'])

            # Zagospodarowanie przestrzenne
            if 'Zagospodarowanie przestrzenne' not in keywords:
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s'." % (
                label.text().strip('*'), 'Zagospodarowanie przestrzenne')
            # PlannedLandUse
            if 'PlannedLandUse' not in keywords:
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s'." % (
                    label.text().strip('*'), 'PlannedLandUse')
            # zakres przestrzenny
            if not ('Regionalnym' in keywords or 'Lokalne' in keywords):
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s', wymagane słowo kluczowe %s." % (
                    label.text().strip('*'), 'zakres przestrzenny', '\'Regionalnym\' lub \'Lokalne\'')
            # Poziom planu zagospodarowania przestrzennego
            if not ('regionalny' in keywords or 'lokalny' in keywords or 'sublokalny' in keywords):
                return False, "W polu '%s' nie wprowadzono wszystkich wymaganych wartości.\nBrak klucza '%s', wymagane słowo kluczowe %s." % (
                    label.text().strip('*'), 'Poziom planu zagospodarowania przestrzennego', '\'regionalny\', \'lokalny\' lub \'sublokalny\'')

        # E11 prostokąt ograniczający
        if elementId == 'e11':
            bboxes = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                bboxes.append(data['e11_lineEdit'])
            for bbox in bboxes:
                # zła ilość kropek lub przecinków
                if bbox.count(',') != 3 or bbox.count('.') != 4:
                    return False, "Niepoprawna wartość w polu '%s'.\nZły format prostokąta ograniczającego.\nPodano: '%s'\nPoprawny format to: '<xmin>,<xmax>,<ymin>,<ymax>'.\nKażda współrzędna musi być zdefiniowana z dokładnoscią conajmniej 4 cyfr dziesiętnych." % (
                        label.text().strip('*'), bbox)
                # sprawdzenie wartości
                bboxList = bbox.strip().split(',')
                for strValue in bboxList:
                    if len(strValue.split('.')[1]) < 4:
                        return False, "Niepoprawna wartość w polu '%s'.\nWspółrzędne powinny być zdefiniowane z dokładnością conajmniej 4 cyfr dziesiętnych.\nPodano: '%s'." % (
                            label.text().strip('*'), strValue)
                xmin = float(bboxList[0])
                xmax = float(bboxList[1])
                ymin = float(bboxList[2])
                ymax = float(bboxList[3])
                if (
                        xmin > xmax or
                        ymin > ymax or
                        (xmin < -180 or xmin > 180) or
                        (xmax < -180 or xmax > 180) or
                        (ymin < -90 or ymin > 90) or
                        (ymax < -90 or ymax > 90)
                ):
                    return False, "Niepoprawna wartość w polu '%s'.\nZła wartość współrzędnych prostokąta ograniczającego.\nPodano: '%s'\nPoprawny format to: '<xmin>,<xmax>,<ymin>,<ymax>'\nx musi być w zakresie <-180;180>\ny musi być w zakresie <-90;90>." % (
                        label.text().strip('*'), bbox)

        # E20
        print(elementId)
        if elementId == 'e20':
            roles = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                roles.append(data['e20_lineEdit'])
                print(roles)
            if 'Brak warunków dostępu i użytkowania' not in roles:
                return False, "Brak wymaganej definicji w polu '%s'.\nMusi być zdefiniowana wartość: 'Brak warunków dostępu i użytkowania'." % label.text().strip(
                    '*')

        # E22 i E23 Jednostka odpowiedzialna
        if elementId == 'e22':
            roles = []
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                data = item.data(Qt.UserRole)
                roles.append(data['e23_cmbbx'])
            if 'Administrator (custodian)' not in roles:
                return False, "Brak wymaganej definicji w polu '%s'.\nMusi być zdefiniowany przynajmniej 'Administrator (custodian)'." % label.text().strip('*')
    return [True]