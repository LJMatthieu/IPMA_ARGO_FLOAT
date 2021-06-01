# IPMA_ARGO_FLOAT
Algorithm based on [VirtualFleet](https://github.com/euroargodev/VirtualFleet/). that determines the best parameters for an agro-float to stay in a defined area. 

# The algorithm
In order to determine the best parameters to keep the float in the same area we use a generic algorithm.
The study area is defined by the deployment plan of the floats.

## Configuration 

To run a simulation from the Manager.py class
```
manager = Manager();
manager.simulate(4); # 4 is the number of generations desired 
manager.plotFitness();
```

To set up the mutation of the floats 

1. Setting the float operating interval FloatMuttant.py
```
parking_depth_min = 250;
parking_depth_max = 1500;
    
vertical_speed_min = 0.001;
vertical_speed_max = 0.14;
    
cycle_duration_min = 3;
cycle_duration_max = 10;
```

2. Configure the size of limited area 
```
box = Box("US", 2.5, output_file); # 2.5 is the size of area ( cf exemple )
box.initValueCorner()
box.initPolygon()
```

Here is an example of a 'box' defined with a size of 2.5 on each side. 
![alt text](http://image.noelshack.com/fichiers/2021/22/2/1622546145-screenshot-1.png)

