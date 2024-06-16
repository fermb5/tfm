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
ETRAnual=pd.DataFrame()
filename=localizacion[0]+'_TMY_Dia.xlsx'
temp=pd.read_excel(filename)
TmaxAnual=temp.iloc[:,3].max()
TminAnual=temp.iloc[:,4].min()
tempanual=pd.DataFrame({'Año':['TMY'],'ETRAnual': [TmaxAnual-TminAnual],'TmaxAnual': [TmaxAnual], 'TminAnual':[TminAnual]})
ETRAnual=pd.concat([ETRAnual,tempanual],ignore_index=True)
filename='PSA_ETRAnual_movmedian10_TMY.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos\\TMY'
os.chdir(ruta2)
ETRAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')