import pygame
from game_logic import variables, logic

pygame.init()

screen = pygame.display.set_mode(variables.size)
while variables.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            variables.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                variables.running = False
        elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            logic.control_mouse_event(event, screen)
    logic.check_game_stage(screen)
    pygame.display.update()
    pygame.display.flip()
pygame.quit()
