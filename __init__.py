# -*- coding: utf-8 -*-

"""
/***************************************************************************
 WtyczkaAPP
                                 A QGIS plugin
 Wtyczka QGIS wspomagająca przygotowanie aktów planowania przestrzennego zgodnych z rozporządzeniem Ministra Rozwoju.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-05-27
        copyright            : (C) 2020 by EnviroSolutions Sp. z o.o.
        email                : office@envirosolutions.pl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import os
PLUGIN_VERSION = 'niezdefiniowana'
with open(os.path.join(os.path.dirname(__file__), 'metadata.txt'), 'r') as pluginMetadataFile:
    for line in pluginMetadataFile.readlines():
        if line.startswith("version="):
            PLUGIN_VERSION = line.strip().split('=')[-1]
            break

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load WtyczkaAPP class from file WtyczkaAPP.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .wtyczka_app import WtyczkaAPP
    return WtyczkaAPP(iface)