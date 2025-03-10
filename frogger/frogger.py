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

log = py.image.load("frogger/images/log.png")
log = py.transform.rotate(log, 90)
log = py.transform.scale(log, (50,50))

cars = [
    py.image.load("frogger/images/car1.png"),
    py.image.load("frogger/images/car2L.png"),
    py.image.load("frogger/images/car3L.png"),
    #py.image.load("frogger/images/car4.png")
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
    def __init__(self, image, x, y, speed, car_group):
        super().__init__()
        self.car_group = car_group
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.spawn_x = x

    def update(self):
        self.rect.x += self.speed

        if self.rect.x < -120:
            if self.car_group and self.respawn():
                self.rect.x = self.spawn_x

    def respawn(self):

        if self.car_group:
            for car in self.car_group:
                if self.rect.colliderect(car.rect) or car == self:
                    return False
        return True
    
   

## Road Class ##
class Road(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_group = py.sprite.Group()
        self.lanes = {}
        self.direction = ["right","left"]

        for i in range(8):  # 8 lanes
            y = HEIGHT - (10 * TILE_SIZE) + (i * TILE_SIZE)
            self.lanes[i] = {
                "y": y,
                "direction": random.choice(self.direction)  # Randomly set direction once
            }

    ## temp ##
    def draw_lanes(self):
        ## road ##
        for i in self.lanes:
            py.draw.rect(screen, GRAY, (0, self.lanes[i]["y"], WIDTH, TILE_SIZE))


            ## kerbs ##
        y = HEIGHT - (10 * TILE_SIZE) + (i * TILE_SIZE)
        py.draw.line(screen, LIGHT_GRAY, (0, 600), (WIDTH, 600), 6)
        py.draw.line(screen, LIGHT_GRAY, (0, y + TILE_SIZE), (WIDTH, y + TILE_SIZE), 6)

            ## dotted line ##  `` fix ``
        for j in range(0, WIDTH, TILE_SIZE):
            py.draw.line(screen, WHITE, (j + 10, y + 2 * TILE_SIZE), (j + 40, y + 2 * TILE_SIZE), 4)

    def add_car(self, image, x, i, speed):
        if self.lanes:
            lane = random.choice(list(self.lanes.values()))
            if lane["direction"] == "right":#
                speed *= -1
                x = -120
            elif lane["direction"] == "left":
                image = py.transform.rotate(image, 180)
                speed *= 1
                x = WIDTH + 120

            car = Car(image, x, lane["y"] + 25, speed, self.car_group)
            self.car_group.add(car)


    def collision(self, frog):
        for car in self.car_group:
            if frog.rect.colliderect(car.rect):
                return True
    
        
    def draw_cars(self):
        self.car_group.draw(screen)
    
    def update(self):
        self.car_group.update()

class Log(py.sprite.Sprite):
    def __init__(self):
        self.image = log

class River:
    def __init__(self):
        self.river = {}
        self.direction = ["right","left"]

    def draw_lanes(self):
        ## road ##
        for i in range(6):
            y = (3 * TILE_SIZE) + (i * (TILE_SIZE))
            py.draw.rect(screen, BLUE, (0, y, WIDTH, TILE_SIZE))
            self.river[i] = {"y": y, "direction": random.choice(self.direction)}


## Temporary Grid ##
def draw_grid():
    for col in range(COLS + 1):
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for row in range(ROWS + 1):
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))



frog = Frog()
road = Road()
river = River()
sprite = py.sprite.Group(frog)
car_sprite = py.sprite.Group()

pos = 0

## Game Loop ##
running = True
while running:
    screen.fill(GREEN)
    
    for ev in py.event.get():
        if ev.type == py.QUIT:
            running = False
        if ev.type == py.KEYDOWN:
            frog.move_frog()

    
    
    road.draw_lanes()
    river.draw_lanes()

    sprite.update()
    sprite.draw(screen)

    
    road.update()
    road.draw_cars()

   


    if CD == 0:
        x = random.randint(1,7)
        car = random.choice(cars)
        road.add_car(car,1200, x, -3)
        CD = random.randint(10, 50)
    CD -=1    

    if road.collision(frog):
        pos += 1
        print(pos)
    

    draw_grid()

    
    animation.tick(100)
    py.display.flip()
    

py.quit()
