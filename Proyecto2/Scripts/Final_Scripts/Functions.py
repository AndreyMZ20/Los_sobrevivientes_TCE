import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from rcosdesign import rcosdesign
import numpy as np
from reedsolo import RSCodec
import binascii
from scipy.signal import find_peaks

from scipy import signal

#------------------ TRANSFORMAR COLOR ------------------#
def hex_to_kivy_color(hex_color):
    # Convertir el color hexadecimal a RGB
    rgb_color = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    # Normalizar los valores RGB a la escala de 0 a 1
    kivy_color = [value/255 for value in rgb_color]

    return kivy_color

#------------------ CONVERTIDORES ------------------#
def complete_byte(textbox_value):
    if len(textbox_value) % 2 != 0:
        textbox_value = '0' + textbox_value
    return textbox_value

def hex_to_bin(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    return bin_string.zfill(4 * len(hex_string))  # Asegura que el string binario tenga una longitud múltiplo de 4

def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)

def bytes_to_hex(bytes_string):
    return bytes_string.hex()

def bytes_to_string(bytes_string):
    return bytes_string.decode('utf-8')

#------------------ GRAFICAR BITS, TIEMPO Y FRECUENCIA DE UNA SEÑAL CUADRADA ------------------#
#graficar señal cuadrada representacion de bits
def graficar_bin(bin_string, title, msj_original=None): 
    # Convertir el string binario en una lista de números
    bin_list = [int(bit) for bit in bin_string]
    # Crear una lista de tiempos para el eje x
    t = list(range(len(bin_list)))
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar entrada
    ax.step(t, bin_list, where='post', linewidth=3)  
    # Configurar los límites del eje y
    ax.set_ylim([-0.1, 1.1])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(bin_string)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # Configurar los títulos de los ejes
    ax.set_xlabel("Posición del bit", fontsize=16)
    ax.set_ylabel("Valor del bit", fontsize=16)
    ax.set_title(title, fontsize=20)
    # Añadir etiqueta después de msj_original
    if msj_original:
        idx = bin_string.find(msj_original)
        if idx >= 0:
            ax.axvline(x=idx + len(msj_original), color='red', linestyle='--', linewidth=2)
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    
    return plot_widget

# generar señal cuadrada con frecuencia de reloj
def generar_senal(data, frecuencia_reloj = 100):
    # Generar el reloj
    #clock = np.array([0, 1] * int(len(data) // frecuencia_reloj))

    # Crear la señal digital
    digital_mysignal = np.zeros((int(data.size * frecuencia_reloj),))
    for i in range(data.size):
        digital_mysignal[i*int(frecuencia_reloj):(i+1)*int(frecuencia_reloj)] = data[i]

    return digital_mysignal

# graficar señal cuadrada en el tiempo
def graficar_tiempo(digital_mysignal, title):
    # Crear el tiempo
    time = np.linspace(0, 1, len(digital_mysignal), endpoint=False)

    fig, ax = plt.subplots()
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar entrada
    ax.plot(time, digital_mysignal, drawstyle='steps-pre', linewidth=3)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xlabel('Tiempo (s)', fontsize=16)
    ax.set_ylabel('Amplitud', fontsize=16)
    ax.set_title(title, fontsize=20)
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

# graficar señal cuadrada en la frecuencia
def graficar_frecuencia(digital_mysignal, title, nyqt = 3):
    # Calcular la Transformada de Fourier con más puntos
    num_puntos = nyqt * len(digital_mysignal) 
    transformada = np.fft.fft(digital_mysignal, n=num_puntos)
    transformada_shift = np.fft.fftshift(transformada)  # Centrar la Transformada de Fourier
    frecuencias = np.fft.fftfreq(num_puntos)
    frecuencias_shift = np.fft.fftshift(frecuencias)  # Centrar las frecuencias

    # Graficar el espectro de frecuencia
    fig, ax = plt.subplots()
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar entrada
    ax.plot(frecuencias_shift, np.abs(transformada_shift))
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xlabel('Frecuencia (Hz)', fontsize=16)
    ax.set_ylabel('Amplitud', fontsize=16)
    ax.set_title(title, fontsize=20)
    ax.set_xlim([-0.2, 0.2])
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

#------------------ CORRECION DE ERRORES: REED-SALOMON ------------------#
def label_div_red(bit_reedsolo, bit_string):
   # Verifica si bit_string es un subconjunto de bit_reedsolo
    if bit_string in bit_reedsolo:
        # Encuentra la posición de la última ocurrencia de bit_string en bit_reedsolo
        last_position = bit_reedsolo.rfind(bit_string)
        
        # Inserta un "/" justo después de la última ocurrencia de bit_string
        result = bit_reedsolo[:last_position + len(bit_string)] + '/' + bit_reedsolo[last_position + len(bit_string):]
        
        # Divide el resultado en dos partes: antes del '/' y después del '/'
        before_slash, after_slash = result.split('/')
        
        # Agrega un guion bajo (_) cada 4 caracteres en ambas partes
        before_slash_with_underscore = '_'.join([before_slash[i:i+4] for i in range(0, len(before_slash), 4)])
        after_slash_with_underscore = '_'.join([after_slash[i:i+4] for i in range(0, len(after_slash), 4)])
        
        # Une ambas partes nuevamente con '/' y devuelve el resultado
        result_with_underscore = before_slash_with_underscore + '/' + after_slash_with_underscore
        
        return result
    else:
        # Si bit_string no se encuentra en bit_reedsolo, simplemente devuelve bit_reedsolo sin cambios
        return bit_reedsolo

def encode_with_reedsolo(hex_string):
    rs = RSCodec(5)
    bytes_string = hex_to_bytes(hex_string)
    encoded_bytes = rs.encode(bytes_string)
    return bytes_to_hex(encoded_bytes)

def decode_with_reedsolo(hex_string):
    rs = RSCodec(5)
    bytes_string = hex_to_bytes(hex_string)
    decoded_bytes, _ = rs.decode(bytes_string)[:2]  # Tomar sólo los dos primeros elementos de la tupla
    return bytes_to_hex(decoded_bytes)

#------------------ CODIFICACION BINARIA ------------------#
def encode(bit_string, encoder_type, type_m):

    if type_m == '2-PAM':
        if encoder_type == 'PRZ-AMI (Alter Zero Return Polar)':
            mapping = {'0': [0, 0]}
            mysignal = []
            last_one = -1  # Cambiado para comenzar con 1
            for bit in bit_string:
                if bit == '1':
                    last_one *= -1
                    mapping['1'] = [last_one, 0]
                mysignal.extend(mapping[bit])
            return mysignal
        elif encoder_type == 'Manchester':
            mapping = {'0': [-1, 1], '1': [1, -1]}
            mysignal = [level for bit in bit_string for level in mapping[bit]]
            return mysignal
        else:
            mapping = {'0': -1, '1': 1}
            mysignal = [mapping[bit] for bit in bit_string]
            return mysignal
    else:
        if encoder_type == 'PRZ-AMI (Alter Zero Return Polar)':
            mapping = {'00': [-3, 0], '01': [-1, 0], '10': [1, 0]}
            mysignal = []
            last_one = -3
            for i in range(0, len(bit_string), 2):
                bits = bit_string[i:i+2]
                if bits == '11':
                    last_one *= -1
                    mapping['11'] = [last_one, 0]
                mysignal.extend(mapping[bits])
            return mysignal
        elif encoder_type == 'Manchester':
            mapping = {'00': [-1, 1, -1, 1], '01': [-1, 1, 1, -1], '10': [1, -1, -1, 1], '11': [1, -1, 1, -1]}
            mysignal = [level for i in range(0, len(bit_string), 2) for level in mapping[bit_string[i:i+2]]]
            return mysignal
        else:  # PNRZ
            mapping = {'00': -3, '01': -1, '10': 1, '11': 3}
            mysignal = [mapping[bit_string[i:i+2]] for i in range(0, len(bit_string), 2)]
            return mysignal


def plot_encod(mysignal, bit_string, msj_original, encoder_type, type_m):
    if encoder_type == 'PRZ-AMI (Alter Zero Return Polar)':
        return plot_prz_ami(mysignal, bit_string, msj_original, type_m)
    elif encoder_type == 'Manchester':
        return plot_manchester(mysignal, bit_string, msj_original, type_m)
    else:
        return plot_pnrz(mysignal, bit_string, msj_original, type_m)

def plot_pnrz(mysignal, bit_string, msj_original, type_m):
    # Crear una lista de tiempos para el eje x
    t = list(range(1, len(mysignal) + 1))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [''] * len(mysignal)
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    if type_m == '2-PAM':
        # Configurar los límites del eje y
        ax.set_ylim([-1.1, 1.1])  # Adecuado para la codificación PNRZ 2-PAM
        for i in range(0, len(bit_string)):
            if bit_string[i] == '0':
                x_labels[i] = '0'
            elif bit_string[i] == '1':
                x_labels[i] = '1'
    else:  # 4-PAM
        # Configurar los límites del eje y
        ax.set_ylim([-3.1, 3.1])  # Adecuado para la codificación PNRZ 4-PAM
        for i in range(0, len(bit_string), 2):
            x_labels[i//2] = bit_string[i:i+2]

    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar la codificación PNRZ
    ax.step(t, mysignal, where='post', linewidth=3)  
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # Configurar los títulos de los ejes
    ax.set_xlabel("Bit position", fontsize=16) 
    ax.set_ylabel("Bit value", fontsize=16)
    ax.set_title("PNRZ encoding in bits", fontsize=20)
    for i in range(len(x_labels)):
        if type_m == '2-PAM':
            if i == len(msj_original):  # Marcar el inicio de los bits de Reed-Solomon
                ax.axvline(x=i+1, color='red', linestyle='--')
        else:
            if i == len(msj_original) // 2:
                ax.axvline(x=i+1, color='red', linestyle='--')
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

def plot_prz_ami(mysignal, bit_string, msj_original, type_m):
    # Crear una lista de tiempos para el eje x
    t = list(range(1, len(mysignal) + 1))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [''] * len(mysignal)
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    if type_m == '2-PAM':
        # Configurar los límites del eje y
        ax.set_ylim([-1.1, 1.1])  # Adecuado para la codificación PRZ-AMI 2-PAM
        for i in range(0, len(bit_string)):
            if bit_string[i] == '0':
                x_labels[2*i+1] = '0'
            elif bit_string[i] == '1':
                x_labels[2*i+1] = '1'
    else:  # 4-PAM
            # Configurar los límites del eje y
        ax.set_ylim([-3.1, 3.1])  # Adecuado para la codificación PRZ-AMI 4-PAM
        for i in range(0, len(bit_string), 2):
            x_labels[i+1] = bit_string[i:i+2]
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar la codificación PRZ 'AMI'
    ax.step(t, mysignal, where='post', linewidth=3)  
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # Configurar los títulos de los ejes
    ax.set_xlabel("Bit position", fontsize=16) 
    ax.set_ylabel("Bit value", fontsize=16)
    ax.set_title("PRZ-AMI encoding in bits", fontsize=20)
    # Dibujar líneas adicionales en las posiciones donde las etiquetas del eje x están en blanco
    for i in range(len(x_labels)):
        if type_m == '2-PAM':
            if i == len(msj_original) * 2:  # Marcar el inicio de los bits de Reed-Solomon
                ax.axvline(x=i+1, color='red', linestyle='--')
            elif x_labels[i] == '':
                ax.axvline(x=i+1, color='grey', linestyle='--')
        else:
            if i == len(msj_original):  # Marcar el inicio de los bits de Reed-Solomon
                ax.axvline(x=i+1, color='red', linestyle='--')
            elif x_labels[i] == '':
                ax.axvline(x=i+1, color='grey', linestyle='--')
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

def plot_manchester(mysignal, bit_string, msj_original, type_m):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(mysignal)))
    # Duplicar cada bit en las etiquetas del eje x
    x_labels = [''] * len(mysignal)
    for i in range(0, len(bit_string)):
        if bit_string[i] == '0':
            x_labels[2*i+1] = '0'
        elif bit_string[i] == '1':
            x_labels[2*i+1] = '1'
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar la codificación Manchester
    ax.step(t, mysignal, where='post', linewidth=3)  
    # Configurar los límites del eje y
    ax.set_ylim([-1.1, 1.1])
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(x_labels)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # Configurar los títulos de los ejes
    ax.set_xlabel("Bit position", fontsize=16) 
    ax.set_ylabel("Bit value", fontsize=16)
    # Dibujar líneas adicionales en las posiciones donde las etiquetas del eje x están en blanco
    if type_m == '2-PAM':
        for i in range(len(x_labels)):
            if i == len(msj_original) * 2:  # Marcar el inicio de los bits de Reed-Solomon
                ax.axvline(x=i, color='red', linestyle='--')
            elif x_labels[i] == '':
                ax.axvline(x=i, color='grey', linestyle='--')
    else:
        for i in range(len(x_labels)):
            if i == len(msj_original) * 2:  # Marcar el inicio de los bits de Reed-Solomon
                ax.axvline(x=i, color='red', linestyle='--')
            elif x_labels[i] == '' and i % 4 == 0:  # Agregar condición para dibujar solo en índices pares
                ax.axvline(x=i, color='grey', linestyle='--')
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

#------------------ RAIZ DE COSENOS ALZADOS ------------------#
def cose_alzado_func(roll_off, mysignal):
    # Parámetros del pulso de coseno alzado
    L = 16
    pt = rcosdesign(roll_off, 6, L, 'normal')

    # Inicializar una lista vacía para almacenar la señal transmitida
    señal_transmitida = []
    
    # Transmitir cada bit como un pulso de coseno alzado separado
    for bit in mysignal:
        pulso = bit * pt  # Modula el pulso de coseno alzado con el bit
        señal_transmitida.extend(pulso)
    
    return np.array(señal_transmitida)


def graficar_rcc_time(rcc_mysignal, title): 
    # Crear el tiempo
    time = np.linspace(0, 1, len(rcc_mysignal), endpoint=False)
    fig, ax = plt.subplots()
    # Ajustar los espacios alrededor de la gráfica
    plt.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
    # Dibujar entrada
    ax.plot(time, rcc_mysignal, linewidth=3)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xlabel('Tiempo (s)', fontsize=16)
    ax.set_ylabel('Amplitud', fontsize=16)
    ax.set_title(title, fontsize=20)
    # Create the Kivy FigureCanvasKivyAgg widget
    plot_widget = FigureCanvasKivyAgg(fig)
    plot_widget.size_hint_y = 1.0
    return plot_widget

#------------------ FILTRO ADAPTADO ------------------#

def filtro_adaptado_func(roll_off, mysignal):
    # Parámetros del pulso de coseno alzado
    L = 16
    pt = rcosdesign(roll_off, 6, L, 'normal')
    # Crear el filtro adaptado invirtiendo el pulso de coseno alzado en el tiempo
    filtro_adaptado = pt[::-1]
    # Aplicar el filtro adaptado a la señal
    señal_filtro_adaptado = np.convolve(mysignal, filtro_adaptado, mode='same')
    return señal_filtro_adaptado

import matplotlib.pyplot as plt

class ClockRecovery:
    def __init__(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.sample_time = 0
        self.clock_phase = 0
        self.clock_phase_inc = 2 * np.pi / samples_per_symbol
        self.clock_phase_offset = 0

    def recover(self, input_mysignal):
        output_mysignal = []
        for sample in input_mysignal:
            self.sample_time += 1
            if self.sample_time >= self.samples_per_symbol:
                self.sample_time -= self.samples_per_symbol
                output_mysignal.append(sample)
            self.clock_phase += self.clock_phase_inc + self.clock_phase_offset
            self.clock_phase_offset = 0
            if self.clock_phase >= 2 * np.pi:
                self.clock_phase -= 2 * np.pi
                self.clock_phase_offset = -self.clock_phase_inc
        return np.array(output_mysignal)




def graficar_señales(roll_off, mysignal):
    # Parámetros del pulso de coseno alzado
    L = 16
    pt = rcosdesign(roll_off, 6, L, 'normal')

    # Inicializar una lista vacía para almacenar la señal transmitida
    señal_transmitida = []
    
    # Transmitir cada bit como un pulso de coseno alzado separado
    for bit in mysignal:
        pulso = bit * pt  # Modula el pulso de coseno alzado con el bit
        señal_transmitida.extend(pulso)
    
        # Filtrar la señal recibida con el pulso de coseno alzado
    senal_filtrada = np.convolve(señal_transmitida, pt, mode='same')
    


    muestras_por_simbolo = len(pt)
    senal_muestreada = senal_filtrada[::L]


    # Define el umbral
    umbral = 0.65

    # Inicializa una lista vacía para almacenar los bits
    bits = []

    # Inicializa una variable para almacenar el estado anterior
    estado_anterior = 0

    # # Recorre cada valor en la señal muestreada
    # for valor in senal_muestreada:
    #     # Si el valor es mayor que el umbral, es un 1
    #     if valor > umbral:
    #         if estado_anterior != 1:
    #             bits.append(1)
    #         estado_anterior = 1
    #     # Si el valor es menor que el umbral negativo, es un -1
    #     elif valor < -umbral:
    #         if estado_anterior != -1:
    #             bits.append(-1)
    #         estado_anterior = -1
    #     # Si el valor está entre los umbrales, es un 0
    #     else:
    #         estado_anterior = 0













    #FUNCIONA
    # Define el umbral
    umbral = 0.6

    # Inicializa una lista vacía para almacenar los bits
    bits = []

    # Recorre cada valor en la señal filtrada
    for valor in senal_filtrada:
        # Si el valor es mayor que el umbral, es un 1
        if valor > umbral:
            if estado_anterior != 1:
                bits.append(1)
            estado_anterior = 1
        # Si el valor es menor que el umbral negativo, es un -1
        elif valor < -umbral:
            if estado_anterior != -1:
                bits.append(-1)
            estado_anterior = -1
        # Si el valor está entre los umbrales, es un 0
        else:
            estado_anterior = 0


    # Crear la figura y los ejes
    fig, axs = plt.subplots(5)
    
    # Graficar la señal original
    axs[0].plot(mysignal)
    axs[0].set_title('Señal Original')
    
    # Graficar la señal después de aplicar el filtro de coseno elevado
    axs[1].plot(señal_transmitida)
    axs[1].set_title('Señal con Filtro de Coseno Elevado')

    # Graficar la señal después de aplicar el filtro de coseno elevado
    axs[2].plot(senal_filtrada)
    axs[2].set_title('Señal con Filtro adaptado')

    # Graficar la señal después de aplicar el filtro de coseno elevado
    axs[3].stem(senal_muestreada)
    axs[3].set_title('Señal muestreada')

    # Graficar la señal después de aplicar el filtro adaptado
    axs[4].plot(bits)
    axs[4].set_title('Señal recuperada')

    # # Graficar la señal después de aplicar el filtro adaptado
    # axs[4].plot(bits_decididos)
    # axs[4].set_title('Señal recuperada trama')

    print("RATATATATA bits originales", mysignal)
    print("RATATATATA bits recuperados", bits)
    # Mostrar la figura
    plt.show()

