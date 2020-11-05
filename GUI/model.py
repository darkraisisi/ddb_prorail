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

        depth = self.model.decision_path(x_pred)[1][1]
        leaf = pd.DataFrame(columns=['node_id'])
        path = self.model.decision_path(x_pred)[0].toarray()
        for i in range(1,len(self.model.decision_path(x_pred)[1][1:])):
            start = self.model.decision_path(x_pred)[1][i-1]
            end = self.model.decision_path(x_pred)[1][i]
            leaf = leaf.append(pd.DataFrame(path[:,start:end]).apply(
                lambda x: self.nodeScaler(x,depth), axis=1).to_frame(
            name='node_id'))
        leaf['record_id'] = leaf.index
    
        leaf = leaf.merge(self.node_ys_dedup, on='node_id').drop('node_id', axis=1)
        duur = leaf.groupby(leaf['duur'])
        return (duur.sum() / duur.count()).reset_index()[['duur','prob']].dropna().sort_values('prob',ascending=False)[:10]

    def nodeScaler(self, x, depth):
        x_ar = x.to_numpy().nonzero()[0]
        flr = np.floor(x_ar / depth)
        x = (x_ar - (flr * depth)).astype(int).max()
        return x


    def getDetails(self, prio:int, oorz_code:int, oorz_group:int, equip_type:int, geo_code:int):
        x_pred = np.array([prio, oorz_code, oorz_group, equip_type, geo_code])
        return x_pred.sum()


    def enc_lab(self, ozgr:str, equipsrt:str):
        return self.le_ozgr.transform([ozgr])[0], self.le_equipsrt.transform([equipsrt])[0]