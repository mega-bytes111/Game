import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 32)

# Bird properties
bird_x = 50
bird_y = 300
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Score
score = 0
game_over = False


def draw_bird(x, y):
    pygame.draw.circle(screen, BLACK, (x, y), bird_radius)
    pygame.draw.circle(screen, WHITE, (x, y), bird_radius - 3)


def draw_pipes(pipes):
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, SCREEN_HEIGHT - pipe["bottom"]))


def create_pipe():
    top_height = random.randint(50, SCREEN_HEIGHT - pipe_gap - GROUND_HEIGHT - 50)
    bottom_height = top_height + pipe_gap
    return {"x": SCREEN_WIDTH, "top": top_height, "bottom": bottom_height}


def check_collision(bird_y, pipes):
    # Check ground and ceiling
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= SCREEN_HEIGHT - GROUND_HEIGHT:
        return True

    # Check pipes
    for pipe in pipes:
        if bird_x + bird_radius > pipe["x"] and bird_x - bird_radius < pipe["x"] + pipe_width:
            if bird_y - bird_radius < pipe["top"] or bird_y + bird_radius > pipe["bottom"]:
                return True
    return False


def draw_ground():
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))


def draw_text(text, size, x, y, color=BLACK):
    font_obj = pygame.font.SysFont("Arial", size)
    label = font_obj.render(text, True, color)
    screen.blit(label, (x, y))


# Main game loop
while True:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Spacebar for jump
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

        # Restart game
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                bird_y = 300
                bird_velocity = 0
                pipes.clear()
                score = 0
                game_over = False

    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipes movement
        if len(pipes) == 0 or pipes[-1]["x"] < SCREEN_WIDTH - 200:
            pipes.append(create_pipe())

        for pipe in pipes:
            pipe["x"] -= pipe_velocity

        # Remove pipes that go off screen
        pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]

        # Collision check
        if check_collision(bird_y, pipes):
            game_over = True

        # Score update
        for pipe in pipes:
            if pipe["x"] + pipe_width == bird_x:
                score += 1

    # Draw everything
    draw_bird(bird_x, int(bird_y))
    draw_pipes(pipes)
    draw_ground()
    draw_text(f"Score: {score}", 32, 10, 10)

    if game_over:
        draw_text("GAME OVER", 50, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 50, (200, 0, 0))
        draw_text("Press R to Restart", 28, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2, (0, 0, 0))

    pygame.display.update()
    clock.tick(FPS)
