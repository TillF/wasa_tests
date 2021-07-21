#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 16:49:55 2021

@author: alicelegendre
"""

import os
import pandas as pd



""" FUNCTIONS DEFINITION """

##### Getting the path into the Output folder of the case for the two versions we want to compare

def test_path(folder_version1, folder_version2, case_nb):
    path1 = '/Users/alicelegendre/Desktop/WASA/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_version1, case_nb)
    path2 = '/Users/alicelegendre/Desktop/WASA/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_version2, case_nb)
    
    return path1, path2


##### Read the files and create a datafram for each

def create_df_to_compare(path):
    os.chdir(path)
    file_list = os.listdir(path)
    
    file_names =[]
    df_list = []
    
    #Create list of files we want to compare
    for file in file_list :
        if file.endswith(".out"):
            file_names.append(file)
    
    #Create a list of dataframe. Each dataframe contains one file
    for f in file_names :
        df = pd.read_csv(f, sep='\t', header=1) #header=1 => start at the second line of the file (first line=title +info)
        df_list.append(df)
       
    #return file_list_clean
    return file_names, df_list 



##### Return True or False if the 2 dataframes are identical or not

def simple_comparison(df1, df2):
    comp=df1.equals(df2)
    return comp



##### Comparison of all the files for one case (list of dataframes = 1 dataframe per file)

def comparisonTF(namelist1, dflist1, namelist2, dflist2):
    n= len(dflist1) #we suppose namelist1=namelist2
    res = []
    
    for i in range(n):
        if simple_comparison(dflist1[i], dflist2[i])==False:
            res.append(namelist1[i])
    
    if res == []:
        return "OK"
    else :
        return res #return OK for the case all the files are identical or return the name of the files which are different into one case


##### Calculation of the error

def error_calculation(v1, v2):
    e1 = abs(v1-v2)/v1
    e2 = abs(v1-v2)/v2
    error = round((e1+e2)/2,3)  #to have 3 decimal places
    return error



##### Check if the error is acceptable or not

def comparison_threshold(error_exact, error_acceptable):
    if error_exact <= error_acceptable :
        return True
    else :
        return False



##### Compare the files in pairs for one case and the result is a list containing list each with two elements : the name of the file and the maximum error we found in the file

def comparisonBIG(namelist1, dflist1, namelist2, dflist2):
    nb_files = len(dflist1)
    sort1 = []
    sort1_name = []
    
    for i in range(nb_files):
        if simple_comparison(dflist1[i], dflist2[i])==False:
            sort1.append([dflist1[i], dflist2[i]])
            sort1_name.append(namelist1[i])
    
    n = len(sort1) #=len(L) 
    L_df = [] #list after the comparison so it contains a dataframe with the values which are different = values we have to compare and calculate the difference error there is between them
    L = [] #list of lists which contain the dataframes converted into lists
    final_result = []
    
    for j in range(n):
        L_df.append(sort1[j][0].compare(sort1[j][1]))
        L.append(L_df[j].values.tolist())
    
    for k in range(n):
        m = len(L[k])
        S = []
        for p in range(m):
            cal = error_calculation(L[k][p][0], L[k][p][1])
            S.append(cal)
        max_error = max(S)
        
        final_result.append([sort1_name[k], max_error]) #to have the name file with the error
            
    
    return final_result



""" CALCULATIONS """

#"""
new_version_folder = 'version1'
old_version_folder = 'version2'
nb_cases = 3
c=0 #counter 
threshold = 0.02
general_results = []

result_file = open("test_results2", mode = 'w+')
result_file.truncate()
result_file.write('This file present the results of the comparison of the out files for version 1 and version 2 made with the Python code WASAoutputSimilarityTest. \n See what we get for each case of study : \n')


for k in range(11,11+nb_cases):
    p_new, p_old = test_path(new_version_folder, old_version_folder, k)
    name_new, df_new = create_df_to_compare(p_new)
    name_old, df_old = create_df_to_compare(p_old)
    result = comparisonBIG(name_new, df_new, name_old, df_old)
    for q in result: #q[0] file name and q[1] error associated
        if comparison_threshold(q[1],threshold)==True:  
            result.remove(q)
    if result==[]:
        general_results.append('OK') #=> no significant error or no error at all
    else:
        general_results.append(result)


for l in general_results:
    c+=1
    if l != 'OK':
        print('Case ',c, ' : ERROR => ', l, '\n \n')
        result_file.writelines(['\n Case ',str(c), ' : ERROR =>', str(l), '\n'])
    else :
        print('Case ',c, ' : OK \n')
        result_file.writelines(['\n Case ', str(c), ' : OK \n'])


result_file.close()

#"""




"""
new_version_folder = 'version1'
old_version_folder = 'version2'
nb_cases = 10
general_results = []
c=0 #counter 

result_file = open("test_results", mode = 'w+')
result_file.truncate()
result_file.write('This file present the results of the comparison of the out files for version 1 and version 2 made with the Python code WASAoutputSimilarityTest. \n See which files are different for each case of study : \n')

for k in range(1,nb_cases+1):
    p_new, p_old = test_path(new_version_folder, old_version_folder, k)
    name_new, df_new = create_df_to_compare(p_new)
    name_old, df_old = create_df_to_compare(p_old)
    result = comparisonTF(name_new, df_new, name_old, df_old)
    general_results.append(result)


for l in general_results:
    c+=1
    if l != 'OK':
        print('Case ',c, ' : ERROR => ', l, '\n \n')
        result_file.writelines(['\n Case ',str(c), ' : ERROR =>', str(l), '\n'])
    else :
        print('Case ',c, ' : OK \n')
        result_file.writelines(['\n Case ', str(c), ' : OK \n'])


result_file.close()

#print(general_results)
"""    




