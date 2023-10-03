import os
import sys
import getopt
import csv
from math import log2

# Parametros de entrada y ayuda:
file_full_path = ""
file_split_path = [];
def myfunc(argv):
    global file_full_path, file_split_path
    arg_help = "{0} -i <input>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hi:", ["help", "input="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  
            sys.exit(2)
        elif opt in ("-i", "--input"):
            file_full_path = arg
            file_split_path = os.path.normpath(file_full_path)
            file_split_path = os.path.split(file_split_path)


if __name__ == "__main__":
    myfunc(sys.argv)


file_huffman_comprimido = file_full_path+".bin"
ruta_diccionario = file_full_path+".diccionario.csv"
recovered_path = os.path.join(file_split_path[0], "recovered_"+file_split_path[1]);
#-----------------------------------------------------
# Algorithmo de compresión de huffman
#-----------------------------------------------------
#Apertura y lectura del archivo
string=[];
with open(file_full_path, "rb") as f:
    while (byte := f.read(1)):
        int_val = int.from_bytes(byte, "big")
        string.append(int_val)

# Árbol binario
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def children(self):
        return (self.left, self.right)
    def nodes(self):
        return (self.left, self.right)
    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def insert_in_tree(raiz, ruta, valor):
    if(len(ruta)==1):
        if(ruta=='0'):
            raiz.left = valor;
        else:
            raiz.right = valor;
    else:
        if(ruta[0]=='0'):
            if(raiz.left==None):
                raiz.left = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.left,ruta,valor);
        else:
            if(raiz.right==None):
                raiz.right = NodeTree(None,None);
            ruta = ruta[1:];
            insert_in_tree(raiz.right,ruta,valor);


# Función principal del algoritmo de Huffman
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

# calculo de frecuencias y probabilidades
prob_unit = 1/len(string)
freq = {}
for c in string:
    if c in freq:
        freq[c] += prob_unit
    else:
        freq[c] = prob_unit

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))
    #print(nodes)
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

if len(freq)==1:
    huffmanCode= {freq[0][0]: '1'}
else:
    huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

#-------------------PARTE1-----------------------

#Calculo de la entropia, longitud media y varianza
entropia = 0
longitud_media = 0
varianza = 0
for (char, frequency) in freq:
    entropia += frequency*log2(1/frequency)
    longitud_media += frequency*len(huffmanCode[char])
    varianza += frequency*(len(huffmanCode[char])**2)
varianza = varianza - (longitud_media**2)

#eficiencia de la fuente
eficiencia_fuente = entropia/8

#eficiencia de la codificacion de huffman
eficiencia_huffman = entropia/longitud_media

#-----------------------------------------------------
print("-----------------------------------------------------"); 

print("Entropía", entropia)   
print("Longitud media", longitud_media)
print("Varianza", varianza)
print("Eficiencia de la fuente", eficiencia_fuente)
print("Eficiencia de la codificación de huffman", eficiencia_huffman)


#-------------------PARTE2-----------------------

#creacion del archivo comprimido
binary_string = []
for c in string :
    binary_string += huffmanCode [ c ]

compressed_length_bit = len( binary_string )

if( compressed_length_bit %8>0):
    for i in range (8 - len( binary_string ) % 8) :
        binary_string += "0"

byte_string ="". join ([ str( i ) for i in binary_string ])

byte_string =[ byte_string [ i : i +8] for i in range (0 , len( byte_string ), 8) ]


byte_array = []
for byte in byte_string:
    byte_array.append(int(byte,2))

#Escribe los datos comprimidos en un archivo binario
with open(file_huffman_comprimido, "wb") as f:
    f.write(bytearray(byte_array))

#-----------------------------------------------------
# Creación del archivo de diccionario
with open(ruta_diccionario, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([str(compressed_length_bit), " bits"])
    for entrada in huffmanCode:
        writer.writerow([str(entrada), huffmanCode[entrada]])

#-----------------------------------------------------
#calculo de la taza de compresion
taza_compresion = os.path.getsize(file_full_path)/compressed_length_bit*8

#descripcion del archivo comprimido
print("-----------------------------------------------------")
print("Archivo comprimido: ", file_huffman_comprimido)
print("Tamaño del archivo original: ", os.path.getsize(file_full_path), "bytes")
print("Tamaño del archivo comprimido: ", compressed_length_bit/8, "bytes")
print("Taza de compresión: ", taza_compresion)
print("-----------------------------------------------------")

#-------------------Descompresion-de-datos----------------------------------

csvfile = open ( ruta_diccionario , 'r')
reader = csv . reader ( csvfile )
bits_a_leer = None ;
diccionario = dict () ;

for row in reader:      #For para leer cada línea de datos
  if (bits_a_leer ==None):
    bits_a_leer = int(row [0]);
  else:
    diccionario.update({ int (row [0]): row[1]})

Decoding = NodeTree (None, None); # Crear objeto arbol para la decodificacion
for entrada in diccionario:  # Insertar al arbol las etiquetas de diccionario
  insert_in_tree (Decoding, diccionario [entrada], entrada)

nodo = Decoding;
data_estimated = [];
for i in range(compressed_length_bit): 
  (l , r ) = nodo . children () ; #Extraer los nodos hijos del nodo actual

  if (binary_string [i]=='1'): #Ir al siguiente nodo según el bit de dato
    nodo = r;
  else:
    nodo = l;
  if type(nodo) is int:
    data_estimated.append(nodo) #Extraer el dato parado en el nodo 

    nodo = Decoding; # Para voler a empezar con el siguiente dato
    
#Escribir los datos descomprimidos en un archivo binario
with open(recovered_path, "wb") as f:
    f.write(bytearray(data_estimated))