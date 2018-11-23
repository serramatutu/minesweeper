#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygame
from pygame.locals import * # constantes

from board import Board, BoardState, TileState # minesweeper packages

DEFAULT_SCREEN_SIZE = 400
DEFAULT_FIELD_SIZE = 25
DEFAULT_MINE_RATIO = 0.125

class Sweeper:
    PANEL_MARGIN = 40

    @staticmethod
    def screen_size(field_size, tile_size):
        return (field_size[0] * tile_size[0], field_size[1] * tile_size[1])

    def __init__(self, 
                field_size=(DEFAULT_FIELD_SIZE, DEFAULT_FIELD_SIZE), 
                screen_size=(DEFAULT_SCREEN_SIZE, DEFAULT_SCREEN_SIZE), 
                mine_ratio=DEFAULT_MINE_RATIO):
        pygame.init()

        self._screen_size = screen_size
        self._field_size = field_size
        self._mine_ratio = mine_ratio

        self._screen = pygame.display.set_mode(self._screen_size)
        self._board = None
        self._running = False
        self._start_tick = 0
        self._time = -1

    def _restart(self):
        pygame.display.set_caption('Minesweeper')
        pygame.display.flip()

        self._board = Board(screen_size=(self._screen_size[0], self._screen_size[1] - Sweeper.PANEL_MARGIN), 
                            field_size=self._field_size,
                            mine_ratio=self._mine_ratio)

        self._running = False
        self._start_tick = 0
        self._time = -1
    
    def _mousedown(self, e):
        state = TileState.INVISIBLE
        if e.button == 3:
            state = TileState.FLAGGED
        elif e.button == 1:
            state = TileState.VISIBLE
        else:
            return True

        pos = (e.pos[0], e.pos[1] - Sweeper.PANEL_MARGIN)
        row, col = self._board.position(pos)

        if not self._running:
            self._running = True
            self._start_tick = pygame.time.get_ticks()

        return self._board.report(row, col, state)

    def run(self):
        background = pygame.Surface(self._screen.get_size())
        background.convert()
        panel = pygame.Surface((self._screen.get_size()[0], self.PANEL_MARGIN))
        panel.convert()
        
        font = pygame.font.Font(None, 40)

        clock = pygame.time.Clock()

        # mostra a imagem de inicio
        info_img = pygame.image.load('info.png')
        img_size = info_img.get_rect().size
        pos = ((self._screen_size[0] - img_size[0])//2, (self._screen_size[1] - img_size[1])//2)
        background.fill((255, 255, 255))
        background.blit(info_img, pos)
        self._screen.blit(background, (0, 0))
        pygame.display.flip() # atualiza tela
        self.waitstart(clock)

        continue_playing = True
        while continue_playing:
            self._restart()

            time_text_size = font.size('0000.000')
            mine_text = 'minas: ' + str(self._board.mines)
            mine_text_size = font.size(mine_text)
            while True:
                clock.tick(60) # 60fps

                end = False
                for event in pygame.event.get(): # Processa todos os eventos
                    if event.type == QUIT:
                        return
                    if event.type == MOUSEBUTTONDOWN:
                        v = not self._mousedown(event)
                        if not end:
                            end = v

                # desenha o mouse     
                mousepos = None
                if pygame.mouse.get_focused():
                    mousepos = pygame.mouse.get_pos()
                    mousepos = (mousepos[0], mousepos[1] - Sweeper.PANEL_MARGIN)
                background.blit(self._board.surface(mousepos), (0, Sweeper.PANEL_MARGIN))

                panel_size = panel.get_size()
                panel.fill((0, 0, 0))

                # desenha o painel
                panel.blit(font.render(mine_text, 
                                    True,
                                    (255, 255, 255),
                                    (0, 0, 0)),
                                    (5, int((panel_size[1] - mine_text_size[1])/2)))

                if self._running:
                    time_text = "{0:.3f}".format((pygame.time.get_ticks() - self._start_tick)/float(1000))
                    panel.blit(font.render(time_text, 
                                        True,
                                        (255, 255, 255),
                                        (0, 0, 0)),
                                        (panel_size[0] - time_text_size[0] - 5, int((panel_size[1] - time_text_size[1])/2)))
                background.blit(panel, (0, 0))

                self._screen.blit(background, (0, 0))
                pygame.display.flip() # atualiza tela

                if end:
                    self.end()
                    continue_playing = self.waitstart(clock)
                    break
    
    def end(self):
        self._time = pygame.time.get_ticks() - self._start_tick

        font = pygame.font.Font(None, 60)

        text = ''
        if self._board.state is BoardState.WON:
            text = 'Very much good presentation'
        else:
            text = 'You lost 2 points'

        self._board.show_all()
        screen_size = self._screen.get_size()
        text_size = font.size(text)

        # desenha a mensagem na tela
        self._screen.blit(self._board.surface(), (0, Sweeper.PANEL_MARGIN))
        s = pygame.Surface((text_size[0] + 50, text_size[1] + 50))
        s.set_alpha(180)
        size = s.get_size()
        pos = (int((screen_size[0] - size[0])/2), int((screen_size[1] - size[1])/2))
        self._screen.blit(s, pos)
        self._screen.blit(font.render(text, 
                                      True, 
                                      (255, 255, 255)),
                          (pos[0] + 25, pos[1] + 25))

        pygame.display.flip() # atualiza tela
    
    def waitstart(self, clock):
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False 
                if event.type == KEYDOWN:
                    return event.key != 27 # Esc


