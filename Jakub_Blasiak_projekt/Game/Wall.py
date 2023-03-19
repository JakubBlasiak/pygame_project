import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.width = width
        self.height = height
        self.border = pygame.surface.Surface([self.width, self.height])
        self.rect = self.border.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, surface):
        if self.width == 40 and self.height == 40:
            surface.blit(self.image, self.rect)
        elif self.height == 40:
            for x in range(0, self.width, 40):
                surface.blit(self.image, [self.rect.x + x, self.rect.y])
        elif self.width == 40:
            for x in range(0, self.height, 40):
                surface.blit(self.image, [self.rect.x, self.rect.y + x])


class Gate(Wall):
    def __init__(self, image, width, height, pos_x, pos_y, coins, player):
        super().__init__(image, width, height, pos_x, pos_y)
        self.needed_coins = coins
        self.player = player

    def update(self):
        if self.player.eq['coin'] >= self.needed_coins:
            self.kill()
