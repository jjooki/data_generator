# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:33:02 2021

@author: jjooki

Time set mode : Real-time / Bundle

1. set mode
2. Sampling Rate
3. Start Time
4. Time range
"""
import numpy as np
import datetime
import time
import csv
from ppg import waveform as wf

class Generator:
    def __init__(self, sampling_rate, start_time, time_range):
        self.sr = sampling_rate # Sampling rate(Hz), dtype = float in [20.0, 100.0]
        self.start = start_time # Start Time, dtype = datetime.datetime
        self.time = start_time  # time, dtype = datetime.datetime
        self.tr = time_range    # Time range(hours), dtype = datetime.timedelta
        self.ppg = wf.PPG()     # PPG Signal
        self.noise = wf.Noise() # Noise Signal
        self.interval = datetime.timedelta(seconds = 1. / self.sr)  # Signal input interval
        self.file_name = ""
        self.signal = []
        self.timestamp = []
        self.power = 0.

        directory = './ppg/files/'
        file = self.time.strftime('%y%m%d_%H%M%S') + "_ppg_HR_log.csv"
      
        self.ppg_period = datetime.timedelta(seconds = self.ppg.period())
        self.ppg_time = self.start
        self.noise_period = datetime.timedelta(seconds = 10)

        self.cycle = [0,0,0]  # [total cycle, ppg cycle, noise cycle]
        
        self.file_name = directory + file
        
        with open(self.file_name,'w', newline="") as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(["Timestamp", "Heart Rate(bpm)"])
        
    
    def ppg_gen(self):
        
        if self.still_run():
            dt = self.time - self.start         # Timedelta from start to now
            dt_ppg = self.time - self.ppg_time  # timephase in a ppg signal period
            
            self.cycle[0] += 1
            self.power = self.ppg.power(self.timedelta_to_float(dt_ppg)) + self.noise.power(self.timedelta_to_float(dt))
            
            # Save signal power and timestamp
            self.timestamp.append(self.time.strftime('%Y-%m-%d %H:%M:%S.%f'))
            self.signal.append(self.power)
            
            if dt_ppg >= self.ppg_period:
                self.cycle[1] += 1
                self.ppg_time += self.ppg_period
                self.ppg.update()
                self.ppg_period = datetime.timedelta(seconds = self.ppg.period())   # PPG Signal frequency repeatedly changes at the end of a period.
                
            if dt >= self.cycle[2] * self.noise_period:
                self.cycle[2] += 1
                self.noise.update()
                
            self.time += self.interval
            self.ppg_log_write(self.heart_rate())
        else:
            print("Loop Finish!")
            return 

    def still_run(self):
        if self.cycle[0] <= self.sr * self.tr.seconds:
            return True
        else:
            return False

    def ppg_log_write(self, freq):
        with open(self.file_name, 'a', newline="") as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow([self.time.strftime('%Y-%m-%d %H:%M:%S.%f'), freq])

    def timedelta_to_float(self, td):
        res = td.microseconds/1000000. + (td.seconds + td.days * 24. * 3600.)
        return res

    def heart_rate(self):
        return 60 * self.ppg.value_list[0]
    
    def ppg_amplitude(self):
        return self.ppg.value_list[1]
    
    def Timestamp(self):
        return time.time()
    
    def mqtt_message(self):
        return f'Timestamp: {self.Timestamp()} |\t PPG: {self.power}'
        b1 = bytearray(struct.pack('>d', self.Timestamp()))
        b2 = bytearray(struct.pack('>d', self.power))

        b1.extend(b2)

        # Returns byte array | timestamp 8 bytes | latitude 8 bytes | longitude 8 bytes |
        return b1
        #return f'Timestamp: {time} |\t Latitude: {self.lat}\' |\t Longitude: {self.long}\''
