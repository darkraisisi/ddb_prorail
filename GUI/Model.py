import numpy as np
import pandas as pd
import pickle

class Model:
    def __init__(self):
        filename = 'finalized_model_lin.sav'
        self.model = pickle.load(open(filename,'rb'))
        cols = ['stm_prioriteit','stm_oorz_code','stm_oorz_groep','stm_equipm_nr_*','stm_equipm_soort_*']
        self.data = pd.read_csv('sap_storing_data_hu_project_norm.csv',usecols=cols, low_memory=True)


    def predict(self, prio:int, oorz_code:int, oorz_group:int, equip_nr:int, equip_type:int):
        x_pred = np.array([prio, oorz_code, oorz_group, equip_nr, equip_type]).reshape(1, -1)
        return self.model.predict(x_pred)[0]


    def getDetails(self, prio:int, oorz_code:int, oorz_group:int, equip_nr:int, equip_type:int):
        x_pred = np.array([prio, oorz_code, oorz_group, equip_nr, equip_type])
        return x_pred.sum()