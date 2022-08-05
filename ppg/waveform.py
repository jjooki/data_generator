import numpy as np
import pandas as pd
import json
import sys
sys.setrecursionlimit(8640000)

from ppg import gaussian as gs
from ppg import random_walk as rw
import datetime

class PPG:
    def __init__(self):
        """
        Read the json file which have the statistics information('mean','std','max','min') of all parameters.
        If you change directory name or location, must change below path.
        """
        f = open('ppg/wave.json','r')
        js = json.load(f)
        f.close()
        self.info = pd.DataFrame(js)
        
        """
        Parameter list have index like this.
        1. freq
        2. sys_amp
        3. sys_phase
        4. sys_width
        5. dias_amp
        6. dias_phase
        7. dias_width
        """
        
        self.info_list = [self.info['frequency'], self.info['systolic amplitude'], self.info['systolic peak_phase'], 
                          self.info['systolic width'], self.info['diastolic amplitude'],
                          self.info['diastolic peak_phase'], self.info['diastolic width']]
        
        self.set_list = [rw.Randomwalk(info) for info in self.info_list]    # call the the 'Randomwalk' class
        
        self.value_list = np.array([s.val for s in self.set_list])          # set the initial value of all parameters
        # print(self.value_list)
        self.pre_value = np.zeros(7)
        self.post_value = np.array([s.Random_walk() for s in self.set_list])
        # print(self.post_value)
        self.noise = Noise()
    
    def param_log(self):
        return self.value_list
    
    def value(self, i):
        return self.value_list[i]
    
    def frequency(self):
        return self.value_list[0]
        
    def period(self):
        return 1. / self.value_list[0]
    
    # update the value through random walk after finishing 1 period.
    def update(self):
        self.pre_value = self.value_list
        self.value_list = self.post_value
        update_list = [s.Random_walk() for s in self.set_list]
        self.post_value = np.array(update_list)
            
    """
    Wave Function : Sum of two gaussian function(Systolic part + Diastolic part)
    time : dtype = float64
    values : dtype = ndarray
    """
    def func(self, time, values):
        sys = gs.func(values[1], values[2], values[3], time * (2 * np.pi * values[0]))
        dias = gs.func(values[4], values[5], values[6], time * (2 * np.pi * values[0]))
        """
        print("time :", time)
        print("values :", values)
        print("systolic power :", sys)
        print("diastolic power :", dias)
        """
        return sys + dias
    
    # power : 3 successive wave funtions summation
    # dt : dtype = datetime.timedelta
    def power(self, time):
        try:
            """
            print("\ntime :", time)
            print("pre_list :", self.pre_value)
            print("present_list :", self.value_list)
            print("post_list :", self.post_value)                
            
            result = self.func(time, self.pre_value) + self.func(time, self.value_list) + self.func(time, self.post_value)
            """
            result = self.func(time, self.value_list)
            
            if np.isnan(result):
                raise ValueError
              
            return result
       
        except AttributeError:
            print("Please use 'timedelta' type.")
       
        except ValueError:
            return (self.func(time, self.value_list) + self.func(time, self.post_value))


class Noise:
    def __init__(self):
        # If you change directory name or location, must change below path.
        f = open('ppg/noise.json', 'r')
        js = json.load(f)
        f.close()
        self.info = pd.DataFrame(js)
        
        self.amp_info = [self.info[self.info.columns[0]],
                         self.info[self.info.columns[1]],
                         self.info[self.info.columns[2]],
                         self.info[self.info.columns[3]],
                         self.info[self.info.columns[4]]]
        
        self.set_list = [rw.Randomwalk(info) for info in self.amp_info]     # call the the 'Randomwalk' class
        
        self.freq_list = np.array([float(f) for f in self.info.columns])    # value list of frequency
        self.amp_list = np.array([s.val for s in self.set_list])            # set the initial value of all parameters
        self.phase_list = 2 * np.pi * np.random.rand(5)                     # set the initial phase for each frequency
        
    # update the amplitude through random walk after finishing 1 period.
    def update(self):
        update_list = []
        
        for s in self.set_list:
            update_list.append(s.Random_walk())
            
        self.amp_list = update_list
        
    #Sine Wave
    def Sine_wave(self, amplitude, frequency, time, phase):
        return amplitude * np.sin(2. * np.pi * frequency * time + phase)
    
    #Noise Function power
    def power(self, time):
        return sum(0.1 * np.array([self.Sine_wave(A, f, time, phase) for A, f, phase in zip(self.amp_list, self.freq_list, self.phase_list)]))

# Test code
if __name__ == "__main__":
    hello = PPG()
    bye = Noise()
    dt = datetime.timedelta(days = 1, hours = 1)
    print(dt)
    print(hello.power(dt))
    print(bye.power(dt))
    for i in range(10):
        hello.update()
        bye.update()
        print("\nppg :", hello.power(dt))
        print('noise :', bye.power(dt))
    