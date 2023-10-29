import random

def generar_cadena_binaria_aleatoria():
    return ''.join(random.choice('01') for _ in range(32))
