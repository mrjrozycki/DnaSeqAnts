import numpy as np
import random

def odczytajDane():
    f = open("dane.txt", "r")
    ciagi = []
    for x in f:
        ciagi.append(x.rstrip())
    f.close()
    # print(ciagi)
    return ciagi


def policzOdelegloscPrzod(a, b):
    if a == b:
        return np.inf
    for i in range(len(a)):
        # print(a[i:len(a)],"\n",b[0:len(b)-i])
        if a[i:len(a)] == b[0:len(b) - i]:
            # print(i)
            break
    # if i == 9:
    #     return i + 10
    # else:
    return i


def macierzeOdlegosci(ciagi):
    dlugosc = len(ciagi)
    macierzPrzod = np.zeros((dlugosc, dlugosc))
    macierzTyl = np.zeros((dlugosc, dlugosc))
    for i in range(dlugosc):
        for j in range(dlugosc):
            macierzPrzod[i][j] = policzOdelegloscPrzod(ciagi[i], ciagi[j])
            # macierzTyl[i][j] = policzOdelegloscPrzod(ciagi[j], ciagi[i])
    # print(macierzPrzod, '\n\n', macierzTyl)
    return macierzPrzod


ciagi = odczytajDane()
przod = macierzeOdlegosci(ciagi)

tablica = []
for i in range(len(ciagi)):
    tablica.append(i)
ogolna = np.inf
najszybsza = []
for i in range(1000):
    random.shuffle(tablica)
    # print(tablica)
    dlugosc = 0
    for i in range(len(tablica)-1):
        dlugosc+=przod[tablica[i]][tablica[i+1]]
    if dlugosc<ogolna:
        najszybsza = tablica
        ogolna = dlugosc
print(ogolna)
for i in najszybsza:
    # print(ciagi[i], end=" ")
    pass
print("\n")
