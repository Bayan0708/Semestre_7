import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constantes
m = 0.43  # Masa del balón (kg)
r = 0.11  # Radio del balón (m)
rho = 1.225  # Densidad del aire (kg/m^3)
A = np.pi * r**2  # Área de la sección transversal del balón (m^2)
C_d = 0.25  # Coeficiente de resistencia aerodinámica
C_m = 0.2  # Coeficiente del efecto Magnus
g = 9.81  # Aceleración de la gravedad (m/s^2)

# Condiciones iniciales
v0 = 35  # Velocidad inicial (m/s)
theta = np.radians(30)  # Ángulo de disparo (grados)
phi = np.radians(10)  # Ángulo horizontal (grados)
omega = np.array([0, 100, 0])  # Velocidad angular del balón (rad/s)

# Componentes de la velocidad inicial
v0_x = v0 * np.cos(theta) * np.cos(phi)
v0_y = v0 * np.sin(phi)
v0_z = v0 * np.sin(theta)

# Tiempo de simulación
dt = 0.01  # Paso de tiempo (s)
t_max = 4  # Tiempo máximo de simulación (s)
n_steps = int(t_max / dt)

# Inicialización de variables
x, y, z = [0], [0], [0]  # Posiciones iniciales
vx, vy, vz = [v0_x], [v0_y], [v0_z]  # Velocidades iniciales

# Simulación de la trayectoria
for _ in range(n_steps):
    # Velocidad actual
    v = np.array([vx[-1], vy[-1], vz[-1]])
    v_mag = np.linalg.norm(v)
    
    # Fuerza de resistencia aerodinámica
    F_d = -0.5 * C_d * rho * A * v_mag * v
    
    # Fuerza de Magnus
    F_m = C_m * rho * A * np.cross(omega, v)
    
    # Fuerza gravitacional
    F_g = np.array([0, 0, -m * g])
    
    # Fuerza total
    F_total = F_d + F_m + F_g
    
    # Aceleración
    a = F_total / m
    
    # Actualización de velocidades
    new_vx = vx[-1] + a[0] * dt
    new_vy = vy[-1] + a[1] * dt
    new_vz = vz[-1] + a[2] * dt
    
    # Actualización de posiciones
    new_x = x[-1] + vx[-1] * dt
    new_y = y[-1] + vy[-1] * dt
    new_z = z[-1] + vz[-1] * dt
    
    # Condición de suelo
    if new_z < 0:
        break
    
    # Almacenar valores
    vx.append(new_vx)
    vy.append(new_vy)
    vz.append(new_vz)
    x.append(new_x)
    y.append(new_y)
    z.append(new_z)

# Graficar trayectoria
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label="Trayectoria del balón")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Efecto Magnus - Gol de Roberto Carlos")
ax.legend()
plt.show()
