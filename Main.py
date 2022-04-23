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
        10 9 8
        1 0 1
        8 9 10
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
        spot = random.randint(0, board_size**2)
        while spot in bombs:
            spot = random.randint(0, board_size ** 2)
        bombs.append(spot)

    for i in range(1, board_size**2+1):
        if i in bombs:
            temp_board += 'b'
        elif i not in bombs:
            temp_board += 'w'
        if i % board_size == 0:
            temp_board += '/'
    return temp_board[:-1]


def generateNumbers(board):
    temp_board = board

    board_size = len(board.split('/'))
    coords = [-board_size-1, -board_size, -board_size+1, -1, 1, board_size-1, board_size, board_size+1]



    return temp_board


if __name__ == '__main__':

    board = gerenateBoardString(15, 10)
    print(board)
    for row in board.split('/'):
        print(row)
    generateNumbers(board)

    #app = pq.QApplication([sys.argv])
    #window = Window()
    #window.setBoard()
    #sys.exit(app.exec_())
