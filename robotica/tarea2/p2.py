from pyevolve import G1DBinaryString #Se importa el objeto genoma de tipo binario
from pyevolve import GSimpleGA
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Statistics
import pyevolve
import math
#Se recomienda usar el archivo ex1.py como referencia.

#En el caso de muchas librerias como pyevolve, el fitness real es una transformacion (lineal, gaussiana, etc) del 
#score entregado por la funcion de evaluacion, por lo que en la pantalla de comando sale un Score o Raw, que corresponde
#al valor entregado por la funcion, y ademas un Fitness, que viene siendo el escalado del Score.

# Defina la funcion de evaluacion del problema
#En este caso tiene que transformar el individuo binario al valor entero que representa, luego aplicarle
#una transformacion lineal para ajustarlo al rango de [0.50], y finalmente aplicarle la funcion del enunciado.
def funcion_buscada(tiempo):
    ptermino = 346*math.exp(-0.0628*tiempo)
    stermino = math.sin(1.2544*tiempo+2.35)
    return abs(ptermino*stermino)

def linear_transform(number,imin,imax,omin,omax):
    result = (omax/imax)*(number-imin) + omin
    return result 

def eval_func(chromosome): #recibe un cromosoma, en este caso una lista de 1s y 0s
   score = 0.0
   pot = chromosome.getListSize()
   valor = chromosome.getDecimal()
   valor_escalado = linear_transform(valor,0,2.0**pot-1,0,50.0)
   print valor_escalado
   score = funcion_buscada(valor_escalado)
   return score

# Defina el tipo de genoma, en este caso G1DBinaryString.G1DBinaryString(numero de genes)
ngenes = 10
genome = G1DBinaryString.G1DBinaryString(ngenes)

#Muchos parametros tienen una opcion predefinida, numero de generaciones, probabilidades de mutacion y cruzamiento,
#metodos de mutacion, crossover, inicializacion, etc; pero se recomienda especificarlos en caso de ser relevantes 

# Defina que funcion evaluadora, initializator, mutator y crossover utilizara. Busque los ultimos 3 en el Anexo
genome.evaluator.set(eval_func)
genome.initializator.set(Initializators.G1DBinaryStringInitializator)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)

# Creacion del algoritmo genetico usando el "genome" definido
ga = GSimpleGA.GSimpleGA(genome)

# Defina el tipo de seleccion del algoritmo. Busquelo en el anexo
ga.selector.set(Selectors.GRouletteWheel)

# Numero de generaciones
ga.setGenerations(500)

#Ejecuta la evolucion
ga.evolve()

#Arroja el mejor individuo
print ga.bestIndividual()
print eval_func(ga.bestIndividual())