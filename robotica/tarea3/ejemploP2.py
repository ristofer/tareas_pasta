from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sbn
wine = load_wine()  # Carga el dataset
print wine.feature_names  # Nombre de caracteristicas
print wine.target_names  # Nombre de etiquetas
print wine.target
x = wine.data
y = wine.target

precisiones = []
for i in range(5,99):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=i/100.0, random_state=1)  # Divide los datos de forma aleatoria
    # Creando dos grupos, uno de entrenamiento y otro de prueba



    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10),
                        max_iter=500)  ##se pueden especificar la cantidad de neuronas por capa
    # con hidden_layer_sizes=(cantidad_capa1,cantidad_capa2,...)
    # Ademas se pueden especificar la cantidad de iteraciones maximas hasta que el MLP converja a un optimo
    mlp.fit(x_train, y_train)

    caso = mlp.predict(x_test[0].reshape(1,-1))
    print y_test[0]

    print caso
    predictions = mlp.predict(x_test)
    acc = accuracy_score(y_test, predictions)
    print acc
    precisiones.append((i,acc))

print precisiones
plt.plot(precisiones)
plt.show()