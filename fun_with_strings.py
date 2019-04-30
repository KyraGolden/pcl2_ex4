import sys
from typing import Iterable


def longest_substrings(x: str, y: str): #-> Iterable[str]:
    x = x.lower()
    y = y.lower()
    m = len(x)
    n = len(y)
    mystring = ''
    result = 0

    mat = [[0 for k in range(n+1)] for l in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if (i==0 or j ==0):
                mat[i][j] = 0
            elif (x[i-1] == y[j-1]):
                mat[i][j] = mat[i-1][j-1] + 1 #increases value by one if same string is found
                result = max(result, mat[i][j])
            else:
                mat[i][j] = 0
    for rows in mat:
        if max(rows) == result:
            end = mat.index(rows)

    temp = end-result
    mystring = mystring +x[temp:end] #hier müsste man noch die beiden bei Mozart und Mozarella herausfinden können... 

    if result == 0:
        return None
    else:
        return mystring

def main():
    var = input("enter string1")
    var1 = input("enter string2")
    print(longest_substrings(var,var1))


if __name__ == '__main__':
    main()