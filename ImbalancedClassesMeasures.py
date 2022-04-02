import pandas as pd
from matplotlib import pyplot as plt
q1 = pd.read_csv("Q1.csv")

#print(q1)

def TPFPR(df, tccol, pcol): #Short for 'True Pos False Pos Rate'
    # takes a dataframe, a column number for the true class, and a column number for the model probability for positive class.
    # Accepts only two class datasets coded as + and -
    tpfpr = []  # list of dictionaries of TPR and FPR
    df1 = df.sort_values(df.columns[pcol])  # , ascending=False)
    #print(df1)
    t = 0
    for i in enumerate(df1.iloc[:,pcol].unique()): #For each t value in the sorted dataframe
        #print(i)
        t = i[1]
        c = confmatrix(df1, tccol, pcol, t)
        #print("TPFPR C matrix: ", c)
        #print('TPR/Recal: ', TPR(c))
        tpfpr.append({'TPR': TPR(c), 'FPR': FPR(c), 't': t})
    return tpfpr


def confmatrix(df, tccol, pcol, t):
    #Data frame, true class column (should be 1) and probability column (should be 2 or 3)
    cm = [0, 0, 0, 0]  # TP, FP, TN, FN
    #print("Confmat t: ", t)
    #print(df.iloc[:,pcol])
    for i in range(len(df.index)):
        #print("confmat i: ", i, df.iloc[i, pcol], df.iloc[i, tccol])
        if df.iloc[i, pcol] >= t:  # for all values above threshold t
            if df.iloc[i, tccol] == '+':  # True positives
                #print("confmat TP")
                cm[0] += 1
            if df.iloc[i, tccol] != '+':
                #print("confmat FP")
                cm[1] += 1  # False Positives
        else:
            if df.iloc[i, tccol] == '-':  # True negetives
                #print("confmat TN")
                cm[2] += 1
            if df.iloc[i, tccol] != '-':  # False negetives
                #print("confmat FN")
                cm[3] += 1
    #print(cm)
    return cm

def TPR(cm): #Same as Recall
    #Takes a confusiton matrix as list of TP, FP, TN, FN
    return cm[0]/(cm[0]+cm[3]) #TP/TP+FN

def FPR(cm):
    return cm[1]/(cm[1]+cm[2]) #FP/FP+TN

def Precision(cm):
    return cm[0]/(cm[0]+cm[1]) #TP/TP+FP

def Fmeasure(cm):
    return 2*cm[0] / ((2*cm[0]) + cm[3] + cm[1]) #2TP / 2TP + FN + FP


roc = pd.DataFrame(TPFPR(q1, 1, 2))
#print(roc)
roc2 = pd.DataFrame(TPFPR(q1, 1, 3))
#print(roc2)
#roc.to_csv('m1ROC.csv')

#print(confmatrix(q1, 1, 2, .25))
plt.axis([-0.01,1.02,-0.01,1.02])  #xlim = (0,1), ylim = (0,1)
plt.plot(roc['FPR'], roc['TPR'], label = "M1", color = 'blue')
plt.plot(roc2['FPR'], roc2['TPR'], label = "M2", color = 'orange', linestyle = 'dashed')
plt.plot(roc['t'], roc['t'], label = "Random classifier", color = 'green')
plt.axline((1, 1), slope=1)
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.show()

print('###for t = .4 ###')

# TP, FP, TN, FN
print("M1:")
cm = confmatrix(q1, 1, 2, 0.4)
print("M1, t = 0.4")
print("confusion matrix, t = 0.4: ", cm)
print("Precision: ", Precision(cm))
print("Recall: ", TPR(cm))
print("F-measure: ", Fmeasure(cm))

print('M2:')
cm = confmatrix(q1, 1, 3, 0.4)
print("M2, t = 0.4")
print("confusion matrix, t = 0.4: ", cm)
print("Precision: ", Precision(cm))
print("Recall: ", TPR(cm))
print("F-measure: ", Fmeasure(cm))

print('###for t = .7 ###')

print('#M1:')
cm = confmatrix(q1, 1, 2, 0.7)
print("M1, t = 0.7")
print("confusion matrix, t = 0.7: ", cm)
print("Precision: ", Precision(cm))
print("Recall: ", TPR(cm))
print("F-measure: ", Fmeasure(cm))

print('#M2: ')
cm = confmatrix(q1, 1, 3, 0.7)
print("M2, t = 0.7")
print("confusion matrix, t = 0.7: ", cm)
print("Precision: ", Precision(cm))
print("Recall: ", TPR(cm))
print("F-measure: ", Fmeasure(cm))
