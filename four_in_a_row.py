import sys
import random
import copy
import pygame
from pygame.locals import *

FPS = 15  # FPS - частота обновления экрана в игре
WINDOWWIDTH = 1100  # Ширина окна программы (в пикселях)
WINDOWHEIGHT = 900  # Высота окна программы (в пикселях)

BOARDWIDTH = 7  # Число игровых ячеек по вертикали
BOARDHEIGHT = 6  # Число игровых ячеек по горизонтали

ITEMSIZE = 100  # Размер фишек и игровых ячеек

# Выравнивание игрового поля относительно оси Х
X_ALIGNMENT = (WINDOWWIDTH - BOARDWIDTH * ITEMSIZE) // 2
# Выравнивание игрового поля относительно оси Y
Y_ALIGNMENT = (WINDOWHEIGHT - BOARDHEIGHT * ITEMSIZE) // 2

BGCOLOR = (159, 111, 66)  # Фон игрового поля - светло-коричневый
TEXTCOLOR = (255, 255, 255)  # Белый цвет

# Объявление основных игровых констант
VOID = ' '
RED = 'red'
YELLOW = 'yellow'
USER = 'user'
BOT = 'bot'


def main():
    # Объявление глобальных переменных
    global FPSCLOCK, DISPLAYSURF
    global BGSOUND, TOKENSOUND, USERWINSOUND, USERLOSESOUND, DRAWNGAMESOUND
    global REDTOKENIMAGE, YELLOWTOKENIMAGE, BOARDIMAGE
    global USERWINIMAGE, BOTWINIMAGE, DRAWNGAMEIMAGE
    global REDTOKENRECT, YELLOWTOKENRECT, WINRECT

    # Инициализация всех подключенных модулей библиотеки pygame
    pygame.init()
    # Создание объекта Clock (для контроля FPS)
    FPSCLOCK = pygame.time.Clock()
    # Инициализация окна
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # Добавление подписи на игровом окне
    pygame.display.set_caption('Пиратские фишки')

    # Зарузка звука фоновой музыки
    BGSOUND = pygame.mixer.music.load('background_sound.wav')
    # Установка уровная громкости фоновой музыки
    pygame.mixer.music.set_volume(0.5)
    # Загрузка звука падения фишки
    TOKENSOUND = pygame.mixer.Sound("drop.wav")
    # Загрузка звука выигрыша игрока
    USERWINSOUND = pygame.mixer.Sound("user_win.wav")
    # Загрузка звука проигрыша игрока
    USERLOSESOUND = pygame.mixer.Sound("user_lose.wav")
    # Загрузка звука ничьи
    DRAWNGAMESOUND = pygame.mixer.Sound("drawn_game.wav")

    # Загрузка изображения красной фишки
    REDTOKENIMAGE = pygame.image.load('red_token.png')
    # Загрузка изображения желтой фишки
    YELLOWTOKENIMAGE = pygame.image.load('yellow_token.png')
    # Загрузка изображения ячейки игровой доски
    BOARDIMAGE = pygame.image.load('board.png')
    # Загрузка изображения выигрыша игрока
    USERWINIMAGE = pygame.image.load('user_win.png')
    # Трансформирование изображения под размер экрана
    USERWINIMAGE = pygame.transform.smoothscale(USERWINIMAGE,
                                               (WINDOWWIDTH, WINDOWHEIGHT))
    # Загрузка изображения выигрыша бота
    BOTWINIMAGE = pygame.image.load('bot_win.png')
    # Трансформирование изображения под размер экрана
    BOTWINIMAGE = pygame.transform.smoothscale(BOTWINIMAGE,
                                               (WINDOWWIDTH, WINDOWHEIGHT))
    # Загрузка изображения ничьи
    DRAWNGAMEIMAGE = pygame.image.load('drawn_game.png')
    # Трансформирование изображения под размер экрана
    DRAWNGAMEIMAGE = pygame.transform.smoothscale(BOTWINIMAGE,
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

    # Для проверки, игра запущена в первый раз или нет
    is_first_game = True
    while True:
        # Включение фоновой музыки
        pygame.mixer.music.play(loops=-1)
        # Запуск игры
        run_game(is_first_game)
        is_first_game = False


def run_game(is_first_game):
    ''' Запуск игры '''

    if is_first_game:
        # Бот делает первый ход при первом запуске игры
        turn = BOT
    else:
        # Если игра после первого раунда запущена повторно, то
        # случайно выберем, кто ходит первым в новом раунде
        if random.randint(0, 1) == 1:
            turn = USER
        else:
            turn = BOT

    # Создание массива для "игровой сетки" из ячеек
    main_board = get_new_board()

    while True:
        ''' Основной игровой цикл '''
        if turn == USER:
            ''' Если ход делает игрок '''
            get_user_move(main_board)
            # Если при проверке оказалось, что игрок выиграл
            if is_winner(main_board, RED):
                # Выбираем соответствующие изображение и звук победы
                win_image = USERWINIMAGE
                win_sound = USERWINSOUND
                # Прерываем игровой цикл
                break
            # Иначе - ход переходит боту
            turn = BOT
        else:
            ''' Если ход делает бот '''
            # Определяем номер колонки, который боту следует выбрать
            column = get_bot_move(main_board)
            # Анимация хода бота
            animated_bot_drop(main_board, column)
            # Вносим изменения в основной массив игрового поля
            make_move(main_board, YELLOW, column)
            # Если при проверке оказалось, что бот выиграл
            if is_winner(main_board, YELLOW):
                # Выбираем соответствующие изображение и звук победы
                win_image = BOTWINIMAGE
                win_sound = USERLOSESOUND
                # Прерываем игровой цикл
                break
            # Иначе - ход переходит игроку
            turn = USER

        # Если при проверке выяснилось, что поле полностью заполнено
        if is_board_full(main_board):
            # Выбираем соответствующие изображение и звук ничьи
            win_image = DRAWNGAMEIMAGE
            win_sound = DRAWNGAMESOUND
            # Прерываем игровой цикл
            break

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
            # Если аттрибут цвета в массиве - красный
            if board[x][y] == RED:
                # Отображаем красную фишку на поле
                DISPLAYSURF.blit(REDTOKENIMAGE, item_rect)
            # Если аттрибут цвета в массиве - желтый
            elif board[x][y] == YELLOW:
                # Отображаем желтую фишку на поле
                DISPLAYSURF.blit(YELLOWTOKENIMAGE, item_rect)

    # Для движущихся (временных) фишек
    if extra_token is not None:
        draw_extra_token(board, extra_token)

    # Прорисовка игрового поля на экране
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # Изменение верхней левой координаты объекта item_rect
            item_rect.topleft = (X_ALIGNMENT + (x * ITEMSIZE),
                                 Y_ALIGNMENT + (y * ITEMSIZE))
            # Отображаем спрайт игровой ячейки на экране
            DISPLAYSURF.blit(BOARDIMAGE, item_rect)

    # Отображение спрайтов игровых фишек на экране (по бокам)
    DISPLAYSURF.blit(REDTOKENIMAGE, REDTOKENRECT)
    DISPLAYSURF.blit(YELLOWTOKENIMAGE, YELLOWTOKENRECT)


def draw_extra_token(board, extra_token):
    ''' Прорисовка пути новых движущихся фишки '''

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
    ''' Отображение траектории движения фишки игрока и
        перемещение ее на нужное место на игровой доске '''
    # Логическая переменная движения фишки
    move_token = False
    # Хранение x, y координат фишки
    token_x, token_y = None, None
    while True:
        # Обработка событий (нажатий)
        for event in pygame.event.get():
            # Если нажат "крестик" на окне pygame
            if event.type == QUIT:
                # Закрыть окно pygame и завершить программу
                pygame.quit()
                sys.exit()

            # Если нажата левая кнопка мыши и курсор "находится" внутри
            # области красной фишки
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and
                  not move_token and REDTOKENRECT.collidepoint(event.pos)):
                # Позволить перетаскивать красную фишку
                move_token = True
                # Получить начальные координаты красной на поле
                token_x, token_y = event.pos

            # Если фишка движется по полю при помощи мышки
            elif event.type == MOUSEMOTION and move_token:
                # Обновить координаты перетаскиваемой красной фишки
                token_x, token_y = event.pos

            # Если красная фишка была отпущена
            # (левая кнопка мыши отпущена)
            elif (event.type == MOUSEBUTTONUP and event.button == 1 and
                  move_token):
                # Если фишка находится в пределах игровой доски
                if (token_x < WINDOWWIDTH - X_ALIGNMENT and
                        token_x > X_ALIGNMENT and token_y < Y_ALIGNMENT):
                    # Вычисление номера колонки на игровой доске,
                    # над которой сверху находится фишка
                    column = int((token_x - X_ALIGNMENT) / ITEMSIZE)
                    #Если есть свободное место в текущей колонке
                    if is_empty_space(board, column):
                        # Плавная прорисовка траектории падения фишки
                        animated_drop(board, column, RED)
                        # Занесение упавшей фишки в массив игрового поля
                        make_move(board, RED, column)
                        # Отображение только что упавшей фишки на
                        # uгровом поле (ход сделан)
                        draw_game_field(board)
                        pygame.display.update()
                        # Выходим из функции досрочно
                        return

                # Если пользователь отпустил красную фишку за пределами
                # игровой доски - сбросим текущие координаты фишки
                # и "вернем ее на место""
                token_x, token_y = None, None
                move_token = False

        # Если фишка не опущена в колонку на игровом поле, то
        # отображать траекторию фишки на игровом поле
        if (token_x is not None) and (token_y is not None):
            # Усреднять координаты для отображения фишки - посередине
            # относительно крусора мышки игрока
            draw_game_field(board, [token_x - int(ITEMSIZE / 2),
                            token_y - int(ITEMSIZE / 2), RED])
        else:
            # Иначе - оставить все как было
            draw_game_field(board)

        # Обновить экран pygame
        pygame.display.update()
        FPSCLOCK.tick()


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
    # Звук при падении фишки
    TOKENSOUND.play()

    # Пока фишка не достигла конечной свободной ячейки
    while ((y_cord - Y_ALIGNMENT) / ITEMSIZE) <= lowest_pos:
        # Двигаем ее вниз
        y_cord += speed_drop
        speed_drop += speed_incr
        # Отображение траектории падающей фишки на игровой доске
        draw_game_field(board, [x_cord, y_cord, color])
        pygame.display.update()
        FPSCLOCK.tick()


def animated_bot_drop(board, column):
    x_cord = YELLOWTOKENRECT.left
    y_cord = YELLOWTOKENRECT.top
    # Начальная скорость падения фишки
    speed_drop = 2
    # Параметр увеличения скорости
    speed_incr = 1
    # moving the yellow tile up
    while y_cord - 25 > (Y_ALIGNMENT - ITEMSIZE):
        y_cord -= speed_drop
        speed_drop += speed_incr
        draw_game_field(board, [x_cord, y_cord, YELLOW])
        pygame.display.update()
        FPSCLOCK.tick()

    # moving the yellow tile over
    y_cord = Y_ALIGNMENT - ITEMSIZE
    # Начальная скорость падения фишки
    speed_drop = 2
    # Параметр увеличения скорости
    speed_incr = 1
    while x_cord > (X_ALIGNMENT + column * ITEMSIZE):
        x_cord -= speed_drop
        speed_drop += speed_incr
        draw_game_field(board, [x_cord, y_cord, YELLOW])
        pygame.display.update()
        FPSCLOCK.tick()

    # dropping the yellow tile
    animated_drop(board, column, YELLOW)


def is_empty_space(board, column):
    ''' Возвращает True, если в колонке есть свободное место для фишки
        Иначе - False '''
    if column < 0 or column >= BOARDWIDTH or board[column][0] != VOID:
        # Если больше ширины доски или колонка заполнена
        return False
    return True


def make_move(board, color, column):
    ''' Определяем самую нижнюю свободную ячейку в заданной колонке'''
    lowest = get_lowest_pos(board, column)
    if lowest != -1:
        # Если есть место в колонке,
        # то заносим в нее фишку заданного цвета
        board[column][lowest] = color


def get_lowest_pos(board, column):
    ''' Нахождение номера свободной ячейки в колонке на игровой доске'''

    # Начинаем проверять с конца списка ячеек в колонке
    for number in range(BOARDHEIGHT - 1, -1, -1):
        # Если найдена пустая ячейка в колонке, то возвращаем ее номер
        if board[column][number] == VOID:
            return number
    # Иначе возращаем -1
    return -1


def get_bot_move(board):
    ''' Бот определяет, какой ход следует сделать следующим'''

    # Список оценок для следующих потенциальных ходов
    bot_moves = get_estimated_moves(board, YELLOW)

    # Изначально оценка потенциального хода - худшая = -1
    best_grade = -1
    # Находим наилучшую оценку для потенциального хода
    for num in range(BOARDWIDTH):
        if bot_moves[num] > best_grade and is_empty_space(board, num):
            best_grade = bot_moves[num]
    # Находим все ходы с такой же лучшей оценкой и заносим номера таких
    # колонок в список
    best_moves = []
    for num in range(len(bot_moves)):
        if bot_moves[num] == best_grade and is_empty_space(board, num):
            best_moves.append(num)

    # Случайно выбираем любую колонку для хода
    return random.choice(best_moves)


def get_estimated_moves(board, token):
    ''' Создание списка оценок для потенциальных следующих ходов бота '''

    # Противник - красная фишка
    enemy_token = RED

    # Список возможных ходов - любая из семи доступных ячеек в линии поля
    bot_moves = [0] * BOARDWIDTH
    # Проходимся по каждой ячейке в линии
    for estimated_move in range(BOARDWIDTH):
        # Методом глубокого копирования создаем временный список
        # положения фишек на поле (для моделирования различных ходов)
        bot_board = copy.deepcopy(board)
        # Пустого места в колонке нет, то пропускаем ее
        if not is_empty_space(bot_board, estimated_move):
            continue
        # Иначе - заносим фишку в ранее созданный список вариантов бота
        make_move(bot_board, token, estimated_move)

        if is_winner(bot_board, token):
            # Если выиграшный ход будет от хода бота, то даем ему
            # наивысшую "оценку" совершенности хода = 1
            bot_moves[estimated_move] = 1
            # Завершаем цикл
            break
        else:
            # Прогоняем "встречные" ходы противника-игрока
            # и определяем наилучший из них
            if is_board_full(bot_board):
                # Если ход бота приведет к полному заполнению игрового
                # поля, то даем этому ходу среднюю оценку = 0
                bot_moves[estimated_move] = 0
            else:
                # Иначе - предугадываем будущий ход противника
                # после хода бота, но берем массив положения фишек на поле,
                # получивший после прохода бота (далее - аналогично)
                for enemy_move in range(BOARDWIDTH):
                    bot_board2 = copy.deepcopy(bot_board)
                    if not is_empty_space(bot_board2, enemy_move):
                        continue
                    make_move(bot_board2, enemy_token, enemy_move)

                    if is_winner(bot_board2, enemy_token):
                        # Если потенциальный ход игрока-противника
                        # приведет к выигрышу, то даем этому ходу худшую
                        # оценку = -1
                        bot_moves[estimated_move] = -1
                        break
    return bot_moves


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
