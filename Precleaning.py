from PyQt5.QtWidgets import QVBoxLayout
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Precleaning():
  def __init__(self, data = pd.DataFrame()):
    self.data = data
    self.abc = data.dtypes
    self.ab = 0
    self.lsd = []
    self.name = []
    for x in self.abc:
        if x == "int64" or x == "float64":
            self.name += [data.columns[self.ab]]      
            self.lsd += [data.iloc[:,self.ab].values]
        self.ab += 1
        
    self.data_num = pd.DataFrame(self.lsd[0], columns = [self.name[0]])
    for x in range(len(self.lsd)-1):
        x = x + 1
        self.data_num.loc[:, self.name[x]] = self.lsd[x]
                  
    self.data_num = self.data_num.fillna(0)
    self.feature_names = list(self.data_num.columns[0:300])

    self.data_0 = MinMaxScaler().fit_transform(self.data_num.iloc[:,0:300])
    self.data_stdz = pd.DataFrame(self.data_0, columns = self.feature_names)

    self.property = []
    self.weight = []

  def addWeight(self, p, w):
    self.property.append(p)
    self.weight.append(w)

  def logTransformation(self):
    z = []   
    for x in range(len(self.property)):
        z.append(self.data_stdz[self.property[x]]*self.weight[x])
        
    self.division = [0 for i in range(len(self.data))]
    for x in range(len(z)):
        self.division += z[x]
    self.division = pd.DataFrame(self.division.values, columns = ['division']) 
    self.division_log = np.log(self.division)

    self.division_log_1 = self.division_log
    self.division_log_inf_index = self.division_log_1[self.division_log_1['division'] == -np.inf].index
    division_log_del_inf = self.division_log_1.drop(self.division_log_inf_index)

    self.division_log['division'] = self.division_log['division'].replace([-np.inf], min(division_log_del_inf['division'])-1)
    self.division_log.isnull().values.any()

    self.division_log_sort = self.division_log.sort_values(['division'], axis = 0, ascending = True)
    print(self.division_log_sort)

  def drawGraphByRange(self, f, layout = QVBoxLayout):
    h = []
    for x in range(f):
        h.append(x*(max(self.division_log['division']) - min(self.division_log['division']))/f)

    self.fig = plt.Figure()
    plt.hist(self.division_log ,bins = np.arange(min(self.division_log['division'])-2, max(self.division_log['division'])+2, 0.5), rwidth = 0.8)
    for x in range(f):
        plt.axvline(min(self.division_log['division'])+h[x], color = 'r', ls = '--')
    plt.axvline(max(self.division_log['division']), color = 'r', ls = '--')
    self.canvas = FigureCanvas(self.fig)
    layout.addWidget(self.canvas)
    self.canvas.draw()
    # plt.show()
    
    for x in range(f):
        h[x] = h[x] + min(self.division_log['division'])    
    h.append(max(self.division_log['division']))
    
    y = max(self.division_log['division'])
    i = []
    for x1 in self.division_log['division']:
        if y == x1:
            i.append(f)
        for x2 in range(f):
            if h[x2] <= x1 < h[x2 + 1]:
                i.append(x2 + 1)
    
    i = pd.DataFrame(i, columns = ['division number'])
    self.data_1 = self.data.join(self.division_log['division'])
    self.data_1 = self.data_1.join(i['division number'])
    self.data_sort = self.data_1.sort_values(['division'], axis = 0, ascending = True)
    self.i1 = i['division number'].value_counts()

    return self.canvas

  def drawGraphByCount(self, f):
    l = []
    for x in range(f):
        l.append(self.division_log_sort.iloc[x*(round(len(self.data)/f))])
    
    j = []   
    for x in range(f):
        j.append(l[x][0])
    
    plt.hist(self.division_log ,bins = np.arange(min(self.division_log['division'])-2, max(self.division_log['division'])+2, 0.5), rwidth = 0.8)
    for x in range(f):
        plt.axvline(j[x], color = 'r', ls = '--')
    plt.axvline(max(self.division_log['division']), color = 'r', ls = '--')
    plt.show()
    
    j.append(max(self.division_log['division']))
    
    y = max(self.division_log['division'])
    k = []
    for x1 in self.division_log['division']:
        if y == x1:
            k.append(f)
        for x2 in range(f):
            if j[x2] <= x1 < j[x2 + 1]:
                k.append(x2 + 1)
  
    k = pd.DataFrame(k, columns = ['division number'])
    self.data_1 = self.data.join(self.division_log['division'])
    self.data_1 = self.data_1.join(k['division number'])
    self.data_sort = self.data_1.sort_values(['division'], axis = 0, ascending = True)
    self.k1 = k['division number'].value_counts()