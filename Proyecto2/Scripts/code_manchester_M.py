import matplotlib.pyplot as plt
import random

def generar_cadena_binaria(M):
    cadena = ''.join(['1' if i % 2 == 0 else '0' for i in range(M)])
    return cadena

def codificar_y_mostrar_manchester(M):
    # Generar una cadena binaria usando la función generar_cadena_binaria
    cadena_binaria = generar_cadena_binaria(M)

    tiempo = []
    señal = []

    for bit in cadena_binaria:
        if bit == "1":
            tiempo.extend([0, 0.5, 0.5, 1])
            señal.extend([1, 1, -1, -1])
        else:
            tiempo.extend([0, 0.5, 0.5, 1])
            señal.extend([-1, -1, 1, 1])

    tiempo = [t for t in range(len(tiempo))]

    plt.step(tiempo, señal, where='post')
    plt.xlabel("Tiempo")
    plt.ylabel("Señal")
    plt.title(f"Codificación Manchester de la secuencia binaria '{cadena_binaria}'")
    plt.grid(True)
    plt.show()

# Cambiar el valor de M para ajustar la cantidad de bits
M = 32  # Puedes cambiar a 4, 8, 16, 32, etc.

# Llamar a la función con el valor de M deseado
codificar_y_mostrar_manchester(M)