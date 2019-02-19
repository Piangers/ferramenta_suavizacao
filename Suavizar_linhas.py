# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from Suavizar_linhas import resources_rc  
import os

class Suavizar_linhas:



    def __init__(self, iface):
            
        # Save reference to the QGIS interface   
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BGTImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        self.actions = []
        self.menu = self.tr(u'&Batch Vector Layer Saver')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BatchVectorLayerSaver')
        self.toolbar.setObjectName(u'Suavizar_linhas')

       
    def tr(self, message):
        
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BatchVectorLayerSaver', message)
        
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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Suavizar_linhas/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Suavizar_linhas'),
            callback=self.suavizar,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Suavizar_linhas'),
                action)
            self.iface.removeToolBarIcon(self.action)
        # remove the toolbar
        del self.toolbar


    def suavizar(self):
        if(self.testLayerAtivo()):
            if(self.testMetro() and self.testTipoGeometria() and self.testGeometriaSelecionada()):
                layer = self.iface.activeLayer()
                for feat in layer.selectedFeatures():
                    #geom recebe a geometria na posição selecionada
                    geom = feat.geometry()
                    #geom_smooth recebe os parametros do metodo: smooth, que recebe alguns parametros para se basear e realizar a suavização
                    geom_smooth = geom.smooth(2,0.3)
                    layer.changeGeometry(feat.id(),geom_smooth)
                    #self.iface.activeLayer().dataProvider().changeGeometryValues({feat.id(): geom_smooth})
                    # mapCanvas() é tudo apresentado na tela do QGIS e ela é atualizada com o metodo: refresh()
                    self.iface.mapCanvas().refresh()
                    

    def testLayerAtivo(self):
        #testa se existe uma camada selecionada
        if(not self.iface.activeLayer()):
            print ("Selecione uma Camada.")
            return False
        else:
            return True

    def testMetro(self):
        
        if (not self.iface.activeLayer().crs().mapUnits() == 6):
            return False
        else:
            return True

    def testTipoGeometria(self):
        if(not self.iface.activeLayer().geometryType() == 1):
            print ("A camada deve possuir geometrias do tipo Linha.")
            return False
        elif(not self.iface.activeLayer().isEditable()):
            print ("A camada deve estar em modo edivel.")
            return False
        else:
            return True

    def testGeometriaSelecionada(self):
        if(not len(self.iface.activeLayer().selectedFeatures()) > 0):
            print("Deve haver pelo menos uma geometria do tipo Linha selecionada.")
            return False
        else:
            return True        
