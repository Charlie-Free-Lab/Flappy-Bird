import pygame
import sys
import random


# Function for moving the floor

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 678))
    screen.blit(floor_surface, (floor_x_pos + 576, 678))


# Function for creating pipes

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos - 700))
    return bottom_pipe, top_pipe


# Function for moving pipes

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


# Function for drawing pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 680:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# Function for collisions

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            game_over_sound.play()
            return False

    if bird_rect.bottom >= 678 or bird_rect.top <= 0:
        game_over_sound.play()
        return False

    return True


# Function for rotating the bird

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


# Function for bird animation

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# Function for displaying the score

def score_display():
    score_surface = game_font.render("SCORE: " + str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rect)


# Function for displaying the high score

def high_score_display():
    global high_score
    global hold
    if high_score < score:
        # if check_score == "Checking"
        high_score = score
        hold = True

    elif hold == True:
        new_high_score_surface = game_font.render("NEW HIGHSCORE!!! " + str(int(high_score)), True, (255, 255, 255))
        new_high_score_rect = new_high_score_surface.get_rect(center=(288, 100))
        screen.blit(new_high_score_surface, new_high_score_rect)

    else:
        high_score_surface = game_font.render("HIGH SCORE: " + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 100))
        screen.blit(high_score_surface, high_score_rect)


# Intializing the pygame module and creating a window

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 768))

# Creating a clock object to control the frame rate

clock = pygame.time.Clock()

# Game font

game_font = pygame.font.Font("C:\Windows\Fonts\BERNHC.TTF", 40)

# Game Variables

gravity = 0.16
bird_movement = 0
game_active = True
score = 0
high_score = 0
hold = False

# Setting the background

bg_surface = pygame.image.load("Flappy_Bird_Items/flappy-bird-assets-master/sprites/background-day.png").convert()

# Scaling the background

bg_surface = pygame.transform.scale(bg_surface, (576, 768))

# Importing the floor

floor_surface = pygame.image.load("Flappy_Bird_Items/flappy-bird-assets-master/sprites/base.png").convert()

# Scaling the floor

floor_surface = pygame.transform.scale(floor_surface, (576, 90))

# Setting the variable for the rate of the floor's movement

floor_x_pos = 0

# Importing the bird

bird_downflap = pygame.image.load(
    "Flappy_Bird_Items/flappy-bird-assets-master/sprites/yellowbird-downflap.png").convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (50, 36))
bird_midflap = pygame.image.load(
    "Flappy_Bird_Items/flappy-bird-assets-master/sprites/yellowbird-midflap.png").convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (50, 36))
bird_upflap = pygame.image.load(
    "Flappy_Bird_Items/flappy-bird-assets-master/sprites/yellowbird-upflap.png").convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (50, 36))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]

bird_rect = bird_surface.get_rect(center=(112, 384))

# Bird animation

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

# Importing the pipe

pipe_surface = pygame.image.load("Flappy_Bird_Items/flappy-bird-assets-master/sprites/pipe-green.png")
pipe_surface = pygame.transform.scale(pipe_surface, (104, 480))

# Pipe Lists

pipe_list = []
pipe_height = [300, 350, 400, 450, 500, 550, 600]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)

# Score lists

score_pipe_list = []

# Game Over Screen

game_over_surface = pygame.image.load("Flappy_Bird_Items/flappy-bird-assets-master/sprites/message.png").convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (285, 400))
game_over_rect = game_over_surface.get_rect(center=(288, 384))

# Flapping sound

flap_sound = pygame.mixer.Sound("Flappy_Bird_Items/flappy-bird-assets-master/audio/wing.wav")

# Game over sound

game_over_sound = pygame.mixer.Sound("Flappy_Bird_Items/flappy-bird-assets-master/audio/hit.wav")

# Score sound

score_sound = pygame.mixer.Sound("Flappy_Bird_Items/flappy-bird-assets-master/audio/point.wav")

# Game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Flapping the bird

            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

            # Restarting the game

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                hold = False
                pipe_list.clear()
                bird_rect.center = 112, 384
                bird_movement = 0
                score = 0
                score_pipe_list.clear()

        # Spawning Pipes

        if event.type == SPAWNPIPE:
            pipe_list.extend(
                create_pipe())  # extend is like append but it adds the elements of the list argument as individual elements

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # Setting the background

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Pipe movement

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Setting the bird

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Pipe collisions

        game_active = check_collision(pipe_list)

        # Displaying the score

        score_display()

    else:
        # Displaying the high score

        high_score_display()

        # Displaying the game over message

        screen.blit(game_over_surface, game_over_rect)

    # Setting the rate of the floor's movement

    floor_x_pos -= 2

    # Setting the floor

    draw_floor()

    # Resetting the floor

    if floor_x_pos == -576:
        floor_x_pos = 0

    # Updating the score

    for pipe in pipe_list:
        if pipe.centerx < bird_rect.centerx and pipe_list.index(pipe) == len(score_pipe_list):
            score_pipe_list.append(pipe)
            score_sound.play()

    score = len(score_pipe_list) / 2

    # Updating the screen each loop iteration

    pygame.display.update()

    # Setting the frame rate

    clock.tick(120)