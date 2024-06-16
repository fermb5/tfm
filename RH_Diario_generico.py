# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:18:11 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['Madrid']
ruta1='D:\\Clima\\'+localizacion[0]+'\\TMY'
os.chdir(ruta1)
RHAnual=pd.DataFrame()
filename=localizacion[0]+'_TMY_Dia.xlsx'
temp=pd.read_excel(filename)
media=(temp['Hext_prm']).mean()
tempanual=pd.DataFrame({'Año':['TMY'], 'RHAnual':[media]})
RHAnual=pd.concat([RHAnual,tempanual],ignore_index=True)
filename='Madrid_RHAnual_SinInterp_TMY.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos\\TMY'
os.chdir(ruta2)
RHAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')