from random import randint
from time import sleep

def coin_toss() -> int:
    return randint(0,1)

def strfy(a: list) -> str:
    res = ''
    for el in a:
        res += str(el)
    return res

def pad(s: str, spacing=1) -> str:
    res = ''
    for letter in s:
        res += letter + ' '*spacing
    return res

def symbolize(A: list, replace={0: '.', 1: '*'}) -> list:
    B = zeros(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            B[i][j] = replace[A[i][j]]
    return B

def zeros(n: int):
    c = [None]*n
    for i in range(n):
        c[i] = [0]*n
    return c

def bin_matr(n: int)->list:
    B = zeros(n)
    for i in range(n):
        for j in range(n):
            B[i][j] = randint(0,1)
    return B

def count_alive_neighbours(A: list, i: int, j: int) -> int:
    res = 0
    for k in range (i-1, i+2):
        for l in range(j-1, j+2):
            if k == i and l == j:
                continue
            elif k < len(A) and l < len(A) and k >= 0 and l >= 0:
                if A[k][l] == 1:
                    res += 1
    return res

def alive_neighbours(A:list) -> list:
    res = zeros(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            res[i][j] = count_alive_neighbours(A, i, j)
    return res

def next_state(A: list) -> list:
    res = zeros(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] == 0 and count_alive_neighbours(A, i, j) == 3:
                res[i][j] = 1
            elif A[i][j] == 1 and (count_alive_neighbours(A, i, j) == 2 or count_alive_neighbours(A,i,j) == 3):
                res[i][j] = 1
    return res

def print_matr(A: list):
    for i in range(len(A)):
        print(A[i])

def print_alt(A:list):
    B = symbolize(A)
    for row in B:
        print(pad(strfy(row)))

def equality(A: list, B: list) -> bool:
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] != B[i][j]:
                return False
    return True

def past_research(history: list, present: int, depth=2) -> tuple[bool, int]:
    start = present-1
    if present - depth - 1 < -1:
        stop = -1
    else:
        stop = present - depth - 1
    for i in range(start, stop, -1):
        if equality(history[present], history[i]):
            return True, present - i
    return False, None

if __name__ == "__main__":
    print('Do you wish to configure an experiment? (default settings: fsize 30, watch mode, full history analysis)')
    interactive = input()

    if interactive == 'yes':
        print('Choose field size')
        size = int(input())
        print('Choose simulation mode\n1. Watch\n2. Analysis')
        kind = int(input())
        print('Choose history depth (d for full past analysis or integer)')
        historical = input()
    else:
        size = 30
        kind = 1
        historical = 'd'

    states = [None] * 2000
    states[0] = bin_matr(size)
    i = 0
    history_repeats_itself = False
    while not history_repeats_itself and i < 2000:
        states[i+1] = next_state(states[i])
        if kind == 1:
            print_alt(states[i])
            print()
            sleep(0.1)
        i += 1
        if historical == 'd':
            history_repeats_itself, cycle_length = past_research(states, i, depth = i)
        else:
            history_repeats_itself, cycle_length = past_research(states, i, depth = int(historical))

    print(f'Finish. Colony age is {i-1}')
    if history_repeats_itself and cycle_length > 1:
        type = f'colony is cyclic with period = {cycle_length}'
    elif history_repeats_itself:
        type = 'colony reached stationary state'
    else:
        type = 'colony died from old age'
    print(f'Stop condition: {type}')