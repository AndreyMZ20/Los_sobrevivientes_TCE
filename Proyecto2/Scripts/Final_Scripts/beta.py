import matplotlib.pyplot as plt
from rcosdesign import rcosdesign
import numpy as np
from reedsolo import RSCodec
import binascii
from scipy.signal import find_peaks

#------------------ CODIFICACION BINARIA ------------------#
def encode(bit_string, encoder_type):
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

def hex_to_bin(hex_string):
    bin_string = bin(int(hex_string, 16))[2:]
    return bin_string.zfill(4 * len(hex_string))  # Asegura que el string binario tenga una longitud múltiplo de 4


def graficar_señales(textbox_value, tipo_cod_simb):

    bit_string = hex_to_bin(textbox_value)
    mysignal = np.array(encode(bit_string, tipo_cod_simb))
    
    roll_off = 0.5

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


textbox_value = "1010"

#tipo_cod_simb = "PRZ-AMI (Alter Zero Return Polar)"
#tipo_cod_simb = "Manchester"

graficar_señales(textbox_value, tipo_cod_simb = "la otra")