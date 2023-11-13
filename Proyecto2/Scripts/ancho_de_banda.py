import numpy as np

def ancho_de_banda(digital_mysignal, nyqt = 3):
    num_puntos = nyqt * len(digital_mysignal) 
    fft_resultado = np.fft.fft(digital_mysignal, n=num_puntos)
    # Calcular el ancho de banda
    ancho_banda = np.sum(np.abs(fft_resultado) > 0.1 * np.max(np.abs(fft_resultado)))
    return ancho_banda

def energia(signal):
    energia = np.sum(np.square(signal))
    return energia

def BER(senal_original, senal_con_ruido):
    bits_erroneos = np.sum(senal_original != senal_con_ruido)
    BER = bits_erroneos / len(senal_original)
    return BER

def snr(original, ruidosa):
    potencia_senal_original = np.sum(original**2) / len(original)
    potencia_senal_ruidosa = np.sum(ruidosa**2) / len(ruidosa)
    potencia_ruido = potencia_senal_ruidosa - potencia_senal_original
    if(potencia_ruido!=0):
        snr = 10 * np.log10(potencia_senal_original / potencia_ruido)
        return snr