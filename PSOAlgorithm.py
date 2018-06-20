import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction

class ParticlePSO:
    x = None
    y = None
    z = None
    theBestX = None
    theBestY = None
    velocityX = None
    velocityY = None

    def __init__(self,x, y, chosenFuntion):
        self.x = x
        self.y = y
        self.z = returnChosenFunction(self.x, self.y, chosenFuntion)
        self.theBestX = x
        self.theBestY = y
        self.velocityX = 0
        self.velocityY = 0

class ParticlePSO3D:
    hive = None
    range = None
    numberOfParticles = None
    alfa = None
    beta = None
    globalBestX = None
    globalBestY = None
    globalBestZ = None
    chosenFuntion = None
    def __init__(self,range,numberOfParticles, chosenFunction):
        self.chosenFuntion = chosenFunction
        self.numberOfParticles = numberOfParticles
        self.range = range
        self.hive = self.createHive()
        self.alfa = 0.2
        self.beta = 0.2
        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.globalBestX = self.hive[0].x
        self.globalBestY = self.hive[0].y
        self.globalBestZ = self.hive[0].z

    def createHive(self):
        hive = []
        for i in range(0,self.numberOfParticles,1):
            hive.append(ParticlePSO(np.random.uniform(low= -self.range, high = self.range),np.random.uniform(low= -self.range, high = self.range),self.chosenFuntion))
        return hive;

    def doOneIteration(self, iteration):
        for i in range(0, self.numberOfParticles,1):
            self.hive[i].velocityX = np.random.random() *self.hive[i].velocityX + self.alfa * (np.random.random()) *(self.globalBestX - self.hive[i].x) +self.beta * (np.random.random()) * (self.hive[i].theBestX - self.hive[i].x)

            self.hive[i].velocityY = np.random.random() * self.hive[i].velocityY + self.alfa * (np.random.random()) *(self.globalBestY - self.hive[i].y) + self.beta * (np.random.random()) * (self.hive[i].theBestY - self.hive[i].y)

            oldZ = self.hive[i].z;
            self.hive[i].x = self.hive[i].x + self.hive[i].velocityX
            self.hive[i].y = self.hive[i].y + self.hive[i].velocityY

            if self.hive[i].x >= self.range:
                self.hive[i].x = self.range - 0.5
            elif self.hive[i].x <= -self.range:
                self.hive[i].x = -self.range + 0.5
            if self.hive[i].y >= self.range:
                self.hive[i].y = self.range - 0.5
            elif self.hive[i].y <= -self.range:
                self.hive[i].y = -self.range + 0.5

            x = self.hive[i].x
            y = self.hive[i].y
            self.hive[i].z = returnChosenFunction(x,y,self.chosenFuntion)
            if (self.hive[i].z < oldZ):
                self.hive[i].theBestX = self.hive[i].x;
                self.hive[i].theBestY = self.hive[i].y;
        self.hive = sorted(self.hive, key=attrgetter('z'))

        if (self.globalBestZ > self.hive[0].z):
            self.globalBestX = self.hive[0].x;
            self.globalBestY = self.hive[0].y;
            self.globalBestZ = self.hive[0].z;

    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.z))
