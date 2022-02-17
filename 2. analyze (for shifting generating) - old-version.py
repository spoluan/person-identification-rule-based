# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:09:12 2018

@author: Sevendi Eldrige Rifki Poluan
"""

import os, pandas as pd, numpy as np, shutil 

class Analyze(object):
    
    def __init__(self):
        self.identification = 'Person identification'
        print('## Start . . .')
              
    def remove_files(self): 
        try:
            address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\Final Result\\The very similar one\\' . format(self.identification)
            file = os.listdir(address)
            for i in file:
                os.remove("{}{}" . format(address, i))
               
            address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\Final Result\\The whole data\\' . format(self.identification)
            file = os.listdir(address)
            for i in file:
                shutil.rmtree("{}{}" . format(address, i)) 
        except:
            pass
    
    def load_data(self):
        
        kinect = []
        insoles = []
        
        address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}' . format(self.identification)
        path = os.listdir(address)[0:21]
        for i in range(len(path)):
            add = '{}/{}/Working Directory/Comparison/' . format(address, path[i])
            file = os.listdir(add)
            for j in range(len(file)):
                if 'Actual' in file[j]:
                    # Load data
                    source = '{}/{}' . format(add, file[j])
                    columns = ['NO', 'KINECT', 'INSOLES', 'TIME', 'KIN_NAME', 'IN_NAME', 'ACC']
                    dataframe = pd.read_csv(source, names = columns, skiprows = 1)  
                    
                    # Get kinects
                    kin = dataframe[['KINECT', 'KIN_NAME']][0:272].transpose().values.tolist()
                    
                    # Get insoles
                    ins = dataframe[['INSOLES', 'IN_NAME']][0:272].transpose().values.tolist()
                    
                    # Append both to separate variables
                    kinect.append(kin)
                    insoles.append(ins) 
    
        return kinect, insoles
     
        
    def preprocessing(self):
        kinect, insoles = self.load_data()
         
        per_pair = []
        for i in range(len(kinect)): 
            temp_pair = []
            get_kinect = np.array(kinect[i])
            for j in range(len(kinect)): # Kinect and insoles are have the same length 
                get_insoles = np.array(insoles[j])
                
                # Concat both data
                temp_pair.append(np.concatenate((get_kinect, get_insoles), axis=0))    
            
            per_pair.append(temp_pair)
             
        return per_pair
    
    def shift(self, one_sample, num=5):  
             
        shift_kinect = np.array(one_sample).tolist()
        shift_insoles = np.array(one_sample).tolist()
        
        results = []
        
        for i in range(num + 1): # Number of shift to be added zero at first and last
            if i == 0:
                results.append(np.array(shift_kinect).tolist()) 
            else:   
                # Shift Insoles
                shift_kinect[0].append('0') # Kinect
                shift_kinect[1].insert(0, shift_kinect[1][0]) # Kinect user
                shift_kinect[2].insert(0, '0') # Insoles
                shift_kinect[3].insert(0, shift_kinect[3][0]) # Insoles user
                results.append(np.array(shift_kinect).tolist())
                
                # Shift Kinect
                shift_insoles[0].insert(0, '0')
                shift_insoles[1].append(shift_insoles[1][0])
                shift_insoles[2].append('0') 
                shift_insoles[3].insert(0, shift_insoles[3][0]) 
                results.append(np.array(shift_insoles).tolist())
     
        return results
    
    def shift_processing(self):
        post_final = self.preprocessing()
        
        cmp_per_user = []
        
        save_all_combinations = []
        # Number of user
        for i in range(len(post_final)): 
            
            one_comparison = [] 
            many_comparison = []
            hold = 0
            
            # Number of comparison per user
            for j in range(len(post_final[i])):
                one_sample = post_final[i][j]
                
                # Shift
                any_comparison = self.shift(one_sample, num=20)
                check = []
                check = self.get_the_very_similar_one(any_comparison)
                many_comparison.append(check)
                
                # Check the hightest score
                if hold < check[4][0]:
                    hold = check[4][0]  
                    one_comparison = check 
                 
            # Save per every user
            addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\The whole data\\SKELETON_{}' . format(self.identification, many_comparison[0][1][0])
            try:
                os.mkdir(addr)
            except:
                pass 
            for i in range(len(many_comparison)):  
                save = np.array(many_comparison[i]).tolist()
                save.insert(0, np.arange(1, len(save[0]) + 1).tolist())
                df = pd.DataFrame(np.array(save)).transpose() 
                df.columns = ['NO', 'KINECT', 'KIN_USER', 'INSOLES', 'INS_USER', 'SIMILARITY'] 
                df.to_csv('{}/{}_kin({}) - in({})_{}.csv' . format(addr, i, save[2][0], save[4][0], save[5][0][0:]), index=False)
                
                save_all_combinations.append(['{} - {}' . format(self.getCharacter(int(save[2][0])), save[4][0]), save[5][0][0:]])
            
            # Save the very high correlation per user
            cmp_per_user.append(one_comparison)
            
        save_all_combinations.sort()
        app = []
        for i in range(len(save_all_combinations)):
           temp = []    
           for j in range(len(save_all_combinations)):
               if save_all_combinations[j][0][0:save_all_combinations[j][0].index(' ')] == save_all_combinations[i][0][0:save_all_combinations[i][0].index(' ')]:
                   temp.append(save_all_combinations[j])
           if temp not in app: app.append(temp)
        
        columns = []
        columns.append('Name')
        for i in range(len(app)): 
            columns.append('Insoles {}' . format(app[i][0][0][0:app[i][0][0].index(' ')]))
        
    
        all_ = []
        for i in range(len(app)):
            a = []
            a.append('Kinect {}' . format(app[i][0][0][0:app[i][0][0].index(' ')]))
            for j in range(len(app[i])):
                a.append(app[i][j][1])
            all_.append(a)
            
        get = pd.DataFrame(np.array(all_).tolist(), columns=columns) 
        get.to_csv('{}' . format('C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\Rule-based after shifting - All_probability.csv' . format(self.identification)), index=False)
        
        addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\The very similar one' . format(self.identification, cmp_per_user[0][1][0])
        
        columns = ['Name', 'Probability']
        save_acc = []
        for i in range(len(cmp_per_user)):
            save = []
            save = np.array(cmp_per_user[i]).tolist()
            save.insert(0, np.arange(1, len(save[0]) + 1).tolist())
            df = pd.DataFrame(np.array(save)).transpose()
            df.columns = ['NO', 'KINECT', 'KIN_USER', 'INSOLES', 'INS_USER', 'SIMILARITY']
            df.to_csv('{}/{}_kin({}) - in({})_{}.csv' . format(addr, i, save[2][0], save[4][0], save[5][0][0:]), index=False) 
            save_acc.append(['Kinect {} - Insoles {}' . format(self.getCharacter(int(save[2][0])), save[4][0]), save[5][0][0:]])
            
        save_acc.sort()
        df = pd.DataFrame(np.array(save_acc).tolist(), columns=columns)
        df.to_csv('C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\Rule-based after shifting - Probability.csv' . format(self.identification), index=False)
          
        return cmp_per_user
    
    def getCharacter(self, val): 
        c = ''  
        char_val = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
        for i in range(len(char_val)):
            if val - 1 == i:
                c = char_val[i] 
        return c
    
    def get_the_very_similar_one(self, any_comparison):  
        check_the_highest = 0
        get_data = []  
         
        store_all_accuracy = []
        
        for j in range(len(any_comparison)):  
            
            acc_t = []
             
            for i in range(len(any_comparison[j][0])): # take one index as sample for loop
                  
                 
                kinect = 60 # Standing normal
                insoles = 60
                if any_comparison[j][0][i] == 'RIGHT': # Kinect
                    kinect = 1 # Standing right
                elif any_comparison[j][0][i] == 'LEFT':
                    kinect = 120 # Standing left
                
                if any_comparison[j][2][i] == 'RIGHT': # Insoles
                    insoles = 1
                elif any_comparison[j][2][i] == 'LEFT':
                    insoles = 120
                  
                if kinect == insoles: # Just for checking where they are the same
                    acc_t.append(1)
                else:
                    acc_t.append(0)
             
             
            similarity = sum(acc_t) / len(acc_t)
            
            if check_the_highest < similarity:
                check_the_highest = similarity
                x = np.zeros(len(any_comparison[j][0]))
                x[:] = similarity
                get_data = np.array(any_comparison[j]).tolist() 
                get_data.append(x.tolist())
                   
                
            store_all_accuracy.append(similarity) 
     
        return get_data
    
    def run(self):
        self.remove_files()
        self.shift_processing()
        
app = Analyze()
app.run()