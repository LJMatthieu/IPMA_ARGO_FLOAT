# -*- coding: utf-8 -*-
import xarray as xr
from shapely.geometry import Point
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, MultiPolygon, Feature

from statistics import *
              
class Box:
 
    corner_box = [];
    polygon = None;
    simu = None;
 
    def __init__(self, name, delta, path):
        self.name = name;
        self.delta = delta;
        self.path = path;
 
        self.simu = xr.open_dataset(path)
 
 
    def getListOfCorner(self, typeData):
        counter = 0;
        toReturn = [];
 
        for i in self.simu['traj']:
            this = self.simu.isel(traj=i).sortby('time')  
 
            counter = counter + 1;        
            if(counter == 1 or counter == self.getNumberOfSimulation(self.simu)): 
                toReturn.append(this[typeData][0].values)    
        return toReturn;
 
    def getNumberOfSimulation(self, simulation):
        return simulation['traj'].values.size;
 
    def getDiffBetweenValue(self, lastValue, nextValue):
        return float(abs((lastValue - nextValue)));
 
    def all_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)
 
    def getDirection(self):
        if(self.all_equal(self.getListOfCorner('lat'))):
            return "lat";
        if(self.all_equal(self.getListOfCorner('lon'))):
            return "lon";
 
    def initValueCorner(self):
        for t in self.getListOfCorner('lat'):
            self.corner_box.append(t);
 
        for t in self.getListOfCorner('lon'):
            self.corner_box.append(t);
 
    def calculPourcentage(self, value, maxi):
        return ((value*100) / maxi);
 
    def initPolygon(self) :
        if(self.getDirection() == "lon"):
           self. polygon = Feature(geometry=MultiPolygon([([(float(self.corner_box[1]), float(self.corner_box[3] - self.delta)),
                                           (float(self.corner_box[0]), float(self.corner_box[2] - self.delta)),
                                           (float(self.corner_box[0]), float(self.corner_box[2] + self.delta)),
                                           (float(self.corner_box[1]), float(self.corner_box[3] + self.delta)),
                                           (float(self.corner_box[1]), float(self.corner_box[3] - self.delta))],)]))
 
 
        if(self.getDirection() == "lat"):
            self.polygon = Feature(geometry=MultiPolygon([([(float(self.corner_box[1] - self.delta), float(self.corner_box[3])),
                                           (float(self.corner_box[0] - self.delta), float(self.corner_box[2])),
                                           (float(self.corner_box[0] + self.delta), float(self.corner_box[2])),
                                           (float(self.corner_box[1] + self.delta), float(self.corner_box[3])),
                                           (float(self.corner_box[1] - self.delta), float(self.corner_box[3]))],)]))
        return self.polygon;
 
 
class Simulation_Case:
    
    box = None;
    FloatMuttant = None;

    def __init__(self, box, FloatMuttant):
        self.box = box;
        self.FloatMuttant = FloatMuttant;
        
    def moyenne(self, liste):
        toReturn = 0;
        for i in liste:
            toReturn = toReturn + i;
        
        return (toReturn/len(liste));
    
    def getBestScore(self, liste):
        toReturn = 0;
        
        for i in liste:
            if(toReturn < i):
                toReturn = i;
        return toReturn;
 
    def simulate(self):
        result = [];
        for i in self.box.simu['traj']:            
            this = self.box.simu.isel(traj=i).sortby('time') 
            end = False;
 
            count_float = 0;
            Point_inside = 0;
 
            #Get all point
            while(end == False):

                x = this['lat'][count_float].values;
                y = this['lon'][count_float].values;
 
                pointToTest = Feature(geometry=Point([float(x), float(y)]))
 
                if(boolean_point_in_polygon(pointToTest, self.box.polygon) == True):
                   Point_inside = Point_inside + 1;
 
                if(count_float == (int(this['lat'].values.size) -1 )): 
                    end = True;
                    
                    # if(round(self.box.calculPourcentage(Point_inside, int(this['lat'].values.size) -1)) != 0):
                    result.append(round(self.box.calculPourcentage(Point_inside, int(this['lat'].values.size) -1), 2))

                 
                count_float = count_float + 1;
                    
        self.FloatMuttant.score = self.getBestScore(result)
        #self.FloatMuttant.setPath(path);
        print("Moyenne: ", self.FloatMuttant.score);
        print("Score: ", result);
        result = []
 
