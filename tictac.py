import math

# Constants for the game
AI = 1
HUMAN = 2
SIDE = 3
AIMOVE = 'O'
HUMANMOVE = 'X'

# Function to initialise the game / Tic-Tac-Toe board
def initialise():
    board = [[' ' for _ in range(SIDE)] for _ in range(SIDE)]
    return board

# Function to print the Tic-Tac-Toe board
def showBoard(board):
    print("\n")
    print("\t {} | {} | {} ".format(board[0][0], board[0][1], board[0][2]))
    print("\t-----------")
    print("\t {} | {} | {} ".format(board[1][0], board[1][1], board[1][2]))
    print("\t-----------")
    print("\t {} | {} | {} \n".format(board[2][0], board[2][1], board[2][2]))

# Function to show the instructions
def showInstructions():
    print("\tTic-Tac-Toe\n")
    print("Choose a cell numbered from 1 to 9 as below:\n")
    print("\t 1 | 2 | 3 ")
    print("\t-----------")
    print("\t 4 | 5 | 6 ")
    print("\t-----------")
    print("\t 7 | 8 | 9 \n")

# Check if there are moves left
def isMovesLeft(board):
    for row in board:
        if ' ' in row:
            return True
    return False

# Evaluate the board
def evaluate(board):
    # Rows
    for row in range(SIDE):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == AIMOVE:
                return +10
            elif board[row][0] == HUMANMOVE:
                return -10
    # Columns
    for col in range(SIDE):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == AIMOVE:
                return +10
            elif board[0][col] == HUMANMOVE:
                return -10
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == AIMOVE:
            return +10
        elif board[0][0] == HUMANMOVE:
            return -10
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == AIMOVE:
            return +10
        elif board[0][2] == HUMANMOVE:
            return -10
    return 0

# Minimax function
def minimax(board, depth, isMax):
    score = evaluate(board)

    # If AI has won
    if score == 10:
        return score - depth  # prefer quicker win
    # If Human has won
    if score == -10:
        return score + depth  # prefer slower loss
    # If no moves left
    if not isMovesLeft(board):
        return 0

    if isMax:
        best = -math.inf
        for i in range(SIDE):
            for j in range(SIDE):
                if board[i][j] == ' ':
                    board[i][j] = AIMOVE
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(SIDE):
            for j in range(SIDE):
                if board[i][j] == ' ':
                    board[i][j] = HUMANMOVE
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = ' '
        return best

# Find the best move for AI
def findBestMove(board):
    bestVal = -math.inf
    bestMove = (-1, -1)

    for i in range(SIDE):
        for j in range(SIDE):
            if board[i][j] == ' ':
                board[i][j] = AIMOVE
                moveVal = minimax(board, 0, False)
                board[i][j] = ' '
                if moveVal > bestVal:
                    bestMove = (i, j)
                    bestVal = moveVal
    return bestMove

# Play Tic-Tac-Toe
def playTicTacToe():
    board = initialise()
    showInstructions()
    showBoard(board)

    while True:
        # Human turn
        humanMove = int(input("Enter your move (1-9): ")) - 1
        x, y = humanMove // SIDE, humanMove % SIDE
        if board[x][y] != ' ':
            print("Invalid move! Try again.")
            continue
        board[x][y] = HUMANMOVE
        showBoard(board)
        if evaluate(board) == -10:
            print("HUMAN wins!")
            break
        if not isMovesLeft(board):
            print("It's a draw!")
            break

        # AI turn
        print("AI is making a move...")
        move = findBestMove(board)
        board[move[0]][move[1]] = AIMOVE
        showBoard(board)
        if evaluate(board) == 10:
            print("AI wins!")
            break
        if not isMovesLeft(board):
            print("It's a draw!")
            break

# Driver function
if __name__ == "__main__":
    playTicTacToe()
