import pygame as py

py.init()

## Window Settings ##
WIDTH, HEIGHT = 801, 1000
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger")

animation = py.time.Clock()

## Load and Scale Images ##
frog = py.image.load("frogger/images/frog.png")
frog = py.transform.scale(frog, (50, 50))

cars = [
    py.image.load("frogger/images/car1.png"),
    py.image.load("frogger/images/car2L.png"),
    py.image.load("frogger/images/car3L.png"),
    py.image.load("frogger/images/car4.png")
]

## Sound ##
py.mixer.music.load("frogger/music.mp3")
# py.mixer.music.play()

TILE_SIZE = 50
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

## Colors ##
GREEN = (0, 150, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

## Frog Class ##
class Frog(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = frog
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2-25, HEIGHT - TILE_SIZE))
        self.angle = 0

    def move_frog(self):
        keys = py.key.get_pressed()
        if keys[py.K_a] and self.rect.left > 0:
            self.rect.move_ip(-50, 0)
            self.angle = 90
        elif keys[py.K_w] and self.rect.top <= HEIGHT:
            self.rect.move_ip(0, -50)
            self.angle = 0
        elif keys[py.K_s] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, 50)
            self.angle = 180
        elif keys[py.K_d] and self.rect.right <= WIDTH - 5:
            self.rect.move_ip(50, 0)
            self.angle = -90

        self.image = py.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

## Road Class ##
class Road(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_rect = [i.get_rect() for i in cars]


    def draw_road(self):
        x, y = WIDTH, HEIGHT - 350
        py.draw.rect(screen, GRAY, (0, y, x, 200))
        py.draw.line(screen, LIGHT_GRAY, (0, y), (x, y), 5)
        py.draw.line(screen, LIGHT_GRAY, (0, y + 200), (WIDTH, y + 200), 5)
        
        for i in range(0, WIDTH, 40):
            py.draw.line(screen, WHITE, (i + 10, y + 100), (i + 30, y + 100), 5)

    
    
    def draw_cars(self):
        pass

## Temporary Grid ##
def draw_grid():
    for col in range(COLS + 1):
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for row in range(ROWS + 1):
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

frog = Frog()
road = Road()
sprites = py.sprite.Group(frog)

## Game Loop ##
running = True
while running:
    screen.fill(GREEN)
    
    for ev in py.event.get():
        if ev.type == py.QUIT:
            running = False
        if ev.type == py.KEYDOWN:
            frog.move_frog()
    
    road.draw_road()
    sprites.update()
    sprites.draw(screen)
    draw_grid()
    
    py.display.flip()
    animation.tick(60)

py.quit()
