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
        cantidadEco = int(input("Cantidad de eco: "))
        ecos = []
        atraso = 0
        senal_con_eco = np.copy(signal)
        for amp in range(cantidadEco):
            atraso += 0.2
            amplitud = float(input("Amplitud de eco: "))
            eco = np.roll(signal, int(atraso * num_puntos)) * amplitud
            eco[:int(atraso * num_puntos)] = 0
            ecos.append(eco)
            senal_con_eco += eco
            plt.plot(t,eco, label="Eco" + str(amp))
            plt.xlabel('Tiempo')
            plt.ylabel('Amplitud')
            plt.title('Señal de Coseno Elevado')
            plt.grid(True)
            plt.legend() 
        plt.show()
        return senal_con_eco

#Para simular una señal de cosenos alzados 

A = 1          # Amplitud
n = 4          # Exponente
f = 1          # Frecuencia en Hz
phi = 0        # Fase
num_puntos = 1000
# Tiempo
t = np.linspace(0, 2, num_puntos)  # Generar valores de tiempo de 0 a 2 segundos

# Generar la señal de coseno elevado
cosine_signal = A * np.cos(2 * np.pi * f * t + phi)**n

noised_signal= canal(cosine_signal, num_puntos, t)

plt.subplot(2, 1, 1)
plt.plot(t,cosine_signal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t,noised_signal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado con ruido/eco')
plt.grid(True)
plt.show()