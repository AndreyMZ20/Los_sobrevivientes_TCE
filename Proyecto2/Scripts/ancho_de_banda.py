import numpy as np

def ancho_de_banda(digital_mysignal, nyqt = 3):
    num_puntos = nyqt * len(digital_mysignal) 
    fft_resultado = np.fft.fft(digital_mysignal, n=num_puntos)
    # Calcular el ancho de banda
    ancho_banda = np.sum(np.abs(fft_resultado) > 0.1 * np.max(np.abs(fft_resultado)))
    return ancho_banda
