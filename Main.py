"""
    @author: TangSan
    This is a game that is used to help practice for League of Legends. Specifically, it is used to help someone train
    their ability to kite and mouse control.
"""

import pygame.mouse as mouse
import pygame.sprite as sprite
from model.model import *
from model.camera import *
import random


# Defining constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720


def main():
    """ Main function for the game. """
    pygame.init()

    # Set the width and height of the screen [width,height]
    screen_size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("My Game")
    bgImg = pygame.image.load("grid-background.png").convert()
    #Image size is 1920 x 1080
    screen_offset = [(SCREEN_WIDTH - bgImg.get_width())/2, (SCREEN_HEIGHT - bgImg.get_height())/2]
    screen.blit(bgImg, screen_offset)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    all_sprites_list = sprite.Group()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 500, 6)
    all_sprites_list.add(player)

    enemy = Enemy(0, 0, 1, player)
    all_sprites_list.add(enemy)
    enemy_sprite_list = sprite.Group()
    enemy_sprite_list.add(enemy)

    bullet_list = sprite.Group()
    attack_move_pressed = False

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if mouse.get_pressed()[2]:
                    # If an enemy sprite was clicked on
                    if enemy_sprite_list.sprites()[0].rect.collidepoint(x, y):
                        if not player.attack(enemy_sprite_list.sprites()[0], all_sprites_list, bullet_list):
                            player.update_move([x, y])
                    else:
                        player.update_move([x, y])
                elif mouse.get_pressed()[0]:
                    if attack_move_pressed:
                        # Attack the closest enemy in attack range otherwise continue
                        can_attack = closestSprite(enemy_sprite_list, mouse.get_pos(), player.range)
                        if can_attack is not None:
                            player.attack(can_attack, all_sprites_list, bullet_list)
                        else:
                            player.update_move([x, y])
                # Reset attack move
                attack_move_pressed = False

            if event.type == pygame.KEYDOWN:
                # Attack move
                if event.key == pygame.K_a:
                    attack_move_pressed = True

                # Center camera
                if event.key == pygame.K_SPACE:
                    centerCamera(player, all_sprites_list, screen_size, screen_offset)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        # Game Logic
        mouseAtScreenEdge = isMouseAtScreenEdge(screen_size, mouse.get_pos())
        if mouseAtScreenEdge is not 0:
            moveCamera(all_sprites_list, screen_size, screen_offset, mouseAtScreenEdge)

        all_sprites_list.update()

        # Calculate mechanics for each bullet
        for enemy in enemy_sprite_list:
            # See if it gets hit by a bullet
            enemy_hit_list = sprite.spritecollide(enemy, bullet_list, True)

            # Remove bullet when it hits enemy
            for i in range(len(enemy_hit_list)):
                enemy.hp -= 1
                if enemy.hp == 0:
                    enemy.kill()
                    new_enemy = Enemy(random.randrange(1, SCREEN_WIDTH), random.randrange(1, SCREEN_HEIGHT),
                                            1, player)
                    enemy_sprite_list.add(new_enemy)
                    all_sprites_list.add(new_enemy)
                    break

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        screen.blit(bgImg, screen_offset)

        all_sprites_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 120 frames per second
        clock.tick(120)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == "__main__":
    main()
