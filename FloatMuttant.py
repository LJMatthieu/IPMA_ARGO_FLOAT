# -*- coding: utf-8 -*-

import random
import Simulation;

class Float:

##########################################################################
###
### Mission parameters and parameters random.randint(0, 3)
###
##########################################################################

    score = 0;
    
    parking_depth = 0;
    profile_depth = 2000;
    vertical_speed = 0;
    cycle_duration = 0;
    
    ## multiplicateur 
    parking_depth_step = 50;
    vertical_speed_step = 0.05;
    cycle_duration_step = 2;
    
    ## max and min
    parking_depth_min = 250;
    parking_depth_max = 750;
    
    vertical_speed_min = 0.001;
    vertical_speed_max = 0.14;
    
    cycle_duration_min = 3;
    cycle_duration_max = 10;
    
    path = "";
    rnd = None;

    # First init with random init
    def __init__(self, scoreMaxi, rnd, flatMuttant, levelofMutation):
        self.score = 0;
        self.rnd = rnd;
        
        if(self.rnd): 
            self.initWithRandomValue();
        else:
            self.initByCopy(flatMuttant, levelofMutation); 
       
    def initWithRandomValue(self):
        self.parking_depth = random.randint(250, self.parking_depth_max);
        self.vertical_speed = round(random.uniform(0.0, 0.14), 3);
        self.cycle_duration = random.randint(7, 10);
   
    def initByCopy(self, flatMuttant, levelOfMutation):
        if(self.rnd == True):
            self.parking_depth = flatMuttant.parking_depth 
            self.vertical_speed = flatMuttant.vertical_speed
            self.cycle_duration = flatMuttant.cycle_duration
        else:
            self.parking_depth = self.getValueOfMutation(flatMuttant.parking_depth, (self.parking_depth_step * levelOfMutation), self.parking_depth_max, self.parking_depth_min);
            self.cycle_duration = round(self.getValueOfMutation(flatMuttant.cycle_duration, (self.cycle_duration_step * levelOfMutation), self.cycle_duration_max, self.cycle_duration_max));
            self.vertical_speed = self.getValueOfMutation(flatMuttant.vertical_speed, (self.vertical_speed_step * levelOfMutation), self.vertical_speed_max, self.vertical_speed_min);


    def doSimulation(self, mutant):
       #  self.printValue();
         simu = Simulation.SimulationArgo(self.parking_depth, self.vertical_speed , self.cycle_duration, mutant);
         simu.simulate();
         
    def setPath(self, path):
        self.path = path;
        
        
    def mutationPossible(self, value, maxCondifation, minCondition):
        if(value > maxCondifation):
            return False;
        else:
            return True;
    
    def getValueOfMutation(self, value, condition, maxC, minC):
        toReturn = 0;
        
        add = random.uniform(0, condition)
        sign = random.uniform(-1, 1);
        
        if (sign >= 0):
           toReturn = value + round(add, 3);
        if(sign < 0):
           toReturn = value - round(add, 3);
                
    
        toReturn = value + add;
        if(self.mutationPossible(toReturn, maxC, minC) == False):
            while(self.mutationPossible(toReturn, maxC, minC) == False):
                add = random.uniform(0, condition)
                if(toReturn > maxC):
                    toReturn = value - round(add, 3);
                if(toReturn < minC):
                    toReturn = value + round(add, 3);            
        return toReturn;
        
    def printValue(self) :
        print("> ", self.parking_depth);
        print("> ", self.vertical_speed);
        print("> ", self.cycle_duration);
        
        

###
### Débuter avec un flotteur et des paramètres choisis
##  Stop si il trouve l'objectif défault 90%
###
########### TEST ###########
#floatArgo = Float(200, True, None);
#floatArgo.printValue();
#print(floatArgo.getValueMutation(floatArgo.parking_depth, 50))
