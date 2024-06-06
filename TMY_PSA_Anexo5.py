# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:30:21 2024

@author: ferma
"""
import os
import pandas as pd
import numpy as np
import calendar
localizacion=['PSA']
VST=pd.DataFrame()
VLT=pd.DataFrame()
Anio=['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
nombre_meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

for i in range(len(Anio)):
    ruta='D:\\Clima\\'+localizacion[0]+'\\Diarios'
    os.chdir(ruta)
    filenameDiario='PSAyMet_'+Anio[i]+'_Dia.xlsx'
    ClimaDia=pd.read_excel(filenameDiario)
    ClimaDiaLT=ClimaDia[['Año','Mes','Dia','VVext_prm']]
    ClimaDiaST=ClimaDia[['VVext_prm']]
    ClimaDiaST.columns=[Anio[i]]
    VST=pd.concat([VST,ClimaDiaST],axis=1)
    VLT=pd.concat([VLT,ClimaDiaLT])    
VLT['MesDia']=VLT.apply(lambda row: f"{row['Mes']}-{row['Dia']}", axis=1)
VLT['MesDia']=pd.to_datetime(VLT['MesDia'], format='%m.0-%d.0')
VLT = VLT.groupby('MesDia').agg({
        'VVext_prm': ['mean']
    })
VLT.reset_index(inplace=True,drop=True)
dias_del_año = pd.date_range(start='2023-01-01', end='2023-12-31')
meses = dias_del_año.month
dias = dias_del_año.day
# Crear un DataFrame con las columnas 'Mes' y 'Día'
df_dias_del_año = pd.DataFrame({'Mes': meses, 'Día': dias})
df_dias_del_año.reset_index(inplace=False)
VLT[['Mes','Dia']]=df_dias_del_año.iloc[:,:]
VLT.columns=['V_LT','Mes','Dia']
VLT=pd.concat([VLT[['Mes','Dia']],VST,VLT['V_LT']],axis=1)

grupos_por_mes=VLT.groupby('Mes')
Anexo5_por_mes = {mes: grupos_por_mes.get_group(mes) for mes in grupos_por_mes.groups}

ruta2='D:\\Clima\\'+localizacion[0]+'\\TMY\\TablaAnexo4'
os.chdir(ruta2)
filenameAnexo4='Tabla_Anexo4.xlsx'
Anexo4=pd.read_excel(filenameAnexo4,header=None,dtype=str)
ruta3='D:\\Clima\\'+localizacion[0]+'\\TMY\\TablaAnexo5'
os.chdir(ruta3)
for j in range(1,13):
    Desv=pd.DataFrame()
    meses_elegidos=Anexo4.iloc[j-1,1:4].to_list()
    for k in range(len(meses_elegidos)):
        Desv[meses_elegidos[k]]=(Anexo5_por_mes[j][meses_elegidos[k]]-Anexo5_por_mes[j]['V_LT']).abs()
    Anexo5=pd.concat([Anexo5_por_mes[j],Desv],axis=1)
    sumatorio=Anexo5.iloc[:, -3:].sum()
    with pd.ExcelWriter('Tabla_Anexo5_'+nombre_meses[j-1]+'.xlsx') as writer:
        # Guardar cada DataFrame en una hoja diferente
        Anexo5.to_excel(writer, sheet_name='Anexo5', index=False)
        sumatorio.to_excel(writer, sheet_name='sumatorio', index=True)

        
        
        

