import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parámetros de la simulación
g = 9.81  # Aceleración debida a la gravedad (m/s²)
radius = 0.1  # Radio del círculo (m)
omega = 2.0  # Velocidad angular (rad/s)
dt = 0.05  # Intervalo de tiempo (s)
num_frames = 200  # Número total de frames

# Condiciones iniciales
y = 100.0  # Altura inicial (m), ahora 100 metros
x = 0.0    # Posición horizontal inicial (m)
vy = 0.0   # Velocidad vertical inicial (m/s)

# Listas para almacenar las posiciones
positions_x = [x]
positions_y = [y]

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(12, 10))  # Aumentar el tamaño de la figura
ax.set_xlim(-50, 50)  # Ampliar el límite horizontal
ax.set_ylim(0, 120)   # Aumentar el límite vertical para acomodar la nueva altura
ax.set_aspect('equal')

# Crear un círculo inicial
circle = plt.Circle((x, y), radius, color='b', fill=True)
ax.add_artist(circle)

# Función para actualizar la animación
def update(frame):
    global x, y, vy

    # Calcular la fuerza Magnus (proporcional a la velocidad y al giro)
    v_horizontal = 5.0  # Velocidad horizontal (m/s)
    force_magnus_x = 0.5 * omega * vy  # Fuerza Magnus en la dirección x
    force_magnus_y = 0.1 * omega * vy  # Fuerza Magnus en la dirección y

    # Actualizar la velocidad y posición
    vy += (g + force_magnus_y) * dt  # Aceleración total (gravedad + Magnus)
    y -= vy * dt  # Actualizar la posición vertical

    x += v_horizontal * dt + force_magnus_x * dt  # Actualizar posición horizontal

    # Almacenar la posición
    positions_x.append(x)
    positions_y.append(y)

    # Limpiar el eje y dibujar el nuevo círculo
    ax.cla()
    ax.set_xlim(-50, 50)  # Mantener el límite horizontal
    ax.set_ylim(0, 120)   # Mantener el límite vertical
    ax.set_aspect('equal')

    # Dibujar el círculo
    circle = plt.Circle((x, y), radius, color='b', fill=True)
    ax.add_artist(circle)

    # Dibujar la trayectoria
    ax.plot(positions_x, positions_y, color='orange', lw=2)

    # Añadir texto
    ax.text(-45, 110, 'Efecto Magnus en Caída Libre', fontsize=16)
    ax.text(-45, 105, f'Tiempo: {frame * dt:.2f} s', fontsize=14)

# Crear la animación
ani = FuncAnimation(fig, update, frames=num_frames, interval=50)

# Mostrar la animación
plt.show()
