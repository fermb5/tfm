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
ruta1='D:\\Clima\\'+localizacion[0]+'\\Diarios'
os.chdir(ruta1)
SUAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Dia_Mastil.xlsx'
    temp=pd.read_excel(filename)
    Suma=(temp['Text_max']>25).sum()
    tempanual=pd.DataFrame({'Año':[Anio[i]], 'SUAnual':[Suma]})
    SUAnual=pd.concat([SUAnual,tempanual],ignore_index=True)
filename='Madrid_SU_movmedian10.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
SUAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')