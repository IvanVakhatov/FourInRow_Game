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


def main():
    global FPSCLOCK, DISPLAYSURF
    global REDTOKENIMAGE, YELLOWTOKENIMAGE, BOARDIMAGE

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

    #Для проверка, запушена первая игра или нет
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
        #Пока игрок не выйдет из игры (закрыв окно)

        # Прорисовка игрового поля
        draw_board(main_board)
        draw_tokens(main_board)
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
        board.append([] * BOARDHEIGHT)
        return board


def draw_board(board):
    ''' Отображение игрового поля на экране'''

    # Заливка всего экрана цветом BGCOLOR
    DISPLAYSURF.fill(BGCOLOR)
    item_rect = pygame.Rect(0, 0, ITEMSIZE, ITEMSIZE)
    # Прориосвка игрового поля на экране
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Изменение верхней левой координаты объекта item_rect
            item_rect.topleft = (X_ALIGNMENT + (x * ITEMSIZE),
                                 Y_ALIGNMENT + (y * ITEMSIZE))
            DISPLAYSURF.blit(BOARDIMAGE, item_rect)


def draw_tokens(board):
    ''' Отображение игровых фишек на экране '''

    # Вычисление координат положения для отображения красной фишки
    red_token_rect = pygame.Rect(ITEMSIZE // 2, WINDOWHEIGHT -
                                 int(3 * ITEMSIZE / 2),
                                 ITEMSIZE, ITEMSIZE)
    # Вычисление координат положения для отображения желтой фишки
    yellow_token_rect = pygame.Rect(WINDOWWIDTH - (3 * ITEMSIZE // 2),
                                    WINDOWHEIGHT - (3 * ITEMSIZE // 2),
                                    ITEMSIZE, ITEMSIZE)
    # Отображение фишек на экран
    DISPLAYSURF.blit(REDTOKENIMAGE, red_token_rect)
    DISPLAYSURF.blit(YELLOWTOKENIMAGE, yellow_token_rect)


if __name__ == '__main__':
    main()
