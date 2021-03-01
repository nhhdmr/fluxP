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
        self.pos_pass = []
        self.rest = 0

    # retourner string pour gérer les piètons sur la visualisation
    def name(self):
        return "ID_" + str(self.id)


# La classe Foule
class Foule:
    # la fonction de construction
    def __init__(self, coords_person, l_w, wall, sorties, obstacles, incendies):
        self.map = map.map(l_w, wall, sorties, obstacles, incendies)
        self.list_person = []
        self.list_move_pc = []
        # initialiser la liste de foule
        i = 0
        for coord in coords_person:
            i += 1
            self.list_person.append(Person(i, int(coord[0]), int(coord[1])))
        # pour stocker les donnees de heat map
        self.thmap = np.zeros(((l_w[0] + 2), (l_w[1] + 2)))
        # stocker les resultats pour Pd
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

    # Déterminez si un point se trouve dans une zone.
    def point_in_zone(self, point):
        if 0 <= point[0] <= self.map.length - 1 and 0 <= point[1] <= self.map.width - 1:
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

        # conserver les voisin dispinibles
        res = []
        for voisin in list_voisin:
            if self.point_in_zone(voisin) and not self.point_obstacle(voisin) and not self.point_stat(voisin):
                res.append(voisin)
        return res

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
        # list_m_n[0] : le nombre total
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
        # les poids de chaque partie
        # u1: coefficient d'attractivité de la sortie
        # u2: coefficient d'attractivité du foule
        # u3: coefficient de répulsion entre foule et obstacle
        # u4: coefficient de friction
        # u5: Coefficient de répulsion du feu
        '''u1 = 20
        u2 = 0.1
        u3 = -0.1
        u4 = -0.05
        u5 = -0.1'''
        u1 = 10
        u2 = 0.01
        u3 = -0.1
        u4 = -0.05
        u5 = -0.01
        '''u2 = 0
        u3 = 0
        u4 = 0
        u5 = 0'''
        list_result = []
        for person in self.list_person:
            list_voisin = self.voisins(person)
            p_max = -9999
            position_next = ()
            list_m_n = self.pc_m_n(person)
            for voisin in list_voisin:
                # calculer pd, pc, pr, pf; pfire
                pd = self.pos_pd[voisin[0]][voisin[1]]
                dir = fon.direction(person.position, voisin)
                pc = fon.pc(list_m_n[dir], list_m_n[0])
                gamma = self.calcul_gamma(voisin)
                pr = fon.pr(gamma)
                pf = fon.pf(gamma)
                # pfire = 0
                sor = fon.proche_sortie(voisin,self.map.sorties)
                pfire = 0
                if len(self.map.incendies)>0 :
                    pfire = fon.pfire(voisin,sor,self.map.incendies[0])
                #print(pd,pc,pr,pf,pfire)
                # Calculer l'intensité totale du mouvement
                p_total = u1 * pd + u2 * pc + u3 * pr + u4 * pf + u5 * pfire
                if p_total > p_max:
                    p_max = p_total
                    position_next = voisin
                # elif math.fabs(p_total - p_max) == 0:
                elif p_max - p_total < 0.0001:
                    d1_x = voisin[0] - person.position[0]
                    d1_y = voisin[1] - person.position[1]
                    distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                    d2_x = position_next[0] - person.position[0]
                    d2_y = position_next[1] - person.position[1]
                    distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                    if distance1 < distance2:
                        position_next = voisin
            # stocker la position avec intensité maximale
            list_result.append((person, position_next))
        return list_result

    # Mettre à jour les positions des piétons
    def maj1(self):
        # Détecter si le piéton a atteint la sortie et mettre à jour la valeur de heat map
        tmp = []
        for person in self.list_person:
            if person.position not in person.pos_pass:
                person.pos_pass.append(person.position)
            self.addMapValue(self.thmap, person.position[0], person.position[1])
            if person.position in self.map.sorties:
                person.stat = True
            else:
                tmp.append(person)
        self.list_person = tmp

        # Classement des piétons selon la même cible mobile suivante
        list_calcul = self.calcul()
        d = defaultdict(list)
        list_pt = []
        for i, v in enumerate(list_calcul):
            d[v[1]].append(v[0])
            if v[1] not in list_pt:
                if v[1] != ():
                    list_pt.append(v[1])

        self.list_move_pc = []
        # Résolution de conflit
        for pt in list_pt:
            #sans conflit si seul point'''
            if len(d[pt]) == 1:
                sor = fon.proche_sortie(d[pt][0].position,self.map.sorties)
                d1_x = sor[0] - d[pt][0].position[0]
                d1_y = sor[1] - d[pt][0].position[1]
                distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                d2_x = sor[0] - pt[0]
                d2_y = sor[1] - pt[1]
                distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                # la limite pour decider le pt move ou pas
                if distance1 > distance2 or d[pt][0].rest > 5:
                    dir = fon.direction(d[pt][0].position, pt)
                    self.list_move_pc.append((d[pt][0].position, dir))
                    d[pt][0].position = pt
                    d[pt][0].rest = 0
                else:
                    d[pt][0].rest += 1
            # Si plusieurs piétons ont la même position suivante,
            # l'un est sélectionné au hasard pour se déplacer et
            # les autres piétons ne bougent pas.
            # else:
            elif len(d[pt]) > 1 and pt != ():
                num = len(d[pt])
                choice = random.randint(0, num - 1)
                sor = fon.proche_sortie(d[pt][choice].position, self.map.sorties)
                d1_x = sor[0] - d[pt][choice].position[0]
                d1_y = sor[1] - d[pt][choice].position[1]
                distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                d2_x = sor[0] - pt[0]
                d2_y = sor[1] - pt[1]
                distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                # la limite pour decider le pt move ou pas
                if distance1 >= distance2 or d[pt][choice].rest > 5:
                    dir = fon.direction(d[pt][choice].position, pt)
                    self.list_move_pc.append((d[pt][choice].position, dir))
                    d[pt][choice].position = pt
                    d[pt][choice].rest = 0
                else:
                    d[pt][choice].rest += 1
        return self

    def maj(self):
        # Détecter si le piéton a atteint la sortie et mettre à jour la valeur de heat map
        tmp = []
        for person in self.list_person:
            if person.position not in person.pos_pass:
                person.pos_pass.append(person.position)
            self.addMapValue(self.thmap, person.position[0], person.position[1])
            if person.position in self.map.sorties:
                person.stat = True
            else:
                tmp.append(person)
        self.list_person = tmp

        # Classement des piétons selon la même cible mobile suivante
        list_calcul = self.calcul()
        d = defaultdict(list)
        list_pt = []
        for i, v in enumerate(list_calcul):
            d[v[1]].append(v[0])
            if v[1] not in list_pt:
                if v[1] != ():
                    list_pt.append(v[1])

        self.list_move_pc = []
        # Résolution de conflit
        for pt in list_pt:
            # Si plusieurs piétons ont la même position suivante,
            # l'un est sélectionné au hasard pour se déplacer et
            # les autres piétons ne bougent pas.
            choice = 0
            if len(d[pt]) > 1 and pt != ():
                num = len(d[pt])
                choice = random.randint(0, num - 1)
            if pt != ():
                sor = fon.proche_sortie(d[pt][choice].position, self.map.sorties)
                d1_x = sor[0] - d[pt][choice].position[0]
                d1_y = sor[1] - d[pt][choice].position[1]
                distance1 = math.sqrt(d1_x ** 2 + d1_y ** 2)
                d2_x = sor[0] - pt[0]
                d2_y = sor[1] - pt[1]
                distance2 = math.sqrt(d2_x ** 2 + d2_y ** 2)
                # la limite pour decider le pt move ou pas
                if distance1 >= distance2 or d[pt][choice].rest > 5:
                    dir = fon.direction(d[pt][choice].position, pt)
                    self.list_move_pc.append((d[pt][choice].position, dir))
                    d[pt][choice].position = pt
                    d[pt][choice].rest = 0
                else:
                    d[pt][choice].rest += 1
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
