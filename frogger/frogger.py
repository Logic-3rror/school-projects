import pygame as py, random


py.init()

## Window Settings ##
WIDTH, HEIGHT = 1251, 1100
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger")

animation = py.time.Clock()

## Load and Scale Images ##
frog_ = py.image.load("frogger/images/frog.png")
frog_ = py.transform.scale(frog_, (50, 50))


cars = [
    py.image.load("frogger/images/car1.png"),
    py.image.load("frogger/images/car2L.png"),
    py.image.load("frogger/images/car3L.png"),
    #py.image.load("frogger/images/car4.png")
]


cars = [py.transform.scale(i, (100,50)) for i in cars]*2


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
        self.image = frog_
        self.original_pos = (WIDTH // 2 , HEIGHT)  # Store the starting position
        self.rect = self.image.get_rect(midbottom=self.original_pos)
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
    
    def reset_pos(self):
         self.rect = self.image.get_rect(midbottom=self.original_pos)
        
    def on_tile(self):
        frog.rect.x = (frog.rect.x//TILE_SIZE)*TILE_SIZE
        frog.rect.y = (frog.rect.y//TILE_SIZE)*TILE_SIZE


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

        if self.rect.x < -190 or self.rect.x > WIDTH +190:
            self.kill()
    

class LaneManager(py.sprite.Sprite):
    def __init__(self, num_lanes, y):
        super().__init__()
        self.obj_group = py.sprite.Group()
        self.lanes = {}
        self.direction = ["right","left"]
        self.y = y

        for i in range(num_lanes):  # 8 lanes
            obj_y = y + (i * TILE_SIZE)
            self.lanes[i] = {
                "y": obj_y,
                "direction": random.choice(self.direction)  # Randomly set direction once
            }

    def spawn(self, obj):
        for object in self.obj_group:
            if obj != object and obj.rect.colliderect(object.rect.inflate(150, 0)):
                return False
        return True
    
    def add_obj(self, x, obj_type, speed, type):
        if self.lanes:
            match type:
                case "small":
                    image = py.image.load("frogger/images/small.png")
                case "medium":
                    image = py.image.load("frogger/images/medium.png")
                case "large":
                    image = py.image.load("frogger/images/large.png")
                case _:
                    image = type

            lane = random.choice(list(self.lanes.values()))
            if lane["direction"] == "right":#
                speed *= -1
                x = -120
            elif lane["direction"] == "left":
                image = py.transform.rotate(image, 180)
                speed *= 1
                x = WIDTH + 120

            if obj_type == "car":
                obj = Car(image, x, lane["y"] + 25, speed, self.obj_group)
            else:
                obj = Log(image, x, lane["y"] + 25, speed, self.obj_group)

              # Ensure no collision before adding
        if self.spawn(obj):
            self.obj_group.add(obj)
        else:
            # If collision happens, either move it forward or delay spawning
            attempts = 0
            while not self.spawn(obj) and attempts < 3:  # Try up to 3 times
                if lane["direction"] == "right":
                    obj.rect.x += 50  # Move forward
                else:
                    obj.rect.x -= 50  # Move backward
                attempts += 1

            if self.spawn(obj):
                self.obj_group.add(obj)
            else:
                del obj  # If still colliding after 3 attempts, don't spawn this cycle

    def draw_obj(self):
        self.obj_group.draw(screen)
    
    def update(self):
        self.obj_group.update()

## Road Class ##
class Road(LaneManager):
    def __init__(self):
        super().__init__(8, HEIGHT - (9 * TILE_SIZE))
        self.car_group = py.sprite.Group()

    def draw_lanes(self):
        ## road ##
        for i in self.lanes:
            py.draw.rect(screen, GRAY, (0, self.lanes[i]["y"], WIDTH, TILE_SIZE))


            ## big kerbs ##
        y = HEIGHT - (9 * TILE_SIZE) + (i* TILE_SIZE)
        py.draw.line(screen, LIGHT_GRAY, (0, 650), (WIDTH, 650), 6)
        py.draw.line(screen, LIGHT_GRAY, (0, y + TILE_SIZE), (WIDTH, y + TILE_SIZE), 6)

        ## small kerbs ##
        for i in range(5):
            py.draw.line(screen, LIGHT_GRAY, (0,2*i* TILE_SIZE + 650), (WIDTH,2*i* TILE_SIZE + 650), 4)
            
            ## dotted line ## 
        for i in range(4):
            for j in range(-10, WIDTH, TILE_SIZE):
                py.draw.line(screen, WHITE, (j + 20, y - 2*i * TILE_SIZE), (j + 50, y - 2*i * TILE_SIZE), 2)

    
    def collision(self, frog):
        for car in self.obj_group:
            if frog.rect.colliderect(car.rect):
                return True


class Log(py.sprite.Sprite):
    def __init__(self, image, x, y, speed, log_group):
        super().__init__()
        self.log_group = log_group
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.spawn_x = x
        
    def update(self):
        self.rect.x += self.speed

        if self.rect.x < -300 or self.rect.x > WIDTH + 300:    
            self.kill()


class River(LaneManager):
    def __init__(self):
        super().__init__(7,(2 * TILE_SIZE+150))
        self.frog_on_log = None
        self.land = []

    def draw_lanes(self):
        ## river ##
        for i in self.lanes:
            py.draw.rect(screen, BLUE, (0, self.lanes[i]["y"], WIDTH, TILE_SIZE))
    
    def draw_land(self):
        for i in range(1, 6):
            rect = py.Rect(250 * i - 200, 150, 150, TILE_SIZE * 2)
        
            # Draw the rectangle to the screen
            py.draw.rect(screen, BLUE, rect)
        
            # Add the rectangle to the land list
            self.land.append(rect)

    ## make frog at center of log for now
    def collision(self, frog):
        for log in self.obj_group:
                if log.rect.colliderect(frog.rect):
                    self.frog_on_log = True
                    if self.frog_on_log :
                        frog.rect.x = log.rect.centerx 
                        frog.rect.y = log.rect.centery - 25
                        
                        
                        self.frog_on_log =  True  
                        return self.frog_on_log 
            # If no log is touching the frog, reset to spawn
        self.frog_on_log = False 
        return self.frog_on_log 
    
    def off_log(self, frog):
        if not self.frog_on_log:
            if 200 < frog.rect.y < 600:
                return True
            else:
                for i in self.land:
                    if frog.rect.colliderect(i):
                        return True
        return False


    

class GameState:
    pass                                  

## Temporary Grid ##
def draw_grid():
    for col in range(COLS + 1):
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for row in range(ROWS + 1):
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))


car_CD = 0
log_CD = 0

log_type  = ["small","medium", "large"]
frog = Frog()
road = Road()
river = River()
sprite = py.sprite.Group(frog)
#car_sprite = py.sprite.Group()
#log_sprite = py.sprite.Group()
froggy_loggy = False

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

    
    road.draw_obj()
    road.update()

    river.draw_obj()
    river.draw_land()
    river.update()
   

    if car_CD == 0:
        x = random.randint(1,7)
        car = random.choice(cars)
        road.add_obj(x,"car", -6, car)

        car_CD = random.randint(1, 15)
    car_CD -=1    

    if log_CD == 0:
        y = random.randint(1,5)
        river.add_obj(1300,"log", -6, random.choice(log_type))

        log_CD = random.randint(1, 15)
        
    log_CD -=1    

    if road.collision(frog):
        frog.reset_pos()
        
    if not river.collision(frog):
        if river.off_log(frog):
            frog.reset_pos()
        

    sprite.draw(screen)
    sprite.update()
    frog.on_tile()
    draw_grid()

    
    animation.tick(60)
    py.display.flip()
    

py.quit()


