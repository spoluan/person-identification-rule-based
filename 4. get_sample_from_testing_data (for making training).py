# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 23:30:18 2018

@author: yzucsemss
""" 

import pandas as pd
import math, os

def get_length(val_a, val_b, val_a2, val_b2):  
    opposite = val_a2 - val_a
    adjacent = val_b2 - val_b  
    hypotenuse = math.sqrt(pow(opposite, 2) + pow(adjacent, 2)) 
    degrees = math.asin(opposite / hypotenuse) * 180 / math.pi 
    return degrees
     
    
address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Concatenation'

## Load dataset
find = '{}/{}' . format(address, 'Master_data.csv') 
data = pd.read_csv('{}' . format(find))  
 
right = []
left = []
normal = []
   
##### The right sliping    
# Slip right and left insoles data in every one pair of skeleton coordinate
data_arrangement = []
for i in range(len(data.values)): 
        
     # Insoles processing
     in_right = data['R_HEEL'][i] + data['R_THUMB'][i] + data['R_INNER_BALL'][i] + data['R_OUTER_BALL'][i]
     in_left = data['L_HEEL'][i] + data['L_THUMB'][i] + data['L_INNER_BALL'][i] + data['L_OUTER_BALL'][i]
     in_status = in_right - in_left
     
     # Skeleton processing
     val_a_r = data['HIP_RIGHT_X'][i]
     val_b_r = data['HIP_RIGHT_Y'][i]
     val_a2_r = data['ANKLE_RIGHT_X'][i]
     val_b2_r = data['ANKLE_RIGHT_Y'][i]
     sk_right = get_length(val_a_r, val_b_r, val_a2_r, val_b2_r)
      
     val_a_l = data['HIP_LEFT_X'][i]
     val_b_l = data['HIP_LEFT_Y'][i]
     val_a2_l = data['ANKLE_LEFT_X'][i]
     val_b2_l = data['ANKLE_LEFT_Y'][i]
     sk_left = get_length(val_a_l, val_b_l, val_a2_l, val_b2_l)
     
     status = []
     if sk_right < 0 and sk_left < 0 and abs(in_left - in_right) > 70 and in_left < in_right:
         status = data.values[i].tolist()[0:len(data.values[i].tolist()) - 1]
         status.append('Right') 
         right.append(status)
     elif sk_right >= 0 and sk_left <= 0 and abs(in_left - in_right) <= 70:
         status = data.values[i].tolist()[0:len(data.values[i].tolist()) - 1]
         status.append('Normal') 
         normal.append(status)
     elif sk_right > 0 and sk_left > 0 and abs(in_left - in_right) > 70 and in_left > in_right:
         status = data.values[i].tolist()[0:len(data.values[i].tolist()) - 1]
         status.append('Left') 
         left.append(status)
         
index = [43, 44, 45]
add_right = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Technical Thesis\\Final Backup\\Backup {} Right/Working Directory/Concatination' . format(index[0])
os.makedirs(add_right) 
add_normal = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Technical Thesis\\Final Backup/Backup {} Normal/Working Directory/Concatination' . format(index[1])
os.makedirs(add_normal) 
add_left = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Technical Thesis\\Final Backup/Backup {} Left/Working Directory/Concatination' . format(index[2])
os.makedirs(add_left) 
colnames = data.columns.tolist() 
get_right = pd.DataFrame(right, columns=colnames)
get_right.to_csv('{}/{}.csv' . format(add_right, 'Master'), index=False)
get_normal = pd.DataFrame(normal, columns=colnames)
get_normal.to_csv('{}/{}.csv' . format(add_normal, 'Master'), index=False)
get_left = pd.DataFrame(left, columns=colnames)
get_left.to_csv('{}/{}.csv' . format(add_left, 'Master'), index=False)

        
      



             