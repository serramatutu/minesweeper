import pygame
from pygame.locals import * # constantes

from board import Board # minesweeper packages

def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Minesweeper')

    pygame.display.flip()
    
    run(screen)
    
def run(screen):
    background = pygame.Surface(screen.get_size())
    
    b = Board()
    
    while True:
        for event in pygame.event.get(): # Processa todos os eventos
            if event.type == QUIT:
                return
            
        background.blit(b.get_surface(screen.get_size()), (0, 0))
        screen.blit(background, (0, 0))
        pygame.display.flip() # atualiza tela
        
        
    
if __name__ == "__main__": main()