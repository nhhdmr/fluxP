import math
from collections import defaultdict
import random
import numpy as np

import fonction as fon
import map


# La classe Person
class Person:
    normal_speed = 1

    # la fonction de construction
    def __init__(self, id, x, y):
        self.id = id
        self.position = (x, y)
        self.speed = Person.normal_speed
        self.stat = False

    # retourner string pour gérer les piètons sur la visualisation
    def name(self):
        return "ID_" + str(self.id)


# La classe Foule
class Foule():
    # la fonction de construction
    def __init__(self, coords_person, l_w, sorties, obstacles, incendies):
        self.map = map.map(l_w, sorties, obstacles, incendies)
        self.list_person = []
        self.list_move_pc = []
        i = 0
        for coord in coords_person:
            i += 1
            self.list_person.append(Person(i, coord[0], coord[1]))
        self.thmap = np.zeros(((l_w[0] + 2), (l_w[1] + 2)))

        self.pos_pd = np.zeros((l_w[0]+1,l_w[1]+1))
        for i in range(0,l_w[0]+1):
            for j in range(0,l_w[1]+1):
                pt = (i,j)
                sor = fon.proche_sortie(pt,self.map.sorties)
                pd = fon.pd(pt,sor)
                self.pos_pd[i][j] = pd

    # Comptez le nombre de personnes à chaque point du graphique
    # Une personne une fois -> la valeur correspondante +1
    def addMapValue(self, mp, x, y, add=1):
        x, y = int(x), int(y)
        mp[x][y] += add

    '''def setMapValue(self, mp, x, y, val=0):
        x, y = int(x), int(y)
        mp[x][y] = val'''

    '''def getMapValue(self, mp, x, y):
        x, y = int(x), int(y)
        return mp[x][y]'''

    # Déterminez si un point se trouve dans une zone.
    def point_in_zone(self, point):
        if 0 < point[0] < self.map.length - 1 and 0 < point[1] < self.map.width - 1:
            return True
        else:
            return False

    # Obtenez la liste des cellules voisines de la cellule.
    def voisins(self, person):
        list_voisin = []
        list_voisin.append((person.position[0] + 1, person.position[1] - 1))
        list_voisin.append((person.position[0] + 1, person.position[1]))
        list_voisin.append((person.position[0] + 1, person.position[1] + 1))
        list_voisin.append((person.position[0], person.position[1] + 1))
        list_voisin.append((person.position[0] - 1, person.position[1] + 1))
        list_voisin.append((person.position[0] - 1, person.position[1]))
        list_voisin.append((person.position[0] - 1, person.position[1] - 1))
        list_voisin.append((person.position[0], person.position[1] - 1))

        for voisin in list_voisin:
            if not self.point_in_zone(voisin):
                list_voisin.remove(voisin)
            else:
                if self.point_obstacle(voisin) or self.point_stat(voisin):
                    list_voisin.remove(voisin)
            '''if self.point_stat(voisin):
                list_voisin.remove(voisin)'''
        return list_voisin

    # Déterminer si un point est occupé
    def point_stat(self, point):
        tmp = False
        for person in self.list_person:
            if point[0] == person.position[0] and point[1] == person.position[1]:
                tmp = True
        return tmp

    # Déterminer si un point est un obstacle
    def point_obstacle(self, point):
        tmp = False
        for obstacle in self.map.list_obstacle:
            if point[0] == obstacle[0] and point[1] == obstacle[1]:
                tmp = True
        return tmp

    # calculer le parametre gamma pour Pr
    def calcul_gamma(self, point):
        pt = Person(999, point[0], point[1])
        num_v_libre = len(self.voisins(pt))
        return 7 - num_v_libre

    # Calculez les nombres correspondants aux directions de déplacement des cellules voisines.
    def pc_m_n(self, person):
        list_m_n = [0,0,0,0,0,0,0,0,0]
        voisins = self.voisins(person)
        for voisin in voisins:
            for pt in self.list_move_pc:
                if pt[0][0]==voisin[0] and pt[0][1]==voisin[1]:
                    dir = pt[1]
                    dir_org = fon.direction(voisin,person.position)
                    if dir != dir_org:
                        list_m_n[0] += 1
                        list_m_n[dir] += 1
        return list_m_n

    # Calculez l'intensité du mouvement des cellules voisin et sélectionnez la prochaine position de déplacement.
    def calcul(self):
        u1 = 10
        '''u2 = 0.001
        u3 = -0.1
        u4 = -0.1
        u5 = -0.3'''
        u2 = 0
        u3 = 0
        u4 = 0
        u5 = 0
        list_result = []
        for person in self.list_person:
            list_voisin = self.voisins(person)
            p_max = -9999
            position_next = ()
            list_m_n = self.pc_m_n(person)
            for voisin in list_voisin:
                # CALCULER AU DEBUT
                #sor = fon.proche_sortie(voisin, self.map.sorties)
                # MEME
                #pd = fon.pd(voisin, sor)
                pd = self.pos_pd[voisin[0]][voisin[1]]
                # print(pd)
                dir = fon.direction(person.position, voisin)
                pc = fon.pc(list_m_n[dir], list_m_n[0])
                gamma = self.calcul_gamma(voisin)
                pr = fon.pr(gamma)
                pf = fon.pf(gamma)
                # TODO
                pfire = 0
                # pfire = fon.pfire(voisin, sor, [10, 10])
                p_total = u1 * pd + u2 * pc + u3 * pr + u4 * pf + u5 * pfire
                #print("p_max: " + str(p_max))
                #print("p_total: " + str(p_total))
                #print(math.fabs(p_total - p_max))
                if p_total > p_max:
                    p_max = p_total
                    position_next = voisin
                # elif math.fabs(p_total - p_max) == 0:
                elif p_total - p_max == 0:
                    d1_x = voisin[0] - person.position[0]
                    d1_y = voisin[1] - person.position[1]
                    distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                    d2_x = position_next[0] - person.position[0]
                    d2_y = position_next[1] - person.position[1]
                    distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                    if distance1 < distance2:
                        position_next = voisin
            list_result.append((person, position_next))
            #print(p_max)
        return list_result

    # Mettre à jour les positions des piétons
    def maj(self):
        # Détecter si le piéton a atteint la sortie et mettre à jour la valeur de heat map
        for person in self.list_person:
            self.addMapValue(self.thmap, person.position[0], person.position[1])
            if person.position in self.map.sorties:
                person.stat = True
                self.list_person.remove(person)

        # Classement des piétons selon la même cible mobile suivante
        list_calcul = self.calcul()
        d = defaultdict(list)
        list_pt = []
        for i, v in enumerate(list_calcul):
            d[v[1]].append(v[0])
            if v[1] not in list_pt:
                list_pt.append(v[1])
        self.list_move_pc = []

        # Résolution de conflit
        for pt in list_pt:
            # sans conflit si seul point
            if len(d[pt]) == 1:
                dir = fon.direction(d[pt][0].position, pt)
                self.list_move_pc.append((d[pt][0].position, dir))
                d[pt][0].position = pt
                '''sor = fon.proche_sortie(d[pt][0].position,self.map.sorties)
                d1_x = sor[0] - d[pt][0].position[0]
                d1_y = sor[1] - d[pt][0].position[1]
                distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                d2_x = sor[0] - pt[0]
                d2_y = sor[1] - pt[1]
                distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                if distance1 > distance2:
                    dir = fon.direction(d[pt][0].position, pt)
                    self.list_move_pc.append((d[pt][0].position, dir))
                    d[pt][0].position = pt'''
            # Si plusieurs piétons ont la même position suivante,
            # l'un est sélectionné au hasard pour se déplacer et
            # les autres piétons ne bougent pas.
            else:
                num = len(d[pt])
                choice = random.randint(0, num - 1)
                dir = fon.direction(d[pt][choice].position, pt)
                self.list_move_pc.append((d[pt][choice].position, dir))
                d[pt][choice].position = pt
                '''sor = fon.proche_sortie(d[pt][choice].position, self.map.sorties)
                d1_x = sor[0] - d[pt][choice].position[0]
                d1_y = sor[1] - d[pt][choice].position[1]
                distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                d2_x = sor[0] - pt[0]
                d2_y = sor[1] - pt[1]
                distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                if distance1 > distance2:
                    dir = fon.direction(d[pt][choice].position, pt)
                    self.list_move_pc.append((d[pt][choice].position, dir))
                    d[pt][choice].position = pt'''
        #print(self.list_person[0].position)
        return self

    '''def run(self):
        i = 0
        list_out = []
        while len(self.list_person)!=0:
            self.maj()
            for pp in self.list_person:
                print(pp.position)
            for person in self.list_person:
                if person.position in self.map.sorties:
                    list_out.append(person)
                    person.stat = True
                    self.list_person.remove(person)
            i += 1
            print(i)
        print(list_out)
        return self'''
