import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parámetros de la animación
radius = 1  # Radio del círculo
num_points = 100  # Número de puntos en el círculo
speed = 0.05  # Velocidad de rotación
frames = 200  # Número total de frames

# Crear figura y ejes
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')

# Crear un círculo inicial
circle = plt.Circle((0, 0), radius, color='b', fill=False)
ax.add_artist(circle)

# Función para actualizar la animación
def update(frame):
    ax.cla()  # Limpiar el eje
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')

    # Calcular la posición del círculo en función del frame
    angle = frame * speed
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    # Actualizar la posición del círculo
    circle = plt.Circle((x, y), radius, color='b', fill=False)
    ax.add_artist(circle)

    # Dibujar el vector de fuerza Magnus
    force_magnus_x = 1.5 * np.sin(angle)
    force_magnus_y = -1.5 * np.cos(angle)
    ax.quiver(x, y, force_magnus_x, force_magnus_y, angles='xy', scale_units='xy', scale=1, color='r')

    # Añadir texto
    ax.text(-2.5, 2.5, 'Efecto Magnus', fontsize=14)

# Crear la animación
ani = FuncAnimation(fig, update, frames=frames, interval=50)

# Mostrar la animación
plt.show()
