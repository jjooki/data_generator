# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:26:38 2021

@author: jjooki

This file is for making 'random walk' change of values.

2021-11-12 14:29 Finished

"""

import numpy as np
import sys
sys.setrecursionlimit(10000000)
import math
import json
import struct

class GPS:
    
    """
    Set the parameter statistics information
    info -> mean, min, max    
    """
    
    def __init__(self, stat_info):

        self.lat_info = stat_info['latitude']
        self.long_info = stat_info['longitude']
        self.lat_move_info = self.lat_info['move']
        self.long_move_info = self.long_info['move']
        
        self.long = self.long_info["start"] # set the initial random value in [min,max]
        self.lat = self.lat_info["start"]   # set the initial random value in [min,max]
        self.dlong = self.long_move_info['mean']    # inital velocity is 0.
        self.dlat = self.lat_move_info["mean"]     # inital velocity is 0.
        self.d2long = 0.
        self.d2lat = 0.
        
    # Random walk function
    # input : update period
    def update(self, interval):
        long = self.long + self.dlong * interval
        lat = self.lat + self.dlat * interval
        
        dlong = self.move(self.long_move_info, self.dlong, interval)
        self.d2long = self.acc
        dlat = self.move(self.lat_move_info, self.dlat, interval)
        self.d2lat = self.acc

        if self.out_of_range(self.long, self.long_info):
            self.update()
        else:
            self.long = long
            self.lat = lat
            self.dlong = dlong
            self.dlat = dlat
            return  
        
    #move
    def move(self, info, vel, interval):
        self.acc = 0.2 * info['max'] * np.random.rand()
        direct = np.random.rand()
        if direct <= self.dist(info['mean'], info['max']/2., vel):
            vel_after = vel - acc * interval
        else:
            vel_after = vel + acc * interval
        
        if not self.out_of_range(vel_after, info):
            return vel_after
        else:
            self.move(info, val)
            return
            
    # After random walk, check value
    def out_of_range(self, vel_after, info):
        if (vel_after < info['min']) or (vel_after > info['max']):
            return True
        else:
            return False

    def location(self):
        return [self.lat, self.long] # (latitude, longitude)
    
    def velocity_xyplane(self):
        theta = np.pi * 6371000 / 180. 
        return [theta * self.dlat, theta * self.dlong]  # velocity vector(m/s, m/s)
    
    def latitude(self):
        return self.lat
    
    def longitude(self):
        return self.long

    def acc_xyplane(self):
        theta = np.pi * 6371000 / 180. 
        return [self.d2long * theta, self.d2lat * theta]

    # Accumulated possibility (X <= x) of gaussian distribution
    def dist(self, mu, sigma, x):
        return (1 + math.erf((x - mu) / sigma / math.sqrt(2))) / 2

    def mqtt_message(self, time):
        b1 = bytearray(struct.pack('>d', time))
        b2 = bytearray(struct.pack('>d', self.lat))
        b3 = bytearray(struct.pack('>d', self.long))

        b1.extend(b2)
        b1.extend(b3)

        # Returns byte array | timestamp 8 bytes | latitude 8 bytes | longitude 8 bytes |
        return b1
        #return f'Timestamp: {time} |\t Latitude: {self.lat}\' |\t Longitude: {self.long}\''
    
    def message(self):
        return f'{self.lat}, {self.long}'
