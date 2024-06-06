# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:48:51 2024

@author: ferma
"""
import os
import numpy as np 
import pandas as pd
import math
#Se carga el archivo con el que se rellenan los datos
localizacion=['Madrid']
Anio=['2021','2022','2023']
ruta2='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Excels_Diferentes_Datos'
os.chdir(ruta2)
filenameMeteo='Val_MadridyMet_Min.xlsx'
ClimaMeteo=pd.read_excel(filenameMeteo)
ruta='D:\\Clima\\'+localizacion[0]+'\\Minutales'
os.chdir(ruta)
filenameEOT=localizacion[0]+'_EOT_Min.xlsx'
EOT=pd.read_excel(filenameEOT)
for i in range(len(Anio)):
#Se carga el archivo minutales a rellenar
    ruta='D:\\Clima\\'+localizacion[0]+'\\Minutales'
    os.chdir(ruta)
    filenameMin='Madrid_'+Anio[i]+'_Min.xlsx'
    ClimaAnualMin=pd.read_excel(filenameMin)
    filas=ClimaAnualMin.shape[0]
    #Se carga el archivo horario en el que puedan faltar filas
    ruta1='D:\\Clima\\'+localizacion[0]+'\\Horarios'
    os.chdir(ruta1)
    filenameHor='Madrid_'+Anio[i]+'_Hor.xlsx'
    ClimaAnualHor=pd.read_excel(filenameHor)
    #Se crea el dataframe a rellenar
    df_vacio=pd.DataFrame(np.nan, index=range(ClimaAnualMin.shape[0]), columns=[f'Columna{i}' for i in range(1, 12)])
    ClimaAnualMin=pd.concat([ClimaAnualMin,df_vacio],axis=1)
    ClimaAnualMin.columns=['Año','Mes','Dia','Hora','Min','TextMastil','HextMastil','Gh','VVext','DVext','Gv','R',
           'Met_TextAvg','Met_TextMax','Met_HextAvg','Met_GhAvg','Met_GhMax',
           'Met_VVextAvg','Met_VVextMax','Met_VVextSdev','Met_DVextAvg','Met_DVextMax','Met_DVextSde']
    #Se observan las filas del archivo horario que necesitan más datos
    columna=ClimaAnualHor.columns.isin(['TextMastil_num','HextMastil_num','Gh_num','Gv_num','VVext_num'])
    Index=np.where(columna==True)[0]
    filasText=np.where(ClimaAnualHor.to_numpy()[:,Index[0]]<15)[0]
    filasHext=np.where(ClimaAnualHor.to_numpy()[:,Index[1]]<15)[0]
    filasGh=np.where(ClimaAnualHor.to_numpy()[:,Index[2]]<15)[0]
    filasVVext=np.where(ClimaAnualHor.to_numpy()[:,Index[4]]<15)[0]
    #Se obtienen los índices del archivo minutal en los que se deben de añadir valores para la variable T
    ClimaAnualHorText=ClimaAnualHor.loc[filasText]
    indices_coincidentes_1_t = ClimaAnualMin[ClimaAnualMin.set_index(['Año', 'Mes','Dia','Hora']).index.isin(ClimaAnualHorText.set_index(['Año', 'Mes','Dia','Hora']).index)].index
    ClimaAnualMinText=ClimaAnualMin.loc[indices_coincidentes_1_t]
    indices_coincidentes_2_t=ClimaMeteo[ClimaMeteo.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaAnualMinText.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    ClimaMeteo_t=ClimaMeteo.loc[indices_coincidentes_2_t]
    indices_coincidentes_3_t=ClimaAnualMinText[ClimaAnualMinText.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaMeteo_t.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    #Se obtienen los índices del archivo minutal en los que se deben de añadir valores para la variable H
    ClimaAnualHorHext=ClimaAnualHor.loc[filasHext]
    indices_coincidentes_1_h = ClimaAnualMin[ClimaAnualMin.set_index(['Año', 'Mes','Dia','Hora']).index.isin(ClimaAnualHorHext.set_index(['Año', 'Mes','Dia','Hora']).index)].index
    ClimaAnualMinHext=ClimaAnualMin.loc[indices_coincidentes_1_h]
    indices_coincidentes_2_h=ClimaMeteo[ClimaMeteo.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaAnualMinHext.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    ClimaMeteo_h=ClimaMeteo.loc[indices_coincidentes_2_h]
    indices_coincidentes_3_h=ClimaAnualMinHext[ClimaAnualMinHext.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaMeteo_h.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    #Se obtienen los índices del archivo minutal en los que se deben de añadir valores para la variable G
    ClimaAnualHorGh=ClimaAnualHor.loc[filasGh]
    indices_coincidentes_1_g = ClimaAnualMin[ClimaAnualMin.set_index(['Año', 'Mes','Dia','Hora']).index.isin(ClimaAnualHorGh.set_index(['Año', 'Mes','Dia','Hora']).index)].index
    ClimaAnualMinGh=ClimaAnualMin.loc[indices_coincidentes_1_g]
    indices_coincidentes_2_g=ClimaMeteo[ClimaMeteo.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaAnualMinGh.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    ClimaMeteo_g=ClimaMeteo.loc[indices_coincidentes_2_g]
    indices_coincidentes_3_g=ClimaAnualMinGh[ClimaAnualMinGh.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaMeteo_g.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    #Se obtienen los índices del archivo minutal en los que se deben de añadir valores para la variable V
    ClimaAnualHorVVext=ClimaAnualHor.loc[filasVVext]
    indices_coincidentes_1_v = ClimaAnualMin[ClimaAnualMin.set_index(['Año', 'Mes','Dia','Hora']).index.isin(ClimaAnualHorVVext.set_index(['Año', 'Mes','Dia','Hora']).index)].index
    ClimaAnualMinVVext=ClimaAnualMin.loc[indices_coincidentes_1_v]
    indices_coincidentes_2_v=ClimaMeteo[ClimaMeteo.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaAnualMinVVext.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    ClimaMeteo_v=ClimaMeteo.loc[indices_coincidentes_2_v]
    indices_coincidentes_3_v=ClimaAnualMinVVext[ClimaAnualMinVVext.set_index(['Año', 'Mes','Dia','Hora','Min']).index.isin(ClimaMeteo_v.set_index(['Año', 'Mes','Dia','Hora','Min']).index)].index
    #Se van añadiendo en los índices correspondientes del dataframe a rellenar los valores de los dataframes utilizados para rellenar
    ClimaAnualMin.loc[indices_coincidentes_3_t.to_list(),['Met_TextAvg','Met_TextMax']]=ClimaMeteo_t[['TextAvg','TextMax']].values
    ClimaAnualMin.loc[indices_coincidentes_3_h.to_list(),['Met_HextAvg']]=ClimaMeteo_h[['HextAvg']].values
    ClimaAnualMin.loc[indices_coincidentes_3_g.to_list(),['Met_GhAvg','Met_GhMax']]=ClimaMeteo_g[['GhAvg','GhMax']].values
    ClimaAnualMin.loc[indices_coincidentes_3_v.to_list(),['Met_VVextAvg','Met_VVextMax','Met_VVextSdev','Met_DVextAvg','Met_DVextMax','Met_DVextSde']]=ClimaMeteo_v[['VVextAvg','VVextMax','VVextSdev','DVextAvg','DVextMax','DVextSde']].values
    #Se genera el archivo excel
    os.chdir(ruta)
    filenameRell=localizacion[0]+'yMet_'+Anio[i]+'_Min.xlsx'
    ClimaAnualMin.to_excel(filenameRell,index=False, engine='openpyxl', na_rep='NaN')
    ClimaAnualMin['Gh'] = np.where(pd.isna(EOT['Gh_0']), ClimaAnualMin['Gh'], EOT['Gh_0'])
    filenameRellEOT=localizacion[0]+'yMet_'+Anio[i]+'_Min_EOT.xlsx'
    ClimaAnualMin.to_excel(filenameRellEOT,index=False, engine='openpyxl', na_rep='NaN')