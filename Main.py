import PyQt5.QtWidgets as pq
import random
import sys


class CustomButton(pq.QPushButton):

    x_val = None
    y_val = None
    bombs_close_by = 0
    temp_bombs = None
    isBomb = None

    def __init__(self, x, y, window, isBomb):
        super().__init__('{}_{}'.format(x+1, y+1), window)

        self.x_val = x
        self.y_val = y
        self.isBomb = isBomb

        if self.isBomb:
            super().setText(("Bomb"))

        super().clicked.connect(self.clicked)
        self.move(x*40, y*40)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)
        self.setStyleSheet("border :2px solid black;")
        self.show()

    def clicked(self):
        super().setText('bitch')
        print('Bomb: {} X_Y: {}_{}'.format(self.isBomb, self.x_val, self.y_val))


class Window(pq.QMainWindow):

    buttons = []
    board_size = 9
    bombsOnBoard = 10

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dom and Steven\'s Minesweeper')
        self.setMinimumSize(self.board_size*40, self.board_size*40)
        self.show()

    def setBoard(self):

        temp_layer = []

        for y in range(self.board_size):
            for x in range(self.board_size):
                temp = CustomButton(x, y, self, False)
                temp_layer.append(temp)
            self.buttons.append(temp_layer)

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


def gerenateBoardString(board_size, num_bombs):
    temp_board = ''
    bombs = []

    for bomb in range(num_bombs):
        spot = random.randint(0, board_size**2 - 1)
        while spot in bombs:
            spot = random.randint(0, board_size ** 2 - 1)
        bombs.append(spot)

    for i in range(1, board_size**2+1):
        if i in bombs:
            temp_board += 'b'
        elif i not in bombs:
            temp_board += 'w'
        #if i % board_size == 0:
        #    temp_board += '/'

    return generateNumbers(list(temp_board),board_size,bombs)


def generateNumbers(board,board_size,bombs):


    temp_board = board
    print(bombs)
    coords = [-board_size-1, -board_size, -board_size+1, -1, 1, board_size-1, board_size, board_size+1]
    #First check for conditions where original rules don't apply
    for i in bombs:
        if i == 0:
            print("1",i)
            setHelper(board, i + coords[4])
            setHelper(board, i + coords[6])
            setHelper(board, i + coords[7])
        elif i < board_size:
            print("2",i)
            setHelper(board, i + coords[3])
            setHelper(board, i + coords[4])
            setHelper(board, i + coords[5])
            setHelper(board, i + coords[6])
            setHelper(board, i + coords[7])
        elif i == board_size:
            print("3",i)
            setHelper(board, i + coords[3])
            setHelper(board, i + coords[5])
            setHelper(board, i + coords[6])
        elif i == board_size * (board_size - 1):
            print("6",i)
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[2])
            setHelper(board, i + coords[4])
        elif i == board_size ** 2:
            print("7",i)
            setHelper(board, i + coords[0])
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[3])
        elif i > board_size * (board_size-1) and i < board_size**2:
            print("8",i)
            setHelper(board, i + coords[0])
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[2])
            setHelper(board, i + coords[3])
            setHelper(board, i + coords[4])
        elif i % board_size == 0:
            print("4",i)
            setHelper(board, i + coords[0])
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[3])
            setHelper(board, i + coords[5])
            setHelper(board, i + coords[6])
        elif i % board_size == 1:
            print("5",i)
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[2])
            setHelper(board, i + coords[4])
            setHelper(board, i + coords[6])
            setHelper(board, i + coords[7])
        else:
            print("9", i)
            setHelper(board, i + coords[0])
            setHelper(board, i + coords[1])
            setHelper(board, i + coords[2])
            setHelper(board, i + coords[3])
            setHelper(board, i + coords[4])
            setHelper(board, i + coords[5])
            setHelper(board, i + coords[6])
            setHelper(board, i + coords[7])

    return board

def setHelper(board,loc):
    if board[loc]  != 'w' and board[loc] != 'b':
        num = int(board[loc]) + 1
        board[loc] = num
    else:
        board[loc] = 1

if __name__ == '__main__':

    board = gerenateBoardString(10, 10)
    print(len(board))
    print(board[0:10])
    print(board[10:20])
    print(board[30:40])
    print(board[40:50])
    print(board[50:60])
    print(board[60:70])
    print(board[70:80])
    print(board[80:90])
    print(board[90:100])




    #app = pq.QApplication([sys.argv])
    #window = Window()
    #window.setBoard()
    #sys.exit(app.exec_())
