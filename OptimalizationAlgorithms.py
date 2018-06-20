import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

from testFunction import returnChosenFunction
from PSOAlgorithm import ParticlePSO3D
from FireflyAlgorithm import Firefly3D
from BatAlgorithm import Bat3D
from GSAAlgorithm import ParticleGSA3D
from CSSAlgorithm import ParticleCSS3D
from AntAlgorithm import Ant3D
from BlackHoleAlgorithm import BlackHole3D
from GlowWormAlgorithm import GlowWorm3D
from SimulatedAnnealing import SimulatedAnnealing3D
from DifferentialEvolution import DE3D


class CenteredTextInput(TextInput):
    text_width = NumericProperty()
    def update_padding(self, *args):
        self.text_width = self._get_text_width(self.text,self.tab_width, self._label_cached)
    
Builder.load_file("ScreenMenu.kv")
class ScreenMenu(Screen):
    listOfAlgorithms = ['PSO', 'Firefly', 'Bat', 'GSA', 'CSS', 'Ant', 'BlackHole', 'GlowWorm', 'SA', 'DE']
    chosenFunction = StringProperty()
    numberOfAgents = StringProperty()
    agentsRange = StringProperty()
    maxIterations = StringProperty()
    interval = StringProperty()
    closePlotWindow = False

    currentIteration = 0
    points = []
    agentsHive = None
    timer = None
    whichAlgorithm = None

    def timerFunction(self, dt):
        for i in range(0,int(self.numberOfAgents),1):
            self.points.append(plt.scatter(x = self.agentsHive.hive[i].x, y = self.agentsHive.hive[i].y, s = 20, color= 'white'))
        self.agentsHive.doOneIteration(self.currentIteration)
            
        if self.closePlotWindow == False and self.currentIteration != int(self.maxIterations):
            plt.pause(0.01)
            for k in range(1,int(self.numberOfAgents)+1,1):
                self.points[-k].remove()
            plt.draw()
        else:
            plt.pause(0.01)
            self.currentIteration = 0
            self.timer.cancel()
            plt.draw()
        self.currentIteration +=1

    def createHive(self):
        if self.whichAlgorithm == self.listOfAlgorithms[0]:
            self.agentsHive = ParticlePSO3D(int(self.agentsRange),int(self.numberOfAgents),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[1]:
            self.agentsHive = Firefly3D(int(self.agentsRange),int(self.numberOfAgents),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[2]:
            self.agentsHive = Bat3D(int(self.agentsRange),int(self.numberOfAgents),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[3]:
            self.agentsHive = ParticleGSA3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[4]:
            self.agentsHive = ParticleCSS3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[5]:
            self.agentsHive = Ant3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[6]:
            self.agentsHive = BlackHole3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[7]:
            self.agentsHive = GlowWorm3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[8]:
            self.agentsHive = SimulatedAnnealing3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)
        elif self.whichAlgorithm == self.listOfAlgorithms[9]:
            self.agentsHive = DE3D(int(self.agentsRange),int(self.numberOfAgents),int(self.maxIterations),self.chosenFunction)

    def startAlgorithm(self, whichAlgorithm):
        self.whichAlgorithm = whichAlgorithm
        self.closePlotWindow = False
        fig = plt.figure(1)
        fig.canvas.mpl_connect('close_event', self.quit_figure)
        ax = fig.add_subplot(111)
        u = np.linspace(-int(self.agentsRange),int(self.agentsRange),100)
        x, y = np.meshgrid(u,u)
        z = returnChosenFunction(x,y,self.chosenFunction)
        plt.xlim(-int(self.agentsRange), int(self.agentsRange))
        plt.ylim(-int(self.agentsRange), int(self.agentsRange))
        ax.contourf(x,y,z)
        
        self.createHive()
        self.timer = Clock.schedule_interval(partial(self.timerFunction), float(self.interval))

        plt.show(block=False)
        


    def quit_figure(self,evt):
        self.timer.cancel()
        self.closePlotWindow = True
        self.currentIteration = 0
        plt.close('all')
    def stopApplication(self):
        Window.close()



class TestApp(App):
    screenManager = ScreenManager()
    screenManager.add_widget(ScreenMenu(name='screen_menu'))
    def build(self):
        return self.screenManager

if __name__ == '__main__':
    TestApp().run()




