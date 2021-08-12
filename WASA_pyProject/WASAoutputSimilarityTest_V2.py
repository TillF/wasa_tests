# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 16:31:52 2021

@author: alicelegendre
"""

import os
import pandas as pd
import math



"""  FUNCTIONS DEFINITION  """

##### This function runs the executable of WASA-SED to run the case we want. The entry is just the case number
def RUNexe(case_nb):
    os.chdir('G:\Documents\wasa_tests') #we go into the folder wasa_tests
    command = 'exeRunFolder\wasa.exe %d\do.dat > Outputs/Output%d/Protocol.txt'%(case_nb,case_nb) #the command we want to execute
    os.system(command) #we execute the command



##### For the case we want, it gives the paths of the output files for the reference (OutputsREF) and for the new version (Outputs)
def CreatePath(case_number):
    path_ref = 'G:/Documents/wasa_tests/OutputsREFfake/Output%d'% (case_number)
    path_new = 'G:/Documents/wasa_tests/OutputsFake/Output%d'% (case_number)
    return path_ref, path_new



##### List of file names creation from a path. It gives a list of file names which are into the folder given by the path
### We remove the files Protocol.txt and parameter.out that we don't need to compare (also the file .DS+Store which appears on mac)
### For the moment we remove also the .stat files because they don't have the good organization to compare them => adapt the code
def FileNamesList(path):
    os.chdir(path)
    file_list = os.listdir(path) #list ofthe names of all the files which are in the folder considered
    for file in file_list :
        if file == 'Protocol.txt':
            file_list.remove(file)
        elif file == 'parameter.out':
            file_list.remove(file)
        elif file == '._.DS_Store':
            file_list.remove(file)
    for f in file_list:
        if f=='.DS_Store':
            file_list.remove(f)
    for f2 in file_list:
        if f2.endswith(".stat"):
            file_list.remove(f2)
    for f1 in file_list:
        if f1.endswith(".stat_start"):
            file_list.remove(f1)
    for f4 in file_list:
        if f4.endswith(".stats"):
            file_list.remove(f4)
    for f3 in file_list:
        if f3.endswith(".stat_start"):
            file_list.remove(f3)
    for f5 in file_list:
        if f5.endswith(".stats_start"):
            file_list.remove(f5)
    return file_list



##### Dataframe creation from a file name. It takes a file name and the path to have access to it and then convert the file into a dataframe 
def CreateDf(file_name,path): #path = where is the file
    os.chdir(path)
    df = pd.read_csv(file_name, 'b', engine='python', delimiter='\t', header=1) #header=1 => start at the second line of the file (first line=title +info)) #delimiter=/t we choose tab as a delimiter between the columns #'b' option permits to read thef binary files (the files .start can be read thanks to this option))
    #df = pd.read_csv(file_name, sep='\t', header=1) 
    return df



##### Simple comparison between two dataframes. It returns 'True' if the 2 dataframes are identical and 'False' if they are not
def TFcomparison(df1, df2): #True/False comparison
    comp=df1.equals(df2)
    return comp



##### Calculation of the error
def ErrorCalculation(ref, value):
    if math.isnan(ref)==True and math.isnan(value)==True: #the case with NaN for the self and the other data = they are equals *see more explanations in the report
        return 0
    elif ref==0: #we don't want to devide by 0 so with just take to ifference when the reference is 0
        e = abs(ref-value)
    else:
        e = abs(ref-value)/ref
    error = float("{:.2f}".format(e))*100 #We want the error in percentage and only 2 decimal numbers
    return error



##### It checks if the error calculated (error_exact) is over or under the thresold we choose (error_acceptable).
def ComparisonThreshold(error_exact, error_acceptable):
    if error_exact <= error_acceptable :
        return True
    else :
        return False



#####  Compare if two df are considered as identical or not.
### 1) If they are exactly identical (test with TFcomparison)) we don't need to continue the comparison
### 2) If not, with dataframe.compare() we get an df with the data which are different between the two df
### -> if we have an imcomparable value such as *** or NaN we do not continue
### -> if not, we caculate the error for each data and append it into a list S.
### 3) We take the maximum error of this list ! maximum error of the file
### 4) We compare this error with the threshold
### -> if under : we consider the error negligible
### -> if over : we keep the error associated (we write it in percentage) with the file
def GeneralComparison(file_name, dfRef, dfNew, error_acceptable, textFile):
    TF = TFcomparison(dfRef, dfNew)
    if TF == True:
        return TF 
    else:  
        CompDf=dfRef.compare(dfNew) #resulting dataframe of the comparison (contains the data which differ from the ref to the other one)
        CompList=CompDf.values.tolist() #convert the df into a list to have access to the data
        n = len(CompList) #list size
        S = []
        for j in range(n):
            m = len(CompList[j]) #the number of lines in the CompDf
            for i in range(0,m,2):
                if i<m:
                    if isinstance(CompList[j][i], str)==True or isinstance(CompList[j][i+1], str)==True or (math.isnan(CompList[j][i])==True and math.isnan(CompList[j][i+1])==False) or (math.isnan(CompList[j][i])==False and math.isnan(CompList[j][i+1])==True):
                        textFile.write('Incomparable value in the file '+file_name+'.\n')
                        return True #so in the function MainLoop nothing will be write in the final list, just the message for the error
                    else:
                        cal = ErrorCalculation(CompList[j][i], CompList[j][i+1])
                        S.append(cal)
        max_error = max(S)
        written_error = str(max_error)+'%'
        TFerror = ComparisonThreshold(max_error, error_acceptable)
        if TFerror == True:
            return TFerror
        else:
            return [file_name, written_error]



##### First verification to do before comparing the data: checking if we have the same files into the two version of the outputs
### If in one of the folder we have a file which is not present in the other folder, we remove it from the file names list because we can't compare it.
def IssueFilePresence(namelistRef, namelistNew):
    diff1=list(set(namelistRef)-set(namelistNew)) #= the names present in namelistRef but not in namelistNew
    diff2=list(set(namelistNew)-set(namelistRef)) #= the names present in namelistNew but not in namelistRef
    res = [] #empty list to append the results
    if diff1 != []: #= they are files in reference that are not in the new version
        bonus_file=''
        for name in diff1:
            bonus_file=bonus_file+name+', '
            namelistRef.remove(name)
        res.append('    The file(s) '+bonus_file+' is (are) missing in the new version.')
    if diff2 != []:
        bonus_file2=''
        for name2 in diff2:
            bonus_file2=bonus_file2+name2+', '
        res.append('    The file(s) '+bonus_file2+' is (are) present in the new version but missing in the reference.')
    return res, namelistRef #If the two list names are identical res = [] | res =  the error message and namelistRef the files we can compare



##### Second verification to do before comparing the data: checking if the file is empty or if in the file there is more data for one version than for the other = more lines.
def IssueEmptyFile(dfRef, dfNew, file_name):
    R = len(dfRef) #size of the datframe=number of lines
    N = len(dfNew)
    res = []
    if R>N:
        if N==0:
            res.append('    The file '+file_name+' is empty in the new version.')
        else:
            res.append('    There are missing data in the file '+file_name+' for the new version.')
    elif R<N:
        if R==0:
            res.append('    The file '+file_name+' is empty in the reference.')
        else:
            res.append('    There are extra data in the file '+file_name+' for the new version.')
    return res #if the two df have at list one line of data (so len>=2) and have the same length, res=[]
    


##### Main part : it uses the other functions
def MainLoop(pathRef, pathNew, namesList, errorAcceptable, textFile):
    result = []
    filesToDelete = []
    for name in namesList: #take each name in the file names list
        df_ref = CreateDf(name,pathRef) #create the dataframe for each version from the file name
        df_new = CreateDf(name,pathNew)
        IEF= IssueEmptyFile(df_ref, df_new, name) #ckeck if the file are empty of if there is extra data
        if IEF != []: #there is extra data or empty file so
            print(IEF[0],'\n')
            textFile.writelines([IEF[0], '\n']) #we write an error message in the result text file
            filesToDelete.append(name) #we keep this file name apart to delete it because we won't compare the two versions of this file
    resultingNamesList=list(set(namesList)-set(filesToDelete)) #we remove the file names contained into filesToDelete from the file names list names_list
    for nameB in resultingNamesList: #take each name of the new file names list (if for the case there is no issue (=no empty file or extra data), we will get names_list=resultingNamesList)
        df_ref2 = CreateDf(nameB,pathRef)
        df_new2 = CreateDf(nameB,pathNew)
        GC=GeneralComparison(nameB, df_ref2, df_new2, errorAcceptable, textFile)
        if GC != True: #because if GC=True that means the files are identical
            result.append(GC)
    return result





"""  CALCULATIONS  """

nb_cases = 16 #number of cases we study 
threshold = 20 #%


#os.chdir('G:/Documents/wasa_tests/WASA_pyProject') #already there because this is where the code is
resultTextFile = open("test_results", mode = 'w+') #create the file or open it if it already exists
resultTextFile.truncate() #delete what there is written in the file
resultTextFile.write('\nThis file presents the results of the similarity checking of the output files between the reference (benchmark) and the new version of WASA-SED by using the Python code WASAoutputSimilarityTest_v2.')
resultTextFile.write('\nNOTE: The file names which appear in the section -General issues- are not compared. We only compare the files which can be compared.  \n\n')

for k in range(1,nb_cases+1):
    #RUNexe(k) #it runs the WASA-SED for each case of study 
    pathRef, pathNew = CreatePath(k) #we get the paths
    listNamesRef = FileNamesList(pathRef)
    listNamesNew = FileNamesList(pathNew)
    IFPmessage, listOfName = IssueFilePresence(listNamesRef, listNamesNew) #If there is some missing file, the error message will be contain in IFPmessage and the list of file names we will compare will be listOfName
    resultTextFile.writelines(['\n\n* Case ', str(k), ' :\n'])
    resultTextFile.write('   - General issues : \n\n')
    if IFPmessage != []:
        for l in IFPmessage:
            resultTextFile.writelines([l, '\n\n']) #write the error message into the text file
        res = MainLoop(pathRef, pathNew,listOfName, threshold, resultTextFile)
    else:
        res=MainLoop(pathRef, pathNew, listOfName, threshold, resultTextFile)
         
    resultTextFile.write('\n   - Data comparison result : \n')
    if res != []: #res will contain a list of lists such as [[filename, 22%], [filename2, 50%]]
        resultTextFile.writelines(['\n     ERROR =>', str(res), '\n'])
    else : #that means res=[] and so we did not keep a file name with an error so => all the files are identical for this case k
        resultTextFile.writelines(['\n     OK \n'])

resultTextFile.close()
print('__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __\n')
print('The results of this similarity checking are presented is the file test_results saved in the folder WASA_pyProject.')
print('\n__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __')


