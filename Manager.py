import FloatMuttant;

import matplotlib.pyplot as plt

import multiprocessing
import threading

import time;

import sys;


class Manager:
    
    ## informations about
    isTraining = False;
    populationSize = 8; ## 4 * 2 (4 number of split)
    generatioNumber = 0;
    numberOfGeneration = 0;
    
    ## Float informations    
    currentPopulation = [];
    listOfResult = [];
    lastBetterFloat = None;

    numberofGeneration = 1;
    numberofFloat = 1;

    
    currentLevel = 0;
    sredes = [];
    
    def __init__(self):
        print("Welcome to the algorithm! Produced for IPMA");

    def spawnGeneration(self):
         ## First spawn
        if(self.generatioNumber == 0):
            mutant = FloatMuttant.Float(100, True, None, 0);
            self.currentPopulation.append(mutant);
            mutant.doSimulation(mutant);
            
        else:
           print("Score précédant > ", self.lastBetterFloat.score);
           self.lastBetterFloat.printValue();
           self.muteFloat();
                
        self.generatioNumber = self.generatioNumber + 1;
        self.setBestElementOfGeneration();
        
        print(self.lastBetterFloat.score);

        print("Current generation: ", self.generatioNumber);
        print("------------------------------------------------------")

    
    def muteFloat(self):
        self.currentPopulation = [];
        mutant = None;
              
        print("Current mutation: 0") #make a copy of the last better
        mutant = FloatMuttant.Float(100, False, self.lastBetterFloat, 0);
        self.currentPopulation.append(mutant);
        mutant.doSimulation(mutant);
        
        print("Level mutation: 2")
        self.currentLevel = 2
        self.run()     
        
        print("Level mutation: 4")
        self.currentLevel = 4
        self.run()
            
        print("Level mutation: 7")
        self.currentLevel = 7
        self.run()
        
        print("Level mutation: 10")
        self.currentLevel = 10
        self.run()
            
    def run(self):    # Default called function with mythread.start()
        print("New simulation start ")
        mutant = FloatMuttant.Float(100, False, self.lastBetterFloat, self.currentLevel)
        mutant.doSimulation(mutant)
        self.currentPopulation.append(mutant);

        return
                    
    def setBestElementOfGeneration(self):
        for c in self.currentPopulation:
            print(c.score)
            if(self.lastBetterFloat == None):
                self.lastBetterFloat = c;
            else:
                if(c.score >= self.lastBetterFloat.score):
                    self.lastBetterFloat = c;
        self.listOfResult.append(self.lastBetterFloat);
        
        if((self.numberOfGeneration + 1) == len(self.listOfResult)):
            print("Result Of Simulation: ");
            print(" ");
            print("parking_depth: ", self.lastBetterFloat.parking_depth);
            print("vertical_speed: ", self.lastBetterFloat.vertical_speed);
            print("cycle_duration: ", self.lastBetterFloat.cycle_duration);
            print(" ");
            print("Result: ", self.lastBetterFloat.score);

    def plotFitness(self):
        x = [];
        y = [];
        
        for i in self.listOfResult:
            y.append(i.score);
            
        print(y);
        
        for i in range(7):
            x.append(i);
      
        
        plt.plot(x, y, label='Fitness result (%)', c='green');
        plt.xlabel("Generation number")
        plt.ylabel("Score %")
        plt.legend()
        plt.show();
            
    def simulate(self, ammount):
        self.isTraining = True;
        self.numberOfGeneration = ammount;
        while(self.isTraining == True):
            
            if(self.generatioNumber == ammount):
                self.isTraining = False;
            
            self.spawnGeneration();
    
manager = Manager();
manager.simulate(3);
#manager.plotFitness();
