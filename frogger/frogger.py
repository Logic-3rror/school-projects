import pygame as py

py.init()
WIDTH, HEIGHT = 720,1280  # iPhone-like resolution
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Frogger Clone")

frog = py.image.load("frog.png")
frog = py.transform.scale(frog, (40,40))#
frog_rect = frog.get_rect()

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False


    screen.fill((0, 150, 0))

    screen.blit(frog, (WIDTH//2, HEIGHT - 10))
    py.display.flip()

py.quit()