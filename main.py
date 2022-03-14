import pygame
pygame.init()

screen = pygame.display.set_mode([500,500])

running = True
while running:

    # "X"-ed window out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the background with white
    screen.fill((255, 255, 255))


    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # updates the screen every frame
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
