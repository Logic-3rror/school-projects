from pygame import*
import random, math

'''

Just to be clear I did get some help from AI.


'''

## display ##
init()

WIDTH, HEIGHT = 900, 1000
window = display.set_mode((WIDTH,HEIGHT))
screen = display.get_surface()

# Fonts
font_ = font.SysFont("Corbel", 40)
font_1 = font.SysFont("Corbel", 100)

# color:
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (127,127,127)

## manager ##
j = []
text=""
CD = 2000
num = 50
exit = False

class InputBox:
    def __init__(self, w, h):
        self.text = ""
        self.texts = []
        self.x = w
        self.y = h
        self.b = Rect(self.x, self.y, 700,55)
        self.active = False
        self.i = False
        self.font_size = 60  
        
    def draw_box(self):
        draw.rect(screen, BLACK, self.b, 5) 

    def calc_font_size(self, radius):
        if not self.texts:
            return 40 

        num_words = len(self.texts)
        adjusted_radius = radius * 0.7
        max_width = 2 * math.pi * adjusted_radius / num_words * 0.8
        max_height = adjusted_radius * 0.3

       
        max_font_size = 60
        min_font_size = 10  #

        # Calculate a base font size based on the number of words
        base_font_size = max(min_font_size, int(max_font_size - (num_words - 1)))

        # Fine-tune the font size
        for font_size in range(base_font_size, min_font_size - 1, -1):
            custom_font = font.SysFont("Corbel", font_size)
            if all(custom_font.render(word, True, BLACK).get_width() <= max_width and 
                   custom_font.render(word, True, BLACK).get_height() <= max_height 
                   for word in self.texts):
                return font_size

        return min_font_size

    def type_words(self, e, radius):
        if e.type == MOUSEBUTTONDOWN:  
            self.active = True if self.b.collidepoint(e.pos) else False

        if self.active and e.type == KEYDOWN:
            if e.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif e.key == K_EQUALS and self.text:
                self.texts.append(self.text)
                self.text = ""
                self.font_size = self.calc_font_size(radius)  
                print(self.texts)
                return self.texts
            else:
                self.text += e.unicode

    def draw_words(self, word, index, radius, angle_offset):
        num_words = len(self.texts)
        if num_words == 0:
            return 

        base_angle = 360 / num_words
        theta = math.radians(base_angle * (index + 0.5) - angle_offset)

        adjusted_radius = radius * 0.7

        x = WIDTH // 2 + adjusted_radius * math.cos(theta)
        y = HEIGHT // 2 + adjusted_radius * math.sin(theta) - 90

        custom_font = font.SysFont("Corbel", self.font_size)
        t_surface = custom_font.render(word, True, BLACK)

        angle = math.degrees(theta) + 180
        rotated_surface = transform.rotate(t_surface, -angle)
        rect = rotated_surface.get_rect(center=(x, y))

        screen.blit(rotated_surface, rect.topleft)



class Circle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 400
        self.color = color
        self.angle = 0
        self.speed = 50
        self.circle_surface = Surface((self.radius * 2, self.radius * 2), SRCALPHA)

    def draw(self, screen):
        self.circle_surface.fill((0, 0, 0, 0))  # Clear previous surface
        draw.circle(self.circle_surface, self.color, (self.radius, self.radius), self.radius)

        num = len(box.texts)
        if num > 0:
            for i in range(num):
                angle = math.radians((360 / num) * i)
                end_x = self.radius + self.radius * math.cos(angle)
                end_y = self.radius + self.radius * math.sin(angle)
                draw.line(self.circle_surface, BLACK, (self.radius, self.radius), (end_x, end_y), 3)

        # Rotate the circle (this includes the lines)
        rotate_surface = transform.rotate(self.circle_surface, -self.angle)
        rotate_rect = rotate_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotate_surface, rotate_rect.topleft)

        # Draw the white center circle
        draw.circle(screen, WHITE, (self.x, self.y), 20)

    def spin(self):
        self.angle += self.speed
        if self.speed > 0:
            self.speed -= 0.088
            if self.speed < 0:
                self.speed = 0
        self.draw(screen)

        rotate_surface = transform.rotate(self.circle_surface, self.angle)
        rotate_rect = rotate_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotate_surface, rotate_rect.topleft)

        #draw.circle(screen, BLACK, (self.x, self.y), 20)  # Center of the circle

    def circle_collide(self, point):
        x, y = point
        distance = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5
        return distance <= self.radius


class Manager(InputBox):
    def __init__(self, w=100, h=100):  
        super().__init__(w, h) 

        self.t_points = [(820, 420), (980, 380), (980, 470)]

    def pointer(self):
        draw.polygon(screen, GRAY, self.t_points)

    def pointer_collision(self, radius):
        word_positions = self.word_positions(radius)
        pt = self.t_points[0]  # The tip of the pointer

        for x, y, word in word_positions:
            distance = math.sqrt((x - pt[0])**2 + (y - pt[1])**2)
            if distance < 30:  # You may need to adjust this value
                print(f"Chosen word: {word}")
                return word
        return None
    
    def word_positions(self, radius):
        positions = []
        words = len(self.texts)
        for i, word in enumerate(self.texts):
            angle = 360 / words
            theta = math.radians(angle * (i + 0.5))
            adjusted_radius = radius * 0.7
            x = WIDTH // 2 + adjusted_radius * math.cos(theta)
            y = HEIGHT // 2 + adjusted_radius * math.sin(theta) - 90
            positions.append((x, y, word))
        return positions


box = InputBox(100,830)
circle = Circle(WIDTH//2, HEIGHT//2-90, RED)
manager = Manager(100, 830)

clock = time.Clock()

active = False
spin = False
while exit == False:
    #keys = key.get_pressed()
    user = mouse.get_pos()
    screen.fill((255,255,255))
    

    for e in event.get():
        if e.type == QUIT:
            exit = True

        box.type_words(e, circle.radius)
        
    if e.type == MOUSEBUTTONDOWN:
        if circle.circle_collide(e.pos):
            active = True if active == False else False  
            spin = True
   
    
    if active and spin:
        CD -= 1
        if CD == 0:
            if circle.speed == 0:  
                active = False
                spin = False
            CD = 2000
        circle.spin()
    else:
        circle.draw(screen)

    if circle.speed == 0:
        chosen_word = manager.pointer_collision(circle.radius)    
        print(f"The wheel landed on: {chosen_word}")
    

    for i in range(len(box.texts)):
        box.draw_words(box.texts[i], i, circle.radius, circle.angle)

    box.draw_box()
    manager.pointer()


    text_surface = font_.render(box.text, True, BLACK)
    screen.blit(text_surface, (box.x + 10, box.y + 10))

    
    
    clock.tick(60)
    display.flip()
