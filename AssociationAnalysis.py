import string
import pandas as pd
from itertools import combinations
from matplotlib import pyplot as plt

q5 = pd.read_csv("Q5.csv")#, converters={'Factors': pd.eval}) #pd.eval converts column "factors" to list of ints instead of list of strings.
q8 = pd.read_csv("Q8.csv")
q9 = pd.read_csv("Q9.csv")

def Q5Support1(df, minsup):
    #To be used only with Question 5, which uses a table of numbers and their factors from 1 to 100.
    #Finds all one term support in df given minsup, df must have 2nd col as values in transaction
    sup = []
    for i in enumerate(df["Numbers"]):
        if i[1] == 1:
            s = (len(df[df.iloc[:,1].map(lambda x: "%d,"%i[1] in x)].index)+1) / len(df.index)
        else:
            s = (len(df[df.iloc[:,1].map(lambda x: ",%d,"%i[1] in x)].index)+1) / len(df.index)
        #print(s)
        if s >= minsup:
            sup.append(str(i[1]))
    return sup

def Support(df, minsup, base):
    #Finds and returns list of frequent itemsets in list base given float minsup, df must have 2nd col as values in transaction
    sup = []
    for i in enumerate(base):
        set1 = set(i[1])
        s = len(df[df.iloc[:, 1].str.split(',').map(set1.issubset)]) / len(df.index)
        if s >= minsup:
            sup.append(i[1])
    return sup

def SupConf(df, base, X = []):
    #Prints and returns list of Support, also confidence if given X (denominator in confidence eq)
    sup = []
    for i in enumerate(base):#Find Support, can take list of bases, matches with list of X
        set1 = set(i[1])
        rawdf = df[df.iloc[:,1].str.split(',').map(set1.issubset)]
        #print(rawdf)
        ssub = len(rawdf)
        s = ssub / len(df.index)
        #print("ssub: ", ssub)
        if X != []: #Find confidnece, x is denominator. For rule {1,2}->{3}, conf= s({1,2,3})/s({1,2})
            #print("X access")
            set2 = set(X[i[0]]) #the ith item in X, same position as base
            csub = len(df[df.iloc[:,1].str.split(',').map(set2.issubset)])
            #print("csub: ", csub)
            c = ssub / len(df[df.iloc[:,1].str.split(',').map(set2.issubset)])
            print(["Confidence numerator: ",i[1], "Denominator: ", X[i[0]], "support: ", s, "confidence: ", c])
            sup.append([i[1], X[i[0]], s, c])
            continue
        print(["Full: ",i[1], "support: ", s])
        sup.append([i[1], s])
    return sup

print("##################Q5##################")

df = q5
minsup = .15
minconf = 1

s1 = Q5Support1(df, minsup)
print("Q5b Supported one item itmesets, minsup >= 0.15: ", s1)
sup2 = list(combinations(s1, 2)) #By using only the one item frequent itemsets to generate the
#Two item datasets, we are using the Apriori algorithm.
s2 = Support(df, minsup, sup2) #The candidate sets are prunded
print("Q5b Supported two item itemsets, minsup >= 0.15: ", s2) #And printed

base = [('1','3','6'), ('1', '2', '3', '6'), ('1', '2', '3', '4', '6'), ('1', '2', '3', '4', '6'), ('1', '2', '3', '4', '6')]
X = ['3', ('1', '2', '6'), ('1', '4', '6'), ('1', '2', '3', '6'), ('3', '4')]

print("Support and Confidence for Q5c, in order skipping iii:")
SupConf(df, base, X)

print("###################### Begin of Q6 #######################")
Q61 = ['A', 'C', 'D', 'E']
Q62 = ['B', 'C', 'D', 'E']
print("Combos 1: ", list(combinations(Q61, 3)))
print("Combos 2: ", list(combinations(Q62, 3)))

print("###################### Begin of Q7 #######################")

Q7 = ['X', 'Y', 'Z', 'W']
print("Q7 2 combos: ", list(combinations(Q7, 2)))
print("Q7 3 combos: ", list(combinations(Q7, 3)))

print("###################### Begin of Q8 #######################")
print("Dataframe for question 8: ")
print(q8)
base81 = ['A', 'B', 'C', 'D', 'E']
base82 = list(combinations(base81, 2))
base83 = list(combinations(base81, 3))
base84 = list(combinations(base81, 4))
print("Base set", base81)
print("One item: ")
m81 = SupConf(q8, base81)
print("Two item: ")
m82 = SupConf(q8, base82)
print("Three item: ")
m83 = SupConf(q8, base83)
print("Four item: ")
m84 = SupConf(q8, base84)

#Graphing stuff:
[m82.append(i) for i in m83]
#print(m82)
cats = [str(i[0]) for i in m82]
height = [i[1] for i in m82]

plt.bar(cats, height)
plt.xticks(rotation = 90)
plt.xlabel("Itemsets size 2 and 3")
plt.ylabel("Support")
plt.show()

print("###################### Begin of Q9 #######################")

#Q9 general set up:
# print(q9)
print("Dataframe for Q9, no NAN: ")
q9.iloc[4,1] = ''
print(q9)
base91 = list(string.ascii_uppercase)
base91 = base91[0:10] #Set of all items
#print(base91)
m91 = Support(q9, 0.2, base91)
print("One item sets with minsup >= 0.2: ", m91)
base92 = list(combinations(m91, 2))
#print(base92)
m92 = Support(q9, 0.2, base92)
print("Two item sets with minsup >= 0.2: ", m92)
base93 = list(combinations(m91,3))
m93 = Support(q9, 0.2, base93)
print("Three item sets with minsup >= 0.2; ", m93)
base94 = list(combinations(m91, 4))
m94 = Support(q9, 0.2, base94)
print("Four item sets with minsup >= 0.2: ", m94)

print("Answering table questions for Q9:")
print("1: is {A,B} a maximal frequent itemset?")
baseab = [('A', 'B'), ('A', 'B', 'D'), ('A', 'B', 'E')]
ab = SupConf(q9, baseab)

print("Confidence of rule {A} → {J} is 100 %")
baseaj = [('A', 'J')]
Xa = ['A']
SupConf(q9, baseaj, Xa)
