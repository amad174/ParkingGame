import pygame, os, button, objects, sys, carMechanics, time

pygame.init()
clock = pygame.time.Clock()
end_font_lose = pygame.font.Font('freesansbold.ttf', 100)
end_font = pygame.font.Font('freesansbold.ttf', 50)
end_font_small = pygame.font.Font('freesansbold.ttf',40)
leader_title_font = pygame.font.Font('freesansbold.ttf', 50)
leader_small_font = pygame.font.Font('freesansbold.ttf', 20)
times = []

WIDTH, HEIGHT = 1000, 500
ROAD_WIDTH, ROAD_HEIGHT = 100, 200
PARK_WIDTH, PARK_HEIGHT = 75, 150

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (153, 204, 255)




#getting images for game
BACKGROUND_ONE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Level1.png")).convert(), (WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "grass.jpg")), 
    (WIDTH, HEIGHT))

PARK_VERTICAL = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "park.png")), (PARK_WIDTH, PARK_HEIGHT))

ROAD = pygame.image.load(os.path.join("assets", "road.png"))
ROAD_ONE = pygame.transform.scale(ROAD ,(ROAD_WIDTH, ROAD_HEIGHT))
ROAD_TWO = pygame.transform.rotate(pygame.transform.scale(ROAD ,(ROAD_WIDTH, ROAD_HEIGHT * 3)), 90)

#Buttons==========================================================
#Getting button images
START_IMG = pygame.image.load("assets\start.png").convert_alpha()
QUIT_IMG = pygame.image.load("assets\quit.png").convert_alpha()
QUIT2_IMG = pygame.image.load("assets\quit2.png").convert_alpha()
RESET_IMG = pygame.image.load("assets/reset.png").convert_alpha()
LEADER_IMG = pygame.image.load("assets/leaderboard.png").convert_alpha()
MENU_IMG = pygame.image.load("assets/menu.png").convert_alpha()
SUB_IMG = pygame.image.load("assets/submit.png").convert_alpha()
#Creating button objects
start_btn = button.Button(375, 50, START_IMG, 1)
quit_btn = button.Button(375, 350, QUIT_IMG, 1)
quit_btn_lose_screen = button.Button(250, 300, QUIT_IMG, 1)
quit2_btn = button.Button(0, 0, QUIT2_IMG, 0.05)
reset_btn = button.Button(550, 300, RESET_IMG, 1)
leader_btn = button.Button(375, 200, LEADER_IMG, 1)
menu_btn = button.Button(550, 300, MENU_IMG, 1)
sub_btn = button.Button(750, 170, SUB_IMG, 1)

def check_car_in_parking_space(car, left, right, bottom, top):
    #print(f"car: {car.rect.left, car.rect.right, car.rect.bottom, car.rect.top}")
    if car.rect.left > left and car.rect.right < right and car.rect.bottom < bottom and car.rect.top > top:
        return True    
    
def lose_screen():
    #creating text object
    text = end_font_lose.render('Game Over', True, WHITE, RED)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 3)

    while True:
        WIN.fill(RED)
        WIN.blit(text, textRect)

        if reset_btn.draw(WIN):
            draw_level_one()
        if quit_btn_lose_screen.draw(WIN):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

def win_screen():
    active = False
    user_text = ""
    user_rect = pygame.Rect(300, 190, 400, 50)
    #caculate time to complete in secondds
    total_time = 0
    for time in times:
        total_time += time
    total_time = round(total_time, 2)

    #creating text object
    text = end_font.render('Game Complete!', True, WHITE, GREEN)
    time_text = f"Time: {total_time}s"
    time_text_render = end_font_small.render(time_text, True, WHITE, GREEN)

    times.clear()

    while True:
        WIN.fill(GREEN)
        WIN.blit(text, (300, 50))
        WIN.blit(time_text_render, (10, 200))

        if active:
            pygame.draw.rect(WIN, SKY_BLUE, user_rect, 2)
        else:
            pygame.draw.rect(WIN, WHITE, user_rect, 2)
        
        text_surface = end_font_small.render(user_text, True, WHITE)
        WIN.blit(text_surface, (user_rect.x + 5, user_rect.y + 5))

        if sub_btn.draw(WIN):
            f = open("scoreboard.txt", "a")
            if user_text == "":
                f.write(f"Anon {total_time} \n")
            else:
                f.write(f"{user_text} {total_time} \n")
            f.close()
            user_text = "Submmited!"

        if reset_btn.draw(WIN):
            draw_level_one()
        if quit_btn_lose_screen.draw(WIN):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
        
        pygame.display.update()

def display_leader_board_text():
    y_pos = 50
    loop = 1

    lines = open("scoreboard.txt", 'r').readlines()
    output = open("leaderboard.txt", 'w')

    for line in sorted(lines, key=lambda line: line.split()[1]):
        output.write(line)
    
    output.close()

    with open("leaderboard.txt") as f:
        for line in f:
            splitStr = line.split()
            personStr = f"{loop}.) {splitStr[0]} {splitStr[1]}"
            txt = leader_small_font.render(personStr, True, BLACK, SKY_BLUE)
            WIN.blit(txt, (0, y_pos))
            y_pos += 30
            loop += 1

def draw_leader_board():
    text = leader_title_font.render('Leaderboard (Top 15)', True, BLACK, SKY_BLUE)
    while True:
        WIN.fill(SKY_BLUE)
        WIN.blit(text, (0,0))

        display_leader_board_text()

        if menu_btn.draw(WIN):
            main_menu()
        if quit_btn_lose_screen.draw(WIN):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

def draw_level_two():
    #Creating car object
    car = carMechanics.PlayerCar((235, 75))
    start = time.time()
    while True:
        clock.tick(FPS)
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(ROAD_TWO, (200 , HEIGHT - ROAD_WIDTH - ROAD_HEIGHT))
        WIN.blit(ROAD_ONE, (200 , 50))
        p = pygame.Rect(725, HEIGHT - ROAD_WIDTH - ROAD_HEIGHT - PARK_HEIGHT, PARK_WIDTH, PARK_HEIGHT)
        WIN.blit(PARK_VERTICAL, (p.x, p.y))

        #draw car
        car.move_player(WIN)

        if quit2_btn.draw(WIN):
            main_menu()

        if check_car_in_parking_space(car, 725, 800, 200, 50):
            times.append(time.time() - start)
            win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def draw_level_one():
    #Creating car object
    car = carMechanics.PlayerCar((150, 400))
    start = time.time()   
    while True:
        clock.tick(FPS)
        WIN.blit(BACKGROUND_ONE, (0, 0))
        WIN.blit(objects.BACKGROUND_ONE_OUTLINE, (0, 0))

        #draw car
        car.move_player(WIN)
        
         
        if car.collide(objects.BACKGROUND_ONE_MASK) !=None:
            times.clear()
            lose_screen()

        if quit2_btn.draw(WIN):
            main_menu()

        if check_car_in_parking_space(car, 778, 860, 80, 5):
            times.append(time.time() - start)
            draw_level_two()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def main_menu():
    run = True
    times.clear()
    while run:
        WIN.fill(SKY_BLUE)
        
        if start_btn.draw(WIN):
            draw_level_one()
        if leader_btn.draw(WIN):
            draw_leader_board()
        if quit_btn.draw(WIN):
            run = False
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()