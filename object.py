from __future__ import division

import pygame

class Object(object):
	
	sprite = pygame.image.load('gfx/unknown.png').convert_alpha()
	
	def __init__(self):
		#self.image = self.sprite
		self.delete = False
		self.solid = False
	
	def update(self, delta):
		pass
		
	def step(self, pos, map, player):
		pass
		
	def on_player(self, player):
		pass
	
	def draw(self, surface, offset):
		#surface.blit(self.image, offset)
		surface.blit(self.sprite, offset)