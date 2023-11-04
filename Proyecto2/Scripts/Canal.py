import numpy as np
import matplotlib.pyplot as plt
import math

def canal(signal, num_puntos, t, f, random_signal, random_phase, random_amp):
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
            return canal_random(signal,num_puntos,t,f,random_phase,random_amp)
        if(random_signal==False):
            return canal_manual(signal,num_puntos,t,f)
        else:
            return
    else:
        return

def canal_random(signal, num_puntos, t, f, random_phase, random_amp):
    senal_con_eco = np.copy(signal)
    for i in range(len(random_phase)):
        if(random_phase[i]==180):
            eco = ecos(signal,num_puntos,f,-random_amp[i],0)
        else:
            eco = ecos(signal,num_puntos,f,random_amp[i],random_phase[i])
        senal_con_eco += eco
        plt.plot(t,eco, label="Eco "+str(i+1))
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Ecos')
    plt.grid(True)
    plt.legend() 
    return senal_con_eco

def canal_manual(signal,num_puntos,t,f,):
    cantidadEco = int(input("\nCantidad de ecos: "))
    senal_con_eco = np.copy(signal)
    for amp in range(cantidadEco):
        print("\n")
        grados_retraso = float(input("Desfase en grados de eco "+str(amp+1)+": "))
        amplitud = float(input("Amplitud de eco "+str(amp+1)+": "))
        if (grados_retraso == 180):
            eco = ecos(signal,num_puntos,f,-amplitud,0)
        else:
            eco = ecos(signal,num_puntos,f,amplitud,grados_retraso)
        senal_con_eco += eco
        plt.plot(t,eco, label="Eco "+str(amp+1))
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('Ecos')
    plt.grid(True)
    plt.legend() 
    return senal_con_eco

def ecos(signal,num_puntos,f,amplitud,grados_retraso):
    radianes_retraso = math.radians(grados_retraso)
    periodo = 1/f
    atraso = ((radianes_retraso) / (2 * np.pi )) * periodo
    muestras_retraso = int(atraso * num_puntos/2)
    eco = np.roll(signal, int(atraso * muestras_retraso)) * amplitud
    eco[:int(atraso * muestras_retraso)] = 0
    return eco

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

noised_signal= canal(cosine_signal, num_puntos, t, f, False,[90,180],[0.1,1])

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