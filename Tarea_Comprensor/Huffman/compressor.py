# compressor.py

import os
import csv
import sys
from math import log2
from tree import NodeTree, huffman_code_tree

# NOTAS:  Para correr este archivo se debe tener el archivo compressor.py en la misma carpeta, y ejecutarlo con el siguiente comando:
#         python3 compressor.py <nombre_archivo.txt> (Se debe incluir la extensión del archivo)
#         El archivo comprimido se guardará en la misma carpeta con el nombre <nombre_archivo.txt>.bin
#         El archivo del diccionario se guardará en la misma carpeta con el nombre <nombre_archivo.txt>.diccionario.csv
#         El archivo comprimido se puede descomprimir con el archivo decompressor.py, que se encuentra en la carpeta Huffman
#         Para cargar archivos de otras carpetas, se debe incluir la ruta completa del archivo, por ejemplo:
#         python3 compressor.py /home/user/Documentos/archivo.txt (Se debe incluir la extensión del archivo)

def compress_file(file_full_path):
    # Leer el archivo y calcular las frecuencias de los bytes
    string = []
    with open(file_full_path, "rb") as f:
        while (byte := f.read(1)):
            int_val = int.from_bytes(byte, "big")
            string.append(int_val)

    prob_unit = 1/len(string)
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += prob_unit
        else:
            freq[c] = prob_unit

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Construir el árbol de Huffman y generar los códigos de Huffman
    nodes = freq
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    # Toma en cuenta si la frecuencia es cero
    huffmanCode = huffman_code_tree(nodes[0][0]) if len(freq) > 1 else {freq[0][0]: '1'}

    # Imprimir la tabla de códigos de Huffman
    print('____________________________________________________________________')
    print('                 TABLA DE CÓDIGOS DE HUFFMAN  ')
    print('--------------------------------------------------------------------')
    print(' ASCII | Char | Huffman code ')
    print('--------------------------------------------------------------------')
    for (char, frequency) in freq:
        print(' %-5r | %-4r |%8s' % (char, chr(char), huffmanCode[char]))

    # Calcular la entropía de la fuente y del mensaje codificado
    entropy_source = sum([frequency * log2(1/frequency) for char, frequency in freq])
    entropy_encoded = sum([frequency * len(huffmanCode[char]) for char, frequency in freq])
    
    print('____________________________________________________________________')
    print('                            ENTROPÍA')
    print('--------------------------------------------------------------------')
    print("Entropía de la fuente: ", entropy_source)
    print("Entropía del mensaje codificado: ", entropy_encoded)

    # Calcular la eficiencia de la fuente y la eficiencia de codificación de Huffman
    source_efficiency = entropy_source / 8
    huffman_efficiency = entropy_source / entropy_encoded

    print('____________________________________________________________________')
    print('                           EFICIENCIA')
    print('--------------------------------------------------------------------')
    print("Eficiencia de la fuente: ", source_efficiency)
    print("Eficiencia de codificación de Huffman: ", huffman_efficiency)
    # Escribir el archivo comprimido y el archivo del diccionario
    binary_string = []
    for c in string :
        binary_string += huffmanCode[c]

    compressed_length_bit = len(binary_string)
    if compressed_length_bit % 8 > 0:
        for i in range(8 - len(binary_string) % 8):
            binary_string += "0"

    byte_string = "".join([str(i) for i in binary_string])
    byte_string =[byte_string[i : i + 8] for i in range(0 , len(byte_string), 8)]

    byte_array = []
    for byte in byte_string:
        byte_array.append(int(byte, 2))

    file_huffman_comprimido = file_full_path + ".bin"
    with open(file_huffman_comprimido, "wb") as f:
        f.write(bytearray(byte_array))

    ruta_diccionario = file_full_path + ".diccionario.csv"
    with open(ruta_diccionario, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(compressed_length_bit), " bits"])
        for entrada in huffmanCode:
            writer.writerow([str(entrada), huffmanCode[entrada]])

    # Imprimir el nombre del archivo comprimido, el tamaño del archivo original y del archivo comprimido y la tasa de compresión
    original_size = os.path.getsize(file_full_path)
    compressed_size = os.path.getsize(file_huffman_comprimido)
    compression_rate = original_size / compressed_size
    print('____________________________________________________________________')
    print('                           COMPRESIÓN')
    print('--------------------------------------------------------------------')
    print("Archivo comprimido: ", file_huffman_comprimido)
    print("Tamaño del archivo original: ", original_size, "bytes")
    print("Tamaño del archivo comprimido: ", compressed_size, "bytes")
    print("Tasa de compresión: ", compression_rate)
    print('____________________________________________________________________')
if __name__ == "__main__":
   compress_file(sys.argv[1])
