# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:18:11 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['PSA']
ruta1='D:\\Clima\\'+localizacion[0]+'\\TMY'
os.chdir(ruta1)
TRAnual=pd.DataFrame()
filename=localizacion[0]+'_TMY_Dia.xlsx'
temp=pd.read_excel(filename)
Suma=(temp['Text_min']>20).sum()
tempanual=pd.DataFrame({'Año':['TMY'], 'TRAnual':[Suma]})
TRAnual=pd.concat([TRAnual,tempanual],ignore_index=True)
filename='PSA_TR_SinInterp_TMY.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos\\TMY'
os.chdir(ruta2)
TRAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')
