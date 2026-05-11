#Fruit Blaster

import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Blaster")

running = True
game_speed = 3 
number_of_items = 2 
last_update_time = pygame.time.get_ticks()
isAlive = False 

fruits = []
pebbles = []

slingshot_img  = pygame.image.load("assets/slingshot.jpeg")
fruit_image = pygame.image.load("assets/apple.jpg")
pebble_image = pygame.image.load("assets/pebble.png")

blaster_sound = pygame.mixer.Sound("assets/blaster.wav")
show_game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")

font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 80)

# Saving and loading highscore
def get_highscore():
    try:
        with open("assets/highscore1.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_highscore():
    with open("assets/highscore1.txt", "w") as file:
        file.write(str(score))

score = 0
highscore = get_highscore()
lives = 5

player_width, player_height = 60, 60
player_x = (WIDTH - player_width) // 2
player_y = (HEIGHT - player_height) // 1.5

clock = pygame.time.Clock()
player_img = pygame.transform.scale(slingshot_img, (player_width, player_height))
#Functions for player stuff
def draw_player():
    global player_x, player_y, player_img 
    screen.blit(player_img, (player_x, player_y))
    
def handle_movement():
    global player_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 8
    if keys[pygame.K_RIGHT]:
        player_x += 8

    player_x = max(0, min(WIDTH - player_width, player_x))

# Functions for fruit handling
def create_fruits():
    fruit_width = 30
    fruit_height = 30
    x = random.randint(0, WIDTH - fruit_width)
    y = -fruit_height
    img = pygame.transform.scale(fruit_image, (fruit_width, fruit_height))
    fruits.append({"x": x, "y": y, "img": img, "width": fruit_width, "height": fruit_height})

def update_fruits():
    global lives, isAlive
    for fruit in fruits:
        fruit["y"] += game_speed
        if fruit["y"] > HEIGHT:
            fruits.remove(fruit)
            lives -= 1
            if lives <= 0:
                show_game_over_sound.play()
                pygame.time.delay(2000)
                isAlive = False
 
def draw_fruits():
    for fruit in fruits:
        screen.blit(fruit["img"], (fruit["x"], fruit["y"]))


def create_pebble():
    keys = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:

        if keys[pygame.K_SPACE]:
            pebble_width = 10
            pebble_height = 20
            x = player_x + (player_width - pebble_width) // 2
            y = player_y - pebble_height
            img = pygame.transform.scale(pebble_image, (pebble_width, pebble_height))
            pebbles.append({"x": x, "y": y, "img": img, "width": pebble_width, "height": pebble_height})

def update_pebbles():
    for pebble in pebbles:
        pebble["y"] -= game_speed
        if pebble["y"] < 0:
            pebbles.remove(pebble)

def draw_pebbles():
    for pebble in pebbles:
        screen.blit(pebble["img"], (pebble["x"], pebble["y"]))
        

# Function to check for collisions between pebbles and fruits
def check_collisions():
    global score, highscore, lives
    for pebble in pebbles:  
        pebble_rect = pygame.Rect(pebble["x"], pebble["y"], pebble["width"], pebble["height"])
        for fruit in fruits: 
            fruit_rect = pygame.Rect(fruit["x"], fruit["y"], fruit["width"], fruit["height"])
            if pebble_rect.colliderect(fruit_rect):
                 pebbles.remove(pebble)
                 fruits.remove(fruit)
                 score += 1
                 if score > highscore:
                    highscore = score
                    save_highscore()
            
#Function to draw the panel at the top of the screen for score and highscore
                
def draw_panel():
    panel_height = 50
    panel_color = (50, 50, 50)
    text_color = (255, 255, 255)

    pygame.draw.rect(screen, panel_color, (0, 0, WIDTH, panel_height))

    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (10, 10))
 
    highscore_text = font.render(f"Highscore: {highscore}", True, text_color)
    screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 10, 10))

    lives_text = font.render(f"Lives: {lives}", True, text_color)
    screen.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, 10))
# Function to increase the difficulty of the game
def increase_difficulty():
    global game_speed, last_update_time, number_of_items
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time > 8000:  # Increase speed every 7 seconds
        game_speed += 1
        last_update_time = current_time

#Function for game over screen
def show_game_over_screen():
    screen.fill((30, 30, 30))
    game_over_text = font.render("Game Over! Press 'R' to restart OR 'ESC' to go back to Main Menu", True, (255, 0, 0))
    final_score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    highscore_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 30))
    screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()


#Main Menu

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=20)
    txt_surface = font.render(text, True, (255, 255, 255))
    screen.blit(txt_surface, (
        rect.centerx - txt_surface.get_width() // 2,
        rect.centery - txt_surface.get_height() // 2
    ))

def display_start_screen():
    global isAlive, score, game_speed, fruits, player_x, player_y, last_update_time, running 

    screen.fill((140, 50, 80))
    title_text = title_font.render("Fruit Blaster", True, (255, 255, 255))

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    
    play_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 50, 150, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50)

    draw_button(play_button, "Play", (0, 200, 0))
    draw_button(quit_button, "Quit", (255, 0, 0))

    high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, HEIGHT // 2 + 100))

    mouse_pos, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    if click[0]:  # Left click
        if play_button.collidepoint(mouse_pos):
            isAlive, score, game_speed = True, 0, 3
            fruits.clear()
            player_x = (WIDTH - player_width) // 2
            player_y = (HEIGHT - player_width) // 1.5
            last_update_time = pygame.time.get_ticks()
    
        elif quit_button.collidepoint(mouse_pos):
            running = False

#Main loop for the game
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                pebble_width = 10
                pebble_height = 20
                x = player_x + (player_width - pebble_width) // 2
                y = player_y - pebble_height
                img = pygame.transform.scale(pebble_image, (pebble_width, pebble_height))
                pebbles.append({"x": x, "y": y, "img": img, "width": pebble_width, "height": pebble_height})
                blaster_sound.play()
            elif event.key == pygame.K_r and not isAlive:
                isAlive = True
                score = 0
                lives = 3
                fruits.clear()
                pebbles.clear()
                player_x = (WIDTH - player_width) // 2
                player_y = (HEIGHT - player_height) // 1.5
                last_update_time = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE and not isAlive:

                score = 0
                lives = 3
                fruits.clear()
                pebbles.clear()
                player_x = (WIDTH - player_width) // 2
                player_y = (HEIGHT - player_height) // 1.5
                last_update_time = pygame.time.get_ticks()
    if isAlive:
        draw_player()
        handle_movement()
        
        if len(fruits) < number_of_items and random.randint(1,70) == 1:
            create_fruits()
        update_fruits()
        draw_fruits()

        update_pebbles()
        draw_pebbles()

        check_collisions()
    
        draw_panel()

        increase_difficulty()

    else:
        if lives > 0:
            display_start_screen()
        else:
            show_game_over_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()