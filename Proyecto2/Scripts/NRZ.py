import matplotlib.pyplot as plt
from random_32bits import generar_cadena_binaria_aleatoria

def nrz_encode(bit_string):
    # Mapeo de bits a niveles NRZ
    mapping = {'0': -1, '1': 1}
    
    # Codificación NRZ de la cadena de bits
    nrz_encoded = [mapping[bit] for bit in bit_string]
    
    return nrz_encoded

def plot_nrz(nrz_encoded, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(nrz_encoded)))
    
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    
    # Dibujar la codificación NRZ
    ax.step(t, nrz_encoded, where='post')
    
    # Configurar los límites del eje y
    ax.set_ylim([-1.5, 1.5])
    
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(list(bit_string))
    
    # Mostrar la gráfica
    plt.show()

# Prueba de las funciones
bit_string = generar_cadena_binaria_aleatoria()
#bit_string = "11110"
nrz_encoded = nrz_encode(bit_string)
print(f"Cadena de bits: {bit_string}")
print(f"Codificación NRZ: {nrz_encoded}")
plot_nrz(nrz_encoded, bit_string)
