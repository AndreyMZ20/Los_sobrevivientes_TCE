import numpy as np
import matplotlib.pyplot as plt
from rcosdesign import rcosdesign



# Aplicar el coseno alzado a la señal
roll_off = 0.5  # Factor de exceso de ancho de banda
signal = [1] # Tu señal como un array de numpy



# Parámetros del pulso de coseno alzado
L = 16
pt = rcosdesign(roll_off, 6, L, 'normal')
# Aplicar el pulso de coseno alzado a la señal
señal_coseno_alzado = np.convolve(signal, pt, mode='same')


# Filtrar la señal recibida con el pulso de coseno alzado
senal_filtrada = np.convolve(señal_coseno_alzado, pt, mode='same')

# Inicializar una lista vacía para almacenar los bits recuperados
bits_recuperados = []

# Procesar la señal filtrada en segmentos correspondientes a cada bit transmitido
for i in range(0, len(senal_filtrada) - L//2, L):
    # Muestrear la señal filtrada en el instante de tiempo correspondiente al pico del pulso
    muestra = senal_filtrada[i + L//2]
    
    # Tomar una decisión sobre la muestra para determinar el valor del bit transmitido
    bit_recuperado = 1 if muestra > 0 else 0
    
    # Añadir el bit recuperado a la lista de bits recuperados
    bits_recuperados.append(bit_recuperado)



print(f'Senal original: {signal}')
# print(f'Señal con coseno alzado: {señal_coseno_alzado}')
# print(f'Señal muestreada: {señal_muestreada}')

print(f'Simbolos recuperados: {bits_recuperados}')