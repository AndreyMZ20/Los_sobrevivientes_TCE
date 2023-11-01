import numpy as np
import matplotlib.pyplot as plt
from rcosdesign import rcosdesign

def generar_cadena_binaria():
    cadena = ''.join(['1' if i % 2 == 0 else '0' for i in range(32)])
    return cadena

def codificar_manchester(binario):
    tiempo = []
    señal = []

    for bit in binario:
        if bit == "1":
            tiempo.extend([0, 0.5, 0.5, 1])
            señal.extend([1, 1, -1, -1])
        else:
            tiempo.extend([0, 0.5, 0.5, 1])
            señal.extend([-1, -1, 1, 1])

    tiempo = [t for t in range(len(tiempo))]

    return tiempo, señal

# Parámetros del pulso de coseno alzado
Ts = 1
L = 16
a_values = [1e-6, 0.25, 0.75, 1.0]
t = np.arange(-3, 3 + Ts / L, Ts / L)

# Crear una nueva figura para el gráfico del pulso de coseno alzado
plt.figure()

# Iterar a través de los valores de a para el pulso de coseno alzado
for a in a_values:
    pt = rcosdesign(a, 6, L, 'normal')
    plt.plot(t, pt, label=f'a = {a}')  # Usar el valor de a como etiqueta

plt.grid(True)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Pulso de Coseno Alzado')
plt.legend()

# Generar una cadena binaria usando la función generar_cadena_binaria
cadena_binaria = generar_cadena_binaria()

# Codificar la señal Manchester
tiempo_manchester, señal_manchester = codificar_manchester(cadena_binaria)

# Crear una nueva figura para el gráfico de la codificación Manchester
plt.figure()
plt.plot(tiempo_manchester, señal_manchester)
plt.grid(True)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Codificación Manchester')

# Aplicar el pulso de coseno alzado a la señal Manchester
señal_coseno_alzado = np.convolve(señal_manchester, pt, mode='same')

# Crear una nueva figura para el gráfico de la señal con el coseno alzado
plt.figure()
plt.plot(tiempo_manchester, señal_coseno_alzado)
plt.grid(True)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal con Pulso de Coseno Alzado')

plt.show()
