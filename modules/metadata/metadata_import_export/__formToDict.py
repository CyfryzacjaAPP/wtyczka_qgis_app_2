# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp, Qt, QDateTime
from collections import ChainMap
from .. import dictionaries, utils


def formToMetadataElementDict(form):
    """pobiera wartości formularza do słownika metadataElementDict"""
    listWidgets = form.findChildren(QListWidget, QRegExp(r'.*'))
    lineEdits = form.findChildren(QLineEdit, QRegExp(r'.*'))
    dateTimeEdits = form.findChildren(QDateTimeEdit, QRegExp(r'.*'))
    comboBoxes = form.findChildren(QComboBox, QRegExp(r'.*'))
    singleWidgets = lineEdits + dateTimeEdits + comboBoxes
    metadataElementDict = {}
    for elementId, licznosc in dictionaries.licznoscMetadataFields.items():

        if not (licznosc == '01' or licznosc == '1'):   # pola wielokrotnego wyboru
            # pobierz listWidget
            listWidget = utils.getWidgetByName(
                layout=form, searchObjectType=QListWidget, name=elementId + '_listWidget')
            dataList = []
            for i in range(listWidget.count()):
                listWidgetItem = listWidget.item(i)
                data = listWidgetItem.data(Qt.UserRole)  # slownik
                # if data is None:
                #     data = listWidgetItem.text()
                dataList.append(data)
            metadataElementDict[elementId] = dataList

        else:   # pola pojedynczego wyboru
            # pobierz wszystkie widgety o danym elementId
            tempList = []
            for input in [x for x in singleWidgets if x.objectName().startswith(elementId + '_')]:
                if isinstance(input, QLineEdit):
                    tempList.append({input.objectName(): input.text()})
                elif isinstance(input, QDateTimeEdit):
                    tempList.append({input.objectName(): input.dateTime()})
                elif isinstance(input, QComboBox):
                    tempList.append({input.objectName(): input.currentText()})

            metadataElementDict[elementId] = dict(ChainMap(*tempList))

    # nadpisanie daty aktualną datą
    metadataElementDict['e30']['e30_dateTimeEdit'] = QDateTime.currentDateTime()

    # for k,v in metadataElementDict.items():
    #     print(k,dictionaries.licznoscMetadataFields[k],v)
    return metadataElementDict
