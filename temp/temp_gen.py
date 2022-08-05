"""
Created on Tue Nov  9 10:33:02 2021

@author: jjooki

temp.json

> mean : 36.5
move : 0.01
min : 35
max : 40
rw_length : 0.01
"""
import datetime
import pandas as pd
from temp import random_walk as rw
import json

class Temp:
    def __init__(self):
        with open('./temp/temp.json','r') as f:
            self.info = json.load(f)

        self.t = rw.Randomwalk(self.info)
        self.temp = self.t.value

    def update(self):
        pre_temp = self.temp
        self.temp = self.t.Random_walk()
        self.covid(pre_temp)

    def covid(self, pre):
        if self.temp >= 37.5 and pre < 37.5:
            print("Alarm : Covid19")

    def temperature(self):
        return self.temp
    
    def mqtt_message(self, time):
        return f'Timestamp: {time} |\t Temp: {self.temp}℃'

if __name__ == "__main__":
    t = Temp()
    temp = t.temp
    print(temp)
    i = 1
    while i < 1000:
        i += 1
        t.update()
        if i % 10 == 0:
            print(t.temp)