import random
import time
from tkinter import *
import tkinter.filedialog
import seaborn as sns
import matplotlib.pyplot as plt
import fonction
import foule_ca
import foule_sf


# La classe GUI
class GUI:
    # Taux d'agrandissement graphique.
    Pic_Ratio = 5

    # Constructeur
    def __init__(self):
        self.foule = None
        self.etat = True
        self.ini = False

        # Interface principale
        self.window = Tk()
        self.window.title('Simulation')
        self.window.geometry('700x500')
        # Le button Initialiser
        self.button_ini = Button(self.window, text='Initialiser', command=self.f_ini1)
        self.button_ini.place(x=10, y=10)
        # Zone d'affichage de l'animation de simulation
        self.canvas = Canvas(self.window, height=350, width=600, bg='grey')
        # self.canvas = Canvas(self.window,height=80, width=110, bg='grey')
        self.canvas.place(x=50, y=50)
        # Le button pour lancer l'animation
        self.button_lancer = Button(self.window, text='Lancer', command=self.run)
        self.button_lancer.place(x=50, y=450)
        # Le button pour suspendre l'animation
        self.button_suspendre = Button(self.window, text='Suspendre', command=self.pause)
        self.button_suspendre.place(x=125, y=450)
        # Le button pour continuer l'animation
        self.button_continuer = Button(self.window, text="Continuer", command=self.resume)
        self.button_continuer.place(x=220, y=450)
        # Le button pour arreter l'animation
        self.button_arreter = Button(self.window, text='Arrêter', command=self.stop)
        self.button_arreter.place(x=320, y=450)
        # Le button pour accelerer l'animation
        self.button_accelerer = Button(self.window, text='Accélérer ')
        self.button_accelerer.place(x=460, y=450)
        # Le button pour ralentir l'animation
        self.button_ralentir = Button(self.window, text='Ralentir')
        self.button_ralentir.place(x=550, y=450)

        # le fichier et modele choisis
        self.txt_nom = StringVar()
        self.model = StringVar()

    # importer un fichier pour initialiser la simulation
    def upload(self):
        select_file_name = tkinter.filedialog.askopenfilename(title='Choisir un fichier', filetypes=[('TXT', '*.txt')],
                                                              initialdir='/Users/mr/Desktop/test')
        if select_file_name != '':
            self.txt_nom.set(select_file_name)
        # return select_file_name

    # La fonction pour annuler l'initialisation
    def annuler(self):
        self.model = StringVar()
        self.txt_nom = StringVar()

    # L'interface pour choisir un modele
    def f_ini1(self):
        window_ini1 = Toplevel(self.window)
        window_ini1.geometry('300x200')
        window_ini1.title('choisir un modèle')

        # Bouton radio
        r1 = Radiobutton(window_ini1, text='Automates Cellulaires', variable=self.model, value='AC')
        r1.place(x=50, y=50)
        r2 = Radiobutton(window_ini1, text='Modèle de force sociale', variable=self.model, value='MFS')
        r2.place(x=50, y=80)

        # Bouton oui et annuler
        command1 = lambda: [self.f_ini2(), window_ini1.destroy()]
        button_oui = Button(window_ini1, text='Oui', command=command1)
        button_oui.place(x=80, y=130)
        command2 = lambda: [self.annuler(), window_ini1.destroy()]
        button_annuler = Button(window_ini1, text='Annuler', command=command2)
        button_annuler.place(x=180, y=130)

    # L'interface pour importer le fichier
    def f_ini2(self):
        window_ini2 = Toplevel(self.window)
        window_ini2.geometry('300x200')
        window_ini2.title('Initialiser')

        # L'affichage du modele choisi
        Label(window_ini2, text='Modèle sélectionné:  ' + self.model.get()).place(x=30, y=20)
        Label(window_ini2, text='importer un fichier:').place(x=30, y=50)
        # Bouton importer
        button_importer = Button(window_ini2, text='importer', command=self.upload)
        button_importer.place(x=180, y=50)
        # L'affichage du fichier choisi
        Label(window_ini2, text='Fichier sélectionné:  ').place(x=30, y=90)
        Label(window_ini2, textvariable=self.txt_nom).place(x=100, y=125)

        # Bouton oui et annuler
        # command1 = lambda: [window_ini2.destroy(), self.change_radio(), self.init()]
        command1 = lambda: [window_ini2.destroy(), self.init()]
        button_oui = Button(window_ini2, text='Oui', command=command1)
        button_oui.place(x=80, y=160)
        command2 = lambda: [self.annuler(), window_ini2.destroy()]
        button_annuler = Button(window_ini2, text='Annuler', command=command2)
        button_annuler.place(x=180, y=160)

    # Dessiner des obstacles
    def set_obstacle(self, foule):
        for (A, B) in foule.map.zone_obstacale:
            x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="red")
        '''for (x, y) in foule.map.list_obstacle:
            sx, sy = x - 1, y - 1
            ex, ey = x + 1, y + 1
            [sx, sy, ex, ey] = map(lambda x: x * GUI.Pic_Ratio, [sx, sy, ex, ey])
            self.canvas.create_rectangle(sx, sy, ex, ey, fill="red", outline="blue")'''

    # Dessiner des sorties
    def set_sortie(self, foule):
        for (x, y) in foule.map.sorties:
            sx, sy = x - 1, y - 1
            ex, ey = x + 1, y + 1
            [sx, sy, ex, ey] = map(lambda x: x * GUI.Pic_Ratio, [sx, sy, ex, ey])
            self.canvas.create_rectangle(sx, sy, ex, ey, fill="green", outline="green")

    # Dessiner des pts incendies
    def set_incendie(self, foule):
        for (x, y) in foule.map.incendies:
            sx, sy = x - 1, y - 1
            ex, ey = x + 1, y + 1
            [sx, sy, ex, ey] = map(lambda x: x * GUI.Pic_Ratio, [sx, sy, ex, ey])
            self.canvas.create_rectangle(sx, sy, ex, ey, fill="pink", outline="pink")

    # Mettre à jour la position des piétons sur le graphique
    def update_people(self, foule):
        for p in foule.list_person:
            self.canvas.delete(p.name())
        self.show_people(foule)

    # Dessiner des piétons
    def show_people(self, foule):
        for per in foule.list_person:
            ox, oy = per.position[0], per.position[1]
            x1, y1 = ox - 0.5, oy - 0.5
            x2, y2 = ox + 0.5, oy + 0.5
            [x1, y1, x2, y2] = map(lambda x: x * GUI.Pic_Ratio, [x1, y1, x2, y2])
            self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", tag=per.name())

    # Calculer le ratio d'affichage
    '''def change_radio(self):
        length_width, wall, sorties, obstacles, incendies, people = fonction.lire_txt(self.txt_nom.get())
        # self.Pic_Ratio = min(600/length_width[0],350/length_width[1])'''

    # Desiner l'etat d'initialisation
    def init(self):
        if self.model.get() == '' or self.txt_nom.get() == '':
            print("Error: no model or fichier")
        else:
            length_width, wall, sorties, obstacles, incendies, people = fonction.lire_txt(self.txt_nom.get())
            print(self.txt_nom.get())
            if self.model.get() == 'AC':
                self.ini = True
                self.foule = foule_ca.Foule(people, length_width, wall, sorties, obstacles, incendies)
            if self.model.get() == 'MFS':
                self.ini = True
                self.foule = foule_sf.Foule(people, length_width, wall, sorties, obstacles, incendies)
            #else:
            #    self.ini = False
                # self.foule = foule_sf.Foule([], [], [], [], [], [])
            self.set_sortie(self.foule)
            self.set_obstacle(self.foule)
            self.set_incendie(self.foule)
            self.show_people(self.foule)

    # Lancer l'animation de simulation
    def run(self):
        if self.ini:
            # calculer le temps de simulation
            time_start = time.time()
            self.set_sortie(self.foule)
            self.set_obstacle(self.foule)
            self.show_people(self.foule)

            # MAJ la visualisation
            i = 0
            while len(self.foule.list_person) != 0:
                if self.etat:
                    self.foule = self.foule.maj()
                    self.update_people(self.foule)
                    # time.sleep(random.uniform(0.15, 0.25))
                    self.canvas.update()
                    self.window.update()
                else:
                    # time.sleep(random.uniform(0.15, 0.25))
                    self.canvas.update()
                    self.window.update()
                i += 1
                # print(i)
            # Calculer le temps de simulation
            time_pass = time.time() - time_start
            print("time:")
            print(time_pass)
            # Dessiner heat map
            sns.heatmap(self.foule.thmap.T, cmap="Reds")
            plt.axis('equal')
            plt.show()

    # Mettre la simulation en pause
    def pause(self):
        if self.ini:
            self.etat = False

    # Reprendre la simulation
    def resume(self):
        if self.ini:
            self.etat = True

    # Arreter la simulation
    def stop(self):
        if self.ini:
            self.foule.list_person = []
            self.canvas.delete(ALL)
