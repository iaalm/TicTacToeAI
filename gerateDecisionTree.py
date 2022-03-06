N=3
colors = [1, 0, -1]
def rotateBoard(board):
    return tuple(zip(*board[::-1]))

def flipBoard(board):
    return tuple(zip(*board))

def bestSolution(board, color):
    for i in range(2):
        for j in range(4):
            if board in bestSolution.resultCache:
                # TODO: rotate result too
                return bestSolution.resultCache[board]
            board = rotateBoard(board)
        board = flipBoard(board)
    res = bestSolutionWithoutCache(board, color)
    bestSolution.resultCache[board] = res
    return res

def bestSolutionWithoutCache(board, color):
    solution = {i:set() for i in colors}

    rboard = flipBoard(board)
    for ix, line in  enumerate(board):
        if sum(line) == color * 2:
            solution[color].add((ix, line.index(0)))
    for ix, line in enumerate(rboard):
        if sum(line) == color * 2:
            solution[color].add((line.index(0), ix))
    empty = -1
    for ix in range(N):
        v = board[ix][ix]
        if v == 0:
            if empty == -1:
                empty = ix
            else:
                break
        elif v != color:
            break
    else:
        solution[color].add((empty, empty))

    empty = -1
    for ix in range(N):
        v = board[ix][N-1-ix]
        if v == 0:
            if empty == -1:
                empty = ix
            else:
                break
        elif v != color:
            break
    else:
        solution[color].add((empty, N-1-empty))


    if len(solution[color]) > 0:
        return color, solution[color]

    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                # tuple copy and assign
                tboard = board[0:i] +\
                        (board[i][0:j] + (color,) + board[i][j+1:],)+\
                        board[i+1:]
                res, sol = bestSolution(tboard, -color)
                solution[res].add((i, j))
    for i in colors[::color]:
        if len(solution[i]) != 0:
            return i, solution[i]

    return 0, set()

bestSolution.resultCache = {}

def printBoard(result):
    # print(result)
    board = result[0]
    color = result[1][0]
    cand = result[1][1]
    candMarker = (color == 1) and "x" or "o"
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                print("X", end="")
            elif board[i][j] == -1:
                print("O", end="")
            elif (i, j) in cand:
                print(candMarker, end="")
            else:
                print("_", end="")
        print("")


if __name__ == "__main__":
    print(bestSolution(tuple(tuple(0 for i in range(N)) for j in range(N)), 1))
    print("resultCache", len(bestSolution.resultCache))
    for i in bestSolution.resultCache:
        r = bestSolution.resultCache[i]
        if r[0] != 0:
            print("============")
            printBoard((i, r))

