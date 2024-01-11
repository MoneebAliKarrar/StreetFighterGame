"""
Street Fighter Game

A simple 2D fighting game implemented using the Pygame library.

Author: MONEEB ABDALBADIE NASRALLAH ALI KARRAR
Date: 07.01.2024

Controls:
    Player 1:
        - Move Left: 'A'
        - Move Right: 'D'
        - Jump: 'W'
        - Attack: 'X'

    Player 2:
        - Move Left: Left Arrow Key
        - Move Right: Right Arrow Key
        - Jump: Up Arrow Key
        - Attack: Spacebar

"""

import pygame
import sys
from functions import *


def main():
    """
    The main function to initialize and run the Street Fighter game.

    Initializes game components, including background music,
    character actions, and Pygame window,
    and enters the game loop to handle player input,
    character animations, and game state
    """
    warrior_attack_sound, wizard_attack_sound, window, \
        arena, backGround, backGroundRec, warriorActionFramesMap, \
        wizardActionFramesMap = initialize_game()
    gameLoop(
            window, arena, backGround, backGroundRec,
            warriorActionFramesMap, wizardActionFramesMap,
            player1_health, player2_health, p1_is_jumping,
            p2_is_jumping, player1, player2, p1_is_falling,
            p2_is_falling, p1_is_attacking, p2_is_attacking,
            warrior_current_action, wizard_current_action,
            p1_jump_count, p2_jump_count, dead_animation_triggered,
            current_round, player1_rounds_won, player2_rounds_won,
            loser, last_update, dead_animation_frame_counter
            )


if __name__ == "__main__":
    main()
