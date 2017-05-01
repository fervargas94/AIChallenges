import numpy as np
import copy
import sys
import time

DEPTH = 4

'''
    Check if there is an horizontal match
    board -> matrix
    player -> R or B 
    times -> number of times it will look for the player'''
def checkHorizontal(Fboard, Fplayer, Ftimes):
    total = 0
    for i in range(6):
        count = 0
        for j in range(7):
            if Fboard[i][j] == Fplayer:
                count += 1
                if count == Ftimes:
                    total += Ftimes
                    count -= 1
            else:
                count = 0
    return total

'''
    Check if there is a vertical match
    board -> matrix
    player -> R or B 
    times -> number of times it will look for the player
'''
def checkVertical(Fboard, Fplayer, Ftimes):
    count = 0
    for i in range(7):
        perColumn = 0
        for j in range(6):
            if Fboard[j][i] == Fplayer:
                perColumn += 1
            else:
                perColumn = 0
            if perColumn == Ftimes:
                perColumn = Ftimes - 1
                count += 1
    return count * Ftimes

'''
    Check if there is a diagonal match
    board -> matrix
    player -> R or B 
    times -> number of times it will look for the player
'''
def checkDiagonal(Fboard, Fplayer, Ftimes):
    count = 0
    #Get all diagonals
    Fboard = np.array(Fboard)
    diags = [Fboard[::-1,:].diagonal(i) for i in range(-Fboard.shape[0]+1,Fboard.shape[1])]
    diags.extend(Fboard.diagonal(i) for i in range(Fboard.shape[1]-1,-Fboard.shape[0],-1))
    for i in range(0, len(diags)):
        if len(diags[i]) >= Ftimes:
            perRow = 0
            for j in range(0, len(diags[i])):
                if diags[i][j] == Fplayer:
                    perRow += 1
                else:
                    perRow = 0
                if perRow == Ftimes:
                    perRow = 1
                    count += 1
    return count * Ftimes
                
''' Check if the position is already taken
    board -> matrix
    row, column -> int
'''
def emptySpace(Fboard, Frow, Fcolumn):
    return False if Fboard[Frow][Fcolumn] != 0 else True
    
''' Check if it is a valid Move
    board -> matrix 
    column -> int
'''
def validMove(Fboard, Fcolumn, Famount):
    if Fcolumn > 7 or Fcolumn < 1:
        print("Not a valid column, try a new one")
        return False
    row = Famount[Fcolumn - 1]
    if row < 0:
        print("There is no more space in that column, try a new one")
        return False
    if not emptySpace(Fboard, row, Fcolumn - 1):
        print("That space is already taken, try a new one")
        return False
    return True

''' Calculate value for each player
    to calculate heuristic
    @params board and player
'''
def getWin(Fboard): 
    global computer
    global human

    if (checkDiagonal(Fboard, human, 4) > 0 or checkHorizontal(Fboard, human, 4) > 0 or checkVertical(Fboard, human, 4) > 0):
        '''print("--------------")
        print(np.array(Fboard))
        print(checkVertical(Fboard, human, 4))
        print(checkDiagonal(Fboard, human, 4))
        print(checkHorizontal(Fboard, human, 4))
        print("--------------")'''
        return -100000000
    else:
        suma = ((checkDiagonal(Fboard, computer, 4) + checkVertical(Fboard, computer, 4) + checkHorizontal(Fboard, computer, 4)) * float("inf"))
        suma += ((checkDiagonal(Fboard, computer, 3) + checkVertical(Fboard, computer, 3) + checkHorizontal(Fboard, computer, 3)) * 1000)
        suma += (checkDiagonal(Fboard, computer, 2) + checkVertical(Fboard, computer, 2) + checkHorizontal(Fboard, computer, 2))
        #print("suma" , suma)
        return suma

    
def alphaBeta(Fboard, Fdepth, Fplayer, Fopponent, alpha, beta):
    global computer
    if Fdepth == 0:
        score = getWin(Fboard), None
        return score
    else:
        if Fplayer == computer:
            bestMove = None
            for i in range(7):
                if Fboard[0][i] == 0:
                    fakeBoard = fakeMove(Fboard, i, Fplayer)
                    if fakeBoard != False:
                        score, move = alphaBeta(fakeBoard, Fdepth - 1, Fopponent, Fplayer, alpha, beta)
                        if score > alpha:
                            alpha = score
                            bestMove = i
                            if alpha >= beta:
                                break
            return alpha, bestMove
        else:
            bestMove = None
            for i in range(7):
                if Fboard[0][i] == 0:
                    fakeBoard = fakeMove(Fboard, i, Fplayer)
                    if fakeBoard != False:
                        score, move = alphaBeta(fakeBoard, Fdepth - 1, Fopponent, Fplayer, alpha, beta)
                        if score < beta:
                            beta = score
                            bestMove = i
                            if alpha >= beta:
                                break
            return beta, bestMove
        

def fakeMove(Fboard, FColumn, Fplayer):
    fakeBoard = copy.deepcopy(Fboard)
    for j in range(5):
        if fakeBoard[j + 1][FColumn] != 0:
            fakeBoard[j][FColumn] = Fplayer
            break
        elif j == 4:
            fakeBoard[j + 1][FColumn] = Fplayer
    return fakeBoard

def minMax(Fboard, Fplayer, Fopponent):
    start = time.time()
    for i in range(7):
        if amount[i] >= 0:
            Fboard[amount[i]][i] = Fplayer
            win = checkWinner(Fboard, Fplayer)
            Fboard[amount[i]][i] = 0
            if win:
                return i + 1

    for i in range(7):
        if amount[i] >= 0:
            Fboard[amount[i]][i] = Fopponent
            win = checkWinner(Fboard, Fopponent)
            Fboard[amount[i]][i] = 0
            if win:
                return i + 1
            
    alpha = float("-inf")
    beta = float("inf")
    move = alphaBeta(Fboard, DEPTH, Fplayer, Fopponent, alpha, beta)
    return move[1] + 1


def checkWinner(Fboard, Fplayer):
    if checkDiagonal(Fboard, Fplayer, 4) > 0 or checkHorizontal(Fboard, Fplayer, 4) > 0 or checkVertical(Fboard, Fplayer, 4) > 0:
        return True
    return False

def printBoard(Fboard):
    for i in range(7):
        sys.stdout.write(" %d " % (i + 1))

    print ""
    print "_" * (21)
    for i in range(6):
        for j in range(7):

            if Fboard[i][j] == 1:
                sys.stdout.write("|O|")
            elif Fboard[i][j] == -1:
                sys.stdout.write("|X|")
            else:
                sys.stdout.write("|-|")

        print ""

    print "_" * (21)
    print ""

'''board = initializeBoard()
board, rounds = board[0], board[1]
checkHorizontal(board, "R", 4)
checkVertical(board, "R", 4)
checkDiagonal(board, "R", 4)'''
'''board = [[-1, -1, 0,  0, 0,  0, 0],
         [-1, 1, 0,  0, 0,  0, 0],
         [1,  -1, 0,  0, 0, 1, 0],
         [-1, -1, 0, 0, 1,  -1, 0],
         [1, 1, 0, 0, -1,  -1, 1],
         [1, -1, 0,  -1, 1, -1, -1]]
         
printBoard(board)    '''     
human = -1
computer = 1
board = [[0 for col in range(7)] for row in range(6)]
rounds = 0
lastOnes = []
turn = human
amount = [5, 5, 5, 5, 5, 5, 5]

#minMax(board, computer, human)
#amount = [3, 3, 1, 2, -1, -1, 1]

#bestMove = minMax(board, computer, human)

#print(maxValue(board, DEPTH, amount, turn, - 1))
#print(lastOnes, lastOnes.index(max(lastOnes)))
winner = 0
printBoard(board)
while rounds < 42:
    if turn == computer:
        print("Computer's turn")
    else: 
        print("Human's turn")
    
    if turn == human:
        valid = False
        while not valid:
            try:
                column = int(raw_input("Enter the column number: (1-7)"))
            except ValueError:
                print "Not valid! Try again."
                continue 
            if validMove(board, column, amount):
                row = amount[column - 1]
                board[row][column - 1] = turn
                amount[column - 1] -= 1
                valid = True
    else:
        bestMove = minMax(board, computer, human)
        if validMove(board, bestMove, amount):
            row = amount[bestMove - 1]
            board[row][bestMove - 1] = turn
            amount[bestMove - 1] -= 1
        lastOnes = []
    printBoard(board)
    if (checkDiagonal(board, turn, 4) > 0) or (checkHorizontal(board, turn, 4) > 0) or (checkVertical(board, turn, 4) > 0):
        if turn == computer:
            winner = "Computer"
        else: 
            winner = "Human"
        print("The winner is:  %s" % winner)
        break;
    if turn == human:
        turn = computer
    else:
        turn = human
    rounds += 1
if winner == 0:
    print("The game if tied")
