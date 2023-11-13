import matplotlib.pyplot as plt
from random_32bits import generar_cadena_binaria_aleatoria

def nrz_m_ary_encode(bit_string, m):
    # Mapeo de bits a niveles NRZ m-aria
    mapping = {str(i): 2 * i / (m - 1) - 1 for i in range(m)}
    
    # Codificación NRZ m-aria de la cadena de bits
    nrz_encoded = [mapping[bit] for bit in bit_string]
    
    return nrz_encoded

def plot_nrz_m_ary(nrz_encoded, bit_string, m):
    # Crear una lista de tiempos para el eje x
    t = list(range(len(nrz_encoded)))
    
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    
    # Dibujar la codificación NRZ m-aria
    ax.step(t, nrz_encoded, where='post')
    
    # Configurar los límites del eje y
    ax.set_ylim([-1.5, 1.5])
    
    # Configurar las etiquetas del eje x
    ax.set_xticks(t)
    ax.set_xticklabels(list(bit_string))
    
    # Mostrar la gráfica
    plt.title(f"NRZ {m}-aria Encoding")
    plt.show()

def nrz_m_ary_decode(nrz_signal, m):
    mapping = {i: str(i) for i in range(m)}
    
    # Decodificación NRZ m-aria y mapeo a bits
    nrz_decoded = [mapping[round((bit + 1) * (m - 1) / 2)] for bit in nrz_signal]
    
    # Convertir la lista de bits en una cadena y devolverla
    decoded_bits_string = ''.join(nrz_decoded)
    return decoded_bits_string

# Prueba de las funciones
bit_string = generar_cadena_binaria_aleatoria()
m = 4  # Número de niveles en la codificación NRZ m-aria
nrz_encoded = nrz_m_ary_encode(bit_string, m)
decoded_bit_string = nrz_m_ary_decode(nrz_encoded, m)
print(f"Cadena de bits: {bit_string}")
print(f"Codificación NRZ {m}-aria: {nrz_encoded}")
print(f"Decodificación NRZ {m}-aria: {decoded_bit_string}")
plot_nrz_m_ary(nrz_encoded, bit_string, m)
