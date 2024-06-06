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
ETRAnual=pd.DataFrame()
tempfinal=pd.DataFrame()
for i in range(len(Anio)): 
    filename=localizacion[0]+'yMet_'+Anio[i]+'_Dia_Mastil.xlsx'
    temp=pd.read_excel(filename)
    tempfinal=pd.concat([tempfinal,temp])
    tempfinal.reset_index(inplace=True,drop=True)
for j in range(0,len(Anio)-1):
    condicionesPri=((tempfinal['Año']==int(Anio[j])) & ((tempfinal['Mes']==4) | (tempfinal['Mes']==5) | 
                ((tempfinal['Mes']==6) & (tempfinal['Dia']<21)) | ((tempfinal['Mes']==3) & (tempfinal['Dia']>=20))))
    TMaxPri=tempfinal.loc[condicionesPri]['Text_max'].max()
    TMinPri=tempfinal[condicionesPri]['Text_min'].min()
    condicionesVer=((tempfinal['Año']==int(Anio[j])) & ((tempfinal['Mes']==7) | (tempfinal['Mes']==8) | 
                ((tempfinal['Mes']==9) & (tempfinal['Dia']<23)) | ((tempfinal['Mes']==6) & (tempfinal['Dia']>=21))))
    TMaxVer=tempfinal.loc[condicionesVer]['Text_max'].max()
    TMinVer=tempfinal[condicionesVer]['Text_min'].min()
    condicionesOto=((tempfinal['Año']==int(Anio[j])) & ((tempfinal['Mes']==10) | (tempfinal['Mes']==11) | 
                ((tempfinal['Mes']==12) & (tempfinal['Dia']<21)) | ((tempfinal['Mes']==9) & (tempfinal['Dia']>=23))))
    TMaxOto=tempfinal.loc[condicionesOto]['Text_max'].max()
    TMinOto=tempfinal[condicionesOto]['Text_min'].min()
    condicionesInv=((tempfinal['Año']==int(Anio[j+1])) & ((tempfinal['Mes']==1) | (tempfinal['Mes']==2) | 
                ((tempfinal['Mes']==3) & (tempfinal['Dia']<20))) | ((tempfinal['Año']==Anio[j]) & 
                (tempfinal['Mes']==12) & (tempfinal['Dia']>=21)))
    TMaxInv=tempfinal.loc[condicionesInv]['Text_max'].max()
    TMinInv=tempfinal[condicionesInv]['Text_min'].min()
# filename='PSA_ETRAnual_movmedian10.xlsx'
# ruta2='D:\\Clima\\'+localizacion[0]+'\\IndicesClimaticos'
# os.chdir(ruta2)
# ETRAnual.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')