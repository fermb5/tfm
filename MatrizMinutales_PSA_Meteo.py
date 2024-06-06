# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:42:33 2024

@author: ferma
"""
import os
import numpy as np 
import pandas as pd
import math
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
# diferentes funciones para filtrar los outliers y los valores que se repiten 
# def eliminar_valores_repetidos_G(series):
#     prim_repeticiones=series[series.ne(0)].duplicated(keep='first') #matriz de booleanos que indica como false aquellos valores que salen por primera vez
#     repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0] #matriz que indica los índices de aquellos valores que ya han salido
#     tempin=np.empty(shape=2)
#     indices_cambio = series.index[series.diff().ne(0)] #matriz que indica los índices donde se cambia  de número
#     if len(repeticiiones>=5): #debe de haber mínimo cinco repeticiones
#         for i in range(4,len(repeticiiones)):
#             if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
#                 repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]: #se cumpla que las repeticiones sean seguidas
#                     tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
#                     tempin=np.vstack((tempin,tempint))
#         tempin=np.delete(tempin,0,axis=0) #se seleccionan diferencias de índices salvo la primera fila (está vacía)
#     for i in range(len(indices_cambio)-1): #se deben de respetar aquellos valores que han salido previamente, pero son un cambio de número. Ej: 1,2,2,2,2,¡1! no es un núm repetido
#         diferencia=indices_cambio[i+1]-indices_cambio[i]
#         if diferencia>5:
#             series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
#     return series
# #mismo criterio que la función anterior
# def eliminar_valores_repetidos_T(series):
#     prim_repeticiones=series.duplicated(keep='first')
#     repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0]
#     tempin=np.empty(shape=2)
#     indices_cambio = series.index[series.diff().ne(0)]
#     if len(repeticiiones>=10):
#         for i in range(4,len(repeticiiones)):
#             if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
#                 repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]:
#                     tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
#                     tempin=np.vstack((tempin,tempint))
#         tempin=np.delete(tempin,0,axis=0)
#     for i in range(len(indices_cambio)-1):
#         diferencia=indices_cambio[i+1]-indices_cambio[i]
#         if diferencia>5:
#             series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
#     return series
# def eliminar_valores_repetidos_H(series):
#     prim_repeticiones=series[series.ne(100)].duplicated(keep='first')
#     repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0]
#     tempin=np.empty(shape=2)
#     indices_cambio = series.index[series.diff().ne(0)]
#     if len(repeticiiones>=10):
#         for i in range(4,len(repeticiiones)):
#             if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
#                 repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]:
#                     tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
#                     tempin=np.vstack((tempin,tempint))
#         tempin=np.delete(tempin,0,axis=0)
#     for i in range(len(indices_cambio)-1):
#         diferencia=indices_cambio[i+1]-indices_cambio[i]
#         if diferencia>5:
#             series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
#     return series

localizacion=['PSA']
#Fuente 1
ruta2='D:\\Clima\\'+localizacion[0]+'\\DatosPedidos\\Fuente 1'
os.chdir(ruta2)
def obtener_fecha(nombre_archivo):
    partes = nombre_archivo.split('-')
    return datetime.strptime(f"{partes[0]}-{partes[1]}-{partes[2][:-4]}", "%d-%m-%Y")
listaMeteoH=os.listdir(ruta2)
listaMeteoH=pd.DataFrame(sorted(listaMeteoH,key=obtener_fecha))
temp=pd.DataFrame()
temp7=pd.DataFrame()
FechaFinal=pd.DataFrame()
for i in range(listaMeteoH.shape[0]):
    temp1=pd.DataFrame(np.loadtxt(listaMeteoH.iloc[i,0],dtype=str,delimiter=';'))
    Fecha=listaMeteoH.iloc[i,0]
    Fecha=Fecha.split('.')
    Fecha=Fecha[0].split('-')
    Fecha=pd.DataFrame([Fecha] * (len(temp1)-2), columns=['Dia', 'Mes', 'Año'])
    FechaFinal=pd.concat([FechaFinal,Fecha])
    FechaFinal=FechaFinal.reset_index(drop=True)
    temp1=pd.Series(temp1.iloc[:,0]).str.split(expand=True)
    cabeceratemp=pd.Series(temp1.iloc[0,:])
    columna=cabeceratemp.isin(['Hora','Met_Ig_horizontal_01','Met_Tae_01','Met_Humidity_01','Met_Vwind_10m','Met_Dwind_10m'])
    Index=np.where(columna==True)[0]
    temp2=temp1.iloc[:,Index]
    temp2=temp2.drop([0,1])
    temp2.columns=['Hora','Gh','Text','Hext','VVext','DVext']
    temp=pd.concat([temp,temp2],axis=0)
    if temp1.shape[0]!=1442:
        print(f'{listaMeteoH.iloc[i,0]}')
        print (f'{temp1.shape[0]}')
temp=temp.reset_index(drop=True)
HoraMin=pd.Series(temp.iloc[:,0]).str.split(pat=':',expand=True)
HoraMin.columns=['Hora','Min']
tempfinal=pd.concat([FechaFinal['Año'],FechaFinal['Mes'],FechaFinal['Dia'],HoraMin,temp[['Gh','Text','Hext','VVext','DVext']]],axis=1)
#fuente 2
ruta3='D:\\Clima\\'+localizacion[0]+'\\DatosPedidos\\Fuente 2'
os.chdir(ruta3)
listaCESA=pd.DataFrame(os.listdir(ruta3))
temp2final=pd.DataFrame()
for i in range(listaCESA.shape[0]):
    temp2=pd.read_excel(listaCESA.iloc[i,0],dtype=str)
    AñoMesDia2=pd.Series(temp2.iloc[:,0]).str.split(pat='-', expand=True)
    HoraMinSeg2=pd.Series(temp2.iloc[:,1]).str.split(pat=':',expand=True)
    Dia2=pd.Series(AñoMesDia2.iloc[:,2]).str.split(pat=' ', expand=True)
    FechaCompleta2=pd.concat([AñoMesDia2.iloc[:,0:2],Dia2.iloc[:,0],HoraMinSeg2],axis=1)
    FechaCompleta2.columns=['Año','Mes','Dia','Hora','Min','Seg']
    FechaCompleta2['Hora']=FechaCompleta2['Hora'].apply(lambda x: str(x).zfill(2))
    FechaCompleta2['Seg']=FechaCompleta2['Seg'].apply(lambda x: '{:08.6f}'.format(float(x.replace(',','.'))))
    FechaCompleta2['Fecha Completa']= FechaCompleta2.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}-{row['Hora']}-{row['Min']}-{row['Seg']}",axis=1)
    tiempo_local=pd.to_datetime(FechaCompleta2['Fecha Completa'],format='%Y-%m-%d-%H-%M-%S.%f')
    FechaCompleta2[['Mes','Dia']]=FechaCompleta2[['Mes','Dia']].astype(int)
    if FechaCompleta2.iloc[0,1] <= 2 or FechaCompleta2.iloc[0,1]==3 and FechaCompleta2.iloc[0,2]<31 or FechaCompleta2.iloc[0,1]>=11 or FechaCompleta2.iloc[0,1]==10 and FechaCompleta2.iloc[0,2]>=27:
        tiempo_ajustado=tiempo_local+pd.Timedelta(hours=1)
    else:
        tiempo_ajustado=tiempo_local+pd.Timedelta(hours=2)
    tiempo_ajustado=tiempo_ajustado.astype(str)
    FechaCompleta2=pd.Series(tiempo_ajustado.iloc[:]).str.split(pat=':', expand=True)
    FechaCompleta2['AñoMesDiaHoraMin']=FechaCompleta2.apply(lambda row: f"{row[0]}-{row[1]}", axis=1)
    temp2=pd.concat([FechaCompleta2['AñoMesDiaHoraMin'],temp2.iloc[:,2:]],axis=1)
    temp2.iloc[:,1:]=temp2.iloc[:,1:].astype(float)
    temp2=temp2.groupby('AñoMesDiaHoraMin').agg({'Radiación directa w/m2  SOL01A': ['mean'],
                        'Temperatura ambiente  TA001A':['mean'],'Humedad Relativa  HA001B':['mean'], 
                        'Velocidad de viento Km/h  VI001A':['mean'],'Dirección de viento  CG301':['mean']})
    temp2.reset_index(inplace=True,drop=False)
    AñoMesDiaHoraMin2=pd.Series(temp2.iloc[:,0]).str.split(pat='-',expand=True)
    DiaHora2=pd.Series(AñoMesDiaHoraMin2.iloc[:,2]).str.split(pat=' ',expand=True)
    temp2=pd.concat([AñoMesDiaHoraMin2.iloc[:,:2],DiaHora2,AñoMesDiaHoraMin2.iloc[:,3],temp2.iloc[:,1:]],axis=1)
    temp2.columns=['Año','Mes','Dia','Hora','Min','Gh','Text','Hext','VVext','DVext']
    temp2final=pd.concat([temp2final,temp2],axis=0)
temptotal=pd.concat([tempfinal,temp2final],axis=0)
# tempfinal=tempfinal.apply(pd.to_numeric,errors='coerce')
# tempfinal['AñoMesDiaHora']=tempfinal.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}-{row['Hora']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
# tempfinal.drop(['Año','Mes','Dia','Hora','Min'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal

# tempfinal['AñoMesDiaHora']=pd.to_datetime(tempfinal['AñoMesDiaHora'], format='%Y.0-%m.0-%d.0-%H.0') # ordena las columnas en formato horario
# tempfinal = tempfinal.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_G(col) if col.name == 'Gh' or col.name == 'Gv' else col))
# tempfinal = tempfinal.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_H(col) if col.name == 'Hext' else col))
# tempfinal = tempfinal.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_T(col) if col.name == 'Text'  else col))  
# if tempfinal.isna().any().any():
#     print("Hay al menos un NaN en el DataFrame.")
    
#     # Contar el número de NaN en cada columna
#     num_nan_por_columna = tempfinal.isna().sum()
#     print("Número de NaN por columna:")
#     print(num_nan_por_columna)
    
#     # Obtener los índices y columnas donde se encuentran los NaN
#     indices_nan = np.where(tempfinal.isna())
#     filas_nan = indices_nan[0]
#     columnas_nan = indices_nan[1]
    
#     print("Índices y columnas de los NaN:")
#     for i in range(len(filas_nan)):
#         fila = filas_nan[i]
#         columna = columnas_nan[i]
#         print("Fila:", fila, "| Columna:", columna)

# else:
#     print("No hay NaN en el DataFrame.")
ruta4='D:\\Clima\\'+localizacion[0]+'\\DatosPedidos'
os.chdir(ruta4)
filenameRell='PSAyMet_Min.xlsx'
temptotal.to_excel(filenameRell, index=False, engine='openpyxl', na_rep='NaN')
    
    