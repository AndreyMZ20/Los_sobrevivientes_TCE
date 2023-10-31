import matplotlib.pyplot as plt
from scipy.signal import rcosdesign, convolve
import numpy as np

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

def rz_encoder(binary_string):
    rz_signal = []

    for bit in binary_string:
        if bit == "0":
            rz_signal.extend([0, 0])
        else:
            rz_signal.extend([1, 0])

    return rz_signal

def nrz_encode(bit_string):
    mapping = {'0': -1, '1': 1}
    nrz_encoded = [mapping[bit] for bit in bit_string]
    return nrz_encoded

def aplicar_coseno_alzado(señal, duracion_bit, frecuencia_muestreo, rolloff=0.2):
    filtro_coseno_alzado = rcosdesign(rolloff, int(1 / (2 * duracion_bit)), int(1 / frecuencia_muestreo))
    señal_coseno_alzado = convolve(señal, filtro_coseno_alzado, mode='same')
    tiempo_coseno = np.linspace(0, len(señal_coseno_alzado) / frecuencia_muestreo, len(señal_coseno_alzado))
    return tiempo_coseno, señal_coseno_alzado

# Generar una cadena binaria usando la función generar_cadena_binaria
cadena_binaria = generar_cadena_binaria()

# Selecciona la codificación deseada (Manchester, NRZ o RZ)
codificacion_deseada = "Manchester"  # Cambiar a "NRZ" o "RZ" según sea necesario

# Codificar la señal según la codificación deseada
if codificacion_deseada == "Manchester":
    tiempo, señal = codificar_manchester(cadena_binaria)
elif codificacion_deseada == "NRZ":
    tiempo = list(range(len(cadena_binaria)))
    señal = nrz_encode(cadena_binaria)
elif codificacion_deseada == "RZ":
    tiempo = list(range(len(cadena_binaria) * 2))
    señal = rz_encoder(cadena_binaria)

# Parámetros de la señal de coseno alzado
duracion_bit = 0.5  # Duración de cada bit en segundos
frecuencia_muestreo = 1000  # Frecuencia de muestreo en Hz
rolloff = 0.2  # Factor de roll-off del filtro de coseno alzado

# Aplicar el coseno alzado a la señal
tiempo_coseno, señal_coseno_alzado = aplicar_coseno_alzado(señal, duracion_bit, frecuencia_muestreo, rolloff)

# Graficar la señal de coseno alzado
plt.plot(tiempo_coseno, señal_coseno_alzado)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.title(f"Señal de Coseno Alzado ({codificacion_deseada})")
plt.grid(True)
plt.show()
  