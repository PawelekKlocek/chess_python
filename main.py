import pygame
import string

pygame.init()

#parameters:
run = True
width = 800
height = 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
white = (255, 255, 255)
grey = (47,79,79)
black = (0, 0, 0)
selected_piece = None
board_pos = []
pieces = []
current_player = 'p1'

#position generation
for i in range(8):
    for n in range(8):
        board_pos.append((n, i))


#main chess piece class
class ChessPiece:
    def __init__(self, color, piece_type, board_pos):
        self.color = color
        self.piece_type = piece_type
        self.board_pos = board_pos

    def get_board_pos(self):
        return self.board_pos

    def get_color(self):
        if self.color == white:
            color = 'white'
        else:
            color = 'black'
        return color



#pawn class
class Pawn(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "pawn", board_pos)

    def draw(self):
        global pawn
        if self.color == white:
            pawn = pygame.image.load('images/white_pawn.png')
        if self.color == black:
            pawn = pygame.image.load('images/black_pawn.png')
        x, y = get_position(self.board_pos)
        window.blit(pawn, (x, y))

    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)
        if self.color == white:
            if clicked_area == (self.board_pos[0], self.board_pos[1] - 1) and check_free_position(x, y):
                self.board_pos = (self.board_pos[0], self.board_pos[1] - 1)
            elif clicked_area == (self.board_pos[0], self.board_pos[1] - 2) and check_free_position(x, y) and (self.board_pos[1] == 6):
                self.board_pos = (self.board_pos[0], self.board_pos[1] - 2)
            return True

        elif self.color == black:
            if clicked_area == (self.board_pos[0], self.board_pos[1] + 1) and check_free_position(x, y):
                self.board_pos = (self.board_pos[0], self.board_pos[1] + 1)
            elif clicked_area == (self.board_pos[0], self.board_pos[1] + 2) and check_free_position(x, y) and (self.board_pos[1] == 1):
                self.board_pos = (self.board_pos[0], self.board_pos[1] + 2)
            return True
        else:
            return False

    def capture(self, first_piece_pos, second_piece_pos, pieces):
        if self.color == white:
            if (first_piece_pos[0] + 1, first_piece_pos[1] - 1) == second_piece_pos:
                captured_piece = None
                for piece in pieces:
                    if piece.board_pos == second_piece_pos:
                        captured_piece = piece
                        break
                if captured_piece is not None:
                    pieces.remove(captured_piece)
                    self.board_pos = second_piece_pos
            elif (first_piece_pos[0] - 1, first_piece_pos[1] - 1) == second_piece_pos:
                captured_piece = None
                for piece in pieces:
                    if piece.board_pos == second_piece_pos:
                        captured_piece = piece
                        break
                if captured_piece is not None:
                    pieces.remove(captured_piece)
                    self.board_pos = second_piece_pos
        else:
            if (first_piece_pos[0] + 1, first_piece_pos[1] + 1) == second_piece_pos:
                captured_piece = None
                for piece in pieces:
                    if piece.board_pos == second_piece_pos:
                        captured_piece = piece
                        break
                if captured_piece is not None:
                    pieces.remove(captured_piece)
                    self.board_pos = second_piece_pos
            elif (first_piece_pos[0] - 1, first_piece_pos[1] + 1) == second_piece_pos:
                captured_piece = None
                for piece in pieces:
                    if piece.board_pos == second_piece_pos:
                        captured_piece = piece
                        break
                if captured_piece is not None:
                    pieces.remove(captured_piece)
                    self.board_pos = second_piece_pos

#rook class
class Rook(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "rook", board_pos)

    def draw(self):
        if self.color == white:
            rook = pygame.image.load('images/white_rook.png')
        else:
            rook = pygame.image.load('images/black_rook.png')
        x, y = get_position(self.board_pos)
        window.blit(rook, (x, y))

    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)
        for i in range(8):
            if clicked_area == (self.board_pos[0] + i, self.board_pos[1]) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1]) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0], self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0], self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

    def capture(self, first_piece_pos, second_piece_pos, pieces):
        for i in range(8):

            if (first_piece_pos[0], first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0], first_piece_pos[1] - i) == second_piece_pos :
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0] - i, first_piece_pos[1]) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0] + i, first_piece_pos[1]) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos

#bishop class
class Bishop(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "bishop", board_pos)

    def draw(self):
        if self.color == white:
            bishop = pygame.image.load('images/white_bishop.png')
        else:
            bishop = pygame.image.load('images/black_bishop.png')
        x, y = get_position(self.board_pos)
        window.blit(bishop, (x, y))


    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)
        for i in range(8):
            if clicked_area == (self.board_pos[0] + i, self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] + i, self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True


    def capture(self, first_piece_pos, second_piece_pos, pieces):
        for i in range(8):
            if (first_piece_pos[0] + i, first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0] - i, first_piece_pos[1] - i) == second_piece_pos :
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0] - i, first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
            elif (first_piece_pos[0] + i, first_piece_pos[1] - i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos

#king class
class King(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "king", board_pos)

    def draw(self):
        if self.color == white:
            king = pygame.image.load('images/white_king.png')
        else:
            king = pygame.image.load('images/black_king.png')
        x, y = get_position(self.board_pos)
        window.blit(king, (x, y))

    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)
        if clicked_area == (self.board_pos[0] + 1, self.board_pos[1] + 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0] - 1, self.board_pos[1] + 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0] - 1, self.board_pos[1] - 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0] + 1, self.board_pos[1] - 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0] + 1, self.board_pos[1]) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0] - 1, self.board_pos[1]) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0], self.board_pos[1] - 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

        elif clicked_area == (self.board_pos[0], self.board_pos[1] + 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True

    def capture(self, first_piece_pos, second_piece_pos, pieces):
        if (first_piece_pos[0] + 1, first_piece_pos[1] + 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 1, first_piece_pos[1] - 1) == second_piece_pos :
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 1, first_piece_pos[1] + 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] + 1, first_piece_pos[1] - 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] + 1, first_piece_pos[1]) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 1, first_piece_pos[1]) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos

        elif (first_piece_pos[0], first_piece_pos[1] + 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0], first_piece_pos[1] - 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos

#queen class
class Queen(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "queen", board_pos)

    def draw(self):
        if self.color == white:
            queen = pygame.image.load('images/white_queen.png')
        else:
            queen = pygame.image.load('images/black_queen.png')
        x, y = get_position(self.board_pos)
        window.blit(queen, (x, y))

    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)
        for i in range(8):
            if clicked_area == (self.board_pos[0] + i, self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] + i, self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] + i, self.board_pos[1]) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0] - i, self.board_pos[1]) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0], self.board_pos[1] - i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True

            elif clicked_area == (self.board_pos[0], self.board_pos[1] + i) and check_free_position(x, y):
                self.board_pos = clicked_area
                return True
    def capture(self, first_piece_pos, second_piece_pos, pieces):
        for i in range(8):
            if (first_piece_pos[0] + i, first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0] - i, first_piece_pos[1] - i) == second_piece_pos :
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0] - i, first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0] + i, first_piece_pos[1] - i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0] - i, first_piece_pos[1]) == second_piece_pos :
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0] + i, first_piece_pos[1]) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0], first_piece_pos[1] - i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

            elif (first_piece_pos[0], first_piece_pos[1] + i) == second_piece_pos:
                for piece in pieces:
                    if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                        pieces.remove(piece)
                        self.board_pos = second_piece_pos
                return True

#knight class
class Knight(ChessPiece):
    def __init__(self, color, board_pos):
        super().__init__(color, "knight", board_pos)

    def draw(self):
        if self.color == white:
            knight = pygame.image.load('images/white_knight.png')
        else:
            knight = pygame.image.load('images/black_knight.png')
        x, y = get_position(self.board_pos)
        window.blit(knight, (x, y))

    def move(self, x, y):
        global current_player
        clicked_area = get_area(x, y)

        if clicked_area == (self.board_pos[0] + 1, self.board_pos[1] - 2) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] - 1, self.board_pos[1] - 2) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] + 1, self.board_pos[1] + 2) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] - 1, self.board_pos[1] + 2) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] + 2, self.board_pos[1] - 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] - 2, self.board_pos[1] - 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] + 2, self.board_pos[1] + 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        elif clicked_area == (self.board_pos[0] - 2, self.board_pos[1] + 1) and check_free_position(x, y):
            self.board_pos = clicked_area
            return True
        else:
            return False

    def capture(self, first_piece_pos, second_piece_pos, pieces):
        if (first_piece_pos[0] + 1, first_piece_pos[1] + 2) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 1, first_piece_pos[1] - 2) == second_piece_pos :
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 1, first_piece_pos[1] + 2) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] + 1, first_piece_pos[1] - 2) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos

        elif (first_piece_pos[0] + 2, first_piece_pos[1] + 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 2, first_piece_pos[1] - 1) == second_piece_pos :
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] - 2, first_piece_pos[1] + 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos
        elif (first_piece_pos[0] + 2, first_piece_pos[1] - 1) == second_piece_pos:
            for piece in pieces:
                if piece.board_pos == second_piece_pos and piece != self and self.color != piece.color:
                    pieces.remove(piece)
                    self.board_pos = second_piece_pos



def get_position(board_pos):
    x, y = board_pos[0] * 100 + 10, board_pos[1] * 100 + 10
    return x, y


def draw_board(selected_piece):
    global board_pos
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(window, white, (row*100, col*100, 100, 100))
            else:
                pygame.draw.rect(window, grey, (row*100, col*100, 100, 100))
    for i in range(9):
        pygame.draw.line(window, black, (i * 100, 0), (i * 100, height))
        pygame.draw.line(window, black, (0, i * 100), (width, i * 100))
    font = pygame.font.Font(None, 36)

    for i, letter in enumerate(string.ascii_uppercase[:8]):
        text = font.render(letter, True, black)
        window.blit(text, (i * 100 + 70, 5))
    for i in range(8):
        text = font.render(str(i + 1), True, black)
        window.blit(text, (5, i * 100 + 70))
    if selected_piece is not None:
        selected_pos = selected_piece.get_board_pos()
        selected_x, selected_y = get_position(selected_pos)
        a, b = selected_pos
        if (a + b) % 2 == 0:
            pygame.draw.rect(window, white, (selected_x - 10, selected_y - 10, 100, 100))
            pygame.draw.rect(window, black, (selected_x - 10, selected_y - 10, 100, 100), 4)
        else:
            pygame.draw.rect(window, grey, (selected_x - 10, selected_y - 10, 100, 100))
            pygame.draw.rect(window, black, (selected_x - 10, selected_y - 10, 100, 100), 4)


def get_area(x, y):
    row = x // 100
    col = y // 100
    return (row, col)

#this function returns True if position is free and False if it isn't
def check_free_position(x, y):
    for piece in pieces:
        clicked_area = get_area(x, y)
        area = piece.get_board_pos()
        if area == clicked_area:
            return False
    return True


def game_loop():
    global run, selected_piece, pieces, turn
    last_clicked_pos = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    clicked_area = get_area(x, y)

                    if last_clicked_pos is None:
                        for piece in pieces:
                            if piece.get_board_pos() == clicked_area:
                                last_clicked_pos = clicked_area
                                selected_piece = piece
                                break
                    else:
                        if last_clicked_pos != clicked_area:
                            selected_piece.move(x, y)
                            selected_piece.capture(last_clicked_pos, clicked_area, pieces)
                            last_clicked_pos = None

        draw_board(selected_piece)

        for piece in pieces:
            piece.draw()

        pygame.display.update()

def setup(pieces):
    p1_w = Pawn(white, board_pos[48])
    p2_w = Pawn(white, board_pos[49])
    p3_w = Pawn(white, board_pos[50])
    p4_w = Pawn(white, board_pos[51])
    p5_w = Pawn(white, board_pos[52])
    p6_w = Pawn(white, board_pos[53])
    p7_w = Pawn(white, board_pos[54])
    p8_w = Pawn(white, board_pos[55])

    p1_b = Pawn(black, board_pos[8])
    p2_b = Pawn(black, board_pos[9])
    p3_b = Pawn(black, board_pos[10])
    p4_b = Pawn(black, board_pos[11])
    p5_b = Pawn(black, board_pos[12])
    p6_b = Pawn(black, board_pos[13])
    p7_b = Pawn(black, board_pos[14])
    p8_b = Pawn(black, board_pos[15])

    r1_b = Rook(black, board_pos[0])
    r2_b = Rook(black, board_pos[7])
    r1_w = Rook(white, board_pos[56])
    r2_w = Rook(white, board_pos[63])
    b1_b = Bishop(black, board_pos[2])
    b2_b = Bishop(black, board_pos[5])
    b1_w = Bishop(white, board_pos[61])
    b2_w = Bishop(white, board_pos[58])

    k1_w = King(white, board_pos[60])
    k1_b = King(black, board_pos[4])

    q1_w = Queen(white, board_pos[59])
    q1_b = Queen(black, board_pos[3])

    kn1_b = Knight(black, board_pos[1])
    kn2_b = Knight(black, board_pos[6])
    kn1_w = Knight(white, board_pos[62])
    kn2_w = Knight(white, board_pos[57])
    pawns = [p1_w, p2_w, p3_w, p4_w, p5_w, p6_w, p7_w, p8_w, p1_b, p2_b, p3_b, p4_b, p5_b, p6_b, p7_b, p8_b]
    rooks = [r1_b, r2_b, r1_w, r2_w]
    bishops = [b2_w, b1_w, b1_b, b2_b]
    knights = [kn1_w, kn1_b, kn2_w, kn2_b]
    kings = [k1_w, k1_b]
    queens = [q1_w, q1_b]

    for pawn in pawns:
        pieces.append(pawn)
    for rook in rooks:
        pieces.append(rook)
    for bishop in bishops:
        pieces.append(bishop)
    for king in kings:
        pieces.append(king)
    for queen in queens:
        pieces.append(queen)
    for knight in knights:
        pieces.append(knight)

if __name__ == '__main__':
    setup(pieces)
    game_loop()
