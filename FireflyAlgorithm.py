import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction
    
class Firefly:
    x = None
    y = None
    lightIntensity = None
    attractiveness = None
        
    def __init__(self,x, y, chosenFunction):
        self.x = x
        self.y = y
        self.lightIntensity = returnChosenFunction(self.x, self.y,chosenFunction)
        self.attractiveness = 1

class Firefly3D:
    range = None
    alfa = None
    hive = None
    numberOfFireflies = None
    absorptionCoefficientOfLight = None
    chosenFunction = None
    def __init__(self,range,numberOfFireflies, chosenFunction):
        self.chosenFunction = chosenFunction
        self.alfa = 0.2
        self.range = range
        self.numberOfFireflies = numberOfFireflies
        self.absorptionCoefficientOfLight = 1
        self.hive = self.createHive()

    def createHive(self):
        hive = []
        for i in range(0,self.numberOfFireflies,1):
            hive.append(Firefly(np.random.uniform(low= -self.range, high = self.range),np.random.uniform(low= -self.range, high = self.range),self.chosenFunction))
        return hive;

    def distanceBetweenFireflies3D(self,firefly1, firefly2):
        helpX = ((firefly1.x - firefly2.x) * (firefly1.x - firefly2.x))
        helpY = ((firefly1.y - firefly2.y) * (firefly1.y - firefly2.y))
        helpZ = ((firefly1.lightIntensity - firefly2.lightIntensity) * (firefly1.lightIntensity - firefly2.lightIntensity))
        return np.sqrt(helpX + helpY + helpZ)

    def calculateLightIntensity(self,firefly, distance):
        return firefly.lightIntensity * np.exp(((-1) * self.absorptionCoefficientOfLight * distance * distance))

    def calculateBeta(self, firefly, distance):
        return firefly.attractiveness * np.exp(((-1) * self.absorptionCoefficientOfLight * distance * distance))

    def doOneIteration(self, iteration):
        for i in range(0,self.numberOfFireflies,1):
            for j in range(0,self.numberOfFireflies,1):
                if (i == j):
                    continue

                distance = self.distanceBetweenFireflies3D(self.hive[i], self.hive[j])

                if (self.calculateLightIntensity(self.hive[i], distance) < self.calculateLightIntensity(self.hive[j], distance)):
                    attractivenessTemp = self.calculateBeta(self.hive[i], distance)
                    self.alfa = 0.2 * np.power(np.random.random(),iteration)

                    if (attractivenessTemp < 0.000000000001):
                        self.hive[i].x = self.hive[i].x + self.alfa * (np.random.random() - 0.5)
                        self.hive[i].y = self.hive[i].y + self.alfa * (np.random.random() - 0.5)
                    else:
                        self.hive[i].x = self.hive[i].x + attractivenessTemp * (self.hive[j].x - self.hive[i].x) + self.alfa * (np.random.random() )
                        self.hive[i].y = self.hive[i].y + attractivenessTemp * (self.hive[j].y - self.hive[i].y) + self.alfa * (np.random.random() )

                    if self.hive[i].x >= self.range:
                        self.hive[i].x = self.range - 0.5
                    elif self.hive[i].x <= -self.range:
                        self.hive[i].x = -self.range + 0.5
                        
                    if self.hive[i].y >= self.range:
                        self.hive[i].y = self.range - 0.5
                    elif self.hive[i].y <= -self.range:
                        self.hive[i].y = -self.range + 0.5

                    self.hive[i].lightIntensity = returnChosenFunction(self.hive[i].x,self.hive[i].y,self.chosenFunction)
        self.hive = sorted(self.hive, key=attrgetter('lightIntensity'))
        self.hive.reverse()


    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.lightIntensity))

