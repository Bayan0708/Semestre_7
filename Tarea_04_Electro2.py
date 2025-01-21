import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constantes
k = 1.0  # Valor arbitrario de la constante k
R = 1.0  # Radio de la esfera

# Densidad de carga en la superficie de la esfera
def rho_surface(theta, phi):
    r = R  # En la superficie de la esfera
    return k * (R / r**2) * (R - 2 * r) * np.sin(theta)

# Crear mallas de coordenadas esféricas
theta = np.linspace(0, np.pi, 100)  # Ángulo polar
phi = np.linspace(0, 2 * np.pi, 100)  # Ángulo azimutal
theta, phi = np.meshgrid(theta, phi)

# Coordenadas cartesianas de la superficie de la esfera
x = R * np.sin(theta) * np.cos(phi)
y = R * np.sin(theta) * np.sin(phi)
z = R * np.cos(theta)

# Evaluar la densidad de carga en la superficie
rho_values = rho_surface(theta, phi)

# Crear la gráfica 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot de la superficie con los valores de la densidad de carga
surface = ax.plot_surface(x, y, z, facecolors=plt.cm.viridis((rho_values - np.min(rho_values)) / (np.max(rho_values) - np.min(rho_values))), rstride=1, cstride=1, antialiased=True)

# Añadir una barra de color para representar la densidad de carga
mappable = plt.cm.ScalarMappable(cmap='viridis')
mappable.set_array(rho_values)
plt.colorbar(mappable, shrink=0.5, aspect=5, label='Densidad de Carga ρ(r, θ)')

# Configurar los ejes
ax.set_title('Densidad de Carga en la Superficie de la Esfera')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
