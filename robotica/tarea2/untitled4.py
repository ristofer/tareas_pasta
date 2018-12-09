#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
mpl.rcParams['xtick.labelsize'] = 18 
mpl.rcParams['ytick.labelsize'] = 18
Pmut=0.03 #probabilidad de mutacion
Pcros=0.9 #probabilidad de cruzamiento
Npop=[80,800,1600] #Numero de individuos por poblacion
files = []
for pop in Npop:
    filename = "fitp4-{}-{}-{}".format(Pmut,Pcros,pop)
    files.append(filename)

ldatos = []
for filename in files:
    datos = pd.read_csv(filename+".txt",header=None)
    fitness = datos.values[0,:]
    ldatos.append(fitness)

generaciones = [i for i in xrange(ldatos[0].size)]

size_f = (20,10)
plt.figure(num=1,figsize=size_f)
for i,fitness in enumerate(ldatos):
    plt.plot(generaciones,fitness,label=u"Número de individuos por población = {}".format(Npop[i]))

plt.legend()
plt.ylabel("Fitness",fontsize=21)
plt.xlabel(u"Generación",fontsize=21)
plt.savefig("poblas"+".png")

plt.show()
