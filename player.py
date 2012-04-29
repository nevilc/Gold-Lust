from __future__ import division

import pygame

from monster import *
from effect import *

class Player(object):
	sprite = pygame.image.load('gfx/player.png').convert_alpha()
	
	def __init__(self):
		self.gold = 500
		self.lust = 0
		
	def move_to(self, map, x, y):
		if not map.tile[x][y].solid:
			if (x, y) in map.objs:
				for obj in map.objs[(x, y)]:
					if issubclass(type(obj), Attackable):
						self.attack(map, (x, y), obj)
						return True
					if obj.solid:
						break
			map.player_xy = (x, y)
			return True
		return False
		
	def attack(self, map, pos, attackable):
		attackable.hp -= 1
		map.add_obj(pos, Slash())
		
	def damage(self, map, pos, amount):
		self.gold -= self.lust * amount
		
		for i in range(self.lust * amount):
			map.add_obj(pos, GoldLoss())
			
		if self.gold <= 0:
			print 'Game Over'
			print 'You are poor!'
			#pygame.quit()
			pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
		
	def draw(self, surface, offset):
		surface.blit(self.sprite, offset)
		
