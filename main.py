import numpy as np
from Mrowki import AntColony
from random import randint
import os
import time
plik = "neglos/55.400-160"
rozmiarN = int(plik[plik.find(".")+1:plik.find(".")+4])+9
dlugosc = rozmiarN
mrowki = int(0.5*rozmiarN)
specjalisci = int(0.3*mrowki)
iteracje = 10
alpha = 5
beta = 3
wspolczynnikFeromonu = 0.8


def odczytajDane():
    f = open(plik, "r")
    ciagi = []
    for x in f:
        ciagi.append(x.rstrip())
    f.close()
    # print(ciagi)
    return ciagi


def policzOdelegloscPrzod(a, b):
    if a == b:
        return np.inf
    for i in range(len(a)+1):
        # print(a[i:len(a)],"\n",b[0:len(b)-i])
        if a[i:len(a)] == b[0:len(b) - i]:
            # print(i)
            break
    return i



def macierzeOdlegosci(ciagi):
    dlugosc = len(ciagi)
    macierzPrzod = np.zeros((dlugosc, dlugosc))
    macierzTyl = np.zeros((dlugosc, dlugosc))
    for i in range(dlugosc):
        for j in range(dlugosc):
            macierzPrzod[i][j] = policzOdelegloscPrzod(ciagi[i], ciagi[j])
            macierzTyl[i][j] = policzOdelegloscPrzod(ciagi[j], ciagi[i])
    # print(macierzPrzod, '\n\n', macierzTyl)
    return macierzPrzod, macierzTyl


def zsumujWartosciIPokazPotencjalne(macierz, ciagi):
    maxIlosc = 1
    ile = 0
    zZerami = np.zeros((len(ciagi), len(ciagi)))
    for i in range(len(macierz)):
        for j in range(len(macierz[i])):
            if macierz[i][j] != np.inf:
                zZerami[i][j] = macierz[i][j]
    sumy = np.mean(zZerami, axis=1)
    potencjalne = []
    maxSum = max(sumy)
    for i in range(len(sumy)):
        if sumy[i] > maxSum - maxSum * 0.001 and ile<maxIlosc:
            ile+=1
            potencjalne.append(i)
    return potencjalne

def odpalIPrintuj(ciagi, macierz, potencjalne, strona):
    for i in potencjalne:
        najkrotszaOgolnie = [[0], np.inf]
        ant_colony = AntColony(macierz, mrowki, specjalisci, iteracje, wspolczynnikFeromonu, alpha=alpha,
                               beta=beta, poczatek=i, ktoraStrona=1, maxDlugosc=dlugosc)
        najkrotsza = ant_colony.run()
        if len(najkrotsza[0]) > len(najkrotszaOgolnie[0]):
            najkrotszaOgolnie = najkrotsza
        elif len(najkrotsza[0]) == len(najkrotszaOgolnie[0]) and najkrotsza[1]>najkrotszaOgolnie[1] and najkrotsza[1]<=dlugosc:
            najkrotszaOgolnie = najkrotsza
    if strona == 1:
        ile = 1
        ciagKoncowy = ""
        pierwszyWierzcholek = najkrotszaOgolnie[0][0][0]
        ciagKoncowy += ciagi[pierwszyWierzcholek]
        # print(ciagKoncowy)
        for i in najkrotszaOgolnie[0]:
            dodane = 0
            for k in range(len(ciagi[i[0]])):
                if ciagi[i[0]][k:len(ciagi[i[0]])] == ciagi[i[1]][0:len(ciagi[i[1]]) - k]:
                    ciagKoncowy += ("|"+ciagi[i[1]][len(ciagi[i[1]]) - k:len(ciagi[i[1]])])
                    dodane = 1
                    ile+=1
                    break
            if not(dodane):
                ciagKoncowy += ("|"+ciagi[i[1]])
                dodane = 1
                ile+=1

    elif strona == -1:
        trasa = najkrotszaOgolnie[0][::-1]
        trasaGotowa = []
        for i in trasa:
            trasaGotowa.append(i[::-1])
        trasaGotowa = (trasaGotowa, najkrotszaOgolnie[1])
        ile = 1
        ciagKoncowy = ""
        pierwszyWierzcholek = trasaGotowa[0][0][0]
        ciagKoncowy += ciagi[pierwszyWierzcholek]
        # print(ciagKoncowy)
        for i in trasaGotowa[0]:
            dodane = 0
            for k in range(len(ciagi[i[0]])):
                if ciagi[i[0]][k:len(ciagi[i[0]])] == ciagi[i[1]][0:len(ciagi[i[1]]) - k]:
                    ciagKoncowy += ("|"+ciagi[i[1]][len(ciagi[i[1]]) - k:len(ciagi[i[1]])])
                    dodane = 1
                    ile+=1
                    break
            if not(dodane):
                ciagKoncowy += ("|"+ciagi[i[1]])
                dodane = 1
                ile+=1


    return ciagKoncowy, len(ciagKoncowy.replace("|","")), ile

folder = "neglos"
i = "18.200-40"
# for i in os.listdir(folder):
plik = folder+"/"+i
rozmiarN = int(plik[plik.find(".")+1:plik.find(".")+4])+9
dlugosc = rozmiarN
# alpha = randint(1,10)
# beta = randint(1,10)
# print("Wartość alpha: ", alpha, "\nWartość beta: ", beta)
print(plik)
start = time.time()
ciagi = odczytajDane()
przod, tyl = macierzeOdlegosci(ciagi)
potPoczatki = zsumujWartosciIPokazPotencjalne(tyl, ciagi)
potKonce = zsumujWartosciIPokazPotencjalne(przod, ciagi)
ciagP, nP, slowaP = odpalIPrintuj(ciagi, przod, potPoczatki, 1)
ciagK, nK, slowaK = odpalIPrintuj(ciagi, tyl, potKonce, -1)
# print(specjalisci)
end = time.time()
print(end-start)
print("\n\nSzukanie od przodu:")
print("\n"+ ciagP)
print("\nDługość tej sekwencji to(n): ", nP)
print("Liczba nukleotydów w tej sekwencji to:", slowaP, "\n")
print("\n\nSzukanie od konca:")
print("\n"+ ciagK)
print("\nDługość tej sekwencji to(n): ", nK)
print("Liczba nukleotydów w tej sekwencji to:", slowaK, "\n")
