from __future__ import division

import sys
import os
import pygame

pygame.init()
screen = pygame.display.set_mode((1024, 768))

from game import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

while True:
	game = Game(screen)

	while game.update() != -1:
		game.draw()
		
	del game