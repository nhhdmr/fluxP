import random
import time

import fonction
import foule
from GUI import GUI
from fonction import lire_txt


# Fonction principale
if __name__ == '__main__':
    UI = GUI()
    '''length_width, sorties, obstacles, incendies, people = fonction.lire_txt("test.txt")
    # print(length_width)
    ppp = foule.Foule(people, length_width, sorties, obstacles, incendies)
    UI.set_sortie(ppp)
    UI.set_obstacle(ppp)
    UI.Show_People(ppp)
    i = 0
    while len(ppp.list_person)!=0:
        ppp = ppp.maj()
        UI.Update_People(ppp)
        time.sleep(random.uniform(0.15, 0.25))
        UI.canvas.update()
        UI.window.update()
        for p in ppp.list_person:
            print(p.position)
        i += 1
        print(i)'''
    #UI.run()
    UI.window.mainloop()




