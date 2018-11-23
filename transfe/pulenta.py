#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sympy as sym
import copy
import seaborn as sns
sns.set()

class Simulacion(object):
    
    def __init__(self,x,y,q_0,t_ext,t_int,t_suelo,k,k_suelo,h_izq,h_der):
        self.x = x
        self.y = y
        self.q_0 = q_0
        self.t_ext = t_ext
        self.t_int = t_int
        self.t_suelo = t_suelo
        self.k = k
        self.k_suelo = k_suelo
        self.h_izq = h_izq 
        self.h_der = h_der
        self.temp_nodos = []
        self.ecuaciones = []
        self.dy = 0.5
        self.dx = 0.5
        
    def _crearMatriz(self):
        self.variables = []
        for j in range(1,self.x+1):
            aux = [sym.Symbol('T_{{{},{}}}'.format(i,j)) for i in range(1,self.y+1)]
            self.temp_nodos.append(copy.copy(aux))
            self.variables = self.variables + copy.copy(aux)
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

    def _generarEcuaciones(self):
        for i in range(self.y):
            for j in range(self.x):
                self.ecuaciones.append(self.ecBorde(i,j))
                
    def ecBorde(self,i,j):
        q_1 = self.calorIzq(i,j)
        q_2 = self.calorDer(i,j)
        q_3 = self.calorArr(i,j)
        q_4 = self.calorAba(i,j)
        return q_1 + q_2 + q_3 + q_4
    
    def calorIzqBorde(self,i,j):
        resistencia = 2*1/(self.dy*self.h_izq)
        diff = self.t_ext-self.temp_nodos[i][j]
        calor = diff/resistencia
        return calor + self.q_0*self.dy/2
    
    def calorDerBorde(self,i,j):
        resistencia = 2*1/(self.dy*self.h_der)
        diff = self.temp_nodos[i][j] - self.t_int
        calor = diff/resistencia
        return calor
    
    def calorArrBorde(self,i,j):
        return 0
    
    def calorAbaBorde(self,i,j):
        resistencia = 2*self.dy/(self.dx*self.k_suelo)
        diff = self.t_suelo - self.temp_nodos[i][j]
        calor = diff/resistencia
        return calor
        
    def calorIzq(self,i,j):
        if j==0:
            return self.calorIzqBorde(i,j)
        else:
            resistencia = 2*self.dx/(self.dy*self.k)
            diff = self.temp_nodos[i][j-1]-self.temp_nodos[i][j]
            calor = diff/resistencia
            return calor
    
    def calorDer(self,i,j):
        if j==self.x-1:
            return self.calorDerBorde(i,j)
        else:
            resistencia = 2*self.dx/(self.dy*self.k)
            diff = self.temp_nodos[i][j+1]-self.temp_nodos[i][j]
            calor = diff/resistencia
            return calor
        
    def calorArr(self,i,j):
        if i==0:
            return self.calorArrBorde(i,j)
        else:
            resistencia = 2*self.dy/(self.dx*self.k)
            diff = self.temp_nodos[i-1][j]-self.temp_nodos[i][j]
            calor = diff/resistencia
            return calor
        
    def calorAba(self,i,j):
        if i==self.y-1:
            return self.calorAbaBorde(i,j)
        else:
            resistencia = 2*self.dy/(self.dx*self.k)
            diff = self.temp_nodos[i+1][j]-self.temp_nodos[i][j]
            calor = diff/resistencia
            return calor
            
    def main(self):
        self._crearMatriz()
        self._generarEcuaciones()
        #print(self.variables)
        self.valores_iniciales = [200]*self.x*self.y
        self.valores_n = sym.nsolve(self.ecuaciones,self.variables,self.valores_iniciales)
        #self.valores = sym.solve(self.ecuaciones)
        print(self.valores_n)
        print(type(self.valores_n))
        self.temperaturas()
        test = np.array(self.mat_num)
        print(type(test[0,0]))
        sns.heatmap(test)
        
    def temperaturas(self):
        self.mat_num = []
        for i,arr in enumerate(self.temp_nodos):
            aux = []
            for j,temp in enumerate(arr):
                aux.append(float(self.valores.get(self.temp_nodos[i][j]).evalf()))
            self.mat_num.append(aux)
        
        
sim = Simulacion(200,200,100,300,290,290,5,5,10,10)
sim.main()
            
            





        