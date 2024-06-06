# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:08:16 2024

@author: ferma
"""

import os
import numpy as np 
import pandas as pd
import math

localizacion=['Madrid']
ruta2='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Excels_Diferentes_Datos'
os.chdir(ruta2)
filename='MadridyMet_Min.xlsx'
ClimaTrat=pd.read_excel(filename)
temp = ClimaTrat[(ClimaTrat.iloc[:, 0] == 343) & (ClimaTrat.iloc[:, 9] == 0)]
MeteoMin=pd.concat([temp.iloc[:,3],temp.iloc[:,2],temp.iloc[:,1],temp.iloc[:,4:-1]],axis=1)
MeteoMin['AñoMesDiaHoraMin']=MeteoMin['Año'].astype(str) + '-' + MeteoMin['Mes'].astype(str)+'-'+MeteoMin['Dia'].astype(str) +\
    '-' + MeteoMin['Hora'].astype(str)+'-'+MeteoMin['Min'].astype(str) #se reordena en año, mes, dia, hora y min
temp=pd.DataFrame(MeteoMin['AñoMesDiaHoraMin'].unique())
TextAvg=pd.DataFrame()
TextMax=pd.DataFrame()
TextMin=pd.DataFrame()
HextAvg=pd.DataFrame()
GhAvg=pd.DataFrame()
GhMax=pd.DataFrame()
VVextAvg=pd.DataFrame()
VVextMax=pd.DataFrame()
VVextSdev=pd.DataFrame()
DVextAvg=pd.DataFrame()
DVextSdev=pd.DataFrame()
DVextMax=pd.DataFrame()
#se asigna lo que significa cada num parámetro y num función a cada diferente variable
for i in range (MeteoMin.shape[0]):
    if MeteoMin.iloc[i,5]==6 and MeteoMin.iloc[i,6]==1:
        TextAvg=pd.concat([TextAvg,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==6 and MeteoMin.iloc[i,6]==4:
        TextMax=pd.concat([TextMax,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==6 and MeteoMin.iloc[i,6]==8:
        TextMin=pd.concat([TextMin,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==2 and MeteoMin.iloc[i,6]==1:
        HextAvg=pd.concat([HextAvg,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==67 and MeteoMin.iloc[i,6]==1:
        GhAvg=pd.concat([GhAvg,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==67 and MeteoMin.iloc[i,6]==4:
        GhMax=pd.concat([GhMax,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==7 and MeteoMin.iloc[i,6]==1:
        VVextAvg=pd.concat([VVextAvg,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==7 and MeteoMin.iloc[i,6]==4:
        VVextMax=pd.concat([VVextMax,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==7 and MeteoMin.iloc[i,6]==6:
        VVextSdev=pd.concat([VVextSdev,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==8 and MeteoMin.iloc[i,6]==1:
        DVextAvg=pd.concat([DVextAvg,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==8 and MeteoMin.iloc[i,6]==4:
        DVextMax=pd.concat([DVextMax,pd.Series(MeteoMin.iloc[i,7])])
    if MeteoMin.iloc[i,5]==8 and MeteoMin.iloc[i,6]==6:
        DVextSdev=pd.concat([DVextSdev,pd.Series(MeteoMin.iloc[i,7])])

temp=temp[0].str.split(pat='-',expand=True)
temp.set_index(pd.Index([0]*temp.shape[0]),inplace=True)
MeteoMinTotal=pd.concat([temp,TextAvg, TextMax, TextMin,HextAvg, GhAvg, GhMax, VVextAvg, VVextMax, VVextSdev, DVextAvg ,DVextMax ,DVextSdev],axis=1)
#se unen todas las variables
MeteoMinTotal.columns=['Año','Mes','Dia','Hora','Min','TextAvg','TextMax',
         'HextAvg','GhAvg','GhMax','VVextAvg','VVextMax','VVextSdev',
         'DVextAvg','DVextMax','DVextSde']
ruta3='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Excels_Diferentes_Datos'
os.chdir(ruta3)
ClimaCiematS2=pd.read_excel('MadridyCiematS2_Min.xlsx',dtype=str)
MeteoMinTotal=pd.concat([ClimaCiematS2,MeteoMinTotal],axis=0)
#se lee la otra fuente de datos y se une al df anterior
if not MeteoMinTotal.empty: #en caso de que no este vacio el archivo 
    MeteoNumMinTotal=MeteoMinTotal.apply(lambda x: x.str.replace(',', '.')).astype(float) #cambia el tipo de dato de ser str a float
    #Validación valores Text,H,VVext,DVext,Gv y Gh
    # Validación Rango Temperatura: -40 a 60ºC
    MeteoNumMinTotal.loc[MeteoNumMinTotal['TextAvg']>60.0 ,'TextAvg']=math.nan
    MeteoNumMinTotal.loc[MeteoNumMinTotal['TextAvg']<-40.0,'TextAvg']=math.nan
    MeteoNumMinTotal.loc[MeteoNumMinTotal['TextMax']>60.0 ,'TextMax']=math.nan
    MeteoNumMinTotal.loc[ MeteoNumMinTotal['TextMax']<-40.0,'TextMax']=math.nan
    # Validación Rango humedad relativa: 0 a 100 %
    MeteoNumMinTotal.loc[MeteoNumMinTotal['HextAvg']>100.5 ,'HextAvg']=math.nan
    MeteoNumMinTotal.loc[MeteoNumMinTotal['HextAvg']<-0.5,'HextAvg']=math.nan
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['HextAvg']>100.0) & (MeteoNumMinTotal['HextAvg']<100.5),'HextAvg']=100.0
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['HextAvg']<0.0) & (MeteoNumMinTotal['HextAvg']>-0.5),'HextAvg']=0.0
    # Validación Rango velocidad viento: 0 a 30 %
    MeteoNumMinTotal.loc[MeteoNumMinTotal['VVextAvg']>30.5,'VVextAvg']=math.nan  
    MeteoNumMinTotal.loc[MeteoNumMinTotal['VVextAvg']<-0.5,'VVextAvg']=math.nan  
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['VVextAvg']>30) & (MeteoNumMinTotal['VVextAvg']<30.5),'VVextAvg']=30.0
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['VVextAvg']>-0.5) & (MeteoNumMinTotal['VVextAvg']<0.0),'VVextAvg']=0.0
    MeteoNumMinTotal.loc[MeteoNumMinTotal['VVextMax']>30.5,'VVextMax']=math.nan  
    MeteoNumMinTotal.loc[MeteoNumMinTotal['VVextMax']<-0.5,'VVextMax']=math.nan 
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['VVextMax']>30) & (MeteoNumMinTotal['VVextMax']<30.5),'VVextMax']=30.0
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['VVextMax']>-0.5) & (MeteoNumMinTotal['VVextMax']<0.0),'VVextMax']=0.0
    # Validación Rango dirección viento: 0 a 365 %
    MeteoNumMinTotal.loc[MeteoNumMinTotal['DVextAvg']>360.5,'DVextAvg']=math.nan  
    MeteoNumMinTotal.loc[ MeteoNumMinTotal['DVextAvg']<-0.5,'DVextAvg']=math.nan  
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['DVextAvg']>360) & (MeteoNumMinTotal['DVextAvg']<360.5),'DVextAvg']=360.0
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['DVextAvg']>-0.5) & (MeteoNumMinTotal['DVextAvg']<0.0),'DVextAvg']=0.0
    MeteoNumMinTotal.loc[MeteoNumMinTotal['DVextMax']>360.5,'DVextMax']=math.nan
    MeteoNumMinTotal.loc[MeteoNumMinTotal['DVextMax']<-0.5,'DVextMax']=math.nan 
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['DVextMax']>360) & (MeteoNumMinTotal['DVextMax']<360.5),'DVextMax']=360.0
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['DVextMax']>-0.5) & (MeteoNumMinTotal['DVextMax']<0.0),'DVextMax']=0.0
    # Validación Rango Gh: 0 a 1500 W/m^2
    MeteoNumMinTotal.loc[MeteoNumMinTotal['GhAvg']>1500.0,'GhAvg' ]=math.nan  
    MeteoNumMinTotal.loc[MeteoNumMinTotal['GhAvg']<-5.0,'GhAvg' ]=math.nan 
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['GhAvg']>-5.0) & (MeteoNumMinTotal['GhAvg']<0.0),'GhAvg']=0.0
    MeteoNumMinTotal.loc[MeteoNumMinTotal['GhMax']>1500.0 ,'GhMax' ]=math.nan  
    MeteoNumMinTotal.loc[MeteoNumMinTotal['GhMax']<-5.0,'GhMax' ]=math.nan  
    MeteoNumMinTotal.loc[(MeteoNumMinTotal['GhMax']>-5.0) & (MeteoNumMinTotal['GhMax']<0.0),'GhMax']=0.0
rutaf='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Excels_Diferentes_Datos'
os.chdir(rutaf)
filenameRell='Val_MadridyMet_min.xlsx'
MeteoNumMinTotal.to_excel(filenameRell, index=False, engine='openpyxl', na_rep='NaN') #se genera el excel


        
