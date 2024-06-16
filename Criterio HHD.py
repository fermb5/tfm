# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:20:29 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
localizacion=['PSA']
ruta1='D:\\Clima\\'+localizacion[0]+'\\TMY'
os.chdir(ruta1)
filename='PSA_TMY_Hor.xlsx'

temp=pd.read_excel(filename)

condicionesPri= ((temp['Mes']==4) | (temp['Mes']==5) | 
            ((temp['Mes']==6) & (temp['Dia']<21)) | ((temp['Mes']==3) & (temp['Dia']>=20)))
condicionesVer=((temp['Mes']==7) | (temp['Mes']==8) | 
            ((temp['Mes']==9) & (temp['Dia']<21)) | ((temp['Mes']==6) & (temp['Dia']>=20)))
condicionesOto= ((temp['Mes']==10) | (temp['Mes']==11) | 
            ((temp['Mes']==12) & (temp['Dia']<21)) | ((temp['Mes']==9) & (temp['Dia']>=20)))
condicionesInv= ((temp['Mes']==1) | (temp['Mes']==2) | 
            ((temp['Mes']==3) & (temp['Dia']<21)) | ((temp['Mes']==12) & (temp['Dia']>=20)))

HDDPri=((temp[condicionesPri]['Text_prm'].apply(lambda x: 19 - x if x < 19 else 0)).sum())/24
HDDVer=((temp[condicionesVer]['Text_prm'].apply(lambda x: 19 - x if x < 19 else 0)).sum())/24
HDDOto=((temp[condicionesOto]['Text_prm'].apply(lambda x: 19 - x if x < 19 else 0)).sum())/24
HDDInv=((temp[condicionesInv]['Text_prm'].apply(lambda x: 19 - x if x < 19 else 0)).sum())/24

CDDPri=((temp[condicionesPri]['Text_prm'].apply(lambda x: x-27 if x > 27 else 0)).sum())/24
CDDVer=((temp[condicionesVer]['Text_prm'].apply(lambda x: x-27 if x > 27 else 0)).sum())/24
CDDOto=((temp[condicionesOto]['Text_prm'].apply(lambda x: x-27 if x > 27 else 0)).sum())/24
CDDInv=((temp[condicionesInv]['Text_prm'].apply(lambda x: x-27 if x > 27 else 0)).sum())/24