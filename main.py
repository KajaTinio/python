import math


class Wezel:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.kosztPrzejscia = 0
        self.kosztHeurystyczny = 0
        self.calkowityKoszt = 0
        self.nodeRodzic = None


    def oblicz_heurystyke(self, celX, celY):
        self.kosztHeurystyczny = math.sqrt((self.posX - celX)**2 + (self.posY - celY)**2) # (odległość euklidesową)
        self.zaktualizuj_koszt()


    def zaktualizuj_koszt(self):
        self.calkowityKoszt = self.kosztPrzejscia + self.kosztHeurystyczny # Aktualizacja całkowitego kosztu węzła



def jest_dostepny(x, y, maxSzer, maxWys, mapa):
    return 0 <= x < maxSzer and 0 <= y < maxWys and mapa[y][x] != 5



def znajdz_sasiadow(aktualny, maxSzer, maxWys, mapa):
    dostepne_pola = []
    ruchy = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in ruchy:
        nowyX = aktualny.posX + dx
        nowyY = aktualny.posY + dy

        # Jeśli węzeł jest dostępny, tworzy nowy obiekt węzła i dodaje go do listy sąsiadów
        if jest_dostepny(nowyX, nowyY, maxSzer, maxWys, mapa):
            nowy_wezel = Wezel(nowyX, nowyY)
            nowy_wezel.nodeRodzic = aktualny
            dostepne_pola.append(nowy_wezel)

    return dostepne_pola



def znajdz_minimalny_koszt(lista):
    najmniejszy = lista[0]
    for wezel in lista:
        if wezel.calkowityKoszt <= najmniejszy.calkowityKoszt:  # Szuka mniejszego kosztu
            najmniejszy = wezel

    return najmniejszy



def wykonaj_a_gwiazdka(poczatekX, poczatekY, celX, celY, maxSzer, maxWys, mapa):
    otwarta_lista = []
    zamknieta_lista = []


    start = Wezel(poczatekX, poczatekY)
    start.oblicz_heurystyke(celX, celY)
    otwarta_lista.append(start)


    while otwarta_lista:
        obecny = znajdz_minimalny_koszt(otwarta_lista)
        otwarta_lista.remove(obecny)


        if obecny.posX == celX and obecny.posY == celY:
            return obecny

        zamknieta_lista.append(obecny)  # Dodaje obecny węzeł do zamkniętej listy

        # Pobiera dostępnych sąsiadów obecnego węzła
        sasiedzi = znajdz_sasiadow(obecny, maxSzer, maxWys, mapa)
        for sasiad in sasiedzi:

            if any(z.posX == sasiad.posX and z.posY == sasiad.posY for z in zamknieta_lista):
                continue

            # Oblicza koszt przejścia do sąsiada
            nowy_kosztG = obecny.kosztPrzejscia + 1
            sasiad.kosztPrzejscia = nowy_kosztG
            sasiad.oblicz_heurystyke(celX, celY)

            # Sprawdza, czy sąsiad jest już na liście otwartej
            otwarty = None
            for o in otwarta_lista:
                if o.posX == sasiad.posX and o.posY == sasiad.posY:
                    otwarty = o
                    break


            if otwarty and nowy_kosztG >= otwarty.kosztPrzejscia:
                continue

            o
            if not otwarty:
                otwarta_lista.append(sasiad)

    return None



def oznacz_sciezke(sciezka, mapa):
    print("\nŚcieżka krok po kroku:")
    while sciezka:
        mapa[sciezka.posY][sciezka.posX] = 3
        print("Krok: ({}, {})".format(sciezka.posX, sciezka.posY))
        sciezka = sciezka.nodeRodzic



def main():
    nazwa_pliku = "grid.txt"
    wysokosc = 20
    szerokosc = 20


    mapa = [[0] * szerokosc for _ in range(wysokosc)]


    print(f"\nWczytanie danych z pliku {nazwa_pliku}...\n")
    with open(nazwa_pliku, "r") as plik:
        for i in range(wysokosc):
            linia = list(map(float, plik.readline().split()))
            for j in range(szerokosc):
                mapa[i][j] = linia[j]


    print("\nMapa:")
    for i in range(wysokosc):
        for j in range(szerokosc):
            print(int(mapa[i][j]), end=" ")
        print()


    startX, startY = 19, 0
    celX, celY = 0, 19


    wynik = wykonaj_a_gwiazdka(startX, startY, celX, celY, szerokosc, wysokosc, mapa)

    if wynik:
        print("\nZnaleziono ścieżkę:")
        oznacz_sciezke(wynik, mapa)
        for i in range(wysokosc):
            for j in range(szerokosc):
                print(int(mapa[i][j]), end=" ")
            print()
    else:
        print("\nNie znaleziono ścieżki.")



if __name__ == "__main__":
    main()
