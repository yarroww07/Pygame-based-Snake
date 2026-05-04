# importing libraries
import pygame
import time
import random
import pandas as pd

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
orange = pygame.Color(255, 140, 0)




# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()


# BONUS FRUIT VARIABLES
bonus_fruit_spawn = False
bonus_fruit_position = [0, 0]
bonus_fruit_timer = 0
bonus_fruit_duration = random.randint(5000,10000)
bonus_fruit_spawn_chance = 0.2 #per frame i think?



# BOMB FRUIT VARIABLES
bomb_fruit_spawn = False
bomb_fruit_position = [0,0]
bomb_fruit_timer = 0
bomb_fruit_duration = random.randint(60000, 180000)
bomb_fruit_spawn_chance = 0.2
# BORDERS
border_right = window_x
border_left = 0
border_up = 0
border_down = window_y
shrink = 20


# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# Borders


# fruit position

fruit_dictionary = {'normal': {
    'color': white,
    'effect': 'none',
    'score': 10,
    'chance': 0.7},
    'multiplier': {
        'color': yellow,
        'effect': 'triple_score',
        'score': 30
    },
    'bomb': {
        'color': orange,
        'effect': 'none',
        'score': 0
    }}

fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

selected_fruit = 'normal'

# displaying Score function
def show_score(choice, color, font, size):
  
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
    
    # create the display surface object 
    # score_surface
    high_score = get_high_score()
    score_surface = score_font.render(f'Score: {score}  High: {high_score}', True, color) 
    
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
    
    # displaying text
    game_window.blit(score_surface, score_rect)
    

# game over function
def game_over():
  
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface on which text 
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    # create a rectangular object for the text 
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    save_score(score)
    
    # after 2 seconds we will quit the program
    time.sleep(2)
    
    # deactivating pygame library
    pygame.quit()
    
    # quit the program
    quit()

def save_score(score):
    scores_sheet = "scores.csv"
    
    
    df = pd.read_csv(scores_sheet)
    
    new_row = pd.DataFrame({"score": [score]})
    df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_csv(scores_sheet, index=False)


def get_high_score():
    df = pd.read_csv("scores.csv")
    return df.max().max()



# Main Function
while True:
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two 
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += fruit_dictionary[selected_fruit]['score'] 
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        selected_fruit = 'normal'
        fruit_position = [
            random.randrange((border_left + 10) // 10, (border_right - 10) // 10) * 10,
            random.randrange((border_up + 10) // 10, (border_down - 10) // 10) * 10
        ]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for x in range(0, 800, 10):
        pygame.draw.line(game_window, (150,150,150), (x,0), (x,600))
    for y in range(0, 600, 10):
        pygame.draw.line(game_window, (150,150,150), (0,y), (800,y))

    
    fruit_color = fruit_dictionary[selected_fruit]['color']

    if not bonus_fruit_spawn:
        if random.random() < bonus_fruit_spawn_chance:
            bonus_fruit_spawn = True
            bonus_fruit_position = [
                random.randrange(1, (window_x // 10)) * 10,
                random.randrange(1, (window_y//10)) * 10
            ]
            bonus_fruit_timer = pygame.time.get_ticks()
            bonus_fruit_duration = random.randint(5000,10000)
    else:
        if pygame.time.get_ticks() - bonus_fruit_timer > bonus_fruit_duration:
            bonus_fruit_spawn = False

        if snake_position[0] == bonus_fruit_position[0] and snake_position[1] == bonus_fruit_position[1]:
            score += fruit_dictionary['multiplier']['score'] 
            bonus_fruit_spawn = False

    if bonus_fruit_spawn:
        pygame.draw.rect(game_window, yellow,
                     pygame.Rect(bonus_fruit_position[0], bonus_fruit_position[1], 10, 10))
    
    if not bomb_fruit_spawn:
        if random.random() < bomb_fruit_spawn_chance:
            bomb_fruit_spawn = True
            bomb_fruit_position = [
                random.randrange(1, (window_x // 10)) * 10,
                random.randrange(1, (window_y//10)) * 10
            ]
            bomb_fruit_timer = pygame.time.get_ticks()
            bomb_fruit_duration = random.randint(60000, 180000)
    else:
        if pygame.time.get_ticks() - bomb_fruit_timer > bomb_fruit_duration: 
            bomb_fruit_spawn = False
        
        elif snake_position[0] == bomb_fruit_position[0] and snake_position[1] == bomb_fruit_position[1]:
            border_left += shrink
            border_right -= shrink
            border_up += shrink
            border_down -= shrink
            bomb_fruit_spawn = False
    
    if bomb_fruit_spawn:
        pygame.draw.rect(game_window, orange,
                         pygame.Rect(bomb_fruit_position[0], bomb_fruit_position[1], 10, 10))

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, fruit_color, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
    border_thickness = 10
    pygame.draw.rect(game_window, red, pygame.Rect(border_left, border_up, border_right - border_left, border_thickness))        # top
    pygame.draw.rect(game_window, red, pygame.Rect(border_left, border_down - border_thickness, border_right - border_left, border_thickness))  # bottom
    pygame.draw.rect(game_window, red, pygame.Rect(border_left, border_up, border_thickness, border_down - border_up))           # left
    pygame.draw.rect(game_window, red, pygame.Rect(border_right - border_thickness, border_up, border_thickness, border_down - border_up))



    # Game Over conditions
    # if snake_position[0] > border_left[0]:
    #     game_over()
    if snake_position[0] < border_left + border_thickness or snake_position[0] >= border_right - border_thickness:
        game_over()
    if snake_position[1] < border_up + border_thickness or snake_position[1] >= border_down - border_thickness:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)


    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)