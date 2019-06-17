
from ete3 import Tree

def UPGMA(matrix, labels):
    order=[]
    labels=list(labels)
    while len(labels) > 1:
        #print(labels)
        max_c = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > max_c:
                    max_c = matrix[i][j]
                    a, b = i, j
        if b < a:
            a, b = b, a

        row = []  
        for i in range(0, a):
            row.append((matrix[a][i] + matrix[b][i])/2)
        matrix[a] = row
        
        for i in range(a+1, b):
            matrix[i][a] = (matrix[i][a]+matrix[b][i])/2

        for i in range(b+1, len(matrix)):
            matrix[i][a] = (matrix[i][a]+matrix[i][b])/2
            del matrix[i][b]
        del matrix[b]

        labels[a] = "(" + labels[a] + "," + labels[b] + ")"
        order.append(labels[a])
        del labels[b]

        
    return labels[0],order

def alpha_labels(start, end):
    labels = []
    for i in range(ord(start), ord(end)+1):
        labels.append(str(i))
    return labels

def main():
    M_labels = alpha_labels("A", "G")   #A through G
    M = [
        [],                         #A
        [19],                       #B
        [27, 31],                   #C
        [8, 18, 26],                #D
        [33, 36, 41, 31],           #E
        [18, 1, 32, 17, 35],        #F
        [13, 13, 29, 14, 28, 12]    #G
    ]
    tree_1=UPGMA(M, M_labels)
    print(tree_1+';')

#main()