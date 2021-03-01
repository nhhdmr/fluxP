import sys
import re
import numpy as np
import math


# la fonction pour obtenir les données de fichier.
def lire_txt(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    tmp = 0
    length_width = (0, 0)
    wall = []
    sortie = []
    obstacle = []
    incendie = []
    foule = []
    # traiter les contenues de fichier et stocker les données
    for line in lines:
        line = re.split(",|;|\n", line)
        if line[0] == 'longueur_largeur:':
            tmp = 1
        elif line[0] == 'Wall:':
            tmp = 2
        elif line[0] == 'Sortie:':
            tmp = 3
        elif line[0] == 'Obstacle:':
            tmp = 4
        elif line[0] == 'Incendie:':
            tmp = 5
        elif line[0] == 'Foule:':
            tmp = 6
        else:
            if tmp == 1:
                length_width = (int(line[0]), int(line[1]))
            elif tmp == 2:
                w = []
                for i in range(0, int((len(line)-1)/2)):
                    wall_s = (int(line[2*i]),int(line[2*i+1]))
                    w.append(wall_s)
                wall.append(w)
                #wall.append((int(line[0]), int(line[1])))
            elif tmp == 3:
                sortie.append((int(line[0]), int(line[1])))
            elif tmp == 4:
                obstacle.append([(int(line[0]), int(line[1])), (int(line[2]), int(line[3]))])
            elif tmp == 5:
                incendie.append((int(line[0]), int(line[1])))
            elif tmp == 6:
                foule.append((float(line[0]), float(line[1])))
    print("nb per:")
    print(len(foule))
    return [length_width, wall, sortie, obstacle, incendie, foule]


# Déterminer la direction du mouvement des piétons 1-8
# 0 s'il reste en place
def direction(pt_or, pt_des):
    x = pt_des[0] - pt_or[0]
    y = pt_des[1] - pt_or[1]
    if (x, y) == (1, -1):
        return 1
    elif (x, y) == (1, 0):
        return 2
    elif (x, y) == (1, 1):
        return 3
    elif (x, y) == (0, 1):
        return 4
    elif (x, y) == (-1, 1):
        return 5
    elif (x, y) == (-1, 0):
        return 6
    elif (x, y) == (-1, -1):
        return 7
    elif (x, y) == (0, -1):
        return 8
    else:
        return 0


# Calculez la sortie la plus proche
def proche_sortie(point, list_sortie):
    tmp = 9999
    sor = ()
    for sortie in list_sortie:
        d_x = sortie[0] - point[0]
        d_y = sortie[1] - point[1]
        # calculer la distance entre le point et la sortie
        distance = math.sqrt(d_x ** 2 + d_y ** 2)
        # conserver la distance plus petit
        if distance < tmp:
            tmp = distance
            sor = sortie
    return sor


# Formule de calcul de l'attractivité de sortie.
def pd(point, sortie):
    vector1 = np.array([point[0], point[1]])
    vector2 = np.array([sortie[0], sortie[1]])
    # calculer la distance entre le point et la sortie
    op = np.linalg.norm(vector1 - vector2)
    if op == 0:
        res = 9999
    else:
        res = 1 / op
    return res


# La formule pour calculer l'attractivité des foules.
def pc(m, n):
    if n == 0:
        return 0
    else:
        return m / n


# La formule pour calculer la force répulsive entre les personnes et les obstacles
def pr(g):
    e = math.e
    # v : la vitesse
    # g: gamma -> Coefficient de dureté de répulsion
    v = 1.0
    res = (1 - pow(e, -g * v)) / (1 + pow(e, -g * v))
    return res


# La formule de calcul du frottement
def pf(g):
    # l: lambda -> Coefficient de friction
    l = 0.5
    return l * pr(g)


# La formule de calcul de la répulsion du feu
def pfire(point, sortie, incendie):
    vector1 = np.array([sortie[0], sortie[1]])
    vector2 = np.array([incendie[0], incendie[1]])
    vector3 = np.array([point[0], point[1]])
    # la distance entre sortie et incendie
    op1 = np.linalg.norm(vector1 - vector2)
    # la distance entre point et incendie
    op2 = np.linalg.norm(vector3 - vector2)
    return 1 - op2 / op1


def g(x):
    return np.max(x, 0)