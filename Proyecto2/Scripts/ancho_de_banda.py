import numpy as np

def ancho_de_banda(senal, muestras_por_segundo):
    fft_resultado = np.fft.fft(senal)
    frecuencias = np.fft.fftfreq(len(fft_resultado), 1/muestras_por_segundo)

    # Encontrar el índice de la frecuencia máxima
    indice_frecuencia_maxima = np.argmax(np.abs(fft_resultado))

    # Calcular el ancho de banda
    ancho_banda = np.sum(np.abs(fft_resultado) > 0.1 * np.max(np.abs(fft_resultado)))
    return ancho_banda
