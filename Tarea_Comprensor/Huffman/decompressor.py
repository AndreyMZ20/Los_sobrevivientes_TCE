# decompressor.py

import os
import csv
import sys
from tree import NodeTree, insert_in_tree

# NOTAS:  para correr este archivo se debe tener el archivo compressor.py en la misma carpeta, y ejecutarlo con el siguiente comando:
#         python3 decompressor.py <nombre_archivo> (No se debe incluir la extensión del archivo)

def decompress_file(file_name):
    # Leer el archivo del diccionario y el archivo comprimido
    ruta_diccionario = file_name + ".txt.diccionario.csv"
    csvfile = open(ruta_diccionario, 'r')
    reader = csv.reader(csvfile)
    bits_a_leer = None
    diccionario = dict()

    for row in reader:      # For para leer cada línea de datos
        if bits_a_leer == None:
            bits_a_leer = int(row[0])
        else:
            diccionario.update({int(row[0]): row[1]})

    # Reconstruir el árbol de Huffman
    Decoding = NodeTree(None, None)  # Crear objeto arbol para la decodificacion
    for entrada in diccionario:  # Insertar al arbol las etiquetas de diccionario
        insert_in_tree(Decoding, diccionario[entrada], entrada)

    # Leer el archivo comprimido y descomprimir los datos
    file_huffman_comprimido = file_name + ".txt.bin"
    with open(file_huffman_comprimido, "rb") as f:
        binary_string = []
        while (byte := f.read(1)):
            binary_string += [bin(int.from_bytes(byte, "big"))[2:].zfill(8)]
        binary_string = "".join(binary_string)[:bits_a_leer]

    nodo = Decoding
    data_estimated = []
    for i in range(bits_a_leer):
        (l, r) = nodo.children()  # Extraer los nodos hijos del nodo actual

        if binary_string[i] == '1':  # Ir al siguiente nodo según el bit de dato
            nodo = r
        else:
            nodo = l
        if type(nodo) is int:
            data_estimated.append(nodo)  # Extraer el dato parado en el nodo 

            nodo = Decoding  # Para voler a empezar con el siguiente dato

    # Escribir los datos descomprimidos en un nuevo archivo con extensión .txt
    recovered_path = file_name + "_recovered.txt"
    with open(recovered_path, "wb") as f:
        f.write(bytearray(data_estimated))

    # Imprimir el nombre del archivo descomprimido, el tamaño del archivo comprimido y recuperado y la tasa de descompresión
    compressed_size = os.path.getsize(file_huffman_comprimido)
    recovered_size = os.path.getsize(recovered_path)
    decompression_rate = compressed_size / recovered_size

    print('____________________________________________________________________')
    print('                           COMPRESIÓN')
    print('--------------------------------------------------------------------')
    print("Archivo descomprimido: ", recovered_path)
    print("Tamaño del archivo comprimido: ", compressed_size, "bytes")
    print("Tamaño del archivo recuperado: ", recovered_size, "bytes")
    print("Tasa de descompresión: ", decompression_rate)
    print('____________________________________________________________________')


if __name__ == "__main__":
    decompress_file(sys.argv[1])
