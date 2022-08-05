"""
Created on Tue Nov 19 11:39:00 2021

@author: jjooki

If moving direction is forward before, probability going forward is 0.7
If moving back before, prob going forward is 0.3
My intension is to make temperature variation trendy
"""
import math
import numpy as np
import sys
sys.setrecursionlimit(100000000)
import matplotlib.pyplot as plt

class Randomwalk:
    
    """
    Set the parameter statistics information
    info -> mean, move distance, min, max    
    """
    
    def __init__(self, stat_info):
        self.info = stat_info   # read the statistics information
        self.value = 0.
        while self.out_of_range(self.value):
            self.value = 0.5 * np.random.randn() + self.info['mean'] # set the initial random value in [min,max]
        self.p = 0.5                      # set initial probability moving up or down
        
    # Random walk function
    # input : update period
    def Random_walk(self):
        length = self.info["move"] + 0.01 * np.random.rand()    # random walk step length in range(0, 0.5*sigma)
        direction_num = np.random.rand()                        # direction decision parameter
        
        # If direction decision parameter value is under the accumulated possible(x <= value) of gaussian distribution, step back as 1 step. 
        if direction_num <= self.p:
            val_after = self.value - length   #Go back
            self.p = 0.7
        else:
            val_after = self.value + length   #Go Forward
            #print("\nGo forward")
            self.p = 0.3
        
        #print("\nAfter value :", val_after)
        #print("Is it out of range? :", self.out_of_range(val_after))
        
        if not self.out_of_range(val_after):
            self.value = val_after
        else:
            self.Random_walk()
            if not self.out_of_range(val_after):
                return
            
        return self.value
    
    # After random walk, check value
    def out_of_range(self, val_after):
        if (val_after < self.info["min"]) or (val_after > self.info["max"]):
            return True
        else:
            return False

    # Accumulated possibility (X <= x) of gaussian distribution
    def prob(mu, sigma, x):
        return (1 + math.erf((x - mu) / sigma / math.sqrt(2))) / 2

# Test Code
if __name__ == "__main__":
    example_info = {"mean": 36.5, "move": 0.1, "min": 40, "max": 33}
    time = np.linspace(0,100,1001)
    rw = Randomwalk(example_info)
    val = [rw.value]
    
    for i in range(1000):
        val.append(rw.Random_walk())
        
    print(val)
    
    plt.plot(time, val)
    plt.xlabel('Time')
    plt.ylabel('randomwalk')
    plt.axis('tight')
    plt.show()
