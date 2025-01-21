import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales
mass = 0.045  # Masa de la esfera (kg)
radius = 0.11  # Radio de la esfera (m)
velocity = np.array([30.0, 20.0], dtype=np.float64)  # Velocidad inicial en (m/s)
angular_velocity = 50  # Velocidad angular en rad/s
drag_coefficient = 0.47  # Coeficiente de arrastre de una esfera
density_air = 1.2  # Densidad del aire (kg/m^3)
g = 9.81  # Gravedad (m/s^2)
dt = 0.01  # Paso de tiempo (s)

# Función para calcular la fuerza Magnus
def magnus_force(radius, angular_velocity, velocity):
    magnus_coefficient = 0.5 * density_air * np.pi * (radius**2)
    perpendicular_velocity = np.array([-velocity[1], velocity[0]])  # Perpendicular a la velocidad
    magnus_force = magnus_coefficient * angular_velocity * perpendicular_velocity
    return magnus_force

# Simulación
positions = [np.array([0, 0])]  # Posición inicial
vel = np.copy(velocity)

for _ in range(1000):
    # Calcular la fuerza Magnus
    Fm = magnus_force(radius, angular_velocity, vel)
    
    # Calcular aceleración neta
    acc = np.array([0, -g]) + Fm / mass  # Incluye gravedad y fuerza Magnus
    
    # Actualizar velocidad y posición
    vel += acc * dt
    new_position = positions[-1] + vel * dt
    positions.append(new_position)
    
    # Parar si la esfera llega al suelo
    if new_position[1] < 0:
        break

# Graficar resultados
positions = np.array(positions)
plt.plot(positions[:, 0], positions[:, 1])
plt.xlabel('Distancia (m)')
plt.ylabel('Altura (m)')
plt.title('Trayectoria del Proyectil con Efecto Magnus')
plt.grid()
plt.show()
