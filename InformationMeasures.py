#Author: Destiny Ziebol

import pandas as pd
import math
hw1 = pd.read_csv("HW2_Q_S22_1.csv")
#HW2_Q_S22_1.csv is a direct import from the PDF, with classes encoded as C1 = 1 and C0 = 0.

def GiniIndex(x, CID, sort="off"):
    #X = data frame, class = number of col that has class info, sort = optional parameter of col # to sort on.
    n = len(x.iloc[:,0])
    #print("N: ", n)
    if sort != "off":
        #print("Sort Active")
        xs = []
        wsum = 0
        splitInfo = 0
        for i in enumerate(set(x.iloc[:,sort])):
            xs.append(x.loc[x.iloc[:,sort]==i[1]]) #where xs is a list of data frames, each containing only one value in the specified column.
            #print(i[1])
            #print(xs)
        for x in xs: #For each df in the list xs
            gsum= 0
            for i in enumerate(set(x.iloc[:,CID])): #For every list, each catagory (0 or 1 in this case, should work with >2 categories)
                counter = 0
                for j in x.iloc[:,CID]: #For every item in the df x, check for the item i
                    if j == i[1]:
                        counter +=1
                gsum += (counter/len(x))**2
                # print("Class: ", i, " Count: ", counter, "p2: ", (counter/len(x))**2)
                # print("Gsum: ", gsum, "Gini: ", 1-gsum, " Weight: ", len(x), n, (len(x)/n), "WEIGHTED gini: ", (len(x)/n) * (1-gsum))
                # print("wsum: ", wsum)
                # print("-----------------------")
            wsum += (len(x)/n) * (1-gsum) #once for each list x
            splitInfo += (len(x)/n) * math.log2((len(x)/n)) # once for each list x
            #print("split i: ", (len(x)/n) * math.log2((len(x)/n)), "split info: ", splitInfo)
        print("Split Info: ",-splitInfo)
        return(wsum)
    gsum= 0
    #print("Sort Not Active")
    for i in enumerate(set(x.iloc[:,CID])):
        counter = 0
        for j in x.iloc[:,CID]:
            if j == i[1]:
                counter +=1
        gsum += (counter/len(x))**2
        # print(counter)
        # print(i)
    return(1-gsum)

def ClassError(x, CID, sort="off"):
    #X = data frame, class = number of col that has class info, supply sort with col # to sort on.
    n = len(x.iloc[:,0])
    #print("N: ", n)
    if sort != "off":
        #print("Sort Active")
        xs = []
        wsum = 0
        for i in enumerate(set(x.iloc[:,sort])):
            xs.append(x.loc[x.iloc[:,sort]==i[1]])
            #print(i[1])
            #print(xs)
        for x in xs:
            cesum= []
            for i in enumerate(set(x.iloc[:,CID])): #For every list, each catagory
                counter = 0
                for j in x.iloc[:,CID]:
                    #counter = 0
                    if j == i[1]:
                        counter +=1
                cesum.append(counter/len(x))
                # print("Class: ", i, " Count: ", counter, "p2: ", (counter/len(x))**2)
                # print("cesum: ", cesum, " Weight: ", len(x), n, (len(x)/n))
                # print("wsum: ", wsum)
                # print("-----------------------")
            wsum += (len(x)/n) * (1-max(cesum))
        return(wsum)
    cesum= []
    #print("Sort Not Active")
    for i in enumerate(set(x.iloc[:,CID])):
        counter = 0
        for j in x.iloc[:,CID]:
            if j == i[1]:
                counter +=1
        cesum.append(counter/len(x))
        # print(counter)
        # print(i)
    return(1-max(cesum))

def Entropy(x, CID, sort="off"):
    #X = data frame, class = column number that has class info, supply sort with col # to sort on.
    n = len(x.iloc[:,0])
    #print("N: ", n)
    if sort != "off":
        #print("Sort Active")
        xs = []
        wsum = 0
        for i in enumerate(set(x.iloc[:,sort])):
            xs.append(x.loc[x.iloc[:,sort]==i[1]])
            #print(i[1])
            #print(xs)
        for x in xs:
            esum= 0
            for i in enumerate(set(x.iloc[:,CID])): #For every list, each catagory
                counter = 0
                for j in x.iloc[:,CID]:
                    if j == i[1]:
                        counter +=1
                pi = (counter/len(x))
                esum += -1*pi*math.log2(pi)
                # print("Class: ", i, " Count: ", counter, "Node Entropy ", -1*pi*math.log2(pi))
                # print("Esum: ", esum, " Weight: ", len(x), n, (len(x)/n), "WEIGHTED entropy: ", (len(x)/n) * -1*pi*math.log2(pi))
                # print("wsum: ", wsum)
                # print("-----------------------")
            wsum += (len(x)/n) * esum
        return(wsum)
    esum= 0
    #print("Sort Not Active")
    for i in enumerate(set(x.iloc[:,CID])):
        counter = 0
        for j in x.iloc[:,CID]:
            if j == i[1]:
                counter +=1
        pi = (counter/len(x))
        esum += -1*pi*math.log2(pi)
        # print("Class: ", i, " Count: ", counter, "Node Entropy ", -1*pi*math.log2(pi))
        # print("Esum: ", esum, " Weight: ", len(x), n, (len(x)/n), " WEIGHTED entropy: ", (len(x)/n) * -1*pi*math.log2(pi))
        # #print("wsum: ", wsum)
        # print("-----------------------")
    return(esum)

print("Gini index, also prints split info")
root = GiniIndex(hw1, 3)
print("no sort: ", root)
print("Movie ID: ", GiniIndex(hw1, 3, sort = 0))
print("Format: ", GiniIndex(hw1, 3, sort = 1))
print("Movie Category: ",GiniIndex(hw1, 3, sort = 2))

print("Gini Gain Ratio: ")
print("Movie ID: ", (root - GiniIndex(hw1, 3, sort = 0))/4.321928094887363)
print("Format: ", (root-GiniIndex(hw1, 3, sort = 1))/0.9709505944546686)
print("Movie Category: ",(root - GiniIndex(hw1, 3, sort = 2))/1.5219280948873621)

print("-----------------------------------")

print("Misclassificaiton Error")
root = ClassError(hw1, 3)
print("no sort: ", root)
print("Movie ID: ", ClassError(hw1, 3, sort = 0))
print("Format: ", ClassError(hw1, 3, sort = 1))
print("Movie Category: ", ClassError(hw1, 3, sort = 2))

print("Misclassification Error Gain Ratio: ")
print("Movie ID: ", (root - ClassError(hw1, 3, sort = 0))/4.321928094887363)
print("Format: ", (root - ClassError(hw1, 3, sort = 1))/0.9709505944546686)
print("Movie Category: ", (root - ClassError(hw1, 3, sort = 2))/1.5219280948873621)

print("-----------------------------------")

print("Entropy")
root = Entropy(hw1, 3)
print("no sort: ", root)
print("Movie ID: ", Entropy(hw1, 3, 0))
print("Format: ", Entropy(hw1, 3, 1))
print("Movie Category: ", Entropy(hw1, 3, 2))

print("Entropy Gain Ratio: ")
print("Movie ID: ", (root - Entropy(hw1, 3, 0))/4.321928094887363)
print("Format: ", (root - Entropy(hw1, 3, 1))/0.9709505944546686)
print("Movie Category: ", (root - Entropy(hw1, 3, 2))/1.5219280948873621)


