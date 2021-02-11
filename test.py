import random
import  fonction

pt = (9,8)
list_sot = [(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(0,17),(0,18),(0,19),(0,20),(0,21),(10,0),(11,0),(12,0),(13,0),(14,0)]

res = fonction.proche_sortie(pt,list_sot)
print(res)

'''for i in range(35,66):
    x = i
    y = 60
    print(str(x) + ',' + str(y))'''

'''for i in range(0,150):
    x = random.randint(2,98)
    y = random.randint(2,18)
    print(str(x) + ',' + str(y))
    #print(i)

for i in range(0,150):
    x = random.randint(2,98)
    y = random.randint(42,58)
    print(str(x) + ',' + str(y))
    #print(i)

for i in range(0,100):
    x = random.randint(2,34)
    y = random.randint(20,40)
    print(str(x) + ',' + str(y))'''
    #print(i)

'''for i in range(0,100):
    x = random.randint(68,98)
    y = random.randint(20,40)
    print(str(x) + ',' + str(y))'''

'''for i in range(0,100):
    x = random.randint(68,98)
    y = random.randint(20,40)
    print(str(x) + ',' + str(y))
    if not (65<=x<=75 and 25<=y<=35) :
        if not (65<=x<=70 and 20<=y<=23):
            if not (65<=x<=70 and 37<=y<=40):
                print(str(x) + ',' + str(y))''
    #print(i)'''

'''point = (8,7)
if 0 < point[0] < 9 and 0 < point[1] < 8:
    print(True)
else:
    print(False)'''

'''person = foule.Person(1,2,3)
list_voisin = []
list_voisin.append((person.position[0] + 1, person.position[1] - 1))
list_voisin.append((person.position[0] + 1, person.position[1]))
list_voisin.append((person.position[0] + 1, person.position[1] + 1))
list_voisin.append((person.position[0], person.position[1] + 1))
list_voisin.append((person.position[0] - 1, person.position[1] + 1))
list_voisin.append((person.position[0] - 1, person.position[1]))
list_voisin.append((person.position[0] - 1, person.position[1] - 1))
list_voisin.append((person.position[0], person.position[1] - 1))

print(list_voisin)'''

'''point = (10,12)
list_obstacle = [[(1,2),(3,3)],[(8,8),(12,15)]]
tmp = False
for obstacle in list_obstacle:
    if obstacle[0][0] <= point[0] <= obstacle[1][0] and obstacle[0][1] <= point[1] <= obstacle[1][1]:
        tmp = True
print(tmp)'''

'''list = [(2,3),(1,1)]
print(len(list))'''

#from collections import defaultdict

'''a = [(1,2), (1,2), (3, 1), (2, 3),(2,3),(0,4)]
d = defaultdict(list)
for i, v in enumerate(a):
    d[v].append(i)
print(d)

for s in d:
    print(d[s])'''

'''a = []
a.append((foule.Person(1, 2, 3), (1, 3)))
a.append((foule.Person(2, 3, 5), (2, 10)))
a.append((foule.Person(3, 1, 8), (2, 5)))
a.append((foule.Person(4, 10, 2), (2, 5)))
a.append((foule.Person(5, 4, 3), (9, 9)))
a.append((foule.Person(6, 9, 6), (5, 10)))
a.append((foule.Person(7, 5, 7), (2, 5)))
a.append((foule.Person(8, 11, 12), (1, 3)))
# a = [(1,2), (1,2), (3, 1), (2, 3),(2,3),(0,4)]

d = defaultdict(list)
list_pt = []
for i, v in enumerate(a):
    d[v[1]].append(v[0])
    if v[1] not in list_pt:
        list_pt.append(v[1])
    # print(d[v[1]])
print(d)
# print(d[2,5][2].position)
# d[2,5][2].position=(2,5)
# print(d[2,5][2].position)
# print(list_pt)
# print(d[list_pt[0]])
for pt in list_pt:
    if len(d[pt]) == 1:
        cc=1
        #print(d[pt][0].position)
    else:
        num = len(d[pt])
        print(num)
        choice = random.randint(0, num -1)
        print(choice)'''

'''import fonction
import foule
length_width, sorties, obstacles, incendies, people = fonction.lire_txt("test.txt")
# print(length_width)
ppp = foule.Foule(people,length_width,sorties,obstacles,incendies)
ppp.run()
'''

'''for i in range(0,200):
    x = random.randint(1,99)
    y = random.randint(1,59)
    print(str(x) + ',' + str(y))'''

'''for i in range(0,300):
    x = random.randint(2,40)
    y = random.randint(2,28)
    print(str(x) + ',' + str(y))'''