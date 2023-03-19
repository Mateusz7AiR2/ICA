import Plan_projektu

#Deklaracja i funkcja odpwoiedzialna za wpisywanie zapisywanie informacji w pliku "Historia_analizy.txt"
#Po wykonaniu programu następne jego uruchomienie usuwa zawartość pliku. By historia była zapisywana z poprzednimi wersjami należy zamienić 'w' na 'a'
zapis_do_pliku = open('Historia_analizy.txt', 'w') 
def wpis_do_pliku(text):
    zapis_do_pliku.write(str(text) + str('\n'))
    print(str(text))
#Informacje ogólne
wpis_do_pliku('Projekt: \nAlgorytm neuronowy dla „gradientowej metody ślepej separacji ICA"\nAutor:\nMateusz Jakiel\nNumer albumu: 324186\nWydział Elektryczny, OKNO') 
wpis_do_pliku('Wymagane pliki w celu popranwgo działania:\nPlan_projektu.py\nBlok_obliczeniowy\nModul_metody\n')

#Właściwa cześć projektu
if __name__ == '__main__':
           
    Steruj = Plan_projektu.Wlasciwa_czesc_projektu()
    Steruj.Rozpocznij()
