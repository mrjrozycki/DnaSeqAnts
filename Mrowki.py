import random as rn
import numpy as np
from numpy.random import choice as np_choice


class AntColony(object):

    def __init__(self, odleglosci, ileMrowek, ileNajlepszychMrowek, iteracje, rozkladFeromonu, alpha=1, beta=1, poczatek=0, ktoraStrona=1):
        """
        Args:
            odleglosci (2D numpy.array) - macierz odlegosci
            ileMrowek (int) - ile mrowek ma ruszac w tym samym momencie
            ileNajlepszychMrowek (int) - ile najlepszych mrowek ma zostawiac feromon
            iteracje (int) - ile ma zrobic iteracji
            rozkladFeromonu (float) - jak szybko rozklada sie feromon (feromon jest mnozony przez ta wartosc wiec np 0.95 to malutki rozklad a 0.5 to ogromyn)
            alpha (int or float) - waznosc feromonu (def 1)
            beta (int or float) - waznosc odleglosci (def 1), im wieksza tym bardziej przypomina zachlanny
            poczatek - numer wierzholka poczatkowego
            ktoraStrona - czy idzie od poczatku czy od konca (1 - poczatek, -1 - koniec)
        Przyklad:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2, poczatek=0, ktoraStrona=1)
        """
        self.odleglosci = odleglosci
        self.feromon = np.ones(self.odleglosci.shape) / len(odleglosci)
        self.ileWierzcholkow = range(len(odleglosci))
        self.ileMrowek = ileMrowek
        self.ileNajlepszychMrowek = ileNajlepszychMrowek
        self.iteracje = iteracje
        self.rozkladFeromonu = rozkladFeromonu
        self.alpha = alpha
        self.beta = beta
        self.poczatek = poczatek
        self.ktoraStrona = ktoraStrona

    def run(self):
        powtorzenie = 0
        poprzedniaNajkrotsza = 0
        najkrotszaTrasa = None
        ogolnieNajkrotszaTrasa = ("placeholder", np.inf)
        print("Aktualny wierzcholek startowy to: ", self.poczatek)
        for i in range(self.iteracje):
            # print("Aktualny wierzcholek startowy to: ", self.poczatek)
            wszystkieSciezki = self.wygenerujWszystkieSciezki()
            # print(self.feromon)
            self.wypuscFeromon(
                wszystkieSciezki, self.ileNajlepszychMrowek,
                shortest_path=najkrotszaTrasa)
            # print(wszystkieSciezki)
            najkrotszaTrasa = min(wszystkieSciezki, key=lambda x: x[1])
            # print(poprzedniaNajkrotsza >= najkrotszaTrasa[1]-najkrotszaTrasa[1]*0.1, poprzedniaNajkrotsza <= najkrotszaTrasa[1]+najkrotszaTrasa[1]*0.1)
            if poprzedniaNajkrotsza >= najkrotszaTrasa[1] - najkrotszaTrasa[1] * 0.1 and poprzedniaNajkrotsza <= najkrotszaTrasa[1] + najkrotszaTrasa[1] * 0.1:
                powtorzenie += 1
            poprzedniaNajkrotsza = najkrotszaTrasa[1]
            # print(najkrotszaTrasa)
            # print("Obliczono juz: {:.2f}% algorytmu".format(
                # (i + 1) * 100 / self.iteracje))
            if najkrotszaTrasa[1] < ogolnieNajkrotszaTrasa[1]:
                ogolnieNajkrotszaTrasa = najkrotszaTrasa
            self.feromon = self.feromon * self.rozkladFeromonu
            if powtorzenie == round(self.iteracje * 0.15):
                powtorzenie = 0
                self.feromon = self.feromon * 0
                for i in range(len(self.feromon)):
                    self.feromon[i] += 0.25
                # print(najkrotszaTrasa)
                self.znajdzNajlepszyPoczatek(najkrotszaTrasa[0])
                print("Resetuje wartosci feromonow, a aktualny wierzcholek startowy to: ", self.poczatek)
        return ogolnieNajkrotszaTrasa

    def wypuscFeromon(self, wszystkieSciezki, ileNajlepszychMrowek, shortest_path):
        posortowanaSciezka = sorted(wszystkieSciezki, key=lambda x: x[1])
        for path, dist in posortowanaSciezka[:ileNajlepszychMrowek]:
            for move in path:
                self.feromon[move] += 0.5 / self.odleglosci[move]

    def podajOdlegloscSciezki(self, path):
        pelenDystans = 0
        for x in path:
            pelenDystans += self.odleglosci[x]
        return pelenDystans

    def wygenerujWszystkieSciezki(self):
        wszystkieSciezki = []
        for i in range(self.ileMrowek):
            path = self.wygenerujSciezke(self.poczatek)
            wszystkieSciezki.append((path, self.podajOdlegloscSciezki(path)))
        # print(wszystkieSciezki)
        return wszystkieSciezki

    def wygenerujSciezke(self, start):
        path = []
        odwiedzone = set()
        odwiedzone.add(start)
        prev = start
        for i in range(len(self.odleglosci) - 1):
            move = self.coDalej(
                self.feromon[prev], self.odleglosci[prev], odwiedzone)
            path.append((prev, move))
            prev = move
            odwiedzone.add(move)
        #path.append((prev, start))
        return path

    def coDalej(self, feromon, dist, odwiedzone):
        feromon = np.copy(feromon)
        feromon[list(odwiedzone)] = 0

        row = feromon ** self.alpha * ((1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.ileWierzcholkow, 1, p=norm_row)[0]
        return move

    def znajdzNajlepszyPoczatek(self, polaczenia):
        wierzcholki = []
        wierzcholki.append([polaczenia[0][0], 0, 0])
        for i in polaczenia:
            wierzcholki.append([i[1], 0, 0])
        for k in polaczenia:
            for l in range(len(wierzcholki)):
                if wierzcholki[l][0] == k[0]:
                    wierzcholki[l][1] = self.odleglosci[wierzcholki[l][0]][k[1]]
                    wierzcholki[l+1][2] = self.odleglosci[wierzcholki[l][0]][k[1]]
                    # print(wierzcholki[l][0], k[0])
        najgorszyKoniec = max(wierzcholki, key=lambda x: x[2] - x[1])
        najgorszyPoczatek = max(wierzcholki, key=lambda x: x[2] - x[1])
        if self.ktoraStrona == -1:
            self.poczatek = najgorszyKoniec[0]
            # print(wierzcholki, najgorszyKoniec)
        elif self.ktoraStrona == 1:
            self.poczatek = najgorszyPoczatek[0]
            # print(wierzcholki, najgorszyPoczatek)
