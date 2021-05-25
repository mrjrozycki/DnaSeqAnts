import numpy as np
from Mrowki import AntColony

kosztyDodatkowe = []


def odczytajDane():
    f = open("testowe.txt", "r")
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
    if i == 9:
        return i + 10
    else:
        return i


def policzOdelegloscTyl(a, b):
    if a == b:
        return np.inf
    for i in range(len(a)):
        # print(a[0:len(a)-i],"\n",b[i:len(b)])
        if a[0:len(a)-i] == b[i:len(b)]:
            # print(i)
            break
    if i == 9:
        return i + 10
    else:
        return i


def macierzeOdlegosci(ciagi):
    dlugosc = len(ciagi)
    macierzPrzod = np.zeros((dlugosc, dlugosc))
    macierzTyl = np.zeros((dlugosc, dlugosc))
    for i in range(dlugosc):
        for j in range(dlugosc):
            macierzPrzod[i][j] = policzOdelegloscPrzod(ciagi[i], ciagi[j])
            macierzTyl[i][j] = policzOdelegloscTyl(ciagi[i], ciagi[j])
    print(macierzPrzod, '\n\n', macierzTyl)
    return macierzPrzod, macierzTyl


ciagi = odczytajDane()
przod, tyl = macierzeOdlegosci(ciagi)
zZeramiPrzod = np.zeros((len(ciagi), len(ciagi)))
zZeramiTyl = np.zeros((len(ciagi), len(ciagi)))
for i in range(len(przod)):
    for j in range(len(przod[i])):
        if przod[i][j] != np.inf:
            zZeramiPrzod[i][j] = przod[i][j]
        if tyl[i][j] != np.inf:
            zZeramiTyl[i][j] = tyl[i][j]

sumyPrzod = np.sum(zZeramiPrzod, axis=1)
potKonce = []
koncowySum = max(sumyPrzod)
for i in range(len(sumyPrzod)):
    if sumyPrzod[i] == koncowySum:
        potKonce.append(i)


sumyTyl = np.sum(zZeramiTyl, axis=1)
potPoczatki = []
pocztkiSum = max(sumyTyl)
for i in range(len(sumyTyl)):
    if sumyTyl[i] == pocztkiSum:
        potPoczatki.append(i)



for i in potPoczatki:
    ant_colony = AntColony(przod, 100, 20, 10, 0.8, alpha=1, beta=0.8, poczatek=i)
    najkrotsza = ant_colony.run()
    pierwsze = True
    for i in najkrotsza[0]:
        pierwsza = i[0]
        druga = i[1]
        if pierwsze:
            print(ciagi[pierwsza], ciagi[druga], end=" ")
            pierwsze = False
        else:
            print(ciagi[druga], end=" ")
    print("\nKoszt takiej sekwencji od przodu to:", najkrotsza[1] - len(ciagi))

for i in potKonce:
    ant_colony = AntColony(przod, 100, 20, 10, 0.8, alpha=1, beta=0.8, poczatek=i)
    najkrotsza = ant_colony.run()
    pierwsze = True
    # for i in najkrotsza[0]:
    #     pierwsza = i[0]
    #     druga = i[1]
    #     if pierwsze:
    #         print(ciagi[pierwsza], ciagi[druga], end=" ")
    #         pierwsze = False
    #     else:
    #         print(ciagi[druga], end=" ")
    print(najkrotsza[0])
    print("\nKoszt takiej sekwencji od tylu to:", najkrotsza[1] - len(ciagi))
