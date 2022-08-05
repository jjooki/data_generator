import sys, os
sys.path.append(os.path.dirname(os.path.abspath('./axis1.py')))
import math
import numpy as np
import json
import pandas as pd
from ppg import random_walk as rw

class Acc:
    def __init__(self,sampling_rate):
        with open('./acc/acc.json') as f:
            jf = json.load(f)
            info = pd.DataFrame(jf)
            self.acc_info = [info['x'], info['y'], info['z']]
        
        self.sr = sampling_rate
        
        self.acc_rw = [rw.Randomwalk(i) for i in self.acc_info]
        self.acc = [i.val for i in self.acc_rw]
        self.vel = [0., 0., 0.]
        self.s = [0., 0., 0.]
        
    def update(self):
        acc_0 = self.acc
        vel_0 = self.vel
        s_0 = self.s
    
        self.acc = [i.Random_walk() for i in self.acc_rw]
        self.vel = [self.integrate(p_0,q_0,q) for p_0, q_0, q in zip(vel_0, acc_0, self.acc)]
        self.s = [self.integrate(p_0,q_0,q) for p_0, q_0, q in zip(s_0, vel_0, self.vel)]
    
    def integrate(self, p_0, q_0, q):
        return p_0 + (q_0 + q)/self.sr/2.

    def acceleration(self):
        return self.acc

    def velocity(self):
        return self.vel

    def displacement(self):
        return self.s
    
    """
    self.move is matrix
    [a_x, a_y, a_z]
    [v_x, v_y, v_z]
    [s_x, s_y, s_z]
    """        
    def matrix(self):
        return [[self.acc_x, self.acc_y, self.acc_z],[self.vel_x, self.vel_y, self.vel_z],[self.x, self.y, self.z]]

if __name__ == '__main__':
    acc = Acc(200)
    for i in range(20000):
        print("Acceleration vector :", acc.acceleration())
        print("Velocitiy vector :", acc.velocity())
        print("Displacement vector :", acc.displacement())
        print()
        acc.update()