# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:52:26 2024

@author: ferma
"""
import os
import pandas as pd
import numpy as np
import calendar
from datetime import datetime, timedelta
localizacion=['Madrid']
ruta='D:\\Clima\\'+localizacion[0]+'\\Minutales'
os.chdir(ruta)
Le=-(3+43/60+48/3600)*np.pi/180
phi=(40+27/60)*np.pi/180
# Número de minutos en un día y en un año
minutos_dia = 24 * 60
dias_año = 365
minutos_año = dias_año * minutos_dia

# Crear un DataFrame con un rango de minutos del año
EOT = pd.DataFrame({'Min': range(minutos_año)})

# Calcular el día del año y la hora decimal para cada minuto
EOT['Dia'] = EOT['Min'] // minutos_dia + 1  # Día del año (1 a 365)
EOT['Hora_decimal'] = (EOT['Min'] % minutos_dia) / 60  # Hora decimal (0.0 a 23.9833...)

# Eliminar la columna de 'Minuto_del_ano' si no es necesaria
EOT.drop(columns=['Min'], inplace=True)
EOT['Gamma']=(2*np.pi/365) * (EOT['Dia']-1)
EOT['Et']=229.18*(0.000075+np.cos(EOT['Gamma'])*0.001868+np.sin(EOT['Gamma'])*0.032077
                  -np.cos(2*EOT['Gamma'])*0.014615-np.sin(2*EOT['Gamma'])*0.04089)
EOT['LST']=EOT['Hora_decimal']-Le/15+EOT['Et']/60
EOT['W']=15*(EOT['LST']-12)*np.pi/180
EOT['Delta']=(0.006918-0.399912*np.cos(EOT['Gamma'])+0.070257*np.sin(EOT['Gamma'])-
              0.006758*np.cos(EOT['Gamma']*2)+0.000907*np.sin(EOT['Gamma']*2)-
              0.002697*np.cos(EOT['Gamma']*3)+0.00148*np.sin(EOT['Gamma']*3))
EOT['Alfa']=np.arcsin(np.sin(EOT['Delta'])*np.sin(phi)+np.cos(EOT['Delta'])*
                      np.cos(phi)*np.cos(EOT['W']))*180/np.pi
EOT['Gh_0'] = EOT['Alfa'].apply(lambda x: 0 if x < 7 else np.nan)
filenameEOT=localizacion[0]+'_EOT_Min.xlsx'
EOT.to_excel(filenameEOT,index=False, engine='openpyxl', na_rep='NaN')