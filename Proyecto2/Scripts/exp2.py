# import numpy as np
# import matplotlib.pyplot as plt

# # Parámetros del pulso
# T = 0.5  # Duración del pulso
# t = np.linspace(-3, 3, 1500, endpoint=False)

# # Generar dos pulsos rectangulares
# pulso_rectangular1 = np.where((t >= -T/2) & (t <= T/2), 1, 0)
# pulso_rectangular2 = np.where((t >= 2*T) & (t <= 3*T), 1, 0)
# pulso_rectangular = pulso_rectangular1 + pulso_rectangular2

# # Calcular la Transformada de Fourier
# transformada = np.fft.fft(pulso_rectangular)
# transformada_shift = np.fft.fftshift(transformada)  # Centrar la Transformada de Fourier
# frecuencias = np.fft.fftfreq(t.shape[-1])
# frecuencias_shift = np.fft.fftshift(frecuencias)  # Centrar las frecuencias

# # Crear las gráficas
# plt.figure()

# # Gráfica del pulso rectangular
# plt.subplot(2, 1, 1)
# plt.plot(t, pulso_rectangular)
# plt.title('Pulso Rectangular')

# # Gráfica de la Transformada de Fourier
# plt.subplot(2, 1, 2)
# plt.plot(frecuencias_shift, np.abs(transformada_shift))
# plt.title('Transformada de Fourier')


# plt.tight_layout()
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Usa tu lista específica de 1s y 0s
data = np.array([0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,1,1,0,0,0,1,1,0,0,1,1,0,0])

# Frecuencia del reloj
frecuencia_reloj = 100  # Ajusta este valor a la frecuencia deseada

# Generar el reloj
clock = np.array([0, 1] * int(len(data) // frecuencia_reloj))

# Crear la señal digital
digital_signal = np.zeros((int(data.size * frecuencia_reloj),))
for i in range(data.size):
    digital_signal[i*int(frecuencia_reloj):(i+1)*int(frecuencia_reloj)] = data[i]

# Crear el tiempo
time = np.linspace(0, 1, len(digital_signal), endpoint=False)

# Graficar la señal en el tiempo
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(time, digital_signal, drawstyle='steps-pre')
plt.title('Señal en el Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')

# Calcular la Transformada de Fourier con más puntos
num_puntos = 3 * len(digital_signal)  # Ajusta este valor al número de puntos que desees
transformada = np.fft.fft(digital_signal, n=num_puntos)
transformada_shift = np.fft.fftshift(transformada)  # Centrar la Transformada de Fourier
frecuencias = np.fft.fftfreq(num_puntos)
frecuencias_shift = np.fft.fftshift(frecuencias)  # Centrar las frecuencias

# Graficar el espectro de frecuencia
plt.subplot(2, 1, 2)
plt.plot(frecuencias_shift, np.abs(transformada_shift))
plt.title('Espectro de Frecuencia')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.tight_layout()
plt.show()




