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
