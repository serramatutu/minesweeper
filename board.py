#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from array import array
import math
import random
from enum import Enum
from collections import deque
    
import pygame

class TileState(Enum):
    INVISIBLE = 0
    FLAGGED = 1
    VISIBLE = 2
    
MINE = -1

class Tile:
    def __init__(self, value=0, state=TileState.INVISIBLE):
        self._value=value
        self.state=state
        
    def __str__(self):
        if self.state is TileState.INVISIBLE:
            return ''
        elif self.state is TileState.FLAGGED:
            return 'F'
        
        if self.value >= 0:
            return str(self.value)
            
        return 'M'
        
    def setMine(self):
        self.value = MINE
        
    @property
    def isMine(self):
        return self.value == MINE
    
    @property
    def value(self):
        return self._value;
    
    @value.setter
    def value(self, v):
        if not self.isMine:         
            self._value = v

            
            
            
            
class Board:
    def __init__(self, screen_size, field_size=(20, 20), mine_ratio=0.15625):
        self._width = field_size[0]
        self._height = field_size[1]
        self._screen_size = screen_size
        
        self._board = []
        for i in range(0, self._height):
            l = []
            for i in range(0, self._width):
                l.append(Tile())
            self._board.append(l)
        
        mines = int(math.floor(mine_ratio * self._width * self._height)) # quantidade de minas

        for i in range(0, mines):
            # inicializa a mina em posição aleatória
            while True:
                row, col = random.randint(0, self._height - 1), random.randint(0, self._width - 1)
                
                if (not self._board[row][col].isMine):
                    break
            
            self._board[row][col].setMine()
            
            for i in range(0, 9):
                nrow = row + i % 3 - 1
                ncol = col + i // 3 - 1

                if (nrow < 0 or nrow >= self._height or # porco mas caguei
                    ncol < 0 or ncol >= self._width):
                    continue
                    
                if not self._board[nrow][ncol].isMine:
                    self._board[nrow][ncol].value += 1
        
        # inicializa superfície para desenho
        self._surface = pygame.Surface(screen_size)
        self._surface.convert()
        self._font = pygame.font.Font(None, 20)
        
        w = math.floor(screen_size[0]/self._width)
        h = math.floor(screen_size[1]/self._height)
        for row in range(0, self._height):
            for col in range(0, self._width):
                pygame.draw.rect(self._surface, 
                                 self._background_color(row, col), 
                                 pygame.Rect(col * w, 
                                             row * h, 
                                             w, 
                                             h)) # desenha o fundo
        
    @property
    def size(self):
        return (self._width, self._height)

    
    def _background_color(self, row, col):
        return (230, 230, 230) if (col - row) % 2 == 0 else (200, 200, 200)
            
    def position(self, screen_pos):
        return (int(math.floor(screen_pos[1]/self._height)),
                int(math.floor(screen_pos[0]/self._width)))
    
    def _flood(self, row, col):
        queue = deque()
        queue.append((row, col))
        
        x_offset = [1, 0, -1, 0]
        y_offset = [0, 1, 0, -1]

        while len(queue) > 0:
            row, col = queue.popleft()

            # atualiza o quadrado atual
            self._update_tile(row, col, TileState.VISIBLE)

            accept_non_zero = self._board[row][col].value is 0
            for i in range(0, 4):
                nrow = row + x_offset[i]
                ncol = col + y_offset[i]

                tile = self._board[nrow][ncol]
                if (nrow < 0 or nrow >= self._height or
                    ncol < 0 or ncol >= self._width or
                    tile.state is not TileState.INVISIBLE): # Sò reprocessa se for invisível
                    continue
                    
                # adiciona todos os vizinhos elegíveis na fila
                if (accept_non_zero or tile.value is 0) and not tile.isMine:
                    queue.append((nrow, ncol))

    def report(self, row, col, state):
        if self._board[row][col].value is 0:
            self._flood(row, col)
        else:
            self._update_tile(row, col, state)

    def _update_tile(self, row, col, state):    
        tile = self._board[row][col]
        tile.state = state

        text = str(tile)
        size = self._font.size(text)

        # cor do tile
        color = (0, 180, 0)
        if tile.state is TileState.FLAGGED:
            color = (0, 0, 0)
        elif 1 <= tile.value <= 2:
            color = (255, 128, 0)
        elif tile.value > 2:
            color = (255, 0, 0)
        elif tile.isMine:
            color = (0, 0, 255)

        w = math.floor(self._screen_size[0]/self._width)
        h = math.floor(self._screen_size[1]/self._height)
        self._surface.blit(self._font.render(text,
                                             True,
                                             color,
                                             self._background_color(row, col)),
                           (col * w + (w - size[0])/2, 
                            row * h + (h - size[1])/2)
                          )

    def surface(self, mousepos=None):
        s = pygame.Surface(self._screen_size)
        s.blit(self._surface, (0, 0))
        
        if mousepos is not None:
            pos = self.position(mousepos)
            w = math.floor(self._screen_size[0]/self._width)
            h = math.floor(self._screen_size[1]/self._height)
            pygame.draw.rect(s, 
                             (130, 130, 130), 
                             pygame.Rect(pos[1] * w, 
                                         pos[0] * h, 
                                         w, 
                                         h),
                                         2)
        return s