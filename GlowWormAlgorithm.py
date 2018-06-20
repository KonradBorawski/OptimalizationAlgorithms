import numpy as np
from testFunction import returnChosenFunction

class Glowworm:
    x = None
    y = None
    fitness = None
    sensorRange = None
    luciferin = None
    moveProbability = None

    def __init__(self, x = 0, y = 0, fitness = 0, sensor_range = 0, luciferin = 0):
        self.x = x
        self.y = y
        self.fitness = fitness
        self.sensorRange = sensor_range
        self.luciferin = luciferin
        self.moveProbability = 0

class GlowWorm3D:
    alpha = None
    beta = None
    gamma = None
    s = None
    n_t = None
    r_max = None
    hive = None
    range = None
    nrGlowworms = None
    maxIterations = None
    chosenFunction = None
    def __init__(self, range1, nrGlowworms,maxIterations, chosenFunction):
        self.chosenFunction = chosenFunction
        self.maxIterations = maxIterations
        self.range = range1
        self.hive = []
        self.nrGlowworms = nrGlowworms
        self.alpha = 0.4
        self.beta = 0.08
        self.gamma = 0.6
        self.r_max = (2 * self.range) / float(3)
        self.s = self.range / float(((self.range*self.range + 2)))
        self.n_t = 5

        for i in range(0,self.nrGlowworms,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            fitness = returnChosenFunction(x, y,self.chosenFunction)
            sensor_range = (2*self.range) / float(4)
            self.hive.append(Glowworm(x = x, y = y, fitness = fitness, sensor_range = sensor_range ,luciferin = 5))

    def doOneIteration(self, iterations):
        if (iterations < self.maxIterations):
            self.updateLuciferin()
            self.moveGlowworms()

    def updateLuciferin(self):
        for i in range(0,self.nrGlowworms,1):
            self.hive[i].luciferin = (float(1) - self.alpha) * self.hive[i].luciferin + (self.gamma * self.hive[i].fitness)

    def moveGlowworms(self):
        for i in range(0,self.nrGlowworms,1):
            i_neighbours = []
            i_neighbours_luciferin_sum = 0
            for j in range(0,self.nrGlowworms,1):
                if (i != j):
                    d = self.distanceBetweenGlowworms(self.hive[i], self.hive[j])

                    if ((d < self.hive[i].sensorRange) and (self.hive[i].luciferin < self.hive[j].luciferin)):
                        i_neighbours.append(self.hive[j])
                        i_neighbours_luciferin_sum += (self.hive[j].luciferin - self.hive[i].luciferin)

            for j in range(0,len(i_neighbours),1):
                i_neighbours[j].moveProbability = (i_neighbours[j].luciferin - self.hive[i].luciferin) / i_neighbours_luciferin_sum

            i_to_j_glowworm_index = self.getRandomBestGlowwormIndex(i_neighbours)

            if (i_to_j_glowworm_index != -1):
                i_j_difference_X = self.hive[i_to_j_glowworm_index].x - self.hive[i].x
                self.hive[i].x += self.s * (i_j_difference_X / np.abs(i_j_difference_X))

                i_j_difference_Y = self.hive[i_to_j_glowworm_index].y - self.hive[i].y
                self.hive[i].y += self.s * (i_j_difference_Y / np.abs(i_j_difference_Y))

                self.hive[i].fitness = returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction)

                self.hive[i].sensorRange = min(self.r_max, max(0, self.hive[i].sensorRange + self.beta * (self.n_t - np.abs(len(i_neighbours)))))

    def getRandomBestGlowwormIndex(self, glowworms_list):
        if (len(glowworms_list) != 0):
            result_index = 500
            rng__max_range = 0
            for i in range(0,len(glowworms_list),1):
                rng__max_range += glowworms_list[i].moveProbability
                
            rng_move_number = np.random.uniform(low= 0, high = rng__max_range)
            sum_range = 0

            for i in range(0,len(glowworms_list),1):
                if ((rng_move_number >= sum_range) and (rng_move_number <= (sum_range + glowworms_list[i].moveProbability))):
                    result_index = self.hive.index(glowworms_list[i])
                    break
                sum_range += glowworms_list[i].moveProbability
            return result_index
        else:
            return -1

    def distanceBetweenGlowworms(self, glowworm1, glowworm2):
        helpX = ((glowworm1.x - glowworm2.x) * (glowworm1.x - glowworm2.x))
        helpY = ((glowworm1.y - glowworm2.y) * (glowworm1.y - glowworm2.y))

        return np.sqrt(helpX + helpY + 0)
