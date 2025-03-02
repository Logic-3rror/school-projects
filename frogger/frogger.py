import pygame as py

py.init()

## window settings ##
WIDTH, HEIGHT = 761, 1280
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger Clone")

animation = py.time.Clock()

# Load and scale frog image
frog = py.image.load("frogger/frog.png")
frog = py.transform.scale(frog, (40, 40))

TILE_SIZE = 40

ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# Colors for tiles
GRASS_COLOR = (0, 150, 0)  # Grass (background)
ROAD_COLOR = (50, 50, 50)  # Road color
WATER_COLOR = (0, 0, 255)  # Water color
GRID_COLOR = (255, 255, 255) 



## Frog class ##
class Frog(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = frog
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 41))  # Centered at bottom

    def move_frog(self):
        keys = py.key.get_pressed()  
        if keys[py.K_a] and self.rect.left > 0:
            self.rect.move_ip(-40, 0)  
        elif keys[py.K_d] and self.rect.right <= WIDTH - 5:
            self.rect.move_ip(40, 0)  
        elif keys[py.K_w] and self.rect.top <= HEIGHT:
            self.rect.move_ip(0, -40)  
        elif keys[py.K_s] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, 40)  


class Infra:
    def __init__():
        pass


## temprorary tiles ##
def draw_grid():
    # Draw vertical lines
    for col in range(COLS + 1):  # +1 to draw line at the far right edge
        py.draw.line(screen, GRID_COLOR, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    
    # Draw horizontal lines
    for row in range(ROWS + 1):  # +1 to draw line at the bottom edge
        py.draw.line(screen, GRID_COLOR, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

frog = Frog()
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

    sprites.update()
    sprites.draw(screen)

    py.display.flip()
    animation.tick(60)

py.quit()
