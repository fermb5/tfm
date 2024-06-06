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
#Hay que tener en cuenta que este programa es adecuado para el formato de meteogenica, no para otros
localizacion=['Madrid']
ruta2='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Datos_2021_2023'
os.chdir(ruta2)
#se define una función para ordenar correctamente los archivos en función de su fecha, (no trate el 01-10-2022 como anterior al 20-10-2021)
def obtener_fecha(nombre_archivo):
    partes = nombre_archivo.split('_')
    return datetime.strptime(f"{partes[1]}_{partes[2]}_{partes[3][:-4]}", "%d_%m_%Y")
listaMeteoH=os.listdir(ruta2) #obtiene los archivos del directorio
listaMeteoH=pd.DataFrame(sorted(listaMeteoH,key=obtener_fecha)) #ordena los archivos según su nombre
temp=pd.DataFrame()
temp7=pd.DataFrame()
for i in range(listaMeteoH.shape[0]): #bucle por todos los archivos del directorio
    temp1=pd.DataFrame(np.loadtxt(listaMeteoH.iloc[i,0],dtype=str,delimiter=';')) #genera un dataframe por cada archivo
    temp=pd.concat([temp,temp1],axis=0) #une cada dataframe nuevo al anterior para tener uno con todos los datos juntos
for j in range(temp.shape[0]):
    temp2=pd.Series(temp.iloc[j,1]).str.split(expand=True) #separa la columna FechaHora del dataframe por espacios
    if temp2.shape[1]==2:
        temp2.columns=['Fecha','Hora'] #asigna el nombre fecha hora si estuviesen separados
    else:
        temp2=pd.DataFrame({
            'Fecha':temp2.iloc[0,0],'Hora':'00:00'},index=[f'{j}'])
    temp3=pd.Series(temp2.iloc[0,0]).str.split(pat='/',expand=True)
    temp4=pd.Series(temp2.iloc[0,1]).str.split(pat=':',expand=True)
    #se separan la fecha y la hora
    if temp4.shape[1]==3:
        temp4=temp4[[0,1]] #se desprecian los segundos
        temp4.columns=[0,1]
    temp5=temp.iloc[[j],2:6] #datos que no tienen que ver con la fecha
    temp5.index=[0]
    temp6=pd.concat([pd.Series(temp.iloc[j,0]),temp3,temp4,temp5],axis=1) #une las diferentes columnas
    temp7=pd.concat([temp7,temp6]) #une cada dataframe nuevo al anterior para tener uno con todos los datos juntos
temp7.columns=['Estacion','Dia','Mes','Año','Hora','Min','NumParametro','NumFuncion','Valor','Control'] #nombra las columnas
filenameRell='MadridyMet_Min.xlsx'
temp7.to_excel(filenameRell, index=False, engine='openpyxl', na_rep='NaN') #genera el excel
    
    