# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 16:31:52 2021

@author: alicelegendre
"""

import os
import pandas as pd
import math



"""  FUNCTIONS DEFINITION  """

def RUNexe(case_nb):
    os.chdir('G:\Documents\wasa_tests')
    command = 'exeRunFolder\wasa.exe %d\do.dat > Outputs/Output%d/Protocol.txt'%(case_nb,case_nb)
    os.system(command)

#def CreatePath(folder_reference, folder_newversion, case_number):
#    path_ref = 'G:/Documents/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_reference, case_number)
#    path_new = 'G:/Documents/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_newversion, case_number)
#    #path_ref = '/Users/alicelegendre/Desktop/WASA/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_reference, case_number)
#    #path_new = '/Users/alicelegendre/Desktop/WASA/wasa_tests/WASA_pyProject/test_folder/%s/Outputs/Output%d'% (folder_newversion, case_number)
#    return path_ref, path_new

def CreatePath(case_number):
    path_ref = 'G:/Documents/wasa_tests/OutputsRefFakeBis/Output%d'% (case_number)
    path_new = 'G:/Documents/wasa_tests/OutputsFake/Output%d'% (case_number)
    return path_ref, path_new


##### Gives a list of file names which are into the folder given by the path 

def FileNamesList(path):
    os.chdir(path)
    file_list = os.listdir(path)
    #Delete the files we don't want to compare
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



##### Read a file, create a datafram and return  it 

def CreateDf(file_name,path): #path = where is the file
    os.chdir(path)
    df = pd.read_csv(file_name, 'b', engine='python', delimiter='\t', header=1) #header=1 => start at the second line of the file (first line=title +info))
    #df = pd.read_csv(file_name, sep='\t', header=1) 
    return df


##### Return OK if the 2 dataframes are identical and the name of the file if they are not

def TFcomparison(df1, df2): #True/False comparison
    comp=df1.equals(df2)
    return comp
    #if comp == True:
    #    return 'OK'
    #else:
    #    return file_name


##### Calculation of the error

def ErrorCalculation(ref, value):
    if math.isnan(ref)==True and math.isnan(value)==True:
        return 0
    elif ref==0:
        e = abs(ref-value)
    else:
        e = abs(ref-value)/ref
    #error = round(e, 4)*100  #to have 3 decimal places and in %
    error = float("{:.2f}".format(e))*100
    return error


##### Check if the error is acceptable or not

def ComparisonThreshold(error_exact, error_acceptable):
    if error_exact <= error_acceptable :
        return True
    else :
        return False


#####  Compare if two df are identical or not thanks to the threshold

def GeneralComparison(file_name, dfRef, dfNew, error_acceptable, textFile):
    TF = TFcomparison(dfRef, dfNew)
    if TF == True:
        return TF
    else:  
        CompDf=dfRef.compare(dfNew) #resulting dataframe of the comparison (contains the data which differ from the ref to the other one)
        CompList=CompDf.values.tolist() #convert the df into a list
        n = len(CompList)
        S = []
        for j in range(n):
            m = len(CompList[j])
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


##### Different verification to make before comparing the data

def IssueFilePresence(namelistRef, namelistNew):
    diff1=list(set(namelistRef)-set(namelistNew))
    diff2=list(set(namelistNew)-set(namelistRef))
    res = []
    if diff1 != []:
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



def IssueEmptyFile(dfRef, dfNew, file_name):
    R = len(dfRef)
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
    


def MainLoop(path_ref, path_new, names_list, error_acceptable, textFile):
    result = []
    filesToDelete = []
    for name in names_list:
        df_ref = CreateDf(name,path_ref)
        df_new = CreateDf(name,path_new)
        #print('dfRef=',df_ref)
        #print('dfNew=',df_new)
        IEF= IssueEmptyFile(df_ref, df_new, name)
        if IEF != []:
            print(IEF[0],'\n')
            textFile.writelines([IEF[0], '\n'])
            filesToDelete.append(name)
    resultingNamesList=list(set(names_list)-set(filesToDelete))
    for nameB in resultingNamesList: 
        df_ref2 = CreateDf(nameB,path_ref)
        df_new2 = CreateDf(nameB,path_new)
        #print('dfRef2=',df_ref2)
        #print('dfNe2w=',df_new2)
        #print('name=',nameB)
        GC=GeneralComparison(nameB, df_ref2, df_new2, threshold, textFile)
        #print('GC=',GC)
        if GC != True:
            result.append(GC)
    return result





"""  CALCULATIONS  """

reference_folder = 'version1'
newVersion_folder = 'version2'
nb_cases = 16
c=0 #counter 
threshold = 20 #%
general_results = []
cases=[1,2,3,4,5,6,11,12,13,14,15,16]
#cases=[1]

#os.chdir('G:/Documents/wasa_tests/WASA_pyProject')
resultTextFile = open("test_results", mode = 'w+')
resultTextFile.truncate()
resultTextFile.write('\nThis file presents the results of the similarity checking of the output files between the reference (benchmark) and the new version of WASA-SED by using the Python code WASAoutputSimilarityTest.')
resultTextFile.write('\nNOTE: The file names which appear in the section -General issues- are not compared. We only compare the files which are possible to compare.  \n\n')

for k in range(1,nb_cases+1): #11,11+nb_cases
#for k in cases:
    print(k)
    #RUNexe(k)
    #pathRef, pathNew = CreatePath(reference_folder, newVersion_folder, k)
    pathRef, pathNew = CreatePath(k)
    listNamesRef = FileNamesList(pathRef)
    listNamesNew = FileNamesList(pathNew)
    IFPmessage, listOfName = IssueFilePresence(listNamesRef, listNamesNew)
    resultTextFile.writelines(['\n\n* Case ', str(k), ' :\n'])
    resultTextFile.write('   - General issues : \n\n')
    if IFPmessage != []:
        for l in IFPmessage:
            print(l,'\n')
            resultTextFile.writelines([l, '\n\n'])
        res = MainLoop(pathRef, pathNew,listOfName, threshold, resultTextFile)
    else:
        res=MainLoop(pathRef, pathNew, listOfName, threshold, resultTextFile)
         
    resultTextFile.write('\n   - Data comparison result : \n')
    if res != []:
        print('Case ',k, ' : ERROR => ', res, '\n \n')
        resultTextFile.writelines(['\n     ERROR =>', str(res), '\n'])
    else :
        print('Case ',k, ' : OK \n')
        resultTextFile.writelines(['\n     OK \n'])

resultTextFile.close()
print('__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __\n')
print('The results of this similarity checking are presented is the file test_results saved in the folder WASA_pyProject.')
print('\n__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __')
