from __future__ import division

import pygame
import sys
import random

from map import *
from player import *
from gold import *

class Game(object):

	wres = 1024
	hres = 768
	
	fps = 60
	
	#color = (255, 0, 255)
	color = (0, 0, 0)
	
	font_display = pygame.font.SysFont("Courier New", 16)

	def __init__(self, screen):
		random.seed()
	
		pygame.mixer.init()
		
		#self.screen = pygame.display.set_mode((self.wres, self.hres), pygame.FULLSCREEN)
		self.screen = screen
		self.clock = pygame.time.Clock()
		
		type = AreaType()
		type.size = type.tiny
		type.treasure_level = 2
		type.stairdown = True
		self.map = Map(type)
		
		self.player = Player()
		self.map.player_xy = (random.randrange(0, self.map.w), random.randrange(0, self.map.h))
		while (self.map.tile[self.map.player_xy[0]][self.map.player_xy[1]].solid):
			self.map.player_xy = (random.randrange(0, self.map.w), random.randrange(0, self.map.h))
		
		
	def update(self):
		delta = float(self.clock.tick(self.fps)) / 1000
		
		self.map.objs_lock = True
		for pos, objs in self.map.objs.items():
			for obj in objs:
				obj.update(delta)
		self.map.objs = {k: [x for x in self.map.objs[k] if x.delete == False] for k in self.map.objs.keys()}
		self.map.objs_lock = False
		
		self.map.merge_objs()
		
		self.handle_events()
		
		return 0
		
	def handle_events(self):
		prev_xy = self.map.player_xy
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				elif event.key == pygame.K_SPACE:
					self.step(prev_xy)
				elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					k = event.key
					if self.player.lust >= 50:
						if random.random() <= 0.125:
							k = random.choice((pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
					if k == pygame.K_LEFT:
						if self.map.player_xy[0] > 0 and self.player.move_to(self.map, self.map.player_xy[0] - 1, self.map.player_xy[1]):
							self.step(prev_xy)
					elif k == pygame.K_RIGHT:
						if self.map.player_xy[0] < self.map.w - 1 and self.player.move_to(self.map, self.map.player_xy[0] + 1, self.map.player_xy[1]):
							self.step(prev_xy)
					elif k == pygame.K_UP:
						if self.map.player_xy[1] > 0 and self.player.move_to(self.map, self.map.player_xy[0], self.map.player_xy[1] - 1):
							self.step(prev_xy)
					elif k == pygame.K_DOWN:
						if self.map.player_xy[1] < self.map.h - 1 and self.player.move_to(self.map, self.map.player_xy[0], self.map.player_xy[1] + 1):
							self.step(prev_xy)
				
					
		
	def step(self, prev_xy):
		if self.map.player_xy in self.map.objs:
			for obj in self.map.objs[self.map.player_xy]:
				if isinstance(obj, StairUp) and prev_xy != self.map.player_xy:
					self.map = self.map.prev
				elif isinstance(obj, StairDown) and prev_xy != self.map.player_xy:
					if not self.map.next:
						t = copy.copy(self.map.type)
						t.stairup = True
						t.stairdown = True
						t.size = random.choice((t.tiny, t.small, t.medium))
						t.treasure_level = int(random.triangular(0.0, 9.9, math.sqrt(self.map.level)))
						t.monster_level = int(random.triangular(0.0, 9.9, math.sqrt(self.map.level)))
						self.map.next = Map(t)
						self.map.next.prev = self.map
					self.map = self.map.next
					return
				obj.on_player(self.player)
			self.map.objs[self.map.player_xy][:] = [x for x in self.map.objs[self.map.player_xy] if x.delete == False]
			
		self.map.objs_lock = True
		for pos, objs in self.map.objs.items():
			for obj in objs:
				obj.step(pos, self.map, self.player)
		self.map.objs = {k: [x for x in self.map.objs[k] if x.delete == False] for k in self.map.objs.keys()}
		self.map.objs_lock = False
		
		self.player.lust += 1
		
	def draw(self):
		self.screen.fill(self.color)
	
		self.map.draw(self.screen, (0, 0))
		
		self.player.draw(self.screen, (self.map.player_xy[0] * self.map.tile_size, self.map.player_xy[1] * self.map.tile_size))
		
		pygame.draw.rect(self.screen, (0, 0, 0, 255), pygame.Rect((0, self.hres - 16), (self.wres, self.hres)))
		
		text_gold = self.font_display.render('Gold: ' + (' ' * (5 - len(str(self.player.gold)))) + str(self.player.gold), True, pygame.Color(226, 191, 31, 255))
		text_lust = self.font_display.render('Greed: ' + (' ' * (4 - len(str(self.player.lust)))) + str(self.player.lust), True, pygame.Color(96, 54, 54, 255))
		
		self.screen.blit(text_gold, (16, self.hres - 16))
		self.screen.blit(text_lust, (self.wres - 16 - text_lust.get_width(), self.hres - 16))
		
		pygame.display.flip()
	