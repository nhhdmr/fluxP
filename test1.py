#!/usr/bin/env python
# coding: utf-8
import threading
import time

import fonction
import foule

length_width, sorties, obstacles, incendies, people = fonction.lire_txt("test2.txt")
ppp = foule.Foule(people, length_width, sorties, obstacles, incendies)
res = ppp.pos_pd
print(res[65][0])



'''class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


a = Job()
a.start()
time.sleep(3)
a.pause()
time.sleep(3)
a.resume()
time.sleep(3)
a.pause()
#time.sleep(2)
a.stop()


def pc_m_n(self, direction, person):
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    d6 = 0
    d7 = 0
    d8 = 0
    num = 0
    voisins = self.voisins(person)
    for voisins in voisins:
        for pt in self.list_move_pc:
            if pt[0][0] == voisins[0] and pt[0][1] == voisins[1]:
                num += 1
                dir = pt[1]
                if dir == 1:
                    d1 += 1
                elif dir == 2:
                    d2 += 1
                elif dir == 3:
                    d3 += 1
                elif dir == 4:
                    d4 += 1
                elif dir == 5:
                    d5 += 1
                elif dir == 6:
                    d6 += 1
                elif dir == 7:
                    d7 += 1
                elif dir == 8:
                    d8 += 1
    if direction == 1:
        return (d1, num)
    elif direction == 2:
        return (d2, num)
    elif direction == 3:
        return (d3, num)
    elif direction == 4:
        return (d4, num)
    elif direction == 5:
        return (d5, num)
    elif direction == 6:
        return (d6, num)
    elif direction == 7:
        return (d7, num)
    elif direction == 8:
        return (d8, num)

    def pc_m_n(self, person):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        d5 = 0
        d6 = 0
        d7 = 0
        d8 = 0
        num = 0
        voisins = self.voisins(person)
        for voisins in voisins:
            for pt in self.list_move_pc:
                if pt[0][0]==voisins[0] and pt[0][1]==voisins[1]:
                    num += 1
                    dir = pt[1]
                    if dir == 1:
                        d1 += 1
                    elif dir == 2:
                        d2 += 1
                    elif dir == 3:
                        d3 += 1
                    elif dir == 4:
                        d4 += 1
                    elif dir == 5:
                        d5 += 1
                    elif dir == 6:
                        d6 += 1
                    elif dir == 7:
                        d7 += 1
                    elif dir == 8:
                        d8 += 1
        return (num,d1,d2,d3,d4,d5,d6,d7,d8)'''