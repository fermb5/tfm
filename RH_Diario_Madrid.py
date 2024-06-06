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
RHAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Dia_Mastil.xlsx'
    temp=pd.read_excel(filename)
    media=(temp['Hext_prm']).mean()
    tempanual=pd.DataFrame({'Año':[Anio[i]], 'RHAnual':[media]})
    RHAnual=pd.concat([RHAnual,tempanual],ignore_index=True)
filename='Madrid_RHAnual_SinInterp.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
RHAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')