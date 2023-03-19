import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, image, name, pos_center_x, pos_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = [pos_center_x, pos_center_y]


class Coin(Item):
    def __init__(self, image_list, name, pos_center_x, pos_center_y):
        super().__init__(image_list[0], name, pos_center_x, pos_center_y)
        self.image_list = image_list
        self._count = 0

    def _animation(self):
        self.image = self.image_list[self._count // 8]
        self._count = (self._count + 1) % 48

    def update(self):
        self._animation()
