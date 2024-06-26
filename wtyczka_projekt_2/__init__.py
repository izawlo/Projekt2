# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WtyczkaProjekt2
                                 A QGIS plugin
 Wtyczka robi podstawowe operacje na punktach (np. liczy rónice wysokości, liczy pole powierzchni). 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-06-08
        copyright            : (C) 2023 by Alicja Wołosiewicz, Izabela Włodarczyk
        email                : 01179247@pw.edu.pl
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
    """Load WtyczkaProjekt2 class from file WtyczkaProjekt2.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .wtyczka_projekt_2 import WtyczkaProjekt2
    return WtyczkaProjekt2(iface)
