# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GoogleMapsAPI_linker
                                 A QGIS plugin
 GoogleMapsAPI_linker
                             -------------------
        begin                : 2016-07-18
        copyright            : (C) 2016 by Stephen Law
        email                : stephen.law@ucl.ac.uk
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GoogleMapsAPI_linker class from file GoogleMapsAPI_linker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GoogleMapsAPI_linker import GoogleMapsAPI_linker
    return GoogleMapsAPI_linker(iface)
