import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter



#Para simular una señal de cosenos alzados 

A = 1          # Amplitud
n = 4          # Exponente
f = 1          # Frecuencia en Hz
phi = 0        # Fase
num_puntos = 1000
# Tiempo
t = np.linspace(0, 2, num_puntos)  # Generar valores de tiempo de 0 a 2 segundos

# Generar la señal de coseno elevado
cosine_signal = A * np.cos(2 * np.pi * f * t)**n


# Definir la frecuencia de muestreo y la frecuencia de corte del filtro
fs = 1000  # Frecuencia de muestreo en Hz
cutoff_freq = 100  # Frecuencia de corte del filtro en Hz

# Longitud del filtro FIR (número de coeficientes)
num_taps = 101

# Crear los coeficientes del filtro FIR usando firwin
coefficients = firwin(num_taps, cutoff_freq, fs=fs)



# Aplicar el filtro FIR a la señal de entrada usando lfilter
senal_filtrada = lfilter(coefficients, 1.0, cosine_signal)

# Graficar la señal de entrada y la señal filtrada
plt.figure(figsize=(10, 6))
plt.plot(t, cosine_signal, label='Señal de Entrada')
plt.plot(t, senal_filtrada, label='Señal Filtrada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()