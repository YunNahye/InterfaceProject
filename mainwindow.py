import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
import time
from PandasModel import PandasModel
from Precleaning import Precleaning

form_class = uic.loadUiType("uisample.ui")[0]
_translate = QtCore.QCoreApplication.translate

class MyWindow(QMainWindow, form_class):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.initUI()

  def initUI(self):
    self.setWindowTitle("전처리도구")
    self.importButton.clicked.connect(self.fileopen)
    self.addButton.clicked.connect(self.addProperty)
    self.runPrecleaningButton.clicked.connect(self.logTrans)

  def fileopen(self):
    global filename
    filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
    self.dataload()

  def dataload(self):
    start1 = time.time()
    global data
    data = pd.read_excel(filename[0], index_col = None, header = 0)
    self.precleaning = Precleaning(data)
    print("time :", time.time() - start1)
    start2 = time.time()
    model = PandasModel(data)
    self.tableView.setModel(model)
    print("time :", time.time() - start2)
    for i in range(len(data.columns)):
      self.comboBox.addItem("")
      self.comboBox.setItemText(i, _translate("Dialog", data.columns[i]))

  def addProperty(self):
    rowPosition = self.tableWidget.rowCount()
    p = self.comboBox.currentText()
    w = self.weightInput.text()
    self.tableWidget.insertRow(rowPosition)
    self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(p))
    self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(w))
    self.precleaning.addWeight(p, float(w))

  def logTrans(self):
    self.precleaning.logTransformation()
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = MyWindow()
  myWindow.show()
  app.exec_()