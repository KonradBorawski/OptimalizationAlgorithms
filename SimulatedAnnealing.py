import numpy as np
from testFunction import returnChosenFunction

class Particle:
    x = None
    y = None
    fitness = None

    def __init__(self,x=0, y=0, fitness=0):
        self.x = x
        self.y = y
        self.fitness = fitness

class SimulatedAnnealing3D:
    particles = None
    range = None
    maxIterations = None
    alpha = None
    T = None
    chosenFunction = None

    def __init__(self,range1, nrParticles,maxIterations, chosenFunction):
        self.chosenFunction = chosenFunction
        self.range = range1
        self.maxIterations = maxIterations
        self.hive = []
        self.alpha = 0.72
        self.T = 100

        for i in range(0,nrParticles,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            fitness = returnChosenFunction(x, y,self.chosenFunction)
            self.hive.append(Particle(x, y, fitness))

    def doOneIteration(self,iterations):
        if (iterations < self.maxIterations ):
            for i in range(0, len(self.hive),1):
                x_t_1 = self.hive[i].x + np.random.uniform(low= -1, high = 1)
                y_t_1 = self.hive[i].y + np.random.uniform(low= -1, high = 1)
                fitness_t_1 = returnChosenFunction(x_t_1, y_t_1,self.chosenFunction)
                D_F = fitness_t_1 - self.hive[i].fitness
                if(D_F < 0):
                    self.hive[i].x = x_t_1
                    self.hive[i].y = y_t_1
                    self.hive[i].fitness = fitness_t_1

                    if(self.hive[i].x > self.range or self.hive[i].x < -self.range or self.hive[i].y > self.range or self.hive[i].y < -self.range):
                        x = np.random.uniform(low= -self.range, high = self.range)
                        y = np.random.uniform(low= -self.range, high = self.range)
                        fitness = returnChosenFunction(x, y,self.chosenFunction)
                        self.hive[i] = Particle(x, y, fitness)
                else:
                    r = np.random.random()
                    if (r < np.exp(-D_F/self.T)):
                        self.hive[i].x = x_t_1
                        self.hive[i].y= y_t_1
                        self.hive[i].fitness = fitness_t_1
                        if (self.hive[i].x > self.range or self.hive[i].x < -self.range or self.hive[i].y > self.range or self.hive[i].y < -self.range):
                            x = np.random.uniform(low= -self.range, high = self.range)
                            y = np.random.uniform(low= -self.range, high = self.range)
                            fitness = returnChosenFunction(x, y,self.chosenFunction)
                            self.hive[i] = Particle(x, y, fitness)

            self.T = self.T * self.alpha