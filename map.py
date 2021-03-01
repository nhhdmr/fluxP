# Ajustez la représentation de la zone d'obstacles.
def range_obstacle(A, B):
    if A[0] > B[0]:
        A, B = B, A
    x1, y1 = A[0], A[1]
    x2, y2 = B[0], B[1]
    if y1 < y2:
        return ((x1, y1), (x2, y2))
    else:
        return ((x1, y2), (x2, y1))


# La classe Map
class map:
    #Constructeur
    def __init__(self, l_w, wall, sorties, obstacles, incendies):
        self.length = l_w[0]
        self.width = l_w[1]
        self.wall = wall
        self.sorties = sorties
        self.incendies = incendies
        self.zone_obstacale = []
        self.list_obstacle = []

        # initialiser les obstacles
        for i in range(0,self.length):
            self.list_obstacle.append((i,0))
            self.list_obstacle.append((i,l_w[1]-1))

        for i in range(1,self.width-1):
            self.list_obstacle.append((0,i))
            self.list_obstacle.append((l_w[0]-1,i))

        for obstacle in obstacles:
            A,B = range_obstacle(obstacle[0],obstacle[1])
            self.zone_obstacale.append((A, B))
            for i in range(A[0],B[0]+1):
                for j in range(A[1],B[1]+1):
                    self.list_obstacle.append((i,j))

        for sortie in self.sorties:
            if sortie in self.list_obstacle:
                self.list_obstacle.remove(sortie)
