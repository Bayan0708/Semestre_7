import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Definir los datos
lista_de_numerosx = [0.069, 0.546, 1.265, 1.942, 2.585, 3.307, 3.93, 4.615, 5.348, 6.086, 6.619]
lista_de_numerosy = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Función para calcular el ajuste lineal y la pendiente
def ajuste_lineal(x, y):
    # Calcular la pendiente, intersección, coeficiente de correlación, valor p, y error estándar
    pendiente, intersección, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Generar valores ajustados basados en la pendiente e intersección
    ajuste = pendiente * np.array(x) + intersección
    
    # Imprimir los resultados
    print(f'Pendiente: {pendiente}')
    print(f'Intersección: {intersección}')
    print(f'Coeficiente de correlación: {r_value}')
    print(f'Valor p: {p_value}')
    print(f'Error estándar: {std_err}')
    
    # Graficar los datos y el ajuste lineal
    plt.scatter(x, y, label='Datos originales')
    plt.plot(x, ajuste, color='red', label='Ajuste lineal')
    plt.xlabel('amplitud real')
    plt.ylabel('amplitud efectiva')
    plt.title('Ajuste Lineal')
    plt.legend()
    plt.show()

    return pendiente, intersección, ajuste

# Ejemplo de uso
ajuste_lineal(lista_de_numerosx, lista_de_numerosy)
