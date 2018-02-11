
# sorry for bad spelling in the comments
import random
# text effect codes
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'
# text color codes
CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
# wether irt randomly decides were to place a move when there is a tie in point
randomness = True
# wether a current game is running
gameOn = True
# the inex position of the last move placed by the bot (so that it can be underilned)
previousMoveX = 0
previousMoveY = 0
# A function that draws the tic atc toe board, and if guided is true then it will aslo show the placment guides
def displayBoard(array, guided=True):
    # gets them for global usage
    global previousMoveX,previousMoveY
    # shows the top of the board
    print(" _ _ _", end='', flush=True)
    if(guided):
        # and if its guided it also hsows the top of the board of  the guided map
        print("     _ _ _", end='')
    # goes to the next line
    print("")
    # will loop throught the inputed array and display the rest of the board, and the guide if specified
    for indexX, x in enumerate(array):
        # prints a horizantel wall
        print("|", end='')
        for indexY, y in enumerate(x):
            # if the tile countains a X
            if(y == "X"):
                # then it will print a blue, bold x
                print(CBLUE+CBOLD+'X'+CEND, end='')
            # if the tile countains a Y
            elif(y == "O"):
                # and the tile is the previous move
                if(indexX == previousMoveX and indexY == previousMoveY):
                # then it will print a red, underlined, bold, O
                  print(CRED+CURL+CBOLD+'O'+CEND, end='')
                else:
                # if its not the first move then it will just pring a bold, red, O
                  print(CRED+CBOLD+'O'+CEND, end='')
            else:
                # and if its not a O or an X (then its an empty space), then it will print a _
                print(y, end='')
            # then it will place a divider
            print("|", end='')
        # if it should be guided then it will print on of the rows of the guide
        if(guided):
            print("   |", end='')
            for y in guide[indexX]:
                print(y, end='')
                print("|", end='')
            print("")
        else:
            print("")
    #and then go to the next line once, just for good looks
    print("")
# the defensive cheker, this gives points to the tiles that will block X's          
def deffensiveCheck():
    # the winning trios are way down there, at the bottom of the code, Its a 3d array that stors the corrdiantes of all of the thigs to check, horizantel, diagnol, vertical...
    # loops througth eahc of the arrays of 3 points
    for y in winningTrios:
        # the amount of O's
        Ocount = 0
        # the amont of X's
        Xcount = 0
        # loops through al the points
        for x in y:
            # if the point is an X, it adds one to Xcount
            if(board[x[0]][x[1]] == "X"):
                Xcount+=1
            # if the point is an O it adds one to Ocount
            elif(board[x[0]][x[1]] == "O"):
                Ocount+=1
        # if there are more than 0 x's and no O's (If there is already an O than there is no need to block it because it is already blocked)
        if(Xcount != 0 and Ocount == 0):
            # loops through the points, again
            for x in y:
                # if there is nothing there then...
                if(board[x[0]][x[1]] != "X" and board[x[0]][x[1]] != "O"):
                    # if there is 2 X's, than add 50 because its urgent
                    if(Xcount == 2):
                        boardPoints[x[0]][x[1]]+=50
                    # and if there is onl one, than add just 1 point
                    else:
                        boardPoints[x[0]][x[1]]+=(Xcount)
# this checks to see were it can win, and adds point accoringly
def offensiveCheck():
    # same system as deffensive check, it counts Xs and Os...
    for y in winningTrios:
        Ocount = 0
        Xcount = 0
        for x in y:
            if(board[x[0]][x[1]] == "X"):
                Xcount+=1
            elif(board[x[0]][x[1]] == "O"):
                Ocount+=1
        # here it changes though, if there are no Xs (because then it pointles because its already been blocked, and there is no point in tring to win there)
        if(Xcount == 0):
            # loops through the points
            for x in y:
                # if the spot is empty
                if(board[x[0]][x[1]] == "_"):
                    # then if there are 2 already
                    if(Ocount == 2):
                        # then it adds 1000 because this is the best place to evre possibly place
                        boardPoints[x[0]][x[1]]+=1000
                    # if there is only 0 or 1 than it adds Ocount+0.5, so that even empty rows have at least a littiple bit of value, or else it would never tri to win them over.
                    else:
                        boardPoints[x[0]][x[1]]+=(Ocount+0.5)
# A funciton that gets the move from the player, and makes sure He is not tring to messe with the program
def getMove():
    # stores the inputed move (as a string)
    move = input("your turn: ")
    # sees if its a number, not text
    if(move.isdigit()):
        # converts it from string to integer
        move = int(move)
        # checks if it is in range
        if(move < 0 or move > 9):
            # if its not it askes for a number in range
            print(CRED+"please enter a valid move"+'\x1b[0m')
            move = getMove()
        if(move!=0):
            # if the inputed move has something already laces there, it asks to place somwere elese
            if(getValHuman(move) != "_"):
                print(CRED+"something is already placed there, please place again"+'\x1b[0m')
                move = getMove()
    # if it is not a number then it calls itself again, and asks for a number
    else:
        print(CRED+"please enter an integer"+'\x1b[0m')
        move = getMove()
    # returns the final move.
    return move
# gets the value of a tile, with a human input (so not cordinates but a number form 1-9)
def getValHuman(pos):
    pos = pos-1
    y = int(pos/3)
    x = pos%3
    return board[y][x]
# places the human move, takes a human input (so not cordinates but a number form 1-9)
def placeMove(pos):
    global gameOn
    # if its not O then it places the move
    if(pos!=0):
        pos = pos-1
        y = int(pos/3)
        x = pos%3
        board[y][x] = "X"
    else:
        # but if it is ) then it ends the current game (this is just a feature that I added so you can restart the game my enterig 0)
        gameOn = False
# this prints out the text to say who wins
def displayWinner(winner):
    global gameOn
    # if the winner is O
    if(winner == "O"):
        # then it prints that
        print(CVIOLET + 'Haha! I win you idiot!! [BOT > YOU]' + '\x1b[0m')
        # and turns of the teh current game
        gameOn = False
    # if the winner is X (but that will never happen cause my thing is impossible to beat!).......I think.
    if(winner == "X"):
        # then it prints that
        print(CGREEN + 'Good job, you won! (but I am going to beat you next time)' + '\x1b[0m')
         # and turns of the teh current game
        gameOn = False

    if(winner == "tie"):
         # then it prints that
        print(CYELLOW + 'Lucky you! it\'s a tie, at least you didn\'t loose.' + '\x1b[0m')
         # and turns of the  current game
        gameOn = False  
# checeks for the winner
def checkForWinner(): 
    global winningTrios
    # same system as defensiveCheck and Offensive check
    for y in winningTrios:
        Ocount = 0
        Xcount = 0
        for x in y:
            if(board[x[0]][x[1]] == "X"):
                Xcount+=1
            elif(board[x[0]][x[1]] == "O"):
                Ocount+=1
        if(Ocount == 3):
            return "O"
        elif(Xcount == 3):
            return "X"
    
    # if the thing above did not end the function than that means that means tehre is either a tie or the baord is not full yet
    emptyCount = 0
    # so it counts the number of empty tiles 
    for x in board:
        for y in x:
            if(y == "_"):
                emptyCount+=1
    # and if there are none then its a tie
    if(emptyCount == 0):
        return "tie"   
# function that places the bots move
def BotPlaceMove():
    global previousMoveX,previousMoveY
    # gets the max value coordinates of the baordpoitns array
    x,y = getMax2dArray(boardPoints)
    # updates previous move
    previousMoveX = y
    previousMoveY = x
    # places the move
    board[y][x] = "O"
# finds the maximum value in a 2d array, if thres a tie it randomly chooses (if randomness = True, all the way at the top of teh code)
def getMax2dArray(array):
    # index position of the chosen maximum value
    indexX = 0
    indexY = 0
    # the maximum value found yet
    max = 0
    # the amount of ties it has found, this is used to make a more even randomness
    tieCount = 1
    # loops through the inputed array
    for x in range(3):
        for y in range(3):
            # the value is equalt to max
            if(boardPoints[y][x] == max):
                # and we are supposed to use randomness
                if(randomness):
                # then we add ne to tie count
                    tieCount += 1
                    # randomly choose if we want to switch the index from the current one to this one
                    if(random.randint(1,tieCount) == tieCount):
                        indexX = x
                        indexY = y
                        max = boardPoints[y][x]
                # if randomness is not on then we swtitch it
                else:
                    indexX = x
                    indexY = y
                    max = boardPoints[y][x]
            # and if its greater than then we switch it
            elif boardPoints[y][x] > max:
                indexX = x
                indexY = y
                max = boardPoints[y][x]
    # then we return the coordinates
    return indexX,indexY
# THE ONE AND ONLY WAY TO BEAT IT IS SOLVED BY THIS EXCSEPTION
def exception():
    global previousMoveX, previousMoveY
    # these are the 2 scenarios were it can be beat
    exception1 = [
            ["X","_","_"],
            ["_","O","_"],
            ["_","_","X"]]
    exception2 = [
            ["_","_","X"],
            ["_","O","_"],
            ["X","_","_"]]
    # this finds if the scenarios are true, if the board is currently in one of these scenarios
    if(board == exception1 or board == exception2):
        # if it is then it will randomly place one of the correct moves that wont make it loose
        place = random.randint(0,4)
        if(place == 1):
            board[0][1] = "O"
            previousMoveX = 0
            previousMoveY = 1
        elif(place == 2):
            board[1][0] = "O"
            previousMoveX = 1
            previousMoveY = 0
        elif(place == 3):
            board[1][2] = "O"
            previousMoveX = 1
            previousMoveY = 2
        elif(place == 4):
            board[2][1] = "O"
            previousMoveX = 2
            previousMoveY = 1
        # and it will return true, to say that it ran and the bot does not need to run its normal routine, becasue it played for it
        return True 
    # and if it didnt play for it then it returns false
    return False
# this function actually runs the program
def gameLoop():
    # imports al the global variables it needs
    global gameOn
    global boardPoints
    global board
    # turns on the game
    gameOn = True
    # clears the board
    board = [
            ["_","_","_"],
            ["_","_","_"],
            ["_","_","_"]]
    # displays the first empty board
    displayBoard(board)
    # and loops the actual game until it is turned off.
    while(gameOn == True):
        # clears the board points
        boardPoints = [
            [0.0,0.0,0.0],
            [0.0,0.0,0.0],
            [0.0,0.0,0.0]]
        # gets and places the move from the player
        placeMove(getMove())
        # runs its checks
        offensiveCheck()
        deffensiveCheck()
        displayBoard(boardPoints, False)
        # checks if there is a winner (because the human already placed his move)
        displayWinner(checkForWinner())
        # if there is a winner then it ends the while loop, the game is over
        if(checkForWinner()!= None):
            break
        # if the exception ha snot fired, then it makes the bot place its move
        if(exception() == False):
            BotPlaceMove()
        # it displayes the board
        displayBoard(board)
        # and checks for a winner asecond time (bacause now the bo has placed his move)
        displayWinner(checkForWinner())
# the player guide
guide = [
    [1,2,3],
    [4,5,6],
    [7,8,9]]
# the winning trios as i was talking about
winningTrios = [
    [[0,0],[0,1],[0,2]],
    [[1,0],[1,1],[1,2]],
    [[2,0],[2,1],[2,2]],
    [[0,0],[1,0],[2,0]],
    [[0,1],[1,1],[2,1]],
    [[0,2],[1,2],[2,2]],
    [[0,0],[1,1],[2,2]],
    [[0,2],[1,1],[2,0]],
    ]

# prints isntructions on how to play teh game
print(CYELLOW + "To play, please enter the number on the board to the right to place a tile on the corresponding place in the board to the left" + '\x1b[0m')
# runs game loop forever so the games keep on coming
while True:
    gameLoop()
    # and lets make the last line sof code, with some nice text art.
    print(CBLUE+"╔═╦══════════╦═╗"+ '\x1b[0m')
    print(CBLUE+"║═╣ NEW GAME ╠═║"+ '\x1b[0m')
    print(CBLUE+"╚═╩══════════╩═╝"+ '\x1b[0m')

