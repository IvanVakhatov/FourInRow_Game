import sys
import pygame
from pygame.locals import *

FPS = 15  # FPS - частота обновления экрана в игре
WINDOWWIDTH = 1100  # Ширина окна программы (в пикселях)
WINDOWHEIGHT = 900  # Высота окна программы (в пикселях)

BOARDWIDTH = 7  # Число игровых ячеек по вертикали
BOARDHEIGHT = 6  # Число игровых ячеек по горизонтали

ITEMSIZE = 100  # Размер фишек и игровых ячеек

# Выравнивание игрового поля относительно оси Х
X_ALIGNMENT = int((WINDOWWIDTH - BOARDWIDTH * ITEMSIZE) / 2)
# Выравнивание игрового поля относительно оси Y
Y_ALIGNMENT = int((WINDOWHEIGHT - BOARDHEIGHT * ITEMSIZE) / 2)

BGCOLOR = (159, 111, 66)  # Фон игрового поля - светло-коричневый
TEXTCOLOR = (255, 255, 255)  # Белый цвет
VOID = ' '
RED = 'red'
YELLOW = 'yellow'
USER = 'user'
BOT = 'bot'


def main():
    global FPSCLOCK, DISPLAYSURF, TOKENSOUND, USERWINSOUND
    global REDTOKENIMAGE, YELLOWTOKENIMAGE, BOARDIMAGE
    global USERWINIMAGE, BOTWINIMAGE
    global REDTOKENRECT, YELLOWTOKENRECT, WINRECT

    # Инициализация всех подключенных модулей библиотеки pygame
    pygame.init()
    # Создание объекта Clock (для контроля FPS)
    FPSCLOCK = pygame.time.Clock()
    # Инициализация окна
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Добавление подписи на игровом окне
    pygame.display.set_caption('Пиратские фишки')

    # Загрузка звука падения фишки
    TOKENSOUND = pygame.mixer.Sound("drop_sound.wav")
    # Загрузка звука выигрыша игрока
    USERWINSOUND = pygame.mixer.Sound("user_wins.wav")

    # Загрузка изображения красной фишки
    REDTOKENIMAGE = pygame.image.load('red_cell.png')
    # Загрузка изображения желтой фишки
    YELLOWTOKENIMAGE = pygame.image.load('yellow_cell.png')
    # Загрузка изображения ячейки игровой доски
    BOARDIMAGE = pygame.image.load('board.png')
    # Загрузка изображения выигрыша игрока
    USERWINIMAGE = pygame.image.load('user_win.png')
    # Трансформирование изображения под размер экрана
    USERWINIMAGE = pygame.transform.smoothscale(USERWINIMAGE,
                                               (WINDOWWIDTH, WINDOWHEIGHT))
     # Загрузка изображения выигрыша компьютера
    BOTWINIMAGE = pygame.image.load('bot_win.png')
    # Трансформирование изображения под размер экрана
    BOTWINIMAGE = pygame.transform.smoothscale(BOTWINIMAGE,
                                               (WINDOWWIDTH, WINDOWHEIGHT))

    # Координаты положения красной фишки
    REDTOKENRECT = pygame.Rect(ITEMSIZE // 2, WINDOWHEIGHT -
                               int(3 * ITEMSIZE / 2),
                               ITEMSIZE, ITEMSIZE)
    # Координаты положения желтой фишки
    YELLOWTOKENRECT = pygame.Rect(WINDOWWIDTH - (3 * ITEMSIZE // 2),
                                  WINDOWHEIGHT - (3 * ITEMSIZE // 2),
                                  ITEMSIZE, ITEMSIZE)
    # Координаты положения картинки выигрыша
    WINRECT = USERWINIMAGE.get_rect()
    WINRECT.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)

    #Для проверки, запушена первая игра или нет
    is_first_game = True
    while True:
        # Цикл запуска игры
        run_game(is_first_game)
        is_first_game = False


def run_game(is_first_game):
    ''' Запуск игры '''

    if is_first_game:
        # Пользователь делает первый ход при первом запуске игры
        turn = USER
    else:
        #Если игра после завершения запущена повторно, то
        # случайно выберем, кто ходит первым
        if 1 == 0:
            turn = BOT
        else:
            turn = USER

    # Создание массива для "игровой сетки" из ячеек
    main_board = get_new_board()

    while True:
        ''' Основной игровой цикл '''
        if turn == USER:
            # Пользователь делает ход
            get_user_move(main_board)
            if is_winner(main_board, RED):
                win_image = USERWINIMAGE
                win_sound = USERWINSOUND
                break
            turn = USER

    sound_flag = True
    while True:
        #Пока игрок не выйдет из игры (закрыв окно)

        # Прорисовка игрового поля
        draw_game_field(main_board)
        # Изображение выигрыша игрока или компьютера
        DISPLAYSURF.blit(win_image, WINRECT)
        if sound_flag is True:
            # Включение звука выигрыша игрока
            pygame.mixer.Sound.play(win_sound)
            pygame.mixer.music.stop()
            sound_flag = False
        # Обновление экрана
        pygame.display.update()
        # Установка значения частоты обновления экрана
        FPSCLOCK.tick(FPS)
        # Обработка событий (нажатий)
        for event in pygame.event.get():
            # Если нажата кнопка закрытия окна или клавиша "Escape"
            if event.type == QUIT or (event.type == KEYUP and
                                      event.key == K_ESCAPE):
                # Закрытие окна и завершение программы
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return


def get_new_board():
    ''' Создание массива ячеек игрового поля '''
    board = []
    for x in range(BOARDWIDTH):
        board.append([VOID] * BOARDHEIGHT)
    return board


def draw_game_field(board, extra_token=None):
    ''' Отображение игрового поля и фишек на экране '''

    # Заливка всего экрана цветом BGCOLOR
    DISPLAYSURF.fill(BGCOLOR)
    item_rect = pygame.Rect(0, 0, ITEMSIZE, ITEMSIZE)

    # Прорисовка уже "сыгранных" фишек на экране
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Изменение верхней левой координаты объекта item_rect
            item_rect.topleft = (X_ALIGNMENT + (x * ITEMSIZE),
                                 Y_ALIGNMENT + (y * ITEMSIZE))
            if board[x][y] == RED:
                DISPLAYSURF.blit(REDTOKENIMAGE, item_rect)
            elif board[x][y] == YELLOW:
                DISPLAYSURF.blit(YELLOWTOKENIMAGE, item_rect)

    if extra_token is not None:
        draw_extra_token(board, extra_token)

    # Прорисовка игрового поля на экране
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Изменение верхней левой координаты объекта item_rect
            item_rect.topleft = (X_ALIGNMENT + (x * ITEMSIZE),
                                 Y_ALIGNMENT + (y * ITEMSIZE))
            DISPLAYSURF.blit(BOARDIMAGE, item_rect)

    # Отображение спрайтов игровых фишек на экране (по бокам)
    DISPLAYSURF.blit(REDTOKENIMAGE, REDTOKENRECT)
    DISPLAYSURF.blit(YELLOWTOKENIMAGE, YELLOWTOKENRECT)


def draw_extra_token(board, extra_token):
    ''' Прорисовка пути новой фишки '''

    # Извлечение параметров фишки (координаты и цвет)
    x_cord = extra_token[0]
    y_cord = extra_token[1]
    color = extra_token[2]

    if color == RED:
        DISPLAYSURF.blit(REDTOKENIMAGE, (x_cord, y_cord, ITEMSIZE, ITEMSIZE))
    elif color == YELLOW:
        DISPLAYSURF.blit(YELLOWTOKENIMAGE, (x_cord, y_cord,
                                            ITEMSIZE, ITEMSIZE))


def get_user_move(board):
    move_token = False
    token_x, token_y = None, None
    while True:
        # Обработка событий (нажатий)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and
                  not move_token and REDTOKENRECT.collidepoint(event.pos)):
                # Начать перетаскивать красную фишку
                move_token = True
                # Получить ее координаты на поле
                token_x, token_y = event.pos
                print(token_x)

            # Если фишка движется по полю при помощи мышки
            elif event.type == MOUSEMOTION and move_token:
                # Обновить координаты перетаскиваемой красной фишки
                token_x, token_y = event.pos
                print(token_x)

            # Если красная фишка была отпущена
            # (левая кнопка мыши отпущена)
            elif (event.type == MOUSEBUTTONUP and event.button == 1 and
                  move_token):
                # Если фишка находится в пределах игровой доски
                if (token_x < WINDOWWIDTH - X_ALIGNMENT and
                        token_x > X_ALIGNMENT and token_y < Y_ALIGNMENT):
                    # Вычисление номера ячейки на игровой доске,
                    # Над которой находится фишка
                    column = int((token_x - X_ALIGNMENT) / ITEMSIZE)
                    #Если есть свободное место в колонке
                    if is_empty_space(board, column):
                        # Плавная прорисовка траектории падения фишки
                        animated_drop(board, column, RED)
                        # Занесение упавшей фишки в массив игрового поля
                        board[column][get_lowest_pos(board, column)] = RED
                        # Отображение только что упавшей фишки на
                        # uгровом поле (ход сделан)
                        draw_game_field(board)
                        pygame.display.update()
                        return

                token_x, token_y = None, None
                move_token = False

        if (token_x is not None) and (token_y is not None):
            draw_game_field(board, [token_x - int(ITEMSIZE / 2),
                            token_y - int(ITEMSIZE / 2), RED])
        else:
            draw_game_field(board)

        pygame.display.update()
        FPSCLOCK.tick()


def is_empty_space(board, column):
    # Возвращает True, если в столбце есть свободное место для фишки
    # Иначе - False.
    if column < 0 or column >= BOARDWIDTH or board[column][0] != VOID:
        # Если больше ширины доски или колонка заполнена
        return False
    return True


def animated_drop(board, column, color):
    ''' Плавная анимация траектории падения игровой фишки'''

    # Рассчет стартовой координаты Х (столбца на поле)
    x_cord = X_ALIGNMENT + column * ITEMSIZE
    # Начинать падение с верхней игровой ячейки
    y_cord = Y_ALIGNMENT - ITEMSIZE
    # Начальная скорость падения фишки
    speed_drop = 25
    # Параметр увеличения скорости
    speed_incr = 5
    # Рассчет конечной координаты Y (последней свободной ячейки в столбце)
    lowest_pos = get_lowest_pos(board, column) - 1

    pygame.mixer.Sound.play(TOKENSOUND)
    # Пока не достигнуто конечной свободной ячейки
    while ((y_cord - Y_ALIGNMENT) / ITEMSIZE) <= lowest_pos:
        y_cord += speed_drop
        speed_drop += speed_incr
        # Отображение падающей фишки на игровой доске
        draw_game_field(board, [x_cord, y_cord, RED])
        pygame.display.update()
        FPSCLOCK.tick()
    pygame.mixer.music.stop()


def get_lowest_pos(board, column):
    ''' Нахождение номера свободной ячейки на игровой доске'''

    # Начинаем проверять с конца списка ячеек в колонке
    for number in range(BOARDHEIGHT - 1, -1, -1):
        # Если найдена пустая ячейка в колонке, то возвращаем ее номер
        if board[column][number] == VOID:
            return number
    return -1


def is_board_full(board):
    ''' Возвращает True, если все ячейки на доске заполнены
        Иначе - возвращает False'''
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == VOID:
                return False
    return True


def is_winner(board, color):
    # Проверка горизонтальных "линий" на поле
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if ((board[x][y] == color) and
               (board[x+1][y] == color) and
               (board[x+2][y] == color) and
               (board[x+3][y] == color)):
                    return True
    # Проверка вертикальных "линий" на поле
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if ((board[x][y] == color) and
               (board[x][y+1] == color) and
               (board[x][y+2] == color) and
               (board[x][y+3] == color)):
                    return True
    # Проверка диагоналей на поле, наклоненных вправо
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if ((board[x][y] == color) and
               (board[x+1][y-1] == color) and
               (board[x+2][y-2] == color) and
               (board[x+3][y-3] == color)):
                    return True
    # Проверка диагоналей на поле, наклоненных влево
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if ((board[x][y] == color) and
               (board[x+1][y+1] == color) and
               (board[x+2][y+2] == color) and
               (board[x+3][y+3] == color)):
                    return True
    return False


if __name__ == '__main__':
    main()
