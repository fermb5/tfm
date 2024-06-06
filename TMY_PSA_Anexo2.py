# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:37:02 2024

@author: ferma
"""

import os
import pandas as pd
import numpy as np
import calendar
#Se elige la localización y los años empleados para la elaboración del TMY
localizacion=['PSA']

Anio=['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
#Se generan las variables a rellenar
CDFLT=pd.DataFrame()

#se definen los días que puede haber cada mes
dias_por_mes_esperados = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}
#se crea un df en el que se obtienen las medias diarias para todos los años. 
for i in range(len(Anio)):
    ruta='D:\\Clima\\'+localizacion[0]+'\\Diarios'
    os.chdir(ruta)
    filenameDiario='PSAyMet_'+Anio[i]+'_Dia.xlsx'
    ClimaDia=pd.read_excel(filenameDiario)
    ClimaDia=ClimaDia[['Año','Mes','Dia','Text_prm','Hext_prm','Gh_prm']]
    CDFLT=pd.concat([CDFLT,ClimaDia])
CDFLT['MesDia']=CDFLT.apply(lambda row: f"{row['Mes']}-{row['Dia']}", axis=1)
CDFLT['MesDia']=pd.to_datetime(CDFLT['MesDia'], format='%m.0-%d.0')
CDFLT = CDFLT.groupby('MesDia').agg({
        'Text_prm': ['mean'],'Hext_prm':['mean'],'Gh_prm': ['mean']
    })
#Se genera la columna CDLF
CDFLT.reset_index(inplace=True,drop=True)
dias_del_año = pd.date_range(start='2023-01-01', end='2023-12-31')
meses = dias_del_año.month
dias = dias_del_año.day
# Crear un DataFrame con las columnas 'Mes' y 'Día'
df_dias_del_año = pd.DataFrame({'Mes': meses, 'Día': dias})
df_dias_del_año.reset_index(inplace=False)
CDFLT[['Mes','Dia']]=df_dias_del_año.iloc[:,:]
K_LT_T=pd.DataFrame()
K_LT_H=pd.DataFrame()
K_LT_G=pd.DataFrame()
J_ST_T=pd.DataFrame()
J_ST_H=pd.DataFrame()
J_ST_G=pd.DataFrame()
CDFST_CDF_T_final=pd.DataFrame()
CDFLT_CDF_T_final=pd.DataFrame()
CDFST_CDF_H_final=pd.DataFrame()
CDFLT_CDF_H_final=pd.DataFrame()
CDFST_CDF_G_final=pd.DataFrame()
CDFLT_CDF_G_final=pd.DataFrame()
filenameDiario2='PSAyMet_'+Anio[14]+'_Dia.xlsx'
CDFST=pd.read_excel(filenameDiario2)
CDFST=CDFST[['Mes','Dia','Text_prm','Hext_prm','Gh_prm']]
CDFST=CDFST.dropna()
dias_por_mes = CDFST.groupby('Mes')['Dia'].transform('count')
CDFST['Diferencia_Dias'] = CDFST['Mes'].map(dias_por_mes_esperados) - dias_por_mes

# Filtrar los meses que tienen una diferencia mayor que 5
meses_a_eliminar = CDFST['Mes'][CDFST['Diferencia_Dias'] > 5].unique()
CDFST = CDFST[~CDFST['Mes'].isin(meses_a_eliminar)]

CDFST['Posicion'] = CDFST.groupby('Mes')['Dia'].rank(method='first')
# Contar el número total de días en cada mes
dias_por_mes_filtrado = CDFST.groupby('Mes')['Dia'].transform('count')
# Crear la nueva columna
CDFST['CDF'] = CDFST['Posicion'] / dias_por_mes_filtrado
# Eliminar la columna de diferencia de días ya que no es necesaria en el resultado final
CDFST = CDFST.drop(columns=['Posicion','Diferencia_Dias'])
CDFLT=CDFLT.loc[CDFST.index]
CDFLT['CDF']=CDFST['CDF']
gruposL_por_mes=CDFLT.groupby('Mes')
gruposS_por_mes = CDFST.groupby('Mes')
# Crear un diccionario para almacenar los DataFrames de cada mes
CDFLT_por_mes = {mes: gruposL_por_mes.get_group(mes) for mes in gruposL_por_mes.groups}
# Se extraen los valores de 1 año cualquiera (podría hacerse un bucle para sacar todos los años a la vez)
# Crear un diccionario para almacenar los DataFrames de cada mes
CDFST_por_mes = {mes: gruposS_por_mes.get_group(mes) for mes in gruposS_por_mes.groups}
for j in range(1,13):
    if j in CDFLT_por_mes:
        #indices L
        indice_inicialL= CDFLT_por_mes[j].index[0]
        indice_finalL= CDFLT_por_mes[j].index[-1]+1
        indices_por_mes_L=CDFLT_por_mes[j].index
        CDFLT_por_mes[j].index=pd.RangeIndex(start=indice_inicialL, stop=indice_inicialL + len(CDFLT_por_mes[j]), step=1)
        #temperatura L
        CDFLT_sortedT=CDFLT_por_mes[j].sort_values(by=[('Text_prm','mean')])
        CDFLT_sortedT.reset_index(inplace=True,drop=False)
        CDFLT_sortedT['indicesordenados']=CDFLT_sortedT[('index','')].sort_values().reset_index(drop=True)
        CDFLT_sortedT= CDFLT_sortedT.set_index('indicesordenados')    
        CDFLT_sortedT=pd.concat([CDFLT_por_mes[j]['CDF'],CDFLT_sortedT[['index','CDF','Text_prm']]],axis=1)
        CDFLT_CDF_T=pd.DataFrame(np.zeros(CDFLT_sortedT.shape[0]))
        #humedad L
        CDFLT_sortedH=CDFLT_por_mes[j].sort_values(by=[('Hext_prm','mean')])
        CDFLT_sortedH.reset_index(inplace=True,drop=False)
        CDFLT_sortedH['indicesordenados']=CDFLT_sortedH[('index','')].sort_values().reset_index(drop=True)
        CDFLT_sortedH= CDFLT_sortedH.set_index('indicesordenados')    
        CDFLT_sortedH=pd.concat([CDFLT_por_mes[j]['CDF'],CDFLT_sortedH[['index','CDF','Hext_prm']]],axis=1)
        CDFLT_CDF_H=pd.DataFrame(np.zeros(CDFLT_sortedH.shape[0]))
        #radiación L
        CDFLT_sortedG=CDFLT_por_mes[j].sort_values(by=[('Gh_prm','mean')])
        CDFLT_sortedG.reset_index(inplace=True,drop=False)
        CDFLT_sortedG['indicesordenados']=CDFLT_sortedG[('index','')].sort_values().reset_index(drop=True)
        CDFLT_sortedG= CDFLT_sortedG.set_index('indicesordenados')    
        CDFLT_sortedG=pd.concat([CDFLT_por_mes[j]['CDF'],CDFLT_sortedG[['index','CDF','Gh_prm']]],axis=1)
        CDFLT_CDF_G=pd.DataFrame(np.zeros(CDFLT_sortedG.shape[0]))
        #Relleno cdflt
        for k in range(CDFLT_CDF_T.shape[0]):
            CDFLT_CDF_T.iloc[CDFLT_sortedT.iloc[k,1]-indice_inicialL,0]=CDFLT_sortedT.iloc[k,0]
            CDFLT_CDF_H.iloc[CDFLT_sortedH.iloc[k,1]-indice_inicialL,0]=CDFLT_sortedH.iloc[k,0]
            CDFLT_CDF_G.iloc[CDFLT_sortedG.iloc[k,1]-indice_inicialL,0]=CDFLT_sortedG.iloc[k,0]
        CDFLT_CDF_T.index=indices_por_mes_L
        CDFLT_CDF_H.index=indices_por_mes_L
        CDFLT_CDF_G.index=indices_por_mes_L
        #indices S
        indice_inicialS=CDFST_por_mes[j].index[0]
        indice_finalS=CDFST_por_mes[j].index[-1]+1
        indices_por_mes_S=CDFST_por_mes[j].index
        CDFST_por_mes[j].index=pd.RangeIndex(start=indice_inicialS, stop=indice_inicialS + len(CDFST_por_mes[j]), step=1)
        #temperatura S
        CDFST_sortedT=CDFST_por_mes[j].sort_values(by=['Text_prm'])
        CDFST_sortedT.reset_index(inplace=True,drop=False)
        CDFST_sortedT['indicesordenados']=CDFST_sortedT['index'].sort_values().reset_index(drop=True)
        CDFST_sortedT= CDFST_sortedT.set_index('indicesordenados') 
        CDFST_sortedT=pd.concat([CDFST_por_mes[j]['CDF'],CDFST_sortedT[['index','CDF','Text_prm']]],axis=1)
        CDFST_CDF_T=pd.DataFrame(np.zeros(CDFST_sortedT.shape[0]))
        CDFST_CDF_T['Index']=CDFST_sortedT['index'].sort_values().reset_index(drop=True)
        CDFST_CDF_T= CDFST_CDF_T.set_index('Index') 
        CDFST_CDF_T.index.name=None
        #humedad S
        CDFST_sortedH=CDFST_por_mes[j].sort_values(by=['Hext_prm'])
        CDFST_sortedH.reset_index(inplace=True,drop=False)
        CDFST_sortedH['indicesordenados']=CDFST_sortedH['index'].sort_values().reset_index(drop=True)
        CDFST_sortedH= CDFST_sortedH.set_index('indicesordenados') 
        CDFST_sortedH=pd.concat([CDFST_por_mes[j]['CDF'],CDFST_sortedH[['index','CDF','Hext_prm']]],axis=1)
        CDFST_CDF_H=pd.DataFrame(np.zeros(CDFST_sortedH.shape[0]))
        CDFST_CDF_H['Index']=CDFST_sortedH['index'].sort_values().reset_index(drop=True)
        CDFST_CDF_H= CDFST_CDF_H.set_index('Index') 
        CDFST_CDF_H.index.name=None
        #radiacion S
        CDFST_sortedG=CDFST_por_mes[j].sort_values(by=['Gh_prm'])
        CDFST_sortedG.reset_index(inplace=True,drop=False)
        CDFST_sortedG['indicesordenados']=CDFST_sortedG['index'].sort_values().reset_index(drop=True)
        CDFST_sortedG= CDFST_sortedG.set_index('indicesordenados') 
        CDFST_sortedG=pd.concat([CDFST_por_mes[j]['CDF'],CDFST_sortedG[['index','CDF','Gh_prm']]],axis=1)
        CDFST_CDF_G=pd.DataFrame(np.zeros(CDFST_sortedG.shape[0]))
        CDFST_CDF_G['Index']=CDFST_sortedG['index'].sort_values().reset_index(drop=True)
        CDFST_CDF_G= CDFST_CDF_G.set_index('Index') 
        CDFST_CDF_G.index.name=None
        #relleno cdfst
        for l in range(CDFST_CDF_T.shape[0]):
            CDFST_CDF_T.iloc[CDFST_sortedT.iloc[l,1]-indice_inicialS,0]=CDFST_sortedT.iloc[l,0]    
            CDFST_CDF_H.iloc[CDFST_sortedH.iloc[l,1]-indice_inicialS,0]=CDFST_sortedH.iloc[l,0]
            CDFST_CDF_G.iloc[CDFST_sortedG.iloc[l,1]-indice_inicialS,0]=CDFST_sortedG.iloc[l,0]
        CDFST_CDF_T.index=indices_por_mes_S
        CDFST_CDF_H.index=indices_por_mes_S
        CDFST_CDF_G.index=indices_por_mes_S
        #se definen las variables k, j, CDFLT y CDFST para t, h y g
        CDFLT_sortedT.index=indices_por_mes_L
        CDFLT_sortedH.index=indices_por_mes_L
        CDFLT_sortedG.index=indices_por_mes_L
        CDFST_sortedT.index=indices_por_mes_S
        CDFST_sortedH.index=indices_por_mes_S
        CDFST_sortedG.index=indices_por_mes_S
        K_LT_T=pd.concat([K_LT_T,CDFLT_sortedT[[('Text_prm','mean')]]])
        J_ST_T=pd.concat([J_ST_T,CDFST_sortedT['Text_prm']])
        CDFLT_CDF_T_final=pd.concat([CDFLT_CDF_T_final,CDFLT_CDF_T],axis=0)
        CDFST_CDF_T_final=pd.concat([CDFST_CDF_T_final,CDFST_CDF_T],axis=0)
        K_LT_H=pd.concat([K_LT_H,CDFLT_sortedH[[('Hext_prm','mean')]]])
        J_ST_H=pd.concat([J_ST_H,CDFST_sortedH['Hext_prm']])
        CDFLT_CDF_H_final=pd.concat([CDFLT_CDF_H_final,CDFLT_CDF_H],axis=0)
        CDFST_CDF_H_final=pd.concat([CDFST_CDF_H_final,CDFST_CDF_H],axis=0)
        K_LT_G=pd.concat([K_LT_G,CDFLT_sortedG[[('Gh_prm','mean')]]])
        J_ST_G=pd.concat([J_ST_G,CDFST_sortedG['Gh_prm']])
        CDFLT_CDF_G_final=pd.concat([CDFLT_CDF_G_final,CDFLT_CDF_G],axis=0)
        CDFST_CDF_G_final=pd.concat([CDFST_CDF_G_final,CDFST_CDF_G],axis=0)
# #se rellenan las tablas finales

tablafinalT=pd.concat([df_dias_del_año,CDFST[['CDF','Text_prm']],J_ST_T,CDFST_CDF_T_final,CDFLT[[('Text_prm','mean')]],K_LT_T,CDFLT_CDF_T_final],axis=1)
tablafinalT.columns=[['Mes','Dia','CDF','p_ST_Text','J_ST_Text','CDF_ST_Text','p_LT_Text','K_LT_Text','CDF_LT_Text']]

tablafinalH=pd.concat([df_dias_del_año,CDFST[['CDF','Hext_prm']],J_ST_H,CDFST_CDF_H_final,CDFLT[[('Hext_prm','mean')]],K_LT_H,CDFLT_CDF_H_final],axis=1)
tablafinalH.columns=[['Mes','Dia','CDF','p_ST_Hext','J_ST_Hext','CDF_ST_Hext','p_LT_Hext','K_LT_Hext','CDF_LT_Hext']]

tablafinalG=pd.concat([df_dias_del_año,CDFST[['CDF','Gh_prm']],J_ST_G,CDFST_CDF_G_final,CDFLT[[('Gh_prm','mean')]],K_LT_G[[('Gh_prm','mean')]],CDFLT_CDF_G_final],axis=1)
tablafinalG.columns=[['Mes','Dia','CDF','p_ST_Gh','J_ST_Gh','CDF_ST_Gh','p_LT_Gh','K_LT_Gh','CDF_LT_Gh']]
rutaAnexo2='D:\\Clima\\'+localizacion[0]+'\\TMY\\TablaAnexo2'
os.chdir(rutaAnexo2)
with pd.ExcelWriter('Tabla_Anexo2_'+str(Anio[14])+'.xlsx') as writer:
    # Guardar cada DataFrame en una hoja diferente
    tablafinalT.to_excel(writer, sheet_name='HojaT', index=False)
    tablafinalH.to_excel(writer, sheet_name='HojaH', index=False)
    tablafinalG.to_excel(writer, sheet_name='HojaG', index=False)