# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Suavizacao
                                 A QGIS plugin
 ferramenta
                              -------------------
        begin                : 2018-03-07
        git sha              : $Format:%H$
        copyright            : (C) 2018 by piangers
        email                : cesar_piangers@hotmail.com
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
from qgis.core import QGis, QgsVectorLayer, QgsGeometry
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QAction

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from suavizacao_dialog import SuavizacaoDialog
import os.path
import Tkinter       
import tkMessageBox
from qgis.gui import QgsMessageBar

class Suavizacao:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # Declare instance attributes
        self.actions = []
        self.menu = u'&Suavizacao'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Suavizacao')
        self.toolbar.setObjectName(u'Suavizacao')
	self.dlg = SuavizacaoDialog()

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
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

        # Create the dialog (after translation) and keep reference
        self.dlg = SuavizacaoDialog()

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

        icon_path = ':/plugins/Suavizacao/w.png'
        self.add_action(
            icon_path,
            text=u'Suavizacao',
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&Suavizacao', action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        if(self.testLayerAtivo()):
            if(self.testMetro() and self.testTipoGeometria() and self.testGeometriaSelecionada()):
                
                layer = self.iface.activeLayer()
                #if(self.iface.QgsGeometry().smooth()):
                #UM LAÇO QUE PERCORRE AS IMAGENS SELECIONADAS E GUARDA NA VARIAVEL feat.
                for feat in layer.selectedFeatures():
                    #geom RECEBE AGEOMETRIA DA VEZ
                    geom = feat.geometry()
                    #geom_smooth RECEBE OS PARAMETROS DO METODO smooth QUE RECEBE ALGUNS PARAMETROS PARA SE CORDENAR E REALIZAR A SUAVIZAÇÃO
                    geom_smooth = geom.smooth(2,0.3)
                    layer.changeGeometry(feat.id(),geom_smooth)
                    #self.iface.activeLayer().dataProvider().changeGeometryValues({feat.id(): geom_smooth})
                    # mapCanvas() É A TOTALIDADE APRESENTADA NA TELA DO QGIS E ELA É ATUALIZADA COM O METODO refresh()
                    self.iface.mapCanvas().refresh()
                    

    def testLayerAtivo(self):
        if(not self.iface.activeLayer()):
            self.iface.messageBar().pushMessage("Selecione uma Camada.", level=QgsMessageBar.INFO, duration=5)
            return False
        
        else:
            return True

    def testMetro(self):
        
        if (not self.iface.activeLayer().crs().mapUnits() == QGis.Meters):
            
            return False
        else:
            return True

    def testTipoGeometria(self):
        if(not self.iface.activeLayer().geometryType() == QGis.Line):
            self.iface.messageBar().pushMessage("A camada deve possuir geometrias do tipo linha.", level=QgsMessageBar.INFO, duration=5)
            return False
        elif(not self.iface.activeLayer().isEditable()):
            self.iface.messageBar().pushMessage ("A camada deve estar em modo edivel.", level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True

    def testGeometriaSelecionada(self):
        if(not len(self.iface.activeLayer().selectedFeatures()) > 0):
            self.iface.messageBar().pushMessage("Deve haver pelo menos uma geometria linha selecionada.", level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True        
