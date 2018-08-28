"""
    @author: TangSan
    This is a game that is used to help practice for League of Legends. Specifically, it is used to help someone train
    their ability to kite and mouse control.
"""

import pygame
import model.model
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
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    all_sprites_list = pygame.sprite.Group()

    player = model.model.Player(20, 20, 500, 6)
    all_sprites_list.add(player)

    enemy = model.model.Enemy(200, 200, 4, player)
    all_sprites_list.add(enemy)
    enemy_sprite_list = pygame.sprite.Group()
    enemy_sprite_list.add(enemy)

    bullet_list = pygame.sprite.Group()

    # -------- Main Program Loop -----------
    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    player.update_move(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # Attack the closest enemy in attack range otherwise continue
                    can_attack = player.attackable(enemy_sprite_list)
                    if can_attack is not None:
                        player.attack(can_attack, all_sprites_list, bullet_list)

            # Clicking on an enemy to attack
            # elif pygame.mouse.get_pressed()[0]:
            #     # If an enemy gets clicked on
            #     if True:
            #         player.attack(enemy, all_sprites_list, bullet_list)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        # Game Logic
        all_sprites_list.update()

        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hit a block
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_sprite_list, True)

            # Remove bullet when it hits enemy
            for i in range(len(enemy_hit_list)):
                bullet.kill()
                new_enemy = model.model.Enemy(random.randrange(1, SCREEN_WIDTH), random.randrange(1, SCREEN_HEIGHT), 4,
                                              player)
                enemy_sprite_list.add(new_enemy)
                all_sprites_list.add(new_enemy)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)

        all_sprites_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == "__main__":
    main()
