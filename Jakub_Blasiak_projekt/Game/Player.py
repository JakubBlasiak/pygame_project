import pygame
import game_module as gm
import Item as it


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self._direction = 0
        self._direction_previous = 0
        self.level = None
        self.eq = {'coin': 0, 'hearts': 3}
        self.set_of_hearts = pygame.sprite.Group()
        self.add_hearts()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.set_of_hearts.draw(surface)

    def turn_right(self):
        self.movement_x = 5

    def turn_left(self):
        self.movement_x = -5

    def turn_up(self):
        self.movement_y = -5

    def turn_down(self):
        self.movement_y = 5

    def stop_x(self):
        self.movement_x = 0

    def stop_y(self):
        self.movement_y = 0

    def update(self):

        # ruch w poziomie i pionie
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        # zapobieganie zatrzymywania się postaci
        if self.movement_y == 0 and self.movement_x == 0:
            self.change_direction(self._direction_previous)
            if self._direction == 0:
                self.turn_right()
            if self._direction == 1:
                self.turn_down()
            if self._direction == 2:
                self.turn_left()
            if self._direction == 3:
                self.turn_up()

        # animacja
        if self.movement_x > 0:
            self._move(gm.PLAYER_WALK_LIST_R)
        if self.movement_x < 0:
            self._move(gm.PLAYER_WALK_LIST_L)
        if self.movement_y > 0:
            self._move(gm.PLAYER_WALK_LIST_D)
        if self.movement_y < 0:
            self._move(gm.PLAYER_WALK_LIST_U)

        # kolizja ze ścianami
        colliding_walls = pygame.sprite.spritecollide(self, self.level.set_of_walls, False)
        for w in colliding_walls:
            if self.movement_x > 0:
                self.rect.right = w.rect.left
                self.stop_x()
            if self.movement_x < 0:
                self.rect.left = w.rect.right
                self.stop_x()
            if self.movement_y > 0:
                self.rect.bottom = w.rect.top
                self.stop_y()
            if self.movement_y < 0:
                self.rect.top = w.rect.bottom
                self.stop_y()

        # kolizja z wyjściami
        colliding_gates = pygame.sprite.spritecollide(self, self.level.set_of_gates, False)
        for w in colliding_gates:
            if self.movement_x > 0:
                self.rect.right = w.rect.left
                self.stop_x()
            if self.movement_x < 0:
                self.rect.left = w.rect.right
                self.stop_x()
            if self.movement_y > 0:
                self.rect.bottom = w.rect.top
                self.stop_y()
            if self.movement_y < 0:
                self.rect.top = w.rect.bottom
                self.stop_y()

        # kolizja z przeciwnikami
        colliding_enemies = pygame.sprite.spritecollide(self, self.level.set_of_enemies, False)
        if colliding_enemies:
            if self.eq['hearts'] > 1:
                self.set_of_hearts = pygame.sprite.Group()
                self.eq['hearts'] = self.eq['hearts'] - 1
                self.add_hearts(self.eq['hearts'])
                self.rect.left = 400
                self.rect.bottom = 560
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('../music/death.mp3'))
            else:
                self.eq['hearts'] = 0
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('../music/game_over.mp3'))

        # kolizja z przedmiotami
        colliding_coins = pygame.sprite.spritecollide(self, self.level.set_of_coins, False)
        for coin in colliding_coins:
            if coin.name == 'coin':
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('../music/coin_pick.mp3'))
                self.eq[coin.name] += 1
                coin.kill()

    # 0 - RIGHT, 1 - DOWN, 2 - LEFT, 3 - UP
    # zapamiętanie poprzedniego kierunku ruchu na drugiej osi
    def change_direction(self, x):
        if x % 2 == self._direction % 2:
            self._direction = x
        else:
            self._direction_previous = self._direction
            self._direction = x

    # obsługa klawiszy
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self._direction != 0:
                    self.stop_y()
                    self.turn_right()
                    self.change_direction(0)
            if event.key == pygame.K_LEFT:
                if self._direction != 2:
                    self.stop_y()
                    self.turn_left()
                    self.change_direction(2)
            if event.key == pygame.K_DOWN:
                if self._direction != 1:
                    self.stop_x()
                    self.turn_down()
                    self.change_direction(1)
            if event.key == pygame.K_UP:
                if self._direction != 3:
                    self.stop_x()
                    self.turn_up()
                    self.change_direction(3)

    # obsługa animacji
    def _move(self, image_list):
        self.image = image_list[self._count//4]
        self._count = (self._count + 1) % 32

    # dodawanie żyć
    def add_hearts(self, x=3):
        self.eq['hearts'] = x
        for i in range(0, x):
            self.set_of_hearts.add(it.Item(gm.HEART, 'heart' + str(i), 60 + i*40, 20))
