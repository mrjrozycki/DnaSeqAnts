import numpy as np
from Mrowki import AntColony

kosztyDodatkowe = []


def odczytajDane():
    f = open("dane2.txt", "r")
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
        if a[0:len(a) - i] == b[i:len(b)]:
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
            macierzTyl[i][j] = policzOdelegloscPrzod(ciagi[j], ciagi[i])
    # print(macierzPrzod, '\n\n', macierzTyl)
    return macierzPrzod, macierzTyl


def zsumujWartosciIPokazPotencjalne(macierz, ciagi):
    zZerami = np.zeros((len(ciagi), len(ciagi)))
    for i in range(len(macierz)):
        for j in range(len(macierz[i])):
            if macierz[i][j] != np.inf:
                zZerami[i][j] = macierz[i][j]
    sumy = np.sum(zZerami, axis=1)
    potencjalne = []
    maxSum = max(sumy)
    for i in range(len(sumy)):
        if sumy[i] > maxSum - maxSum * 0.01:
            potencjalne.append(i)
    return potencjalne


ciagi = odczytajDane()
przod, tyl = macierzeOdlegosci(ciagi)
potPoczatki = zsumujWartosciIPokazPotencjalne(tyl, ciagi)
potKonce = zsumujWartosciIPokazPotencjalne(przod, ciagi)


poczatki = 1
for i in potPoczatki:
    # print("sprawdzanie nukleotydu początkowego nr ", poczatki)
    poczatki += 1
    najkrotszaOgolnie = [[0], np.inf]
    ant_colony = AntColony(przod, 100, 20, 30, 0.8, alpha=5,
                           beta=3, poczatek=i, ktoraStrona=1)
    najkrotsza = ant_colony.run()
    if najkrotsza[1] < najkrotszaOgolnie[1]:
        najkrotszaOgolnie = najkrotsza
pierwsze = True
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
            break
    if not(dodane):
        ciagKoncowy += ("|"+ciagi[i[1]])
        dodane = 1
print("\n"+ ciagKoncowy, len(ciagKoncowy.replace("|","")))

print("\nKoszt takiej sekwencji od przodu to:",
      najkrotszaOgolnie[1] - len(najkrotszaOgolnie[0]))

konce = 1
for i in potKonce:
    # print("sprawdzanie nukleotydu koncowego nr ", konce)
    konce += 1
    najkrotszaOgolnie = [[0], np.inf]
    ant_colony = AntColony(tyl, 100, 20, 30, 0.8, alpha=5,
                           beta=3, poczatek=i, ktoraStrona=-1)
    najkrotsza = ant_colony.run()
    if najkrotsza[1] < najkrotszaOgolnie[1]:
        najkrotszaOgolnie = najkrotsza

trasa = najkrotszaOgolnie[0][::-1]
trasaGotowa = []
for i in trasa:
    trasaGotowa.append(i[::-1])
trasaGotowa = (trasaGotowa, najkrotszaOgolnie[1])
pierwsze = True
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
            break
    if not(dodane):
        ciagKoncowy += ("|"+ciagi[i[1]])
        dodane = 1
print("\n"+ ciagKoncowy, len(ciagKoncowy.replace("|","")))
print("\nKoszt takiej sekwencji od tylu to:",
      najkrotszaOgolnie[1] - len(najkrotszaOgolnie[0]))
