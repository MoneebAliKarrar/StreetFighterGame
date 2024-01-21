"""
Street Fighter Game

A simple 2D fighting game implemented using the Pygame library.

Author: MONEEB ABDALBADIE NASRALLAH ALI KARRAR
Date: 07.01.2024
This file contains all the function for the game .
"""
import os
import pygame
import sys

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PLAYER_WIDTH = 100
PLAYER_HIGHT = 200
player1 = pygame.Rect(200, 330, PLAYER_WIDTH, PLAYER_HIGHT)
player2 = pygame.Rect(900, 330, PLAYER_WIDTH, PLAYER_HIGHT)
JUMP_HEIGHT = 200
p1_is_jumping = False
p1_is_falling = False
p2_is_jumping = False
p2_is_falling = False
p1_is_attacking = False
p2_is_attacking = False
p1_jump_count = 0
p2_jump_count = 0
p1_got_hit = False
p2_got_hit = False
jump_timer = 0
GRAVITY = 10
PLAYERSPEED = 3
ATTACK_DISTANCE = 170
ATTACK_DAMAGE = 20
JUMPSPEED = 10
actions = ['run', 'jump', 'attack', 'dead', 'fall', 'idle', 'take_hit']
warrior_sheet_paths = ['warriorSprites/Run.png',
                       'warriorSprites/Jump.png',
                       'warriorSprites/Attack2.png',
                       'warriorSprites/Death.png',
                       'warriorSprites/Fall.png',
                       'warriorSprites/Idle.png',
                       'warriorSprites/Takehit.png'
                       ]
warrior_frames_per_action = [8, 3, 7, 7, 3, 10, 3]
warrior_frame_size = (162, 162)
warrior_scale = 5
wizard_sheet_paths = ['wizardSprites/Run.png',
                      'wizardSprites/Jump.png',
                      'wizardSprites/Attack1.png',
                      'wizardSprites/Death.png',
                      'wizardSprites/Fall.png',
                      'wizardSprites/Idle.png',
                      'wizardSprites/Takehit.png'
                      ]
wizard_frames_per_action = [8, 2, 8, 7, 2, 8, 3]
wizard_frame_size = (250, 250)
wizard_scale = 3
warrior_current_action = 'idle'
wizard_current_action = 'idle'
player1_health = 100
player2_health = 100
warrior_frame = 0
wizard_frame = 0
animation_cooldown = 60
player1_rounds_won = 0
player2_rounds_won = 0
current_round = 0
dead_animation_start_time = 0
dead_animation_triggered = False
loser = None
dead_animation_frame_counter = 0
dead_animation_duration = 2000
pygame.mixer.init()
background_music = pygame.mixer.Sound("background.mp3")
warrior_attack_sound = pygame.mixer.Sound("sword.wav")
wizard_attack_sound = pygame.mixer.Sound("magic.wav")
background_music.play(-1)
last_update = pygame.time.get_ticks()


def get_frame(sheet_path, frame_index, frame_size, target_size):
    """
    Load and resize a specific frame from a sprite sheet.

    Args:
        sheet_path (str): Path to the sprite sheet.
        frame_index (int): Index of the frame to be loaded.
        frame_size (tuple):
        Size of each frame in the sprite sheet (width, height).
        target_size (tuple):
        Size to which the frame should be resized (width, height).

    Returns:
        pygame.Surface: Resized frame as a Pygame surface.
    """
    sheet = pygame.image.load(sheet_path).convert_alpha()
    frame_x = frame_index * frame_size[0]
    frame_y = 0
    original_frame = sheet.subsurface(
                                        pygame.Rect(
                                                    frame_x, frame_y,
                                                    frame_size[0],
                                                    frame_size[1]))
    resized_frame = pygame.Surface(target_size, pygame.SRCALPHA)
    resized_frame.blit(pygame.transform.scale(
                                              original_frame,
                                              target_size), (0, 0))

    return resized_frame


def load_frames(sheet_path, num_frames, frame_size, scale):
    """
    Load and resize all frames from a sprite sheet.

    Args:
        sheet_path (str): Path to the sprite sheet.
        num_frames (int): Number of frames in the sprite sheet.
        frame_size (tuple):
        Size of each frame in the sprite sheet (width, height).
        scale (int): Scaling factor for resizing frames.

    Returns:
        list: List of Pygame surfaces representing frames.
    """
    frames = [get_frame(sheet_path,
              i, frame_size,
              (
               frame_size[0]*scale,
               frame_size[1]*scale)
               )for i in range(num_frames)]
    return frames


def create_action_map(
                      actions, sheet_paths_list,
                      frames_per_action, frame_size, scale
                      ):
    """
    Create a dictionary mapping actions to their corresponding frames.

    Args:
        actions (list): List of action names.
        sheet_paths_list (list): List of paths to sprite sheets for each action.
        frames_per_action (list): Number of frames for each action.
        frame_size (tuple):
        Size of each frame in the sprite sheet (width, height).
        scale (int): Scaling factor for resizing frames.

    Returns:
        dict: Dictionary mapping actions to lists of frames.
    """
    action_map = {}
    for action, sheet_path, num_frames in zip(
                                              actions,
                                              sheet_paths_list,
                                              frames_per_action
                                              ):
        frames = load_frames(sheet_path, num_frames, frame_size, scale)
        action_map[action] = frames
    return action_map


def calculate_direction(player1, player2):
    """
    Calculate the direction (left or right) between two players.

    Args:
        player1 (pygame.Rect):
        Rectangle representing the position of the first player.
        player2 (pygame.Rect):
        Rectangle representing the position of the second player.

    Returns:
        int: Direction (1 for right, -1 for left).
    """
    return 1 if player1.x < player2.x else -1


def welcome_screen(screen, screen_rectangle):
    """
    Display the welcome screen.

    Args:
        screen: Pygame window surface.
        screen_rectangle: Rectangle representing the screen dimensions.
    """
    screen.fill(BLACK)
    welcome_font = pygame.font.Font('freesansbold.ttf', 48)
    welcome_text = welcome_font.render(
                                        "Welcome to Street Fighter game!",
                                        True, WHITE
                                        )
    welcome_box = welcome_text.get_rect()
    welcome_box.center = screen_rectangle.center
    screen.blit(welcome_text, welcome_box)

    pygame.display.flip()
    pygame.time.wait(2000)


def goodbye_screen(screen, screen_rectangle):
    """
    Display the goodbye screen.

    Args:
        screen: Pygame window surface.
        screen_rectangle: Rectangle representing the screen dimensions.
    """
    screen.fill(BLACK)
    goodbye_font = pygame.font.Font('freesansbold.ttf', 48)
    goodbye_text = goodbye_font.render(
        "Goodbye! Thanks for playing!", True, WHITE)
    goodbye_box = goodbye_text.get_rect()
    goodbye_box.center = screen_rectangle.center
    screen.blit(goodbye_text, goodbye_box)

    pygame.display.flip()
    pygame.time.wait(2000)


def display_scores(
                   window, current_round, player1_rounds_won,
                   player2_rounds_won
                   ):
    """
    Display current round and player scores.

    Args:
        window: Pygame window surface.
        current_round (int): Current game round.
        player1_rounds_won (int): Number of rounds won by Player 1.
        player2_rounds_won (int): Number of rounds won by Player 2.
    """
    font = pygame.font.Font(None, 36)

    round_text = font.render(f"Round {current_round+1}", True, WHITE)
    player1_score_text = font.render(
                                     f"Player 1 Score: {player1_rounds_won}",
                                     True, WHITE
                                     )
    player2_score_text = font.render(
                                     f"Player 2 Score: {player2_rounds_won}",
                                     True, WHITE
                                     )

    window.blit(round_text, (10, 10))
    window.blit(player1_score_text, (10, 70))
    window.blit(
                player2_score_text,
                (SCREEN_WIDTH - player2_score_text.get_width() - 10, 70)
                )


def handle_events(window, arena):
    """
    Handle Pygame events.

    Args:
        window: Pygame window surface.
        arena: Rectangle representing the game area.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            goodbye_screen(window, arena)
            sys.exit()


def move_player(direction, player, PLAYERSPEED, arena):
    """
    Move the player based on the specified direction.

    Args:
        direction (str): Direction of movement ('right' or 'left').
        player (pygame.Rect): Rectangle representing the player's position.
        PLAYERSPEED (int): Speed of player movement.
        arena: Rectangle representing the game area.

    Returns:
        pygame.Rect: Updated player rectangle after movement.
    """
    if direction == "right":
        player = player.move(PLAYERSPEED, 0)
    elif direction == "left":
        player = player.move(-PLAYERSPEED, 0)
    if player.right > arena.right:
        player.right = arena.right
    elif player.left < arena.left:
        player.left = arena.left
    return player


def jump(
         is_jumping, is_falling, player, JUMP_HEIGHT,
         JUMPSPEED, GRAVITY, jump_count
         ):
    """
    Handle player jumping and falling.

    Args:
        is_jumping (bool): Whether the player is currently jumping.
        is_falling (bool): Whether the player is currently falling.
        player (pygame.Rect): Rectangle representing the player's position.
        JUMP_HEIGHT (int): Maximum height the player can jump.
        JUMPSPEED (int): Speed at which the player jumps.
        GRAVITY (int): Gravity affecting the player's fall.
        jump_count (int): Counter for tracking jump progress.

    Returns:
        tuple: Updated state of jumping, falling, player, and jump count.
    """
    if is_jumping:
        if jump_count < JUMP_HEIGHT:
            player.y -= JUMPSPEED
            jump_count += JUMPSPEED
        else:
            is_jumping = False
            is_falling = True

    if not is_jumping and player.y < 330:
        player.y += GRAVITY
    elif not is_jumping and player.y >= 0:
        jump_count = 0
        is_falling = False
    return is_jumping, is_falling, player, jump_count


def draw_bars(
              window, player1_health, player2_health,
              bar_width=550, bar_height=20
              ):
    """
    Draw health bars for both players on the window.

    Args:
        window: Pygame window surface.
        player1_health (int): Health of Player 1.
        player2_health (int): Health of Player 2.
        bar_width (int): Width of the health bars.
        bar_height (int): Height of the health bars.
    """
    player1_bar_rect = pygame.Rect(50, 50, bar_width, bar_height)
    player2_bar_rect = pygame.Rect(
                                   SCREEN_WIDTH - bar_width - 50,
                                   50, bar_width, bar_height
                                   )
    pygame.draw.rect(window, RED, player1_bar_rect)
    pygame.draw.rect(window, WHITE, player1_bar_rect, 2)

    pygame.draw.rect(window, BLUE, player2_bar_rect)
    pygame.draw.rect(window, WHITE, player2_bar_rect, 2)

    player1_fill_rect = pygame.Rect(
                                    player1_bar_rect.left,
                                    player1_bar_rect.top,
                                    int(bar_width * (player1_health / 100)),
                                    bar_height
                                    )
    player2_fill_rect = pygame.Rect(
        player2_bar_rect.left + int(bar_width * ((100 - player2_health) / 100)),
        player2_bar_rect.top, bar_width - int(
            bar_width * ((100 - player2_health) / 100)
            ),
        bar_height
        )

    pygame.draw.rect(window, GREEN, player1_fill_rect)
    pygame.draw.rect(window, GREEN, player2_fill_rect)


def display_winning_screen(message, window):
    """
    Display the winning screen with the specified message.

    Args:
        message (str): Message to be displayed on the winning screen.
        window: Pygame window surface.
    """
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    window.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def reset_game(
               current_round, player1_x, player2_x,
               warrior_current_action, wizard_current_action,
               p1_got_hit, p2_got_hit
               ):
    """
    Reset game-related variables for a new round.

    Args:
        current_round (int): Current game round.
        player1_x (int): Initial x-coordinate for Player 1.
        player2_x (int): Initial x-coordinate for Player 2.
        warrior_current_action (str): Current action for the warrior.
        wizard_current_action (str): Current action for the wizard.
        p1_got_hit (bool): Whether Player 1 got hit in the previous round.
        p2_got_hit (bool): Whether Player 2 got hit in the previous round.

    Returns:
        tuple:
        Updated values for player health, current round,
        player positions, and action states.
    """
    player1_x = 200
    player2_x = 900
    player1_health = 100
    player2_health = 100
    current_round += 1
    warrior_current_action = 'idle'
    wizard_current_action = 'idle'
    p1_got_hit = False
    p2_got_hit = False
    return player1_health, player2_health, current_round, player1_x, \
        player2_x, warrior_current_action, wizard_current_action, \
        p1_got_hit, p2_got_hit


def handle_player1_input(
                         arena, warriorActionFramesMap, player2_health,
                         p1_is_jumping, player1, p1_is_falling,
                         p1_is_attacking, p2_is_jumping, p2_is_falling,
                         player2, warrior_current_action
                         ):
    """
    Handle player input and update game state for Player 1.

    Args:
        arena (pygame.Rect): The game arena rectangle.
        warriorActionFramesMap (dict):
        Dictionary mapping warrior actions to corresponding frames.
        player2_health (int): Health of Player 2.
        p1_is_jumping (bool): Whether Player 1 is currently jumping.
        player1 (pygame.Rect): Player 1 rectangle.
        p1_is_falling (bool): Whether Player 1 is currently falling.
        p1_is_attacking (bool): Whether Player 1 is currently attacking.
        p2_is_jumping (bool): Whether Player 2 is currently jumping.
        p2_is_falling (bool): Whether Player 2 is currently falling.
        player2 (pygame.Rect): Player 2 rectangle.
        warrior_current_action (str): Current action for the warrior.

    Returns:
        tuple: Updated values for warrior action, hit status,
        Player 2 health, jumping/falling states, and player positions.
    """
    keys = pygame.key.get_pressed()
    global p2_got_hit, warrior_frame, last_update, wizard_frame
    if keys[pygame.K_a] and not p1_is_attacking:
        player1 = move_player("left", player1, PLAYERSPEED, arena)
        warrior_current_action = 'run'
    elif keys[pygame.K_d] and not p1_is_attacking:
        player1 = move_player("right", player1, PLAYERSPEED, arena)
        warrior_current_action = 'run'
    elif keys[pygame.K_w] and not p1_is_jumping and not p1_is_attacking:
        p1_is_jumping = True
        warrior_current_action = 'jump'
    elif keys[pygame.K_x] and not p1_is_attacking and \
            not p1_is_falling and not p1_is_jumping:
        warrior_attack_sound.play()
        p1_is_attacking = True
        warrior_frame = 0
        warrior_current_action = 'attack'
        if abs(player1.x-player2.x) < ATTACK_DISTANCE and \
                not p2_is_jumping and not p2_is_falling:
            p2_got_hit = True
            player2_health -= ATTACK_DAMAGE
    elif p1_got_hit:
        warrior_current_action = 'take_hit'
    elif not keys[pygame.K_w] and p1_is_falling and not p1_is_attacking:
        warrior_current_action = 'fall'
    elif not keys[pygame.K_w] and not keys[pygame.K_x] and \
            not p1_is_jumping and not p1_is_attacking:
        p1_is_jumping = False
        warrior_current_action = 'idle'
    elif p1_is_attacking and \
            warrior_frame >= len(warriorActionFramesMap['attack'])-1:
        p1_is_attacking = False
        warrior_current_action = 'idle'
        p2_got_hit = False
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        warrior_frame += 1
        wizard_frame += 1
        last_update = current_time
    if warrior_frame >= len(warriorActionFramesMap[warrior_current_action]):
        warrior_frame = 0
    return warrior_current_action, p2_got_hit, player2_health, \
        p1_is_jumping, p1_is_falling, player1, p1_is_attacking, warrior_frame


def handle_player2_input(
                         arena, wizardActionFramesMap, player1_health,
                         p2_is_jumping, player2, p2_is_falling,
                         p2_is_attacking, p1_is_jumping, p1_is_falling,
                         player1, wizard_current_action
                         ):
    """
    Handle player input and update game state for Player 2.

    Args:
        arena (pygame.Rect): The game arena rectangle.
        wizardActionFramesMap (dict):
        Dictionary mapping wizard actions to corresponding frames.
        player1_health (int): Health of Player 1.
        p2_is_jumping (bool): Whether Player 2 is currently jumping.
        player2 (pygame.Rect): Player 2 rectangle.
        p2_is_falling (bool): Whether Player 2 is currently falling.
        p2_is_attacking (bool): Whether Player 2 is currently attacking.
        p1_is_jumping (bool): Whether Player 1 is currently jumping.
        p1_is_falling (bool): Whether Player 1 is currently falling.
        player1 (pygame.Rect): Player 1 rectangle.
        wizard_current_action (str): Current action for the wizard.

    Returns:
        tuple: Updated values for wizard action, hit status,
        Player 1 health, jumping/falling states, and player positions.
    """
    keys = pygame.key.get_pressed()
    global p1_got_hit, wizard_frame, last_update
    if keys[pygame.K_LEFT] and not p2_is_attacking:
        player2 = move_player("left", player2, PLAYERSPEED, arena)
        wizard_current_action = 'run'
    elif keys[pygame.K_RIGHT] and not p2_is_attacking:
        player2 = move_player("right", player2, PLAYERSPEED, arena)
        wizard_current_action = 'run'
    elif keys[pygame.K_UP] and not p2_is_jumping and not p2_is_attacking:
        p2_is_jumping = True
        wizard_current_action = 'jump'
    elif keys[pygame.K_SPACE] and not p2_is_attacking and \
            not p2_is_falling and not p2_is_jumping:
        wizard_attack_sound.play()
        p2_is_attacking = True
        wizard_frame = 0
        wizard_current_action = 'attack'
        if abs(player1.x-player2.x) < ATTACK_DISTANCE and \
                not p1_is_jumping and not p1_is_falling:
            p1_got_hit = True
            player1_health -= ATTACK_DAMAGE
    elif p2_got_hit:
        wizard_current_action = 'take_hit'
    elif not keys[pygame.K_UP] and p2_is_falling and not p2_is_attacking:
        wizard_current_action = 'fall'
    elif not keys[pygame.K_UP] and not keys[pygame.K_SPACE] and \
            not p2_is_jumping and not p2_is_attacking:
        p2_is_jumping = False
        wizard_current_action = 'idle'
    elif p2_is_attacking and \
            wizard_frame >= len(wizardActionFramesMap['attack'])-1:
        p1_got_hit = False
        p2_is_attacking = False
        wizard_current_action = 'idle'
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        wizard_frame += 1
        last_update = current_time
    if wizard_frame >= len(wizardActionFramesMap[wizard_current_action]):
        wizard_frame = 0
    return wizard_current_action, p1_got_hit, player1_health, \
        p2_is_jumping, p2_is_falling, player2, p2_is_attacking, wizard_frame


def handleDirection(
                    warrior_frame_to_draw, wizard_frame_to_draw,
                    player1, player2
                    ):
    """
    Flip the player character frames based on their facing direction.

    Args:
        warrior_frame_to_draw (pygame.Surface):
         Frame of the warrior character to be drawn.
        wizard_frame_to_draw (pygame.Surface):
         Frame of the wizard character to be drawn.
        player1 (pygame.Rect): Player 1 rectangle.
        player2 (pygame.Rect): Player 2 rectangle.

    Returns:
        tuple: Updated frames of the warrior and wizard
        characters based on their facing direction.
    """
    warrior_direction = calculate_direction(player1, player2)
    wizard_direction = calculate_direction(player2, player1)
    if warrior_direction == -1:
        warrior_frame_to_draw = pygame.transform.flip(
                                                      warrior_frame_to_draw,
                                                      True, False
                                                      )

    if wizard_direction == -1:
        wizard_frame_to_draw = pygame.transform.flip(
                                                     wizard_frame_to_draw,
                                                     True, False
                                                     )
    return warrior_frame_to_draw, wizard_frame_to_draw


def initialize_game():
    """
    Initialize the Pygame window, background music, and character action frames.

    Returns:
        Pygame window,
               game arena rectangle, background image, background rectangle,
               warrior action frames map, and wizard action frames map.
    """
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    arena = window.get_rect()
    backGround = pygame.image.load("stage.jpg")
    backGroundRec = backGround.get_rect()

    warriorActionFramesMap = create_action_map(
                                               actions,
                                               warrior_sheet_paths,
                                               warrior_frames_per_action,
                                               warrior_frame_size,
                                               warrior_scale
                                               )
    wizardActionFramesMap = create_action_map(
                                              actions,
                                              wizard_sheet_paths,
                                              wizard_frames_per_action,
                                              wizard_frame_size,
                                              wizard_scale
                                              )
    return window, arena, \
        backGround, backGroundRec, warriorActionFramesMap, wizardActionFramesMap


def gameLoop(
             window, arena, backGround, backGroundRec,
             warriorActionFramesMap, wizardActionFramesMap,
             player1_health, player2_health, p1_is_jumping,
             p2_is_jumping, player1, player2, p1_is_falling,
             p2_is_falling, p1_is_attacking, p2_is_attacking,
             warrior_current_action, wizard_current_action,
             p1_jump_count, p2_jump_count, dead_animation_triggered,
             current_round, player1_rounds_won, player2_rounds_won,
             loser, last_update, dead_animation_frame_counter,
             dead_animation_start_time
             ):
    """
    Main game loop.

    Args:
        window (pygame.Surface): Pygame window.
        arena (pygame.Rect): Rectangle representing the game area.
        backGround (pygame.Surface): Background image.
        backGroundRec (pygame.Rect): Rectangle representing
        the background image position.
        warriorActionFramesMap (dict): Dictionary mapping
        warrior actions to frames.
        wizardActionFramesMap (dict): Dictionary mapping wizard
        actions to frames.
        player1_health (int): Player 1's health.
        player2_health (int): Player 2's health.
        p1_is_jumping (bool): Whether Player 1 is jumping.
        p2_is_jumping (bool): Whether Player 2 is jumping.
        player1 (pygame.Rect): Rectangle representing Player 1's position.
        player2 (pygame.Rect): Rectangle representing Player 2's position.
        p1_is_falling (bool): Whether Player 1 is falling.
        p2_is_falling (bool): Whether Player 2 is falling.
        p1_is_attacking (bool): Whether Player 1 is attacking.
        p2_is_attacking (bool): Whether Player 2 is attacking.
        warrior_current_action (str): Current action for the warrior.
        wizard_current_action (str): Current action for the wizard.
        p1_jump_count (int): Counter for Player 1's jump progress.
        p2_jump_count (int): Counter for Player 2's jump progress.
        dead_animation_triggered (bool): Whether the dead animation
        is triggered.
        current_round (int): Current game round.
        player1_rounds_won (int): Number of rounds won by Player 1.
        player2_rounds_won (int): Number of rounds won by Player 2.
        loser (str): Player who lost the game.
        last_update (int): Timestamp of the last animation update.
        dead_animation_frame_counter (int): Counter for dead animation frames.
        dead_animation_start_time (int): Timestamp when the dead
        animation was triggered.
    """
    fpsClock = pygame.time.Clock()
    welcome_screen(window, arena)
    while True:
        handle_events(window, arena)
        warrior_current_action, p2_got_hit, player2_health, \
            p1_is_jumping, p1_is_falling, player1, p1_is_attacking, \
            warrior_frame = handle_player1_input(
                                                 arena,
                                                 warriorActionFramesMap,
                                                 player2_health, p1_is_jumping,
                                                 player1, p1_is_falling,
                                                 p1_is_attacking, p2_is_jumping,
                                                 p2_is_falling, player2,
                                                 warrior_current_action
                                                 )
        p1_is_jumping, p1_is_falling, \
            player1, p1_jump_count = jump(
                                          p1_is_jumping, p1_is_falling,
                                          player1, JUMP_HEIGHT,
                                          JUMPSPEED, GRAVITY,
                                          p1_jump_count
                                          )
        wizard_current_action, p1_got_hit, \
            player1_health, p2_is_jumping, p2_is_falling, \
            player2, p2_is_attacking, \
            wizard_frame = handle_player2_input(
                                                arena,
                                                wizardActionFramesMap,
                                                player1_health,
                                                p2_is_jumping, player2,
                                                p2_is_falling, p2_is_attacking,
                                                p1_is_jumping, p1_is_falling,
                                                player1, wizard_current_action
                                                )
        p2_is_jumping, p2_is_falling, \
            player2, p2_jump_count = jump(
                                          p2_is_jumping, p2_is_falling,
                                          player2, JUMP_HEIGHT,
                                          JUMPSPEED, GRAVITY,
                                          p2_jump_count
                                          )
        window.blit(backGround, backGroundRec)
        warrior_frame_to_draw, \
            wizard_frame_to_draw = \
            get_player_frames_to_draw(
                                     warriorActionFramesMap,
                                     wizardActionFramesMap,
                                     warrior_current_action,
                                     wizard_current_action,
                                     warrior_frame, wizard_frame,
                                     player1, player2
                                     )
        if not dead_animation_triggered:
            window.blit(warrior_frame_to_draw, (player1.x-350, player1.y-300))
            window.blit(wizard_frame_to_draw, (player2.x-320, player2.y-300))
        display_scores(
                       window, current_round,
                       player1_rounds_won, player2_rounds_won
                       )
        draw_bars(window, player1_health, player2_health)

        player1_health, player2_health, player1_rounds_won, \
            player2_rounds_won, current_round, \
            warrior_current_action, wizard_current_action, \
            p1_got_hit, \
            p2_got_hit = handle_round_end(
                                          window, player1_health,
                                          player2_health, current_round,
                                          player1, player2,
                                          warrior_current_action,
                                          wizard_current_action,
                                          p1_got_hit, p2_got_hit,
                                          player1_rounds_won,
                                          player2_rounds_won
                                          )

        if current_round == 3 and not dead_animation_triggered:
            if player1_rounds_won > player2_rounds_won:
                loser = 'player2'
            elif player2_rounds_won > player1_rounds_won:
                loser = 'player1'
            dead_animation_start_time = pygame.time.get_ticks()
            dead_animation_triggered = True
        if dead_animation_triggered:
            dead_animation_current_time = \
                    pygame.time.get_ticks() - dead_animation_start_time
            if dead_animation_current_time < dead_animation_duration:
                if pygame.time.get_ticks() - last_update >= animation_cooldown:
                    dead_animation_frame_counter += 1
                    last_update = pygame.time.get_ticks()
                if loser == 'player1':
                    if dead_animation_frame_counter < \
                            len(wizardActionFramesMap['dead']):
                        window.blit(
                            warriorActionFramesMap['dead'][
                                dead_animation_frame_counter
                                ],
                            (player1.x - 350, player1.y - 300)
                            )
                elif loser == 'player2':
                    if dead_animation_frame_counter < \
                            len(wizardActionFramesMap['dead']):
                        window.blit(
                            wizardActionFramesMap['dead'][
                                dead_animation_frame_counter
                                ],
                            (player2.x - 320, player2.y - 300)
                            )
            else:
                dead_animation_triggered = False
                if loser == 'player2':
                    display_winning_screen("Player 1 Wins the Game!", window)
                elif loser == 'player1':
                    display_winning_screen("Player 2 Wins the Game!", window)
                goodbye_screen(window, arena)
                sys.exit()
        else:
            if loser == 'player1':
                window.blit(
                            warriorActionFramesMap[
                                                   warrior_current_action
                                                   ][warrior_frame],
                            (player1.x - 350, player1.y - 300)
                            )
            elif loser == 'player2':
                window.blit(
                            wizardActionFramesMap[
                                                  wizard_current_action
                                                  ][wizard_frame],
                            (player2.x - 320, player2.y - 300))
        pygame.display.flip()
        fpsClock.tick(100)


def get_player_frames_to_draw(
                              warriorActionFramesMap, wizardActionFramesMap,
                              warrior_current_action, wizard_current_action,
                              warrior_frame, wizard_frame,
                              player1, player2
                              ):
    """
    Get the frames to draw for the warrior and wizard players based on their
    current actions and positions.

    Args:
        warriorActionFramesMap (dict): Dictionary mapping
        warrior actions to frames.
        wizardActionFramesMap (dict): Dictionary mapping wizard
        actions to frames.
        warrior_current_action (str): Current action for the warrior.
        wizard_current_action (str): Current action for the wizard.
        warrior_frame (int): Frame index for the warrior's current action.
        wizard_frame (int): Frame index for the wizard's current action.
        player1 (pygame.Rect): Rectangle representing Player 1's position.
        player2 (pygame.Rect): Rectangle representing Player 2's position.

    Returns:
        pygame.Surface, pygame.Surface: Two pygame.Surface objects representing
        the frames to draw for the warrior and wizard players after
        handling their directions.
    """
    warrior_frame_to_draw = warriorActionFramesMap[
                                                       warrior_current_action
                                                       ][warrior_frame]
    wizard_frame_to_draw = wizardActionFramesMap[
                                                    wizard_current_action
                                                    ][wizard_frame]
    warrior_frame_to_draw, \
        wizard_frame_to_draw = handleDirection(
                                                warrior_frame_to_draw,
                                                wizard_frame_to_draw,
                                                player1, player2
                                                )
    return warrior_frame_to_draw, wizard_frame_to_draw


def handle_round_end(
                    window, player1_health, player2_health,
                    current_round, player1, player2,
                    warrior_current_action, wizard_current_action,
                    p1_got_hit, p2_got_hit, player1_rounds_won,
                    player2_rounds_won
                    ):
    """
    Check if the current round has ended and handle the consequences.

    Args:
        window: Pygame window.
        player1_health (int): Player 1's health.
        player2_health (int): Player 2's health.
        current_round (int): Current game round.
        player1 (pygame.Rect): Rectangle representing Player 1's position.
        player2 (pygame.Rect): Rectangle representing Player 2's position.
        warrior_current_action (str): Current action for the warrior.
        wizard_current_action (str): Current action for the wizard.
        p1_got_hit (bool): Whether Player 1 got hit in the current round.
        p2_got_hit (bool): Whether Player 2 got hit in the current round.
        player1_rounds_won (int): Number of rounds won by Player 1.
        player2_rounds_won (int): Number of rounds won by Player 2.

    Returns:
        int, int, int, int, int, str, str, bool, bool: Updated health,
        rounds won, current round, player positions, and action states
        after handling the round end.
    """
    if player1_health <= 0:
        player2_rounds_won += 1
        player1_health, player2_health, \
            current_round, player1.x, \
            player2.x, warrior_current_action, \
            wizard_current_action, \
            p1_got_hit, p2_got_hit = reset_game(
                                                current_round,
                                                player1.x, player2.x,
                                                warrior_current_action,
                                                wizard_current_action,
                                                p1_got_hit, p2_got_hit
                                                )
        display_winning_screen("Player 2 Wins The Round!", window)
        print(warrior_current_action)
    elif player2_health <= 0:
        player1_rounds_won += 1
        player1_health, player2_health, \
            current_round, player1.x, \
            player2.x, warrior_current_action, \
            wizard_current_action, \
            p1_got_hit, p2_got_hit = reset_game(
                                                current_round,
                                                player1.x, player2.x,
                                                warrior_current_action,
                                                wizard_current_action,
                                                p1_got_hit, p2_got_hit
                                                )
        display_winning_screen("Player 1 Wins The Round!", window)

    return player1_health, player2_health, player1_rounds_won, \
        player2_rounds_won, current_round, warrior_current_action, \
        wizard_current_action, p1_got_hit, p2_got_hit
