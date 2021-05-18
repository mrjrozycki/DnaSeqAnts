import numpy as np
from Mrowki import AntColony

kosztyDodatkowe = []

def odczytajDane():
    f = open("dane.txt", "r")
    ciagi = []
    for x in f:
        ciagi.append(x.rstrip())
    f.close()
    # print(ciagi)
    return ciagi


def policzOdeleglosc(a, b):
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


def macierzOdlegosci(ciagi):
    dlugosc = len(ciagi)
    macierz = np.zeros((dlugosc, dlugosc))
    for i in range(dlugosc):
        for j in range(dlugosc):
            macierz[i][j] = policzOdeleglosc(ciagi[i], ciagi[j])
    print(macierz)
    return macierz


ciagi = odczytajDane()
gotowa = macierzOdlegosci(ciagi)
ant_colony = AntColony(gotowa, 200, 5, 30, 0.7, alpha=1, beta=1)
najkrotsza = ant_colony.run()
# print ("Najkrotsza trasa to: {}".format(najkrotsza))
pierwsze = True
for i in najkrotsza[0]:
    pierwsza = i[0]
    druga = i[1]
    if pierwsze:
        print(ciagi[pierwsza], ciagi[druga], end=" ")
        pierwsze = False
    else:
        print(ciagi[druga], end=" ")
print("\nKoszt takiej sekwencji to:", najkrotsza[1] - len(ciagi))
print(kosztyDodatkowe)
# print(i[0], i[1])
# print(najkrotsza[0][1])
