#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 17:29:20 2018

@author: tof
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
ngen = 30
#mi = 1.85728250244
mi = 0
def linear_transform(number,imin,imax,omin,omax):
    result = (omax/imax)*(number-imin) + omin
    return result 

def eval_func(valor): #recibe un cromosoma, en este caso una lista de 1s y 0s
   valor_escalado = linear_transform(valor,0,2**ngen-1,0,50.0)
   print valor_escalado
   score = funcion_buscada(valor_escalado)
   return score

def funcion_buscada(tiempo):
    ptermino = 346*np.exp(-0.0628*tiempo)
    stermino = np.sin(1.2544*tiempo+2.35)
    return ptermino*stermino

pg = linear_transform(np.arange(0,2**ngen,1.0),0,2**ngen-1,0,50.0)
ps = funcion_buscada(pg)

t = np.arange(0.0, 50.0, 0.01)
s = funcion_buscada(t)
fig, ax = plt.subplots()
ax.plot(t, s)
ax.scatter(mi,funcion_buscada(mi),c='k',s=200,label='Mejor individuo')
ax.scatter(pg,ps,c='g',label='Posibles individuos')

ax.set(xlabel=u'Tiempo [s]', ylabel=u'Posición [cm]',
       title=u'Gráfico de oscilación, cantidad de genes = %s'%ngen)
ax.grid()
ax.legend()

fig.savefig("test.png")
plt.show()