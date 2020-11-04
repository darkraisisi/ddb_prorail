import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

class Model:
    def __init__(self):
        filename = 'rand_for.sav'
        self.model = pickle.load(open(filename,'rb'))
        cols = ['stm_prioriteit','stm_oorz_code','stm_oorz_groep','stm_equipm_nr_*','stm_equipm_soort_*']
        self.data = pd.read_csv('sap_storing_data_hu_project_norm.csv',usecols=cols, low_memory=True)

        self.le_ozgr = pickle.load(open('le_ozgr','rb'))
        self.le_equipsrt = pickle.load(open('le_equipsrt','rb'))
        self.node_ys_dedup = pd.read_csv('nodes_prob.csv',usecols=['node_id', 'duur', 'prob'])


    def predict(self, prio:int, oorz_code:int, oorz_group:int, equip_type:int, geo_code:int):
        x_pred = np.array([prio, oorz_code, oorz_group, equip_type,geo_code]).reshape(1, -1)
        return self.model.predict(x_pred)[0]


    def predict_prob(self, prio:int, oorz_code:int, oorz_group:int, equip_type:int, geo_code:int):
        
        x_pred = np.array([prio, oorz_code, oorz_group, equip_type,geo_code]).reshape(1, -1)

        dept = self.model.decision_path(x_pred)[1][1]
        leaf = pd.DataFrame(self.model.decision_path(x_pred)[0].toarray()[:,:dept]).apply(
            lambda x:x.to_numpy().nonzero()[0].max(), axis=1).to_frame(name='node_id')
        leaf['record_id'] = leaf.index
    
        return leaf.merge(self.node_ys_dedup, on='node_id').drop('node_id', axis=1).sort_values(['record_id', 'duur']).sort_values('prob',ascending=False)[['duur','prob']][:10]


    def getDetails(self, prio:int, oorz_code:int, oorz_group:int, equip_type:int, geo_code:int):
        x_pred = np.array([prio, oorz_code, oorz_group, equip_type, geo_code])
        return x_pred.sum()


    def enc_lab(self, ozgr:str, equipsrt:str):
        return self.le_ozgr.transform([ozgr]), self.le_equipsrt.transform([equipsrt])