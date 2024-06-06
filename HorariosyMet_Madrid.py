# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:28:22 2024

@author: ferma
"""
import os
import pandas as pd
import numpy as np
localizacion=['Madrid']
Anio=['2021','2022','2023']
#Define una función para filtrar outliers


#Hace un bucle para cada año
ruta1='D:\\Clima\\'+localizacion[0]+'\\Horarios'
os.chdir(ruta1)
for i in range(len(Anio)):
    filenameHor=localizacion[0]+'_'+Anio[i]+'_Hor_EOT.xlsx'
    ClimaAnualOrigen=pd.read_excel(filenameHor)
    ruta='D:\\Clima\\'+localizacion[0]+'\\Minutales'
    os.chdir(ruta)
    filenameMin=localizacion[0]+'yMet_'+Anio[i]+'_Min_EOT.xlsx'
    ClimaAnual=pd.read_excel(filenameMin) #genera el dataframe a partir del excel minutal
    ClimaAnual['AñoMesDiaHora']=ClimaAnual.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}-{row['Hora']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
    ClimaAnual.drop(['Año','Mes','Dia','Hora','Min'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
    ClimaAnual['AñoMesDiaHora']=pd.to_datetime(ClimaAnual['AñoMesDiaHora'], format='%Y.0-%m.0-%d.0-%H.0') # ordena las columnas en formato horario
    
    
    #se realizan las operaciones pertinentes agrupando por cada hora
    ClimaAnualHorario = ClimaAnual.groupby('AñoMesDiaHora').agg({
        'Met_TextAvg': ['mean', 'max', 'min', 'count'],
        'Met_HextAvg': ['mean', 'max', 'min', 'count'],
        'Met_GhAvg': ['mean', 'max', 'min',  'count'],
        'Met_VVextAvg': ['mean', 'max', 'min', 'count'],
        
    })
    ClimaAnualHorario.reset_index(inplace=True) #reestablece los índices
    ClimaAnualHorario = ClimaAnualHorario.drop(ClimaAnualHorario.columns[0], axis=1) #se elimina la columna previamente creada AñoMesDiaMin
    ClimaAnualHorario.columns=['Text_prm_Meteo','Text_max_Meteo','Text_min_Meteo','Text_num_Meteo',
                'Hext_prm_Meteo','Hext_max_Meteo','Hext_min_Meteo','Hext_num_Meteo',
                'Gh_prm_Meteo','Gh_max_Meteo','Gh_min_Meteo','Gh_num_Meteo',
                'VVext_prm_Meteo','VVext_max_Meteo','VVext_min_Meteo','VVext_num_Meteo']
    #se nombran las columnas correctamente con los datos tratados
    
    ClimaAnualHorario=pd.concat([ClimaAnualOrigen,ClimaAnualHorario],axis=1)
    #se nombran de nuevo una vez están todas las columnas del df(dataframe) final
    os.chdir(ruta1)
    #se genera el excel
    ClimaAnualHorario.to_excel(localizacion[0]+'yMet_'+Anio[i]+'_EOT_Hor.xlsx',index=False, engine='openpyxl', na_rep='NaN')


    
        