import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, Label, Entry, Button, messagebox

# Definición de la función Magnus
def magnus_proyectil(t, x, w):
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
def stop_magnus_1(t, x, *args):
    return x[4]

stop_magnus_1.terminal = True
stop_magnus_1.direction = -1

# Función para simular y graficar
def simulate_and_plot():
    try:
        # Lectura de los valores desde la interfaz
        v0 = float(v0_entry.get())
        angle = float(angle_entry.get()) * np.pi / 180
        w_values = [
            np.array([0, float(wy1_entry.get()), float(wz1_entry.get())]),
            np.array([0, float(wy2_entry.get()), float(wz2_entry.get())]),
            np.array([0, float(wy3_entry.get()), float(wz3_entry.get())]),
            np.array([0, float(wy4_entry.get()), float(wz4_entry.get())]),
            np.array([0, float(wy5_entry.get()), float(wz5_entry.get())]),
        ]

        # Condiciones iniciales
        x0 = [0, v0 * np.cos(angle), 0, 0, 0, v0 * np.sin(angle)]
        T = v0 * np.sin(angle) / 4.9

        # Simulación para cada velocidad angular
        trajectories = []
        for w in w_values:
            sol = solve_ivp(
                magnus_proyectil, 
                [0, 2 * T], 
                x0, 
                args=(w,), 
                events=stop_magnus_1, 
                t_eval=np.linspace(0, 2 * T, 500)
            )
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
        ax.view_init(20, 50)

        ax.legend([
            'ω_y={}, ω_z={}'.format(w[1], w[2]) for w in w_values
        ])
        plt.grid(True)
        plt.show()
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Interfaz gráfica con Tkinter
root = Tk()
root.title("Simulación Magnus")

# Entradas de datos
Label(root, text="Velocidad inicial (m/s):").grid(row=0, column=0)
v0_entry = Entry(root)
v0_entry.grid(row=0, column=1)
v0_entry.insert(0, "60")

Label(root, text="Ángulo inicial (°):").grid(row=1, column=0)
angle_entry = Entry(root)
angle_entry.grid(row=1, column=1)
angle_entry.insert(0, "12")

# Velocidades angulares
Label(root, text="ω_y1:").grid(row=2, column=0)
wy1_entry = Entry(root)
wy1_entry.grid(row=2, column=1)
wy1_entry.insert(0, "-300")

Label(root, text="ω_z1:").grid(row=2, column=2)
wz1_entry = Entry(root)
wz1_entry.grid(row=2, column=3)
wz1_entry.insert(0, "0")

Label(root, text="ω_y2:").grid(row=3, column=0)
wy2_entry = Entry(root)
wy2_entry.grid(row=3, column=1)
wy2_entry.insert(0, "212")

Label(root, text="ω_z2:").grid(row=3, column=2)
wz2_entry = Entry(root)
wz2_entry.grid(row=3, column=3)
wz2_entry.insert(0, "212")

Label(root, text="ω_y3:").grid(row=4, column=0)
wy3_entry = Entry(root)
wy3_entry.grid(row=4, column=1)
wy3_entry.insert(0, "0")

Label(root, text="ω_z3:").grid(row=4, column=2)
wz3_entry = Entry(root)
wz3_entry.grid(row=4, column=3)
wz3_entry.insert(0, "300")

Label(root, text="ω_y4:").grid(row=5, column=0)
wy4_entry = Entry(root)
wy4_entry.grid(row=5, column=1)
wy4_entry.insert(0, "-212")

Label(root, text="ω_z4:").grid(row=5, column=2)
wz4_entry = Entry(root)
wz4_entry.grid(row=5, column=3)
wz4_entry.insert(0, "-212")

Label(root, text="ω_y5:").grid(row=6, column=0)
wy5_entry = Entry(root)
wy5_entry.grid(row=6, column=1)
wy5_entry.insert(0, "0")

Label(root, text="ω_z5:").grid(row=6, column=2)
wz5_entry = Entry(root)
wz5_entry.grid(row=6, column=3)
wz5_entry.insert(0, "-300")

# Botón para graficar
Button(root, text="Simular y Graficar", command=simulate_and_plot).grid(row=7, column=0, columnspan=4)

root.mainloop()
