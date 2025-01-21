import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk, Label, Entry, Button, messagebox

# Definición de la función Magnus
def magnus_proyectil(t, x, w):
    # Diámetro del proyectil en metros
    D = 7.2008e-2  
    # Masa del proyectil en kilogramos
    m = 1.5947e-1  
    # Coeficiente k relacionado con la resistencia del aire
    k = 1.22 * np.pi * D**2 / (8 * m)  
    # Coeficiente de arrastre (drag coefficient)
    Cd = 0.45  
    # Magnitud de la velocidad angular (norma del vector w)
    wRot = np.linalg.norm(w)  
    # Coeficiente lift (sustentación) que depende de la velocidad angular
    Cl = 0.3187 * (1 - np.exp(-2.483e-3 * wRot))  
    # Velocidad del proyectil calculada a partir de sus componentes
    v = np.sqrt(x[1]**2 + x[3]**2 + x[5]**2)  
    
    if wRot != 0:
        # Ecuaciones diferenciales que describen el movimiento del proyectil
        der = [
            x[1],  # Velocidad en x
            -k * v * (Cd * x[1] - Cl * (w[1] * x[5] - w[2] * x[3]) / wRot),  # Aceleración en x
            x[3],  # Velocidad en y
            -k * v * (Cd * x[3] - Cl * (w[2] * x[1] - w[0] * x[5]) / wRot),  # Aceleración en y
            x[5],  # Velocidad en z
            -9.8 - k * v * (Cd * x[5] - Cl * (w[0] * x[3] - w[1] * x[1]) / wRot)  # Aceleración en z, incluyendo gravedad
        ]
    else:
        # Ecuaciones diferenciales sin efecto Magnus (cuando no hay rotación)
        der = [
            x[1],  # Velocidad en x
            -k * v * Cd * x[1],  # Aceleración en x sin efecto Magnus
            x[3],  # Velocidad en y
            -k * v * Cd * x[3],  # Aceleración en y sin efecto Magnus
            x[5],  # Velocidad en z
            -9.8 - k * v * Cd * x[5]  # Aceleración en z sin efecto Magnus, incluyendo gravedad
        ]
    
    return der

# Evento para detener la simulación cuando z = 0
def stop_magnus_1(t, x, *args):
    return x[4]  # Se detiene cuando la posición z es cero

stop_magnus_1.terminal = True  # Indica que es un evento terminal
stop_magnus_1.direction = -1   # Indica que se debe buscar el evento al decrecer

# Función para simular y graficar la trayectoria del proyectil
def simulate_and_plot():
    try:
        # Lectura de los valores desde la interfaz gráfica
        v0 = float(v0_entry.get())  # Velocidad inicial ingresada por el usuario
        angle = float(angle_entry.get()) * np.pi / 180  # Conversión de grados a radianes
        
        # Lectura de las velocidades angulares ingresadas por el usuario y creación de vectores numpy
        w_values = [
            np.array([0, float(wy1_entry.get()), float(wz1_entry.get())]),
            np.array([0, float(wy2_entry.get()), float(wz2_entry.get())]),
            np.array([0, float(wy3_entry.get()), float(wz3_entry.get())]),
            np.array([0, float(wy4_entry.get()), float(wz4_entry.get())]),
            np.array([0, float(wy5_entry.get()), float(wz5_entry.get())]),
        ]

        # Condiciones iniciales del sistema: posición y velocidad iniciales del proyectil
        x0 = [0, v0 * np.cos(angle), 0, 0, 0, v0 * np.sin(angle)]  
        T = v0 * np.sin(angle) / 4.9  # Tiempo total de vuelo aproximado

        # Simulación para cada velocidad angular ingresada por el usuario
        trajectories = []  
        for w in w_values:
            sol = solve_ivp(
                magnus_proyectil, 
                [0, 2 * T], 
                x0, 
                args=(w,), 
                events=stop_magnus_1, 
                t_eval=np.linspace(0, 2 * T, 500)  # Evaluar la solución en puntos equidistantes en el tiempo
            )
            trajectories.append(sol)  # Almacena la solución de cada trayectoria

        # Creación de gráficas en 3D para visualizar las trayectorias del proyectil
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i, sol in enumerate(trajectories):
            ax.plot(sol.y[0], sol.y[2], sol.y[4])  # Grafica cada trayectoria

        ax.set_xlim(0, max(trajectories[0].y[0]))  # Limite del eje X basado en la trayectoria máxima
        ax.set_ylim(-5, 5)   # Limites fijos para el eje Y
        ax.set_zlim(0, 12)   # Limites fijos para el eje Z
        
        ax.set_xlabel('x (m)')   # Etiqueta para el eje X
        ax.set_ylabel('y (m)')   # Etiqueta para el eje Y
        ax.set_zlabel('z (m)')   # Etiqueta para el eje Z
        
        ax.set_title('Trayectoria del proyectil')   # Título del gráfico
        
        ax.view_init(20, 50)   # Configuración de la vista inicial del gráfico

        ax.legend([
            'ω_y={}, ω_z={}'.format(w[1], w[2]) for w in w_values   # Leyenda con las velocidades angulares para cada trayectoria
        ])
        
        plt.grid(True)   # Activa la cuadrícula en el gráfico
        plt.show()       # Muestra el gráfico
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")   # Manejo de errores si los valores ingresados no son válidos

# Interfaz gráfica con Tkinter para ingresar datos y ejecutar la simulación
root = Tk()
root.title("Simulación Magnus")   # Título de la ventana principal

# Entradas de datos para velocidad inicial y ángulo inicial con etiquetas correspondientes
Label(root, text="Velocidad inicial (m/s):").grid(row=0, column=0)
v0_entry = Entry(root)
v0_entry.grid(row=0, column=1)
v0_entry.insert(0, "60")   # Valor predeterminado

Label(root, text="Ángulo inicial (°):").grid(row=1, column=0)
angle_entry = Entry(root)
angle_entry.grid(row=1, column=1)
angle_entry.insert(0, "12")   # Valor predeterminado

# Entradas para las velocidades angulares con etiquetas correspondientes y valores predeterminados
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
wz4_entry.grid(row=5,column=3)
wz4_entry.insert(0,"-212")

Label(root,text="ω_y5:").grid(row=6,column=0)
wy5_entry = Entry(root)
wy5_entry.grid(row=6,column=1)
wy5_entry.insert(0,"0")

Label(root,text="ω_z5:").grid(row=6,column=2)
wz5_entry = Entry(root)
wz5_entry.grid(row=6,column=3)
wz5_entry.insert(0,"-300")

# Botón para ejecutar la simulación y graficar resultados al ser presionado por el usuario.
Button(root,text="Simular y Graficar",command=simulate_and_plot).grid(row=7,column=0,columnspan=4)

root.mainloop()   # Inicia el bucle principal de la interfaz gráfica.