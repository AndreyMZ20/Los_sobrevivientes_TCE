import matplotlib.pyplot as plt

def generar_cadena_binaria():
    cadena = ''.join(['1' if i % 2 == 0 else '0' for i in range(32)])
    return cadena

print(generar_cadena_binaria())

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

    plt.step(tiempo, señal, where='post')
    plt.xlabel("Tiempo")
    plt.ylabel("Señal")
    plt.title(f"Codificación Manchester de la secuencia binaria '{binario}'")
    plt.grid(True)
    plt.show()

# Generar una cadena binaria usando la función generar_cadena_binaria
cadena_binaria = generar_cadena_binaria()

# Codificar y mostrar la señal Manchester
codificar_manchester(cadena_binaria)