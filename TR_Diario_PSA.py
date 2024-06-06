# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:18:11 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['PSA']
Anio=['2021','2022','2023']
ruta1='D:\\Clima\\'+localizacion[0]+'\\Diarios'
os.chdir(ruta1)
TRAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Dia.xlsx'
    temp=pd.read_excel(filename)
    Suma=(temp['Text_min']>20).sum()
    tempanual=pd.DataFrame({'Año':[Anio[i]], 'TRAnual':[Suma]})
    TRAnual=pd.concat([TRAnual,tempanual],ignore_index=True)
filename='PSA_TR_SinInterp.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
TRAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')
