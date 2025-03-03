import pygame as py

py.init()

## window settings ##
WIDTH, HEIGHT = 761, 1280
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger")

animation = py.time.Clock()

# Load and scale frog image
frog = py.image.load("frogger/frog.png")
frog = py.transform.scale(frog, (40, 40))


## sound ##
py.mixer.music.load("frogger/music.mp3")
#py.mixer.music.play()

TILE_SIZE = 40

ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# Colors
GREEN = (0, 150, 0)  
GRAY = (50, 50, 50)  
LIGHT_GRAY = (150,150,150)
BLUE = (0, 0, 255)  
WHITE = (255, 255, 255) 



## Frog class ##
class Frog(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = frog
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 41))  
        self.angle = 0

    def move_frog(self):
        keys = py.key.get_pressed()  
        if keys[py.K_a] and self.rect.left > 0:
            self.rect.move_ip(-40, 0)  
            self.angle = 90
        elif keys[py.K_w] and self.rect.top <= HEIGHT:
            self.rect.move_ip(0, -40)
            self.angle = 0
        elif keys[py.K_s] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, 40)
            self.angle = 180  
        elif keys[py.K_d] and self.rect.right <= WIDTH - 5:
            self.rect.move_ip(40, 0) 
            self.angle = -90
        
        self.rotate_f()        

    def rotate_f(self):
        self.image = py.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        


class Road(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cars = []

    ## temp ##
    def draw_road(self):
        x, y = WIDTH, HEIGHT - 320
        py.draw.rect(screen, GRAY, (0, HEIGHT - 320, WIDTH, 160))
        py.draw.line(screen, LIGHT_GRAY, (0,y), (x, y), 5)
        py.draw.line(screen, LIGHT_GRAY, (0,y+160), (x, y+160), 5)



## temprorary tiles ##
def draw_grid():
    # Draw vertical lines
    for col in range(COLS + 1):  # +1 to draw line at the far right edge
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    
    # Draw horizontal lines
    for row in range(ROWS + 1):  # +1 to draw line at the bottom edge
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
        
        
frog = Frog()
road = Road()
sprites = py.sprite.Group(frog)

# Game loop
running = True
while running:
    screen.fill((0, 150, 0)) 
    for ev in py.event.get():
        if ev.type == py.QUIT:
            running = False
        if ev.type == py.KEYDOWN:
            frog.move_frog()   
    
    draw_grid()

    road.draw_road()    

    sprites.update()
    sprites.draw(screen)

    py.display.flip()
    animation.tick(60)

py.quit()

