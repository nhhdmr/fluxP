from math import fabs, sqrt
import pytest
import fonction as fon
import foule_ca
import map


# test de la fonction lire_txt dans fonction.py
def test_lire_txt():
    res = fon.lire_txt('test.txt')
    assert res == [(50,30),[[(0, 49)], [(0, 29)], [(0, 49)], [(0, 3), (7, 29)]],[(0,6),(0,5),(0,4)],[[(5,5),(8,4)]],[(10,10)],[(8,2),(10,6)]]


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
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
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
def test_per():
    res = foule_ca.Person(2, 21, 22)
    assert res.id == 2
    assert res.position == (21,22)
    assert res.speed == 1
    assert res.name() == 'ID_2'


# test d'initialisation de la classe foule dans foule_ca.py
def test_foule():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
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
def test_amv():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.addMapValue(res.thmap,10,11)
    assert res.thmap[10][11] == 1
    assert res.thmap[1][1] == 0


# test de la fonction point_in_zone de la classe foule dans foule_ca.py
def test_piz():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.point_in_zone((12,13))
    assert not res.point_in_zone((52,6))


# test de la fonction voisins de la classe foule dans foule_ca.py
def test_voi():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    list = res.voisins(res.list_person[0])
    assert list == [(9,1),(9,2),(9,3),(8,3),(7,3),(7,2),(7,1),(8,1)]
    per = foule_ca.Person(3, 9, 5)
    list = res.voisins(per)
    #print(list)
    assert list == [(10,4),(10,5),(9,6),(8,6),(9,4)]


# test de la fonction point_stat de la classe foule dans foule_ca.py
def test_pt_st():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.point_stat((8,2))
    assert not res.point_stat((13,12))


# test de la fonction point_obstacle de la classe foule dans foule_ca.py
def test_pt_obs():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert not res.point_obstacle((12,13))
    assert res.point_obstacle((7,5))


# test de la fonction calcul_gamma de la classe foule dans foule_ca.py
def test_cal_gam():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    assert res.calcul_gamma((9,5)) == 2
    assert res.calcul_gamma((15,5)) == -1


# test de la fonction pc_m_n de la classe foule dans foule_ca.py
def test_pcmn():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.list_move_pc = [((9,2),1),((9,1),1)]
    assert res.pc_m_n(res.list_person[0]) == [2,2,0,0,0,0,0,0,0]
    assert res.pc_m_n(res.list_person[1]) == [0,0,0,0,0,0,0,0,0]


# test de la fonction calcul de la classe foule dans foule_ca.py
def test_calcul():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    list = res.calcul()
    assert list[0][0].position == (8,2)
    assert list[0][1] == (7, 2)
    assert list[1][0].position == (10, 6)
    assert list[1][1] == (9, 7)


# test de la fonction maj de la classe foule dans foule_ca.py
def test_maj():
    length_width, wall, sorties, obstacles, incendies, people = fon.lire_txt('test.txt')
    res = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
    res.maj()
    assert res.list_person[0].position == (7,2)
    assert res.list_person[1].position == (9,7)
    assert res.list_move_pc == [((8,2),6),((10,6),5)]


if __name__ == '__main__':
       pytest.main(["-s","test.py"])

