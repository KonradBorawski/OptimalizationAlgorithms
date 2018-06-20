import numpy as np
from testFunction import returnChosenFunction

class Vector2D:
    x = None
    y = None

    def __init__(self,x = 0, y = 0, vector = 0, whichConstructor = 0):
        if(whichConstructor==0):
            self.x = x
            self.y = y
        elif(whichConstructor==1):
            self.x = vector.x
            self.y = vector.y
    
class Vector3D:
    x = None
    y = None
    Fitness = None

    def __init__(self,x = 0, y = 0, fitness = 0, vector = 0, whichConstructor = 0):
        if(whichConstructor==0):
            self.x = x
            self.y = y
            self.Fitness = fitness
        elif(whichConstructor==1):
            self.x = vector.x
            self.y = vector.y
            self.Fitness = fitness

class DE3D:
    hive = None
    range = None
    maxIterations = None
    nrVectors = None
    F = None
    C = None
    chosenFunction = None
    def __init__(self, range1, nrVectors, maxIterations, chosenFunction):
        self.chosenFunction = chosenFunction
        self.maxIterations = maxIterations
        self.range = range1
        self.nrVectors = nrVectors
        self.hive = []
        self.C = 0.5
        self.F = 0.8

        for i in range(0,nrVectors,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            z = returnChosenFunction(x, y,self.chosenFunction)
            self.hive.append(Vector3D(x = x, y = y, fitness = z, whichConstructor=0))

    def doOneIteration(self,iterations):
        if (iterations < self.maxIterations):
            self.moveVectors()

    def mutation(self):
        x = None
        y = None
        Xr = Vector2D(x=0, y=0, whichConstructor=0)
        Xs = Vector2D(x=0, y=0, whichConstructor=0)
        result = Vector2D(x=0, y=0, whichConstructor=0)

        strong_fitness = max(the_best.Fitness for the_best in self.hive)
        index = 0
        for index, item in enumerate(self.hive):
            if item.Fitness == strong_fitness:
                break
            else:
                index = -1
        Xbest = Vector2D(x=self.hive[index].x, y= self.hive[index].y , whichConstructor =0)

        while True:
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            Xr = Vector2D(x = x, y = y, whichConstructor = 0)
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            Xs = Vector2D(x = x, y = y, whichConstructor = 0)
            temp = Vector2D(x = Xbest.x, y = Xbest.y, whichConstructor =0)
            temp.x = Xbest.x + self.F * (Xr.x - Xs.x)
            temp.y = Xbest.y + self.F * (Xr.y - Xs.y)
            result = Vector2D(vector = Vector2D(x = temp.x, y = temp.y, whichConstructor =0), whichConstructor=1)

            if(result.x < self.range and result.x > -self.range and result.y < self.range and result.y > -self.range):
                break

        return result

    def recombination(self,V, x_i, y_i):
        result = Vector2D(x=0, y=0, whichConstructor=0)

        p = np.random.random()
        if (p <= self.C):
            result.x = V.x
        else:
            result.x = x_i

        p = np.random.random()
        if (p <= self.C):
            result.y = V.y
        else:
            result.y = y_i

        return result

    def moveVectors(self):
        for i in range(0,len(self.hive),1):
            U = self.recombination(self.mutation(), self.hive[i].x, self.hive[i].y)
            U_fitness = returnChosenFunction(U.x, U.y,self.chosenFunction)
            if (U_fitness > self.hive[i].Fitness):
                self.hive[i] = Vector3D(vector = U, fitness = U_fitness, whichConstructor=1)