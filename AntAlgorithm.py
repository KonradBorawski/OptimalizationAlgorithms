import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction

class Ant:
    x = None
    y = None
    z = None
    probability = None
    pheromone = None
    distance = None
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.probability = 0
        self.pheromone = 0
        self.distance = 0

class Ant3D:
    ants = None
    maxIterations = None
    range = None
    nrAnts = None
    a_T = None
    chosenFunction = None
    def __init__(self,range1,nrAnts,maxIterations,chosenFunction):
        self.chosenFunction = chosenFunction
        self.hive = []
        self.maxIterations = maxIterations
        self.nrAnts = nrAnts
        self.range = range1
        self.a_T = 5
        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.hive.reverse()


        for i in range(0,self.nrAnts,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            z = -returnChosenFunction(x,y,self.chosenFunction)
            self.hive.append(Ant(x, y, z))

        self.initAlhorithm()

    def initAlhorithm(self):
        fiSUM = 0
        for i in range(0,self.nrAnts,1):
            self.hive[i].distance =  self.hive[i].z - self.hive[self.nrAnts-1].z
            self.hive[i].pheromone = np.exp(-np.power(self.hive[i].distance, 2) / 0.01)
            fiSUM += self.hive[i].pheromone

        for i in range(0,self.nrAnts,1):
            self.hive[i].probability = self.hive[i].pheromone / fiSUM
        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.hive.reverse()

    def doOneIteration(self,iteration):
        if (self.maxIterations >= iteration):
            for i in range(0,self.nrAnts,1):
                move_to_index = 0

                sum_range = 0
                rng_move = np.random.random()
                for j in range(0,self.nrAnts-1,1):
                    if ((rng_move >= sum_range) and (rng_move <= (sum_range + self.hive[j + 1].probability))):
                        move_to_index = j + 1
                        break

                    sum_range += np.round(self.hive[j+1].probability, 3)


                dx = np.random.uniform(low= 0, high = self.a_T)
                if (self.hive[i].x > self.hive[move_to_index].x):
                    self.hive[i].x -= dx
                elif (self.hive[i].x < self.hive[move_to_index].x):
                    self.hive[i].x += dx
                else:
                    dx = np.random.uniform(low= -self.a_T, high = self.a_T)
                    self.hive[i].x += dx

                dx = np.random.uniform(low= 0, high = self.a_T)
                if (self.hive[i].y > self.hive[move_to_index].y):
                    self.hive[i].y -= dx
                elif(self.hive[i].y < self.hive[move_to_index].y):
                    self.hive[i].y += dx
                else:
                    dx = np.random.uniform(low= -self.a_T, high = self.a_T)
                    self.hive[i].y += dx

                if (self.hive[i].y > self.range or self.hive[i].y < -self.range or self.hive[i].x > self.range or self.hive[i].x < -self.range):
                    self.hive[i].x = np.random.uniform(low= -self.range, high = self.range)
                    self.hive[i].y = np.random.uniform(low= -self.range, high = self.range)

                self.hive[i].z = -returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction)
            self.a_T *= 0.9
            self.initAlhorithm()

    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.z))