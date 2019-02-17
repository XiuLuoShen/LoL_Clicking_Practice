"""
    @author: TangSan
    This file contains functions for controlling the camera.
"""
import pygame.sprite as sprite
from model import *

EDGE_OFFSET  = 40   # mouse needs to be 20 pixels away to cause camera movement
CAMERA_SPEED = 5

def centerCamera(player, all_sprites, screen_size, screen_offset):
    """
    Centers all sprites onto the player
    :param player: sprite to center every other sprite around
    :param all_sprites: list containing all the sprites
    :param screen_size: size of the screen
    :param screen_offset: the background image's current offset in relation to the display
    """
    center_x = screen_size[0]/2
    center_y = screen_size[1]/2
    dx = center_x - player.real_x
    dy = center_y - player.real_y

    for sprite in all_sprites:
        sprite.rect.centerx += dx
        sprite.rect.centery += dy
        if isinstance(sprite, model.Champion) or isinstance(sprite, model.Bullet):
            sprite.real_x += dx
            sprite.real_y += dy
            sprite.x_destination += dx
            sprite.y_destination += dy

    screen_offset[0] += dx
    screen_offset[1] += dy


def isMouseAtScreenEdge(screen_size, mouse_pos):
    """
    :param screen_size: containing size of the screen, (width, height)
    :param mouse_pos: mouse position on the screen (x, y)
    :return: the edge that the mouse is at
    """
    x_offset_left = mouse_pos[0]    # distance from left of the screen
    x_offset_right = screen_size[0] - mouse_pos[0]  # distance from right of the screen
    y_offset_top = mouse_pos[1]     # distance from top of screen
    y_offset_bot = screen_size[1] - mouse_pos[1]    # distance from bottom of screen

    if 0 <= x_offset_left <= EDGE_OFFSET:
        return 1
    elif 0 <= x_offset_right <= EDGE_OFFSET:
        return 2
    elif 0 <= y_offset_bot <= EDGE_OFFSET:
        return 3
    elif 0 <= y_offset_top <= EDGE_OFFSET:
        return 4
    else:
        return 0

def moveCamera(all_sprites, screen_size, screen_offset, edge):
    if edge == 1 or edge == 2:
        if edge == 1:
            dx = CAMERA_SPEED
        else:
            dx = -CAMERA_SPEED
        for sprite in all_sprites:
            sprite.rect.centerx += dx
            if isinstance(sprite, model.Champion) or isinstance(sprite, model.Bullet):
                sprite.real_x += dx
                sprite.x_destination += dx

        screen_offset[0] += dx

    if edge == 3 or edge == 4:
        if edge == 3:
            dy = -CAMERA_SPEED
        else:
            dy = CAMERA_SPEED
        for sprite in all_sprites:
            sprite.rect.centery += dy
            if isinstance(sprite, model.Champion) or isinstance(sprite, model.Bullet):
                sprite.real_y += dy
                sprite.y_destination += dy

        screen_offset[1] += dy
