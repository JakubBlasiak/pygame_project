import pygame
import os
import game_module as gm
import Player as pl
import Level as le


def game():
    pygame.init()

    # centrowanie okna
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    # tworzenie okna gry
    screen = pygame.display.set_mode(gm.SIZESCREEN)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Ravie", 30)

    # konkretyzacja obiektów
    player = pl.Player(gm.PLAYER_R0)
    current_level = le.Menu(gm.MENU, player)
    player.level = current_level

    # załączenie muzyki w tle
    pygame.mixer.music.load('../music/background.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    # pętla gry
    window_open = True
    while window_open:
        screen.fill(gm.BLACK)
        for event in pygame.event.get():
            # obsługa przycisku quit okna
            if event.type == pygame.QUIT:
                if current_level.number == 0:
                    window_open = False
                else:
                    current_level = le.Menu(gm.MENU, player)
                    player.level = current_level
            # obsługa menu
            if current_level.number == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        player.eq['coin'] = 0
                        current_level = current_level.next_level()
                        player.level = current_level
            player.get_event(event)
        # jeżeli gracz przeszedł poziom
        if player.rect.x <= -40 or player.rect.x >= 880:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('../music/win.mp3'))
            player.eq['coin'] = 0
            current_level = current_level.next_level()
            player.level = current_level
        # jeśli gracz stracił wszystkie życia
        if player.eq['hearts'] == 0:
            player.eq['coin'] = 0
            current_level = current_level.game_over()
            player.level = current_level
            player.add_hearts(3)
        # aktualizacja i rysowanie obiektów
        current_level.update()
        current_level.draw(screen)
        # licznik monet
        if current_level.number != 0:
            text = font.render(str(player.eq['coin']) + '/' + str(int(current_level.number_of_coins / 2)),
                               False, [255, 255, 255])
            screen.blit(text, [680, 7])

        # aktualizacja okna gry
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
