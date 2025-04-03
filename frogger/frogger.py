import pygame as py, random

py.init()

## Window Settings ##
WIDTH, HEIGHT = 1251, 1100
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger")

animation = py.time.Clock()


#lilypad = py.image.load("frogger/images/lilypad.png")

TILE_SIZE = 50
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

## Colors ##
GREEN = (0, 150, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

## Frog Class ##
class Frog(py.sprite.Sprite):
    frog_ = py.image.load("frogger/images/frog.png")
    frog_ = py.transform.scale(frog_, (50, 50))
    
    def __init__(self):
        super().__init__()
        self.image = self.frog_
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
        
    def on_tile(self, frog):
        frog.rect.x = (frog.rect.x//TILE_SIZE)*TILE_SIZE
        frog.rect.y = (frog.rect.y//TILE_SIZE)*TILE_SIZE

class Car(py.sprite.Sprite):
    cars = [
        py.image.load("frogger/images/car1.png"),
        py.image.load("frogger/images/car2L.png"),
        py.image.load("frogger/images/car3L.png"),
    ]
    cars = [py.transform.scale(i, (100,50)) for i in cars]*2
    
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
    
class LilyPad(py.sprite.Sprite):
    lilypad = py.image.load("frogger/images/lilypad.png")
    
    def __init__(self, image, x, y, speed, lily_group):
        super().__init__()
        self.log_group = lily_group
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.spawn_x = x
        
    def update(self):
        self.rect.x += self.speed

        if self.rect.x < -300 or self.rect.x > WIDTH + 300:    
            self.kill()

class LaneManager(py.sprite.Sprite):
    def __init__(self, num_lanes, y, type):
        super().__init__()
        self.obj_group = py.sprite.Group()
        self.lanes = {}
        self.num_lanes = num_lanes
        self.direction = ["right","left"]
        self.river_obj_type = ["log", "lily"]
        self.y = y
        self.log_type_  = ["small","medium", "large"]
        self.num_logs = 1
        
        self.add_lanes(type)

    def log_type(self, type):
        match type:
            case "small":
                image = py.image.load("frogger/images/small.png")
                self.num_logs = random.randint(1,3)
            case "medium":
                image = py.image.load("frogger/images/medium.png")
                self.num_logs = random.randint(1,2)
            case "large":
                image = py.image.load("frogger/images/large.png")
                self.num_logs = 1
            case _:
                return type, None
        return image, self.num_logs
    
    def add_lanes(self, type):
        obj_type = random.choice(self.river_obj_type)
        for i in range(self.num_lanes):  # 8 lanes
            obj_y = self.y + (i * TILE_SIZE)
            if type == "river":
                obj_type = "lily" if obj_type == "log" else "log" 
            self.lanes[i] = {
                "y": obj_y,
                "direction": random.choice(self.direction),  # Randomly set direction once
                "object" : obj_type
            }
                    

    def spawn(self, obj):
        for object in self.obj_group:
            if obj != object and obj.rect.colliderect(object.rect):
                return False
        return True
    
    def add_obj(self, x, obj_type, speed, img):
        # temp fix
        if obj_type == "car":
            image = img
        else:
            image, i = self.log_type(random.choice(self.log_type_))

        if self.lanes:
            lane = random.choice(list(self.lanes.values()))
            if lane["direction"] == "right":#
                speed *= -1
                x = -130
            elif lane["direction"] == "left":
                image = py.transform.rotate(image, 180)
                speed *= 1
                x = WIDTH + 130
            

            if obj_type == "log":
                for i in range(self.num_logs):
                    log_x = x - i * (image.get_width())  # Adjust spacing to prevent overlap
                    obj = Log(image, log_x, lane["y"] + 25, speed, self.obj_group)

                    if self.spawn(obj) and lane["object"] == "log":  # no collision
                        self.obj_group.add(obj)

            elif obj_type == "lily":
                for j in range(3):
                    lil_x = x - j * (image.get_width()-100) 
                    obj = LilyPad(img, lil_x, lane["y"] +25, speed, self.obj_group)

                    if self.spawn(obj) and lane["object"] == "lily":  # no collision
                        self.obj_group.add(obj)
                        
            else:
                obj = Car(image, x, lane["y"] + 25, speed, self.obj_group)

              # no collision before adding
                if self.spawn(obj):
                    self.obj_group.add(obj)
        
        

    def draw_obj(self):
        self.obj_group.draw(screen)
    
    def update(self):
        self.obj_group.update()

## Road Class ##
class Road(LaneManager):
    def __init__(self):
        super().__init__(8, HEIGHT - (9 * TILE_SIZE), None)
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
        bool_ = False
        for car in self.obj_group:
            if frog.rect.colliderect(car.rect):
                bool_ = True
                break
        return bool_ 
            


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
        super().__init__(7,(2 * TILE_SIZE+150), "river")
        self.frog_on_log = None
        self.land = []
        self.log = None

    def draw_lanes(self):
        ## draw river ##
        for i in self.lanes:
            py.draw.rect(screen, BLUE, (0, self.lanes[i]["y"], WIDTH, TILE_SIZE))
    
    def draw_land(self):
        for i in range(1, 6):
            rect = py.Rect(250 * i - 200, 200, 150, TILE_SIZE)
        
            py.draw.rect(screen, BLUE, rect)

            self.land.append(rect)

    ## make frog at center of log for now
    def on_log(self, frog):
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
            if 200 < frog.rect.y < 600:  # between river
                return True
            else:
                for i in self.land:
                    if frog.rect.colliderect(i): 
                        return True
        return False

    
class GameState:
    def __init__(self, lives):
        self.frog_score = 0
        self.lives = lives
        self.font = py.font.Font("frogger/PressStart2P.ttf",60)
        self.font2 = py.font.Font("frogger/PressStart2P.ttf",40) # smaller font
        self.hi_score = 0 
        self.time = 60
        self.lose = False
        self.frame_count = 0

    @staticmethod
    def draw_thing():
        py.draw.rect(screen, BLACK, (0, 0, WIDTH, 150))

    def check_win(self, frog, type):
        if frog.rect.y < 150:
            self.frog_score += 10*self.time + 50  # score based on time remaining
            return "win"
        
        elif not type:
            self.frog_score -= 100
            self.lives -= 1

        elif self.lives < 0:
            return "lose"

        elif self.time == 0 :
            return "game_over"
        
    def get_hi_score(self):
        hi_score_text = self.font2.render(f"HIGH SCORE", True, (255, 90, 170))  # the text
        screen.blit(hi_score_text, (750, 10)) 

        hi_score_text2 = self.font2.render(f"{self.hi_score}", True, (255, 90, 170)) # the number
        screen.blit(hi_score_text2, (910, 60)) 
        
    def score(self):
        score_text = self.font.render(f"SCORE:{self.frog_score}", True, WHITE)
        screen.blit(score_text, (10, 10)) 

    def show_lives(self, image):
        image = py.transform.scale(image, (70, 70))
        for i in range(self.lives):
            screen.blit(image, (20 + i * 100, 70))

    def update_timer(self):
        self.frame_count += 1
        if self.frame_count >= 60:  # Every 60 frames 1 second
            self.frame_count = 0 
            if self.time > 0:
                self.time -= 1  

    def show_time(self):
        time_text = self.font.render(f"{self.time}", True, WHITE)
        screen.blit(time_text, (HEIGHT//2, 100)) 

    def draw_button(self, screen, location, size, text, mouse, events):
        button_rect = py.Rect(location[0], location[1], size[0], size[1])

        # Check for hover
        if button_rect.collidepoint(mouse):
            py.draw.rect(screen, LIGHT_GRAY, button_rect)
        else:
            py.draw.rect(screen, GRAY, button_rect)

        # Draw button text
        text_surface = self.font2.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Check for click
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse):
                return True
        return False

    def menu(self):
        running = True
        while running:
            mouse = py.mouse.get_pos()
            events = py.event.get()

            screen.fill(BLACK)  # Ensure screen is cleared before drawing

            title_surface = self.font2.render("PLAY AGIN???", True, WHITE)
            title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
            screen.blit(title_surface, title_rect)

            self.draw_button(screen, (500, 200), (200, 100), "YES", mouse, events)
            self.draw_button(screen, (500, 400), (200, 100), "NO", mouse, events)

            py.display.update()  # Update display after drawing buttons

            # Update display after drawing buttons

            for event in events:
                if event.type == py.QUIT:
                    quit()

                if event.type == py.MOUSEBUTTONDOWN:
                    if self.draw_button(screen, (500, 200), (200, 100), "YES", mouse, events):
                        return "again"
                    elif self.draw_button(screen, (500, 400), (200, 100), "NO", mouse, events):
                        return "no"
                    

            py.display.update()

    def show(self, image):
        self.get_hi_score()
        self.show_lives(image)
        self.score()
        self.show_time()


## Temporary Grid ##
def draw_grid():
    for col in range(COLS + 1):
        py.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for row in range(ROWS + 1):
        py.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))


## Game Loop ##
def frogger(hi_score, lives):
    car_CD = 0
    log_CD = 0
    lp_CD = 0 
    win = True

    lilypad = py.image.load("frogger/images/lilypad.png")

    ## Sound ##
    py.mixer.music.load("frogger/music.mp3")
    py.mixer.music.play()

    ## Game Initialization ##
    frog = Frog()
    road = Road()
    river = River()
    gt = GameState(lives)
    sprite = py.sprite.Group(frog)
    froggy_loggy = False


    gt.hi_score = hi_score
    running = True
    while running:
        screen.fill(GREEN)

        for ev in py.event.get():
            if ev.type == py.QUIT:
                running = False
            if ev.type == py.KEYDOWN:
                frog.move_frog()

        gt.update_timer()

        road.draw_lanes()
        river.draw_lanes()


        road.draw_obj()
        road.update()

        river.draw_obj()
        river.draw_land()
        river.update()
    

        if car_CD == 0:
            x = random.randint(1,7)
            road.add_obj(x,"car", -6, random.choice(Car.cars))

            car_CD = random.randint(5, 15)
        car_CD -=1    

        if log_CD == 0:
            y = random.randint(1,5)
            river.add_obj(1300,"log", -6, None)

            log_CD = random.randint(10, 20)

        log_CD -=1  

        if lp_CD == 0:
            y = random.randint(1,5)
            river.add_obj(1300,"lily", -4, lilypad)

            lp_CD = random.randint(10, 30)

        lp_CD -=1  



        if road.collision(frog):
            gt.check_win(frog, "lose")
            win = False
            frog.reset_pos()

        if not river.on_log(frog):
            if river.off_log(frog):
                win = False
                frog.reset_pos()

        if gt.check_win(frog, "lose") == "gameover" or gt.check_win(frog, "lose") == "lose":
            menu = gt.menu()
            if menu == "no": py.quit()
            else: frogger(gt.frog_score, 3)
                

        sprite.draw(screen)
        sprite.update()
        frog.on_tile(frog)


        gt.draw_thing()
        gt.show(Frog.frog_)

        temp = gt.check_win(frog, win)

        if temp == "win":
            frog.reset_pos()

        elif temp == "lose":
            gt.hi_score = gt.frog_score
            #gt.reset() 
        else:
            win = True

        draw_grid()

        animation.tick(60)
        py.display.flip()


    py.quit()

frogger(0, 3)
