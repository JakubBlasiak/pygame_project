import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_list, pos_x, pos_y, level):
        super().__init__()
        self.image = image_list[0]
        self.image_list = image_list
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.movement_x = 0
        self.movement_y = 0
        self._count = 0
        self._direction = 0
        self._direction_previous = 0
        self.level = level

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn_right(self):
        self.movement_x = 5
        self.stop_y()

    def turn_left(self):
        self.movement_x = -5
        self.stop_y()

    def turn_up(self):
        self.movement_y = -5
        self.stop_x()

    def turn_down(self):
        self.movement_y = 5
        self.stop_x()

    def stop_x(self):
        self.movement_x = 0

    def stop_y(self):
        self.movement_y = 0

    def stop(self):
        self.stop_y()
        self.stop_x()

    def update(self):

        # ruch w poziomie i pionie
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        self._count += 1
        if self._count == 8:
            x = random.randint(0, 3)
            if x == 0:
                if self._direction != 0:
                    self.change_direction(0)
            if x == 1:
                if self._direction != 1:
                    self.change_direction(1)
            if x == 2:
                if self._direction != 2:
                    self.change_direction(2)
            if x == 3:
                if self._direction != 3:
                    self.change_direction(3)
            self._count = 0

        # kolizja ze ścianami
        colliding_walls = pygame.sprite.spritecollide(self, self.level.set_of_walls, False)
        for w in colliding_walls:
            if self.movement_x > 0:
                self.rect.right = w.rect.left
            if self.movement_x < 0:
                self.rect.left = w.rect.right
            if self.movement_y > 0:
                self.rect.bottom = w.rect.top
            if self.movement_y < 0:
                self.rect.top = w.rect.bottom
            self.change_direction(self._direction_previous)

        # kolizja z wyjsciami
        colliding_gates = pygame.sprite.spritecollide(self, self.level.set_of_gates, False)
        for w in colliding_gates:
            if self.movement_x > 0:
                self.rect.right = w.rect.left
            if self.movement_x < 0:
                self.rect.left = w.rect.right
            if self.movement_y > 0:
                self.rect.bottom = w.rect.top
            if self.movement_y < 0:
                self.rect.top = w.rect.bottom
            self.change_direction(self._direction_previous)

        self.stop()

        if self._direction == 0:
            self.turn_right()
        if self._direction == 1:
            self.turn_down()
        if self._direction == 2:
            self.turn_left()
        if self._direction == 3:
            self.turn_up()

        # animacja
        if self._direction == 0:
            self.image = self.image_list[0]
        if self._direction == 1:
            self.image = self.image_list[1]
        if self._direction == 2:
            self.image = self.image_list[2]
        if self._direction == 3:
            self.image = self.image_list[3]

    # 0 - RIGHT, 1 - DOWN, 2 - LEFT, 3 - UP
    # zapamiętanie poprzedniego kierunku ruchu na drugiej osi
    def change_direction(self, x):
        if x % 2 == self._direction % 2:
            self._direction = x
        else:
            self._direction_previous = self._direction
            self._direction = x

    # # obsługa animacji
    # def _move(self, image_list):
    #     self.image = image_list[self._count//4]
    #     self._count = (self._count + 1) % 32
