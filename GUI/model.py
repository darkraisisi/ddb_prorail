import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime as date

from sklearn import linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

usefullcols = ['stm_mon_nr','stm_sap_meld_ddt','stm_status_melding_sap','stm_km_van_mld','stm_km_tot_mld','stm_km_van_gst',
'stm_km_tot_gst','stm_fh_tijd','stm_sap_melddatum','stm_aanngeb_tijd','stm_aanntpl_tijd','stm_arbeid',
'stm_progfh_in_tijd','stm_progfh_in_invoer_tijd','stm_progfh_in_duur','stm_sap_storeindtijd','stm_progfh_gw_tijd',
'stm_reactie_duur','stm_progfh_gw_duur','stm_progfh_gw_teller','stm_afspr_aanvangdd','stm_afspr_aanvangtijd',
'stm_fh_duur','stm_evb','stm_sap_meldtijd','stm_sap_meldtekst_lang','stm_prioriteit','stm_oh_pg_gst',
'stm_sap_meldtekst','stm_techn_gst','stm_contractgeb_gst','stm_tao_indicator','stm_geo_mld','stm_functiepl_mld',
'stm_geo_mld_uit_functiepl','stm_aanngeb_ddt','stm_aanngeb_dd','stm_oorz_code','stm_oorz_groep','stm_oorz_tkst',
'stm_fh_dd','stm_fh_status','stm_geo_gst','stm_functiepl_gst','stm_geo_gst_uit_functiepl','stm_fh_ddt',
'stm_aanntpl_dd','stm_techn_mld','stm_sap_storeinddatum','stm_equipm_nr_mld','stm_equipm_soort_mld',
'stm_equipm_omschr_mld','stm_sap_storeind_ddt','stm_contractgeb_mld','stm_equipm_nr_gst','stm_equipm_soort_gst',
'stm_equipm_omschr_gst','stm_progfh_in_invoer_dat','stm_progfh_in_datum','stm_oorz_tekst_kort','stm_dstrglp_naar',
'stm_tao_indicator_vorige','stm_vl_post','stm_dstrglp_van','stm_pplg_van','stm_tao_soort_mutatie',
'stm_progfh_gw_lwd_tijd','stm_pplg_naar','stm_progfh_gw_lwd_datum']

df = pd.read_csv('sap_storing_data_hu_project.csv',usecols=usefullcols, low_memory=True)
features = ['stm_prioriteit','stm_oorz_code','stm_oorz_groep','stm_equipm_nr_*','stm_equipm_soort_*']
target = 'stm_fh_duur'

now = date.datetime.today()
zeroTimeDiff = now - now

df['stm_sap_meld_ddt'] = pd.to_datetime(df['stm_sap_meld_ddt'], format='%d/%m/%Y %H:%M:%S')
df['stm_sap_storeind_ddt'] = pd.to_datetime(df['stm_sap_storeind_ddt'], format='%d/%m/%Y %H:%M:%S')
# df['stm_fh_tijd'] = pd.to_timedelta(df['stm_fh_tijd'], unit='s')


# Meldingen waar de oplossing in de toekomst is zijn onzin.
df[df['stm_sap_storeind_ddt'] >= now][['stm_sap_storeind_ddt','stm_sap_meld_ddt']]
df.drop(df[df['stm_sap_storeind_ddt'] >= now][['stm_sap_storeind_ddt','stm_sap_meld_ddt']].index,inplace=True)

# Een datetime diff om extra waardes te kunnen filteren.
# df['diff_meld_strend'] = df['stm_sap_storeind_ddt']-df['stm_sap_meld_ddt']

# Rijen waar het probleem eerder is opgelost dan de meldingen zijn onbetrouwbaar.
# df.drop(df[df['diff_meld_strend'] < zeroTimeDiff].index, inplace = True)

# Alles wat langer dan een dag duurt is niet urgent genoeg en dus niet nuttig.
# df.drop(df[df['diff_meld_strend'] > pd.to_timedelta(6, unit='h')].index, inplace = True)
# df.drop(df[df['stm_fh_tijd'] > pd.to_timedelta(6, unit='h')].index, inplace = True)
df.drop(df[df['stm_fh_duur'] > 360].index, inplace = True)

# Waar geen duur is hebben we niks aan dus die moeten weg.
df.dropna(subset=['stm_fh_duur'],inplace=True)

dubbleCol = ['stm_equipm_omschr_*', 'stm_equipm_soort_*', 'stm_equipm_nr_*',
             'stm_geo_*_uit_functiepl', 'stm_functiepl_*', 'stm_geo_*',
             'stm_km_van_*', 'stm_km_tot_*',
             'stm_contractgeb_*', 'stm_techn_*']
original = 'mld'
optional = ['gst']  # Order of least to most important
for colPH in dubbleCol:
    colOg = colPH.replace('*', original)

    for option in optional:
        colOp = colPH.replace('*', option)
        df[colPH] = np.where(df[colOp].isna(), df[colOg], df[colOp])
        df.drop(columns=[colOp], inplace=True)
    df.drop(columns=[colOg], inplace=True)

df['stm_prioriteit'] = df['stm_prioriteit'].fillna(1) # Laagste prio
df['stm_oorz_code'] = df['stm_oorz_code'].fillna(299) # 'Niet gemeld' code
df['stm_oorz_groep'] = df['stm_oorz_groep'].fillna('x')
df['stm_fh_status'] = df['stm_fh_status'].fillna(1) # Median of values
df['stm_aanngeb_tijd'] = df['stm_aanngeb_tijd'].fillna(df['stm_sap_meldtijd']) # Aannemer beltijd gelijk met melding zetten.
df['stm_progfh_in_invoer_tijd'] = df['stm_progfh_in_invoer_tijd'].fillna(df['stm_aanngeb_tijd']) # Tijd van prognose op beltijd zetten.
df['stm_equipm_nr_*'] = df['stm_equipm_nr_*'].fillna(0)
df['stm_equipm_soort_*'] = df['stm_equipm_soort_*'].fillna('x')
df['stm_contractgeb_*'] = df['stm_contractgeb_*'].fillna(0)
df['stm_progfh_gw_teller'] = df['stm_progfh_gw_teller'].fillna(0)

df['stm_prioriteit'] = df['stm_prioriteit'].astype(int)
df['stm_oorz_code'] = df['stm_oorz_code'].astype(int)
df['stm_fh_status'] = df['stm_fh_status'].astype(int)
df['stm_fh_duur'] = df['stm_fh_duur'].astype(int)
df['stm_progfh_gw_teller'] = df['stm_progfh_gw_teller'].astype(int)
df['stm_equipm_nr_*'] = df['stm_equipm_nr_*'].astype(int)
df['stm_contractgeb_*'] = df['stm_contractgeb_*'].astype(int)

amntInTime = df[df['stm_fh_duur'] < 137].count()[0]
total = df.shape[0]
print(f'{amntInTime / total * 100}% van de tijd heeft het baseline model het goed.')

le_ozgr = LabelEncoder()
le_ozgr.fit(df['stm_oorz_groep'].unique())
df['stm_oorz_groep'] = le_ozgr.transform(df['stm_oorz_groep'])
# df['stm_oorz_groep'].unique()

le_equipsrt = LabelEncoder()
le_equipsrt.fit(df['stm_equipm_soort_*'].unique())
df['stm_equipm_soort_*'] = le_equipsrt.transform(df['stm_equipm_soort_*'])
# df['stm_equipm_soort_*'].unique()

X = df[features]
Y = df[target]

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=10)

linearModel = linear_model.LinearRegression().fit(x_train,y_train)
linYPrediction = linearModel.predict(x_test)
print(f'Score: {linearModel.score(x_test,y_test)}')
print(f'Mean squared error: {np.sqrt(mean_squared_error(y_test,linYPrediction))}')


