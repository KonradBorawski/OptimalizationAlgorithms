import numpy as np
from testFunction import returnChosenFunction

class Location:
    x = None
    y = None
    def __init__(self,x = 0,y = 0,position = 0,whichConstructorLocation = 0):
        if(whichConstructorLocation==0):
            self.x = x
            self.y = y
        elif(whichConstructorLocation==1):
            self.x = position.x
            self.y = position.y

class Star:
    position = None
    x = None
    y = None
    fitness = None
    charge = None
    energy = None
    acceleration = None
    velocity = None
    FG = None
    FQ = None

    def __init__(self,x1 = 0, y1 = 0, fitness = 0, star = 0, whichConstructorStar = 0):
        if(whichConstructorStar==0):
            self.x = x1
            self.y = y1
            self.fitness = fitness
            self.charge = 0
            self.energy = Location(x = 0,y = 0,whichConstructorLocation = 0)
            self.acceleration = Location(x = 0,y = 0,whichConstructorLocation = 0)
            self.velocity = Location(x = 0,y = 0,whichConstructorLocation = 0)
        elif(whichConstructorStar==1):
            self.position = Location(x = x1, y = y1,whichConstructorLocation = 0)
            self.x = x1
            self.y = y1
            self.fitness = star.fitness
            self.charge = star.charge
            self.energy = star.energy
            self.acceleration = star.acceleration
            self.velocity = Location(position = star.velocity,whichConstructorLocation = 1)
        




class BlackHole3D:
    hive = None
    black_hole = None
    range = None
    maxIterations = None
    alpha = None
    epsilon = None
    nrStars = None
    chosenFunction = None
    def __init__(self,range1,nrStars,maxIterations,chosenFunction):
        self.chosenFunction = chosenFunction
        self.nrStars = nrStars
        self.range = range1
        self.maxIterations = maxIterations
        self.hive = []
        self.alpha = 0.8
        self.epsilon = 0.1

        for i in range(0,nrStars,1):
            x = np.random.uniform(low= -self.range, high = self.range)
            y = np.random.uniform(low= -self.range, high = self.range)
            fitness1 = -returnChosenFunction(x, y,self.chosenFunction)
            self.hive.append(Star(x1 = x, y1 = y, fitness = fitness1, whichConstructorStar = 0))

        strong_fitness = max(the_best.fitness for the_best in self.hive)
        index = None
        for index, item in enumerate(self.hive):
            if item.fitness == strong_fitness:
                break
            else:
                index = -1
        self.black_hole = Star(x1 = self.hive[index].x, y1 = self.hive[index].y,star = self.hive[index], whichConstructorStar = 1)

        if self.black_hole not in self.hive:
            self.hive.append(Star(star = self.black_hole, whichConstructorStar = 1))

    def calculateCharge(self):
        charge_i_list = []

        strong_fitness = max(the_best.fitness for the_best in self.hive)
        weak_fitness = min(the_worst.fitness for the_worst in self.hive)
        charge_sum = 0

        for i in range(0,len(self.hive),1):
            charge_i = (self.hive[i].fitness - weak_fitness) / (strong_fitness - weak_fitness)
            charge_i_list.append(charge_i)
            charge_sum += charge_i

        for i in range(0,len(self.hive),1):
            self.hive[i].charge = (charge_i_list[i] ) / charge_sum

    def calculateMove(self,iterations):
        iteration_add = np.power(1 / iterations+1, self.alpha)
        for i in range(0,len(self.hive),1):
            self.hive[i].energy.x = 0
            self.hive[i].energy.y = 0
            for j in range(0,len(self.hive),1):
                if (i != j):
                    self.hive[i].energy.x += np.random.random() * 2 * ((self.hive[i].charge * self.hive[j].charge) / ((self.distanceBetweenStars(self.hive[i], self.hive[j]) + self.epsilon))) * (self.hive[j].x - self.hive[i].x)

                    self.hive[i].energy.y += np.random.random() * 2 * ((self.hive[i].charge * self.hive[j].charge) / ((self.distanceBetweenStars(self.hive[i], self.hive[j]) + self.epsilon))) * (self.hive[j].y - self.hive[i].y)
                

            self.hive[i].acceleration.x = self.hive[i].energy.x / self.hive[i].charge
            self.hive[i].acceleration.y = self.hive[i].energy.y / self.hive[i].charge
                
            if (self.hive[i].charge != 0):
                self.hive[i].velocity.x = (np.random.random() * self.hive[i].velocity.x) + self.hive[i].acceleration.x
                self.hive[i].velocity.y = (np.random.random() * self.hive[i].velocity.y) + self.hive[i].acceleration.y
            else:
                self.hive[i].velocity = Location(x = 0,y = 0,whichConstructorLocation = 0)

    def distanceBetweenStars(self,star1,star2):
        helpX = ((star1.x - star2.x) * (star1.x - star2.x))
        helpY = ((star1.y - star2.y) * (star1.y - star2.y))
        helpZ = ((star1.fitness - star2.fitness) * (star1.fitness - star2.fitness))
        return np.sqrt(helpX + helpY + helpY)


    def findBlackHole(self):
        if (self.black_hole.fitness > max(the_best.fitness for the_best in self.hive)):
            strong_fitness = max(the_best.fitness for the_best in self.hive)
            index = None
            for index, item in enumerate(self.hive):
                if item.fitness == strong_fitness:
                    break
                else:
                    index = -1
            self.black_hole = Star(star = self.hive[index], whichConstructorStar = 1)

            self.hive.pop(len(self.hive)-1)
            self.hive.append(Star(star = self.black_hole, whichConstructorStar = 1))

    def moveStar(self):
        for i in range(0,self.nrStars,1):
            if (((self.hive[i].x + self.hive[i].velocity.x) < -self.range) or ((self.hive[i].x + self.hive[i].velocity.x) > self.range)):
                self.hive[i].x = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].x += self.hive[i].velocity.x

            if (((self.hive[i].y + self.hive[i].velocity.y) < -self.range) or ((self.hive[i].y + self.hive[i].velocity.y) > self.range)):
                self.hive[i].y = np.random.uniform(low= -self.range, high = self.range)
            else:
                self.hive[i].y += self.hive[i].velocity.y

            self.hive[i].fitness = -returnChosenFunction(self.hive[i].x, self.hive[i].y,self.chosenFunction)



    def doOneIteration(self, iterations):
        if(iterations < self.maxIterations):
            self.findBlackHole()
            self.calculateCharge()
            self.calculateMove(iterations+1)
            self.moveStar()


    def __repr__(self):
        return repr((self.hive.x, self.hive.y, self.hive.fitness))