# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:09:12 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['Madrid']
Anio=['2021']
ruta1='D:\\Clima\\'+localizacion[0]+'\\Horarios'
os.chdir(ruta1)
filename=localizacion[0]+'yMet_'+Anio[0]+'_Hor.xlsx'
temp=pd.read_excel(filename)
temp=temp[['Año','Mes','Dia','Hora','Text_prm',
    'Hext_prm','Gh_prm','Text_prm_Meteo',
    'Hext_prm_Meteo','Gh_prm_Meteo','VVext_prm','VVext_prm_Meteo']]
# mes=['1','2','3','4','5','6','7','8','9','10','11','12']
dia=['6','8','18','1','22','14','29','25','20','4','12','21']
temp['Gh_prm']=temp['Gh_prm'].combine_first(temp['Gh_prm_Meteo'])
temp['Hext_prm']=temp['Hext_prm'].combine_first(temp['Hext_prm_Meteo'])
temp['Text_prm']=temp['Text_prm'].combine_first(temp['Text_prm_Meteo'])
temp['Text_prm']=temp['VVext_prm'].combine_first(temp['VVext_prm_Meteo'])
temp['AñoMesDia']=temp.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}", axis=1)
temp['AñoMesDia']=pd.to_datetime(temp['AñoMesDia'], format='%Y.0-%m.0-%d.0')
temp.drop(['Año','Mes','Dia','Hora','Text_prm_Meteo','Hext_prm_Meteo','Gh_prm_Meteo','VVext_prm_Meteo'],axis=1,inplace=True)
fechas=[]
for i in range(12):
    fechas.append(Anio[0]+'.0-'+str(i+1)+'.0-'+dia[i]+'.0')
fechas=pd.DataFrame(fechas)
fechas.columns=['AñoMesDia']
fechas['AñoMesDia']=pd.to_datetime(fechas['AñoMesDia'], format='%Y.0-%m.0-%d.0')
temp=pd.merge(temp,fechas,on='AñoMesDia',how='inner')
temp = temp.groupby('AñoMesDia').agg({
        'Text_prm': ['mean'],'Hext_prm': ['mean'],'Gh_prm': ['mean'],'VVext_prm': ['mean']
    })
temp.reset_index(inplace=True)
Fecha=pd.Series(temp.iloc[:,0]).astype(str).str.split('-', expand=True)
Fecha.columns=[['Año','Mes','Dia']]
temp= temp.drop(temp.columns[0],axis=1)
temp=pd.concat([Fecha,temp],axis=1)
temp.columns=['Año','Mes','Dia','Text_prm', 'Hext_prm' ,'Gh_prm','Vext_prm']

filenamediario='MadridyMet_Psicrom_Hor_Exp12.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\Psicrometrico'
os.chdir(ruta2)
temp.to_excel(filenamediario,index=False, engine='openpyxl', na_rep='NaN')
