from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Initializators
from pyevolve import Statistics
from pyevolve import DBAdapters
import pyevolve

def eval_func(chromosome):
   score = 0.0
   for value in chromosome:
      score = -value**2 +100
   return score

genome = G1DList.G1DList(1)
genome.setParams(rangemin=-10, rangemax=10)

genome.evaluator.set(eval_func)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealRange)
genome.crossover.set(Crossovers.G1DListCrossoverUniform)

ga = GSimpleGA.GSimpleGA(genome)

ga.selector.set(Selectors.GTournamentSelector)

ga.setGenerations(500)

ga.evolve()

print ga.bestIndividual()