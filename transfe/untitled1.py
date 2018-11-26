#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

class Simulacion(object):
    
    def __init__(self,x,y,q_0,t_ext,t_int,t_suelo,k,k_suelo,h_izq,h_der,espesor):
        self.x = x
        self.width = espesor
        self.y = y
        self.q_0 = q_0
        self.t_ext = t_ext
        self.t_int = t_int
        self.t_suelo = t_suelo
        self.k = k
        self.k_suelo = k_suelo
        self.h_int = h_izq 
        self.h_ext = h_der
        self.temp_nodos = []
        self.ecuaciones = []
        self.dy = 2.0/y
        self.dx = self.width/x
        self.t_inicial = 288
        self._crearMatriz()
        
        
    def _crearMatriz(self):
        self.temp_nodos = np.ones((self.y,self.x))*self.t_inicial
        #print(self.variables)
    
#    def _generarEcuaciones(self):
#        
#        for i in range(self.y):
#            self.ecuaciones.append(ecBorde(i,0))
#        for i in range(self.y):
#            self.ecuaciones.append(ecBorde(i,self.y-1))
#        for j in range(self.x):
#            self.ecuaciones.append(ecBorde(0,j))
#        for j in range(self.x):
#            self.ecuaciones.append(ecBorde(self.x-1,j))
#        
#        for i in range(1,x-1):
#            for j in range(1,y-1):
#                self.ecuaciones.append(ecInterior(i,j))
                
    def calcTempInterior(self,i,j):
        t1 = self.temp_nodos[i-1,j] 
        t2 = self.temp_nodos[i+1,j]
        t3 = self.temp_nodos[i,j-1] 
        t4 = self.temp_nodos[i,j+1]
        self.temp_nodos[i,j] = self.calcProm(t1,t2,t3,t4)
        
    def calcProm(self,t1,t2,t3,t4):
        suma = t1+t2+t3+t4
        return suma/4.0
        
    def calcTempEsquina(self,temp,t_p,t_s,t_conv,k,h,q_0,dp,ds,t_suelo=None):
        coef_ks_extra = 0
        coef_conv = h*(dp**2)*ds/2
        coef_kp = k*(dp**2)/2
        coef_ks = k*(ds**2)/2
        coef_k_suelo = self.k_suelo*(ds**2)/2
        coef_rad = (dp**2)*ds/2
        temp = t_conv*coef_conv + t_p*coef_kp + t_s*coef_ks + q_0*coef_rad
        if t_suelo is not None:
            temp = temp + t_suelo*coef_k_suelo
            coef_ks_extra = coef_k_suelo
        temp = temp/(coef_conv+coef_kp+coef_ks+coef_ks_extra)
        return temp
                
    def calcTempEsquinaIzqArr(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j+1]
        t_s = self.temp_nodos[i+1,j]
        t_conv = self.t_ext
        k = self.k
        h = self.h_ext
        q_0 = self.q_0
        dp = self.dy
        ds = self.dx
        self.temp_nodos[i,j] = self.calcTempEsquina(temp,t_p,t_s,t_conv,k,h,q_0,dp,ds)
        
    def calcTempEsquinaDerArr(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j-1]
        t_s = self.temp_nodos[i+1,j]
        t_conv = self.t_int
        k = self.k
        h = self.h_int
        q_0 = 0
        dp = self.dy
        ds = self.dx
        self.temp_nodos[i,j] = self.calcTempEsquina(temp,t_p,t_s,t_conv,k,h,q_0,dp,ds)

    def calcTempEsquinaDerAba(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j-1]
        t_s = self.temp_nodos[i-1,j]
        t_conv = self.t_int
        k = self.k
        h = self.h_int
        q_0 = 0
        dp = self.dy
        ds = self.dx
        #self.temp_nodos[i,j] = self.calcTempEsquina(temp,t_p,t_s,t_conv,k,h,q_0,dp,ds,t_suelo=self.t_suelo)
        self.temp_nodos[i,j] = self.t_suelo
        
    def calcTempEsquinaIzqAba(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j+1]
        t_s = self.temp_nodos[i-1,j]
        t_conv = self.t_ext
        k = self.k
        h = self.h_ext
        q_0 = self.q_0
        dp = self.dy
        ds = self.dx
        #self.temp_nodos[i,j] = self.calcTempEsquina(temp,t_p,t_s,t_conv,k,h,q_0,dp,ds,t_suelo=self.t_suelo)
        self.temp_nodos[i,j] = self.t_suelo
        
    def calcTempPared(self,temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds,t_suelo=0,k_suelo=None):
        coef_conv = h*(dp**2)*ds
        coef_kp = k*(dp**2)
        coef_ks = k*(ds**2)/2
        coef_rad = (dp**2)*ds
        coef_k_suelo = 0
        if t_suelo is not None and k_suelo is not None:
            coef_k_suelo = k_suelo*(dp**2)
        temp = t_conv*coef_conv + t_p*coef_kp + (t_s1+t_s2)*coef_ks + q_0*coef_rad + t_suelo*coef_k_suelo
        temp = temp/(coef_conv+coef_kp+2*coef_ks+coef_k_suelo)
        return temp

    def calcTempIzq(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j+1]
        t_s1 = self.temp_nodos[i-1,j]
        t_s2 = self.temp_nodos[i+1,j]
        t_conv = self.t_ext
        k = self.k
        h = self.h_ext
        q_0 = self.q_0
        dp = self.dy
        ds = self.dx
        self.temp_nodos[i,j] = self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds)
    
    def calcTempDer(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i,j-1]
        t_s1 = self.temp_nodos[i-1,j]
        t_s2 = self.temp_nodos[i+1,j]
        t_conv = self.t_int
        k = self.k
        h = self.h_int
        q_0 = 0
        dp = self.dy
        ds = self.dx
        self.temp_nodos[i,j] = self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds)

    def calcTempArr(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i+1,j]
        t_s1 = self.temp_nodos[i,j-1]
        t_s2 = self.temp_nodos[i,j+1]
        t_conv = self.t_int
        k = self.k
        h = 0
        q_0 = 0
        dp = self.dx
        ds = self.dy
        #print(self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds)-self.calcProm(t_p,t_s1,t_s2,t_p))
        assert abs(self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds)-self.calcProm(t_p,t_s1,t_s2,t_p))<10
        self.temp_nodos[i,j] = self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds)
        
    def calcTempAba(self,i,j):
        temp = self.temp_nodos[i,j]
        t_p = self.temp_nodos[i-1,j]
        t_s1 = self.temp_nodos[i,j-1]
        t_s2 = self.temp_nodos[i,j+1]
        t_conv = self.t_int
        k = self.k
        h = 0
        q_0 = 0
        dp = self.dx
        ds = self.dy
        #self.temp_nodos[i,j] = self.calcTempPared(temp,t_p,t_s1,t_s2,t_conv,k,h,q_0,dp,ds,k_suelo=self.k_suelo,t_suelo=self.t_suelo)
        #self.temp_nodos[i,j] = self.calcProm(t_p,t_s1,t_s2,self.t_suelo)
        self.temp_nodos[i,j] = self.t_suelo
        
    def calcTeorico(self):
        pterm = self.t_int - self.t_ext - self.q_0/self.h_ext
        sterm = ((self.k + self.h_ext*self.width)/self.h_int) + self.k/self.h_ext
        c1 = pterm/sterm
        c2 = self.t_ext + (self.k*c1+self.q_0)/self.h_ext
        posiciones = np.linspace(0,self.width,num=self.x)
        grilla,_ = np.meshgrid(posiciones,posiciones)
        temp_teoricas = c1*grilla + c2
        sns.heatmap(temp_teoricas)
        
    def calcTeorico2(self):
        pterm1 = self.q_0 + self.h_ext*self.t_ext
        pterm2 = self.k*(pterm1 + self.h_int*self.t_int)/(self.h_int*self.width)
        pterm = pterm1 + pterm2
        sterm = self.k*(self.h_ext+self.h_int)/(self.h_int*self.width) + self.h_ext
        c2 = pterm/sterm
        c1 = (pterm1 + self.h_int*self.t_int - c2*(self.h_ext+self.h_int))/(self.h_int*self.width)
        posiciones = np.linspace(0,self.width,num=self.x)
        grilla,_ = np.meshgrid(posiciones,posiciones)
        temp_teoricas = c1*grilla + c2
        sns.heatmap(temp_teoricas)
        
   
    def test(self):
        y = self.y
        x = self.x
        for i in range(self.y):
            for j in range(self.x):
                if i==0 and j==0:
                    self.calcTempEsquinaIzqArr(i,j)
                    continue
                if i==y-1 and j==0:
                    self.calcTempEsquinaIzqAba(i,j)
                    continue
                if i==0 and j==x-1:
                    self.calcTempEsquinaDerArr(i,j)
                    continue
                if i==y-1 and j==x-1:
                    self.calcTempEsquinaDerAba(i,j)
                    continue
                if i==0 and j!=0 and j!=x-1:
                    self.calcTempArr(i,j)
                    continue
                if i==y-1 and j!=0 and j!=x-1:
                    self.calcTempAba(i,j)
                    continue
                if j==0 and i!=0 and i!=y-1:
                    self.calcTempIzq(i,j)
                    continue
                if j==x-1 and i!=0 and i!=y-1:
                    self.calcTempDer(i,j)
                    continue
                self.calcTempInterior(i,j)
    
    def plotito(self):
        sns.heatmap(self.temp_nodos)
                    
#    def main(self):
#        self._crearMatriz()
#        self._generarEcuaciones()
#        #print(self.variables)
#        self.valores_iniciales = [200]*self.x*self.y
#        self.valores_n = sym.nsolve(self.ecuaciones,self.variables,self.valores_iniciales)
#        #self.valores = sym.solve(self.ecuaciones)
#        print(self.valores_n)
#        print(type(self.valores_n))
#        self.temperaturas()
#        test = np.array(self.mat_num)
#        print(type(test[0,0]))
#        sns.heatmap(test)
        
    def temperaturas(self):
        self.mat_num = []
        for i,arr in enumerate(self.temp_nodos):
            aux = []
            for j,temp in enumerate(arr):
                aux.append(float(self.valores.get(self.temp_nodos[i][j]).evalf()))
            self.mat_num.append(aux)

radiaciones = [0,99,911,700] #w/m2
temperaturas = [15,11,22,24] #grados celcius
viento = np.array([2,2,3,3]) #m/s
temperaturas_casa = [10,7,17,19]
temperaturas = [n+273.15 for n in temperaturas]
temperaturas_casa = [n+273.15 for n in temperaturas_casa]
espesores = [0.08,0.12,0.30,0.60]
xs = [int(n/0.001) for n in espesores]

densidades = [1.225,1.246,1.204,1.184]
visco_cine = [1.470,1.426,1.516,1.562]
visco_cine = np.array([n*(10**-5) for n in visco_cine])
reynolds = viento*2.0/visco_cine
prandt = np.array([0.7323,0.7336,0.7309,0.7296])
k_aire = np.array([0.02476,0.02439,0.02514,0.02551])
nusselt = 0.664 * reynolds**(1/2) * prandt**(1/3)
hs = nusselt*k_aire/2.0
mallasx = [20,200,600,1000]
mallasy = [40,400,600,1400]
count = 1
for j,s in enumerate(mallasx):
    for i,r in enumerate(radiaciones):
        for n,l in enumerate(espesores):
            sim = Simulacion(x=mallasx[j],y=mallasy[j],q_0=radiaciones[i],t_ext=temperaturas[i],t_int=temperaturas_casa[i],t_suelo=273.15+15,k=0.46,k_suelo=0.46,h_izq=hs[i],h_der=3,espesor=espesores[n])
            for c in range(2000):
                sim.test()
                print(c)
            count += 1
            plt.figure(count)
            count += 1
            sim.plotito()
            plt.title("Temperatura en pared de espesor {}".format(espesores[n]))
            plt.savefig("simulado-{}-{}-{}.png".format(i,j,n))
            plt.figure(count)



        