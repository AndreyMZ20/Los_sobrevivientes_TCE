import matplotlib.pyplot as plt

def rz_encoder(binary_string):
    rz_signal = []

    for bit in binary_string:
        if bit == "0":
            rz_signal.extend([0, 0])
        else:
            rz_signal.extend([1, 0])

    return rz_signal

binary_input = input("Ingresa una secuencia binaria: ")
rz_encoded = rz_encoder(binary_input)

time = [i / 2 for i in range(len(rz_encoded))]

plt.step(time, rz_encoded, where="post")
plt.xlabel("Tiempo")
plt.ylabel("Señal RZ")
plt.title("Señal RZ Codificada")
plt.grid(True)
plt.show()