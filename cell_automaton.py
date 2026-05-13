from random import randint
from time import sleep

# duplicate .join() for education purposes
def strfy(a: list[str]) -> str:
    res = ''
    for el in a:
        res += el
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
        B[i] = [''] * len(A)
        for j in range(len(A)):
            B[i][j] = replace[A[i][j]]
    return B

# generate default square numeric matrix
def zeros(n: int) -> list[list[int]]:
    c:list[list[int]] = [[]]*n
    for i in range(n):
        c[i] = [0]*n
    return c

# generate randomized binary square matrix
def bin_matr(n: int)->list[list[int]]:
    B = zeros(n)
    for i in range(n):
        for j in range(n):
            B[i][j] = randint(0,1)
    return B

# calculate neighbours for a given cell
def count_alive_neighbours(A: list[list[int]], i: int, j: int) -> int:
    res = 0
    for k in range (i-1, i+2):
        for l in range(j-1, j+2):
            if k < len(A) and l < len(A) and k >= 0 and l >= 0 and (k != i or l != j):
                if A[k][l] == 1:
                    res += 1
    return res

# transition to the next state
def next_state(A: list[list[int]]) -> list[list[int]]:
    res = zeros(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
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
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] != B[i][j]:
                return False
    return True

# try to find repeating states in array of states
def past_research(history: list[list[list[int]]], present: int) -> tuple[bool, int]:
    start = present-1
    for i in range(start, -1, -1):
        if equality(history[present], history[i]):
            return True, present - i
    return False, 0

# print array of states one by one
def watch(history: list[list[list[int]]], pause:float=0.1):
    i = 0
    while i < len(history) and history[i] != []:
        printout(history[i])
        print()
        sleep(pause)
        i += 1

if __name__ == "__main__":
    print('Input field size or skip for default (30x30)')
    size = input()

    if size != '':
        size = int(size)
    else:
        size = 30

    # array of states till stop
    states:list[list[list[int]]] = [[]] * 2000
    # first state is random
    states[0] = bin_matr(size)
    i = 0
    # repeat flag
    history_repeats_itself = False
    # size of period
    cycle_length=-1
    # maximum 2000 states or until period encountered
    while not history_repeats_itself and i < 2000:
        states[i+1] = next_state(states[i])
        i += 1
        history_repeats_itself, cycle_length = past_research(states, i)

    print(f'Finish. Colony age is {i-1}')
    if history_repeats_itself and cycle_length > 1:
        type = f'colony is cyclic with period = {cycle_length}'
    elif history_repeats_itself:
        type = 'colony reached stationary state'
    else:
        type = 'colony died from old age'
    print(f'Stop condition: {type}')
    print('Do you wish to watch this?')
    watching = input()
    if watching[0] in {'y', 'Y'}:
        watch(states)