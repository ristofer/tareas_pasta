#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
mpl.rcParams['xtick.labelsize'] = 20 
mpl.rcParams['ytick.labelsize'] = 20
filename = "fitp4-0.03-0.6-80"
datos = pd.read_csv(filename+".txt",header=None)
fitness = datos.values[0,:]
generaciones = [i for i in xrange(fitness.size)]

#size_f = (20,10)
#plt.figure(num=1,figsize=size_f)
plt.plot(generaciones,fitness)


plt.savefig(filename+".png")
plt.show()
