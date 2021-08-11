import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Precleaning():
  def __init__(self, data = pd.DataFrame()):
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