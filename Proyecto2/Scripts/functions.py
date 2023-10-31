import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

def encode(bit_string, encoder_type):
    # Convierte el string hexadecimal en un string binario
    bit_string = hex_to_bin(bit_string)

    if encoder_type == 'RZ (Return-to-zero)':
        mapping = {'0': [0, 0], '1': [1, 0]}
        signal = [level for bit in bit_string for level in mapping[bit]]
        print("RATATATATATATTAATAAAAAAAAAAAAAAAAAA")
        plot_rz(signal, bit_string)
        return signal, bit_string
    elif encoder_type == 'Manchester':
        mapping = {'0': [-1, 1], '1': [1, -1]}
        signal = [level for bit in bit_string for level in mapping[bit]]
        plot_manchester(signal, bit_string)
        return signal, bit_string
    else:
        mapping = {'0': -1, '1': 1}
        signal = [mapping[bit] for bit in bit_string]
        plot_nrz(signal, bit_string)
        return signal, bit_string

def plot_nrz(signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación NRZ
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-2, 2])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(list(bit_string))
    # Mostrar la gráfica
    plt.show()

def plot_rz(signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [bit for bit in bit_string for _ in range(2)]
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación RZ
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-2, 2])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    # Mostrar la gráfica
    plt.show()

def plot_manchester(signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [bit for bit in bit_string for _ in range(2)]
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación Manchester
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-2, 2])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    # Mostrar la gráfica
    plt.show()

def hex_to_bin(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    return bin_string.zfill(4 * len(hex_string))  # Asegura que el string binario tenga una longitud múltiplo de 4

def hex_to_kivy_color(hex_color):
    # Convertir el color hexadecimal a RGB
    rgb_color = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    # Normalizar los valores RGB a la escala de 0 a 1
    kivy_color = [value/255 for value in rgb_color]

    return kivy_color

