from random import randint
from time import sleep

# duplicate .join() for education purposes
def strfy(a: list[str]) -> str:
    res = ''
    for el in a:
        res += el
    return res

# convert symbol matrix to string
def strfy_matr(A:list[list[str]]) -> str:
    res = ''
    for row in A:
        res += pad(strfy(row)) + '\n'
    return res

# insert whitespaces between every symbol
def pad(s: str) -> str:
    res = ''
    for letter in s:
        res += letter + ' '
    return res

# prepare binary matrix for printing
def symbolize(A: list[list[int]], replace:dict[int, str]={0: '-', 1: '+'}) -> list[list[str]]:
    B:list[list[str]] = [[]] * len(A)
    for i in range(len(A)):
        B[i] = [''] * len(A[0])
        for j in range(len(A[0])):
            B[i][j] = replace[A[i][j]]
    return B

# generate default rect numeric matrix
def zeros(n: int, m:int=0) -> list[list[int]]:
    if m == 0:
        m = n
    c:list[list[int]] = [[]]*n
    for i in range(n):
        c[i] = [0]*m
    return c

# generate randomized binary rect matrix
def bin_matr(n: int, m:int=0)->list[list[int]]:
    if m == 0:
        m = n
    B = zeros(n, m)
    for i in range(n):
        for j in range(m):
            B[i][j] = randint(0,1)
    return B

# calculate neighbours for a given cell
def count_alive_neighbours(A: list[list[int]], i: int, j: int) -> int:
    res = 0
    for k in range ((i-1)%len(A), (i+2)%len(A)):
        for l in range((j-1)%len(A[0]), (j+2)%len(A[0])):
            if k != i or l != j:
                if A[k][l] == 1:
                    res += 1
    return res

# count alive cells
def population(A:list[list[int]]) -> int:
    pop = 0
    for row in A:
        for el in row:
            if el == 1:
                pop += 1
    return pop

# transition to the next state
def next_state(A: list[list[int]]) -> list[list[int]]:
    res = zeros(len(A), len(A[0]))
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 0 and count_alive_neighbours(A, i, j) == 3:
                res[i][j] = 1
            elif A[i][j] == 1 and (count_alive_neighbours(A, i, j) == 2 or count_alive_neighbours(A,i,j) == 3):
                res[i][j] = 1
    return res

# print binary matrix to console 
def printout(A:list[list[int]]):
    B = symbolize(A)
    for row in B:
        print(pad(strfy(row)))

# check binary matrices for equality
def equality(A: list[list[int]], B: list[list[int]]) -> bool:
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] != B[i][j]:
                return False
    return True

# try to find repeating states in array of states
def past_research(history: list[list[list[int]]], present: int) -> tuple[bool, int]:
    start = present-1
    for i in range(start, -1, -1):
        if equality(history[present], history[i]):
            return True, present - i
    return False, -1

# print array of states one by one
def watch(history: list[list[list[int]]], pause:float=0.1):
    i = 0
    while i < len(history) and history[i] != []:
        printout(history[i])
        print()
        sleep(pause)
        i += 1

# write run result
def elder_scrool(history:list[list[list[int]]], period:int, fname:str='nestor.txt'):
    delimiter = '==' * len(history[0]) + '\n'
    thescroll = 'This is a proud colony history. It all began like this:\n'
    thescroll += delimiter
    thescroll += strfy_matr(symbolize(history[0]))
    thescroll += delimiter
    thescroll += f'There were {population(history[0])} living beings.\n'
    thescroll += f'After {len(history)} generations '
    if period > 1:
        thescroll += f'the colony achieved a healthy,\nunevanescing oscillation with {period} different states.\n'
        thescroll += 'This is the cycle:\n'
        thescroll += delimiter
        for i in range(len(history)-period-1, len(history) - 1):
            thescroll += strfy_matr(symbolize(history[i]))
            thescroll += delimiter
    else:
        thescroll += 'the colony became set in stone.\n'
    thescroll += f'And this is how it ended with {population(history[len(history)-1])} creatures:\n'
    thescroll += delimiter
    thescroll += strfy_matr(symbolize(history[len(history)-1]))
    thescroll += delimiter
    with open(fname, 'w') as f:
        f.write(thescroll)

# conduct a test run
def run(max_states:int, size1:int=30, size2:int=30, rand:bool=True) -> tuple[list[list[list[int]]], int]:
    H:list[list[list[int]]]=[[]]*max_states
    if rand:
        H[0] = bin_matr(size1, size2)
    else:
        H[0] = zeros(size1, size2)
    i = 0
    period = -1
    rep = False
    while not rep and i < len(H) - 1:
        H[i+1] = next_state(H[i])
        i += 1
        rep, period = past_research(H, i)
    return H[:i+1], period

# check whether a state is static
def is_static_state(S: list[list[int]]) -> bool:
    Sn = next_state(S)
    if equality(Sn, S):
        return True
    return False

# TODO find all static states for given matrix size
def find_static_states(n:int, m:int):
    pass


if __name__ == "__main__":
    states, per = run(2000)
    watch(states)
    elder_scrool(states, per)