from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Statistics
import pyevolve
import pandas as pd
textfile = "obj_p3.txt"
#En este problema puede ser de utilidad crear una clase que definan los objetos
#con el que cada objeto tiene las cualidades de valor y peso. Puede no usarla.
class Objeto(object):
    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso

#Peso maximo soportado por la mochila
maxpeso= 2000
costo = 100

#Agregue de alguna forma los objetos a una lista, o sus datos a la lista
datos = pd.read_csv(textfile,header=None)
valores = datos.values.astype('double')
n = valores.shape[0]
objetos = []
for i in xrange(n):
    objetos.append(Objeto(valores[i,0],valores[i,1]))

#Para la funcion de evaluacion, sume los valores de los objetos que estan
#en la mochila (en binario: 1 si esta dentro, 0 si no), y tambien los pesos
#si el peso se pasa del limite, reduzca el score de manera proporcional al exceso
#Recuerde que puede acceder a la propiedades de la clase usando x.valor y x.peso
def eval_func(chromosome):
    score = 0.0
    peso = 0.0
    binario = chromosome.getBinary()
    lbin = map(float, binario)
    for i,bit in enumerate(lbin):
        peso = peso + bit*objetos[i].peso
        score = score + bit*objetos[i].valor
    score = score - costo*(peso-maxpeso)*float((peso-maxpeso)>0)
    score = score*float(score>0)
    return score

#Defina el resto de parametros
genome = G1DBinaryString.G1DBinaryString(n)


genome.evaluator.set(eval_func)
genome.initializator.set(Initializators.G1DBinaryStringInitializator)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)

ga = GSimpleGA.GSimpleGA(genome)
#ga.selector.set(Selectors.GRouletteWheel)
#ga.selector.set(Selectors.GTournamentSelector)
#ga.selector.set(Selectors.GRankSelector)
ga.setGenerations(5)

ga.evolve()

print ga.bestIndividual()

mip = 0.0
mi = ga.bestIndividual().getBinary()
lbin = map(float,mi)
for i,bit in enumerate(lbin):
    mip = mip + bit*objetos[i].peso
print mip
