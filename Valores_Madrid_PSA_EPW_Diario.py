# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:39:52 2024

@author: ferma
"""

import os
import math
import pandas as pd
import numpy as np
#Define una función para filtrar outliers
def filtrar_outliers(series):
    if series.notna().any():
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        series[(series < (q25 - 1.5 * iqr)) | (series > (q75 + 1.5 * iqr))] = np.nan
        return series
    else:
        return pd.Series([np.nan] * len(series), index=series.index)
#se definen una función para eliminar los valores repetidos
def eliminar_valores_repetidos(series):
    prim_repeticiones=series.duplicated(keep='first')
    repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0]
    tempin=np.empty(shape=2)
    indices_cambio = series.index[series.diff().ne(0)]
    if len(repeticiiones>=10):
        for i in range(4,len(repeticiiones)):
            if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
                repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]:
                    tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
                    tempin=np.vstack((tempin,tempint))
        tempin=np.delete(tempin,0,axis=0)
    for i in range(len(indices_cambio)-1):
        diferencia=indices_cambio[i+1]-indices_cambio[i]
        if diferencia>5:
            series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
    return series
def ajustar_angulo(angulo):
    if angulo >= 337.15:
        return angulo-360
    else:
        return angulo
ruta='D:\\Clima\\Madrid\\TMY'
os.chdir(ruta)
filenameMens='FicherosEPW.xlsx'
ClimaTrat=pd.read_excel(filenameMens,sheet_name=1)

ClimaTrat['MesDia']=ClimaTrat.apply(lambda row: f"{row['Mes']}-{row['Dia ']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
ClimaTrat.drop(['Mes','Dia ','Hora'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
ClimaTrat['MesDia']=pd.to_datetime(ClimaTrat['MesDia'], format='%m.0-%d.0') # ordena las columnas en formato horario
ClimaTrat = ClimaTrat.groupby('MesDia').agg({
        'Tbs': ['mean','max','min'],
        'HR': ['mean'],
        'Ig': ['mean'], 'Vv':['mean'] 
    })
ClimaTrat.columns=[['Text_prm','Text_max','Text_min', 'Hext_prm',
                    'Gh_prm','VVext_prm']]
ClimaTrat=ClimaTrat.reset_index()
Fecha=pd.Series(ClimaTrat.iloc[:,0]).astype(str).str.split('-', expand=True)
Fecha.columns=[['Año','Mes','Dia']]
ClimaTrat= ClimaTrat.drop(ClimaTrat.columns[0],axis=1)
ClimaTrat=pd.concat([Fecha[['Mes','Dia']],ClimaTrat],axis=1)
rutadia='D:\\Clima\\PSA\\Diarios'
os.chdir(rutadia)
filename='PSAyMet_EPW_Dia.xlsx'
ClimaTrat.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')
#el archivo creado tiene la cabecera de las columnas desplazado, IMPORTANTE asegurarse de que 
#estén bien las columnas posteriormente

    
    