# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:48:43 2024

@author: ferma
"""

import os
import math
import pandas as pd
import numpy as np
localizacion=['Madrid']
ruta='D:\\Clima\\'+localizacion[0]+'\\Horarios'
os.chdir(ruta)
filenameTPYHor=localizacion[0]+'_prediccion_2050_Hor_585.xlsx'
TPY=pd.read_excel(filenameTPYHor)
TPY['MesDia']=TPY.apply(lambda row: f"{row['Mes']}-{row['Dia']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
TPY.drop(['Mes','Dia','Hora'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
TPY['MesDia']=pd.to_datetime(TPY['MesDia'], format='%m.0-%d.0') 
TPY=TPY.groupby('MesDia').agg({
    'Text_prm':['mean','max','min'],'Hext_prm':['mean'],'Gh prm':['mean'],'Vext_prm':['mean']})
TPY.columns=['Text_prm','Text_max','Text_min','Hext_prm','Gh_prm','VV_prm']
TPY.reset_index(inplace=True)
Fecha=pd.Series(TPY.iloc[:,0]).astype(str).str.split('-', expand=True)
Fecha.columns=[['Año','Mes','Dia']]
TPY= TPY.drop(TPY.columns[0],axis=1)
TPY=pd.concat([Fecha[['Mes','Dia']],TPY],axis=1)
TPY.columns=['Mes','Dia','Text_prm','Text_max','Text_min','Hext_prm','Gh_prm','VV_prm']
ruta2='D:\\Clima\\'+localizacion[0]+'\\Diarios'
filenameTPYDia=localizacion[0]+'_prediccion_2050_Dia_585.xlsx'
os.chdir(ruta2)
TPY.to_excel(filenameTPYDia,index=False, engine='openpyxl', na_rep='NaN')