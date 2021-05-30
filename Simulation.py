d# -*- coding: utf-8 -*-
import sys
import numpy as np
import xarray as xr
import pandas as pd

sys.path.insert(0, "..") # This is while waiting for the pypi integration
import virtualargofleet as vaf

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mpl_toolkits.mplot3d import Axes3D

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from traitement import *

import random;
import string;


class SimulationArgo:
    
    # Mission parameters
    parking_depth = 0; #in m
    profile_depth = 2000;
    vertical_speed = 0; #0.1 #in m/s 90 cm.s^-1
    cycle_duration = 0; # in days
    
    output_file = "";
    FloatMutant = None;
    
    def __init__(self, parking_depth, vertical_speed, cycle_duration, FloatMutant):
        self.parking_depth = parking_depth;
        self.vertical_speed = vertical_speed;
        self.cycle_duration = cycle_duration;
        self.FloatMutant = FloatMutant;
        
    def random_char(self, y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))
    
    def simulate(self):
        land_feature = cfeature.NaturalEarthFeature(category='physical',name='land',scale='50m',facecolor=[0.4,0.6,0.7])
        
        
        # Set how to find the velocity field
        # src = "/home/datawork-lops-oh/somovar/WP1/data/GLOBAL-ANALYSIS-FORECAST-PHY-001-024" # Datarmor
        # src = "/Users/gmaze/data/MERCATOR/data/GLOBAL-ANALYSIS-FORECAST-PHY-001-024" # Laptop
        src = "data/current/US" 
        
        filenames = {'U': src + "/2019*.nc",
                     'V': src + "/2019*.nc"}
        variables = {'U':'uo','V':'vo'}
        dimensions = {'time': 'time', 'depth':'depth', 'lat': 'latitude', 'lon': 'longitude'}
        
        # Ddefine the velocity field object of the VF:
        # USAGE : obj = vaf.velocityfield(ds=filenames, var=variables, dim=dimensions, isglobal=0 or 1) 
        VELfield = vaf.velocityfield(ds=filenames, var=variables, dim=dimensions, isglobal=0)
        
       # VELfield.plot()
        
        # Number of floats we want to simulate:
        nfloats = 5;
        
        # Define space/time locations of deployments:
        #lat = np.linspace(30, 38, nfloats)
        #lon = np.full_like(lat, -60)
        
        lon = np.linspace(-68, -66, nfloats)
        lat = np.full_like(lon, 34)
        
        dpt = np.linspace(1.0, 1.0, nfloats) #1m depth
        tim = np.array(['2019-01-01' for i in range(nfloats)],dtype='datetime64')
        
        
        mission = {'parking_depth':self.parking_depth, 'profile_depth':self.profile_depth, 'vertical_speed':self.vertical_speed, 'cycle_duration':self.cycle_duration}
        
        # DEFINE THE FLOAT OBJECT
        VFleet = vaf.virtualfleet(lat=lat, lon=lon, depth=dpt, time=tim, vfield=VELfield, mission=mission)
        
       # VFleet.plotfloat()
        
        plt.hist(VFleet.time);
        
        # Define where to store results
        run_outputs = "out"
        output_file = "file_{}_{}_{}_{}.nc".format(self.parking_depth, self.vertical_speed, self.cycle_duration,  self.random_char(3)) # ID 
        print("Simulation data saved in:", output_file)
        
        # USAGE : float_object.simulate(duration=days,dt_run=hours,dt_out=hours,output_file='my_advection_nXX.nc')
        # VFleet.simulate(duration=12, dt_run=1/4, dt_out=1/6, output_file=output_file)
        VFleet.simulate(duration=250, dt_run=5, dt_out=0.40, output_file=output_file)
        
        
        # Load simulation results:
        simu = xr.open_dataset(output_file)
        
        pr1 = ccrs.PlateCarree()
        
        fig = plt.figure(figsize=(10,10), dpi=90)
        ax3 = fig.add_subplot(1,1,1,projection=pr1)
        ax3.add_feature(land_feature, edgecolor='black')
        ax3.set_extent([simu.lon.min()-10, simu.lon.max()+10, simu.lat.min()-10, simu.lat.max()+10])
        ax3.gridlines(linewidth=1, color='gray', alpha=0.5, linestyle=':')
        
        for i in simu['traj']:
            this = simu.isel(traj=i).sortby('time')
            ax3.plot(this['lon'][0], this['lat'][0],'k.', transform=pr1)
            ax3.plot(this['lon'], this['lat'], linewidth=1, transform=pr1)
            
            
        plt.title("Virtual Fleet simulation: float trajectories\n(%s)" % output_file);
        
    
        box = Box("US", 2.5, output_file);
        box.initValueCorner()
        box.initPolygon()
        
        simuBox = Simulation_Case(box, self.FloatMutant);
        simuBox.simulate();  
    
##simu = Simulation.SimulationArgo(700, 0.1 , 10, mutant);##simu.simulate();