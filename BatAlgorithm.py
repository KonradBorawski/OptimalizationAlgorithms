import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction

class Bat:
    x = None
    y = None
    z = None
    velocityX = None
    velocityY = None

    frequency = None
    audibility = None
    waveLength = None
    rateOfImpulses = None

    def __init__(self,x, y, chosenFunction):
        self.x = x
        self.y = y
        self.z = returnChosenFunction(self.x, self.y,chosenFunction)
        self.velocityX = 0
        self.velocityY = 0
        self.rateOfImpulses = np.random.random()
        self.audibility = np.random.random()

class Bat3D:
    hive = None
    range = None
    numberOfBats = None
    alpha = None
    gamma = None
    globalBestX = None
    globalBestY = None
    globalBestZ = None
    frequencyMIN = None
    frequencyMAX = None

    chosenFunction = None
    def __init__(self,range,numberOfBats, chosenFunction):
        self.chosenFunction = chosenFunction
        self.numberOfBats = numberOfBats
        self.range = range
        self.hive = self.createHive()
        self.alpha = 0.9
        self.gamma = 0.9
        self.frequencyMIN = 0
        self.frequencyMAX = 10

        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.globalBestX = self.hive[0].x
        self.globalBestY = self.hive[0].y
        self.globalBestZ = self.hive[0].z

    def createHive(self):
        hive = []
        for i in range(0,self.numberOfBats,1):
            hive.append(Bat(np.random.uniform(low= -self.range, high = self.range),np.random.uniform(low= -self.range, high = self.range),self.chosenFunction))
        return hive

    def doOneIteration(self, iteration):
        for i in range(0,self.numberOfBats,1):
            self.hive[i].frequency = self.frequencyMIN + (self.frequencyMAX - self.frequencyMIN) * np.random.random()

            self.hive[i].velocityX = (self.hive[i].x - self.globalBestX) * self.hive[i].frequency * 0.1
            self.hive[i].velocityY = (self.hive[i].y - self.globalBestY) * self.hive[i].frequency * 0.1

            self.hive[i].x = self.hive[i].x - self.hive[i].velocityX
            self.hive[i].y = self.hive[i].y - self.hive[i].velocityY
            self.hive[i].z = returnChosenFunction(self.hive[i].x,self.hive[i].y,self.chosenFunction)

            if (np.random.random() < self.hive[i].audibility and returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction) < returnChosenFunction(self.globalBestX, self.globalBestY,self.chosenFunction)):
                self.hive[i].rateOfImpulses = self.hive[i].rateOfImpulses * (1 - np.exp((-1) * self.gamma * iteration))
                self.hive[i].audibility = self.alpha * self.hive[i].audibility

            self.hive = sorted(self.hive, key=attrgetter('z'))
            if (self.globalBestZ > self.hive[0].z):
                self.globalBestX = self.hive[0].x
                self.globalBestY = self.hive[0].y
                self.globalBestZ = self.hive[0].z

            if (np.random.random() > self.hive[0].rateOfImpulses):
                helpRandomX = np.random.randint(2) % 2 + 1
                helpRandomY = np.random.randint(2) % 2 + 1

                if (helpRandomX == 1):
                    randomX = (-1) * np.random.random()
                else:
                    randomX = np.random.random()

                if (helpRandomY == 1):
                    randomY = (-1) * np.random.random()
                else:
                    randomY = np.random.random()

                sumOfAudibility = 0
                for k in range(0,self.numberOfBats,1):
                    sumOfAudibility += self.hive[k].audibility

                averageAudibility = sumOfAudibility / self.numberOfBats
                self.hive[0].x = self.hive[0].x + randomX * averageAudibility
                self.hive[0].y = self.hive[0].y + randomY * averageAudibility
                self.hive[0].z =  returnChosenFunction(self.hive[0].x, self.hive[0].y,self.chosenFunction)
            
            if (self.globalBestZ > self.hive[0].z):
                self.globalBestX = self.hive[0].x
                self.globalBestY = self.hive[0].y
                self.globalBestZ = self.hive[0].z


    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.z))