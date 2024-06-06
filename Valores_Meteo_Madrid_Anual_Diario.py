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
localizacion=['Madrid']
Anio=['2021','2022','2023']
for i in range(len(Anio)):
    ruta='D:\\Clima\\'+localizacion[0]+'\\Horarios'
    os.chdir(ruta)
    filenameMens='MadridyMet_'+Anio[i]+'_EOT_Hor.xlsx'
    ClimaTrat=pd.read_excel(filenameMens)
    
    ruta2='D:\\Clima\\'+localizacion[0]+'\\Minutales'
    os.chdir(ruta2)
    filenameMin='MadridyMet_'+Anio[i]+'_Min_EOT.xlsx'
    ClimaMin=pd.read_excel(filenameMin)
    ClimaTrat['AñoMesDia']=ClimaTrat.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
    ClimaTrat.drop(['Año','Mes','Dia','Hora'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
    ClimaTrat['AñoMesDia']=pd.to_datetime(ClimaTrat['AñoMesDia'], format='%Y.0-%m.0-%d.0') # ordena las columnas en formato horario
    if ClimaTrat.shape[1]>22:
        ClimaTrat['TextMastil_prm']=ClimaTrat['TextMastil_prm'].combine_first(ClimaTrat['Text_prm_Meteo'])
        ClimaTrat['TextMastil_max']=ClimaTrat['TextMastil_max'].combine_first(ClimaTrat['Text_max_Meteo'])
        ClimaTrat['TextMastil_min']=ClimaTrat['TextMastil_min'].combine_first(ClimaTrat['Text_min_Meteo'])
        ClimaTrat['HextMastil_prm']=ClimaTrat['HextMastil_prm'].combine_first(ClimaTrat['Hext_prm_Meteo'])
        ClimaTrat['HextMastil_max']=ClimaTrat['HextMastil_max'].combine_first(ClimaTrat['Hext_max_Meteo'])
        ClimaTrat['HextMastil_min']=ClimaTrat['HextMastil_min'].combine_first(ClimaTrat['Hext_min_Meteo'])
        ClimaTrat['Gh_prm']=ClimaTrat['Gh_prm'].combine_first(ClimaTrat['Gh_prm_Meteo'])
        ClimaTrat['Gh_max']=ClimaTrat['Gh_max'].combine_first(ClimaTrat['Gh_max_Meteo'])
        ClimaTrat['Gh_min']=ClimaTrat['Gh_min'].combine_first(ClimaTrat['Gh_min_Meteo'])
        ClimaTrat['VVext_prm']=ClimaTrat['VVext_prm'].combine_first(ClimaTrat['VVext_prm_Meteo'])
    ClimaTrat = ClimaTrat.groupby('AñoMesDia').agg({
            'TextMastil_prm': ['mean'], 'TextMastil_max': ['max'], 'TextMastil_min': ['min'],
            'HextMastil_prm': ['mean'], 'HextMastil_max':['max'],'HextMastil_min': ['min'],
            'Gh_prm': ['mean','count','sum'], 'Gh_max':['max'],'Gh_min': ['min'], 'VVext_prm':['mean'] 
        })
    ClimaTrat.columns=[['Text_prm', 'Text_max', 'Text_min', 'Hext_prm', 'Hext_max', 'Hext_min',
                        'Gh_prm', 'Gh_num', 'Gh_suma', 'Gh_max','Gh_min','VVext_prm']]
    if ClimaMin.shape[1]>8:
        tempVDVext=ClimaMin.loc[:,['Año','Mes','Dia','Hora','VVext','DVext']]
    elif ClimaMin.shape[1]>15:
        tempVDVext=ClimaMin.loc[:,['Año','Mes','Dia','Hora','VVext','DVext','Met_VVextAvg','Met_DVextAvg']]
        tempVDVext['VVext']=tempVDVext['VVext'].combine_first(tempVDVext['Met_VVextAvg'])
        tempVDVext['DVext']=tempVDVext['DVext'].combine_first(tempVDVext['Met_DVextAvg'])
        tempVDVext=tempVDVext.drop(['Met_VVextAvg','Met_DVextAvg'])
    tempVDVext['AñoMesDia']=tempVDVext.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
    tempVDVext.drop(['Año','Mes','Dia','Hora'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
    tempVDVext['AñoMesDia']=pd.to_datetime(tempVDVext['AñoMesDia'], format='%Y.0-%m.0-%d.0') # ordena las columnas en formato horario
    tempVDVext = tempVDVext.groupby('AñoMesDia').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos(col) if col.name != 'AñoMesDia' else col))
    tempVDVext = tempVDVext.groupby('AñoMesDia').apply(lambda group: group.apply(lambda col: filtrar_outliers(col) if col.name != 'AñoMesDia' else col))
    Vmax=math.trunc(tempVDVext['VVext'].max())+1
    VDVN=tempVDVext[(tempVDVext['DVext']>=337.5) | (tempVDVext['DVext']<=22.5)]
    VDVNE=tempVDVext[(tempVDVext['DVext']>=22.5) & (tempVDVext['DVext']<=67.5)]
    VDVE=tempVDVext[(tempVDVext['DVext']>=67.5) & (tempVDVext['DVext']<=112.5)]
    VDVSE=tempVDVext[(tempVDVext['DVext']>=112.5) & (tempVDVext['DVext']<=157.5)]
    VDVS=tempVDVext[(tempVDVext['DVext']>=157.5) & (tempVDVext['DVext']<=202.5)]
    VDVSO=tempVDVext[(tempVDVext['DVext']>=202.5) & (tempVDVext['DVext']<=247.5)]
    VDVO=tempVDVext[(tempVDVext['DVext']>=247.5) & (tempVDVext['DVext']<=292.5)]
    VDVNO=tempVDVext[(tempVDVext['DVext']>=292.5) & (tempVDVext['DVext']<=337.5)]
    VDVN.loc[:,'DVext']=VDVN.loc[:,'DVext'].apply(ajustar_angulo)
    cabecera=[]
    V=pd.DataFrame()
    for j in range(Vmax):
        velo='V'+str(j+1)
        cabecera.append(velo)
        V_a=tempVDVext['VVext'][(tempVDVext['VVext']>=j) & (tempVDVext['VVext']<=j+1)]
        V=pd.concat([V,V_a],axis=1)
    V=V.sort_index()
    V.columns=[cabecera]
    V.index = V.index // 1440 * 1440
    V.index = pd.to_datetime(V.index, unit='s')
    conteo= V.resample('1440S').count()
    conteo=conteo.reset_index()
    conteo=conteo.drop(['index'],axis=1)
    tempVDVext[['VVext','DVext']]=np.nan
    
    tempVDVext_unicoN = tempVDVext[~tempVDVext.index.isin(VDVN.index)]
    VDVN = pd.concat([VDVN, tempVDVext_unicoN])
    VDVN=VDVN.sort_index()
    VDVN=VDVN.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVN.columns=[['VVextN_prm', 'DVextN_prm', 'DVextN_num']]
    
    tempVDVext_unicoNE = tempVDVext[~tempVDVext.index.isin(VDVNE.index)]
    VDVNE = pd.concat([VDVNE, tempVDVext_unicoNE])
    VDVNE=VDVNE.sort_index()
    VDVNE=VDVNE.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVNE.columns=[['VVextNE_prm', 'DVextNE_prm', 'DVextNE_num']]
    
    tempVDVext_unicoE = tempVDVext[~tempVDVext.index.isin(VDVE.index)]
    VDVE = pd.concat([VDVE, tempVDVext_unicoE])
    VDVE=VDVE.sort_index()
    VDVE=VDVE.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVE.columns=[['VVextE_prm', 'DVextE_prm', 'DVextE_num']]
    
    tempVDVext_unicoSE = tempVDVext[~tempVDVext.index.isin(VDVSE.index)]
    VDVSE = pd.concat([VDVSE, tempVDVext_unicoSE])
    VDVSE=VDVSE.sort_index()
    VDVSE=VDVSE.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVSE.columns=[['VVextSE_prm', 'DVextSE_prm', 'DVextSE_num']]
    
    tempVDVext_unicoS = tempVDVext[~tempVDVext.index.isin(VDVS.index)]
    VDVS = pd.concat([VDVS, tempVDVext_unicoS])
    VDVS=VDVS.sort_index()
    VDVS=VDVS.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVS.columns=[['VVextS_prm', 'DVextS_prm', 'DVextS_num']]
    
    tempVDVext_unicoSO = tempVDVext[~tempVDVext.index.isin(VDVSO.index)]
    VDVSO = pd.concat([VDVSO, tempVDVext_unicoSO])
    VDVSO=VDVSO.sort_index()
    VDVSO=VDVSO.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVSO.columns=[['VVextSO_prm', 'DVextSO_prm', 'DVextSO_num']]
    
    tempVDVext_unicoO = tempVDVext[~tempVDVext.index.isin(VDVO.index)]
    VDVO = pd.concat([VDVO, tempVDVext_unicoO])
    VDVO=VDVO.sort_index()
    VDVO=VDVO.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVO.columns=[['VVextO_prm', 'DVextO_prm', 'DVextO_num']]
    
    tempVDVext_unicoNO = tempVDVext[~tempVDVext.index.isin(VDVNO.index)]
    VDVNO = pd.concat([VDVNO, tempVDVext_unicoNO])
    VDVNO=VDVNO.sort_index()
    VDVNO=VDVNO.groupby('AñoMesDia').agg({
        'VVext':['mean'],'DVext':['mean','count']})
    VDVNO.columns=[['VVextNO_prm', 'DVextNO_prm', 'DVextNO_num']]
    ClimaTrat=pd.concat([ClimaTrat,VDVN,VDVNE,VDVE,VDVSE,VDVS,VDVSO,VDVO,VDVNO],axis=1)
    ClimaTrat.reset_index(inplace=True)
    Fecha=pd.Series(ClimaTrat.iloc[:,0]).astype(str).str.split('-', expand=True)
    Fecha.columns=[['Año','Mes','Dia']]
    ClimaTrat= ClimaTrat.drop(ClimaTrat.columns[0],axis=1)
    ClimaTrat=pd.concat([Fecha,ClimaTrat,conteo],axis=1)
    rutadia='D:\\Clima\\'+localizacion[0]+'\\Diarios'
    os.chdir(rutadia)
    filename='MadridyMet_'+Anio[i]+'_Dia_Mastil_EOT.xlsx'
    ClimaTrat.to_excel(filename,index=False, engine='openpyxl', na_rep='NaN')
#el archivo creado tiene la cabecera de las columnas desplazado, IMPORTANTE asegurarse de que 
#estén bien las columnas posteriormente

    
    