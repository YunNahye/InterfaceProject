import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from PandasModel import PandasModel

form_class = uic.loadUiType("uisample.ui")[0]

class MyWindow(QMainWindow, form_class):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.initUI()

  def initUI(self):
    self.setWindowTitle("파일 오픈")
    self.pushButton.clicked.connect(self.fileopen)

  def fileopen(self):
    global filename
    filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
    self.dataload()

  def dataload(self):
    start1 = time.time()
    data = pd.read_excel(filename[0], index_col = None, header = 0)
    print("time :", time.time() - start1)
    start2 = time.time()
    model = PandasModel(data)
    self.tableView.setModel(model)
    print("time :", time.time() - start2)
    abc = data.dtypes
    ab = 0
    lsd = []
    name = []
    for x in abc:
        if x == "int64" or x == "float64":
            name += [data.columns[ab]]      
            lsd += [data.iloc[:,ab].values]
        ab += 1
        
    data_num = pd.DataFrame(lsd[0], columns = [name[0]])
    for x in range(len(lsd)-1):
        x = x + 1
        data_num.loc[:, name[x]] = lsd[x]
                  
    data_num = data_num.fillna(0)
    feature_names = list(data_num.columns[0:300])

    from sklearn.preprocessing import MinMaxScaler

    data_0 = MinMaxScaler().fit_transform(data_num.iloc[:,0:300])
    data_stdz = pd.DataFrame(data_0, columns = feature_names)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = MyWindow()
  myWindow.show()
  app.exec_()