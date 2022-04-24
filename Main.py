import PyQt5.QtWidgets as pq
import random
import sys


class CustomButton(pq.QPushButton) :

    x_val = None
    y_val = None
    bombs_close_by = 0
    temp_bombs = None
    isBomb = None
    stateString = ''
    loc = None
    def __init__(self, x, y, window, isBomb,stateString):
        super().__init__('{}_{}'.format(x+1, y+1), window)

        self.x_val = x
        self.y_val = y
        self.neighbors = self.getNeighbors()
        self.isBomb = isBomb
        self.stateString = stateString
        super().clicked.connect(self.clicked)
        self.move(x*40, y*40)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)
        self.setStyleSheet("border :2px solid black;")
        self.show()

    def clicked(self):
        self.clickFunction(clicked = True, explored = [])
        print('Bomb: {} X_Y: {}_{}'.format(self.isBomb, self.x_val, self.y_val))

    #Recursion with Multipath Pruning
    def clickFunction(self,clicked,explored):
        stateString = self.stateString
        if stateString != 'b' and stateString != 'w':
            super().setText(self.stateString)
            return
        elif stateString == 'b':
            if clicked:
                # EndGame code here
                super().setText(self.stateString)
                window.endGame()
        else:
            super().setText(self.stateString)
            for neighbor in self.neighbors:
                #print(window.buttons[neighbor],explored)
                if neighbor not in explored:
                    explored.append(neighbor)
                    window.buttons[neighbor].clickFunction(clicked = False,explored = explored)
    #GetNeighbors function to find nearby blocks
    def getNeighbors(self):
        board_size = window.board_size
        i = (self.y_val * board_size + self.x_val)
        coords = [i + -board_size - 1, i + -board_size, i + -board_size + 1, i -1, i + 1, i + board_size - 1, i + board_size, i + board_size + 1]
        if i == 0:
            return [coords[4], coords[6], coords[7]]
        elif i < board_size - 1:
            return [coords[3], coords[4], coords[5],coords[6], coords[7]]
        elif i == board_size - 1:
            return [coords[3], coords[5], coords[6]]
        elif i == board_size * (board_size - 1):
            return[coords[1], coords[2], coords[4]]
        elif i == board_size * board_size - 1:
            return[coords[0], coords[1], coords[3]]
        elif i % board_size == 0:
            return [coords[1], coords[2], coords[4], coords[6], coords[7]]
        elif i % board_size == board_size-1:
            print("5", i)
            return [coords[0], coords[1], coords[3], coords[5], coords[6]]
        elif i > board_size * (board_size - 1) and i < board_size ** 2 - 1:
            print("8", i)
            return [coords[0], coords[1], coords[2], coords[3], coords[4]]
        else:
            return coords
class Window(pq.QMainWindow):

    buttons = []
    board_size = 10
    bombsOnBoard = 10

    def __init__(self):
        super().__init__()
        self.board = self.generateBoardString(self.board_size, self.bombsOnBoard)
        self.setWindowTitle('Dom and Steven\'s Minesweeper')
        self.setMinimumSize(self.board_size*40, self.board_size*40)
        self.show()

    def setBoard(self):
        temp_layer = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                state = (self.board[(y * self.board_size + x)])
                temp = CustomButton(x, y, self, False,stateString=state)
                #temp_layer.append(temp)
                self.buttons.append(temp)
    def resetBoard(self):
        self.board = self.generateBoardString(self.board_size,self.bombsOnBoard)
        self.printAnswerKey()
        for i in range(0,len(self.buttons)):
            self.buttons[i].setText("")
            self.buttons[i].stateString = self.board[i]
        #self.setBombs()
        #self.count3x3()

    def setBombs(self):

        available = self.buttons.copy()
        bombsLeft = self.bombsOnBoard

        for bomb in range(self.bombsOnBoard):
            index = int(random.uniform(0, len(available)*self.board_size))+1
            row = int(index / 9)
            column = int(index % 9)
            temp = available[row-1][column-1]
            temp.isBomb = True
            temp.setText('Bomb')
            available[row].remove(temp)
            bombsLeft -= 1

    def count3x3(self):

        """
        0 1 2
        3 0 4
        5 6 7
        """

        coords = [-10, -9, -8, -1, 1, 8, 9, 10]

        for square in self.buttons:
            if not square.isBomb:
                x = square.x_val
                y = square.y_val
                temp_count = 0
                temp_bombs = []

                index = self.buttons.index(square)
                for i in coords:
                    try:
                        if self.buttons[index+i].isBomb:
                            temp_count += 1
                            temp_bombs.append(i)
                    except:
                        continue
                square.bombs_close_by = temp_count
                square.temp_bombs = temp_bombs
                square.setText(str(temp_count))

    def endGame(self):
        print("You Suck")
        self.resetBoard()
    def generateBoardString(self,board_size, num_bombs):
        temp_board = ''
        bombs = []

        for bomb in range(num_bombs):
            spot = random.randint(0, board_size**2 - 1)
            while spot in bombs:
                spot = random.randint(0, board_size ** 2 - 1)
            bombs.append(spot)
        for i in range(0, board_size**2):
            if i in bombs:
                temp_board += 'b'
            elif i not in bombs:
                temp_board += 'w'
            #if i % board_size == 0:
            #    temp_board += '/'

        return self.generateNumbers(list(temp_board),board_size,bombs)


    def generateNumbers(self,board,board_size,bombs):
        """
                0 1 2
                3 0 4
                5 6 7
                """
        temp_board = board

        coords = [-board_size-1, -board_size, -board_size+1, -1, 1, board_size-1, board_size, board_size+1]
        print(coords)
        #First check for conditions where original rules don't apply
        for num in bombs:
            i = num
            if i == 0:
                print("1", i)
                self.setHelper(board, i, [coords[4], coords[6], coords[7]])
            elif i < board_size - 1:
                print("2", i)
                self.setHelper(board, i, [coords[3], coords[4], coords[5],coords[6], coords[7]])
            elif i == board_size - 1:
                print("3",i)
                self.setHelper(board, i, [coords[3], coords[5], coords[6]])
            elif i == board_size * (board_size - 1):
                print("4",i)
                self.setHelper(board, i, [coords[1], coords[2], coords[4]])
            elif i == board_size * board_size - 1:
                print("6",i)
                self.setHelper(board, i, [coords[0], coords[1], coords[3]])
            elif i % board_size == 0:
                self.setHelper(board, i, [coords[1], coords[2], coords[4], coords[6], coords[7]])
            elif i % board_size == board_size-1:
                print("5", i)
                self.setHelper(board, i, [coords[0], coords[1], coords[3], coords[5], coords[6]])
            elif i > board_size * (board_size - 1) and i < board_size ** 2 - 1:
                print("8", i)
                self.setHelper(board, i, [coords[0], coords[1], coords[2], coords[3], coords[4]])
            else:
                print("9", i)
                self.setHelper(board, i, coords)
        return board

    def setHelper(self,board,num,locs):
        for location in locs:
            loc = num + location
            if board[loc] == 'b':
                board[loc] = 'b'
            elif board[loc] != 'w':
                number = int(board[loc]) + 1
                board[loc] = str(number)
            else:
                board[loc] = '1'
    def printAnswerKey(self):
        for i in range(0, self.board_size):
            print(self.board[(self.board_size * i):(self.board_size * i + self.board_size)])
if __name__ == '__main__':
    """
    board_size = 10
    board = gerenateBoardString(board_size, 10)
    print(len(board))
    for i in range(0,board_size):
        print(board[(board_size * i):(board_size * i + board_size)])
    """
    app = pq.QApplication([sys.argv])
    window = Window()
    window.setBoard()
    window.printAnswerKey()
    sys.exit(app.exec_())
