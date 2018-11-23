from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import GAllele
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import Crossovers
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import Consts
import sys, random
from math import sqrt
import pandas as pd
#En este problema tiene ingresar las coordenadas de las ciudades al codigo, y usarlas en el algoritmo.
#Tiene que generar un grafico de fitness(raw score) maximo vs generacion para distintos valores de Pcros, Pmut, y Npop.
#El codigo incluye una manera de guardar estos datos en un archivo de texto 'fitp4.txt' que puede luego trabajar en Matlab
filename = "coordenadas_p4.txt"
datos = pd.read_csv(filename,header=None)
ciudades = datos.values


#Funcion que ayuda a guardar los datos de fitness, no necesita modificarla 
Ldat=[]#lista de datos para la funcion callback
def evolve_callback(ga):
	x=ga.getCurrentGeneration()
	stats = ga.getStatistics()
	Ldat.append(stats["rawMax"])

#Debido a que pyevolve no tiene un inicializador de orden, se crea uno para la ocasion
def G1DListTSPInitializator(genome, **args):
	genome.clearList()
	lst = [i for i in xrange(1,21)]
	for i in xrange(1,21):
		choice = random.choice(lst)
		lst.remove(choice)
		genome.append(choice)

def calc_dist(x1,y1,x2,y2):
	fterm = (x1-x2)**2
	sterm = (y1-x2)**2
	dist = sqrt(fterm+sterm)
	return dist


#Funcion de evaluacion
#Recuerde que debe minimizar la distancia recorrida
def eval_func(chromosome):
	score = 0.0
	distancia = 0
	orden = chromosome
	prev = orden[0] - 1
	for i in xrange(1,20):
		j = orden[i] - 1
		distancia = distancia + calc_dist(ciudades[prev][0],ciudades[prev][1],ciudades[j][0],ciudades[j][1])
		prev = j
	score = 60/distancia
	return score
#Para generar los datos fitness maximo vs generacion para distintos parametros,
#corra este archivo p4.py cada vez que cambie Pmut, Pcros o Npop,
#el programa guardara los datos de fitness maximoen cada generacion de dicha evolucion en el archivo 'fitp4.txt'
#El archivo 'fitp4.txt' se reescribe cada vez que corre la evolucion, asi que guardelo para cada valor que cambie
#Puede hacer los graficos en Matlab

#use 3 valores distintos para la probabilidad de mutacion, 3 distintos para la probabilidad de cruzamiento,
#y 3 distintos numero de individuos por poblacion
Pmut=0.3 #probabilidad de mutacion
Pcros=0.9 #probabilidad de cruzamiento
Npop=1600 #Numero de individuos por poblacion

#Elija el numero de generaciones que quiera
Numero_generaciones=5000


setOfAlleles = GAllele.GAlleles()

genome = G1DList.G1DList(20)

genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DListMutatorSwap)
genome.crossover.set(Crossovers.G1DListCrossoverOX)
genome.initializator.set(G1DListTSPInitializator)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GTournamentSelector)

ga.setGenerations(Numero_generaciones)
ga.setCrossoverRate(Pcros)
ga.setMutationRate(Pmut)
ga.setPopulationSize(Npop)

#llama a la funcion evolve_callback en cada generacion, que guarda el fitness
ga.stepCallback.set(evolve_callback)

ga.evolve()
best = ga.bestIndividual()
print best



#se escribe el fitness de cada generacion en el archivo fitp4.txt,
filehandle = open('fitp4-{}-{}-{}.txt'.format(Pmut,Pcros,Npop), "w")
for w in xrange(len(Ldat)-1):
	filehandle.write(str(Ldat[w])+',')
filehandle.write(str(Ldat[w+1]))
filehandle.close()

#Estando en Matlab, el archivo fitp4.txt puede importarlo a Matlab usando:
# L = csvread('fitp4.txt');
#
#lo que crea un vector de nombre L con los valores de fitness
