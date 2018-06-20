import numpy as np
from kivy.properties import StringProperty

chosenFunction = StringProperty()
def returnChosenFunction(x,y, chosenFunction):
    if(chosenFunction == 'Cztery szczyty'):
        return (np.sqrt(x*x)+np.sqrt(y*y))*np.exp((-0.0625)*(x*x +y*y))
    elif(chosenFunction == 'Funkcja Rosenbrocka'):
        return -(((1 - x) * (1 - x)) + (100 * (y - x * x) * (y - x * x)))
    elif(chosenFunction == 'Funkcja Schwefela'):
        return (-1)*418.9829*2 + x*np.sin(np.sqrt(np.abs(x)))+y*np.sin(np.sqrt(np.abs(y)))
    elif(chosenFunction == 'Funkcja Easoma'):
        return -np.cos(x)*np.cos(y)*np.exp(-np.power((x-3.14),2)-np.power((y-3.14),2))
    elif(chosenFunction == 'Funkcja Schaffera'):
        return 0.5+(np.power(np.sin(np.sqrt(x*x+y*y)),2)-0.5)/np.power((1+0.001*(x*x+y*y)),2)
    elif(chosenFunction == 'Funkcja Bealea'):
        return np.power(1.5 - x + (x*y),2)+ np.power(2.25 - x +np.power(x*y,2),2)+ np.power(2.625 - x +np.power(x*y,3),2)
    elif(chosenFunction == 'Funkcja Himmemblau'):
        return np.power(x*x + y - 11,2) + np.power(x +y*y -7,2) 
    elif(chosenFunction == 'Funkcja Bootha'):
        return np.power(x +2* y - 7,2) + np.power(2*x +y -5,2)
    elif(chosenFunction == 'Opakowanie jajek'):
        return (x*x + y*y) + 25*(np.power(np.sin(x),2)+ np.power(np.cos(y),2))