import sys
import pygame
from pygame.locals import *


FPS = 30  # FPS - частота обонвления экрана в игре
WINDOWWIDTH = 1100  # Ширина окна программы (в пикселях)
WINDOWHEIGHT = 900  # Высота окна программы (в пикселях)

BOARDWIDTH = 7  # Число игровых ячеек по вертикали
BOARDHEIGHT = 6  # Число игровых ячеек по горизонтали

DIFFICULTY = 2  # "Уровень сложности" бота (1 или 2)
ITEMSIZE = 100  # Размер фишек и игровых ячеек

# Выравнивание игрового поля относительно оси Х
X_ALIGNMENT = int((WINDOWWIDTH - BOARDWIDTH * ITEMSIZE) / 2)
# Выравнивание игрового поля относительно оси Y
Y_ALIGNMENT = int((WINDOWHEIGHT - BOARDHEIGHT * ITEMSIZE) / 2)

BGCOLOR = (159, 111, 66)  # Фон игровго поля - светло-коричневый
TEXTCOLOR = (255, 255, 255)  # Белый цвет
VOID = ' '
RED = 'red'
YELLOW = 'yellow'


def main():
    global FPSCLOCK, DISPLAYSURF
    global REDTOKENIMAGE, YELLOWTOKENIMAGE, BOARDIMAGE
    global REDTOKENRECT, YELLOWTOKENRECT

    # Инициализация всех подключенных модулей библиотеки pygame
    pygame.init()
    # Создание объекта Clock (для контроля FPS)
    FPSCLOCK = pygame.time.Clock()
    # Инициализция окна
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Четыре в ряд')

    # Загрузка изображения красной фишки
    REDTOKENIMAGE = pygame.image.load('red_cell.png')
    # Загрузка изображения желтой фишки
    YELLOWTOKENIMAGE = pygame.image.load('yellow_cell.png')
    # Загрузка изображения ячейки игровой доски
    BOARDIMAGE = pygame.image.load('board.png')
    # Координаты положения красной фишки
    REDTOKENRECT = pygame.Rect(ITEMSIZE // 2, WINDOWHEIGHT -
                               int(3 * ITEMSIZE / 2),
                               ITEMSIZE, ITEMSIZE)
    # Координаты положения желтой фишки
    YELLOWTOKENRECT = pygame.Rect(WINDOWWIDTH - (3 * ITEMSIZE // 2),
                                  WINDOWHEIGHT - (3 * ITEMSIZE // 2),
                                  ITEMSIZE, ITEMSIZE)

    #Для проверки, запушена первая игра или нет
    is_first_game = True
    while True:
        # Основной игровой цикл
        run_game(is_first_game)
        is_first_game = False


def run_game(is_first_game):
    ''' Запуск игры '''

    # Создание массива для "игровой сетки" из ячеек
    main_board = get_new_board()

    while True:
        ''' Основной игровой цикл '''
        get_user_move(main_board)
        break

    while True:
        #Пока игрок не выйдет из игры (закрыв окно)

        # Прорисовка игрового поля
        draw_game_field(main_board)
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

    if extra_token is not None:
        draw_extra_token(board, extra_token)

    # Прориосвка игрового поля на экране
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Изменение верхней левой координаты объекта item_rect
            item_rect.topleft = (X_ALIGNMENT + (x * ITEMSIZE),
                                 Y_ALIGNMENT + (y * ITEMSIZE))
            DISPLAYSURF.blit(BOARDIMAGE, item_rect)

    # Отображение фишек на экран
    DISPLAYSURF.blit(REDTOKENIMAGE, REDTOKENRECT)
    DISPLAYSURF.blit(YELLOWTOKENIMAGE, YELLOWTOKENRECT)


def draw_extra_token(board, extra_token):
    ''' Прорисовка пути новой фишки '''
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

            #Если фишка дивижется по полю при помощи мышки
            elif event.type == MOUSEMOTION and move_token:
                # Обновить координаты перетаскиваемой красной фишки
                token_x, token_y = event.pos
                print(token_x)

            # Если красная фишка была отпушена
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
        FPSCLOCK.tick(FPS)


def is_empty_space(board, column):
    # Возвращает True, если в столбце есть свободное место для фишки
    # Иначе - False.
    if column < 0 or column >= BOARDWIDTH or board[column][0] != VOID:
        # Если больше ширины доски или колонка заполнена
        return False
    return True


if __name__ == '__main__':
    main()
