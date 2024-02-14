# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os


import numpy as np 
import pandas as pd
import warnings
from datetime import datetime, timedelta
import math
import time
#Acceso al directorio de archivos .txt
#IDENTIFICAR EL NOMBRE DE LA LOCALIZACION Y EL PERIODO A ANALIZAR
start_time = time.time()
localizacion=[]
localizacion=['PSA']
Anio=np.array([])
clima=[]
Anio=np.array([2021,2022,2023])
# ## GENERACIÓN MATRICES CLIMA 
#  #for i=1:size (localizacion,1)
ruta:str='D:\\Clima\\'+ localizacion[0]+'\\Datosoriginales'
os.chdir(ruta)
# #Función para generar un dataframe que se introducirá en el excel
# def generar_dataframe(anio):
#     Fecha_de_inicio = datetime(year=anio, month=1, day=1, hour=0, minute=0)
#     Fecha_de_final = datetime(year=anio, month=12, day=31, hour=23, minute=59)
#     # Genera un dataframe de fechas separadas cada minuto
#     Rango_de_dias = pd.date_range(start=Fecha_de_inicio, end=Fecha_de_final, freq='T')
#     # Crea un dataframe con año, mes, día, hora, minuto y siete otras variables que de momento aparecen vacías
#     df = pd.DataFrame({
#         'Año': Rango_de_dias.year,
#         'Mes': Rango_de_dias.month,
#         'Dia': Rango_de_dias.day,
#         'Hora': Rango_de_dias.hour,
#         'Min': Rango_de_dias.minute,
#         'Text': [float('nan')] * len(Rango_de_dias),
#         'H_ext': [float('nan')] * len(Rango_de_dias),
#         'Gh': [float('nan')] * len(Rango_de_dias),
#         'VVext': [float('nan')] * len(Rango_de_dias),
#         'DVext': [float('nan')] * len(Rango_de_dias),
#         'Gv': [float('nan')] * len(Rango_de_dias),
#         'R': [float('nan')] * len(Rango_de_dias)
#     })
#     return df

anio_introducido = Anio[2]
os.chdir(ruta)
# filenameRellNul=localizacion[0]+'_'+str(anio_introducido)+'_Min_Nul.xlsx'
# #Funcion para guardar el dataframe en un excel
# def save_to_excel(dataframe, excel_filename=filenameRellNul):
#     dataframe.to_excel(excel_filename, index=False, engine='openpyxl', na_rep='NaN')

# # Generar el dataframe para ese año
# minutal_dataframe = generar_dataframe(anio_introducido)
# # Guardar el dataframe en un excel
# save_to_excel(minutal_dataframe)

#%%
filenameClimaTrat=localizacion[0]+'_'+str(anio_introducido)+'_Min_Nul.xlsx' #Nombre del excel
ClimaTrat=pd.read_excel(filenameClimaTrat) #Lee el excel y lo guarda en un dataframe
# Se generan cuales son las filas que no están como NaN en ClimaTrat, se ordenan y cuántas son
fila = ClimaTrat.index[~ClimaTrat.iloc[:, 0].isna()].tolist() # genera un array con todas las líneas del excel en caso de que sea un nº el año
dia = np.unique(fila) #un array con el nº de líneas de fila
md = len(dia) #se obtiene la longitud de dia
climaARFRISOL=pd.DataFrame()
climaNumARFRISOL=pd.DataFrame() #se crean 6 dataframes vacíos a rellenar
climaMonitorizacion=pd.DataFrame()
climaNumMonitorizacion=pd.DataFrame()
temp7=pd.DataFrame(columns=range(11))
temp8=pd.DataFrame(columns=range(11))
for a in range(md):
    if a==0 or ClimaTrat.iloc[dia[a],2]!=ClimaTrat.iloc[dia[a-1],2]: #el primer día o si se cambia de día
        ClimaTrat.iloc[dia[a],2] #se indica el día en el que se está
        indfichARFRISOL=0 # se inicializan a cero
        indfichMonitorizacion=0
        #se pone el nombre del mes y día y se cambia en caso de los meses y días con un solo dígito
        if len(str(ClimaTrat.iloc[dia[a],1]))==1:
            mesname='0'+str(ClimaTrat.iloc[dia[a],1])
        else:
            mesname=str(ClimaTrat.iloc[dia[a],1])
        if len(str(ClimaTrat.iloc[dia[a],2]))==1:
            dianame='0'+str(ClimaTrat.iloc[dia[a],2])
        else:
            dianame=str(ClimaTrat.iloc[dia[a],2])
        #Primeraopción:Aplicación Arfrisol
        ruta2='D:\\Clima\\'+localizacion[0]+'\\DatosOriginales\\Adquisición\\diarios\\'+str(Anio[2])+'\\'+str(Anio[2])+'_min'
        os.chdir(ruta2)  
        nameArfrisol='ARFRISOL_SP4_'+str(ClimaTrat.iloc[dia[a],0])+mesname+dianame+'_min.txt' #nombre del archivo tipo ARFRISOL
        listaARFRISOLH= os.listdir(ruta2) #lista con todos los nombres de archivos en el directorio ruta 2
        if nameArfrisol in listaARFRISOLH:
            indfichARFRISOL=1
            temp= pd.DataFrame(np.loadtxt(nameArfrisol,dtype=str,delimiter=';')) #genera el dataframe a partir del txt
            temp.columns=['a'] #cambia el nombre a la columna para poder trabajar con ella
            cabeceratemp=pd.Series(temp.iloc[1,0]).str.split(pat='\t',expand=True) #divide la segunda línea por espacios
            if cabeceratemp.shape[1]<10:
                print(f'no hay cabecera el {dianame} del {mesname}-a')
            else: 
                columna=cabeceratemp.isin(['Fecha','Hora','Text','H_ext','VVext','DVext','Gv','Gh','R']) 
                #identifica las columnas en las que coincide con el nombre de algunas de esas magnitudes 
                Index=np.where(columna==True)[1] #números de las columnas que cumplen que coincidan con las magnitudes previamente mencionadas
                df_divididas =temp['a'].iloc[4:].str.split(expand=True) #divide las columnas desde la 5 fila
                temp2 = pd.DataFrame(index=df_divididas.index) #genera el indice del dataframe
                temp2 = pd.concat([temp2, df_divididas], axis=1) #une el indice mas las filas divididas 
                if temp2.shape[0]==1:
                    print(f'solo hay un valor el {dianame} del {mesname}-m')
                else:           
                    temp3= temp2.iloc[:,Index] #extrae los datos de las columnas que nos interesa
                    temp4=pd.Series(temp3.iloc[:,0]).str.split(pat='-',expand=True) #extrae los datos de fecha y los divide por guiones
                    temp4=temp4[list(temp4.columns[::-1])] #cambia el orden al formato Año Mes Día
                    temp5=pd.Series(temp3.iloc[:,1]).str.split(pat=':',expand=True) #extrae los datos de hora y los divide por guiones
                    temp5=temp5.iloc[:,:2] #cambia el orden al formato hora min
                    temp6=pd.concat([temp4,temp5,temp3.iloc[:,2:]],axis=1) #une todos los dataframes
                    if temp6.shape[0]!=1440: #en caso de que el dataframe generado no contenga todos los minutos
                        print(f'Hay un error el {dianame} del {mesname}-a')
                        if temp6.shape[1]==11:
                            temp7.columns=temp6.columns
                            temp7=pd.concat([temp7,temp6])#uno cuando faltan minutos
                        else:
                            print('El error es que no están definidas todas las magnitudes en el archivo-a')
                            temp6=pd.DataFrame(columns=range(11))
                    temp6.columns=['Año','Mes','Dia', 'Hora', 'Min','Text','H_ext','VVext','DVext','Gv','Gh' ] 
                    climaARFRISOL=pd.concat([climaARFRISOL,temp6],axis=0) #genera una matriz uniendo los dataframes de cada dia
        else: #cuando no existe el archivo
            print(f'Faltan los datos del {dianame} del {mesname}-a')
        #SegundaOpción:leer archivo monitorizacionciemat
        ruta3='D:\\Clima\\'+localizacion[0]+'\\DatosOriginales\\monitorizacionciemat\\'+str(Anio[2])
        os.chdir(ruta3)
        listaMonitorizacionH=os.listdir(ruta3)
        nameMonitorizacion=dianame+'-'+mesname+'-'+str(Anio[2])+'.txt'
        if nameMonitorizacion in listaMonitorizacionH:
            indfichMonitorizacion=1
            temp= pd.DataFrame(np.loadtxt(nameMonitorizacion,dtype=str,delimiter=';')) #genera el dataframe a partir del txt
            temp.columns=['a'] #cambia el nombre a la columna para poder trabajar con ella
            cabeceratemp=pd.Series(temp.iloc[0,0]).str.split(pat='\t',expand=True) #divide la segunda línea por espacios
            if cabeceratemp.shape[1]<10:
                print(f'no hay cabecera el {dianame} del {mesname}-m')
            else:
                columna=cabeceratemp.isin(['Hora','Text','H_ext','VVext','DVext','Gv','Gh'])
                #identifica las columnas en las que coincide con el nombre de algunas de esas magnitudes 
                Index=np.where(columna==True)[1] #números de las columnas que cumplen que coincidan con las magnitudes previamente mencionadas
                df_divididas =temp['a'].iloc[2:].str.split(expand=True) #divide las columnas desde la 3 fila
                temp2 = pd.DataFrame(index=df_divididas.index) #genera el indice del dataframe
                temp2 = pd.concat([temp2, df_divididas], axis=1) #une el indice mas las filas divididas 
                if temp2.shape[0]==1:
                    print(f'solo hay un valor el {dianame} del {mesname}-m')
                else:           
                    temp3= temp2.iloc[:,Index] #extrae los datos de las columnas que nos interesa
                    temp4=pd.Series(temp3.iloc[:,0]).str.split(pat=':',expand=True) #extrae los datos de hora y los divide por:
                    temp5=pd.DataFrame({'Año':[Anio[2]]*len(temp2.index),'Mes':[mesname]*len(temp2.index),'Dia':[dianame]*len(temp2.index)},index=temp2.index) #genera las fechas en función del nº de datos que se tenga
                    temp6=pd.concat([temp5,temp4,temp3.iloc[:,1:]],axis=1) #une todos los dataframes
                    if temp6.shape[0]!=1440:
                        print(f'Hay un error el {dianame} del {mesname}-m')
                        if temp6.shape[1]==11:
                            temp8.columns=temp6.columns
                            temp8=pd.concat([temp8,temp6])#uno cuando faltan minutos
                        else:
                            print('El error es que no están definidas todas las magnitudes en el archivo-m')
                            temp6=pd.DataFrame(columns=range(11))
                    temp6.columns=['Año','Mes','Dia', 'Hora', 'Min','Text','H_ext','VVext','DVext','Gv','Gh' ]
                    climaMonitorizacion=pd.concat([climaMonitorizacion,temp6],axis=0) #genera una matriz uniendo los dataframes de cada dia
        else:
            print(f'Faltan los datos del {dianame} del {mesname}-m')
                    
if not climaARFRISOL.empty: #en caso de que no este vacio el archivo 
    climaNumARFRISOL=climaARFRISOL.astype(float) #cambia el tipo de dato de ser str a float
    ##Validación valores Text,H,VVext,DVext,Gv y Gh
    #Validación Rango Temperatura: -40 a 60ºC
    climaNumARFRISOL.loc[climaNumARFRISOL['Text']>60.0 ,'Text']=math.nan
    climaNumARFRISOL.loc[climaNumARFRISOL['Text']<-40.0,'Text']=math.nan
    # Validación Rango humedad relativa: 0 a 100 %
    climaNumARFRISOL.loc[climaNumARFRISOL['H_ext']>100.5,'H_ext']=math.nan
    climaNumARFRISOL.loc[climaNumARFRISOL['H_ext']<-0.5,'H_ext']=math.nan
    climaNumARFRISOL.loc[(climaNumARFRISOL['H_ext']>100.0) & (climaNumARFRISOL['H_ext']<100.5),'H_ext']=100.0
    climaNumARFRISOL.loc[(climaNumARFRISOL['H_ext']<0.0) & (climaNumARFRISOL['H_ext']>-0.5),'H_ext']=0.0
    # Validación Rango velocidad viento: 0 a 30 %
    climaNumARFRISOL.loc[climaNumARFRISOL['VVext']>30.5,'VVext']=math.nan  
    climaNumARFRISOL.loc[climaNumARFRISOL['VVext']<-0.5,'VVext']=math.nan 
    climaNumARFRISOL.loc[(climaNumARFRISOL['VVext']>30) & (climaNumARFRISOL['VVext']<30.5),'VVext']=30.0
    climaNumARFRISOL.loc[(climaNumARFRISOL['VVext']>-0.5) & (climaNumARFRISOL['VVext']<0.0),'VVext']=0.0
    # Validación Rango dirección viento: 0 a 365 %
    climaNumARFRISOL.loc[climaNumARFRISOL['DVext']>360.5,'DVext']=math.nan  
    climaNumARFRISOL.loc[climaNumARFRISOL['DVext']<-0.5,'DVext']=math.nan 
    climaNumARFRISOL.loc[(climaNumARFRISOL['DVext']>360) & (climaNumARFRISOL['DVext']<360.5),'DVext']=360.0
    climaNumARFRISOL.loc[(climaNumARFRISOL['DVext']>-0.5) & (climaNumARFRISOL['DVext']<0.0),'DVext']=0.0
    # Validación Rango Gh: 0 a 1500 W/m^2
    climaNumARFRISOL.loc[climaNumARFRISOL['Gh']>1500.0,'Gh']=math.nan  
    climaNumARFRISOL.loc[climaNumARFRISOL['Gh']<-5.0,'Gh']=math.nan 
    climaNumARFRISOL.loc[(climaNumARFRISOL['Gh']>-5.0) & (climaNumARFRISOL['Gh']<0.0),'Gh']=0.0
    # Validación Rango Gv: 0 a 1500 W/m^2
    climaNumARFRISOL.loc[climaNumARFRISOL['Gv']>1500.0,'Gv']=math.nan  
    climaNumARFRISOL.loc[climaNumARFRISOL['Gv']<-5.0,'Gv']=math.nan 
    climaNumARFRISOL.loc[(climaNumARFRISOL['Gv']>-5.0) & (climaNumARFRISOL['Gv']<0.0),'Gv']=0.0
if not climaMonitorizacion.empty: #en caso de que no este vacio el archivo 
    climaNumMonitorizacion=climaMonitorizacion.copy()
    climaNumMonitorizacion[['Mes','Dia', 'Hora', 'Min','Text','H_ext','VVext','DVext','Gv','Gh']] = (climaNumMonitorizacion
         [['Mes','Dia', 'Hora', 'Min','Text','H_ext','VVext','DVext','Gv','Gh']].apply(lambda x: x.str.replace(',', '.')).astype(float)) #cambia el tipo de dato de str a float cuando es str
    ##Validación valores Text,H,VVext,DVext,Gv y Gh
    #Validación Rango Temperatura: -40 a 60ºC
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Text']>60.0 ,'Text']=math.nan
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Text']<-40.0,'Text']=math.nan
    # Validación Rango humedad relativa: 0 a 100 %
    climaNumMonitorizacion.loc[climaNumMonitorizacion['H_ext']>100.5,'H_ext']=math.nan
    climaNumMonitorizacion.loc[climaNumMonitorizacion['H_ext']<-0.5,'H_ext']=math.nan
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['H_ext']>100.0) & (climaNumMonitorizacion['H_ext']<100.5),'H_ext']=100.0
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['H_ext']<0.0) & (climaNumMonitorizacion['H_ext']>-0.5),'H_ext']=0.0
    # Validación Rango velocidad viento: 0 a 30 %
    climaNumMonitorizacion.loc[climaNumMonitorizacion['VVext']>30.5,'VVext']=math.nan  
    climaNumMonitorizacion.loc[climaNumMonitorizacion['VVext']<-0.5,'VVext']=math.nan 
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['VVext']>30) & (climaNumMonitorizacion['VVext']<30.5),'VVext']=30.0
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['VVext']>-0.5) & (climaNumMonitorizacion['VVext']<0.0),'VVext']=0.0
    # Validación Rango dirección viento: 0 a 365 %
    climaNumMonitorizacion.loc[climaNumMonitorizacion['DVext']>360.5,'DVext']=math.nan  
    climaNumMonitorizacion.loc[climaNumMonitorizacion['DVext']<-0.5,'DVext']=math.nan 
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['DVext']>360) & (climaNumMonitorizacion['DVext']<360.5),'DVext']=360.0
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['DVext']>-0.5) & (climaNumMonitorizacion['DVext']<0.0),'DVext']=0.0
    # Validación Rango Gh: 0 a 1500 W/m^2
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Gh']>1500.0,'Gh']=math.nan  
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Gh']<-5.0,'Gh']=math.nan 
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['Gh']>-5.0) & (climaNumMonitorizacion['Gh']<0.0),'Gh']=0.0
    # Validación Rango Gv: 0 a 1500 W/m^2
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Gv']>1500.0,'Gv']=math.nan  
    climaNumMonitorizacion.loc[climaNumMonitorizacion['Gv']<-5.0,'Gv']=math.nan 
    climaNumMonitorizacion.loc[(climaNumMonitorizacion['Gv']>-5.0) & (climaNumMonitorizacion['Gv']<0.0),'Gv']=0.0
#Filtrado de los dataframes
climaNumARFRISOL_no_cero = climaNumARFRISOL.loc[(climaNumARFRISOL.iloc[:, -5:] != 0).any(axis=1)] #identifica los datos no nulos
climaNumARFRISOL_cero = climaNumARFRISOL.loc[(climaNumARFRISOL.iloc[:, -5:] == 0).all(axis=1)] #identifica los datos nulos
filas_duplicadas_ARFRISOL= (climaNumARFRISOL_no_cero.iloc[:, :5].eq(climaNumARFRISOL_no_cero.iloc[:, :5].shift())).all(axis=1) #identifica las filas con fecha duplicada
climaNumARFRISOL_filtrado=climaNumARFRISOL_no_cero[~filas_duplicadas_ARFRISOL] #selecciona las fechas no duplicadas
R=pd.DataFrame({'R':[0]*len(climaNumARFRISOL_filtrado.index)},index=climaNumARFRISOL_filtrado.index) #se crea la columna R con valor 0
climaNumARFRISOL_filtrado=pd.concat([climaNumARFRISOL_filtrado,R],axis=1) #se añade la columna R
climaNumMonitorizacion_no_cero = climaNumMonitorizacion.loc[(climaNumMonitorizacion.iloc[:, -5:] != 0).any(axis=1)]
climaNumMonitorizacion_cero = climaNumMonitorizacion.loc[(climaNumMonitorizacion.iloc[:, -5:] == 0).all(axis=1)]
filas_duplicadas_Monitorizacion= (climaNumMonitorizacion_no_cero.iloc[:, :5].eq(climaNumMonitorizacion_no_cero.iloc[:, :5].shift())).all(axis=1)
climaNumMonitorizacion_filtrado=climaNumMonitorizacion_no_cero[~filas_duplicadas_Monitorizacion]
R=pd.DataFrame({'R':[1]*len(climaNumMonitorizacion_filtrado.index)},index=climaNumMonitorizacion_filtrado.index)
climaNumMonitorizacion_filtrado=pd.concat([climaNumMonitorizacion_filtrado,R],axis=1)
climaNumARFRISOL_filtrado=climaNumARFRISOL_filtrado[['Año','Mes','Dia', 'Hora', 'Min','Text','H_ext','Gh','VVext','DVext','Gv','R']] #se reestructuran las columnas acorde a ClimaTrat
climaNumMonitorizacion_filtrado=climaNumMonitorizacion_filtrado[['Año','Mes','Dia', 'Hora', 'Min','Text','H_ext','Gh','VVext','DVext','Gv','R']]
climaNumARFRISOL_filtrado.set_index(['Año','Mes','Dia', 'Hora', 'Min',],inplace=True) #se establecen las primeras cinco filas como indices
climaNumMonitorizacion_filtrado.set_index(['Año','Mes','Dia', 'Hora', 'Min'],inplace=True)
ClimaTrat.set_index(['Año','Mes','Dia', 'Hora', 'Min'],inplace=True)
#se sustituye la fila de ClimaTrat por la de ClimaARFRISOL primero y luego ClimaMonitorizacion en caso de que coincida la fecha. ClimaMonitorizacion solo sustituye en caso de que no haya dato de ClimaArfrisol
for index, fila in climaNumARFRISOL_filtrado.iterrows():
    if index in ClimaTrat.index:
        ClimaTrat.loc[index]=fila
for index, fila in climaNumMonitorizacion_filtrado.iterrows():
    if index in ClimaTrat.index:
        if ClimaTrat.loc[index,'Text':].isnull().all():
            ClimaTrat.loc[index]=fila
ClimaTrat.reset_index(inplace=True)
ClimaTrat.columns=['Año','Mes','Dia', 'Hora', 'Min','Text','Hext','Gh','VVext','DVext','Gv','R' ] #se cambia el nombre de las columnas
os.chdir(ruta)
ClimaTrat.to_excel(localizacion[0]+'_'+str(Anio[2])+'.xlsx',index=False, engine='openpyxl', na_rep='NaN') #se crea el excel


end_time = time.time()

# Calcula la diferencia para obtener el tiempo total
execution_time = end_time - start_time


    
    
    
    
    