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
ruta1='D:\\Clima\\'+localizacion[0]+'\\TMY'
os.chdir(ruta1)
SUAnual=pd.DataFrame()
filename=localizacion[0]+'_TMY_Dia.xlsx'
temp=pd.read_excel(filename)
Suma=(temp['Text_max']>25).sum()
tempanual=pd.DataFrame({'Año':['TMY'], 'SUAnual':[Suma]})
SUAnual=pd.concat([SUAnual,tempanual],ignore_index=True)
filename='PSA_SU_movmedian10_TMY.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos\\TMY'
os.chdir(ruta2)
SUAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')