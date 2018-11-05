#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 18:23:03 2018

@author: tof
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
mpl.rcParams['xtick.labelsize'] = 20 
mpl.rcParams['ytick.labelsize'] = 20
orden = [19, 7, 12, 5, 2, 1, 3, 4, 6, 9, 10, 13, 14, 17, 16, 11, 18, 20, 15, 8]
#orden = [2,1]
filename = "coordenadas_p4.txt"
datos = pd.read_csv(filename,header=None)
ciudades = datos.values
size_f = (20,10)
plt.figure(num=1,figsize=size_f)
plt.scatter(ciudades[:,0],ciudades[:,1],s=50)
for i, txt in enumerate(orden):
   plt.annotate(txt, (ciudades[txt-1][0], ciudades[txt-1][1]),size=30)

j = orden[0]
for i in orden:
    if i==j:
        continue
    plt.plot([ciudades[j-1][0],ciudades[i-1][0]],[ciudades[j-1][1],ciudades[i-1][1]],c='r')
    j = i

plt.savefig("ciudades.png")
plt.show()
