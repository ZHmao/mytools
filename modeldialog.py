# coding:UTF8

from modelui import QtCore, QtGui, Ui_Dialog
from PyQt4.QtCore import QModelIndex
from datamodel import model
import os
import sys
import logging
import pubtool

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 

'''
author mzh
2014-12-29

<!--where里面的flag：0是第一个条件，1是第二个条件。type：0是and连接，1是or连接  mzh 2014-12-17 count: 0表示不计数，1表示计数-->


'''

class ModelDialog(QtGui.QDialog):

    '''
        currentRow是会更新当前选择行，没有选择时为-1
        insertLines是一个列表（列表里的单个元素是map），是新增的模板，当点击确定的时候要增加到template.xml文件中
        deleteLines是一个列表（列表里的单个元素是index属性的值），存储被删除的模板，当点击确定时修改template.xml文件
    '''
    currentRow = -1

    deleteLines = []
    
    def __init__(self, parent=None):
        self.currentPath = os.getcwd()
        logpath = self.currentPath + '\\log.py'
        logging.basicConfig(filename=logpath, level=logging.DEBUG, filemode='a')
        logging.info('configuration model')
        
        QtGui.QDialog.__init__(self, parent)
        self.setUI()
        self.displayData()
        
    def setUI(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setSignalAndSlot()
        
    def setSignalAndSlot(self):
        self.ui.btnLineAdd.clicked.connect(self.addLine)
        self.ui.btnLineDel.clicked.connect(self.delLine)
        self.ui.tableViewModel.clicked.connect(self.setSelectedLineNo)
        self.ui.buttonBox.accepted.connect(self.saveAction)
        self.ui.buttonBox.rejected.connect(self.delLine)
        
    @QtCore.pyqtSlot()
    def addLine(self):
        tempMap = {}
        tempMap['sheetname'] = ''
        tempMap['ascolumnname'] = ''
        tempMap['count'] = ''
        tempMap['sum'] = ''
        tempMap['groupby'] = ''
        tempMap['where'] = ''
        tempMap['coefficient'] = ''
        #state为0则是正常，state为1则是新增
        tempMap['state'] = '1'

        self.dataList.append(tempMap)
        newModel = model.DataModel(self.dataList, self.headList, self.ui.tableViewModel)
        self.ui.tableViewModel.setModel(newModel.model)

    
    @QtCore.pyqtSlot()
    def delLine(self):
        self.currentRow = self.ui.tableViewModel.currentIndex().row()
        if self.currentRow == -1:
            pass
    
    @QtCore.pyqtSlot()
    def saveAction(self):
        pubtool.writeXml(self.currentPath+'\\template.xml', self.ui.tableViewModel.model(), self.headList)
    
    @QtCore.pyqtSlot()
    def cancelAction(self):
        pass
    
    @QtCore.pyqtSlot(QModelIndex)
    def setSelectedLineNo(self, modelIndex):
        self.currentRow = modelIndex.row()
        
    def displayData(self):
        self.dataList = pubtool.readXml(self.currentPath+'\\template.xml')
        self.headList = ['sheetname', 'ascolumnname', 'count', 'sum', 'groupby', 'where', 'coefficient', 'state']
            
        mymodel = model.DataModel(self.dataList, self.headList, self.ui.tableViewModel)
        self.ui.tableViewModel.setModel(mymodel.model)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    testdlg = ModelDialog()
    testdlg.show()
    app.exec_()
        