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
#Hay que tener en cuenta que este programa es adecuado para el formato de CiematS2, no para otros
localizacion=['Madrid']
ruta2='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Datos_Extras'
os.chdir(ruta2)
listaMeteoH=pd.DataFrame(os.listdir(ruta2))
temp=pd.DataFrame()
temp7=pd.DataFrame()
for i in range(listaMeteoH.shape[0]):
    skip_header = 1 if i > 0 else 0 #se elimina la columna de título en caso de que no sea el primer archivo
    temp1=pd.DataFrame(np.loadtxt(listaMeteoH.iloc[i,0],dtype=str,delimiter=';',skiprows=skip_header))
    temp=pd.concat([temp,temp1],axis=0)
temp=temp.iloc[:,:-1]
temp.columns=temp.iloc[0].apply(lambda palabra: palabra[:5]) #se restringe que la primera fila tenga por columna solo 5 caracteres
temp = temp.iloc[1:].reset_index(drop=True) #se establece la primera fila como título de las columnas
temp=temp[['Fecha','7. Te', '8. Te', '10. H', '11. R', '12. R', '1. Ve','2. Ve','3. Ve', '4. Di', '5. Di', '6. Di']]  #se ordena el df
columna=temp.columns.isin(['Fecha','10. H','7. Te','8. Te','1. Ve','2. Ve','3. Ve','4. Di', '5. Di', '6. Di', '11. R', '12. R'])
Index=np.where(columna==True)[0]  #se comprueba cuáles son las columnas con las que nos debemos de quedar
temp=temp.iloc[:,Index] 
FechaHora= pd.Series(temp.iloc[:,0]).str.split(pat=' ',expand=True)
AñoMesDia=pd.Series(FechaHora.iloc[:,0]).str.split(pat='/',expand=True)
HoraMin=pd.Series(FechaHora.iloc[:,1]).str.split(pat=':',expand=True) #se separa la fecha en el formato que nos interesa
HoraMin=HoraMin.iloc[:,:2]
temp=temp.drop(temp.columns[0],axis=1) #se elimina la col fecha
ClimaCiematS2=pd.concat([AñoMesDia,HoraMin,temp],axis=1) #se unen las distintas columnas
ClimaCiematS2.columns=['Dia','Mes','Año','Hora','Min','TextAvg','TextMax',
          'HextAvg','GhAvg','GhMax','VVextAvg','VVextMax','VVextSdev',
          'DVextAvg','DVextMax','DVextSde'] #se nombran las columnas
rutaf='D:\\Clima\\'+localizacion[0]+'\\MeteoGenica\\Excels_Diferentes_Datos'
os.chdir(rutaf)
ClimaCiematS2.to_excel('MadridyCiematS2_Min.xlsx', index=False, engine='openpyxl', na_rep='NaN')# se genera el excel
