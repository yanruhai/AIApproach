import numpy as np
from mst import MST_Prim



class TSP:
    distance_matrix = []
    visited = []
    unvisited = []
    path = []
    distance = 0

    def __init__(self, n_cities, distance_matrix):
        self.n_cities = n_cities
        self.distance_matrix = distance_matrix

    def search(self):
        self.visited = [0]
        self.unvisited = list(range(1, self.n_cities))
        self.path = [0]
        self.distance = 0
        while len(self.unvisited) > 0:
            min_distance = float('inf')