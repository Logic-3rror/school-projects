from pygame import*
import random


init()


##
WIDTH, HEIGHT = 1600, 1000
window = display.set_mode((WIDTH, HEIGHT))
screen = display.get_surface()
exitProg = False


font_ = font.SysFont("Corbel", 40)
font_1 = font.SysFont("Corbel", 100)


#text_surface = button_font.render(text, True, txt_colour)
#text_rect = text_surface.get_rect(center=button_rect.center)



## player attri
playerIMG = image.load("gojo.jpeg")
playerIMG = transform.scale(playerIMG, (60,50))
player = Rect(600,905, 55,50)

heartIMG = image.load("m_heart.png")
heartIMG = transform.scale(heartIMG, (56,36))
score = 0
text_score = font_.render(str(score), True, (255, 255, 255))


##invaders
invaderIMG = image.load("buff shrek.jpeg")
invaderIMG = transform.scale(invaderIMG, (30,30))

#moving
dx = 2
dy = 7

animationTimer = time.Clock()


def draw_hearts():
    player_lives = []
    x = 10
    while x <= 100:
        h = Rect(x, 960, 45,45)
        player_lives.append(h)
        x += 40
    return player_lives




def draw_invaders():
    invaders = []
    y = 20
    while y <= 320:
        x = 20  
        while x <=440:
            i = Rect(x,y, 50,50)
            invaders.append(i)
            x+= 60
        y += 40
    return invaders




def move_invaders():
    global dx
    hit = False
    for i in invaders:
        dy = 0
        if i.x < 0 or i.x > WIDTH-50:
            hit = True
            break
    if hit:
        dy += 20
        dx *= -1

    for i in invaders:
        i.move_ip(dx, dy)


frame_count = 0
invader_lasers = []
laser_array = []
invaders = draw_invaders()  
hearts = draw_hearts()
lives = 3
CD = random.randint(20,80)



while exitProg == False:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            exitProg = True
        if keys[K_SPACE] and len(laser_array)<20:
            laser = Rect(player[0]+30,player[1], 5, 30)
            laser_array.append(laser)

   
    if keys[K_a] and player.left > 0:  # Move left
        player.move_ip(-10, 0)
    if keys[K_d] and player.right <= WIDTH+15:  # Move right
        player.move_ip(10, 0)


    screen.fill((0,0,0))
    draw.line(screen, (111,123,221), (0,955), (1600,955), 2)


    for laser in laser_array:
        laser.move_ip(0, -5)
        draw.rect(screen, (255, 0, 0), laser)
        for invader in invaders:
            if laser.colliderect(invader):
                invaders.remove(invader)
                laser_array.remove(laser)
                score += 100
                break
        if laser.y < 0:
            laser_array.remove(laser)


    CD -=1
    if CD == 0:
        x = random.randint(0, len(invaders)-1)
        invader_lasers.append(Rect(invaders[x][0] + 15, invaders[x][1], 5, 30))
        CD = random.randint(18,30)
    elif invaders == 0 and len(invaders) == 1:
        CD = 1
        for i in range(100):
            invader_lasers.append(Rect(invaders[0][0] + 15, invaders[0][1], 5, 30))
            dy = 12
            
    for inv_laser in invader_lasers:
        inv_laser.move_ip(0,dy)
        draw.rect(screen, (100, 255, 10), inv_laser)
        if inv_laser.colliderect(player):
            invader_lasers.remove(inv_laser)
            lives -= 1
            hearts.remove(hearts[lives])  
            score -= 350
            break
        if inv_laser.y < 0:
            invader_lasers.remove(inv_laser)
    

    for heart in hearts:
        screen.blit(heartIMG, heart)

    screen.blit(playerIMG, player)

    text_score = font_.render(f"SCORE:{score}", True, (255, 255, 255))  # Update score text
    screen.blit(text_score, (1300, 960))




    if invaders:
        move_invaders()
        for invader in invaders:
            screen.blit(invaderIMG, invader)
    else:
        title_surface = font_1.render("You Win", True, (255,255,255))
        title_rect = title_surface.get_rect(center=((WIDTH // 2), 400))
        screen.blit(title_surface, title_rect)
   
    animationTimer.tick(60)
    display.flip()