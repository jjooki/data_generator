# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:26:38 2021

@author: jjooki

This file is for making 'random walk' change of values.

2021-11-12 14:29 Finished

"""

import numpy as np
import sys
sys.setrecursionlimit(100000000)
from ppg import gaussian as gs
import matplotlib.pyplot as plt

class Randomwalk:
    
    """
    Set the parameter statistics information
    info -> mean, sigma(standard deviation), min, max
    """
    
    def __init__(self, stat_info):
        self.info = stat_info   # read the statistics information
        self.val = (self.info["max"] - self.info["min"]) * np.random.rand() + self.info["min"] # set the initial random value in [min,max]
        
    # Random walk function
    # input : update period
    def Random_walk(self):
        length = np.random.rand() * self.info["sigma"]  # random walk step length in range(0, 0.5*sigma)
        direction_num = np.random.rand()                # direction decision parameter
        p = gs.accum_p_dist(self.info["mean"], self.info["sigma"], self.val) # criteria to determine whether go forward or back.
        
        # If direction decision parameter value is under the accumulated possible(x <= value) of gaussian distribution, step back as 1 step. 
        if direction_num <= p:
            val_after = self.val - length   #Go back
            #print("\nGo back")
        else:                
            val_after = self.val + length   #Go Forward
            #print("\nGo forward")
        
        #print("\nAfter value :", val_after)
        #print("Is it out of range? :", self.out_of_range(val_after))
        
        if not self.out_of_range(val_after):
            self.val = val_after
        else:
            self.Random_walk()
            if not self.out_of_range(val_after):
                return
            
        return self.val
    
    # After random walk, check value
    def out_of_range(self, val_after):
        if (val_after < self.info["min"]) or (val_after > self.info["max"]):
            return True
        else:
            return False


# Test Code
if __name__ == "__main__":
    example_info = {"mean": 1, "sigma": 0.5, "min": 0.5, "max": 1.5}
    time = np.linspace(0,100,1001)
    rw = Randomwalk(example_info)
    val = [rw.val]
    
    for i in range(1000):
        rw.Random_walk()
        val.append(rw.val)
        
    print(val)
    
    plt.plot(time, val)
    plt.xlabel('Time')
    plt.ylabel('randomwalk')
    plt.axis('tight')
    plt.show()