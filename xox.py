import pygame
import math
from database import DataBase

# Oyun tahtası
board = [[0 for _ in range(3)] for _ in range(3)]

# İşaretler
PLAYER_X = -1
PLAYER_O = 1
EMPTY = 0

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Oyun alanı
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3

# Pygame başlatma
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("XOX Game")
clock = pygame.time.Clock()

# Oyun tahtasını çiz
def draw_board():
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

# X ve O çiz
def draw_X(x, y):
    pygame.draw.line(screen, RED, (x * CELL_SIZE + CELL_SIZE * 0.1, y * CELL_SIZE + CELL_SIZE * 0.1), 
                     (x * CELL_SIZE + CELL_SIZE * 0.9, y * CELL_SIZE + CELL_SIZE * 0.9), LINE_WIDTH)
    pygame.draw.line(screen, RED, (x * CELL_SIZE + CELL_SIZE * 0.1, y * CELL_SIZE + CELL_SIZE * 0.9), 
                     (x * CELL_SIZE + CELL_SIZE * 0.9, y * CELL_SIZE + CELL_SIZE * 0.1), LINE_WIDTH)

def draw_O(x, y):
    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3, LINE_WIDTH)

# Oyun tahtasını güncelle
def update_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] == PLAYER_X:
                draw_X(j, i)
            elif board[i][j] == PLAYER_O:
                draw_O(j, i)

# Oyun durumu kontrolü
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None

# Oyun alanı dolu mu?
def is_board_full():
    return all([cell != EMPTY for row in board for cell in row])

# En iyi hamleyi bulma
def find_best_move():
    best_score = -math.inf
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

# Minimax algoritması
def minimax(board, depth, is_maximizing_player):
    if check_winner():
        if check_winner() == PLAYER_O:
            return 1
        else:
            return -1
    elif is_board_full():
        return 0

    if is_maximizing_player:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score
    
    
db = DataBase()
# Oyun döngüsü
# Oyun döngüsü
def main():
    current_player = PLAYER_X  # İlk oyuncu X ile başlasın
    running = True
    player_x_move_made = False
    player_o_move_made = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_player == PLAYER_X:
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if event.type == pygame.MOUSEBUTTONDOWN and board[row][col] == EMPTY:
                board[row][col] = current_player
                print(f"{current_player}'s move: Row {row}, Column {col}")
                db.veriEkle(*[cell for row in board for cell in row])
                player_x_move_made = True
                current_player = PLAYER_O  # Sıradaki oyuncu O
        else:
            row, col = find_best_move()
            if board[row][col] == EMPTY:
                board[row][col] = current_player
                print(f"{current_player}'s move: Row {row}, Column {col}")
                db.veriEkle(*[cell for row in board for cell in row])
                player_o_move_made = True
                current_player = PLAYER_X  # Sıradaki oyuncu X

        # Her iki oyuncunun hamlesi yapıldıysa veya tüm tahta doluysa veritabanına kayıt yap
        if player_x_move_made and player_o_move_made or is_board_full():
            player_x_move_made = False
            player_o_move_made = False

        draw_board()
        update_board()
        pygame.display.flip()

        winner = check_winner()
        if winner:
            print(f"{winner} wins!")
            running = False
        elif is_board_full():
            print("It's a tie!")
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

