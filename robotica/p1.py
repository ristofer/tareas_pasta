import random #libreria util con funciones aleatoruas
import copy #libreria util para copiar objetos, listas por ejemplo

#Es importante destacar que python asigna variables a valores u objetos, no al reves; esto quiere decir que
#que si se tiene x=[1 2] & y=x, si se aplica y.append(3)  (agrega el valor 3 al final de la lista),
#print y   devuelve [1 2 3]  &  print x    devuelve [1 2 3], ambas listas se modifican ya que ambas variables
#estan asignadas al mismo objeto, y lo que se modifica es el objeto en si; la libreria copy ayuda con esto,
#al generar una copia del objeto usando y=copy.copy(x) , asi se asigna cada variable a un objeto distinto


#La funcion de inicializacion es la encargada de crear individuos que serviran de poblacion inicial
#estos tienen que seguir la representacion de individuo que se usara en el algoritmo,
#en este caso un individuo es un numero real aleatorio dentro del rango [-10,10]
#Haga que la funcion cree un individuo de este tipo, y lo devuelva (return)
#Ayudese de la funcion random.uniform()
def Inicializacion(Nmax, Nmin):  #Nmax=numero maximo=10 , Nmin=numero minimo=-10
    indiv = random.uniform(Nmin,Nmax)
    return indiv



#La funcion de cruzamiento toma 2 individuos, los reproduce y crea uno o mas hijos; este cruzamiento debe tener sentido para
#la representacion de individuo, debe definir 'Que significa cruzar 2 individuos',
#en este caso reproducir 2 individuos es tomar el promedio aritmetico entre los padres, y devolver el promedio como hijo
#Esta funcion tambien incluye una probabilidad de que ocurra reproduccion, individuos pueden intentar reproducirse y no lograrlo
#si los individuos no logran reproducirse, devuelva uno de los padres, al azar
#Ayudese de las funciones random.random() y random.choice()
def Cruzamiento(Pcros,indiv1, indiv2): #Pcros=probabilidad cruzamiento, indiv1,indiv2=padres 
    if random.random()<Pcros:
        return random.choice((indiv1,indiv2))
    else:
        prom = (indiv1+indiv2)/2.0
        return prom


    




#La funcion de mutacion toma un hijo y lo muta, debe definir que significa 'mutar un individuo',
#en este caso mutar un individuo es reemplazar el valor del individuo por un valor aleatorio dentro del rango [-10,10]
#Esta funcion tambien incluye una probabilidad de que ocurra mutacion, un individuo puede no mutar
#si el individuo logra mutar, devuelva el individuo mutado, si no muta, devuelva el individuo original
#Ayudese de random.uniform()
def Mutacion(indiv, Pmut,  Nmax, Nmin): #Pmut=probabilidad mutacion, indiv=individuo, Nmax=numero maximo, Nmin=numero minimo
    if random.random()<Pmut:
        return indiv
    else:
        return random.uniform(Nmin,Nmax)

    




#La funcion de fitness se encarga de evaluar que tan bueno es el individuo, y le asigna un valor numerico a ello
#debe definir 'que significa que un individuo sea una buena solucion',
#en este caso, eso se define con la funcion del enunciado, como se busca el maximo, mientras mayor sea f(individuo) mejor
def Func_fitness(indiv): #indiv=individuo
    fitness = 100 - indiv**2
    return fitness




#La funcion de seleccion se encarga de seleccionar que individuos de la poblacion se reproduciran
#Para este problema se usara la seleccion por torneo, esta toma k(definido) individuos de la poblacion, evalua el fitness 
#de cada uno de ellos, toma el individuo con mayor fitness, lo reproduce con el resto k-1 individuos, muta los hijos, y los agrega a la nueva poblacion;
# esto puede producir menos hijos para la nueva poblacion, que padres de la poblacion anterior, por lo que el proceso de torneo se repite hasta 
#que la la cantidad de hijos (la nueva poblacion), sea igual a la cantidad de la poblacion anterior (y asi mantenerla constante)
#NOTA: si se tiene una lista de listas, y se quiere ordenar la lista principal, sorted() ordena de menor a mayor la lista
#principal, basandose en el primer valor de cada lista secundaria, es decir:
# list=[[4,5],[2,9]]    a=sorted(list)   print a --> [[2,9],[4,5]]    porque 2<4

#En resumen, tome la poblacion, escoja k individuos, evalue su fitness, tome el mejor, reproduzcalo con cada uno del k-1 resto,
#mute a los hijos, luego incluyalos a la nueva poblacion, repita hasta que la cantidad de individuos de la nueva poblacion sea igual al anterior 
#Pueden serle util las funciones copy.copy(), random.choice() o random.sample(), x.append(), sorted(), x.remove(), x.reverse() y break
def Seleccion(Pob, Ntor, Pcros, Pmut): #Pob=poblacion, Ntor=k individuos que toma el torneo, Pcros=probabilidad crossover, Pmut=probabilidad mutacion
    New_pob=[]
    Sorted_pob = []
    #ejecute el torneo hasta que las cantidades de individuos sean iguales
    while len(New_pob) < len(Pob):
        Tournament = random.sample(Pob,Ntor)

        #tome k (Ntor) individuos, evalueles y ordenelos (tenga precaucion con este paso) 
        for i in xrange(Ntor):
            ifit = Func_fitness(Tournament[i])
            Sorted_pob.append((ifit,Tournament[i]))
        Sorted_pob.sort()  
        Winner = Sorted_pob[-1][1]
        #agrege a los hijos (reproduzcalocalos con Cruzamiento() y mutelos con Mutacion() ) a la nueva poblacion,
        #si llega al limite de cantidad de individuos por poblacion, salga con break
        for x in xrange(Ntor-1):
            Pareja = Sorted_pob[-x][1]
            if len(New_pob) == len(Pob):
                break
            Son = Cruzamiento(Pcros,Winner,Pareja)
            Son = Mutacion(Pmut,Son,10,-10)
            New_pob.append(Son)
        
    return New_pob

#Defina el numero de individuos por poblacion, numero real maximo para individuo, numero real minimo para individuo,
#probabilidad de cruzamiento, probabilidad de mutacion y numero de generaciones, en ese orden 
Npob = 1000
Nmax = 10
Nmin = -10
Pcros = 0.5
Pmut = 0.5
Ngen = 1000

Ntor= 27

Current_gen = 1 #contador de generaciones
Pob = []
#Ahora se ejecuta la evolucion

#Cree la primera poblacion inicializando cada individuo
for x in xrange(Npob):
    Pob.append(Inicializacion(Nmax,Nmin))

#evolucione las poblaciones hasta llegar al maximo de generaciones
while Ngen > Current_gen:
    New_pob = Seleccion(Pob,Ntor,Pcros,Pmut)
    #Ejecute la seleccion (que incluye la reproduccion), el resultado de esto asignelo como New_pob
    

    Pob = New_pob 
    Current_gen += 1


#Encuentre el individuo con mayor fitness en la poblacion final, y muestrelo en pantalla
Sorted = []
for x in xrange(Npob):
    ifit = Func_fitness(Pob[x])
    Sorted.append((ifit,Pob[x]))
Sorted.sort()  
ganador = Sorted[-1][1]
print ganador
