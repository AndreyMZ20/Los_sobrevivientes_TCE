import numpy as np
import matplotlib.pyplot as plt

def canal(signal, num_puntos, t):
    entrada = int(input("1. Ruido\n2.Eco\n"))
    if(entrada == 1):
        amplitud_ruido = float(input("Nivel de ruido: "))
        ruido = amplitud_ruido * np.random.randn(len(t))
        senal_con_ruido = signal + ruido
        return senal_con_ruido
    else:
        eco = signal
        cantidadEco = int(input("Cantidad de eco: "))
        senal_resultante = np.zeros(num_puntos)
        retraso = 0
        for amp in range(cantidadEco):
            retraso = 0.2+retraso
            print("Retraso: ", retraso)
            amplitudEco = float(input("Amplitud de eco: "))
            eco = np.roll(signal, int(retraso * num_puntos)) * amplitudEco + signal
            senal_con_eco = cosine_signal + eco
            senal_resultante += senal_con_eco
        return senal_resultante

amplitud = 1.0  # Amplitud del coseno elevado
periodo = 100  # Período de la señal
alfa = 0.5     # Factor de forma del coseno elevado

# Número de puntos en la señal
num_puntos = 1000

# Crear un vector de tiempo
t = np.linspace(0, 1, num_puntos)

# Generar la señal de coseno elevado
cosine_signal = amplitud * np.cos(2 * np.pi / periodo * t) * np.sinc(alfa * (t - 0.5 * periodo))



noisedSignal = canal(cosine_signal, num_puntos, t)

print("Original: ",cosine_signal)
print("Con ruido: ",noisedSignal)


plt.subplot(1, 2, 1)
plt.plot(t, cosine_signal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t, noisedSignal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado con Ruido')
plt.grid(True)
plt.show()

