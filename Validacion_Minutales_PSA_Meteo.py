# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:08:16 2024

@author: ferma
"""

import os
import numpy as np 
import pandas as pd
import math

localizacion=['PSA']

ruta3='D:\\Clima\\'+localizacion[0]+'\\DatosPedidos'
os.chdir(ruta3)
ClimaPSA=pd.read_excel('PSAyMet_Min.xlsx',dtype=str)

if not ClimaPSA.empty: #en caso de que no este vacio el archivo 
    ClimaNumPSA=ClimaPSA.apply(lambda x: x.str.replace(',', '.')).astype(float) #cambia el tipo de dato de ser str a float
    #Validación valores Text,H,VVext,DVext,Gv y Gh
    # Validación Rango Temperatura: -40 a 60ºC
    ClimaNumPSA.loc[ClimaNumPSA['Text']>60.0 ,'Text']=math.nan
    ClimaNumPSA.loc[ClimaNumPSA['Text']<-20.0,'Text']=math.nan
    # Validación Rango humedad relativa: 0 a 100 %
    ClimaNumPSA.loc[ClimaNumPSA['Hext']>100.5 ,'Hext']=math.nan
    ClimaNumPSA.loc[ClimaNumPSA['Hext']<-0.5,'Hext']=math.nan
    ClimaNumPSA.loc[(ClimaNumPSA['Hext']>100.0) & (ClimaNumPSA['Hext']<100.5),'Hext']=100.0
    ClimaNumPSA.loc[(ClimaNumPSA['Hext']<0.0) & (ClimaNumPSA['Hext']>-0.5),'Hext']=0.0
    # Validación Rango velocidad viento: 0 a 30 %
    ClimaNumPSA.loc[ClimaNumPSA['VVext']>30.5,'VVext']=math.nan  
    ClimaNumPSA.loc[ClimaNumPSA['VVext']<-0.5,'VVext']=math.nan  
    ClimaNumPSA.loc[(ClimaNumPSA['VVext']>30) & (ClimaNumPSA['VVext']<30.5),'VVext']=30.0
    ClimaNumPSA.loc[(ClimaNumPSA['VVext']>-0.5) & (ClimaNumPSA['VVext']<0.0),'VVext']=0.0
    # Validación Rango dirección viento: 0 a 365 %
    ClimaNumPSA.loc[ClimaNumPSA['DVext']>360.5,'DVext']=math.nan  
    ClimaNumPSA.loc[ ClimaNumPSA['DVext']<-0.5,'DVext']=math.nan  
    ClimaNumPSA.loc[(ClimaNumPSA['DVext']>360) & (ClimaNumPSA['DVext']<360.5),'DVext']=360.0
    ClimaNumPSA.loc[(ClimaNumPSA['DVext']>-0.5) & (ClimaNumPSA['DVext']<0.0),'DVext']=0.0
    # Validación Rango Gh: 0 a 1500 W/m^2
    ClimaNumPSA.loc[ClimaNumPSA['Gh']>1500.0,'Gh' ]=math.nan  
    ClimaNumPSA.loc[ClimaNumPSA['Gh']<-5.0,'Gh' ]=math.nan 
    ClimaNumPSA.loc[(ClimaNumPSA['Gh']>-5.0) & (ClimaNumPSA['Gh']<0.0),'Gh']=0.0
ClimaNumPSA=ClimaNumPSA[['Año','Mes','Dia','Hora','Min','Text','Hext','Gh','VVext','DVext']]
os.chdir(ruta3)
filenameRell='Val_PSAyMet_min.xlsx'
ClimaNumPSA.to_excel(filenameRell, index=False, engine='openpyxl', na_rep='NaN')


        
