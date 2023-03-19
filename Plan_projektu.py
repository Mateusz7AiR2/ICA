import blok_obliczeniowy
import Modul_metody 
import cv2
import numpy as np
import main as mm

#Głowna funkcja sterująca programem. Odpowiada za chronologiczny przebieg dzaiałania programu. Zawarte w niej 
# moduły odpowiedzialne są za: wczytywanie ilości obrazów z terminala; wczytywanie ścieżki do dowolnego obrazu;
# wczytywanie parametrów analizowanych zdjęć;
# wywołanie okien przedstawiająych efekty pracy algorytmu oraz wypisanie parametrów macierzy
class Wlasciwa_czesc_projektu(object):

    def __init__(self):
        self.tablia_obrazu = []
        self.obliczanie_macierzy = blok_obliczeniowy.Obliczenia()
        self.ica = None
        self.rozmiar_obrazu = 128
        
    # Deginicja funkcji odpowiadającej za wczytanie obrazu z ścieżki podanej przeż  użytkownika ze ścieżki path
    def zaladuj_obraz(self, path):
        zdjecie = cv2.imread(path, 0)
        self.tablia_obrazu.append(cv2.resize(zdjecie, (self.rozmiar_obrazu, self.rozmiar_obrazu), interpolation=cv2.INTER_AREA))

    # Definicja funkcji odpowiadającej za chronologiczne podawanie danych przez użytkownika w celu poprawnego dzialania algorytmu
    def Rozpocznij(self):
  
        licznik_zdjec = int(input('Podaj ilość zdjęć do analizy.Uwaga podaj minimum 2 zdjęcia:'))
        mm.wpis_do_pliku('Zostały wybrane ' + str(licznik_zdjec) + ' zdjęcia.')

        #Sprawdzenie poprawności wartości wpisanej przez użytkownika
        if licznik_zdjec <= 1:
            mm.wpis_do_pliku('Wprowadzona została niepoprawna liczba zdjęć.')
            return 1

        #Zadawanie ścieżki do analizowanych zdjęć
        for zdjecie in range(0, licznik_zdjec):
            path = input('Podaj ścieżke obrazu nr. {}:' .format(zdjecie))
            mm.wpis_do_pliku ('Załadowany został obraz z ścieżki '+ str(path))
            try:
                self.zaladuj_obraz(path)
            except cv2.error:
                mm.wpis_do_pliku('Niepoprawna ścieżka bądź inny błąd')
                return 1
        self.obliczanie_macierzy.image_container_to_signal_matrix(self.tablia_obrazu)
        self.obliczanie_macierzy.output_matrix = self.obliczanie_macierzy.macierz_sygnalow_z_mix(self.obliczanie_macierzy.greyscale_to_zero_mean(
            self.obliczanie_macierzy.signal_matrix))
        mm.wpis_do_pliku('Macierz mieszająca A: ')
        mm.wpis_do_pliku(self.obliczanie_macierzy.mixing_matrix)



        #Zadawamoe parametrów uczenia się
        iteracions = int(input('Podaj ilość epok uczenia sieci ICA: '))
        mm.wpis_do_pliku('Wybrałeś %d epok' % iteracions)
        lern_rate = float(input('Podaj krok uczenia sieci ICA: '))
        mm.wpis_do_pliku('Wybrany krok uczenia sieci ICA: %f' % lern_rate)
        self.ica = Modul_metody.ICA(self.obliczanie_macierzy.output_matrix, lern_rate)
        self.obliczanie_macierzy.estimated_signal_matrix = self.ica.metoda_BSS(iteracions)
        mm.wpis_do_pliku('Macierz W^(-1)')
        mm.wpis_do_pliku(np.linalg.inv(self.ica.W))
        mm.wpis_do_pliku('Macierz W')
        mm.wpis_do_pliku(self.ica.W)
       
        self.obliczanie_macierzy.calculate_error(self.ica.W)

        est_images = []
        for image_nb in range(licznik_zdjec):
            est_images.append(self.obliczanie_macierzy.zero_mean_to_greyscale(self.obliczanie_macierzy.estimated_signal_matrix[image_nb, :].
                                                                  reshape((self.rozmiar_obrazu, self.rozmiar_obrazu))))
        
        #Wyświetlanie efektów programu
        
        for licznik, zdjecie in enumerate(self.tablia_obrazu):
            cv2.imshow('Obraz nr.' + str(licznik), zdjecie)
            print('Zdjecie wczytane numer : %d' % licznik)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

        
        for licznik, zdjecie in enumerate(self.obliczanie_macierzy.output_matrix_to_image_container(
                self.obliczanie_macierzy.zero_mean_to_greyscale(self.obliczanie_macierzy.output_matrix))):
            cv2.imshow('Mieszanina obrazów nr.' + str(licznik), zdjecie)
            print('Zdjęcie mieszanin obrazu numer %d ' % licznik)
            cv2.waitKey(0)
        cv2.destroyAllWindows()


        for licznik, zdjecie in enumerate(est_images):
            cv2.imshow('Rekonstrukcja obrazu nr.' + str(licznik), zdjecie)
            print('Zdjęcie numer %d po wykonaniu algorytmu' % licznik)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
  