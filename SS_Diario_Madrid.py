# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:18:11 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['Madrid']
Anio=['2021','2022','2023']
ruta1='D:\\Clima\\'+localizacion[0]+'\\Horarios'
os.chdir(ruta1)
SSAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Hor.xlsx'
    temp=pd.read_excel(filename)
    temp['Gh_prm']=temp['Gh_prm'].combine_first(temp['Gh_prm_Meteo'])
    Suma=(temp['Gh_prm']>160).sum()
    tempanual=pd.DataFrame({'Año':[Anio[i]], 'SSAnual':[Suma]})
    SSAnual=pd.concat([SSAnual,tempanual],ignore_index=True)
filename='Madrid_SS.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
SSAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')