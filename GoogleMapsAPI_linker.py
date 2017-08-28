# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GoogleMapsAPI_linker
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from GoogleMapsAPI_linker_dialog import GoogleMapsAPI_linkerDialog
import os.path
from urllib import urlopen
import simplejson as json
import os.path
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QProgressBar,QComboBox
from qgis.core import *
import os
#from PyQt4 import QtCore, QtGui



class GoogleMapsAPI_linker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GoogleMapsAPI_linker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GoogleMapsAPI_linkerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GoogleMapsAPI_linker')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GoogleMapsAPI_linker')
        self.toolbar.setObjectName(u'GoogleMapsAPI_linker')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GoogleMapsAPI_linker', message)

    def add_action(self,icon_path,text,callback,enabled_flag=True,add_to_menu=True,add_to_toolbar=True,status_tip=None,whats_this=None,parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GoogleMapsAPI_linker/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GoogleMapsAPI_Linker'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GoogleMapsAPI_linker'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

##########################################################################################################################################################

    def gmap_api(self):


        #enter your own time
        #still need to translate
        #Thurs, 18 Aug 2016 09:00:00 GMT
        #d_time=1471510800

        # need a function to convert time

        # enter your own API key
        API=self.dlg.get_api()
        Destination02=self.dlg.get_destination()
        layer = self.dlg.get_layer()
        d_time=self.dlg.get_time()
        #self.iface.messageBar().pushInfo(u'My Plugin says', u'Hello World')

        # need to do a proper Google API key check
        if API == "Enter Google API Key":
            self.iface.messageBar().pushInfo(u'My Plugin says', u'Please enter correct Google API Key')
            self.dlg.close()

        #Check mode
        if self.dlg.radio_PT.isChecked():
            mode = "transit"
        elif self.dlg.radio_VE.isChecked():
            mode = "driving"
        else:
            mode = "transit"
        pref=self.dlg.get_pref()

        print API
        print str(Destination02)

        # this setup the QgsVector Layer to fill in data
        v2 = QgsVectorLayer("Point?crs=epsg:27700", "temporary_output", "memory")
        pr = v2.dataProvider()
        v2.startEditing()
        pr.addAttributes([QgsField("id", QVariant.Int),
                          QgsField("x", QVariant.Double),
                          QgsField("y",QVariant.Double),
                          QgsField("time", QVariant.String),
                          QgsField("mode",QVariant.String),
                          QgsField("origin",QVariant.String),
                          QgsField("destination",QVariant.String)])
        iter=layer.getFeatures()
        count=0

        # this fills the data
        for i in iter:
            try:
                geom=i.geometry()
                x=geom.asPoint()
                x1=x[1]
                x0=x[0]
                url2 = urlopen(
                    'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+str(x1)+','+str(x0)+'&destinations=' + Destination02 + '&mode='+ mode + '&departure_time='+d_time+'&key='+str(API)).read()
                url2 = json.loads(url2)
                time = url2['rows'][0]['elements'][0]['duration']['text']
                origin=url2['origin_addresses'][0]
                destination=url2['destination_addresses'][0]

                feature=QgsFeature()
                feature.setAttributes([count,str(x1),str(x0),time,mode,origin,destination])
                pr.addFeatures([feature])
                count=count+1
                if url2['status'] == 'OK':
                    print 'ok'
                else:
                    print 'error'
                    self.iface.messageBar().pushInfo(u'My Plugin says', u'Invalid call')
                print count

            except KeyError:
                self.iface.messageBar().pushInfo(u'My Plugin says', u'Invalid call')
                print 'error'+str(x)
                continue

        # this commits the layer
        v2.commitChanges()
        v2.updateExtents()
        # this loads the layer
        QgsMapLayerRegistry.instance().addMapLayer(v2)
        self.dlg.close()



##########################################################################################################################################################



    #def set_attribute(self):
        #v2 = QgsVectorLayer("Point?crs=epsg:27700", "temporary_points", "memory")
        #pr = v2.dataProvider()
        #v2.startEditing()
        #pr.addAttributes([QgsField("id", QVariant.Int),QgsField("x", QVariant.Double),QgsField("y", QVariant.Double),QgsField("time", QVariant.String)])
        #Dict = {}
        #count = 1
        #for i in Dict.items():
            #feature = QgsFeature()
            #feature.setAttributes([count, i[0], i[1]])
            #pr.addFeatures([feature])
            #count = count + 1


#############################################################################

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        ###### YOUR OWN CODE ######

        # click pushButtons
        # put code about some radio button has to be pressed
        self.dlg.run_button.clicked.connect(self.run_method)
        self.dlg.close_button.clicked.connect(self.close_method)

        # put current layers into comboBox
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_objects =[]
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                layer_objects.append((layer.name(),layer))
        self.dlg.update_layer(layer_objects)

        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #pass

    def run_method(self):
        self.dlg.show()
        self.gmap_api()

    def close_method(self):
        self.dlg.close()

########################################################################################################################


