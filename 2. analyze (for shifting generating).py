# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:09:12 2018

@author: Sevendi Eldrige Rifki Poluan
"""

import os, pandas as pd, numpy as np 
import shutil

class Analyze(object):
    
    def __init__(self):
        self.identification = 'Person identification'
        print('## Start . . .')
              
    def remove_files(self): 
        try:
            address = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\Final Result\\' . format(self.identification)
            file = os.listdir(address)
            for i in file:
                shutil.rmtree("{}{}" . format(address, i))
               
        except:
            pass
        
        try:
            address =   'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\Final Result\\' . format(self.identification)
            os.mkdir(address)
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
    
    
    def shift_processing(self, init_split=[], number_of_shift=[], acc_name='Accuracy', split_status='overlap'):
        post_final = self.preprocessing()
        to_be_plotting = []
        for time_split in range(len(init_split)):
            split_all = []
            start = 0
            end = init_split[time_split] * 5
            
            if split_status == 'non_overlap':
                for x in range(len(post_final[0][0][0]) // (init_split[time_split] * 5)):
                    temp = []
                    for i in range(len(post_final)): # For user amount
                        for_user_amount = []
                        for j in range(len(post_final[i])):# For all combinations per user
                            for_all_combinations = []
                            for k in range(len(post_final[i][j])): # For the specific data
                                for_all_combinations.append(post_final[i][j][k][start:end])
                            for_user_amount.append(np.array(for_all_combinations).tolist())
                        temp.append(np.array(for_user_amount).tolist())    
                    start = end
                    end += (init_split[time_split] * 5)
                    split_all.append(temp)
            elif split_status == 'overlap':
                end = (init_split[time_split] * 5)
                for x in range(len(post_final[0][0][0])):
                    temp = []
                    try:
                        for i in range(len(post_final)): # For user amount
                            for_user_amount = []
                            for j in range(len(post_final[i])):# For all combinations per user
                                for_all_combinations = []
                                for k in range(len(post_final[i][j])): # For the specific data
                                    for_all_combinations.append(post_final[i][j][k][start:end])
                                for_user_amount.append(np.array(for_all_combinations).tolist())
                            temp.append(np.array(for_user_amount).tolist())    
                        start += 1
                        end += 1
                        split_all.append(temp)
                    except:
                        break
                        pass
            
            get_accuracy = []
            
            for n_ in range(len(split_all)):
                cmp_per_user = []
                
                save_all_combinations = []
                # Number of user
                for i in range(len(split_all[n_])):
                    
                    one_comparison = [] 
                    many_comparison = []
                    hold = -1
                    
                    # Number of comparison per user
                    for j in range(len(split_all[n_][i])):
                        one_sample = split_all[n_][i][j]
                        
                        # Shift
                        any_comparison = self.shift(one_sample, num=number_of_shift[time_split])
                        check = []
                        check = self.get_the_very_similar_one(any_comparison)
                        many_comparison.append(check)
                        # Check the hightest score
                        if hold < check[4][0]:
                            hold = check[4][0]  
                            one_comparison = check
                        elif hold == check[4][0]:
                            to_ = check
                            to_pd = pd.Series(to_[3])
                            to_pd.iloc[:] = 'X'
                            to_[3] = to_pd.values.tolist()
                            one_comparison = to_
     
                    
                    # Save per every user
                    addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\{}\\The whole data\\SKELETON_{}\\{}' . format(self.identification, init_split[time_split], many_comparison[0][1][0], n_)
                    try:
                        os.makedirs(addr)
                    except:
                        pass 
                    for i in range(len(many_comparison)):  
                        save = np.array(many_comparison[i]).tolist()
                        save.insert(0, np.arange(1, len(save[0]) + 1).tolist())
                        df = pd.DataFrame(np.array(save)).transpose() 
                        df.columns = ['NO', 'KINECT', 'KIN_USER', 'INSOLES', 'INS_USER', 'SIMILARITY'] 
                        df.to_csv('{}/{}_kin({}) - in({})_{}.csv' . format(addr, i, self.getCharacter(int(save[2][0])), save[4][0], save[5][0][0:]), index=False)
                        
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
                    
                    
                addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\{}\\All Probability\\{}' . format(self.identification, init_split[time_split], n_)
                try:
                    os.makedirs(addr)
                except:
                    pass
                get = pd.DataFrame(np.array(all_).tolist(), columns=columns) 
                get.to_csv('{}\\{}' . format(addr, 'Rule-based after shifting - All_probability.csv' . format(addr, init_split[time_split])), index=False)
                
                
                addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\{}\\The very similar one\\{}' . format(self.identification, init_split[time_split], n_)
                try:
                    os.makedirs(addr)
                except:
                    pass
                columns = ['Name', 'Probability']
                save_acc = []
                for i in range(len(cmp_per_user)):
                    save = []
                    save = np.array(cmp_per_user[i]).tolist()
                    save.insert(0, np.arange(1, len(save[0]) + 1).tolist())
                    df = pd.DataFrame(np.array(save)).transpose()
                    df.columns = ['NO', 'KINECT', 'KIN_USER', 'INSOLES', 'INS_USER', 'SIMILARITY']
                    df.to_csv('{}/{}_kin({}) - in({})_{}.csv' . format(addr, i, self.getCharacter(int(save[2][0])), save[4][0], save[5][0][0:]), index=False) 
                    save_acc.append(['Kinect {} - Insoles {}' . format(self.getCharacter(int(save[2][0])), save[4][0]), save[5][0][0:]])
                    get_accuracy.append(['{} - {}' . format(self.getCharacter(int(save[2][0])), save[4][0]), save[5][0][0:]]) # Only store the number of label to be counting
                        # Change later . save the probability and later will be taking an average . not by the label
                    # Problem is here
                addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\{}\\Probability\\{}' . format(self.identification, init_split[time_split], n_)
                try:
                    os.makedirs(addr)
                except:
                    pass
                save_acc.sort()
                df = pd.DataFrame(np.array(save_acc).tolist(), columns=columns)
                df.to_csv('{}\\Probability.csv' . format(addr), index=False)
            
            store_acc = []
            get_accuracy.sort() 
            temp = []
            for i in range(len(get_accuracy)):
                try:
                    if get_accuracy[i][0][0:get_accuracy[i][0].index(' ')] == get_accuracy[i + 1][0][0:get_accuracy[i + 1][0].index(' ')]:
                        temp.append(get_accuracy[i])
                    else:
                        temp.append(get_accuracy[i])
                        store_acc.append(temp)
                        temp = []
                except:
                    if i == len(get_accuracy) - 1:
                        temp.append(get_accuracy[i])
                    store_acc.append(temp)
                    pass
            
            store = []
            for i in range(len(store_acc)):
                temp = []
                for j in range(len(store_acc[i])):
                    if store_acc[i][j][0][0:store_acc[i][j][0].index(' ')] == store_acc[i][j][0][store_acc[i][j][0].index('-') + 2:]:
                        temp.append(1)
                    else:
                        temp.append(0)
                store.append([store_acc[i][j][0][0:store_acc[i][j][0].index(' ')], sum(temp) / len(temp)])
            
            addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Final Result\\{}\\Accuracy' . format(self.identification, init_split[time_split])
            try:
                os.makedirs(addr)
            except:
                pass
            columns = ['Label', 'Accuracy']
            df = pd.DataFrame(np.array(store).tolist(), columns=columns)
            df.to_csv('{}/Accuracy.csv' . format(addr), index=False)
            
            
            try:
                print(time_split)
                if time_split == 0:
                    temp_plot = []
                    temp_plot = np.transpose(np.array(store).tolist()).tolist()
                    col = []
                    col = temp_plot[0].copy()
                    col.insert(0, 'Split')
                    to_be_plotting.append(col)
                    val = []
                    val = temp_plot[1].copy()
                    val.insert(0, init_split[time_split])
                    to_be_plotting.append(val)
                else:
                    temp_plot = []
                    temp_plot = np.transpose(np.array(store).tolist()).tolist()[1]
                    val = []
                    val = temp_plot.copy()
                    val.insert(0, init_split[time_split])
                    to_be_plotting.append(val)
                    
            except:
                pass
        
        
        addr = 'C:\\Users\\yzucsemss\\Desktop\\For Competition\\Rule-based approach\\Backup\\{}\\Accuracy' . format(self.identification)
        try:
            os.makedirs(addr)
        except:
            pass
        for i in range(len(to_be_plotting)):
            if i == 0:
                to_be_plotting[i].append('Accuracy')
            else:
                a = np.array(to_be_plotting[i][1:], dtype=float)
                to_be_plotting[i].append(sum(a) / len(a))
            
        df = pd.DataFrame(np.array(to_be_plotting[1:]).tolist(), columns=to_be_plotting[0])
        df.to_csv('{}/{}.csv' . format(addr, acc_name), index=False)
        
        return cmp_per_user
    
    def getCharacter(self, val): 
        c = ''  
        char_val = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
        for i in range(len(char_val)):
            if val - 1 == i:
                c = char_val[i] 
        return c
    
    def get_the_very_similar_one(self, any_comparison):  
        check_the_highest = -1
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
            
            if check_the_highest < similarity: # Take sample of first highest pair
                check_the_highest = similarity
                x = np.zeros(len(any_comparison[j][0]))
                x[:] = similarity
                get_data = np.array(any_comparison[j]).tolist()
                get_data.append(x.tolist()) 
                   
            store_all_accuracy.append(similarity)
        return get_data
    
    def run(self):
        self.remove_files()
        init_split = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        num_of_shift = [3, 3, 3, 5, 10, 10, 10, 10, 10, 10]
#        num_of_shift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.shift_processing(init_split=init_split, number_of_shift=num_of_shift, acc_name='Rule-based (shift)', split_status = 'overlap')
        
app = Analyze()
app.run()