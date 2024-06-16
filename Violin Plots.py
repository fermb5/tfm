# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:39:52 2024

@author: ferma
"""

import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
localizacion=['Madrid']
rutaEPW='D:\\Clima\\Madrid\\TMY'
os.chdir(rutaEPW)
filenameEPW='FicherosEPW.xlsx'
EPW=pd.read_excel(filenameEPW,sheet_name=1)

ruta='D:\\Clima\\'+localizacion[0]+'\\Horarios'
os.chdir(ruta)

filenameTHY=localizacion[0]+'yMet_2022_EOT_Hor.xlsx'
filenameTPY_585=localizacion[0]+'_prediccion_2050_Hor_585.xlsx'
filenameTPY_126=localizacion[0]+'_prediccion_2050_Hor_126.xlsx'
THY=pd.read_excel(filenameTHY)
TPY_585=pd.read_excel(filenameTPY_585)
TPY_126=pd.read_excel(filenameTPY_126)
ruta2='D:\\Clima\\'+localizacion[0]+'\\TMY'
os.chdir(ruta2)
filenameTMY=localizacion[0]+'_TMY_Hor.xlsx'
TMY=pd.read_excel(filenameTMY)
TextEPW=EPW['Tbs']
TextTMY=TMY['Text_prm']
TextTHY=THY['TextMastil_prm'].combine_first(THY['Text_prm_Meteo'])
TextTPY_585=TPY_585['Text_prm']
TextTPY_126=TPY_126['Text_prm']
HextEPW=EPW['HR']
HextTMY=TMY['Hext_prm']
THY['Hext_Mastil_prm']=THY['HextMastil_prm'].combine_first(THY['Hext_prm_Meteo'])
HextTHY=THY['Hext_Mastil_prm'][pd.notna(THY['Hext_Mastil_prm'])]
HextTPY_585=TPY_585['Hext_prm']
HextTPY_126=TPY_126['Hext_prm']
GhEPW=pd.Series(EPW['Ig'][EPW['Ig']!=0])
GhTMY=pd.Series(TMY['Gh_prm'][TMY['Gh_prm']!=0])
THY['Gh_prm']=THY['Gh_prm'].combine_first(THY['Gh_prm_Meteo'])
GhTHY=pd.Series(THY['Gh_prm'][THY['Gh_prm']!=0])
GhTPY_585=pd.Series(TPY_585['Gh prm'][TPY_585['Gh prm']!=0])
GhTPY_126=pd.Series(TPY_126['Gh prm'][TPY_126['Gh prm']!=0])

TextEPWVP=plt.violinplot(TextEPW,positions=[1],showmeans=True)
TextEPWBP=plt.boxplot(TextEPW,positions=[1],showfliers=False)
TextEPWVP['cmeans'].set_color('k')

TextTMYVP=plt.violinplot(TextTMY,positions=[2],showmeans=True)
TextTMYBP=plt.boxplot(TextTMY,positions=[2],showfliers=False)
TextTMYVP['cmeans'].set_color('k')

TextTHYVP=plt.violinplot(TextTHY,positions=[3],showmeans=True)
TextTHYBP=plt.boxplot(TextTHY,positions=[3])
TextTHYVP['cmeans'].set_color('k')

TextTPY_585VP=plt.violinplot(TextTPY_585,positions=[4],showmeans=True)
TextTPy_585BP=plt.boxplot(TextTPY_585,positions=[4])
TextTPY_585VP['cmeans'].set_color('k')

TextTPY_126VP=plt.violinplot(TextTPY_126,positions=[5],showmeans=True)
TextTPy_126BP=plt.boxplot(TextTPY_126,positions=[5])
TextTPY_126VP['cmeans'].set_color('k')

plt.xlim([0,5.5])
plt.legend([TextEPWVP['bodies'][0],TextTMYVP['bodies'][0],TextTHYVP['bodies'][0], TextTPY_585VP['bodies'][0],TextTPY_126VP['bodies'][0]], ['EPW','TMY','THY','TPY_585','TPY_126'], bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.title('Temperatura exterior (ºC)')
plt.show()

HextEPWVP=plt.violinplot(HextEPW,showmeans=True,positions=[1])
HextEPWBP=plt.boxplot(HextEPW,positions=[1])
HextEPWVP['cmeans'].set_color('k')

HextTMYVP=plt.violinplot(HextTMY,showmeans=True,positions=[2])
HextTMYBP=plt.boxplot(HextTMY,positions=[2])
HextTMYVP['cmeans'].set_color('k')

HextTHYVP=plt.violinplot(HextTHY,positions=[3],showmeans=True)
HextTHYBP=plt.boxplot(HextTHY,positions=[3])
HextTHYVP['cmeans'].set_color('k')

HextTPY_585VP=plt.violinplot(HextTPY_585,positions=[4],showmeans=True)
HextTPY_585BP=plt.boxplot(HextTPY_585,positions=[4])
HextTPY_585VP['cmeans'].set_color('k')

HextTPY_126VP=plt.violinplot(HextTPY_126,positions=[5],showmeans=True)
HextTPY_126BP=plt.boxplot(HextTPY_126,positions=[5])
HextTPY_126VP['cmeans'].set_color('k')

plt.xlim([0,5.5])
plt.legend([HextEPWVP['bodies'][0],HextTMYVP['bodies'][0],HextTHYVP['bodies'][0], HextTPY_585VP['bodies'][0], HextTPY_126VP['bodies'][0]],['EPW','TMY','THY','TPY_585','TPY_126'], bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.title('Humedad relativa (%)')
plt.show()

GhEPWVP=plt.violinplot(GhEPW,showmeans=True,positions=[1])
GhEPWVP['cmeans'].set_color('k')
GhEPWBP=plt.boxplot(GhEPW,positions=[1],showfliers=False,showcaps=False)

GhTMYVP=plt.violinplot(GhTMY,showmeans=True,positions=[2])
GhTMYVP['cmeans'].set_color('k')
GhTMYBP=plt.boxplot(GhTMY,positions=[2],showfliers=False,showcaps=False)

GhTHYVP=plt.violinplot(GhTHY,positions=[3],showmeans=True)
GhTHYBP=plt.boxplot(GhTHY,positions=[3],showfliers=False,showcaps=False)
GhTHYVP['cmeans'].set_color('k')

GhTPY_585VP=plt.violinplot(GhTPY_585,positions=[4],showmeans=True)
GhTPY_585BP=plt.boxplot(GhTPY_585,positions=[4],showfliers=False,showcaps=False)
GhTPY_585VP['cmeans'].set_color('k')

GhTPY_126VP=plt.violinplot(GhTPY_126,positions=[5],showmeans=True)
GhTPY_126BP=plt.boxplot(GhTPY_126,positions=[5],showfliers=False,showcaps=False)
GhTPY_126VP['cmeans'].set_color('k')

plt.xlim([0,5.5])
plt.legend([GhEPWVP['bodies'][0],GhTMYVP['bodies'][0],GhTHYVP['bodies'][0], GhTPY_585VP['bodies'][0], GhTPY_126VP['bodies'][0]], ['EPW','TMY','THY','TPY_585','TPY_126'], bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.title('Radiación solar global (W/$m^2$)')
plt.show()