import numpy as np
import pandas as pd
import math
def predictForTest(stats,test):
    #initialize the values of probability
    test['prediction']='False'
    test['pos']=None
    test['neg']=None
    for index,rows in test.iterrows():
        posfactor,negfactor=1.0,1.0
        #Doing individually for each attribute
        a=rows['heart_issue']
        for i in range(len(stats[0])):
            if stats[0][i]==a:
                posfactor*=stats[0][i+1] #updating the positive value
                negfactor*=stats[0][i+2] #updating the negative value
                break
        a=rows['insurance']
        for i in range(len(stats[1])):
            if stats[1][i]==a:
                posfactor*=stats[1][i+1]
                negfactor*=stats[1][i+2]
                break
        a=rows['stress']
        for i in range(len(stats[2])):
            if stats[2][i]==a:
                posfactor*=stats[2][i+1]
                negfactor*=stats[2][i+2]
                break
        rows['pos']=posfactor
        rows['neg']=negfactor
        if posfactor>negfactor:
            rows['prediction']='True'
    print(test.head(15))
    x=len(test.index)
    name='ResultForTestFile'+str(x)+'Rows.csv'
    test.to_csv(name,sep=',',index=False)
def findCount(train,test):
    allColumns=list(train)
    stats=[] #includes the attribute, its all possible values and its positive and negative values as well
    attrs=[] #includes each attribute and its possible row values
    for column in allColumns[0:-1]:
        rowAttr=[]
        rowVals=[]
        rowVals.append(column)
        for index,rows in train.iterrows():
            if rows[column] in rowVals:
                continue
            else:
                rowAttr.append(rows[column])
                rowVals.append(rows[column])
                rowVals.append(0)
                rowVals.append(0)
        stats.append(rowVals)
        attrs.append(rowAttr)
    lastrow=[] #To store the values in the last column of the dataset
    count=[]
    for index,rows in train.iterrows():
        if rows['attack'] in lastrow:
            for i in range(len(lastrow)):
                if rows['attack']==lastrow[i]:
                    count[i]+=1
        else:
            lastrow.append(rows['attack'])
            count.append(1)
    heart_issue=[]
    insurance=[]
    stress=[]
    attack=[]
    for index,rows in train.iterrows(): #retrieving the values from the dataframe columns
        heart_issue.append(rows['heart_issue'])
        insurance.append(rows['insurance'])
        stress.append(rows['stress'])
        attack.append(rows['attack'])
    for i in range(len(heart_issue)):
        for j in range(len(stats[0])):
            if stats[0][j]==heart_issue[i] and str(attack[i])=='True': #updating the positive and negative counts
                stats[0][j+1]+=1
            elif stats[0][j]==heart_issue[i] and str(attack[i])=='False':
                stats[0][j+2]+=1
    for i in range(len(insurance)):
        for j in range(len(stats[1])):
            if stats[1][j]==insurance[i] and str(attack[i])=='True':
                stats[1][j+1]+=1
            elif stats[1][j]==insurance[i] and str(attack[i])=='False':
                stats[1][j+2]+=1
    for i in range(len(stress)):
        for j in range(len(stats[2])):
            if stats[2][j]==stress[i] and str(attack[i])=='True':
                stats[2][j+1]+=1
            elif stats[2][j]==stress[i] and str(attack[i])=='False':
                stats[2][j+2]+=1
    for i in range(len(stats)):
        pos=1
        for j in range(len(stats[i][1:])):
            try:
                stats[i][pos+1]/=count[1] #getting the probability fraction
                stats[i][pos+2]/=count[0]
                pos+=3 #based on the stats array
            except:
                continue
    for i in range(len(stats)):
        print(stats[i][0],':',stats[i][1:]) #printing the values of the stats array
    predictForTest(stats,test)
train=pd.read_csv('train.csv')
print('---------------\nTraining data:\n---------------')
print(train.head())
print('\nShape of training dataset is:',train.shape)
test1=pd.read_csv('test.csv') #First testing dataset
print('---------------\nTesting data 1:\n---------------')
print(test1.head())
print('\nShape of first testing dataset is:',test1.shape)
findCount(train,test1)
test2=pd.read_csv('test2.csv') #second testing dataset
print('---------------\nTesting data 2:\n---------------')
print(test2.head())
print('\nShape of second testing dataset is:',test2.shape)
findCount(train,test2)

