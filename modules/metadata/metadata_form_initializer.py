# -*- coding: utf-8 -*-
from qgis.core import QgsSettings
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def initializeMetadataForm(dlg):
    """Inicjalizuje formularz metadanych na podstawie ustawień"""
    s = QgsSettings()

    # Punkt kontaktowy
    # contactName = s.value("qgis_app2/settings/contactName", "")
    # contactMail = s.value("qgis_app2/settings/contactMail", "")
    contactName = ''
    contactMail = ''
    if contactName and contactMail:
        data = {
            'e22_name_lineEdit': contactName,
            'e22_mail_lineEdit': contactMail,
            'e23_cmbbx': 'Punkt kontaktowy (pointOfContact)'
        }
        item = QListWidgetItem()
        item.setData(Qt.UserRole, QVariant(data))
        item.setText("%s - %s - %s" % (contactName, contactMail, 'Punkt kontaktowy (pointOfContact)'))
        dlg.e22_listWidget.addItem(item)
        data = {
            'e29_name_lineEdit': contactName,
            'e29_mail_lineEdit': contactMail,
            'e29_cmbbx': 'Punkt kontaktowy (pointOfContact)'
        }
        item = QListWidgetItem()
        item.setData(Qt.UserRole, QVariant(data))
        item.setText("%s - %s - %s" % (contactName, contactMail, 'Punkt kontaktowy (pointOfContact)'))
        dlg.e29_listWidget.addItem(item)

    # Administrator danych
    adminName = s.value("qgis_app2/settings/adminName", "")
    adminMail = s.value("qgis_app2/settings/adminMail", "")
    if adminName and adminMail:
        data = {
            'e22_name_lineEdit': adminName,
            'e22_mail_lineEdit': adminMail,
            'e23_cmbbx': 'Administrator (custodian)'
        }
        item = QListWidgetItem()
        item.setData(Qt.UserRole, QVariant(data))
        item.setText("%s - %s - %s" % (adminName, adminMail, 'Administrator (custodian)'))
        dlg.e22_listWidget.addItem(item)