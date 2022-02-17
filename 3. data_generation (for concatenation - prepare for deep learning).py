# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 22:24:00 2018

@author: evendi Eldrige Rifki Poluan
"""

import os
import numpy as np
import pandas as pd

class DataGeneration(object):
    
    def __init__(self):
        print('## Start . . .')
              
    def concat(self):
        ## Concat all available kinect and insoles
        address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\Person identification'
        file = os.listdir(address)[0:5]
        
        kin_in = []
        for i in file:
            index_file = '{}/{}/{}' . format(address, i, 'Working Directory/')
            
            file_specify = os.listdir(index_file)
            
            insoles_concat = []
            kinect_concat = []
            
            for j in file_specify:
                if j == 'Insoles':
                    find = '{}/{}' . format(index_file, j)
                    data = os.listdir(find)
                    
                    for k in data:
                        if 'Master' in k:
                            addr = '{}/{}' . format(find, k)
                            i_dataframe = pd.read_csv('{}' . format(addr), names = [x.upper() for x in['no', 'r_heel', 'r_thumb', 'r_inner_ball', 'r_outer_ball', 'l_heel', 'l_thumb', 'l_inner_ball', 'l_outer_ball', 'time', 'name']], skiprows = 1)  
                            i_dataframe = i_dataframe.drop(['no' . upper()], axis=1)
                            insoles_concat.append(i_dataframe)
                     
                if j == 'Kinect':
                    find = '{}/{}' . format(index_file, j)
                    data = os.listdir(find)
                    
                    for k in data:
                        if 'Master' in k:
                            addr = '{}/{}' . format(find, k)
                            k_dataframe = pd.read_csv('{}' . format(addr), names = [x.upper() for x in['no', 
                                'spine_base_x', 'spine_base_y', 'spine_mid_x', 'spine_mid_y',
                                'hip_right_x', 'hip_right_y', 'hip_left_x', 'hip_left_y', 
                                'knee_right_x', 'knee_right_y', 'knee_left_x', 'knee_left_y',
                                'ankle_right_x', 'ankle_right_y', 'ankle_left_x', 'ankle_left_y', 
                                'foot_right_x', 'foot_right_y', 'foot_left_x', 'foot_left_y',
                                'hip_knee_right', 'hip_knee_left', 'knee_ankle_right', 'knee_ankle_left',
                                'time_stamp', 'user']], skiprows = 1)  
                            k_dataframe = k_dataframe.drop(['no' . upper()], axis=1)
                            kinect_concat.append(k_dataframe)
                    
            ## Concat for deep learning 
            in_columns = [x.upper() for x in['r_heel', 'r_thumb', 'r_inner_ball', 'r_outer_ball', 'l_heel', 'l_thumb', 'l_inner_ball', 'l_outer_ball', 'time', 'name']]
            kin_columns = [x.upper() for x in['user', 
                        'spine_base_x', 'spine_base_y', 'spine_mid_x', 'spine_mid_y', 
                        'hip_right_x', 'hip_right_y', 'hip_left_x', 'hip_left_y', 
                        'knee_right_x', 'knee_right_y', 'knee_left_x', 'knee_left_y',
                        'ankle_right_x', 'ankle_right_y', 'ankle_left_x', 'ankle_left_y', 
                        'foot_right_x', 'foot_right_y', 'foot_left_x', 'foot_left_y',
                        'hip_knee_right', 'hip_knee_left', 'knee_ankle_right', 'knee_ankle_left',
                        'time_stamp']]
            
            in_time = []
            for i in range(len(kinect_concat)): 
                temp = [] 
                for l in range(len(kinect_concat[i])):  
                    kin_time = kinect_concat[i]['time_stamp' . upper()].values[l] 
                    for m in range(len(insoles_concat[i])):
                        in_time = insoles_concat[i]['time' . upper()].values[m]  
                        if kin_time[kin_time.index(':'):] == in_time[in_time.index(':'):]: # Modified the time for similarity checking
                            ext = kinect_concat[i][kin_columns].values[l].tolist()
                            ext.extend(insoles_concat[i][in_columns].values[m].tolist())
                            temp.append(ext)
                        
                kin_in.append(temp)
                
        # Concat it
        if len(kin_in) > 1:
            kin_in = np.concatenate(kin_in).tolist()
            
        count = 1
        for i in range(len(kin_in)):
            kin_in[i].insert(0, count)
            count += 1
        
        ## Concat column
        columns_ = kin_columns
        columns_.extend(in_columns)
        columns_.insert(0, 'no' . upper())
          
        ## Put number
        get = pd.DataFrame(kin_in, columns=columns_)
        get.to_csv('C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Concatenation/{}.csv' . format('Master_data'), index=False)

    def run(self):
        self.concat()
    
app = DataGeneration()
app.run()