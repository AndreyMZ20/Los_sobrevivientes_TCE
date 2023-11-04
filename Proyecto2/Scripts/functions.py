import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as nps
from rcosdesign import rcosdesign
import numpy as np

def encode(bit_string, encoder_type):
    # Convierte el string hexadecimal en un string binario
    bit_string = hex_to_bin(bit_string)

    if encoder_type == 'RZ (Return-to-zero)':
        mapping = {'0': [0, 0], '1': [1, 0]}
        signal = [level for bit in bit_string for level in mapping[bit]]
        return signal, bit_string
    elif encoder_type == 'Manchester':
        mapping = {'0': [-1, 1], '1': [1, -1]}
        signal = [level for bit in bit_string for level in mapping[bit]]
        return signal, bit_string
    else:
        mapping = {'0': -1, '1': 1}
        signal = [mapping[bit] for bit in bit_string]
        return signal, bit_string

def plot_nrz(self, signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación NRZ
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-1.1, 1.1])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(list(bit_string))
    # Mostrar la gráfica
    #plt.show()
    self.current_plot = FigureCanvasKivyAgg(fig)
    self.plot_area.add_widget(self.current_plot)

def plot_rz(self, signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [bit for bit in bit_string for _ in range(2)]
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación RZ
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-0.1, 1.1])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    # Mostrar la gráfica
    #plt.show()
    self.current_plot = FigureCanvasKivyAgg(fig)
    self.plot_area.add_widget(self.current_plot)

def plot_manchester(self, signal, bit_string):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(signal)))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [bit for bit in bit_string for _ in range(2)]
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Dibujar la codificación Manchester
    ax.step(t, signal, where='post')
    # Configurar los límites del eje y
    ax.set_ylim([-1.1, 1.1])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    # Mostrar la gráfica
    #plt.show()
    self.current_plot = FigureCanvasKivyAgg(fig)
    self.plot_area.add_widget(self.current_plot)

def hex_to_bin(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    return bin_string.zfill(4 * len(hex_string))  # Asegura que el string binario tenga una longitud múltiplo de 4

def hex_to_kivy_color(hex_color):
    # Convertir el color hexadecimal a RGB
    rgb_color = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    # Normalizar los valores RGB a la escala de 0 a 1
    kivy_color = [value/255 for value in rgb_color]

    return kivy_color

def rgb_to_rgba(rgb_color):
    return [x / 255.0 for x in rgb_color] + [1]

def cose_alzado_func(roll_off, signal):
    # Parámetros del pulso de coseno alzado
    L = 16
    pt = rcosdesign(roll_off, 6, L, 'normal')
    # Aplicar el pulso de coseno alzado a la señal
    señal_coseno_alzado = np.convolve(signal, pt, mode='same')
    return señal_coseno_alzado

def graficar_rcc(self, signal_rcc): 
    # Crea la figura y los ejes
    fig, ax = plt.subplots()
    # Grafica la señal
    ax.plot(signal_rcc)
    # Configura las etiquetas y el título
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Amplitud')
    ax.set_title('Señal con Pulso de Coseno Alzado')
    # Muestra la cuadrícula
    ax.grid(True)
    # Crea el widget de Kivy con la figura
    self.current_plot = FigureCanvasKivyAgg(fig)
    # Agrega el widget al área de trazado
    self.plot_area.add_widget(self.current_plot)