import random as rn
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, odleglosci, ileMrowek, ileNajlepszychMrowek, iteracje, rozkladFeromonu, alpha=1, beta=1):
        """
        Args:
            odleglosci (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            ileMrowek (int): Number of ants running per iteration
            ileNajlepszychMrowek (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            rozkladFeromonu (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.odleglosci  = odleglosci
        self.feromon = np.ones(self.odleglosci.shape) / len(odleglosci)
        self.ileWierzcholkow = range(len(odleglosci))
        self.ileMrowek = ileMrowek
        self.ileNajlepszychMrowek = ileNajlepszychMrowek
        self.iteracje = iteracje
        self.rozkladFeromonu = rozkladFeromonu
        self.alpha = alpha
        self.beta = beta

    def run(self):
        najkrotszaTrasa = None
        ogolnieNajkrotszaTrasa = ("placeholder", np.inf)
        for i in range(self.iteracje):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.ileNajlepszychMrowek, shortest_path=najkrotszaTrasa)
            najkrotszaTrasa = min(all_paths, key=lambda x: x[1])
            #print (najkrotszaTrasa)
            print("Obliczono juz: {:.2f}% algorytmu".format((i+1) * 100 / self.iteracje))
            if najkrotszaTrasa[1] < ogolnieNajkrotszaTrasa[1]:
                ogolnieNajkrotszaTrasa = najkrotszaTrasa
            self.feromon * self.rozkladFeromonu
        return ogolnieNajkrotszaTrasa

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.feromon[move] += 1.0 / self.odleglosci[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.odleglosci[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.ileMrowek):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.odleglosci) - 1):
            move = self.pick_move(self.feromon[prev], self.odleglosci[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.ileWierzcholkow, 1, p=norm_row)[0]
        return move
