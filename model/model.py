"""
    @author: TangSan
    This file contains implementations of the classes for the game.
"""

import pygame
from math import sqrt, fabs

from pygame.sprite import Sprite

GREEN = (0, 255, 0)  # player color
RED = (255, 0, 0)  # Enemy color
BROWN = (152, 80, 60)  # Bullet color


def determine_direction(start_x, start_y, end_x, end_y):
    """
    Determines the unit vector direction for a sprite to move in
    :param start_x:
    :param start_y:
    :param end_x:
    :param end_y:
    :return: unit vector of the direction
    """
    x_direction = end_x - start_x
    y_direction = end_y - start_y
    magnitude = sqrt(x_direction ** 2 + y_direction ** 2)
    if magnitude == 0:
        return 0, 0
    unit_x = x_direction / magnitude
    unit_y = y_direction / magnitude
    assert (fabs(sqrt(unit_x ** 2 + unit_y ** 2) - 1) < 0.01)
    return unit_x, unit_y


class Champion(Sprite):
    def __init__(self, start_x, start_y, move_speed):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()

        self.move_speed = move_speed

        # Set height, width
        self.image = pygame.Surface([40, 40])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.centerx = start_x
        self.rect.centery = start_y

        # Attributes to keep track of sprite's "real" position as rect.x and rect.y are kept as ints and
        # inconvenient rounding occurs
        self.real_x = start_x
        self.real_y = start_y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # Make destination current position
        self.x_destination = start_x
        self.y_destination = start_y

    def change_direction(self, direction):
        """
        Change the speed of the player
        Direction is an iterable with index 0 corresponding to x unit vector and index 1 corresponding to y unit vector
        """
        self.change_x = self.move_speed * direction[0]
        self.change_y = self.move_speed * direction[1]
        # assert(fabs(sqrt(self.change_x**2 + self.change_y**2) - self.move_speed) < 0.5)

    def update(self):
        if fabs(self.real_x-self.x_destination) > 5:
            self.real_x += self.change_x
            self.rect.centerx = self.real_x
        else:
            self.change_x = 0
            self.rect.centerx = self.real_x = self.x_destination

        if fabs(self.real_y-self.y_destination) > 5:
            self.real_y += self.change_y
            self.rect.centery = self.real_y
        else:
            self.change_y = 0
            self.rect.centery = self.real_y = self.y_destination


class Player(Champion):
    """
    This class is the player controlled sprite.
    It is capable of:
        Moving
        Attacking
    """
    def __init__(self, start_x, start_y, attack_range, move_speed):
        super().__init__(start_x, start_y, move_speed)
        # Attack range is radius that player may launch a attack
        self.range = attack_range
        # Set player sprite to be green
        self.image.fill(GREEN)

    def update_move(self, pos):
        self.x_destination = pos[0]
        self.y_destination = pos[1]
        self.change_direction(determine_direction(self.rect.centerx, self.rect.centery, pos[0], pos[1]))

    def stop(self):
        # Stopping movement
        self.x_destination = self.rect.x
        self.y_destination = self.rect.y
        self.change_x = 0
        self.change_y = 0

    def attack(self, enemy, sprite_list, bullet_list):
        # Stop
        self.stop()

        # Shoot bullet
        shot = Bullet(self, enemy)
        sprite_list.add(shot)
        bullet_list.add(shot)

    def attackable(self, enemy_sprite_list):
        closest_distance = self.range
        closest_enemy = None
        for enemy in enemy_sprite_list:
            x_dist = self.rect.centerx - enemy.rect.centerx
            y_dist = self.rect.centery - enemy.rect.centery
            dist = sqrt(x_dist**2 + y_dist**2)
            if dist < closest_distance:
                closest_enemy = enemy
        return closest_enemy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, enemy):
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()

        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.real_x = self.rect.centerx
        self.real_y = self.rect.centery
        # speed of the bullet
        self.speed = 15

        self.target = enemy

        # Destination of the bullet is always
        # self.x_destination = enemy.rect.centerx
        # self.y_destination = enemy.rect.centery

        self.change_x = 0
        self.change_y = 0

    def change_direction(self, direction):
        """
        Change the speed of the bullet to ensure it is always travelling towards the enemy
        Direction is an iterable with index 0 corresponding to x unit vector and index 1 corresponding to y unit vector
        """
        self.change_x = self.speed * direction[0]
        self.change_y = self.speed * direction[1]

    def update_move(self):
        self.change_direction(determine_direction(self.rect.centerx, self.rect.centery, self.target.rect.centerx,
                                                  self.target.rect.centery))

    def update(self):
        self.update_move()

        if fabs(self.real_x-self.target.rect.centerx) > 10:
            self.real_x += self.change_x
            self.rect.centerx = self.real_x
        else:
            self.change_x = 0
            self.rect.centerx = self.real_x = self.target.rect.centerx

        if fabs(self.real_y-self.target.rect.centery) > 10:
            self.real_y += self.change_y
            self.rect.centery = self.real_y
        else:
            self.change_y = 0
            self.rect.centery = self.real_y = self.target.rect.centery


class Enemy(Champion):
    def __init__(self, start_x, start_y, move_speed, target):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__(start_x, start_y, move_speed)

        # Make the enemy red colored
        self.image.fill(RED)
        # Assign the enemy a target to pursue
        self.target = target
        # Health
        self.hp = 5

    def update_move(self):
        self.x_destination = self.target.rect.centerx
        self.y_destination = self.target.rect.centery
        self.change_direction()

