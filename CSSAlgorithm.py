import numpy as np
from operator import attrgetter
from testFunction import returnChosenFunction

class Particle:
    x = None
    y = None
    z = None
    electricCharge = None
    velocityX = None
    velocityY = None
    forceX = None
    forceY = None

    def __init__(self,x,y, chosenFunction):
        self.x = x
        self.y = y
        self.z = returnChosenFunction(self.x, self.y,chosenFunction)
        self.electricCharge = 0
        self.velocityX = 0
        self.velocityY = 0

class ParticleCSS3D:
    hive = None
    range = None
    numberOfParticles = None
    theBestX = None
    theBestY = None
    theBestZ = None
    particleDiameter = None
    constRandomNumber = None
    constIterations = None
    chosenFunction = None


    def __init__(self,range,numberOfParticles,maxIterations, chosenFunction):
        self.chosenFunction = chosenFunction
        self.range = range
        self.numberOfParticles = numberOfParticles
        self.hive = self.createHive()

        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.hive.reverse()

        self.particleDiameter = 1
        self.constRandomNumber = 0.2
        self.constIterations = maxIterations

    def createHive(self):
        hive = []
        for i in range(0,self.numberOfParticles,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            hive.append(Particle(x, y,self.chosenFunction))
        return hive

    def distanceBetweenParticles3D(self,particle1,particle2):
        helpX = ((particle1.x - particle2.x) * (particle1.x - particle2.x))
        helpY = ((particle1.y - particle2.y) * (particle1.y - particle2.y))
        helpZ = ((particle1.z - particle2.z) * (particle1.z - particle2.z))
        return np.sqrt(helpX + helpY + helpZ)
        
    def doOneIteration(self,iterations):
        self.theBestX = self.hive[0].x
        self.theBestY = self.hive[0].y
        self.theBestZ = self.hive[0].z

        for i in range(0,self.numberOfParticles,1):
            self.hive[i].electricCharge = (self.hive[i].z - self.hive[self.numberOfParticles - 1].z) / (self.hive[0].z - self.hive[self.numberOfParticles - 1].z)
        helpForceX = None
        helpForceY = None
        probability = None
        alfa = None
        beta = None

        for i in range(0,self.numberOfParticles,1):
            helpForceX = 0
            helpForceY = 0
            for j in range(0,self.numberOfParticles,1):
                if (i == j):
                    continue

                if (((self.hive[i].z - self.hive[0].z)/(self.hive[j].z- self.hive[i].z) > np.random.random()) or (self.hive[j].z > self.hive[i].z) ):
                    probability = 1
                else:
                    probability = 0

                distanceBetweenParticles = self.distanceBetweenParticles3D(self.hive[i], self.hive[j])

                if (distanceBetweenParticles < self.particleDiameter):
                    alfa = 1
                    beta = 0
                else:
                    alfa = 0
                    beta = 1

                helpForceX += ((alfa * self.hive[j].electricCharge / np.power(self.particleDiameter, 3) * distanceBetweenParticles) + (beta * self.hive[j].electricCharge / np.power(distanceBetweenParticles, 2))) * self.particleDiameter * distanceBetweenParticles * probability * (self.hive[j].x - self.hive[i].x)

                helpForceY += ((alfa * self.hive[j].electricCharge / np.power(self.particleDiameter, 3) * distanceBetweenParticles) + (beta * self.hive[j].electricCharge / np.power(distanceBetweenParticles, 2))) * self.particleDiameter * distanceBetweenParticles * probability * (self.hive[j].y - self.hive[i].y)
                



            self.hive[i].forceX = self.hive[i].electricCharge * helpForceX
            self.hive[i].forceY = self.hive[i].electricCharge * helpForceY
                
            oldX = self.hive[i].x
            oldY = self.hive[i].y

            newX = (self.hive[i].x + 0.5 * (1 - iterations / self.constIterations) * np.random.random() * self.hive[i].velocityX) + (0.5 * np.random.random() * (1 + iterations / self.constIterations) * self.hive[i].forceX)

            newY = (self.hive[i].y + 0.5 * (1 - iterations / self.constIterations) * np.random.random() * self.hive[i].velocityY) + (0.5 * np.random.random() * (1 + iterations / self.constIterations) * self.hive[i].forceY)

            if (((newX + self.hive[i].velocityX) < -self.range) or ((newX + self.hive[i].velocityX) > self.range)):
                self.hive[i].x = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].x = newX

            if (((newY + self.hive[i].velocityY) < -self.range) or ((newY + self.hive[i].velocityY) > self.range)):
                self.hive[i].y = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].y = newY

                
            self.hive[i].velocityX = self.hive[i].x - oldX
            self.hive[i].velocityY = self.hive[i].y - oldY

            self.hive[i].z = returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction)
        self.hive = sorted(self.hive, key=attrgetter('z'))
        self.hive.reverse()

    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.z))