import pygame
import os
import sys
from data import pygame_textinput
import time
import smtplib


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удалось загрузить изображение:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def send(mail, pos):
    print('отправка')
    smtpObj.sendmail('2b2t.notifier@gmail.com', mail, str("Hey, dude, you are already in the " + str(pos) +
                                                          " place in the queue, do " +
                                                          'not forget about the server. a little ' +
                                                          ' more and you will be able to plungle into the darkness ' +
                                                          'and despair on 2b2t.'))


def main():
    fon = load_image('back.jpg')
    font = pygame.font.Font('data/Font.ttf', 40)
    textinput_username = pygame_textinput.TextInput()
    textinput_email = pygame_textinput.TextInput()
    send_100 = False
    send_50 = False
    send_25 = False
    send_10 = False
    send_3 = False
    try:
        load = open('data/save.txt', 'r')
        data = ''.join(load.read()).split('\n')
        textinput_username.set_text(data[0])
        textinput_email.set_text(data[1])
        events = pygame.event.get()
        textinput_username.update(events)
        textinput_email.update(events)
        load.close()
    except:
        print('Error')
    f = 'u'
    start_pos = 999
    cur_pos = 999
    estim_time = 0
    while True:
        waiting_time = time.time() - startTime
        screen.blit(fon, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 40 <= pygame.mouse.get_pos()[0] <= 1240 and 160 <= pygame.mouse.get_pos()[1] <= 260:
                        f = 'u'
                    elif 40 <= pygame.mouse.get_pos()[0] <= 1240 and 320 <= pygame.mouse.get_pos()[1] <= 420:
                        f = 'e'
        log_path = 'C:/Users/' + textinput_username.get_text() + '/AppData/Roaming/.minecraft/logs/latest.log'
        try:
            log_file = open(log_path, 'r')
            log = log_file.read().split()
            log_file.close()
            if start_pos == 999:
                start_pos = int(log[-1])
            cur_pos = int(log[-1])
        except:
            pass
        if start_pos - cur_pos != 0:
            estim_time = waiting_time / (start_pos - cur_pos) * cur_pos

        save = open('data/save.txt', 'w')
        save.writelines((textinput_username.get_text() + '\n', textinput_email.get_text()))
        save.close()

        if f == 'u':
            textinput_username.update(events)
        else:
            textinput_email.update(events)
        screen.blit(textinput_username.get_surface(), (80, 180))
        screen.blit(textinput_email.get_surface(), (80, 340))

        disp_cp = font.render(str(cur_pos), True, (205, 205, 205))
        disp_sp = font.render(str(start_pos), True, (205, 205, 205))
        wmin = str(int(waiting_time // 60 % 60))
        if int(wmin) < 10:
            wmin = '0' + wmin
        wsec = str(int(waiting_time % 60))
        if int(wsec) < 10:
            wsec = '0' + wsec
        emin = str(int(estim_time // 60 % 60))
        if int(emin) < 10:
            emin = '0' + emin
        disp_wt = font.render(str(int(waiting_time // 3600)) + ':' + wmin + ':' + wsec, True, (205, 205, 205))
        disp_et = font.render(str(int(estim_time // 3600)) + ':' + emin,
                              True, (205, 205, 205))

        screen.blit(disp_cp, (660, 440))
        screen.blit(disp_sp, (660, 500))
        screen.blit(disp_wt, (660, 565))
        screen.blit(disp_et, (660, 625))

        if cur_pos <= 100 < start_pos and not send_100:
            send(textinput_email.get_text(), cur_pos)
            send_100 = True
        if cur_pos <= 50 < start_pos and not send_50:
            send(textinput_email.get_text(), cur_pos)
            send_50 = True
        if cur_pos <= 25 < start_pos and not send_25:
            send(textinput_email.get_text(), cur_pos)
            send_25 = True
        if cur_pos <= 3 < start_pos and not send_3:
            send(textinput_email.get_text(), cur_pos)
            send_3 = True


        pygame.display.flip()
        clock.tick(30)


size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2b2t queue notifier')
pygame.display.set_icon(load_image('icon.png'))
clock = pygame.time.Clock()

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('2b2t.notifier@gmail.com', '277353GayBot')


startTime = time.time()
main()