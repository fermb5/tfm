# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:28:22 2024

@author: ferma
"""
import os
import pandas as pd
import numpy as np
localizacion=['PSA']
Anio=['2021','2022','2023']
#Define una función para filtrar outliers
def filtrar_outliers(series):
    if series.notna().any():
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        series[(series < (q25 - 1.5 * iqr)) | (series > (q75 + 1.5 * iqr))] = np.nan
        return series
    else:
        return pd.Series([np.nan] * len(series), index=series.index)
#se definen una serie de funciones para eliminar los valores repetidos, con condiciones de ciertos números que si se pueden repetir
# como por ej el 0 para el caso de la radiación o el 100 para la humedad
def eliminar_valores_repetidos_G(series):
    prim_repeticiones=series[series.ne(0)].duplicated(keep='first') #matriz de booleanos que indica como false aquellos valores que salen por primera vez
    repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0] #matriz que indica los índices de aquellos valores que ya han salido
    tempin=np.empty(shape=2)
    indices_cambio = series.index[series.diff().ne(0)] #matriz que indica los índices donde se cambia  de número
    if len(repeticiiones>=5): #debe de haber mínimo cinco repeticiones
        for i in range(4,len(repeticiiones)):
            if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
                repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]: #se cumpla que las repeticiones sean seguidas
                    tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
                    tempin=np.vstack((tempin,tempint))
        tempin=np.delete(tempin,0,axis=0) #se seleccionan diferencias de índices salvo la primera fila (está vacía)
    for i in range(len(indices_cambio)-1): #se deben de respetar aquellos valores que han salido previamente, pero son un cambio de número. Ej: 1,2,2,2,2,¡1! no es un núm repetido
        diferencia=indices_cambio[i+1]-indices_cambio[i]
        if diferencia>5:
            series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
    return series
#mismo criterio que la función anterior
def eliminar_valores_repetidos_T(series):
    prim_repeticiones=series.duplicated(keep='first')
    repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0]
    tempin=np.empty(shape=2)
    indices_cambio = series.index[series.diff().ne(0)]
    if len(repeticiiones>=10):
        for i in range(4,len(repeticiiones)):
            if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
                repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]:
                    tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
                    tempin=np.vstack((tempin,tempint))
        tempin=np.delete(tempin,0,axis=0)
    for i in range(len(indices_cambio)-1):
        diferencia=indices_cambio[i+1]-indices_cambio[i]
        if diferencia>5:
            series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
    return series
def eliminar_valores_repetidos_H(series):
    prim_repeticiones=series[series.ne(100)].duplicated(keep='first')
    repeticiiones=np.where(prim_repeticiones.to_numpy()==True)[0]
    tempin=np.empty(shape=2)
    indices_cambio = series.index[series.diff().ne(0)]
    if len(repeticiiones>=10):
        for i in range(4,len(repeticiiones)):
            if repeticiiones[i]-1==repeticiiones[i-1] and repeticiiones[i]-2==repeticiiones[i-2] and \
                repeticiiones[i]-3==repeticiiones[i-3] and repeticiiones[i]-4==repeticiiones[i-4]:
                    tempint=np.array([repeticiiones[i-4],repeticiiones[i]])
                    tempin=np.vstack((tempin,tempint))
        tempin=np.delete(tempin,0,axis=0)
    for i in range(len(indices_cambio)-1):
        diferencia=indices_cambio[i+1]-indices_cambio[i]
        if diferencia>5:
            series.iloc[indices_cambio[i]+1:indices_cambio[i]+diferencia]=np.nan
    return series



#Hace un bucle para cada año
for i in range(len(Anio)):
    ruta='D:\\Clima\\'+localizacion[0]+'\\Minutales'
    os.chdir(ruta)
    filename=localizacion[0]+'_'+Anio[i]+'_Min.xlsx'
    filenameEOT=localizacion[0]+'_EOT_Min.xlsx'
    ClimaAnualEOT=pd.read_excel(filenameEOT) #genera el dataframe a partir del excel minutal
    ClimaAnual=pd.read_excel(filename) #genera el dataframe a partir del excel minutal
    ClimaAnual['Gh'] = np.where(pd.isna(ClimaAnualEOT['Gh_0']), ClimaAnual['Gh'], ClimaAnualEOT['Gh_0'])
    ClimaAnual['AñoMesDiaHora']=ClimaAnual.apply(lambda row: f"{row['Año']}-{row['Mes']}-{row['Dia']}-{row['Hora']}", axis=1) #agrupa las columnas nombradas con el formato correspondiente
    ClimaAnual.drop(['Año','Mes','Dia','Hora','Min'],axis=1,inplace=True) #elimina las columnas ya agrupadas y la minutal
    ClimaAnual['AñoMesDiaHora']=pd.to_datetime(ClimaAnual['AñoMesDiaHora'], format='%Y.0-%m.0-%d.0-%H.0') # ordena las columnas en formato horario
    #se aplican los diferentes filtrados
    ClimaAnual = ClimaAnual.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_G(col) if col.name == 'Gh' or col.name == 'Gv' else col))
    ClimaAnual = ClimaAnual.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_H(col) if col.name == 'Hext' else col))
    ClimaAnual = ClimaAnual.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: eliminar_valores_repetidos_T(col) if col.name == 'Text'  else col))      
    ClimaAnual_filtrado_outliers = ClimaAnual.groupby('AñoMesDiaHora').apply(lambda group: group.apply(lambda col: filtrar_outliers(col) if col.name != 'AñoMesDiaHora' or 'R' else col))
    
    #se realizan las operaciones pertinentes agrupando por cada hora
    ClimaAnualHorario = ClimaAnual_filtrado_outliers.groupby('AñoMesDiaHora').agg({
        'Text': ['mean', 'max', 'min', 'count'],
        'Hext': ['mean', 'max', 'min', 'count'],
        'Gh': ['mean', 'max', 'min',  'count'],
        'VVext': ['mean', 'max', 'min', 'count'],
        # 'DVext': ['mean', 'max', 'min',  'count'],
        'Gv': ['mean', 'max', 'min', 'count'],
    })
    ClimaAnualHorario.reset_index(inplace=True) #reestablece los índices
    Fecha = pd.Series(ClimaAnualHorario.iloc[:,0]).astype(str).str.split('-', expand=True)
    DiaHoraMinSeg=pd.Series(Fecha.iloc[:,2]).str.split(expand=True)
    HoraMinSeg=pd.Series(DiaHoraMinSeg.iloc[:,1]).str.split(':', expand=True)
    #se separan año, mes, día y hor
    ClimaAnualHorario = ClimaAnualHorario.drop(ClimaAnualHorario.columns[0], axis=1) #se elimina la columna previamente creada AñoMesDiaMin
    ClimaAnualHorario.columns=['TextMastil_prm','TextMastil_max','TextMastil_min','TextMastil_num',
                                'HextMastil_prm','HextMastil_max','HextMastil_min','HextMastil_num',
                'Gh_prm','Gh_max','Gh_min','Gh_num',
                'VVext_prm','VVext_max','VVext_min','VVext_num',
                'Gv_prm','Gv_max','Gv_min','Gv_num']
    #se nombran las columnas correctamente con los datos tratados
    ClimaAnualHorario=pd.concat([Fecha.iloc[:,0:2],DiaHoraMinSeg.iloc[:,0],HoraMinSeg.iloc[:,0],ClimaAnualHorario],axis=1)
    #se unen a su formato de año, mes, día y hor
    
    
    
    ClimaAnualHorario.columns=['Año', 'Mes', 'Dia', 'Hora','TextMastil_prm','TextMastil_max','TextMastil_min','TextMastil_num',
                                'HextMastil_prm','HextMastil_max','HextMastil_min','HextMastil_num',
                                'Gh_prm','Gh_max','Gh_min','Gh_num',
                                'VVext_prm','VVext_max','VVext_min','VVext_num',
                                'Gv_prm','Gv_max','Gv_min','Gv_num']
    #se nombran de nuevo una vez están todas las columnas del df(dataframe) final
    ruta2=ruta='D:\\Clima\\'+localizacion[0]+'\\Horarios'
    os.chdir(ruta2)
    #se genera el excel
    ClimaAnualHorario.to_excel(localizacion[0]+'_'+Anio[i]+'_Hor_EOT.xlsx',index=False, engine='openpyxl', na_rep='NaN')

    
        