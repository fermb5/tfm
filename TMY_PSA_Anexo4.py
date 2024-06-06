# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 18:38:38 2024

@author: ferma
"""
import os
import pandas as pd
import numpy as np
import calendar
#Se elige la localización y los años empleados para la elaboración del TMY
localizacion=['PSA']
rutaAnexo2='D:\\Clima\\'+localizacion[0]+'\\TMY\\TablaAnexo2'
os.chdir(rutaAnexo2)
listaAnexo2=pd.DataFrame(os.listdir(rutaAnexo2))
Sumatorio_T_final=pd.DataFrame()
Sumatorio_H_final=pd.DataFrame()
Sumatorio_G_final=pd.DataFrame()
FS_final=pd.DataFrame()
for h in range(len(listaAnexo2)):
    Anexo2 = pd.read_excel(listaAnexo2.iloc[h,0], sheet_name=None)
    
    # Lee cada hoja del archivo Excel y crea un DataFrame para cada una
    dfT = Anexo2['HojaT']
    dfH = Anexo2['HojaH']
    dfG = Anexo2['HojaG']
    dfT_final=pd.DataFrame()
    dfH_final=pd.DataFrame()
    dfG_final=pd.DataFrame()
    
    Anio=listaAnexo2.iloc[h,0].split('.')
    Anio=Anio[0].split('_')[2]
    
    Sumatorio_T=[]
    Sumatorio_H=[]
    Sumatorio_G=[]
    
    gruposdfT_por_mes = dfT.groupby('Mes')
    gruposdfH_por_mes = dfH.groupby('Mes')
    gruposdfG_por_mes = dfG.groupby('Mes')
    dfT_por_mes={mes: gruposdfT_por_mes.get_group(mes) for mes in gruposdfT_por_mes.groups}
    dfH_por_mes={mes: gruposdfH_por_mes.get_group(mes) for mes in gruposdfH_por_mes.groups}
    dfG_por_mes={mes: gruposdfG_por_mes.get_group(mes) for mes in gruposdfG_por_mes.groups}
    
    for i in range (1,13):
        #definición de variables a rellenar
        CDF_S_T=[]
        CDF_S_H=[]
        CDF_S_G=[]
        #procedimiento para la temperatura
        indice_inicial=dfT_por_mes[i].index[0]
        indice_final=dfT_por_mes[i].index[-1]
        dfT=dfT_por_mes[i][['K_LT_Text','CDF_LT_Text','J_ST_Text','CDF_ST_Text']]
        dfT=dfT.dropna()
        dfT_reset=dfT.reset_index()
        if not dfT.empty:   
            dfT_CDF_LT_T=dfT.sort_values(by='CDF_LT_Text', ignore_index=True)
            dfT_CDF_LT_T['Index']=dfT_reset['index']
            dfT_CDF_LT_T= dfT_CDF_LT_T.set_index('Index')
            dfT_CDF_ST_T=dfT.sort_values(by='CDF_ST_Text', ignore_index=True)
            dfT_CDF_ST_T['Index']=dfT_reset['index']
            dfT_CDF_ST_T= dfT_CDF_ST_T.set_index('Index')
            dfT=pd.concat([dfT['K_LT_Text'],dfT_CDF_LT_T['CDF_LT_Text'],dfT['J_ST_Text'],dfT_CDF_ST_T['CDF_ST_Text']],axis=1)
            for j in range(dfT.shape[0]):
                if dfT.iloc[j,2]<min(dfT['K_LT_Text']):
                    CDF_S_T.append(0)
                elif dfT.iloc[j,2]<dfT.iloc[j,0]:
                    valor_inferior=dfT.iloc[:, 1][dfT.iloc[:, 0]<dfT.iloc[j,2]].max()
                    CDF_S_T.append(valor_inferior)
                elif dfT.iloc[j,2]==dfT.iloc[j,0]:
                    valor_igual=dfT.iloc[j,1]
                    CDF_S_T.append(valor_igual)        
                elif dfT.iloc[j,2]>max(dfT['K_LT_Text']):
                    CDF_S_T.append(1)
                elif dfT.iloc[j,2]>dfT.iloc[j,0]:
                    valor_superior=dfT.iloc[:, 1][dfT.iloc[:, 0]>dfT.iloc[j,2]].min()
                    CDF_S_T.append(valor_superior)
            CDF_S_T=pd.DataFrame(CDF_S_T)
            CDF_S_T.columns=['CDF_S_Text']
            CDF_S_T['Index']=dfT_reset['index']
            CDF_S_T= CDF_S_T.set_index('Index')
            dfT=pd.concat([dfT,CDF_S_T],axis=1)
            dfT['CDF_ST_S-1_Text']=dfT['CDF_ST_Text'].shift(periods=1)
            dfT.at[dfT.index[0],'CDF_ST_S-1_Text']=0
            dfT['DIF_ABS_SUP_Text']=abs(dfT['CDF_S_Text']-dfT['CDF_ST_Text'])
            dfT['DIF_ABS_INF_Text']=abs(dfT['CDF_S_Text']-dfT['CDF_ST_S-1_Text'])
            dfT['DIF_MAX_ABS'] = dfT[['DIF_ABS_SUP_Text', 'DIF_ABS_INF_Text']].max(axis=1)
            dfT_final=pd.concat([dfT_final,dfT],axis=0)
            Sumatorio_T.append(dfT['DIF_MAX_ABS'].mean())
        else:
            Sumatorio_T.append(np.nan)
            #procedimiento para la humedad
        dfH=dfH_por_mes[i][['K_LT_Hext','CDF_LT_Hext','J_ST_Hext','CDF_ST_Hext']]
        dfH=dfH.dropna()
        dfH_reset=dfH.reset_index()
        if not dfH.empty: 
            dfH_CDF_LT_H=dfH.sort_values(by='CDF_LT_Hext', ignore_index=True)
            dfH_CDF_LT_H['Index']=dfH_reset['index']
            dfH_CDF_LT_H= dfH_CDF_LT_H.set_index('Index')
            dfH_CDF_ST_H=dfH.sort_values(by='CDF_ST_Hext', ignore_index=True)
            dfH_CDF_ST_H['Index']=dfH_reset['index']
            dfH_CDF_ST_H= dfH_CDF_ST_H.set_index('Index')
            dfH=pd.concat([dfH['K_LT_Hext'],dfH_CDF_LT_H['CDF_LT_Hext'],dfH['J_ST_Hext'],dfH_CDF_ST_H['CDF_ST_Hext']],axis=1)
            for j in range(dfH.shape[0]):
                if dfH.iloc[j,2]<min(dfH['K_LT_Hext']):
                    CDF_S_H.append(0)
                elif dfH.iloc[j,2]<dfH.iloc[j,0]:
                    valor_inferior=dfH.iloc[:, 1][dfH.iloc[:, 0]<dfH.iloc[j,2]].max()
                    CDF_S_H.append(valor_inferior)
                elif dfH.iloc[j,2]==dfH.iloc[j,0]:
                    valor_igual=dfH.iloc[j,1]
                    CDF_S_H.append(valor_igual)        
                elif dfH.iloc[j,2]>max(dfH['K_LT_Hext']):
                    CDF_S_H.append(1)
                elif dfH.iloc[j,2]>dfH.iloc[j,0]:
                    valor_superior=dfH.iloc[:, 1][dfH.iloc[:, 0]>dfH.iloc[j,2]].min()
                    CDF_S_H.append(valor_superior)
            CDF_S_H=pd.DataFrame(CDF_S_H)
            CDF_S_H.columns=['CDF_S_Hext']
            CDF_S_H['Index']=dfH_reset['index']
            CDF_S_H= CDF_S_H.set_index('Index')
            dfH=pd.concat([dfH,CDF_S_H],axis=1)
            dfH['CDF_ST_S-1_Hext']=dfH['CDF_ST_Hext'].shift(periods=1)
            dfH.at[dfH.index[0],'CDF_ST_S-1_Hext']=0
            dfH['DIF_ABS_SUP_Hext']=abs(dfH['CDF_S_Hext']-dfH['CDF_ST_Hext'])
            dfH['DIF_ABS_INF_Hext']=abs(dfH['CDF_S_Hext']-dfH['CDF_ST_S-1_Hext'])
            dfH['DIF_MAX_ABS'] = dfH[['DIF_ABS_SUP_Hext', 'DIF_ABS_INF_Hext']].max(axis=1)
            dfH_final=pd.concat([dfH_final,dfH],axis=0)
            Sumatorio_H.append(dfH['DIF_MAX_ABS'].mean())
        else:
            Sumatorio_H.append(np.nan)
        #procedimiento radiación
        dfG=dfG_por_mes[i][['K_LT_Gh','CDF_LT_Gh','J_ST_Gh','CDF_ST_Gh']]
        dfG=dfG.dropna()
        dfG_reset=dfG.reset_index()
        if not dfG.empty: 
            dfG_CDF_LT_T=dfG.sort_values(by='CDF_LT_Gh', ignore_index=True)
            dfG_CDF_LT_T['Index']=dfG_reset['index']
            dfG_CDF_LT_T= dfG_CDF_LT_T.set_index('Index')
            dfG_CDF_ST_T=dfG.sort_values(by='CDF_ST_Gh', ignore_index=True)
            dfG_CDF_ST_T['Index']=dfG_reset['index']
            dfG_CDF_ST_T= dfG_CDF_ST_T.set_index('Index')
            dfG=pd.concat([dfG['K_LT_Gh'],dfG_CDF_LT_T['CDF_LT_Gh'],dfG['J_ST_Gh'],dfG_CDF_ST_T['CDF_ST_Gh']],axis=1)
            for j in range(dfG.shape[0]):
                if dfG.iloc[j,2]<min(dfG['K_LT_Gh']):
                    CDF_S_G.append(0)
                elif dfG.iloc[j,2]<dfG.iloc[j,0]:
                    valor_inferior=dfG.iloc[:, 1][dfG.iloc[:, 0]<dfG.iloc[j,2]].max()
                    CDF_S_G.append(valor_inferior)
                elif dfG.iloc[j,2]==dfG.iloc[j,0]:
                    valor_igual=dfG.iloc[j,1]
                    CDF_S_G.append(valor_igual)        
                elif dfG.iloc[j,2]>max(dfG['K_LT_Gh']):
                    CDF_S_G.append(1)
                elif dfG.iloc[j,2]>dfG.iloc[j,0]:
                    valor_superior=dfG.iloc[:, 1][dfG.iloc[:, 0]>dfG.iloc[j,2]].min()
                    CDF_S_G.append(valor_superior)
            CDF_S_G=pd.DataFrame(CDF_S_G)
            CDF_S_G.columns=['CDF_S_Gh']
            CDF_S_G['Index']=dfG_reset['index']
            CDF_S_G= CDF_S_G.set_index('Index')
            dfG=pd.concat([dfG,CDF_S_G],axis=1)
            dfG['CDF_ST_S-1_Gh']=dfG['CDF_ST_Gh'].shift(periods=1)
            dfG.at[dfG.index[0],'CDF_ST_S-1_Gh']=0
            dfG['DIF_ABS_SUP_Gh']=abs(dfG['CDF_S_Gh']-dfG['CDF_ST_Gh'])
            dfG['DIF_ABS_INF_Gh']=abs(dfG['CDF_S_Gh']-dfG['CDF_ST_S-1_Gh'])
            dfG['DIF_MAX_ABS'] = dfG[['DIF_ABS_SUP_Gh', 'DIF_ABS_INF_Gh']].max(axis=1)
            dfG_final=pd.concat([dfG_final,dfG],axis=0)
            Sumatorio_G.append(dfT['DIF_MAX_ABS'].mean())
        else:    
            Sumatorio_G.append(np.nan)
    #determinación de FS_sum
    FS_sum=[]
    w1=1/3
    w2=1/3
    w3=1/3
    for k in range(len(Sumatorio_G)):
        FS_sum.append(Sumatorio_T[k]*w1+Sumatorio_H[k]*w2+Sumatorio_G[k]*w3)
    FS_sum=pd.DataFrame(FS_sum)
    Sumatorio_T=pd.DataFrame(Sumatorio_T)
    Sumatorio_H=pd.DataFrame(Sumatorio_H)
    Sumatorio_G=pd.DataFrame(Sumatorio_G)
    Sumatorio_T_final=pd.concat([Sumatorio_T_final,Sumatorio_T],axis=1)
    Sumatorio_H_final=pd.concat([Sumatorio_H_final,Sumatorio_H],axis=1)
    Sumatorio_G_final=pd.concat([Sumatorio_G_final,Sumatorio_G],axis=1)
    FS_sum.columns=[Anio]
    FS_final=pd.concat([FS_final,FS_sum],axis=1)
Anexo3 = FS_final.apply(lambda fila: fila.nsmallest(listaAnexo2.shape[0]).index.tolist(), axis=1)
Anexo3 = pd.DataFrame(Anexo3.tolist(), index=FS_final.index)
Anexo3.index=[['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']]
rutaAnexo3='D:\\Clima\\'+localizacion[0]+'\\TMY\\TablaAnexo4'
os.chdir(rutaAnexo3)
filename='Tabla_Anexo4.xlsx'
Anexo3.to_excel(filename,header=False,index=True)

    

         