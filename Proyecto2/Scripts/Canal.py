import numpy as np
import matplotlib.pyplot as plt

def canal(signal, num_puntos, t, fs):
    entrada = int(input("1.Ruido\n2.Eco\n\nOpcion: "))
    if(entrada == 1):
        amplitud_ruido = float(input("\nNivel de ruido: "))
        ruido = amplitud_ruido * np.random.randn(len(t))
        senal_con_ruido = signal + ruido
        return senal_con_ruido
    else:
        cantidadEco = int(input("\nCantidad de ecos: "))
        ecos = []
        atraso = 0
        senal_con_eco = np.copy(signal)
        for amp in range(cantidadEco):
            print("\n")
            grados_retraso = float(input("Desfase en grados de eco "+str(amp+1)+": "))
            radianes_retraso = np.deg2rad(grados_retraso)  # Convierte grados a radianes
            atraso = (radianes_retraso * num_puntos) / (2 * np.pi * fs)
            amplitud = float(input("Amplitud de eco "+str(amp+1)+": "))
            eco = np.roll(signal, int(atraso * fs)) * amplitud
            eco[:int(atraso * fs)] = 0
            ecos.append(eco)
            senal_con_eco += eco
            plt.plot(t,eco, label="Eco "+str(amp+1))
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
fs = 1.0 / (t[1] - t[0]) 
# Generar la señal de coseno elevado
cosine_signal = A * np.cos(2 * np.pi * f * t + phi)**n

noised_signal= canal(cosine_signal, num_puntos, t, fs)

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