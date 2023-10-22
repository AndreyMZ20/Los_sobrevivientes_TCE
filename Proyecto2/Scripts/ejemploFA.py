import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
num_bits = 1000  # Número de bits en la señal NRZ
snr_dB = 10  # Relación señal-ruido en dB
symbol_rate = 1000  # Tasa de símbolos en símbolos por segundo

# Crear señal NRZ aleatoria
nrz_signal = np.random.choice([-1, 1], size=num_bits)

# Simular el canal ruidoso (Agregar ruido gaussiano)
snr = 10**(snr_dB / 10)  # Convertir SNR de dB a escala lineal
noise_power = 1 / (snr * 2 * symbol_rate)  # Potencia del ruido
received_signal = nrz_signal + np.random.normal(0, np.sqrt(noise_power), size=num_bits)

# Filtro adaptativo LMS para recuperar la señal NRZ
mu = 0.01  # Tasa de aprendizaje del filtro LMS
filter_length = 11  # Longitud del filtro adaptativo

# Inicializar el filtro con coeficientes aleatorios
filter_coeffs = np.random.randn(filter_length)

# Aplicar el algoritmo LMS
recovered_signal = []
for i in range(num_bits):
    input_signal = received_signal[max(0, i - filter_length + 1):i + 1][::-1]
    output = np.dot(input_signal, filter_coeffs[:len(input_signal)])
    error = nrz_signal[i] - output
    filter_coeffs[:len(input_signal)] += 2 * mu * error * input_signal
    recovered_signal.append(output)

recovered_signal = np.array(recovered_signal)

# Visualizar las señales
plt.figure(figsize=(12, 6))
plt.plot(nrz_signal[:100], label='Señal NRZ Original')
plt.plot(received_signal[:100], label='Señal Recibida con Ruido')
plt.plot(recovered_signal[:100], label='Señal Recuperada')
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.title('Señal NRZ, Señal Recibida y Señal Recuperada')
plt.grid(True)
plt.show()
