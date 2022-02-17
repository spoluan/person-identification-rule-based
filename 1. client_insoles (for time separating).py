# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:39:09 2018

@author: Sevendi Eldrige Rifki Poluan
"""  

import requests, json 
import pandas as pd
import numpy as np  
import math
import os

class Client(object):
    
    def __init__(self):
        print('## Start . . .')
    
    def createTable(self):
        url = 'https://insoles.herokuapp.com/req'  
        
        # Create table
        data = {} 
        data['METHOD'] = 'CREATE' 
        json_data = json.dumps(data) 
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=json.loads(json_data), headers=headers) # Refs: http://docs.python-requests.org/en/v0.10.7/user/quickstart/#make-a-get-request
        r.json() 
        
    def insertData(self):
        url = 'https://insoles.herokuapp.com/req'  
        # Insert data
        data = {} 
        data['METHOD'] = 'INSERT' 
        data['R_HEEL'] = '45'
        data['R_THUMB'] = '23' 
        data['R_INNER_BALL'] = '56'
        data['R_OUTER_BALL'] = '67'
        data['L_HEEL'] = '34'
        data['L_THUMB'] = '12' 
        data['L_INNER_BALL'] = '34' 
        data['L_OUTER_BALL'] = '12'
        data['TIME'] = '01:08:38' 
        data['NAME'] = 'SEVENDI' 
        
        json_data = json.dumps(data) 
        r = requests.post(url, json=json.loads(json_data))
        r.json() 
    
    def removeFiles(self):
#        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Raw Data/'
#        file = os.listdir(address)
#        for i in file:
#            os.remove("{}{}" . format(address, i))
#            
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Insoles/'
        file = os.listdir(address)
        for i in file:
            os.remove("{}{}" . format(address, i))
            
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Kinect/'
        file = os.listdir(address)
        for i in file:
            os.remove("{}{}" . format(address, i))
            
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Comparison/'
        file = os.listdir(address)
        for i in file:
            os.remove("{}{}" . format(address, i))   

        
        self.deleteInsoles()
        
    # Delete data
    def deleteInsoles(self):
        url = 'https://insoles.herokuapp.com/req'  
        data = {} 
        data['METHOD'] = 'DELETE' 
        json_data = json.dumps(data) 
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=json.loads(json_data), headers=headers)
        r.json()
    
    def extractInsoles(self, signed, status=True):    
        url = 'https://insoles.herokuapp.com/req'  
        
        all_time = []
        get_df = []
        if status == True:
            ## Get data from heroku
            data = {} 
            data['METHOD'] = 'VIEW'  
            json_data = json.dumps(data) 
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, json=json.loads(json_data), headers=headers)
            r = r.json()['STATUS']
             
            ## Read all detected users
            get_user = []
            for i in r:
                data = i[0] # [{}]
                if data['NAME'] not in get_user:
                    get_user.append(data['NAME'])
                                 
        
            ## Distinguis all user with its data
            separate = [] 
            for x in get_user:
                temp = []
                
                for i in r:
                    data = i[0] # [{}]
                    if data['NAME'] == x:
                        temp.append([data['R_HEEL'], data['R_THUMB'], data['R_INNER_BALL'], data['R_OUTER_BALL'], data['L_HEEL'], data['L_THUMB'], data['L_INNER_BALL'], data['L_OUTER_BALL'], data['TIME'], data['NAME']])
                            
                if len(temp) > 0:
                    separate.append(temp)
            
            ## Sort
            t_sep = []
            for i in range(len(separate)):
                sorting = pd.DataFrame(np.array(separate[i]).tolist(), columns=['R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME'])
                sorting = sorting.sort_values('TIME')
                
                t_sep.append(np.array(sorting).tolist())  
                
            ## Get samples 
            get_d = []
            start_index = 0
            end_index = 0
            check_signed = ''
            loop = 1  
            for i in range(len(t_sep)):
                handle = 0
                for j in range(len(t_sep[i])):
                    second = t_sep[i][j][8].split(':')[-1]
                    minute = t_sep[i][j][8].split(':')[1]
                    ch = '{}:{}' . format(minute, second)
                    if second == signed:
                        if check_signed != ch:
                            check_signed = ch
                            if loop != 0:
                                start_index = j 
                                loop -= 1
                            elif loop == 0:
                                end_index = j
                                break
                    handle = j
                if end_index == 0:
                    end_index = handle
                get_d.append(t_sep[i][start_index:end_index])   
                
            
            ## Store raw data
            for i in range(len(t_sep)):
                count = 1
                for j in range(len(t_sep[i])):
                    t_sep[i][j].insert(0, count) 
                    count += 1 
            for k in range(len(t_sep)): 
                get = pd.DataFrame(np.array(t_sep[k]).tolist(), columns=['NO', 'R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME'])
                get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Raw Data/{}_{}.csv' . format('Insoles raw data', k), index=False)
          
         
            ## Get all time
            for i in range(len(get_d)):
                temp = []
                for j in range(len(get_d[i])):
                    if get_d[i][j][9] not in temp: temp.append(get_d[i][j][9])
                all_time.append(temp)
            
            
            
            # Cast to dataframe
            for i in range(len(get_d)):
                get_df.append(pd.DataFrame(get_d[i], columns=['NO', 'R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME']))
        else:
            address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Raw Data/'
        
            file = os.listdir(address)
            for i in file:
                if 'csv' in i:
                    if 'Insoles' in i:
                        file_kinect_name = i
             
            ####### Specify the column for data reading of csv file #######
            colnames = [x.upper() for x in['NO', 'R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME']]
            
            ####### Read the data from csv file #######
            get_df = [pd.read_csv('{}{}' . format(address, file_kinect_name), names = colnames, skiprows = 1)]
         
            ## Get samples  
            t_sep = [np.array(get_df[0]).tolist()]
            get_d = []
            start_index = 0
            end_index = 0
            check_signed = ''
            loop = 1  
            for i in range(len(t_sep)):
                handle = 0
                for j in range(len(t_sep[i])):
                    second = t_sep[i][j][9].split(':')[-1]
                    minute = t_sep[i][j][9].split(':')[1]
                    ch = '{}:{}' . format(minute, second)
                    if second == signed:
                        if check_signed != ch:
                            check_signed = ch
                            if loop != 0:
                                start_index = j 
                                loop -= 1
                            elif loop == 0:
                                end_index = j
                                break
                    handle = j
                if end_index == 0:
                    end_index = handle
                get_d.append(t_sep[i][start_index:end_index])   
                
            for i in range(len(get_d)):
                temp = []
                for j in range(len(get_d[i])):
                    if get_d[i][j][9] not in temp: temp.append(get_d[i][j][9])
                all_time.append(temp)
            
            
        # Smooth the data 
        t_temp = []
        for i in range(len(all_time)):
            temp = []
            for j in range(len(all_time[i])):
                for k in range(len(get_df)):
                    get_f = get_df[k][['R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME']].query('TIME == ["{}"]' . format(all_time[i][j]))
                    milisecond_ = 1
                    if len(get_f) > 8:
                        R_HEEL = []
                        R_THUMB = []
                        R_INNER_BALL = []
                        R_OUTER_BALL = []
                        L_HEEL = []
                        L_THUMB = []
                        L_INNER_BALL = []
                        L_OUTER_BALL = [] 
                        for l in range(len(get_f)):
                            if l < 11:
                                if l % 2 != 0:
                                    R_HEEL.append(int(get_f['R_HEEL'].values[l]))
                                    R_THUMB.append(int(get_f['R_THUMB'].values[l]))
                                    R_INNER_BALL.append(int(get_f['R_INNER_BALL'].values[l]))
                                    R_OUTER_BALL.append(int(get_f['R_OUTER_BALL'].values[l]))
                                    L_HEEL.append(int(get_f['L_HEEL'].values[l]))
                                    L_THUMB.append(int(get_f['L_THUMB'].values[l]))
                                    L_INNER_BALL.append(int(get_f['L_INNER_BALL'].values[l]))
                                    L_OUTER_BALL.append(int(get_f['L_OUTER_BALL'].values[l])) 
                                    
                                    RHEEL = int(sum(R_HEEL) / len(R_HEEL))
                                    RTHUMB = int(sum(R_THUMB) / len(R_THUMB))
                                    RINNER_BALL = int(sum(R_INNER_BALL) / len(R_INNER_BALL))
                                    ROUTER_BALL = int(sum(R_OUTER_BALL) / len(R_OUTER_BALL))
                                    LHEEL = int(sum(L_HEEL) / len(L_HEEL))
                                    LTHUMB = int(sum(L_THUMB) / len(L_THUMB))
                                    LINNER_BALL = int(sum(L_INNER_BALL) / len(L_INNER_BALL))
                                    LOUTER_BALL = int(sum(L_OUTER_BALL) / len(L_OUTER_BALL)) 
                                        
                                    temp.append([RHEEL, RTHUMB, RINNER_BALL, ROUTER_BALL, LHEEL, LTHUMB, LINNER_BALL, LOUTER_BALL, '{}:{}' . format(get_f['TIME'].values[l], milisecond_), get_f['NAME'].values[l]])
                                    
                                    milisecond_ += 1
                                    
                                    R_HEEL = []
                                    R_THUMB = []
                                    R_INNER_BALL = []
                                    R_OUTER_BALL = []
                                    L_HEEL = []
                                    L_THUMB = []
                                    L_INNER_BALL = []
                                    L_OUTER_BALL = [] 
                                     
                                    
                                if l % 2 == 0:
                                    if len(R_HEEL) == 0: # Check if already have a data or not
                                        R_HEEL.append(int(get_f['R_HEEL'].values[l]))
                                        R_THUMB.append(int(get_f['R_THUMB'].values[l]))
                                        R_INNER_BALL.append(int(get_f['R_INNER_BALL'].values[l]))
                                        R_OUTER_BALL.append(int(get_f['R_OUTER_BALL'].values[l]))
                                        L_HEEL.append(int(get_f['L_HEEL'].values[l]))
                                        L_THUMB.append(int(get_f['L_THUMB'].values[l]))
                                        L_INNER_BALL.append(int(get_f['L_INNER_BALL'].values[l]))
                                        L_OUTER_BALL.append(int(get_f['L_OUTER_BALL'].values[l])) 
                                        
                                    else: # Excecute when have already one data
                                        R_HEEL.append(int(get_f['R_HEEL'].values[l]))
                                        R_THUMB.append(int(get_f['R_THUMB'].values[l]))
                                        R_INNER_BALL.append(int(get_f['R_INNER_BALL'].values[l]))
                                        R_OUTER_BALL.append(int(get_f['R_OUTER_BALL'].values[l]))
                                        L_HEEL.append(int(get_f['L_HEEL'].values[l]))
                                        L_THUMB.append(int(get_f['L_THUMB'].values[l]))
                                        L_INNER_BALL.append(int(get_f['L_INNER_BALL'].values[l]))
                                        L_OUTER_BALL.append(int(get_f['L_OUTER_BALL'].values[l])) 
                                            
                                        RHEEL = int(sum(R_HEEL) / len(R_HEEL))
                                        RTHUMB = int(sum(R_THUMB) / len(R_THUMB))
                                        RINNER_BALL = int(sum(R_INNER_BALL) / len(R_INNER_BALL))
                                        ROUTER_BALL = int(sum(R_OUTER_BALL) / len(R_OUTER_BALL))
                                        LHEEL = int(sum(L_HEEL) / len(L_HEEL))
                                        LTHUMB = int(sum(L_THUMB) / len(L_THUMB))
                                        LINNER_BALL = int(sum(L_INNER_BALL) / len(L_INNER_BALL))
                                        LOUTER_BALL = int(sum(L_OUTER_BALL) / len(L_OUTER_BALL)) 
                                            
                                        temp.append([RHEEL, RTHUMB, RINNER_BALL, ROUTER_BALL, LHEEL, LTHUMB, LINNER_BALL, LOUTER_BALL, '{}:{}' . format(get_f['TIME'].values[l], milisecond_), get_f['NAME'].values[l]])
                                        
                                        milisecond_ += 1
                                            
                                        R_HEEL = []
                                        R_THUMB = []
                                        R_INNER_BALL = []
                                        R_OUTER_BALL = []
                                        L_HEEL = []
                                        L_THUMB = []
                                        L_INNER_BALL = []
                                        L_OUTER_BALL = [] 
                                        
                                    if len(get_f) < 10 and l == len(get_f) - 1:
                                        RHEEL = int(sum(R_HEEL) / len(R_HEEL))
                                        RTHUMB = int(sum(R_THUMB) / len(R_THUMB))
                                        RINNER_BALL = int(sum(R_INNER_BALL) / len(R_INNER_BALL))
                                        ROUTER_BALL = int(sum(R_OUTER_BALL) / len(R_OUTER_BALL))
                                        LHEEL = int(sum(L_HEEL) / len(L_HEEL))
                                        LTHUMB = int(sum(L_THUMB) / len(L_THUMB))
                                        LINNER_BALL = int(sum(L_INNER_BALL) / len(L_INNER_BALL))
                                        LOUTER_BALL = int(sum(L_OUTER_BALL) / len(L_OUTER_BALL)) 
                                            
                                        temp.append([RHEEL, RTHUMB, RINNER_BALL, ROUTER_BALL, LHEEL, LTHUMB, LINNER_BALL, LOUTER_BALL, '{}:{}' . format(get_f['TIME'].values[l], milisecond_), get_f['NAME'].values[l]])
                                        
                                        milisecond_ += 1
                                        
                                        R_HEEL = []
                                        R_THUMB = []
                                        R_INNER_BALL = []
                                        R_OUTER_BALL = []
                                        L_HEEL = []
                                        L_THUMB = []
                                        L_INNER_BALL = []
                                        L_OUTER_BALL = [] 
                            
                    if len(get_f) < 9: 
                        try:
                            for l in range(5): 
                                temp.append([
                                        int(get_f['R_HEEL'].values[l]), 
                                        int(get_f['R_THUMB'].values[l]),
                                        int(get_f['R_INNER_BALL'].values[l]),
                                        int(get_f['R_OUTER_BALL'].values[l]),
                                        int(get_f['L_HEEL'].values[l]),
                                        int(get_f['L_THUMB'].values[l]),
                                        int(get_f['L_INNER_BALL'].values[l]),
                                        int(get_f['L_OUTER_BALL'].values[l]),
                                        '{}:{}' . format(get_f['TIME'].values[l], milisecond_),
                                        get_f['NAME'].values[l]])
    
                                milisecond_ += 1
                        except:
                            pass
                                
            t_temp.append(temp)
        
     
        ## Sum all pressure data
        fix = []
        for i in t_temp:
            temp = [] 
            count = 1
            for j in i:
                r_total = int(j[0]) + int(j[1]) + int(j[2]) + int(j[3])
                l_total = int(j[4]) + int(j[5]) + int(j[6]) + int(j[7])
                if abs(l_total - r_total) <= 70:
                    status = 'NORMAL'
                elif abs(l_total - r_total) > 70:
                    if r_total > l_total:
                        status = 'RIGHT'
                    if l_total > r_total:
                        status = 'LEFT' 
                temp.append([count, status, j[8], j[9], r_total, l_total, abs(r_total-l_total)]) 
                count += 1
            fix.append(temp)
            
        
        ## Smooth the data (if there is one alone replace it)
        for i in range(len(fix)):
            for j in range(len(fix[i])):
                if j < len(fix[i]) - 1:
                    if fix[i][j][1] != fix[i][j - 1][1] and fix[i][j - 1][1] == fix[i][j + 1][1]:
                        fix[i][j][1] = fix[i][j - 1][1]
                        
        ## Store as a sample data
        for k in range(len(fix)): 
            get = pd.DataFrame(np.array(fix[k]).tolist(), columns=['NO', 'STATUS', 'TIME', 'NAME', 'R_TOTAL', 'L_TOTAL', 'ABS_SUB'])
            get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Insoles/{}_{}.csv' . format(fix[k][0][3], signed), index=False)
     
        
        ## Store sample data to csv 
        for i in range(len(t_temp)):
            count = 1
            for j in range(len(t_temp[i])):
                t_temp[i][j].insert(0, count) 
                count += 1 
        for k in range(len(get_d)): 
            get = pd.DataFrame(np.array(t_temp[k]).tolist(), columns=['NO', 'R_HEEL', 'R_THUMB', 'R_INNER_BALL', 'R_OUTER_BALL', 'L_HEEL', 'L_THUMB', 'L_INNER_BALL', 'L_OUTER_BALL', 'TIME', 'NAME'])
            get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Insoles/{}_{}.csv' . format('Master_insoles', k), index=False)
      
        
        print('## Done insoles')
    ###################################################################################
    
    
    def getLength(self, val_a, val_b, val_a2, val_b2): 
        
        opposite = val_a2 - val_a
        adjacent = val_b2 - val_b
        hypotenuse = math.sqrt(pow(opposite, 2) + pow(adjacent, 2))
        
        degrees = math.asin(opposite / hypotenuse) * 180 / math.pi
        return opposite, adjacent, hypotenuse, degrees
    
    def setJoint(self, dataframe, index_frame, joint_1, joint_2, joint_3, joint_4):
        x1 = dataframe[['{}' . format(joint_1), 'count_frame']].query('count_frame == ["{}"]' . format(index_frame))['{}' . format(joint_1)]
        y1 = dataframe[['{}'. format(joint_2), 'count_frame']].query('count_frame == ["{}"]' . format(index_frame))['{}' . format(joint_2)]
        
        x2 = dataframe[['{}' . format(joint_3), 'count_frame']].query('count_frame == ["{}"]' . format(index_frame))['{}' . format(joint_3)]
        y2 = dataframe[['{}'. format(joint_4), 'count_frame']].query('count_frame == ["{}"]' . format(index_frame))['{}' . format(joint_4)]
        
        return x1, y1, x2, y2
    
    def extractVideo(self, signed): 
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Raw Data/'
        
        file = os.listdir(address)
        for i in file:
            if 'csv' in i:
                if 'Insoles' not in i:
                    file_kinect_name = i
         
        ####### Specify the column for data reading of csv file #######
        colnames = [x.upper() for x in['user', 
                    'spine_base_x', 'spine_base_y', 'spine_mid_x', 'spine_mid_y',
                    'hip_right_x', 'hip_right_y', 'hip_left_x', 'hip_left_y', 
                    'knee_right_x', 'knee_right_y', 'knee_left_x', 'knee_left_y',
                    'ankle_right_x', 'ankle_right_y', 'ankle_left_x', 'ankle_left_y', 
                    'foot_right_x', 'foot_right_y', 'foot_left_x', 'foot_left_y',
                    'hip_knee_right', 'hip_knee_left', 'knee_ankle_right', 'knee_ankle_left', 
                    'time_stamp', 'count_frame']]
        
        ####### Read the data from csv file #######
        dataframe = pd.read_csv('{}{}' . format(address, file_kinect_name), names = colnames, skiprows = 1)  
     
        ## Get first index of time_stamp as signed 
#        signed = '35'
        loop = 1 
        count_time = dataframe[['TIME_STAMP']]
        start_index = 0
        end_index = 0
        check_signed = ''
        for i in range(len(count_time)):
            minute = count_time['TIME_STAMP'][i].split(':')[1]
            second = count_time['TIME_STAMP'][i].split(':')[2]
            ch = '{}:{}' . format(minute, second)
            if second == signed: 
                if check_signed != ch: 
                    check_signed = ch
                    if loop != 0:
                        start_index = i 
                        loop -= 1
                    elif loop == 0:
                        end_index = i
                        break 
                    
        ## Get data only for the certain index
        dataframe = dataframe[start_index:end_index]  
        
        # Read all detected user
        all_user = []
        for i in range(len(dataframe)):
            if dataframe['USER'].values[i] not in all_user: all_user.append(dataframe['user' . upper()].values[i])
        
        # Distinguish all user with its data
        separate = []
        for i in all_user:
            temp = []
            for j in range(len(dataframe)):
                if dataframe['USER'].values[i] == i:
                    get = pd.DataFrame() 
                    temp.append(dataframe[j:(j+1)].values[0])
            separate.append(temp)
        
        ## Smooth the data 
        smooth = []
        for i in range(len(separate)): 
            
            spine_base_x = []
            spine_base_y = [] 
            spine_mid_x = [] 
            spine_mid_y = [] 
            
            hip_right_x = [] 
            hip_right_y = [] 
            hip_left_x = [] 
            hip_left_y = []
            
            knee_right_x = [] 
            knee_right_y = [] 
            knee_left_x = [] 
            knee_left_y = []
            
            ankle_right_x = [] 
            ankle_right_y = [] 
            ankle_left_x = [] 
            ankle_left_y = [] 
            
            foot_right_x = [] 
            foot_right_y = [] 
            foot_left_x = [] 
            foot_left_y = []
            
            hip_knee_right = [] 
            hip_knee_left = [] 
            knee_ankle_right = [] 
            knee_ankle_left = [] 
             
            check = ''
            result = []
            for j in range(len(separate[i])): 
                milisecond = separate[0][j][25].split(':')[3][0]
                
                if milisecond != check:
                    check = milisecond
                    
                    if len(spine_base_x) > 0:
                        spine_base_x = int(sum(spine_base_x) / len(spine_base_x))
                        spine_base_y = int(sum(spine_base_y) / len(spine_base_y))
                        spine_mid_x = int(sum(spine_mid_x) / len(spine_mid_x))
                        spine_mid_y = int(sum(spine_mid_y) / len(spine_mid_y)) 
                        
                        hip_right_x = int(sum(hip_right_x) / len(hip_right_x))
                        hip_right_y = int(sum(hip_right_y) / len(hip_right_y))
                        hip_left_x = int(sum(hip_left_x) / len(hip_left_x))
                        hip_left_y = int(sum(hip_left_y) / len(hip_left_y))
                        
                        knee_right_x = int(sum(knee_right_x) / len(knee_right_x))
                        knee_right_y = int(sum(knee_right_y) / len(knee_right_y))
                        knee_left_x = int(sum(knee_left_x) / len(knee_left_x))
                        knee_left_y = int(sum(knee_left_y) / len(knee_left_y))
                        
                        ankle_right_x = int(sum(ankle_right_x) / len(ankle_right_x))
                        ankle_right_y = int(sum(ankle_right_y) / len(ankle_right_y))
                        ankle_left_x = int(sum(ankle_left_x) / len(ankle_left_x))
                        ankle_left_y = int(sum(ankle_left_y) / len(ankle_left_y))
                        
                        foot_right_x = int(sum(foot_right_x) / len(foot_right_x))
                        foot_right_y = int(sum(foot_right_y) / len(foot_right_y))
                        foot_left_x = int(sum(foot_left_x) / len(foot_left_x))
                        foot_left_y = int(sum(foot_left_y) / len(foot_left_y))
                        
                        hip_knee_right = int(sum(hip_knee_right) / len(hip_knee_right))
                        hip_knee_left = int(sum(hip_knee_left) / len(hip_knee_left))
                        knee_ankle_right = int(sum(knee_ankle_right) / len(knee_ankle_right))
                        knee_ankle_left = int(sum(knee_ankle_left) / len(knee_ankle_left)) 
                        
                        result.append([
                                separate[i][j - 1][0],
                                spine_base_x, spine_base_y, spine_mid_x, spine_mid_y,
                                hip_right_x, hip_right_y, hip_left_x, hip_left_y,
                                knee_right_x, knee_right_y, knee_left_x, knee_left_y,
                                ankle_right_x, ankle_right_y, ankle_left_x, ankle_left_y,
                                foot_right_x, foot_right_y, foot_left_x, foot_left_y,
                                hip_knee_right, hip_knee_left, knee_ankle_right, knee_ankle_left,
                                separate[i][j - 1][25][0:8] 
                            ])
                        
                        spine_base_x = []
                        spine_base_y = [] 
                        spine_mid_x = [] 
                        spine_mid_y = [] 
                        
                        hip_right_x = [] 
                        hip_right_y = [] 
                        hip_left_x = [] 
                        hip_left_y = []
                        
                        knee_right_x = [] 
                        knee_right_y = [] 
                        knee_left_x = [] 
                        knee_left_y = []
                        
                        ankle_right_x = [] 
                        ankle_right_y = [] 
                        ankle_left_x = [] 
                        ankle_left_y = [] 
                        
                        foot_right_x = [] 
                        foot_right_y = [] 
                        foot_left_x = [] 
                        foot_left_y = []
                        
                        hip_knee_right = [] 
                        hip_knee_left = [] 
                        knee_ankle_right = [] 
                        knee_ankle_left = [] 
                      
                
                if milisecond == check:
                    spine_base_x.append(separate[i][j][1]) 
                    spine_base_y.append(separate[i][j][2]) 
                    spine_mid_x.append(separate[i][j][3]) 
                    spine_mid_y.append(separate[i][j][4])
                    
                    hip_right_x.append(separate[i][j][5]) 
                    hip_right_y.append(separate[i][j][6]) 
                    hip_left_x.append(separate[i][j][7]) 
                    hip_left_y.append(separate[i][j][8])
                    
                    knee_right_x.append(separate[i][j][9]) 
                    knee_right_y.append(separate[i][j][10]) 
                    knee_left_x.append(separate[i][j][11]) 
                    knee_left_y.append(separate[i][j][12])
                    
                    ankle_right_x.append(separate[i][j][13]) 
                    ankle_right_y.append(separate[i][j][14]) 
                    ankle_left_x.append(separate[i][j][15]) 
                    ankle_left_y.append(separate[i][j][16]) 
                    
                    foot_right_x.append(separate[i][j][17]) 
                    foot_right_y.append(separate[i][j][18]) 
                    foot_left_x.append(separate[i][j][19]) 
                    foot_left_y.append(separate[i][j][20])
                    
                    hip_knee_right.append(separate[i][j][21]) 
                    hip_knee_left.append(separate[i][j][22]) 
                    knee_ankle_right.append(separate[i][j][23]) 
                    knee_ankle_left.append(separate[i][j][24])
                     
                    
                    if len(separate[i]) - 1 == j:
                        
                        spine_base_x = int(sum(spine_base_x) / len(spine_base_x))
                        spine_base_y = int(sum(spine_base_y) / len(spine_base_y))
                        spine_mid_x = int(sum(spine_mid_x) / len(spine_mid_x))
                        spine_mid_y = int(sum(spine_mid_y) / len(spine_mid_y)) 
                        
                        hip_right_x = int(sum(hip_right_x) / len(hip_right_x))
                        hip_right_y = int(sum(hip_right_y) / len(hip_right_y))
                        hip_left_x = int(sum(hip_left_x) / len(hip_left_x))
                        hip_left_y = int(sum(hip_left_y) / len(hip_left_y))
                        
                        knee_right_x = int(sum(knee_right_x) / len(knee_right_x))
                        knee_right_y = int(sum(knee_right_y) / len(knee_right_y))
                        knee_left_x = int(sum(knee_left_x) / len(knee_left_x))
                        knee_left_y = int(sum(knee_left_y) / len(knee_left_y))
                        
                        ankle_right_x = int(sum(ankle_right_x) / len(ankle_right_x))
                        ankle_right_y = int(sum(ankle_right_y) / len(ankle_right_y))
                        ankle_left_x = int(sum(ankle_left_x) / len(ankle_left_x))
                        ankle_left_y = int(sum(ankle_left_y) / len(ankle_left_y))
                        
                        foot_right_x = int(sum(foot_right_x) / len(foot_right_x))
                        foot_right_y = int(sum(foot_right_y) / len(foot_right_y))
                        foot_left_x = int(sum(foot_left_x) / len(foot_left_x))
                        foot_left_y = int(sum(foot_left_y) / len(foot_left_y))
                        
                        hip_knee_right = int(sum(hip_knee_right) / len(hip_knee_right))
                        hip_knee_left = int(sum(hip_knee_left) / len(hip_knee_left))
                        knee_ankle_right = int(sum(knee_ankle_right) / len(knee_ankle_right))
                        knee_ankle_left = int(sum(knee_ankle_left) / len(knee_ankle_left)) 
                        
                        result.append([
                                separate[i][j - 1][0],
                                spine_base_x, spine_base_y, spine_mid_x, spine_mid_y,
                                hip_right_x, hip_right_y, hip_left_x, hip_left_y,
                                knee_right_x, knee_right_y, knee_left_x, knee_left_y,
                                ankle_right_x, ankle_right_y, ankle_left_x, ankle_left_y,
                                foot_right_x, foot_right_y, foot_left_x, foot_left_y,
                                hip_knee_right, hip_knee_left, knee_ankle_right, knee_ankle_left,
                                separate[i][j - 1][25][0:8] 
                            ])
                        
                        spine_base_x = []
                        spine_base_y = [] 
                        spine_mid_x = [] 
                        spine_mid_y = [] 
                        
                        hip_right_x = [] 
                        hip_right_y = [] 
                        hip_left_x = [] 
                        hip_left_y = []
                        
                        knee_right_x = [] 
                        knee_right_y = [] 
                        knee_left_x = [] 
                        knee_left_y = []
                        
                        ankle_right_x = [] 
                        ankle_right_y = [] 
                        ankle_left_x = [] 
                        ankle_left_y = [] 
                        
                        foot_right_x = [] 
                        foot_right_y = [] 
                        foot_left_x = [] 
                        foot_left_y = []
                        
                        hip_knee_right = [] 
                        hip_knee_left = [] 
                        knee_ankle_right = [] 
                        knee_ankle_left = [] 
                        
            smooth.append(result)
            
        ## Get all time
        all_time = []
        for i in range(len(smooth)):
            temp = []
            for j in range(len(smooth[i])):
                if smooth[i][j][25] not in temp: temp.append(smooth[i][j][25])
            all_time.append(temp)
        
        # Cast to dataframe
        get_df = []
        for i in range(len(smooth)):
            get_df.append(pd.DataFrame(smooth[i], columns=colnames[0:26]))
             
        # Smooth the data 
        t_temp = []
        for i in range(len(all_time)):
            temp = []
            for j in range(len(all_time[i])):
                for k in range(len(get_df)):
                    get_f = get_df[k][colnames[0:26]].query('TIME_STAMP == ["{}"]' . format(all_time[i][j]))
     
                    milisecond = 1
                    if len(get_f) > 8:
                        
                        spine_base_x = []
                        spine_base_y = [] 
                        spine_mid_x = [] 
                        spine_mid_y = [] 
                        
                        hip_right_x = [] 
                        hip_right_y = [] 
                        hip_left_x = [] 
                        hip_left_y = []
                        
                        knee_right_x = [] 
                        knee_right_y = [] 
                        knee_left_x = [] 
                        knee_left_y = []
                        
                        ankle_right_x = [] 
                        ankle_right_y = [] 
                        ankle_left_x = [] 
                        ankle_left_y = [] 
                        
                        foot_right_x = [] 
                        foot_right_y = [] 
                        foot_left_x = [] 
                        foot_left_y = []
                        
                        hip_knee_right = [] 
                        hip_knee_left = [] 
                        knee_ankle_right = [] 
                        knee_ankle_left = [] 
                        
                        for l in range(len(get_f)):
                            if l < 11:
                                if l % 2 != 0:
                                    
                                    spine_base_x.append(int(get_f['spine_base_x' . upper()].values[l]))
                                    spine_base_y.append(int(get_f['spine_base_y' . upper()].values[l]))
                                    spine_mid_x.append(int(get_f['spine_mid_x' . upper()].values[l]))
                                    spine_mid_y.append(int(get_f['spine_mid_y' . upper()].values[l]))
                                    hip_right_x.append(int(get_f['hip_right_x' . upper()].values[l]))
                                    hip_right_y.append(int(get_f['hip_right_y' . upper()].values[l]))
                                    hip_left_x.append(int(get_f['hip_left_x' . upper()].values[l]))
                                    hip_left_y.append(int(get_f['hip_left_y' . upper()].values[l])) 
                                    knee_right_x.append(int(get_f['knee_right_x' . upper()].values[l]))
                                    knee_right_y.append(int(get_f['knee_right_y' . upper()].values[l]))
                                    knee_left_x.append(int(get_f['knee_left_x' . upper()].values[l]))
                                    knee_left_y.append(int(get_f['knee_left_y' . upper()].values[l]))
                                    ankle_right_x.append(int(get_f['ankle_right_x' . upper()].values[l]))
                                    ankle_right_y.append(int(get_f['ankle_right_y' . upper()].values[l]))
                                    ankle_left_x.append(int(get_f['ankle_left_x' . upper()].values[l]))
                                    ankle_left_y.append(int(get_f['ankle_left_y' . upper()].values[l])) 
                                    foot_right_x.append(int(get_f['foot_right_x' . upper()].values[l]))
                                    foot_right_y.append(int(get_f['foot_right_y' . upper()].values[l]))
                                    foot_left_x.append(int(get_f['foot_left_x' . upper()].values[l]))
                                    foot_left_y.append(int(get_f['foot_left_y' . upper()].values[l])) 
                                    hip_knee_right.append(int(get_f['hip_knee_right' . upper()].values[l])) 
                                    hip_knee_left.append(int(get_f['hip_knee_left' . upper()].values[l])) 
                                    knee_ankle_right.append(int(get_f['knee_ankle_right' . upper()].values[l])) 
                                    knee_ankle_left.append(int(get_f['knee_ankle_left' . upper()].values[l])) 
                                    
                                    
                                    dspine_base_x = int(sum(spine_base_x) / len(spine_base_x))
                                    dspine_base_y = int(sum(spine_base_y) / len(spine_base_y))
                                    spine_mid_x = int(sum(spine_mid_x) / len(spine_mid_x))
                                    spine_mid_y = int(sum(spine_mid_y) / len(spine_mid_y))
                                    dhip_right_x = int(sum(hip_right_x) / len(hip_right_x))
                                    dhip_right_y = int(sum(hip_right_y) / len(hip_right_y))
                                    dhip_left_x = int(sum(hip_left_x) / len(hip_left_x))
                                    dhip_left_y = int(sum(hip_left_y) / len(hip_left_y)) 
                                    dknee_right_x = int(sum(knee_right_x) / len(knee_right_x))
                                    dknee_right_y = int(sum(knee_right_y) / len(knee_right_y))
                                    dknee_left_x = int(sum(knee_left_x) / len(knee_left_x))
                                    dknee_left_y = int(sum(knee_left_y) / len(knee_left_y))
                                    dankle_right_x = int(sum(ankle_right_x) / len(ankle_right_x))
                                    dankle_right_y = int(sum(ankle_right_y) / len(ankle_right_y))
                                    dankle_left_x = int(sum(ankle_left_x) / len(ankle_left_x))
                                    dankle_left_y = int(sum(ankle_left_y) / len(ankle_left_y)) 
                                    dfoot_right_x = int(sum(foot_right_x) / len(foot_right_x))
                                    dfoot_right_y = int(sum(foot_right_y) / len(foot_right_y))
                                    dfoot_left_x = int(sum(foot_left_x) / len(foot_left_x))
                                    dfoot_left_y = int(sum(foot_left_y) / len(foot_left_y))  
                                    dhip_knee_right = int(sum(hip_knee_right) / len(hip_knee_right)) 
                                    dhip_knee_left = int(sum(hip_knee_left) / len(hip_knee_left)) 
                                    dknee_ankle_right = int(sum(knee_ankle_right) / len(knee_ankle_right)) 
                                    dknee_ankle_left = int(sum(knee_ankle_left) / len(knee_ankle_left)) 
                                    
                                    temp.append([
                                            dspine_base_x,
                                            dspine_base_y,
                                            spine_mid_x,
                                            spine_mid_y,
                                            dhip_right_x,
                                            dhip_right_y,
                                            dhip_left_x,
                                            dhip_left_y, 
                                            dknee_right_x,
                                            dknee_right_y,
                                            dknee_left_x,
                                            dknee_left_y,
                                            dankle_right_x,
                                            dankle_right_y,
                                            dankle_left_x,
                                            dankle_left_y, 
                                            dfoot_right_x,
                                            dfoot_right_y,
                                            dfoot_left_x,
                                            dfoot_left_y,
                                            dhip_knee_right,
                                            dhip_knee_left,
                                            dknee_ankle_right,
                                            dknee_ankle_left,
                                            '{}:{}' . format(get_f['time_stamp' . upper()].values[l], milisecond), 
                                            get_f['user' . upper()].values[l]])
                                    
                                    milisecond += 1
                                    
                                    spine_base_x = []
                                    spine_base_y = [] 
                                    spine_mid_x = [] 
                                    spine_mid_y = [] 
                                    
                                    hip_right_x = [] 
                                    hip_right_y = [] 
                                    hip_left_x = [] 
                                    hip_left_y = []
                                    
                                    knee_right_x = [] 
                                    knee_right_y = [] 
                                    knee_left_x = [] 
                                    knee_left_y = []
                                    
                                    ankle_right_x = [] 
                                    ankle_right_y = [] 
                                    ankle_left_x = [] 
                                    ankle_left_y = [] 
                                    
                                    foot_right_x = [] 
                                    foot_right_y = [] 
                                    foot_left_x = [] 
                                    foot_left_y = []
                                    
                                    hip_knee_right = [] 
                                    hip_knee_left = [] 
                                    knee_ankle_right = [] 
                                    knee_ankle_left = [] 
                        
                                     
                                    
                                if l % 2 == 0:
                                    if len(spine_base_x) == 0: # Check if already have a data or not
                                        spine_base_x.append(int(get_f['spine_base_x' . upper()].values[l]))
                                        spine_base_y.append(int(get_f['spine_base_y' . upper()].values[l]))
                                        spine_mid_x.append(int(get_f['spine_mid_x' . upper()].values[l]))
                                        spine_mid_y.append(int(get_f['spine_mid_y' . upper()].values[l]))
                                        hip_right_x.append(int(get_f['hip_right_x' . upper()].values[l]))
                                        hip_right_y.append(int(get_f['hip_right_y' . upper()].values[l]))
                                        hip_left_x.append(int(get_f['hip_left_x' . upper()].values[l]))
                                        hip_left_y.append(int(get_f['hip_left_y' . upper()].values[l])) 
                                        knee_right_x.append(int(get_f['knee_right_x' . upper()].values[l]))
                                        knee_right_y.append(int(get_f['knee_right_y' . upper()].values[l]))
                                        knee_left_x.append(int(get_f['knee_left_x' . upper()].values[l]))
                                        knee_left_y.append(int(get_f['knee_left_y' . upper()].values[l]))
                                        ankle_right_x.append(int(get_f['ankle_right_x' . upper()].values[l]))
                                        ankle_right_y.append(int(get_f['ankle_right_y' . upper()].values[l]))
                                        ankle_left_x.append(int(get_f['ankle_left_x' . upper()].values[l]))
                                        ankle_left_y.append(int(get_f['ankle_left_y' . upper()].values[l])) 
                                        foot_right_x.append(int(get_f['foot_right_x' . upper()].values[l]))
                                        foot_right_y.append(int(get_f['foot_right_y' . upper()].values[l]))
                                        foot_left_x.append(int(get_f['foot_left_x' . upper()].values[l]))
                                        foot_left_y.append(int(get_f['foot_left_y' . upper()].values[l])) 
                                        hip_knee_right.append(int(get_f['hip_knee_right' . upper()].values[l])) 
                                        hip_knee_left.append(int(get_f['hip_knee_left' . upper()].values[l])) 
                                        knee_ankle_right.append(int(get_f['knee_ankle_right' . upper()].values[l])) 
                                        knee_ankle_left.append(int(get_f['knee_ankle_left' . upper()].values[l]))
                                        
                                    else: # Excecute when have already one data
                                        spine_base_x.append(int(get_f['spine_base_x' . upper()].values[l]))
                                        spine_base_y.append(int(get_f['spine_base_y' . upper()].values[l]))
                                        spine_mid_x.append(int(get_f['spine_mid_x' . upper()].values[l]))
                                        spine_mid_y.append(int(get_f['spine_mid_y' . upper()].values[l]))
                                        hip_right_x.append(int(get_f['hip_right_x' . upper()].values[l]))
                                        hip_right_y.append(int(get_f['hip_right_y' . upper()].values[l]))
                                        hip_left_x.append(int(get_f['hip_left_x' . upper()].values[l]))
                                        hip_left_y.append(int(get_f['hip_left_y' . upper()].values[l])) 
                                        knee_right_x.append(int(get_f['knee_right_x' . upper()].values[l]))
                                        knee_right_y.append(int(get_f['knee_right_y' . upper()].values[l]))
                                        knee_left_x.append(int(get_f['knee_left_x' . upper()].values[l]))
                                        knee_left_y.append(int(get_f['knee_left_y' . upper()].values[l]))
                                        ankle_right_x.append(int(get_f['ankle_right_x' . upper()].values[l]))
                                        ankle_right_y.append(int(get_f['ankle_right_y' . upper()].values[l]))
                                        ankle_left_x.append(int(get_f['ankle_left_x' . upper()].values[l]))
                                        ankle_left_y.append(int(get_f['ankle_left_y' . upper()].values[l])) 
                                        foot_right_x.append(int(get_f['foot_right_x' . upper()].values[l]))
                                        foot_right_y.append(int(get_f['foot_right_y' . upper()].values[l]))
                                        foot_left_x.append(int(get_f['foot_left_x' . upper()].values[l]))
                                        foot_left_y.append(int(get_f['foot_left_y' . upper()].values[l])) 
                                        hip_knee_right.append(int(get_f['hip_knee_right' . upper()].values[l])) 
                                        hip_knee_left.append(int(get_f['hip_knee_left' . upper()].values[l])) 
                                        knee_ankle_right.append(int(get_f['knee_ankle_right' . upper()].values[l])) 
                                        knee_ankle_left.append(int(get_f['knee_ankle_left' . upper()].values[l]))
                                            
                                        dspine_base_x = int(sum(spine_base_x) / len(spine_base_x))
                                        dspine_base_y = int(sum(spine_base_y) / len(spine_base_y))
                                        spine_mid_x = int(sum(spine_mid_x) / len(spine_mid_x))
                                        spine_mid_y = int(sum(spine_mid_y) / len(spine_mid_y))
                                        dhip_right_x = int(sum(hip_right_x) / len(hip_right_x))
                                        dhip_right_y = int(sum(hip_right_y) / len(hip_right_y))
                                        dhip_left_x = int(sum(hip_left_x) / len(hip_left_x))
                                        dhip_left_y = int(sum(hip_left_y) / len(hip_left_y)) 
                                        dknee_right_x = int(sum(knee_right_x) / len(knee_right_x))
                                        dknee_right_y = int(sum(knee_right_y) / len(knee_right_y))
                                        dknee_left_x = int(sum(knee_left_x) / len(knee_left_x))
                                        dknee_left_y = int(sum(knee_left_y) / len(knee_left_y))
                                        dankle_right_x = int(sum(ankle_right_x) / len(ankle_right_x))
                                        dankle_right_y = int(sum(ankle_right_y) / len(ankle_right_y))
                                        dankle_left_x = int(sum(ankle_left_x) / len(ankle_left_x))
                                        dankle_left_y = int(sum(ankle_left_y) / len(ankle_left_y)) 
                                        dfoot_right_x = int(sum(foot_right_x) / len(foot_right_x))
                                        dfoot_right_y = int(sum(foot_right_y) / len(foot_right_y))
                                        dfoot_left_x = int(sum(foot_left_x) / len(foot_left_x))
                                        dfoot_left_y = int(sum(foot_left_y) / len(foot_left_y))  
                                        dhip_knee_right = int(sum(hip_knee_right) / len(hip_knee_right)) 
                                        dhip_knee_left = int(sum(hip_knee_left) / len(hip_knee_left)) 
                                        dknee_ankle_right = int(sum(knee_ankle_right) / len(knee_ankle_right)) 
                                        dknee_ankle_left = int(sum(knee_ankle_left) / len(knee_ankle_left)) 
                                            
                                        temp.append([
                                            dspine_base_x,
                                            dspine_base_y,
                                            spine_mid_x,
                                            spine_mid_y,
                                            dhip_right_x,
                                            dhip_right_y,
                                            dhip_left_x,
                                            dhip_left_y, 
                                            dknee_right_x,
                                            dknee_right_y,
                                            dknee_left_x,
                                            dknee_left_y,
                                            dankle_right_x,
                                            dankle_right_y,
                                            dankle_left_x,
                                            dankle_left_y, 
                                            dfoot_right_x,
                                            dfoot_right_y,
                                            dfoot_left_x,
                                            dfoot_left_y,
                                            dhip_knee_right,
                                            dhip_knee_left,
                                            dknee_ankle_right,
                                            dknee_ankle_left,
                                            '{}:{}' . format(get_f['time_stamp' . upper()].values[l], milisecond), 
                                            get_f['user' . upper()].values[l]])
            
                                        milisecond += 1
            
                                        spine_base_x = []
                                        spine_base_y = [] 
                                        spine_mid_x = [] 
                                        spine_mid_y = [] 
                                        
                                        hip_right_x = [] 
                                        hip_right_y = [] 
                                        hip_left_x = [] 
                                        hip_left_y = []
                                        
                                        knee_right_x = [] 
                                        knee_right_y = [] 
                                        knee_left_x = [] 
                                        knee_left_y = []
                                        
                                        ankle_right_x = [] 
                                        ankle_right_y = [] 
                                        ankle_left_x = [] 
                                        ankle_left_y = [] 
                                        
                                        foot_right_x = [] 
                                        foot_right_y = [] 
                                        foot_left_x = [] 
                                        foot_left_y = []
                                        
                                        hip_knee_right = [] 
                                        hip_knee_left = [] 
                                        knee_ankle_right = [] 
                                        knee_ankle_left = [] 
                        
                                        
                                    if len(get_f) < 10 and l == len(get_f) - 1:
                                        dspine_base_x = int(sum(spine_base_x) / len(spine_base_x))
                                        dspine_base_y = int(sum(spine_base_y) / len(spine_base_y))
                                        spine_mid_x = int(sum(spine_mid_x) / len(spine_mid_x))
                                        spine_mid_y = int(sum(spine_mid_y) / len(spine_mid_y))
                                        dhip_right_x = int(sum(hip_right_x) / len(hip_right_x))
                                        dhip_right_y = int(sum(hip_right_y) / len(hip_right_y))
                                        dhip_left_x = int(sum(hip_left_x) / len(hip_left_x))
                                        dhip_left_y = int(sum(hip_left_y) / len(hip_left_y)) 
                                        dknee_right_x = int(sum(knee_right_x) / len(knee_right_x))
                                        dknee_right_y = int(sum(knee_right_y) / len(knee_right_y))
                                        dknee_left_x = int(sum(knee_left_x) / len(knee_left_x))
                                        dknee_left_y = int(sum(knee_left_y) / len(knee_left_y))
                                        dankle_right_x = int(sum(ankle_right_x) / len(ankle_right_x))
                                        dankle_right_y = int(sum(ankle_right_y) / len(ankle_right_y))
                                        dankle_left_x = int(sum(ankle_left_x) / len(ankle_left_x))
                                        dankle_left_y = int(sum(ankle_left_y) / len(ankle_left_y)) 
                                        dfoot_right_x = int(sum(foot_right_x) / len(foot_right_x))
                                        dfoot_right_y = int(sum(foot_right_y) / len(foot_right_y))
                                        dfoot_left_x = int(sum(foot_left_x) / len(foot_left_x))
                                        dfoot_left_y = int(sum(foot_left_y) / len(foot_left_y))  
                                        dhip_knee_right = int(sum(hip_knee_right) / len(hip_knee_right)) 
                                        dhip_knee_left = int(sum(hip_knee_left) / len(hip_knee_left)) 
                                        dknee_ankle_right = int(sum(knee_ankle_right) / len(knee_ankle_right)) 
                                        dknee_ankle_left = int(sum(knee_ankle_left) / len(knee_ankle_left)) 
                                            
                                        temp.append([
                                            dspine_base_x,
                                            dspine_base_y,
                                            spine_mid_x,
                                            spine_mid_y,
                                            dhip_right_x,
                                            dhip_right_y,
                                            dhip_left_x,
                                            dhip_left_y, 
                                            dknee_right_x,
                                            dknee_right_y,
                                            dknee_left_x,
                                            dknee_left_y,
                                            dankle_right_x,
                                            dankle_right_y,
                                            dankle_left_x,
                                            dankle_left_y, 
                                            dfoot_right_x,
                                            dfoot_right_y,
                                            dfoot_left_x,
                                            dfoot_left_y,
                                            dhip_knee_right,
                                            dhip_knee_left,
                                            dknee_ankle_right,
                                            dknee_ankle_left,
                                            '{}:{}' . format(get_f['time_stamp' . upper()].values[l], milisecond), 
                                            get_f['user' . upper()].values[l]])
                                        
                                        milisecond += 1
            
                                        spine_base_x = []
                                        spine_base_y = [] 
                                        spine_mid_x = [] 
                                        spine_mid_y = [] 
                                        
                                        hip_right_x = [] 
                                        hip_right_y = [] 
                                        hip_left_x = [] 
                                        hip_left_y = []
                                        
                                        knee_right_x = [] 
                                        knee_right_y = [] 
                                        knee_left_x = [] 
                                        knee_left_y = []
                                        
                                        ankle_right_x = [] 
                                        ankle_right_y = [] 
                                        ankle_left_x = [] 
                                        ankle_left_y = [] 
                                        
                                        foot_right_x = [] 
                                        foot_right_y = [] 
                                        foot_left_x = [] 
                                        foot_left_y = []
                                        
                                        hip_knee_right = [] 
                                        hip_knee_left = [] 
                                        knee_ankle_right = [] 
                                        knee_ankle_left = [] 
                        
                            
                    if len(get_f) < 9 and len(get_f) > 4: 
                        for l in range(5): 
                            temp.append([
                                    int(get_f['spine_base_x' . upper()].values[l]),
                                    int(get_f['spine_base_y' . upper()].values[l]),
                                    int(get_f['spine_mid_x' . upper()].values[l]),
                                    int(get_f['spine_mid_y' . upper()].values[l]),
                                    int(get_f['hip_right_x' . upper()].values[l]),
                                    int(get_f['hip_right_y' . upper()].values[l]),
                                    int(get_f['hip_left_x' . upper()].values[l]),
                                    int(get_f['hip_left_y' . upper()].values[l]),
                                    int(get_f['knee_right_x' . upper()].values[l]),
                                    int(get_f['knee_right_y' . upper()].values[l]),
                                    int(get_f['knee_left_x' . upper()].values[l]),
                                    int(get_f['knee_left_y' . upper()].values[l]),
                                    int(get_f['ankle_right_x' . upper()].values[l]),
                                    int(get_f['ankle_right_y' . upper()].values[l]),
                                    int(get_f['ankle_left_x' . upper()].values[l]),
                                    int(get_f['ankle_left_y' . upper()].values[l]),
                                    int(get_f['foot_right_x' . upper()].values[l]),
                                    int(get_f['foot_right_y' . upper()].values[l]),
                                    int(get_f['foot_left_x' . upper()].values[l]),
                                    int(get_f['foot_left_y' . upper()].values[l]), 
                                    int(get_f['hip_knee_right' . upper()].values[l]),
                                    int(get_f['hip_knee_left' . upper()].values[l]),
                                    int(get_f['knee_ankle_right' . upper()].values[l]),
                                    int(get_f['knee_ankle_left' . upper()].values[l]),
                                    '{}:{}' . format(get_f['time_stamp' . upper()].values[l], milisecond), 
                                    get_f['user' . upper()].values[l]])
            
                            milisecond += 1
                                
            t_temp.append(temp)
     
    
        ## Compute standing
        data = [] 
        for i in range(len(t_temp)):
            temp = []
            count = 1
            for j in range(len(t_temp[i])): # i means number of user
                
                hiprightx, hiprighty, hipleftx, hiplefty = t_temp[i][j][4], t_temp[i][j][5], t_temp[i][j][6], t_temp[i][j][7]
                anklerightx, anklerighty, ankleleftx, anklelefty = t_temp[i][j][12], t_temp[i][j][13], t_temp[i][j][14], t_temp[i][j][15]
                 
                try:
                    # Deciding for right foot
                    ar_opposite, ar_adjacent, ar_hypotenuse, ar_degrees = self.getLength(hiprightx, hiprighty, anklerightx, anklerighty)
                        
                    # Deciding for left foot
                    al_opposite, al_adjacent, al_hypotenuse, al_degrees = self.getLength(hipleftx, hiplefty, ankleleftx, anklelefty)
                    
                    standing_status = ''    
                    if ar_degrees < 0 and al_degrees < 0:
                        standing_status = 'RIGHT'
#                        print('STANDING RIGHT', smooth[i][j][8]) # time stamp
                    elif ar_degrees > -1 and al_degrees > -1:
                        standing_status = 'LEFT'
#                        print('STANDING LEFT', smooth[i][j][8])
                    else:
                        standing_status = 'NORMAL'
#                        print('STANDING NORMAL', smooth[i][j][8])
                        
                    temp.append([count, standing_status, t_temp[i][j][24], t_temp[i][j][25]]) # time_stamp, user
                    count += 1
                except Exception as e:
                    print('No body is found.', e)
            data.append(temp)  
     
        ## Store the data for deep learning 
    #    for i in range(len(smooth)):
    #        count = 1
    #        for j in range(len(smooth[i])):
    #            smooth[i][j].insert(0, count)
    #            smooth[i][j].append(data[i][j][1]) 
    #            count += 1
    #    for i in range(len(smooth)):
    #        get = pd.DataFrame(np.array(smooth[i]).tolist(), columns=['NO', 'USER', 'HIPRIGHTX', 'HIPRIGHTY', 'HIPLEFTX', 'HIPLEFTY', 'ANKLERIGHTX', 'ANKLERIGHTY', 'ANKLELEFTX', 'ANKLELEFTY', 'TIME_STAMP', 'STATUS'])
    #        get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Deep Learning/{}.csv' . format('Master_kinect'), index=False)
    #      
        ## Store to csv
        for i in range(len(data)):
            get = pd.DataFrame(np.array(data[i]).tolist(), columns=['NO', 'STATUS', 'TIME', 'NAME'])
            get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Kinect/{}_{}.csv' . format(data[i][0][3], signed), index=False)
        
        ## Store the data for deep learning 
        for i in range(len(t_temp)):
            count = 1
            for j in range(len(t_temp[i])):
                t_temp[i][j].insert(0, count) 
                count += 1
        colnames = ['no',
                    'spine_base_x', 'spine_base_y', 'spine_mid_x', 'spine_mid_y',
                    'hip_right_x', 'hip_right_y', 'hip_left_x', 'hip_left_y', 
                    'knee_right_x', 'knee_right_y', 'knee_left_x', 'knee_left_y',
                    'ankle_right_x', 'ankle_right_y', 'ankle_left_x', 'ankle_left_y', 
                    'foot_right_x', 'foot_right_y', 'foot_left_x', 'foot_left_y',
                    'hip_knee_right', 'hip_knee_left', 'knee_ankle_right', 'knee_ankle_left',
                    'time_stamp', 'user']
        colnames = [x.upper() for x in colnames]
        for i in range(len(t_temp)):
            get = pd.DataFrame(t_temp[i], columns=colnames)
            get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Kinect/{}_{}.csv' . format('Master_kinect', i), index=False)
     
        
        print('## Done Kinect')
        
    def loadAllData(self):
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Insoles/'
        file = os.listdir(address)  
        for i in file:
            if 'csv' in i:
                if 'Master' not in i:
                    file_insoles_name = i 
        insoles = [] 
        dataframe = pd.read_csv('{}{}' . format(address, file_insoles_name)).values
        insoles.append(dataframe)
        
        address = 'C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Kinect/'
        file = os.listdir(address) 
        for i in file:
            if 'csv' in i:
                if 'Master' not in i:
                    file_kinect_name = i
        kinect = [] 
        dataframe = pd.read_csv('{}{}' . format(address, file_kinect_name)).values
        kinect.append(dataframe)
        
        return kinect, insoles
            
    def match_cases(self, kinect, insoles): 
        
        separate = []
        for i in kinect:
            temp = []
            for j in insoles:
                temp.append([i, j])
            separate.append(temp)
        
        post_final = []
        for i in separate: 
            post_temp = []
            count = 1
            for j in i[0][0]: # Kinect 
                temp = []
                for k in i[0][1]: # Insoles
                    if j[2][j[2].index(':'):] == k[2][k[2].index(':'):]:
                        temp.append([count, j[1], k[1], j[2], j[3], k[3]])
                if len(temp) > 0:
                    post_temp.append(temp[0])
                    count += 1
            if len(post_temp) > 0:
                post_final.append(post_temp)
        
        acc = []
        for i in range(len(post_final)):
            a_temp = []
            for j in range(len(post_final[i])):
                print(post_final[i][j][1], post_final[i][j][2])
                if post_final[i][j][1] == post_final[i][j][2]: 
                    a_temp.append(1)
                else:
                    a_temp.append(0)
            acc.append(a_temp)
         
        for i in range(len(post_final)):
            for j in range(len(post_final[i])):
                post_final[i][j].append(sum(acc[i]) / len(acc[i]))
        
        ## Store to csv
        for i in range(len(post_final)):
            get = pd.DataFrame(np.array(post_final[i]).tolist(), columns=['NO', 'KINECT', 'INSOLES', 'TIME', 'KIN_NAME', 'IN_NAME', 'ACC'])
            get.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Comparison/Actual_{}_{}_{}.csv' . format(post_final[i][0][4], post_final[i][0][5], sum(acc[i]) / len(acc[i])), index=False)
            
        return post_final
            
    def shift(self, post_final, num): 
        a = []
        b = []
        kin_user = []
        in_user = []
        for i in range(len(post_final[0])):
            a.append(post_final[0][i][1])
            b.append(post_final[0][i][2])
            kin_user.append(post_final[0][i][4])
            in_user.append(post_final[0][i][5])
        c = [] 
        one = []
        one.append(a)
        one.append(b)
        one.append(kin_user)
        one.append(in_user)
        
        two = np.array(one).tolist()
        for i in range(num + 1): 
            if i == 0:
                c.append(np.array(one).tolist()) 
            else:   
                one[0].append('0')
                one[1].insert(0, '0') 
                one[2].insert(0, one[2][0]) 
                one[3].insert(0, one[3][0]) 
                c.append(np.array(one).tolist())
                
                two[0].insert(0, '0')
                two[1].append('0')
                two[2].insert(0, two[2][0]) 
                two[3].insert(0, two[3][0]) 
                c.append(np.array(two).tolist()) 
     
        return c
        
 
    def get_simil(self, post_final, num_shift): 
        final = self.shift(post_final, num_shift)  
        check_the_highest = 0
        get_data = []
        sim = []
        kin_usr = ''
        in_usr = ''
        
        
        acc = []
        
        a = []
        b = []  
         
        for j in range(len(final)):  
            a_t = []
            b_t = []
            
            acc_t = []
            for i in range(len(final[j][0])): # take one index as sample for loop
                kin_usr = final[j][2][i]
                in_usr = final[j][3][i]
                kinect = 60 # Standing normal
                insoles = 60
                if final[j][0][i] == 'RIGHT': # Kinect
                    kinect = 1 # Standing right
                elif final[j][0][i] == 'LEFT':
                    kinect = 120 # Standing left
                
                if final[j][1][i] == 'RIGHT': # Insoles
                    insoles = 1
                elif final[j][1][i] == 'LEFT':
                    insoles = 120 
                    
                a_t.append(kinect)
                b_t.append(insoles)
                
                if kinect == insoles:
                    acc_t.append(1)
                else:
                    acc_t.append(0) 
                
            acc = sum(acc_t) / len(acc_t) # Use this
            
            if check_the_highest < acc:
                check_the_highest = acc
                
                get_data = np.array(final[j]).tolist()
                 
                sim = [in_usr, kin_usr, acc]
                a = np.array(a_t).tolist()
                b = np.array(b_t).tolist()
                 
                
        # Save comparison
        get_data.insert(0, np.arange(1, len(get_data[0]) + 1))      
        get_data.append(a)   
        get_data.append(b)   
        df = pd.DataFrame(np.array(get_data)).transpose()
        df.columns = ['NO', 'KINECT', 'INSOLES', 'USER_INSOLES', 'USER_KINECT', 'KIN_LAB', 'INS_LAB']
        df.to_csv('C:/Users/yzucsemss/Desktop/For Competition/Rule-based approach/Working Directory/Comparison/{}_{}.csv' . format('After_shift_comparison', sim[2]), index=False)
    
        return sim
     
    
    def run(self, second, move=1):  
        self.removeFiles()
        self.extractInsoles(second, status=False) # Uncomment if in the real implementation
        self.extractVideo(second)
            
        kinect, insoles = self.loadAllData()
        post_final = self.match_cases(kinect, insoles)
        sim = self.get_simil(post_final, 20) # Number of shift 
        print('\nSimilarity: ', sim)  
        
run = Client()
run.run('15') # starting second at # 0 = move to the backup folder


