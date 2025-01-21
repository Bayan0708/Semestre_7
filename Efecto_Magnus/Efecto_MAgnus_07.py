import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Definición de la función Magnus
def magnus_proyectil(t, x):
    D = 7.2008e-2
    m = 1.5947e-1
    k = 1.22 * np.pi * D**2 / (8 * m)
    Cd = 0.45
    wRot = np.linalg.norm(w)
    Cl = 0.3187 * (1 - np.exp(-2.483e-3 * wRot))
    v = np.sqrt(x[1]**2 + x[3]**2 + x[5]**2)
    
    if wRot != 0:
        der = [
            x[1],
            -k * v * (Cd * x[1] - Cl * (w[1] * x[5] - w[2] * x[3]) / wRot),
            x[3],
            -k * v * (Cd * x[3] - Cl * (w[2] * x[1] - w[0] * x[5]) / wRot),
            x[5],
            -9.8 - k * v * (Cd * x[5] - Cl * (w[0] * x[3] - w[1] * x[1]) / wRot)
        ]
    else:
        der = [
            x[1],
            -k * v * Cd * x[1],
            x[3],
            -k * v * Cd * x[3],
            x[5],
            -9.8 - k * v * Cd * x[5]
        ]
    
    return der

# Evento para detener la simulación cuando z = 0
def stop_magnus_1(t, x):
    return x[4]

stop_magnus_1.terminal = True
stop_magnus_1.direction = -1

# Condiciones iniciales
th = 12 * np.pi / 180
v0 = 60
x0 = [0, v0 * np.cos(th), 0, 0, 0, v0 * np.sin(th)]
T = v0 * np.sin(th) / 4.9

# Simulación para diferentes velocidades angulares
w_values = [
    np.array([0, -300, 0]), 
    np.array([0, 212, 212]), 
    np.array([0, 0, 300]), 
    np.array([0, -212, -212]), 
    np.array([0, 0, -300])
]

trajectories = []
for w in w_values:
    sol = solve_ivp(magnus_proyectil, [0, 2 * T], x0, events=stop_magnus_1, t_eval=np.linspace(0, 2 * T, 500))
    trajectories.append(sol)

# Gráficas 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, sol in enumerate(trajectories):
    ax.plot(sol.y[0], sol.y[2], sol.y[4])

ax.set_xlim(0, max(trajectories[0].y[0]))
ax.set_ylim(-5, 5)
ax.set_zlim(0, 12)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.set_title('Trayectoria del proyectil')
ax.view_init(20, 50)  # Ajuste del ángulo de vista

ax.legend(['ω_y=-300', 'ω_y=212, ω_z=212', 'ω_z=300', 'ω_y=-212, ω_z=-212', 'ω_z=-300'])
plt.grid(True)
plt.show()
