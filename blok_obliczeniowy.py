import numpy as np
import main as mm
#Moduł problemu
class Obliczenia(object):

    def __init__(self):
        self.mixing_matrix = 0
        self.signal_matrix = 0
        self.output_matrix = 0
        self.estimated_signal_matrix = 0
        self.n = 0
    # Definicja funkcji odpowiedzialnej za wygenerowanie macierzy sygnałow na podstawie macierzy miksujacej

    def macierz_sygnalow_z_mix(self, signal_matrix, mixing_matrix=None):
        self.signal_matrix = signal_matrix
        self.n = self.signal_matrix.shape[0]
        if mixing_matrix is None:
            self.mixing_matrix = np.random.uniform(-1/self.n, 1/self.n, (self.n, self.n))
        else:
            self.mixing_matrix = mixing_matrix

        try:
            self.output_matrix = np.matmul(self.mixing_matrix, self.signal_matrix)
        except:
            mm.wpis_do_pliku('Błąd miksowania macierzy! Program kończy działanie!')
            return 1
        return self.output_matrix

    # Definicja funkcji przekształcająca macierz o zerowej wartości średniej na macierz w skali szarości
    @staticmethod
    def zero_mean_to_greyscale(matrix):
        return np.array((matrix + np.ones(matrix.shape))*127.5, dtype=np.uint8)

   
    # Definicja funkcji odpowiedzialna za  przekształcenie tablicy obrazów sygnałów w macierz sygnałów
    def image_container_to_signal_matrix(self, image_container):
        size = image_container[0].shape[0]
        self.signal_matrix = np.zeros((1, size * size))
        for image in image_container:
            self.signal_matrix = np.vstack([self.signal_matrix, np.array([image]).reshape([1, size*size])])
        self.signal_matrix = self.signal_matrix[1:, :]
        return self.signal_matrix
        
    # Definicja funkcji odpowiedzialna za  przekształcenie macierzy w skali szarości na macierz o zerowej warości sredniej
    @staticmethod
    def greyscale_to_zero_mean(matrix):
        return np.array(matrix/127.5 - np.ones(matrix.shape), dtype=np.float64)

    # Definicja funkcji przekształcającej macierz mieszanin w tablice obrazów mieszanin
    @staticmethod
    def output_matrix_to_image_container(output_matrix):
        size = int(np.sqrt(output_matrix[0].shape[0]))
        image_container = []
        for signal in output_matrix:
            image_container.append(signal.reshape((size, size)).astype(np.ubyte))
        return image_container

    # Definicja funkcji obliczającej błąd EI(P)
    def calculate_error(self, W):
        mm.wpis_do_pliku('1. Macierz P = W * A = ')
        P = np.matmul(W, self.mixing_matrix)
        mm.wpis_do_pliku(P)

        Pw = []
        for wiersz in range(len(P)):
            Pw.append(P[wiersz] / max(P[wiersz]))
        Pw = np.array(Pw).reshape((self.n, self.n))
        P_1 = 0
        for wiersz in range(len(Pw)):
            for elem in range(len(Pw[wiersz])):
                P_1 += Pw[wiersz][elem]
        P_1 = (P_1 - self.n) / self.n
        Pc = []
        P = P.transpose()
        for wiersz in range(len(P)):
            Pc.append(P[wiersz] / max(P[wiersz]))
        Pc = np.array(Pc).reshape((self.n, self.n))
        P_2 = 0
        for wiersz in range(len(Pc)):
            for elem in range(len(Pc[wiersz])):
                P_2 += Pc[wiersz][elem]
        P_2 = (P_2 - self.n) / self.n
        mm.wpis_do_pliku('EI(P) = ')
        error = P_1 + P_2
        mm.wpis_do_pliku(error)
        return error
