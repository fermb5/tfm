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
FGAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Hor.xlsx'
    temp=pd.read_excel(filename)
    media=(temp['VVext_prm']).mean()
    tempanual=pd.DataFrame({'Año':[Anio[i]], 'FGAnual':[media]})
    FGAnual=pd.concat([FGAnual,tempanual],ignore_index=True)
filename='Madrid_FGAnual_SinInterp.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
FGAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')