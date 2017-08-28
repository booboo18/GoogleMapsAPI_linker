# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GoogleMapsAPI_linkerDialog
                                 A QGIS plugin
 GoogleMapsAPI_linker
                             -------------------
        begin                : 2016-07-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Stephen Law
        email                : stephen.law@ucl.ac.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import time

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'GoogleMapsAPI_linker_dialog_base.ui'))


class GoogleMapsAPI_linkerDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GoogleMapsAPI_linkerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # public transport is checked for default
        self.radio_PT.click()

    # update layer - fill combo with layer lists
    def update_layer(self, layer_objects):
        for layer in layer_objects:
            self.layer_comboBox.addItem(layer[0], layer[1])


    # get layer - retrieving the value of the current selected layer
    def get_layer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        return layer

    def get_api(self):
        API=self.APIKey_lineEdit.text()
        return API

    def get_destination(self):
        Destination02 = self.Postcode_lineEdit.text()
        return Destination02

    def get_time(self):
        d_time=self.departure_lineEdit.text()
        if d_time == "current_time":
            d_time = str(int(time.time()))
        else:
            d_time = str(int(time.time()))
        return d_time

    def get_mode(self):
        #index=self.transit_layer_comboBox.currentIndex()
        #mode=self.transit_layer_comboBox.itemData(index)
        mode="transit"
        #mode="driving"
        #mode="bicycling"
        #mode="walking"
        return mode

    def get_pref(self):
        pref="best guess"
        #pref="pessimistic" worst scenario
        #pref="optimistic" best scenario
        return pref
