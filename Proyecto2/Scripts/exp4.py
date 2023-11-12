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
            mapping = {'00': [0, 0], '01': [1, 0], '10': [-1, 0], '11': [0, 0]}
            mysignal = []
            last_one = -1
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
        

import matplotlib.pyplot as plt

def plot_signal(signal):
    print(signal)
    plt.figure(figsize=(10, 4))
    plt.plot(signal, drawstyle='steps-pre')
    plt.ylim(-4, 4)
    plt.grid(True)
    plt.show()


bit_string = '0011'
encoder_type = 'PRZ-AMI (Alter Zero Return Polar)'
encoder_type = "Manchester"
type_m = '4-PAM'

signal = encode(bit_string, encoder_type, type_m)
plot_signal(signal)
