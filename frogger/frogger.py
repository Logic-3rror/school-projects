import pygame as py, random

py.init()

## Window Settings ##
WIDTH, HEIGHT = 1101, 1100
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

cars = [py.transform.scale(i, (100,50)) for i in cars]*2
CD = random.randint(60,180)

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

class Car(py.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

        if self.rect.x < -120:
            self.rect.x = WIDTH

## Road Class ##
class Road(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_group = py.sprite.Group()
        self.lanes = []
    

    ## temp ##
    def draw_road(self):
        ## road ##
        for i in range(8):
            y = HEIGHT - (10 * TILE_SIZE) + (i * (TILE_SIZE))
            py.draw.rect(screen, GRAY, (0, y, WIDTH, TILE_SIZE))

            ## kerbs ##
        py.draw.line(screen, LIGHT_GRAY, (0, 600), (WIDTH, 600), 6)
        py.draw.line(screen, LIGHT_GRAY, (0, y + TILE_SIZE), (WIDTH, y + TILE_SIZE), 6)

            ## dotted line ##
        for j in range(0, WIDTH, TILE_SIZE):
            py.draw.line(screen, WHITE, (j + 10, y + 2 * TILE_SIZE), (j + 40, y + 2 * TILE_SIZE), 4)

    def add_car(self, image, x, y, speed):

        car = Car(image, x, y, speed)
        self.car_group.add(car)
        
    def draw_cars(self):
        self.car_group.draw(screen)
    
    def update(self):
        self.car_group.update()




## Temporary Grid ##
def draw_grid():
    for col in range(COLS + 1):
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for row in range(ROWS + 1):
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))



frog = Frog()
road = Road()
sprite = py.sprite.Group(frog)
car_sprite = py.sprite.Group()



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
    sprite.update()
    sprite.draw(screen)

    
    road.update()
    road.draw_cars()

    if CD == 0:
        x = random.randint(1,7)
        road.add_car(cars[0],1200, 625 + (x*50), -5)
        CD = random.randint(80,160)

    CD -=1    
    draw_grid()

    
    animation.tick(100)
    py.display.flip()
    

py.quit()
