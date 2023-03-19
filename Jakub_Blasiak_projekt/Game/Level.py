import pygame
import game_module as gm
import Wall as wa
import Item as it
import Enemy as en


class Menu(pygame.sprite.Sprite):
    def __init__(self, image, player):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.player = player
        self.player.rect.x = 0
        self.player.rect.y = 0
        self.number = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        pass

    def next_level(self):
        return Level1(self.player)


class Level:
    def __init__(self, player):
        self.player = player
        self.set_of_enemies = pygame.sprite.Group()
        self.set_of_walls = pygame.sprite.Group()
        self.set_of_coins = pygame.sprite.Group()
        self.set_of_gates = pygame.sprite.Group()
        self.number_of_coins = 0

    def update(self):
        self.set_of_coins.update()
        self.set_of_gates.update()
        self.player.update()
        self.set_of_enemies.update()

    def draw(self, surface):
        for x in self.set_of_walls:
            x.draw(surface)
        for x in self.set_of_gates:
            x.draw(surface)
        self.set_of_coins.draw(surface)
        self.player.draw(surface)
        self.set_of_enemies.draw(surface)

    def game_over(self):
        return Menu(gm.MENU, self.player)


class Level1(Level):
    def __init__(self, player):
        super().__init__(player)
        self._create_walls()
        self._create_coins()
        self._create_gates()
        self._create_enemies()
        self.player.rect.left = 400
        self.player.rect.bottom = 560
        self.number = 1

    def _create_walls(self):
        walls_cor = gm.LEVEL1_WALLS
        for cor in walls_cor:
            self.set_of_walls.add(wa.Wall(gm.WALL, *cor))

    def _create_coins(self):
        coins_cor = gm.LEVEL1_COINS
        for cor in coins_cor:
            self.number_of_coins += 1
            self.set_of_coins.add(it.Coin(gm.COIN_LIST, 'coin', *cor))
        self.number_of_coins -= 1

    def _create_gates(self):
        gates_cor = gm.LEVEL1_GATES
        for cor in gates_cor:
            self.set_of_gates.add(wa.Gate(gm.WALL, *cor, self.number_of_coins/2, self.player))

    def _create_enemies(self):
        self.set_of_enemies.add(en.Enemy(gm.ENEMY_PINK_LIST, 40, 160, self))
        self.set_of_enemies.add(en.Enemy(gm.ENEMY_BLUE_LIST, 760, 160, self))

    def next_level(self):
        return Level2(self.player)


class Level2(Level):
    def __init__(self, player):
        super().__init__(player)
        self._create_walls()
        self._create_coins()
        self._create_gates()
        self.player.rect.left = 400
        self.player.rect.bottom = 560
        self.number = 2

    def _create_walls(self):
        walls_cor = gm.LEVEL1_WALLS
        for cor in walls_cor:
            self.set_of_walls.add(wa.Wall(gm.WALL, *cor))

    def _create_coins(self):
        coins_cor = gm.LEVEL1_COINS
        for cor in coins_cor:
            self.number_of_coins += 1
            self.set_of_coins.add(it.Coin(gm.COIN_LIST, 'coin', *cor))
        self.number_of_coins -= 1

    def _create_gates(self):
        gates_cor = []
        for cor in gates_cor:
            self.set_of_gates.add(wa.Gate(gm.WALL, *cor, self.number_of_coins/2, self.player))

    def next_level(self):
        return Level3(self.player)


class Level3(Level):
    def __init__(self, player):
        super().__init__(player)
        self._create_walls()
        self._create_coins()
        self._create_gates()
        self.player.rect.left = 400
        self.player.rect.bottom = 560
        self.number = 3

    def _create_walls(self):
        walls_cor = gm.LEVEL1_WALLS
        for cor in walls_cor:
            self.set_of_walls.add(wa.Wall(gm.WALL, *cor))

    def _create_coins(self):
        coins_cor = gm.LEVEL1_COINS
        for cor in coins_cor:
            self.number_of_coins += 1
            self.set_of_coins.add(it.Coin(gm.COIN_LIST, 'coin', *cor))
        self.number_of_coins -= 1

    def _create_gates(self):
        gates_cor = []
        for cor in gates_cor:
            self.set_of_gates.add(wa.Gate(gm.WALL, *cor, self.number_of_coins/2, self.player))

    def next_level(self):
        return Menu(gm.MENU, self.player)
