import numpy as np
import math
def findThreeAssociation(pair,iapt,minSupport): #finding association of 3 items
    allItems=[]
    pairs=[]
    pairOfThree=[] #array for pairs of three
    for k in pair:
        l=k.strip('[|]').split(',')
        for i in range(len(l)):
            l[i]=int(l[i].strip())
        pairs.append(l)
        itemname=k.strip('[|]').split(',')
        for i in range(len(itemname)):
            if int(itemname[i].strip()) in allItems:
                continue
            else:
                allItems.append(int(itemname[i].strip()))
    #Finding all pairs of 3 in the allItems array. 
    pos,pos1,pos2=0,1,2
    for i in range(0,len(allItems)-2):
        for j in range(i+1,len(allItems)-1):
            for k in range(j+1,len(allItems)): #loops for finging all the pairs of 3
                if ([allItems[i],allItems[j]] in pairs or [allItems[j],allItems[i]] in pairs) and ([allItems[j],allItems[k]] in pairs or [allItems[k],allItems[j]] in pairs) and ([allItems[i],allItems[k]] in pairs or [allItems[k],allItems[i]] in pairs):
                    pairOfThree.append([allItems[i],allItems[j],allItems[k]])
                else:
                    continue
    supVal=[] #array for support value of each pair of three
    for i in range(len(pairOfThree)):
        supVal.append(0)
    for i in range(len(pairOfThree)):
        for j in range(len(iapt)):
            for k in range(len(pairOfThree[i])):
                if pairOfThree[i][k] in iapt[j]:
                    if k==len(pairOfThree[i])-1: #checking the support value
                        supVal[i]+=1
                    else:
                        continue
                else:
                    break
    print('Association of 3 items..')
    print('---------------------------------------')
    print('Pair\t\t\tSupport_Value')
    print('---------------------------------------')
    for i in range(len(pairOfThree)):
        print(str(pairOfThree[i]),'\t\t\t',supVal[i])
    print('Items selected above minimum support..')
    print('---------------------------------------')
    print('Pair\t\t\tSupport_Value')
    print('---------------------------------------')
    count=0
    for i in range(len(pairOfThree)):
        if supVal[i]>=minSupport:
            print(str(pairOfThree[i]),'\t\t\t',supVal[i])
            count+=1
    if count<=1: #if only one pair remains
        print('No More Association possible..')
def increaseItems(itemNum,itemCount,iapt,minSupport):
    npr = math.factorial(len(itemNum))/math.factorial(len(itemNum)-2) #to get total number of pairs possible
    count=int(npr/math.factorial(2)) #nCr formula
    pos1,pos2=0,1
    pair={}
    for i in range(count):
        for item in iapt:
            if itemNum[pos1] in item and itemNum[pos2] in item:
                if str([itemNum[pos1],itemNum[pos2]]) in pair.keys():
                    pair[str([itemNum[pos1],itemNum[pos2]])]+=1 #adding the pairs in array and checking support value
                else:
                    pair[str([itemNum[pos1],itemNum[pos2]])]=1 #adding in dictionary
        if pos2==len(itemNum)-1:
            pos1+=1
            pos2=pos1+1 #for all pairs
        else:
            pos2+=1
    if len(pair)<2:
        print('No more association possible!') #stopping if only one pair exists
    else:
        print('Selecting above Minimum support..')
        print('---------------------------------------')
        print('Pair\t\t\tSupport_Value')
        print('---------------------------------------')
        for key,value in pair.items():
            if value>=minSupport:
                print(str(','.join(key.strip('[|]').split(','))),'\t\t\t',value)
    if len(pair)>=2:
        findThreeAssociation(pair,iapt,minSupport)
def findAssociation(itemNum,itemCount,minSupport,itemAsPerTransaction): #to check the association of 2 items
    print('---------------------------------------')
    print('Transactions selected above minimum support:')
    print('---------------------------------------')
    print('Item_Name\t\tSupport_Value')
    print('---------------------------------------')
    for i in range(len(itemCount)):
        try:
            if(itemCount[i]<minSupport): #checking above min support and removing unwanted
                itemCount.pop(i)
                itemNum.pop(i)
        except:
            break
    for i in range(len(itemCount)):
        print('\t',itemNum[i],'\t\t\t',itemCount[i])
    print('Finding association of 2 items:')
    increaseItems(itemNum,itemCount,itemAsPerTransaction,minSupport)
def checkCount(items,n,minSupport,conf):
    itemNum=[]
    itemCount=[]
    itemAsPerTransaction=[] #storing the transactions in array
    for i in range(len(items)):
        itemAsPerTransaction.append(list(map(int,items[i].split())))
        listItems=map(int,items[i].split())
        for l in listItems:
            if l in itemNum:
                for j in range(len(itemNum)):
                    if itemNum[j]==l:
                        itemCount[j]+=1
            else:
                itemNum.append(l)
                itemCount.append(1)
    print('---------------------------------------')
    print('Item_Name\t\tSupport_Value')
    print('---------------------------------------')
    for i in range(len(itemCount)):
        print('\t',itemNum[i],'\t\t\t',itemCount[i])
    findAssociation(itemNum,itemCount,minSupport,itemAsPerTransaction)
n=int(input('Enter the number of transactions:'))
items=[]
for i in range(n):
    print('Enter the items in transaction ',i+1,':')
    items.append(input())
minSupport=int(input('Enter the minimum support:'))
conf=int(input('Enter the confidence percentage:'))
checkCount(items,n,minSupport,conf)

