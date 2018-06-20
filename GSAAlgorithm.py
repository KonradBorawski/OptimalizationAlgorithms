import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction

class Particle:
    x = None
    y  = None
    fitness  = None
    helpMass  = None
    activeMass  = None
    forceX  = None
    forceY  = None
    accelerationX  = None
    accelerationY = None
    velocityX  = None
    velocityY  = None

    def __init__(self,x, y, chosenFunction):
        self.x = x
        self.y = y
        self.fitness = returnChosenFunction(self.x, self.y, chosenFunction)
        self.activeMass = 0
        self.forceX = 0
        self.forceY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.velocityX = 0
        self.velocityY = 0

class ParticleGSA3D:
    range = None
    initialConstG = None
    constBeta = None
    constMaxIterations = None
    hive = None
    numberOfParticles = None
    k = None
    chosenFunction = None
    def __init__(self,range,numberOfParticles,maxIterations, chosenFunction):
        self.chosenFunction = chosenFunction
        self.range = range
        self.numberOfParticles = numberOfParticles
        self.k = numberOfParticles

        self.initialConstG = 100
        self.constBeta = 20
        self.constMaxIterations = maxIterations
        self.hive = self.createHive()


    def createHive(self):
        hive = []
        for i in range(0,self.numberOfParticles,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            hive.append(Particle(x, y,self.chosenFunction))
        return hive

    def distanceBetweenParticles(self,particle1, particle2):
        helpX = ((particle1.x - particle2.x) * (particle1.x - particle2.x))
        helpY = ((particle1.y - particle2.y) * (particle1.y - particle2.y))
        helpZ = ((particle1.fitness - particle2.fitness) * (particle1.fitness - particle2.fitness))
        return np.sqrt(helpX + helpY + helpZ)

    def doOneIteration(self,iterations):
        self.hive = sorted(self.hive, key=attrgetter('fitness'))
        self.hive.reverse()

        constG = self.initialConstG * np.exp(-self.constBeta * (iterations / self.constMaxIterations))
        delta = 0.001

        if (iterations % 1) == 0:
            if self.k > 3:
                self.k -= 1
        helpMassSum = 0
        for i in range(0,self.numberOfParticles,1):
            self.hive[i].helpMass = (self.hive[i].fitness - self.hive[self.numberOfParticles - 1].fitness) / (self.hive[0].fitness - self.hive[self.numberOfParticles - 1].fitness)
            helpMassSum = helpMassSum + self.hive[i].helpMass

        for i in range(0,self.numberOfParticles,1):
            self.hive[i].activeMass = self.hive[i].helpMass / helpMassSum

        for i in range(0,self.numberOfParticles-1,1):
            self.hive[i].forceX = 0
            self.hive[i].forceY = 0

            for j in range(0, self.k, 1):
                if (i != j):
                    self.hive[i].forceX = self.hive[i].forceX + np.random.random() * constG *  ((self.hive[i].activeMass * self.hive[j].activeMass) / ((self.distanceBetweenParticles(self.hive[i], self.hive[j]) + delta))) * (self.hive[j].x - self.hive[i].x)

                    self.hive[i].forceY = self.hive[i].forceY + np.random.random() * constG *  ((self.hive[i].activeMass * self.hive[j].activeMass) / ((self.distanceBetweenParticles(self.hive[i], self.hive[j]) + delta))) * (self.hive[j].y - self.hive[i].y)
            
            self.hive[i].accelerationX = self.hive[i].forceX / self.hive[i].activeMass
            self.hive[i].accelerationY = self.hive[i].forceY / self.hive[i].activeMass
            
            self.hive[i].velocityX = (np.random.random() * self.hive[i].velocityX) + self.hive[i].accelerationX
            self.hive[i].velocityY = (np.random.random() * self.hive[i].velocityY) + self.hive[i].accelerationY
            
            if (((self.hive[i].x + self.hive[i].velocityX) < -self.range) or ((self.hive[i].x + self.hive[i].velocityX) > self.range)):
                self.hive[i].x = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].x = self.hive[i].x + self.hive[i].velocityX

            if (((self.hive[i].y + self.hive[i].velocityY) < -self.range) or ((self.hive[i].y + self.hive[i].velocityY) > self.range)):
                self.hive[i].y = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].y = self.hive[i].y + self.hive[i].velocityY

            self.hive[i].fitness = returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction)
        
    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.fitness))
