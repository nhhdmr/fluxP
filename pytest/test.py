import math
from math import fabs, sqrt
import pytest
import fonction as fon
import foule_ca
import foule_sf
import map


# test de la fonction lire_txt dans fonction.py
def test_lire_txt():
    res = fon.lire_txt('pytest/test.txt')
    assert res == [(50,30),[[(0, 49)], [(0, 29)], [(0, 49)], [(0, 3), (7, 29)]],[(0,6),(0,5),(0,4)],[[(5,5),(8,4)]],[(10,10)],[(8,2),(10,6)]]


# test de la fonction g dans fonction.py
def test_g():
    assert fon.g(-3) == 0
    assert fon.g(3) == 3


# test de la fonction direction dans fonction.py
def test_direction1():
    assert fon.direction((5,5),(6,6)) == 3


# test de la fonction direction dans fonction.py
def test_direction2():
    assert fon.direction((5,5),(5,5)) == 0


# test de la fonction proche_sortie dans fonction.py
def test_pro_sor():
    pt = (8,7)
    list_sortie = [(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(7,0),(8,0)]
    assert fon.proche_sortie(pt,list_sortie) == (8,0)


# test de la fonction pd dans fonction.py
def test_pd1():
    pt = (12,13)
    sor = (15,0)
    assert fabs(fon.pd(pt,sor) - sqrt(1/178)) < 0.00000001


# test de la fonction pd dans fonction.py
def test_pd2():
    pt = (15,0)
    sor = (15,0)
    assert fon.pd(pt,sor) == 9999


# test de la fonction pc dans fonction.py
def test_pc1():
    assert fon.pc(15,30) == 0.5


# test de la fonction pc dans fonction.py
def test_pc2():
    assert fon.pc(15,0) == 0


# test de la fonction pr dans fonction.py
def test_pr1():
    assert fon.pr(0) == 0


# test de la fonction pr dans fonction.py
def test_pr2():
    assert fabs(fon.pr(1) - 0.462117157) < 0.00000001


# test de la fonction pf dans fonction.py
def test_pf1():
    assert fon.pf(0) == 0


# test de la fonction pf dans fonction.py
def test_pf2():
    assert fabs(fon.pf(1) - 0.231058578) < 0.00000001


# test de la fonction pfire dans fonction.py
def test_pfire():
    pt = (13,5)
    sor = (8,0)
    inc = (20,20)
    assert fabs(fon.pfire(pt,sor,inc) - 0.29029832 ) < 0.00000001


# test de la fonction range_obstacle dans map.py
def test_ran_obs1():
    assert map.range_obstacle((23,15),(7,22)) == ((7,15),(23,22))


# test de la fonction range_obstacle dans map.py
def test_ran_obs2():
    assert map.range_obstacle((23,99),(7,22)) == ((7,22),(23,99))


# test de la classe map dans map.py
def test_map():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = map.map(length_width, wall, sorties, obstacles, incendies)
    assert res.length == 50
    assert res.width == 30
    assert res.wall == [[(0, 49)], [(0, 29)], [(0, 49)], [(0, 3), (7, 29)]]
    assert res.sorties == [(0,6),(0,5),(0,4)]
    assert res.incendies == [(10,10)]
    assert res.zone_obstacale == [((5,4),(8,5))]
    assert (0,29) in res.list_obstacle
    assert (6,5) in res.list_obstacle


# test de la classe person dans foule_ca.py
def test_per_ca():
    res = foule_ca.Person(2, 21, 22)
    assert res.id == 2
    assert res.position == (21,22)
    assert res.speed == 1
    assert res.name() == 'ID_2'


# test d'initialisation de la classe foule dans foule_ca.py
def test_foule_ca():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.map.length == 50
    assert res.map.width == 30
    assert res.map.wall == [[(0, 49)], [(0, 29)], [(0, 49)], [(0, 3), (7, 29)]]
    assert res.map.sorties == [(0, 6), (0, 5), (0, 4)]
    assert res.map.incendies == [(10, 10)]
    assert res.map.zone_obstacale == [((5, 4), (8, 5))]
    assert (0, 29) in res.map.list_obstacle
    assert (6, 5) in res.map.list_obstacle
    assert len(res.list_person) == 2
    assert res.list_person[0].id == 1
    assert res.list_person[0].position == (8,2)
    assert res.list_person[1].id == 2
    assert res.list_person[1].position == (10, 6)
    assert res.pos_pd[4][1] == 0.2
    assert res.pos_pd[10][6] == 0.1


# test de la fonction addMapValue de la classe foule dans foule_ca.py
def test_amv_ca():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.addMapValue(res.thmap,10,11)
    assert res.thmap[10][11] == 1
    assert res.thmap[1][1] == 0


# test de la fonction point_in_zone de la classe foule dans foule_ca.py
def test_piz_ca():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.point_in_zone((12,13))
    assert not res.point_in_zone((52,6))


# test de la fonction voisins de la classe foule dans foule_ca.py
def test_voi():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    list = res.voisins(res.list_person[0])
    assert list == [(9,1),(9,2),(9,3),(8,3),(7,3),(7,2),(7,1),(8,1)]
    per = foule_ca.Person(3, 9, 5)
    list = res.voisins(per)
    #print(list)
    assert list == [(10,4),(10,5),(9,6),(8,6),(9,4)]


# test de la fonction point_stat de la classe foule dans foule_ca.py
def test_pt_st():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.point_stat((8,2))
    assert not res.point_stat((13,12))


# test de la fonction point_obstacle de la classe foule dans foule_ca.py
def test_pt_obs():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert not res.point_obstacle((12,13))
    assert res.point_obstacle((7,5))


# test de la fonction calcul_gamma de la classe foule dans foule_ca.py
def test_cal_gam():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.calcul_gamma((9,5)) == 2
    assert res.calcul_gamma((15,5)) == -1


# test de la fonction pc_m_n de la classe foule dans foule_ca.py
def test_pcmn():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.list_move_pc = [((9,2),1),((9,1),1)]
    assert res.pc_m_n(res.list_person[0]) == [2,2,0,0,0,0,0,0,0]
    assert res.pc_m_n(res.list_person[1]) == [0,0,0,0,0,0,0,0,0]


# test de la fonction calcul de la classe foule dans foule_ca.py
def test_calcul_ca():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    list = res.calcul()
    assert list[0][0].position == (8,2)
    assert list[0][1] == (7, 2)
    assert list[1][0].position == (10, 6)
    assert list[1][1] == (9, 7)


# test de la fonction maj de la classe foule dans foule_ca.py
def test_maj_ca():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.maj()
    assert res.list_person[0].position == (7,2)
    assert res.list_person[1].position == (9,7)
    assert res.list_move_pc == [((8,2),6),((10,6),5)]


# test de la classe person dans foule_sf.py
def test_per_sf():
    res = foule_sf.Person(2, 21, 22)
    assert res.id == 2
    assert res.position == (21,22)
    assert res.dt == 0.05
    assert res.poids == 50
    assert res.rayon == 0.2
    assert res.vitesse_esp == 1
    assert res.v == (0, 0)
    assert res.a == (0, 0)
    assert res.destination == (0, 0)
    assert res.name() == 'ID_2'


# test d'initialisation de la classe foule dans foule_sf.py
def test_foule_mfs():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.map.length == 27
    assert res.map.width == 17
    assert res.map.wall == [[(0, 26)], [(0, 3),(5,16)], [(0, 26)], [(0, 16)]]
    assert res.map.sorties == [(26,4)]
    assert res.map.incendies == []
    assert res.map.zone_obstacale == [((5, 4), (8, 5))]
    assert (0, 15) in res.map.list_obstacle
    assert (6, 4) in res.map.list_obstacle
    assert len(res.list_person) == 2
    assert res.list_person[0].id == 1
    assert res.list_person[0].position == (1.5, 15.5)


# test de la fonction addMapValue de la classe foule dans foule_sf.py
def test_amv_sf():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.addMapValue(res.thmap,22,10)
    assert res.thmap[22][10] == 1
    assert res.thmap[2][2] == 0


# test de la fonction point_in_zone de la classe foule dans foule_sf.py
def test_piz_sf():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.point_in_zone((11,10))
    assert not res.point_in_zone((60,10))


# test de la fonction force_mur de la classe foule dans foule_sf.py
def test_force_mur():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    for_mur = res.force_mur(res.list_person[0])
    assert for_mur[0] == 2000.0
    assert fabs(for_mur[1] - (-13.47589)) < 0.00001


# test de la fonction force_obs de la classe foule dans foule_sf.py
def test_force_obs():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    for_obs = res.force_obs(res.list_person[1],res.map.zone_obstacale[0])
    assert for_obs[0] == 0
    assert fabs(for_obs[1] - (-164.17000)) < 0.00001


# test de la fonction calcul_a de la classe foule dans foule_sf.py
def test_cal_a():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.calcul_a()
    assert fabs(res.list_person[0].a[0] - (58.10474)) < 0.00001
    assert fabs(res.list_person[0].a[1] - (-8.76766)) < 0.00001


# test de la fonction move de la classe foule dans foule_sf.py
def test_move():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.calcul_a()
    res.move()
    assert fabs(res.list_person[0].v[0] - (0.29052)) < 0.00001
    assert fabs(res.list_person[0].v[1] - (-0.04384)) < 0.00001
    assert fabs(res.list_person[0].position[0] - (1.50182)) < 0.00001
    assert fabs(res.list_person[0].position[1] - (15.49973)) < 0.00001


# test de la fonction maj de la classe foule dans foule_sf.py
def test_maj_sf():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('pytest/MFS_ex copy.txt')
    res = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.maj()
    assert fabs(res.list_person[1].v[0] - (0.09988)) < 0.00001
    assert fabs(res.list_person[1].v[1] - (-0.01131)) < 0.00001
    assert fabs(res.list_person[1].position[0] - (6.00062)) < 0.00001
    assert fabs(res.list_person[1].position[1] - (2.99993)) < 0.00001


if __name__ == '__main__':
       pytest.main(["-s","pytest/test.py"])

