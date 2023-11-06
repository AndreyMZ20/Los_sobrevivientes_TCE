from reedsolo import RSCodec
import binascii

def hex_to_bytes(hex_string):
    return bytes.fromhex(hex_string)

def bytes_to_hex(bytes_string):
    return bytes_string.hex()

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

def bytes_to_string(bytes_string):
    return bytes_string.decode('utf-8')

# Ejemplo de uso
hex_string = '68656c6c6f20776f726c64'  # 'hello world' en hexadecimal
encoded = encode_with_reedsolo(hex_string)



# Decodifica la cadena con error
decoded = decode_with_reedsolo(encoded)

# Convierte los bytes decodificados a una cadena de texto
decoded_string = bytes_to_string(hex_to_bytes(decoded))

print(f'Original: {hex_string}')
print(f'Codificado: {encoded}')
print(f'Decodificado: {decoded}')
print(f'Cadena de texto decodificada: {decoded_string}')