import random as rn
import numpy as np
from numpy.random import choice as np_choice


class AntColony(object):

    def __init__(self, odleglosci, ileMrowek, ileNajlepszychMrowek, iteracje, rozkladFeromonu, alpha=1, beta=1, poczatek=0):
        """
        Args:
            odleglosci (2D numpy.array) - macierz odlegosci
            ileMrowek (int) - ile mrowek ma ruszac w tym samym momencie
            ileNajlepszychMrowek (int) - ile najlepszych mrowek ma zostawiac feromon
            iteracje (int) - ile ma zrobic iteracji
            rozkladFeromonu (float) - jak szybko rozklada sie feromon (feromon jest mnozony przez ta wartosc wiec np 0.95 to malutki rozklad a 0.5 to ogromyn)
            alpha (int or float) - waznosc feromonu (def 1)
            beta (int or float) - waznosc odleglosci (def 1), im wieksza tym bardziej przypomina zachlanny
        Przyklad:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
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

    def run(self):
        powtorzenie = 0
        poprzedniaNajkrotsza = 0
        najkrotszaTrasa = None
        ogolnieNajkrotszaTrasa = ("placeholder", np.inf)
        for i in range(self.iteracje):
            wszystkieSciezki = self.wygenerujWszystkieSciezki()
            # print(self.feromon)
            self.wypuscFeromon(
                wszystkieSciezki, self.ileNajlepszychMrowek,
                shortest_path=najkrotszaTrasa)
            # print(wszystkieSciezki)
            najkrotszaTrasa = min(wszystkieSciezki, key=lambda x: x[1])
            # print(najkrotszaTrasa)
            print("Obliczono juz: {:.2f}% algorytmu".format(
                (i + 1) * 100 / self.iteracje))
            if najkrotszaTrasa[1] < ogolnieNajkrotszaTrasa[1]:
                ogolnieNajkrotszaTrasa = najkrotszaTrasa
            self.feromon = self.feromon * self.rozkladFeromonu
        return ogolnieNajkrotszaTrasa

    def wypuscFeromon(self, wszystkieSciezki, ileNajlepszychMrowek, shortest_path):
        posortowanaSciezka = sorted(wszystkieSciezki, key=lambda x: x[1])
        for path, dist in posortowanaSciezka[:ileNajlepszychMrowek]:
            for move in path:
                self.feromon[move] += 1.0 / self.odleglosci[move]

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
