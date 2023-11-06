import numpy as np
import matplotlib.pyplot as plt
import math

def canal(signal, num_puntos, t, random_signal, random_phase, random_amp):
    entrada = int(input("1.Ruido\n2.Eco\n\nOpcion: "))
    plt.figure(1)
    plt.subplot(3, 1, 1)
    if(entrada == 1):
        amplitud_ruido = float(input("\nNivel de ruido: "))
        ruido = amplitud_ruido * np.random.randn(len(t))
        senal_con_ruido = signal + ruido
        plt.plot(t,ruido)
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
        plt.title('Ruido')
        plt.grid(True)
        return senal_con_ruido
    if(entrada == 2):
        if(random_signal):
            return canal_random(signal,num_puntos,t,random_phase,random_amp)
        if(random_signal==False):
            return canal_manual(signal,num_puntos,t)
        else:
            return
    else:
        return

def canal_random(signal, num_puntos, t, random_phase, random_amp):
    senal_con_eco = np.copy(signal)
    for i in range(len(random_phase)):
        if(random_phase[i]==180):
            eco = ecos(signal,num_puntos,-random_amp[i],0)
        else:
            eco = ecos(signal,num_puntos,random_amp[i],random_phase[i])
        senal_con_eco += eco
        plt.plot(t,eco, label="Eco "+str(i+1))
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Ecos')
    plt.grid(True)
    plt.legend() 
    return senal_con_eco

def canal_manual(signal,num_puntos,t):
    cantidadEco = int(input("\nCantidad de ecos: "))
    senal_con_eco = np.copy(signal)
    for amp in range(cantidadEco):
        print("\n")
        grados_retraso = float(input("Desfase en grados de eco "+str(amp+1)+": "))
        amplitud = float(input("Amplitud de eco "+str(amp+1)+": "))
        if (grados_retraso == 180):
            eco = ecos(signal,num_puntos,-amplitud,0)
        else:
            eco = ecos(signal,num_puntos,amplitud,grados_retraso)
        senal_con_eco += eco
        plt.plot(t,eco, label="Eco "+str(amp+1))
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Ecos')
    plt.grid(True)
    plt.legend() 
    return senal_con_eco

def ecos(signal,num_puntos,amplitud,grados_retraso):
    radianes_retraso = math.radians(grados_retraso)
    atraso = ((radianes_retraso) / (2 * np.pi ))
    muestras_retraso = int(atraso * num_puntos)
    eco = np.roll(signal, muestras_retraso) * amplitud
    eco[:int(atraso * muestras_retraso)] = 0
    return eco

A = 1          # Amplitud
n = 1         # Exponente
f = 1          # Frecuencia en Hz
phi = 0        # Fase
num_puntos = 100
# Tiempo
t = np.linspace(0, 1, num_puntos)  # Generar valores de tiempo de 0 a 2 segundos

# Generar la señal de coseno elevado
cosine_signal = A * np.cos(2 * np.pi * f * t)**n
print("Tamaño: ",len(cosine_signal)/num_puntos)

noised_signal= canal(cosine_signal, num_puntos, t, True,[170,350],[0.5,0.4])

plt.subplot(3, 1, 2)
plt.plot(t,cosine_signal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t,noised_signal)
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal de Coseno Elevado con ruido/eco')
plt.grid(True)
plt.show()