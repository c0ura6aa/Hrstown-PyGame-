import pygame as pg
import PIL
import random
import time
from win32api import GetSystemMetrics
from PIL import Image
from CardClass import HandCard, CastedCard
# данные о картах, чтобы добавить карту, нужно добавить изображение в папку и информацию в список
DECK = ['drug/5/6/5/creature/drug_card.png', 'judah/1/3/1/creature/judah_card.png',
        'jaba/2/3/2/creature/jaba_card.png', 'igor/4/12/8/creature/igor_card.png',
        'mario/5/4/4/creature/mario_card.png', 'duck/4/3/3/creature/duck_card.png',
        'drevmesh/6/7/6/creature/drevmesh_card.png']


# рисует информацию(чей ход, мана, здоровье, оставшееся время на ход


def draw_data(height, width, ticks, screen):
    font = pg.font.Font(None, height // 12)
    mana_text = font.render(str(mana), True, (255, 255, 255))
    if ticks < 30:
        ticks_text = font.render(str(30 - ticks), True, (255, 0, 0))
    else:
        ticks_text = font.render(str(0), True, (255, 0, 0))
    screen.blit(ticks_text, (width // 24 - ticks_text.get_width() // 2, height // 2))
    screen.blit(mana_text, (width * 11.45 // 12 - mana_text.get_width() // 2, height * 5.25 // 8))
    if turn_of1:
        enemy_text = font.render('Ход игрока 1', True, (0, 0, 0))
        font = pg.font.Font(None, height // 6)
        enemy_hp_text = font.render(str(hp2), True, (192, 64, 0))
        my_hp_text = font.render(str(hp1), True, (192, 64, 0))
    else:
        enemy_text = font.render('Ход игрока 2', True, (0, 0, 0))
        font = pg.font.Font(None, height // 6)
        enemy_hp_text = font.render(str(hp1), True, (192, 64, 0))
        my_hp_text = font.render(str(hp2), True, (192, 64, 0))
    screen.blit(enemy_text, (width // 4 - enemy_text.get_width() // 2, height // 32))
    screen.blit(enemy_hp_text, (width // 2 - enemy_hp_text.get_width() // 2, height // 64))
    screen.blit(my_hp_text, (width * 5.55 // 6 - my_hp_text.get_width() // 2, height * 6.5 // 8))


# рисует карты в руке


def draw_hand(width, height, current, hand_len, screen):
    x1 = width * 5.5 // 12 - width // 8 - width // 40
    x2 = width * 6.5 // 12 + width // 40
    y1 = y2 = height * 5.25 // 8
    w1 = w2 = width // 8
    h1 = h2 = height // 4
    for i in range(0, current):
        screen.fill((46, 14, 44), pg.Rect((x1, y1), (w1, h1)))
        w1 -= width * 0.5 // 12
        x1 -= w1 // 2
        y1 += height * 0.25 // 8
        h1 -= height * 0.5 // 8
    for i in range(current + 1, hand_len):
        screen.fill((46, 14, 44), pg.Rect((x2, y2), (w2, h2)))
        w2 -= width * 0.25 // 12
        x2 += (w2 // 2)
        y2 += height * 0.25 // 8
        h2 -= height * 0.5 // 8


# выдает координаты выставляемым картам


def get_free_coords(minions_number, is_opponents):
    if is_opponents:
        x_min = width // 12 + width // 60 + minions_number * (width // 12 + width // 60)
        y_min = height * 1.1 // 8
        x_max = x_min + width // 12
        y_max = y_min + height * 1.8 // 8
    else:
        x_min = width // 12 + width // 60 + minions_number * (width // 12 + width // 60)
        y_min = height * 3.1 // 8
        x_max = x_min + width // 12
        y_max = y_min + height * 1.8 // 8
    return x_min, y_min, x_max, y_max


# рисует карты на столе


def draw_board(board1, board2):
    for i in board1:
        if i.is_active():
            screen.fill((109, 242, 7), pg.Rect((i.get_coords()[0] - width // 180, i.get_coords()[1] - height // 160),
                                               (width // 12 + width // 90, height * 1.8 // 8 + height // 80)))
        casted = Image.open(i.get_imgname())
        casted = casted.resize((width // 12, int(height * 1.8 // 8)), PIL.Image.ANTIALIAS)
        casted.save('cur_casted.png')
        casted = pg.image.load('cur_casted.png')
        font = pg.font.Font(None, height // 40)
        def_text = font.render(str(i.get_def()), True, (0, 0, 0))
        casted.blit(def_text, (width * 4.55 // 60 - def_text.get_width() // 2, height * 8.1 // 40))
        screen.blit(casted, (i.get_coords()[0], i.get_coords()[1]))
    for i in board2:
        casted = Image.open(i.get_imgname())
        casted = casted.resize((width // 12, int(height * 1.8 // 8)), PIL.Image.ANTIALIAS)
        casted.save('cur_casted.png')
        casted = pg.image.load('cur_casted.png')
        font = pg.font.Font(None, height // 40)
        def_text = font.render(str(i.get_def()), True, (0, 0, 0))
        casted.blit(def_text, (width * 4.55 // 60 - def_text.get_width() // 2, height * 8.1 // 40))
        screen.blit(casted, (i.get_coords()[0], i.get_coords()[1]))


# рисует курсор при атаке


def draw_pointer(x1, y1, x2, y2):
    pg.draw.circle(screen, (192, 64, 0), (x2, y2), height // 80)
    pg.draw.circle(screen, (192, 64, 0), (x2, y2), height // 20, height // 80)
    pg.draw.line(screen, (192, 64, 0), (x1, y1), (x2, y2), 40)


# анимация выставления - смерти


def placing_animation(coordinates, backwards):
    if backwards:
        for i in range(10):
            screen.fill(pg.Color(18 * (10 - i), 15 * (10 - i), 23 * (10 - i)),
                        pg.Rect(coordinates[0] - width // 180, coordinates[1] - height // 160,
                                width // 12 + width // 90, height * 1.8 // 8 + height // 80))
            screen.blit(punch_particle, (coordinates[0] + width // 48,
                                         coordinates[1] + height * 0.9 // 8 - height // 32))
            pg.display.flip()
            time.sleep(0.03)
    else:
        for i in range(10):
            screen.fill(pg.Color(18 * i, 15 * i, 23 * i), pg.Rect(coordinates[0],
                                                                  coordinates[1], width // 12, height * 1.8 // 8))
            pg.display.flip()
            time.sleep(0.03)


# функция обновления экрана, вынесенная из цикла


def update_screen():
    screen.blit(board_surf, (0, 0))
    draw_data(height, width, ticks, screen)
    if muted:
        screen.blit(pg.image.load('v_mute1.png'), (width * 11 // 12, 0))
    else:
        screen.blit(pg.image.load('ne_v_mute1.png'), (width * 11 // 12, 0))
    if turn_of1:
        draw_board(board1, board2)
        draw_hand(width, height, current, len(hand1), screen)
        if len(hand1) > 0:
            if hand1[current].get_manacost() <= mana:
                hand1[current].set_active(True)
            card = Image.open(hand1[current].get_imgname())
            if int(hand1[current].get_manacost()) <= mana:
                screen.fill((109, 242, 7), pg.Rect((width * 5 // 12 - 20, height * 5 // 8 - 20),
                                                   (width // 6 + 40, height * 3 // 8 + 40)))
            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
            card.save('cur_card.png')
            card_img = pg.image.load('cur_card.png')
            screen.blit(card_img, (width * 5 // 12, height * 5 // 8))
        if attacking:
            draw_pointer(board1[chosen].get_coords()[0] + width // 24,
                         board1[chosen].get_coords()[1] + height * 3 // 32,
                         pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    else:
        draw_board(board2, board1)
        draw_hand(width, height, current, len(hand2), screen)
        if len(hand2) > 0:
            if hand2[current].get_manacost() <= mana:
                hand2[current].set_active(True)
            card = Image.open(hand2[current].get_imgname())
            if int(hand2[current].get_manacost()) <= mana:
                screen.fill((109, 242, 7), pg.Rect((width * 5 // 12 - 20, height * 5 // 8 - 20),
                                                   (width // 6 + 40, height * 3 // 8 + 40)))
            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
            card.save('cur_card.png')
            card_img = pg.image.load('cur_card.png')
            screen.blit(card_img, (width * 5 // 12, height * 5 // 8))
        if attacking:
            draw_pointer(board2[chosen].get_coords()[0] + width // 24,
                         board2[chosen].get_coords()[1] + height * 3 // 32,
                         pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Hrstown')
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    size = (width, height - 60)
    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    TIMESUP = pg.USEREVENT + 1
    bg_img = Image.open('game.png')
    bg_img = bg_img.resize((width, height), PIL.Image.ANTIALIAS)
    bg_img.save('game1.png')
    bg_img = Image.open('winscreen.jpg')
    bg_img = bg_img.resize((width, height), PIL.Image.ANTIALIAS)
    bg_img.save('winscreen1.png')
    v_mute = Image.open('v_mute.png')
    v_mute = v_mute.resize((width // 12, height // 8), PIL.Image.ANTIALIAS)
    v_mute.save('v_mute1.png')
    ne_v_mute = Image.open('ne_v_mute.png')
    ne_v_mute = ne_v_mute.resize((width // 12, height // 8), PIL.Image.ANTIALIAS)
    ne_v_mute.save('ne_v_mute1.png')
    board_surf = pg.image.load('game1.png')
    screen.blit(board_surf, (0, 0))
    faq = Image.open('chikibamboni.png')
    faq = faq.resize((width // 2, height * 8 // 10), PIL.Image.ANTIALIAS)
    faq.save('faq.png')
    punch_particle = Image.open('punch_particle.png')
    punch_particle = punch_particle.resize((width // 24, height // 16), PIL.Image.ANTIALIAS)
    punch_particle.save('punch_particle.png')
    punch_particle = pg.image.load('punch_particle.png')
    punch_particle.set_colorkey((255, 255, 255))
    start_game = pg.mixer.Sound('start_game.wav')
    pick_card = pg.mixer.Sound('card2hand.wav')
    turn_change = pg.mixer.Sound('turn.wav')
    turn_change.set_volume(0.2)
    pick_card.set_volume(0.25)
    punch = pg.mixer.Sound('attack.wav')
    place = pg.mixer.Sound('place.wav')
    playin = False
    running = True
    clicked = False
    attacking = False
    game_started = False
    game_ended = False
    turn_of1 = True
    muted = False
    current = 0
    chosen = 0
    mana = 0
    max_mana = 0
    turns = 0
    ticks = 0
    deck1 = []
    deck2 = []
    hand1 = []
    hand2 = []
    board1 = []
    board2 = []
    while running:
        if not game_started and not game_ended:  # стартовый экран
            if not playin:
                pg.mixer.music.load('greeting.mp3')
                pg.mixer.music.set_volume(0.2)
                if not muted:
                    pg.mixer.music.play(-1)
                playin = True
                bg_img = Image.open('greeting.png')
                bg_img = bg_img.resize((width, height), PIL.Image.ANTIALIAS)
                bg_img.save('greeting1.png')
                board_surf = pg.image.load('greeting1.png')
            screen.blit(board_surf, (0, 0))
            if muted:
                mute = pg.image.load('v_mute1.png')
            else:
                mute = pg.image.load('ne_v_mute1.png')
            screen.blit(mute, (width * 11 // 12, height * 6 // 8))
            font = pg.font.Font(None, height // 6)
            faq1 = font.render('?', False, (0, 0, 0))
            screen.blit(faq1, (width // 12 - faq1.get_width() // 2, height * 6.5 // 8 - height // 12))
            font = pg.font.Font(None, height * 10 // 65)
            if (width // 24 < pg.mouse.get_pos()[0] < width * 1.5 // 12
                    and height * 6 // 8 < pg.mouse.get_pos()[1] < height * 6.5 // 8):
                faq2 = font.render('?', False, (109, 242, 7))
                screen.blit(faq2, (width // 12 - faq2.get_width() // 2, height * 6.5 // 8 - height * 10 // 125))
                faq = pg.image.load('faq.png')
                screen.blit(faq, (width // 4, height // 10))
            else:
                faq2 = font.render('?', False, (255, 255, 255))
                screen.blit(faq2, (width // 12 - faq2.get_width() // 2, height * 6.5 // 8 - height * 10 // 125))
            for event in pg.event.get():
                if (event.type == pg.MOUSEBUTTONDOWN and
                        width * 11 // 12 < event.pos[0] < width and height * 6 // 8 < event.pos[1] < height):
                    if muted:
                        muted = False
                        pg.mixer.music.play()
                    else:
                        pg.mixer.music.stop()
                        muted = True
                if event.type == pg.MOUSEBUTTONDOWN and (width // 3 < event.pos[0] < width * 2 // 3
                                                         and height * 5 // 8 < event.pos[1] < height * 7 // 8):
                    game_started = True
                    playin = False
                    bg_img = Image.open('game1.png')
                    bg_img = bg_img.resize((width, height), PIL.Image.ANTIALIAS)
                    board_surf = pg.image.load('game1.png')
                if event.type == pg.QUIT:
                    running = False
        if game_started and not game_ended:  # игра
            if not playin:
                attacking = False
                clicked = False
                deck1 = []
                deck2 = []
                for i in range(2):
                    for j in DECK:
                        deck1.append(HandCard(j.split('/')[0], j.split('/')[1], j.split('/')[2], j.split('/')[3],
                                              j.split('/')[4], j.split('/')[5]))
                        deck2.append(HandCard(j.split('/')[0], j.split('/')[1], j.split('/')[2], j.split('/')[3],
                                              j.split('/')[4], j.split('/')[5]))
                if not muted:
                    start_game.play()
                hand1 = []
                hand2 = []
                board1 = []
                board2 = []
                pg.time.set_timer(TIMESUP, 1000)
                hp1 = 30
                hp2 = 30
                turns = 0
                ticks = 0
                max_mana = 1
                mana = 1
                for i in range(2):
                    r = random.randint(0, len(deck1) - 1)
                    hand1.append(deck1[r])
                    del deck1[r]
                for i in range(3):
                    r = random.randint(0, len(deck2) - 1)
                    hand2.append(deck2[r])
                    del deck2[r]
                current = 0
                if not clicked:
                    update_screen()
                pg.mixer.music.stop()
                pg.mixer.music.load('game.mp3')
                pg.mixer.music.set_volume(0.1)
                if not muted:
                    pg.mixer.music.play(-1)
                playin = True
            board_surf = pg.image.load('game1.png')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if (event.type == pg.MOUSEBUTTONDOWN and
                        width * 11 // 12 < event.pos[0] < width and 0 < event.pos[1] < height // 8):  # вкл\выкл звук
                    if muted:
                        pg.mixer.music.play()
                        muted = False
                        if not clicked:
                            update_screen()
                    else:
                        pg.mixer.music.stop()
                        muted = True
                        if not clicked:
                            update_screen()
                if event.type == TIMESUP:  # 1 tick - 1 секунда, при 30 меняет ход
                    ticks += 1
                    if ticks >= 30:
                        if not muted:
                            turn_change.play()
                        clicked = False
                        attacking = False
                        pg.mouse.set_visible(True)
                        turns += 1
                        if turn_of1:
                            for i in board1:
                                i.set_coords((i.get_coords()[0], i.get_coords()[1] - height // 4,
                                              i.get_coords()[2], i.get_coords()[3] - height // 4))
                                i.set_active(True)
                            for i in board2:
                                i.set_coords((i.get_coords()[0], i.get_coords()[1] + height // 4,
                                              i.get_coords()[2], i.get_coords()[3] + height // 4))
                            if len(deck1) > 0 and len(hand1) < 7:
                                r = random.randint(0, len(deck1) - 1)
                                hand1.append(deck1[r])
                                if not muted:
                                    pick_card.play()
                                del deck1[r]
                            if len(hand1) > 0:
                                hand1[current].set_active(False)
                            turn_of1 = False
                            current = 0
                        else:
                            for i in board2:
                                i.set_coords((i.get_coords()[0], i.get_coords()[1] - height // 4,
                                              i.get_coords()[2], i.get_coords()[3] - height // 4))
                                i.set_active(True)
                            for i in board1:
                                i.set_coords((i.get_coords()[0], i.get_coords()[1] + height // 4,
                                              i.get_coords()[2], i.get_coords()[3] + height // 4))
                            if len(deck2) > 0 and len(hand2) < 7:
                                r = random.randint(0, len(deck2) - 1)
                                hand2.append(deck2[r])
                                if not muted:
                                    pick_card.play()
                                del deck2[r]
                            if len(hand2) > 0:
                                hand2[current].set_active(False)
                            turn_of1 = True
                            current = 0
                            if max_mana < 10:
                                max_mana += 1
                        if not clicked:
                            update_screen()
                        mana = max_mana
                        ticks = 0
                    update_screen()
                    pg.time.set_timer(TIMESUP, 1000)
                # выставление карты
                if event.type == pg.MOUSEBUTTONUP and clicked and event.button == 1 and not attacking:
                    if width // 12 < event.pos[0] < width * 11 // 12 and height // 8 < event.pos[1] < height * 5 // 8:
                        if turn_of1:
                            if hand1[current].is_active() and len(board1) < 8:
                                if not muted:
                                    place.play()
                                mana -= hand1[current].get_manacost()
                                board1.append(CastedCard(hand1[current].get_name(),
                                                         hand1[current].get_attack(),
                                                         hand1[current].get_def(),
                                                         hand1[current].get_manacost(),
                                                         hand1[current].get_type(),
                                                         hand1[current].get_imgname(),
                                                         get_free_coords(len(board1), False)))
                                placing_animation(board1[-1].get_coords(), False)
                                del hand1[current]
                                current += 1
                                if len(hand1) > 0:
                                    current = current % len(hand1)
                                else:
                                    current = 0
                        else:
                            if hand2[current].is_active() and len(board2) < 8:
                                if not muted:
                                    place.play()
                                mana -= hand2[current].get_manacost()
                                board2.append(CastedCard(hand2[current].get_name(),
                                                         hand2[current].get_attack(),
                                                         hand2[current].get_def(),
                                                         hand2[current].get_manacost(),
                                                         hand2[current].get_type(),
                                                         hand2[current].get_imgname(),
                                                         get_free_coords(len(board2), False)))
                                placing_animation(board2[-1].get_coords(), False)
                                del hand2[current]
                                current += 1
                                if len(hand2) > 0:
                                    current = current % len(hand2)
                                else:
                                    current = 0
                    update_screen()
                    clicked = False
                # листание карт в руке
                if event.type == pg.KEYDOWN and ((turn_of1 and len(hand1) > 0) or (not turn_of1 and len(hand2) > 0)):
                    attacking = False
                    pg.mouse.set_visible(True)
                    if turn_of1:
                        hand1[current].set_active(False)
                    else:
                        hand2[current].set_active(False)
                    if event.key == pg.K_RIGHT:
                        current += 1
                        if turn_of1:
                            current = current % len(hand1)
                        else:
                            current = current % len(hand2)
                        if turn_of1:
                            card = Image.open(hand1[current].get_imgname())
                            draw_hand(width, height, current, len(hand1), screen)
                        else:
                            card = Image.open(hand2[current].get_imgname())
                            draw_hand(width, height, current, len(hand2), screen)
                        card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                        card.save('cur_card.png')
                        card_img = pg.image.load('cur_card.png')
                        screen.blit(card_img, (width * 6 // 12, height * 4 // 8))
                        if not muted:
                            pick_card.play()
                        clicked = False
                        update_screen()
                    elif event.key == pg.K_LEFT:
                        current -= 1
                        if turn_of1 and current < 0:
                            current = current + len(hand1)
                        elif not turn_of1 and current < 0:
                            current = current + len(hand2)
                        if turn_of1:
                            card = Image.open(hand1[current].get_imgname())
                            draw_hand(width, height, current, len(hand1), screen)
                        else:
                            card = Image.open(hand2[current].get_imgname())
                            draw_hand(width, height, current, len(hand2), screen)
                        card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                        card.save('cur_card.png')
                        card_img = pg.image.load('cur_card.png')
                        screen.blit(card_img, (width * 4 // 12, height * 4 // 8))
                        if not muted:
                            pick_card.play()
                        clicked = False
                        update_screen()
                # кнопка сдаться
                if event.type == pg.MOUSEBUTTONDOWN and width // 24 < event.pos[0] < width * 1.5 // 12 \
                        and height * 6.5 // 8 < event.pos[1] < height and event.button == 1\
                        and not clicked and not attacking:
                    if turn_of1:
                        turn_of1 = False
                    else:
                        turn_of1 = True
                    game_started = False
                    game_ended = True
                    playin = False
                    pg.mixer.music.stop()
                    update_screen()
                # взятие карты в руку для выставления
                if event.type == pg.MOUSEBUTTONDOWN and width * 5 // 12 < event.pos[0] < width * 7 // 12 \
                        and height * 5 // 8 < event.pos[1] < height and event.button == 1:
                    attacking = False
                    pg.mouse.set_visible(True)
                    screen.blit(board_surf, (0, 0))
                    draw_data(height, width, ticks, screen)
                    if muted:
                        mute = pg.image.load('v_mute1.png')
                    else:
                        mute = pg.image.load('ne_v_mute1.png')
                    screen.blit(mute, (width * 11 // 12, 0))
                    if turn_of1:
                        draw_board(board1, board2)
                        draw_hand(width, height, current, len(hand1), screen)
                        if len(hand1) > 0:
                            card = Image.open(hand1[current].get_imgname())
                            if int(hand1[current].get_manacost()) <= mana:
                                screen.fill((109, 242, 7), pg.Rect((event.pos[0] - width // 12 - 20,
                                                                    event.pos[1] - height * 3 // 16 - 20),
                                                                   (width // 6 + 40, height * 3 // 8 + 40)))
                            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                            card.save('cur_card.png')
                            card_img = pg.image.load('cur_card.png')
                            screen.blit(card_img, (event.pos[0] - width // 12, event.pos[1] - height * 3 // 16))
                            clicked = True
                    else:
                        draw_board(board2, board1)
                        draw_hand(width, height, current, len(hand2), screen)
                        if len(hand2) > 0:
                            card = Image.open(hand2[current].get_imgname())
                            if int(hand2[current].get_manacost()) <= mana:
                                screen.fill((109, 242, 7), pg.Rect((event.pos[0] - width // 12 - 20,
                                                                    event.pos[1] - height * 3 // 16 - 20),
                                                                   (width // 6 + 40, height * 3 // 8 + 40)))
                            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                            card.save('cur_card.png')
                            card_img = pg.image.load('cur_card.png')
                            screen.blit(card_img, (event.pos[0] - width // 12, event.pos[1] - height * 3 // 16))
                            clicked = True
                # кнопка передачи хода
                if (event.type == pg.MOUSEBUTTONDOWN and 0 < event.pos[0] < width // 12 and
                        height * 5 // 8 < event.pos[1] < height * 3 // 4 and not clicked and event.button == 1):
                    ticks = 30
                # когда карта взята, она прикреплена к курсору
                if event.type == pg.MOUSEMOTION and clicked and not attacking:
                    screen.blit(board_surf, (0, 0))
                    draw_data(height, width, ticks, screen)
                    if muted:
                        mute = pg.image.load('v_mute1.png')
                    else:
                        mute = pg.image.load('ne_v_mute1.png')
                    screen.blit(mute, (width * 11 // 12, 0))
                    if turn_of1:
                        draw_board(board1, board2)
                        draw_hand(width, height, current, len(hand1), screen)
                        if len(hand1) > 0:
                            card = Image.open(hand1[current].get_imgname())
                            if int(hand1[current].get_manacost()) <= mana:
                                screen.fill((109, 242, 7), pg.Rect((event.pos[0] - width // 12 - 20,
                                                                    event.pos[1] - height * 3 // 16 - 20),
                                                                   (width // 6 + 40, height * 3 // 8 + 40)))
                            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                            card.save('cur_card.png')
                            card_img = pg.image.load('cur_card.png')
                            screen.blit(card_img, (event.pos[0] - width // 12, event.pos[1] - height * 3 // 16))
                    else:
                        draw_board(board2, board1)
                        draw_hand(width, height, current, len(hand2), screen)
                        if len(hand2) > 0:
                            card = Image.open(hand2[current].get_imgname())
                            if int(hand2[current].get_manacost()) <= mana:
                                screen.fill((109, 242, 7), pg.Rect((event.pos[0] - width // 12 - 20,
                                                                    event.pos[1] - height * 3 // 16 - 20),
                                                                   (width // 6 + 40, height * 3 // 8 + 40)))
                            card = card.resize((width // 6, height * 3 // 8), PIL.Image.ANTIALIAS)
                            card.save('cur_card.png')
                            card_img = pg.image.load('cur_card.png')
                            screen.blit(card_img, (event.pos[0] - width // 12, event.pos[1] - height * 3 // 16))
                    if (width // 12 + 20 >= event.pos[0] or event.pos[0] == width - 1
                            or height * 3 // 16 + 40 > event.pos[1] or event.pos[0] == height - 1):
                        clicked = False
                        screen.blit(board_surf, (0, 0))
                        draw_data(height, width, ticks, screen)
                        if turn_of1:
                            draw_board(board1, board2)
                            draw_hand(width, height, current, len(hand1), screen)
                        else:
                            draw_board(board2, board1)
                            draw_hand(width, height, current, len(hand2), screen)
                # выбор карты для атаки
                if (event.type == pg.MOUSEBUTTONDOWN and not clicked and event.button == 1
                        and width // 12 < event.pos[0] < width * 11 // 12
                        and height // 8 < event.pos[1] < height * 5 // 8):
                    if turn_of1:
                        for i in range(len(board1)):
                            if (board1[i].get_coords()[0] < event.pos[0] < board1[i].get_coords()[2]
                                    and board1[i].get_coords()[1] < event.pos[1] < board1[i].get_coords()[3]
                                    and board1[i].is_active()):
                                chosen = i
                                attacking = True
                                pg.mouse.set_visible(False)
                                draw_pointer(board1[chosen].get_coords()[0] + width // 24,
                                             board1[chosen].get_coords()[1] + height * 3 // 32,
                                             event.pos[0], event.pos[1])
                    else:
                        for i in range(len(board2)):
                            if (board2[i].get_coords()[0] < event.pos[0] < board2[i].get_coords()[2]
                                    and board2[i].get_coords()[1] < event.pos[1] < board2[i].get_coords()[3]
                                    and board2[i].is_active()):
                                chosen = i
                                attacking = True
                                pg.mouse.set_visible(False)
                                draw_pointer(board2[chosen].get_coords()[0] + width // 24,
                                             board2[chosen].get_coords()[1] + height * 3 // 32,
                                             event.pos[0], event.pos[1])
                    update_screen()
                # когда атака совершена, смотрит на кого и производит вычисления
                if event.type == pg.MOUSEBUTTONUP and attacking:
                    if turn_of1:
                        for i in range(len(board2)):
                            if (board2[i].get_coords()[0] < event.pos[0] < board2[i].get_coords()[2]
                                    and board2[i].get_coords()[1] < event.pos[1] < board2[i].get_coords()[3]):
                                board2[i].set_def(board2[i].get_def() - board1[chosen].get_attack())
                                board1[chosen].set_def(board1[chosen].get_def() - board2[i].get_attack())
                                if board1[chosen].get_def() <= 0:
                                    placing_animation(board1[chosen].get_coords(), True)
                                    for j in range(chosen + 1, len(board1)):
                                        board1[j].set_coords((board1[j].get_coords()[0] - width // 10,
                                                              board1[j].get_coords()[1],
                                                              board1[j].get_coords()[2] - width // 10,
                                                              board1[j].get_coords()[3]))
                                    del board1[chosen]
                                else:
                                    screen.blit(punch_particle, event.pos)
                                    board1[chosen].set_active(False)
                                attacking = False
                                pg.mouse.set_visible(True)
                                if not muted:
                                    punch.play()
                                if board2[i].get_def() <= 0:
                                    placing_animation(board2[i].get_coords(), True)
                                    for j in range(i + 1, len(board2)):
                                        board2[j].set_coords((board2[j].get_coords()[0] - width // 10,
                                                              board2[j].get_coords()[1],
                                                              board2[j].get_coords()[2] - width // 10,
                                                              board2[j].get_coords()[3]))
                                    del board2[i]
                                    break
                                else:
                                    screen.blit(punch_particle, event.pos)
                        if attacking:
                            if width * 5 // 12 < event.pos[0] < width * 7 // 12 and 0 < event.pos[1] < height // 8:
                                hp2 -= board1[chosen].get_attack()
                                screen.blit(punch_particle, event.pos)
                                board1[chosen].set_active(False)
                                if not muted:
                                    punch.play()
                                if hp2 <= 0:
                                    attacking = False
                                    pg.mouse.set_visible(True)
                                    game_started = False
                                    game_ended = True
                                    playin = False
                                    pg.mixer.music.stop()
                        if attacking:
                            attacking = False
                            pg.mouse.set_visible(True)
                    else:
                        for i in range(len(board1)):
                            if (board1[i].get_coords()[0] < event.pos[0] < board1[i].get_coords()[2]
                                    and board1[i].get_coords()[1] < event.pos[1] < board1[i].get_coords()[3]):
                                board1[i].set_def(board1[i].get_def() - board2[chosen].get_attack())
                                board2[chosen].set_def(board2[chosen].get_def() - board1[i].get_attack())
                                if board2[chosen].get_def() <= 0:
                                    placing_animation(board2[chosen].get_coords(), True)
                                    for j in range(chosen + 1, len(board2)):
                                        board2[j].set_coords((board2[j].get_coords()[0] - width // 10,
                                                              board2[j].get_coords()[1],
                                                              board2[j].get_coords()[2] - width // 10,
                                                              board2[j].get_coords()[3]))
                                    del board2[chosen]
                                else:
                                    screen.blit(punch_particle, event.pos)
                                    board2[chosen].set_active(False)
                                attacking = False
                                pg.mouse.set_visible(True)
                                if not muted:
                                    punch.play()
                                if board1[i].get_def() <= 0:
                                    placing_animation(board1[i].get_coords(), True)
                                    for j in range(i + 1, len(board1)):
                                        board1[j].set_coords((board1[j].get_coords()[0] - width // 10,
                                                              board1[j].get_coords()[1],
                                                              board1[j].get_coords()[2] - width // 10,
                                                              board1[j].get_coords()[3]))
                                    del board1[i]
                                    break
                                else:
                                    screen.blit(punch_particle, event.pos)
                        if attacking:
                            if width * 5 // 12 < event.pos[0] < width * 7 // 12 and 0 < event.pos[1] < height // 8:
                                hp1 -= board2[chosen].get_attack()
                                screen.blit(punch_particle, event.pos)
                                board2[chosen].set_active(False)
                                if not muted:
                                    punch.play()
                                if hp1 <= 0:
                                    attacking = False
                                    pg.mouse.set_visible(True)
                                    game_started = False
                                    game_ended = True
                                    playin = False
                                    pg.mixer.music.stop()
                        if attacking:
                            attacking = False
                            pg.mouse.set_visible(True)
                    update_screen()
                # двигает курсор при атаке
                if event.type == pg.MOUSEMOTION and attacking:
                    update_screen()
        if not game_started and game_ended:  # экран с результатами
            if not playin:
                if not muted:
                    pg.mixer.music.load('victory_jingle.wav')
                    pg.mixer.music.set_volume(0.2)
                    pg.mixer.music.play()
                playin = True
            board_surf = pg.image.load('winscreen1.png')
            screen.blit(board_surf, (0, 0))
            font = pg.font.Font(None, height // 12)
            if muted:
                mute = pg.image.load('v_mute1.png')
            else:
                mute = pg.image.load('ne_v_mute1.png')
            screen.blit(mute, (width * 11 // 12, height * 6 // 8))
            if turn_of1:
                winner_text = font.render('Победил игрок 1!', True, (0, 0, 0))
            else:
                winner_text = font.render('Победил игрок 2!', True, (0, 0, 0))
            screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height * 3.37 // 8))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if (event.type == pg.MOUSEBUTTONDOWN and
                        width * 11 // 12 < event.pos[0] < width and height * 6 // 8 < event.pos[1] < height):
                    if muted:
                        muted = False
                    else:
                        pg.mixer.music.stop()
                        muted = True
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if (width * 5 // 12 < event.pos[0] < width * 7 // 12 and
                            height * 5 // 8 < event.pos[1] < height * 6.5 // 8):
                        game_ended = False
                        game_started = False
                        playin = False
                    if (width * 5 // 12 < event.pos[0] < width * 7 // 12 and
                            height * 6.5 // 8 < event.pos[1] < height):
                        running = False
        pg.display.flip()
        clock.tick(50)
