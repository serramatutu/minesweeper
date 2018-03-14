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
        if self.state is TileState.INVISIBLE or self.value == 0:
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

            
class BoardState(Enum):
    IN_GAME = 0
    WON = 1
    LOST = 2  
            
            
class Board:
    def __init__(self, screen_size, field_size=(20, 20), mine_ratio=0.15625):
        self._width = field_size[0]
        self._height = field_size[1]
        self._screen_size = screen_size
        
        self._generated = False
        # inicializa a board vazia
        self._board = []
        for i in range(0, self._height):
            l = []
            for i in range(0, self._width):
                l.append(Tile())
            self._board.append(l)
        
        self._mines = int(math.floor(mine_ratio * self._width * self._height)) # quantidade de minas
        self._remaining_tiles = self._width * self._height - self._mines # condição de vitória
        
        # inicializa superfície para desenho
        self._surface = pygame.Surface(screen_size)
        self._surface.convert()
        w, h = self.tile_size()
        self._font = pygame.font.Font(None, max(w, h))
        
        w, h = self.tile_size()
        for row in range(0, self._height):
            for col in range(0, self._width):
                pygame.draw.rect(self._surface, 
                                 self._background_color(row, col), 
                                 pygame.Rect(col * w, 
                                             row * h, 
                                             w, 
                                             h)) # desenha o fundo

    def _generate(self, clicked_row, clicked_col):
        for i in range(0, self._mines):
            # inicializa a mina em posição aleatória
            while True:
                row, col = random.randint(0, self._height - 1), random.randint(0, self._width - 1)
                
                if ((row != clicked_row or col != clicked_col) and 
                    not self._board[row][col].isMine):
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

        self._state = BoardState.IN_GAME
        self._generated = True

    @property
    def state(self):
        return self._state
    
    def _die(self):
        self._state = BoardState.LOST

    def _win(self):
        self._state = BoardState.WON

    @property
    def size(self):
        return (self._width, self._height)

    
    def _background_color(self, row, col):
        tile = self._board[row][col]

        if tile.state is TileState.FLAGGED:
            return (230, 150, 230) if (col - row) % 2 == 0 else (200, 120, 200)
        elif tile.state is TileState.VISIBLE:
            if tile.isMine:
                return (0, 0, 0)
            if tile.value == 0:
                return (150, 230, 150) if (col - row) % 2 == 0 else (120, 200, 120)
            if 1 <= tile.value <= 2:
                return (230, 230, 150) if (col - row) % 2 == 0 else (200, 200, 120) 
            if tile.value > 2:
                return (230, 150, 150) if (col - row) % 2 == 0 else (200, 120, 120) 

        return (230, 230, 230) if (col - row) % 2 == 0 else (200, 200, 200)

    def _font_color(self, row, col):
        tile = self._board[row][col]

        if tile.state is TileState.FLAGGED:
            return (120, 0, 120)
        if tile.isMine:
            return (255, 0, 0)
        if 1 <= tile.value <= 2:
            return (200, 100, 0)
        if tile.value > 2:
            return (200, 0, 0)

        return (0, 180, 0)
            
    def tile_size(self):
        return (math.floor(self._screen_size[0]/self._width),
                math.floor(self._screen_size[1]/self._height))

    def position(self, screen_pos):
        w, h = self.tile_size()
        return (int(math.floor(screen_pos[1]/h)),
                int(math.floor(screen_pos[0]/w)))
    
    def _flood(self, row, col):
        queue = deque()
        queue.append((row, col))

        processed = set() # evita que coloque o mesmo tile duas vezes na fila
        while len(queue) > 0:
            row, col = queue.popleft()

            # atualiza o quadrado atual
            self._update_tile(row, col, TileState.VISIBLE)

            accept = self._board[row][col].value is 0
            for i in range(0, 9):
                nrow = row + i % 3 - 1
                ncol = col + i // 3 - 1

                if (nrow < 0 or nrow >= self._height or
                    ncol < 0 or ncol >= self._width):
                    continue
                
                tile = self._board[nrow][ncol]

                if tile.state is not TileState.INVISIBLE: # Só reprocessa se for invisível
                    continue
                    
                # adiciona todos os vizinhos elegíveis na fila
                pos = (nrow, ncol)
                if (not pos in processed and 
                    (accept and (accept or tile.value is 0))
                    and not tile.isMine):
                    queue.append(pos)
                    processed.add(pos)

    def report(self, row, col, state):
        if not self._generated:
            self._generate(row, col)

        if state is TileState.INVISIBLE:
            raise ValueError()

        if self._board[row][col].isMine and state is not TileState.FLAGGED:
            self._die()
            return False

        if self._board[row][col].value is 0:
            self._flood(row, col)
        else:
            self._update_tile(row, col, state)

        # checa se ganhou
        if self._remaining_tiles <= 0:
            self._win()
            return False

        return True

    def _update_tile(self, row, col, state):    
        tile = self._board[row][col]

        if (tile.state is TileState.FLAGGED and
            state is TileState.FLAGGED):
            state = TileState.INVISIBLE

        tile.state = state

        if state is TileState.VISIBLE: # VISIBLE
            self._remaining_tiles -= 1


        text = str(tile)
        size = self._font.size(text)

        w, h = self.tile_size()
        color = self._font_color(row, col)
        background = self._background_color(row, col)
        pygame.draw.rect(self._surface, # limpa o fundo
                         background,
                         pygame.Rect(col * w, row * h, w, h))
        self._surface.blit(self._font.render(text,
                                             True,
                                             color,
                                             background),
                           (col * w + (w - size[0])/2, 
                            row * h + (h - size[1])/2)
                          )

    def surface(self, mousepos=None):
        s = pygame.Surface(self._screen_size)
        s.blit(self._surface, (0, 0))
        
        if mousepos is not None:
            row, col = self.position(mousepos)
            w, h = self.tile_size()
            pygame.draw.rect(s, 
                             (130, 130, 130), 
                             pygame.Rect(col * w, 
                                         row * h, 
                                         w, 
                                         h),
                                         2)
        return s