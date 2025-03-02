from pygame import *
import random

init()

# Window Setup
WIDTH, HEIGHT = 1600, 1000
window = display.set_mode((WIDTH, HEIGHT))
screen = display.get_surface()

# Fonts
font_ = font.SysFont("Corbel", 40)
font_1 = font.SysFont("Corbel", 100)

# Player Attributes
playerIMG = image.load("gojo.jpeg")
playerIMG = transform.scale(playerIMG, (60, 50))

# Heart Image
heartIMG = image.load("m_heart.png")
heartIMG = transform.scale(heartIMG, (58, 36))

# Invader Attributes
invaderIMG = image.load("buff shrek.jpeg")
invaderIMG = transform.scale(invaderIMG, (30, 30))

#moving
dx = 5
dy = 2

score = 0
lives = 3

exitProg = False

animationTimer = time.Clock()


class Laser:
    def __init__(self, x, y, direction):
        self.laser = Rect(x, y, 5, 30)
        self.speed = 5
        self.direction = direction


    def move_laser(self, screen , color):
        self.laser.move_ip(0, self.direction*5)
        draw.rect(screen, color, self.laser)

        if self.direction == -1:
            if self.laser.y < 0:
                player.laser.remove(self)
        
        if self.direction == 1:
            if self.laser.y > 970:
                invader.laser.remove(self)

    def collision(self, temp, laser, laser_list, thing):
        if temp == "invader": 
            for i in thing:
                if laser.laser.colliderect(i.invader):
                    thing.remove(i)
                    laser_list.remove(laser)
                    game.score += 125  # Update score
                    break   

        if temp == "player":
            for laser in laser_list:
                if laser.laser.colliderect(player.player):
                    laser_list.remove(laser)          
                    game.score -= 350  
                    game.lives -= 1  # Decrease lives

class Player:
    def __init__(self, x,y, lives):
        self.image = playerIMG
        self.player = Rect(x, y, 60, 52)
        self.speed = 10
        self.lives = lives
        self.laser = []

    def show(self):
        screen.blit(playerIMG, self.player)
    
    def move(self):
        if keys[K_a] and self.player.left > 0:  # Move left
            self.player.move_ip(-10, 0)
        if keys[K_d] and self.player.right <= WIDTH-15:  # Move right
            self.player.move_ip(10, 0)

    def shoot(self):
        if keys[K_SPACE] and len(self.laser)<200:
            laser = Laser(player.player[0]+29, player.player[1]+20, -1)
            self.laser.append(laser)

class Invaders:
    def __init__(self, x, y, invader_list):
        self.image = invaderIMG
        self.invader = Rect(x,y, 34,40) 
        self.invader_list = invader_list
        self.speed = dx
        self.laser = []

    def show_i(self, screen):
        screen.blit(self.image, self.invader)

    def move_i(self):
        #global dy
        hit = False
        dy = 0

        for i in self.invader_list:    
            if i.invader.x < 0 or i.invader.x > WIDTH-50:
                hit = True
                break
    
        if hit:
            dy += 30
            for i in self.invader_list:
                i.speed *= -1  

        for i in self.invader_list:
            i.invader.move_ip(self.speed, dy)   

    def shoot_i(self):
        x = random.randint(0, len(invader_list)-1)
        i = self.invader_list[x]
        self.laser.append(Laser(i.invader[0] + 15, i.invader[1] + 15, 1))

class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3

    def show_score(self):
        text_score = font_.render(f"SCORE: {self.score}", True, (255, 255, 255))
        screen.blit(text_score, (1300, 960))

    def show_lives(self):
        for i in range(self.lives):
            screen.blit(heartIMG, (20 + i * 50, 960))

    def game_over(self):
        global exitProg
        if self.lives == -1:
            title_surface = font_1.render("You Lose...", True, (255,255,255))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title_surface, title_rect)
        
        elif player.player.colliderect(invader.invader):
            title_surface = font_1.render("You Lose...", True, (255,255,255))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title_surface, title_rect)

        elif not invader.invader_list:
            title_surface = font_1.render("You Win!", True, (255,255,255))
            title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title_surface, title_rect)

def draw_invaders():
    invaders = []
    for y in range(20, 280, 40):
        for x in range(20, 500, 60):
            i = Invaders(x,y, invaders)
            invaders.append(i)
    return invaders

CD = random.randint(18,30)
player = Player(600, 905, lives)
invader_list = draw_invaders()
invader = Invaders(20,20, invader_list)
game = GameState()  # Initialize game state


while exitProg == False:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            exitProg = True
        
        player.shoot()

    screen.fill((0,0,0))
    
    # Player Lasers
    for laser in player.laser:
        laser.move_laser(screen, (255,0,0))
        laser.collision("invader", laser, player.laser, invader_list)

    # Invader Shooting
    CD -= 1
    if CD == 0:
        invader.shoot_i()
        CD = random.randint(18,30)
    
    # Invader Lasers
    for laser in invader.laser:     
        laser.move_laser(screen, (100, 255, 10))
        laser.collision("player", laser, invader.laser, player.player)

    player.show()
    player.move()

    
    if invader_list:
        if len(invader_list) == 1:
            invader_list[0].speed = 20
            #CD = 1
            #invader.speed = 20  
            #dy = 12  

            #for i in range(3):  # Shoot multiple bullets at once
            #    invader.laser.append(Rect(invader_list[0][0] + 15, invader_list[0][1], 5, 30))

        invader.move_i() 
        for invader in invader_list:
            invader.show_i(screen)

    


    # Display Score and Lives
    draw.rect(screen, (111,123,221), (0,955, 1600,955), 490, 1)
    game.show_score()
    game.show_lives()
    game.game_over()

    
    animationTimer.tick(60)
    display.flip()

