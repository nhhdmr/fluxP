import math
import random
import numpy as np
import fonction as fon
import map


# La classe Person
class Person:
    # la fonction de construction
    def __init__(self, id, x, y):
        self.id = id  # id de personne
        self.position = (x, y)  # la position de personne
        self.dt = 0.05   # delta t de personne
        self.poids = 50  # poids de personne
        self.rayon = (0.4) / 2  # taille de personne
        self.vitesse_esp = (100) / 100  # la vitesse esperée
        self.v = (0, 0)  # la vitesse presente
        self.a = (0, 0)  # l'acceleration prensent
        self.destination = (0, 0)  # destination

    # retourner string pour gérer les piètons sur la visualisation
    def name(self):
        return "ID_" + str(self.id)


# La classe Foule
class Foule:
    # la fonction de construction
    def __init__(self, coords_person, l_w, wall, sorties, obstacles, incendies):
        self.arg_A = 2000
        self.arg_B = 0.08
        self.k = 120000
        self.delta_time = 0.005
        self.map = map.map(l_w, wall, sorties, obstacles, incendies)
        self.list_person = []
        # initialiser la liste de foule
        i = 0
        for coord in coords_person:
            i += 1
            per = Person(i, coord[0], coord[1])
            per.destination = fon.proche_sortie(per.position, self.map.sorties)
            self.list_person.append(per)
        # pour stocker les donnees de heat map
        self.thmap = np.zeros(((l_w[0] + 2), (l_w[1] + 2)))

    # Comptez le nombre de personnes à chaque point du graphique
    # Une personne une fois -> la valeur correspondante +1
    def addMapValue(self, mp, x, y, add=1):
        x, y = int(x), int(y)
        mp[x][y] += add

    # Déterminez si un point se trouve dans une zone.
    def point_in_zone(self, point):
        if 0 <= point[0] <= self.map.length - 1 and 0 <= point[1] <= self.map.width - 1:
            return True
        else:
            return False

    # Calculer la force de mur
    def force_mur(self, person):
        sum_fiw = (0, 0)
        d_max = 3
        d = (person.position[0] - 1) * 0.4
        if 0 < d < d_max:
            for line in self.map.wall[3]:
                if line[0] < person.position[1] < line[1]:
                    fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
                    sum_fiw = (fiw + sum_fiw[0], sum_fiw[1])
        d = (self.map.length - person.position[0]) * 0.4
        if 0 < d < d_max:
            for line in self.map.wall[1]:
                if line[0] < person.position[1] < line[1]:
                    fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
                    sum_fiw = (fiw * (-1) + sum_fiw[0], sum_fiw[1])
        d = (person.position[1] - 1) * 0.4
        if 0 < d < d_max:
            for line in self.map.wall[0]:
                if line[0] < person.position[0] < line[1]:
                    fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
                    sum_fiw = (sum_fiw[0], fiw + sum_fiw[1])
        d = (self.map.width - person.position[1]) * 0.4
        if 0 < d < d_max:
            if 0 < d < d_max:
                for line in self.map.wall[2]:
                    if line[0] < person.position[0] < line[1]:
                        fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
                        sum_fiw = (sum_fiw[0], fiw * (-1) + sum_fiw[1])
        return sum_fiw

    # Calculer la force des obstacles
    def force_obs(self, person, zone_obs):
        sum_fiw = (0, 0)
        d_max = 3
        d = (zone_obs[0][0] - person.position[0]) * 0.4
        if (d < d_max) and (d > 0) and (person.position[1] > zone_obs[0][1]) and (person.position[1] < zone_obs[1][1]):
            fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
            sum_fiw = (fiw * (-1) + sum_fiw[0], sum_fiw[1])
        d = (person.position[0] - zone_obs[1][0]) * 0.4
        if (d < d_max) and (d > 0) and (person.position[1] > zone_obs[0][1]) and (person.position[1] < zone_obs[1][1]):
            fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
            sum_fiw = (fiw + sum_fiw[0], sum_fiw[1])
        d = (zone_obs[0][1] - person.position[1]) * 0.4
        if (d < d_max) and (d > 0) and (person.position[0] > zone_obs[0][0]) and (person.position[0] < zone_obs[1][0]):
            fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
            sum_fiw = (sum_fiw[0], fiw * (-1) + sum_fiw[1])
        d = (person.position[1] - zone_obs[1][1]) * 0.4
        if (d < d_max) and (d > 0) and (person.position[0] > zone_obs[0][0]) and (person.position[0] < zone_obs[1][0]):
            fiw = self.arg_A * math.exp((person.rayon - d) / self.arg_B)
            sum_fiw = (sum_fiw[0], fiw + sum_fiw[1])
        return sum_fiw

    # Calculer l'accélération
    def calcul_a(self):
        for person in self.list_person:
            # Calculez la force motrice.
            e = ((person.destination[0] - person.position[0]) * 0.4,
                 (person.destination[1] - person.position[1]) * 0.4)
            tmp = math.sqrt(math.pow(e[0], 2) + math.pow(e[1], 2))
            if tmp == 0:
                continue
            e = (e[0] / tmp, e[1] / tmp)
            v0e0 = (e[0] * person.vitesse_esp, e[1] * person.vitesse_esp)
            diff_x = v0e0[0] - person.v[0]
            diff_y = v0e0[1] - person.v[1]

            force_auto = (person.poids * diff_x / person.dt, person.poids * diff_y / person.dt)

            # Calculez la force de la foule
            force_foule = (0, 0)
            for per in self.list_person:
                if per.id == person.id:
                    continue
                d = ((person.position[0] - per.position[0]) * 0.4,
                     (person.position[1] - per.position[1]) * 0.4)
                distance = math.sqrt(math.pow(d[0], 2) + math.pow(d[1], 2))
                if distance == 0:
                    continue
                if distance >= 1.4:
                    continue
                diff_r_d = (person.rayon + per.rayon - distance)
                res_nij = self.arg_A * math.exp(diff_r_d / self.arg_B)  # + self.k*fon.g(diff_r_d)
                force_foule = (force_foule[0] + d[0] / distance * res_nij, force_foule[1] + d[1] / distance * res_nij)

            # Calculez la force des obstacles
            force_obs = (0, 0)
            f_mur = self.force_mur(person)
            force_obs = (force_obs[0] + f_mur[0], force_obs[1] + f_mur[1])
            for obs in self.map.zone_obstacale:
                f_obs = self.force_obs(person, obs)
                force_obs = (force_obs[0] + f_obs[0], force_obs[1] + f_obs[1])
            # Calculez la force total
            force_total = (force_auto[0] + force_foule[0] + force_obs[0], force_auto[1] + force_foule[1] + force_obs[1])
            # Calculer l'accélération
            person.a = (force_total[0] / person.poids, force_total[1] / person.poids)

    def move(self):
        # Supprimer les personnes qui sont parties
        new_list = []
        for person in self.list_person:
            if self.point_in_zone(person.position):
                new_list.append(person)
        self.list_person = new_list

        for person in self.list_person:
            # Calculer la nouvelle vitesse
            new_vx = person.v[0] + person.a[0] * self.delta_time
            new_vy = person.v[1] + person.a[1] * self.delta_time
            # Calculer le déplacement
            l_x = (person.v[0] + new_vx) / 2 * self.delta_time / 0.4
            l_y = (person.v[1] + new_vy) / 2 * self.delta_time / 0.4
            # Mettre à jour les informations de la personne
            person.position = (person.position[0] + l_x, person.position[1] + l_y)
            if int(person.position[0]) < self.thmap.shape[0] and int(person.position[1]) < self.thmap.shape[1]:
                self.thmap[int(person.position[0])][int(person.position[1])] += 1
            person.v = (new_vx, new_vy)

    # Mettre à jour les positions des piétons
    def maj(self):
        self.calcul_a()
        self.move()
        return self
