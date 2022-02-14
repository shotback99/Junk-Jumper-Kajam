import pygame
from sys import exit
from random import randint, choice
pygame.init()

HEIGHT = 530
WIDTH = 960

cur_cost = 0
max_budget = 50
budget_length = 400
budget_ratio = max_budget/budget_length
jump_height = -22
good_count = 0
anim_gravity = -3
high_score = 0
dist_bet = 20
game_active = False
start = True


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
plr_size = [100, 100]
plr_rect = pygame.Rect((0, 10), plr_size)
gravity = 1
#Font
title_temp = pygame.font.Font(None, 120)
font_temp = pygame.font.Font(None, 75)
min_temp = pygame.font.Font(None, 40)
sign_temp = pygame.font.Font(None, 70)
sign_surf = sign_temp.render("$", False, (255,255,0))
sign_rect = sign_surf.get_rect(center = (plr_rect.x, plr_rect.y))

#Sound
jump_sound = pygame.mixer.Sound("Huge-GameJamAssets/SOUNDS/JUMP.wav")
jump_sound.set_volume(0.5)
gameover_sound = pygame.mixer.Sound("Huge-GameJamAssets/SOUNDS/GameOver2.wav")
beep_sound = pygame.mixer.Sound("Huge-GameJamAssets/SOUNDS/HealthPoints.wav")
bg_music = pygame.mixer.Sound("Huge-GameJamAssets/SOUNDS/music.wav")
bg_music.set_volume(0)
bg_music.play(loops = -1)
#Surfs
bg = pygame.image.load("Huge-GameJamAssets/MENU/START END MENU/tillshop.jpg").convert_alpha()
bg = pygame.transform.rotozoom(bg, 0, 0.5)
barcode_surf = pygame.image.load("Huge-GameJamAssets/RECEIPT.png").convert_alpha()
barcode_surf = pygame.transform.rotozoom(barcode_surf, 0, 0.6)
barcode_rect = barcode_surf.get_rect(center = (WIDTH//2,HEIGHT//2))
bad_food = [
pygame.image.load("Huge-GameJamAssets/BAD FOOD/1.png").convert_alpha(),
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/BAD FOOD/Burger.png").convert_alpha(), 0, 1.7),
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/BAD FOOD/Pizza - 1.png").convert_alpha(), 0, 2),
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/BAD FOOD/Pizza - 2.png").convert_alpha(), 0, 2)
]
good_food = [
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/GOOD FOOD/apple.png").convert_alpha(), 0, 0.4),
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/GOOD FOOD/banana.png").convert_alpha(), 0, 0.4),
pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/GOOD FOOD/TOMATO.png").convert_alpha(), 0, 0.1)
]
star = pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/STAR.png").convert_alpha(), 0, 0.08)
bf_surf = pygame.image.load("Huge-GameJamAssets/BAD FOOD/NUGGET_ANIM.png")
gf_surf = pygame.transform.rotozoom(pygame.image.load("Huge-GameJamAssets/GOOD FOOD/APPLE_ANIM.png"), 0, 0.4)

outline_message = title_temp.render("Junk Jumper", False, (255, 255, 255))
out_rect = outline_message.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 63))
start_message = title_temp.render("Junk Jumper", False, (100, 100, 255))
start_rect = start_message.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 60))
message = font_temp.render("Click to play", False, (111, 196,255))
message_rect = message.get_rect(center = (WIDTH//2, HEIGHT-100))

bf = bf_surf.convert_alpha().get_rect(center = (100, 60))
gf = gf_surf.get_rect(center = (800, 60))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)
obstacles = []
obstacle_rect = pygame.Rect(950, HEIGHT - 45, 50, 50)

def title_anim():
    global gf, bf, anim_gravity
    gf.y += anim_gravity
    bf.y += anim_gravity
    if gf.bottom >= HEIGHT: anim_gravity *= -1
    if gf.top <= 0: anim_gravity *= -1
    screen.blit(gf_surf, gf)
    screen.blit(bf_surf, bf)
def upd_health():
    global cur_cost, budget_ratio, max_budget
    if cur_cost > max_budget: cur_cost = max_budget
    budget_ratio = max_budget/budget_length
    pygame.draw.rect(screen, "Green", (10, 10, cur_cost//budget_ratio, 25))
    pygame.draw.rect(screen, "White", (10, 10, budget_length, 25), 4)
def obstacle_move(obstacles):
    global score
    if obstacles:
        for index, obs in enumerate(obstacles):
            for index, other_obs in enumerate(obstacles):
                if obstacles[index] == obs:continue
                if obs[1].x <= other_obs[1].x <= obs[1].x + dist_bet:
                    obstacles.pop(index)
            obs[1].x -= 5
            if obs[2] == "g":
                screen.blit(obs[0], obs[1])#pygame.draw.rect(screen, "Blue", obs[0])
            else:screen.blit(obs[0], obs[1])
            obstacles = [obstacle for obstacle in obstacles if obstacle[1].x > -100]
        return obstacles
    else:return []
def obstacle_col(obstacles):
    global plr_size, cur_cost, max_budget, jump_height, good_count, sign_temp
    for index, item in enumerate(obstacles):
        if plr_rect.colliderect(item[1]):
            if item[2] == "b"and plr_size[0] < 500:
                cur_cost += 1
                sign_temp = pygame.font.Font(None, plr_size[0] - 25)
                plr_size[0] += 20
                plr_size[1] += 20
            elif item[2] == "g":
                good_count += 1
                cur_cost += 1
                if cur_cost > max_budget: cur_cost = max_budget
            elif item[2] == "s":
                sign_temp = pygame.font.Font(None, 70)
                plr_size = [100, 100]


            obstacles.pop(index)
def reset_values():
    global plr_size, cur_cost, good_count, obstacles, plr_rect, sign_temp
    plr_size = [100, 100]
    cur_cost = good_count = 0
    obstacles = []
    plr_rect = pygame.Rect((0, 10), plr_size)
    sign_temp = pygame.font.Font(None, 70)
def sign_follow():
    global sign_rect, sign_surf, plr_rect
    sign_surf = sign_temp.render("$", False, (255,255,0))
    sign_rect = sign_surf.get_rect(center = plr_rect.center)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start:
                    game_active = True
                    start = False
                if not start and not game_active: start = True
        if game_active:
            if event.type == obstacle_timer:
                chance = randint(1, 100)
                br, gr = choice(bad_food), choice(good_food)
                obstacle_rect.x = randint(1000, 1200)
                if chance <= 43:obstacles.append([gr ,gr.get_rect(center = (obstacle_rect.x, obstacle_rect.y + 5)), "g"])#obstacles.append([obstacle_rect.copy(), "g"])
                if chance in (99, 100) and plr_size[0] > 100:obstacles.append([star ,star.get_rect(center = (obstacle_rect.x, obstacle_rect.y + 5)), "s"])
                else:obstacles.append([br, br.get_rect(center = (obstacle_rect.x, obstacle_rect.y + 10)), "b"])
    if start:
        screen.fill((173,216,230))
        title_anim()
        if high_score > 0:
            reset_values()
            score = font_temp.render(f"High Score : {high_score}", False, (111, 196,255))
            score_rect = score.get_rect(center = (WIDTH//2, HEIGHT-200))
            screen.blit(score, score_rect)
        screen.blit(outline_message, out_rect)
        screen.blit(start_message, start_rect)
        screen.blit(message, message_rect)
        screen.blit(message, message_rect)
    elif game_active:
        screen.blit(bg, (0, 0))

        plr_rect.w = plr_size[0]
        plr_rect.h = plr_size[1]

        obstacle_col(obstacles)
        casher_message = min_temp.render(F"£{cur_cost}.00", False, [255, 255, 255])
        casher_rect = casher_message.get_rect(center = (WIDTH // 2 + 360, HEIGHT // 2 + 35))
        screen.blit(casher_message, casher_rect)
        pygame.draw.ellipse(screen, "Gold", plr_rect)
        screen.blit(sign_surf, sign_rect)
        gravity += 0.8
        plr_rect.y += gravity
        obstacles = obstacle_move(obstacles)
        upd_health()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            plr_rect.x -= 4
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            plr_rect.x += 4
        if plr_rect.bottom >= HEIGHT: plr_rect.bottom = HEIGHT
        if plr_rect.left <= 0: plr_rect.left = 0
        if plr_rect.right >= WIDTH: plr_rect.right = WIDTH
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and plr_rect.bottom == HEIGHT:
            gravity = jump_height
            jump_sound.play()
        if cur_cost >= max_budget:
            game_active = False
        sign_follow()
    else:
        if good_count > high_score:
            high_score = good_count
        if good_count > cur_cost*0.75:
            screen.fill((111, 196, 169))
            outline = font_temp.render("YOU WIN! :)", False, (255, 255, 255))
            outline_rect = outline.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 3))
            front = font_temp.render("YOU WIN! :)", False, (100, 100, 255))
            front_rect = front.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            count_surf = min_temp.render(f"you spent £{good_count} healthy food", False, (100, 100, 255))
            count_rect = count_surf.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(outline, outline_rect)
            screen.blit(start, start_rect)
            screen.blit(count_surf, count_rect)
        else:
            screen.fill("Red")
            outline = font_temp.render("GAME OVER! >:)", False, (255, 255, 255))
            outline_rect = outline.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 3))
            front = font_temp.render("GAME OVER! >:)", False, (255, 100, 100))
            front_rect = front.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            count_surf = min_temp.render(f"you only spent £{good_count} on healthy food", False, (255, 100, 100))
            count_rect = count_surf.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 50))
            #screen.blit(barcode_surf, barcode_rect)
            screen.blit(outline, outline_rect)
            screen.blit(front, front_rect)
            screen.blit(count_surf, count_rect)

    pygame.display.update()
    clock.tick(60)
