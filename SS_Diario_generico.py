# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:18:11 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['Madrid']
ruta1='D:\\Clima\\Madrid\\TMY'
os.chdir(ruta1)
SSAnual=pd.DataFrame()
filename=localizacion[0]+'_TMY_Hor.xlsx'
temp=pd.read_excel(filename,sheet_name=0)
# temp['Gh_prm']=temp['Gh_prm'].combine_first(temp['Gh_prm_Meteo'])
Suma1=(temp['Gh_prm']>160).sum()
# Suma2=
tempanual=pd.DataFrame({'Año':['TMY'], 'SSAnual':[Suma1]})
SSAnual=pd.concat([SSAnual,tempanual],ignore_index=True)
filename='Madrid_SS_TMY.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos\\TMY'
os.chdir(ruta2)
SSAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')