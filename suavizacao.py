# -*- coding: utf-8 -*-

from qgis.core import QGis, QgsGeometry
from PyQt4.QtGui import QIcon, QAction
from PyQt4.QtCore import QObject, SIGNAL
import resources_rc  
from qgis.gui import QgsMessageBar

class Suavizacao:

    def __init__(self, iface):
        
        self.iface = iface

    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/Suavizacao/w.png'
        self.action = QAction (QIcon (icon_path),"Suavizar linha", pai)
        self.action.setObjectName ("Suavizar linha")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        QObject.connect (self.action, SIGNAL ("triggered()"), self.suaviza)
        # Adicionar o botão icone
        self.iface.addToolBarIcon (self.action) 

    def unload(self):
        # remove o item de ícone do QGIS GUI.
        self.iface.removeToolBarIcon (self.action)
        
        
    def suaviza(self):
        if(self.testLayerAtivo()):
            if(self.testMetro() and self.testTipoGeometria() and self.testGeometriaSelecionada()):
                layer = self.iface.activeLayer()
                #if(self.iface.QgsGeometry().smooth()):
                #Um laço que percorre as imagens selecionadas e guarda na variavel: feat.
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
