import multiprocess as mp
import numpy as np
import time
from itertools import product
from multiprocessing import Process
import multiprocessing as mp2
from multiprocessing import Value, Array


seq1 = "ASAYTUYDSD"
seq2 = "ATPPREY"
gap = -1
match = 5
mismatch = -10
global A

def gapPenaltyline(x):
    if x<len(seq1)+1:
            return gap* x
    else:
            return  gap*(x-len(seq1))


def scoring_multiprocess(i,j):
    up=A[i-1,j]+gap
    left=A[i,j-1]+gap
    if seq1[j-1]==seq2[i-1]:
        dia = A[i - 1, j - 1]+match
    else:
        dia = A[i - 1, j - 1] +mismatch
    #print(dia)
    return max(up,left,dia)

def scoring_serial(i,j):
    up=A[i-1,j]+gap
    left=A[i,j-1]+gap
    if seq1[j-1]==seq2[i-1]:
        dia = A[i - 1, j - 1]+match
    else:
        dia = A[i - 1, j - 1] +mismatch
    list=[up,left,dia]
    maxn=max(list)
    maxposition=list.index(maxn)
    return maxposition

def mprocessph1():
    processes=[]
    global A
    global results
    pool = mp.Pool(processes=len(seq1)+len(seq2))
    results = [pool.apply(gapPenaltyline, args=(x,)) for x in range(1, len(seq1)+len(seq2)+1)]
    #print(len(results))
    #print(results)
    #print(len(seq1))
    for i in range (1,len(results)+1):
        if i<len(seq1)+1:
            A[0,i]=results[i-1]
            #print(i)
        else:
            A[i-len(seq1),0]=results[i-1]

def mprocessph2():
    global A
    #toShare = Array(A, len(A), lock=False)
    minseq=min(len(seq1),len(seq2))
    for i in range(1,len(seq1)+len(seq2)+1):
            #a = np.memmap('A', dtype='float32', mode='w+', shape=(100000, 1000))
            if (i<=minseq):
                with mp2.Pool(processes=i) as pool:
                    iterlist=list(range(1,i))
                    iterproduct=product(iterlist,repeat=2)
                    iterproduct=[x for x in iterproduct if x[0]+x[1]==i]
                    results = pool.starmap(scoring_multiprocess,iterproduct)
                    #print(results)
                    count=0
                    for x in iterproduct:
                        A[x[0],x[1]]=results[count]
                        count=count+1
            else:
                with mp2.Pool(processes=len(seq1)+len(seq2)+1-i) as pool:
                    iterlist=list(range(1,i))
                    #print(iterlist)
                    iterproduct=product(iterlist,repeat=2)
                    iterproduct=[x for x in iterproduct if x[0]+x[1]==i]
                    iterproduct=[x for x in iterproduct if x[1]<=len(seq1)]
                    iterproduct = [x for x in iterproduct if x[0] <= len(seq2)]
                    print(iterproduct)
                    results = pool.starmap(scoring_multiprocess,iterproduct)
                    #print(results)
                    count=0
                    for x in iterproduct:
                        A[x[0],x[1]]=results[count]
                        count=count+1
                    #print(A)

#
# 0 is for up 1 is for left 2 is for diagonal move
def traceback():
    j=len(seq1)-1
    i=len(seq2)-1
    score=[]
    move=[]
    while i>=0 and j>=0:
        print(i,j)
        score.append(A[i, j])
        if seq1[j]==seq2[i]:
            i=i-1
            j=j-1
            move.append(2)
        else:
            position=scoring_serial(i,j)
            move.append(position)
            if position==0:
                i=i-1
            elif position==1:
                j=j-1
            else:
                i=i-1
                j=j-1

    return move , score


if __name__ == '__main__':
    global A
    A = np.zeros((len(seq2) + 1, len(seq1) + 1))
    mprocessph1()
    mprocessph2()
    print("Max Number of processes : " + str (len(seq1)+ len(seq2)) )
    print("Scoring Matrix")
    print(A)
    move,score = traceback()
    print(move)
    list.reverse(move)
    print(move)
    movestring=[]
    for pos in move:
        if pos==0:
            movestring.append("Up")
        if pos==1:
            movestring.append("Left")
        else:
            movestring.append("Diagonal")
    print(movestring)