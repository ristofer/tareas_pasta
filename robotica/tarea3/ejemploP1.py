from sklearn.neural_network import MLPClassifier
#Ejemplo de manzanas y duraznos
#Caracteristicas = [Peso,textura]
#0=suave;1=aspero
#Manzana = 0, Durazno = 1
#Datos de entrenamiento
#caracteristicas = [[120,0],[170,1],[180,1],[140,0]]
#etiquetas= [0, 1, 1, 0]
caracteristicas = [[60, 1], [30, 2.5], [70, 1.5], [48, 2], [55, 1.5], [58, 2]]
etiquetas = [1, 0, 1, 0, 0, 1]


#Creacion del clasificador (tipo MLP)
clf=MLPClassifier(hidden_layer_sizes=(10, 10))
#Entrenamiento
clf=clf.fit(caracteristicas,etiquetas)

test = [[57,1.5],[60,1.7]]

print clf.predict(test)
