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
GSLAnual=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Dia.xlsx'
    temp=pd.read_excel(filename)
    temp2=temp.loc[temp['Text_prm']>12]
    indices=pd.DataFrame(temp2.index)
    contador=1
    indices_rellenar=pd.DataFrame()
    tempanual=pd.DataFrame()
    for j in range(len(indices)):
        if j<len(indices)-1:
            if indices.iloc[j,0]+1==indices.iloc[j+1,0]:
                contador=contador+1
            else:
                if contador>=6:
                    indices_inicio_final=pd.DataFrame({'indice_inicio':[indices.iloc[j,0]-contador+1],'indice_final':[indices.iloc[j,0]]})
                    indices_rellenar=pd.concat([indices_rellenar,indices_inicio_final],ignore_index=True)
                    contador=1
                else:
                    contador=1
        else:
            if contador>=6:
                    indices_inicio_final=pd.DataFrame({'indice_inicio':[indices.iloc[j,0]-contador+1],'indice_final':[indices.iloc[j,0]]})
                    indices_rellenar=pd.concat([indices_rellenar,indices_inicio_final],ignore_index=True)
    for k in range(indices_rellenar.shape[0]):
        indices_anual=pd.DataFrame({'Año':[int(Anio[i])],
                    'DiasGSL':[indices_rellenar.iloc[k,1]-indices_rellenar.iloc[k,0]+1],
                    'MesIni': [temp.iloc[indices_rellenar.iloc[k,0],1]],
                    'DiaIni': [temp.iloc[indices_rellenar.iloc[k,0],2]],
                    'MesFin': [temp.iloc[indices_rellenar.iloc[k,1],1]],
                    'DiaFin': [temp.iloc[indices_rellenar.iloc[k,1],2]]})
        tempanual=pd.concat([tempanual,indices_anual],ignore_index=True)
    GSLAnual=pd.concat([GSLAnual,tempanual],ignore_index=True)
    temp2=temp.loc[temp['Text_prm']<12]
    indices=pd.DataFrame(temp2.index)
    contador=1
    indices_rellenar=pd.DataFrame()
    tempanual=pd.DataFrame()
    for j in range(len(indices)):
        if j<len(indices)-1:
            if indices.iloc[j,0]+1==indices.iloc[j+1,0]:
                contador=contador+1
            else:
                if contador>=6:
                    indices_inicio_final=pd.DataFrame({'indice_inicio':[indices.iloc[j,0]-contador+1],'indice_final':[indices.iloc[j,0]]})
                    indices_rellenar=pd.concat([indices_rellenar,indices_inicio_final],ignore_index=True)
                    contador=1
                else:
                    contador=1
        else:
            if contador>=6:
                    indices_inicio_final=pd.DataFrame({'indice_inicio':[indices.iloc[j,0]-contador+1],'indice_final':[indices.iloc[j,0]]})
                    indices_rellenar=pd.concat([indices_rellenar,indices_inicio_final],ignore_index=True)
    for k in range(indices_rellenar.shape[0]):
        indices_anual=pd.DataFrame({'Año':[int(Anio[i])],
                    'DiasGSL':[indices_rellenar.iloc[k,1]-indices_rellenar.iloc[k,0]+1],
                    'MesIni': [temp.iloc[indices_rellenar.iloc[k,0],1]],
                    'DiaIni': [temp.iloc[indices_rellenar.iloc[k,0],2]],
                    'MesFin': [temp.iloc[indices_rellenar.iloc[k,1],1]],
                    'DiaFin': [temp.iloc[indices_rellenar.iloc[k,1],2]]})
        if indices_anual.iloc[0,2]>=6:            
            tempanual=pd.concat([tempanual,indices_anual],ignore_index=True) 
    GSLAnual=pd.concat([GSLAnual,tempanual],ignore_index=True)
filename='PSA_GSL_movmedian10.xlsx'
ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
os.chdir(ruta2)
GSLAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')