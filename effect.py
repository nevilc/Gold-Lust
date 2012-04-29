from __future__ import division

import random

from object import *

class Effect(Object):
	
	
	
	def __init__(self):
		super(Effect, self).__init__()
		self.lifespan = 1.0
		self.life = self.lifespan
		self.position = (0, 0)
		self.velocity = (0, 0)
		self.acceleration = (0, 0)
		self.rect = pygame.Rect((0, 0), (self.sprite.get_width(), self.sprite.get_height()))
		
	def update(self, delta):
		self.life -= delta
		self.delete = self.life <= 0.0
		
		self.position = (self.position[0] + self.velocity[0] * delta, self.position[1] + self.velocity[1] * delta)
		self.velocity = (self.velocity[0] + self.acceleration[0] * delta, self.velocity[1] + self.acceleration[1] * delta)
		
	def draw(self, surface, offset):
		surface.blit(self.sprite, (offset[0] + self.position[0], offset[1] + self.position[1]), self.rect)
		
class Slash(Effect):
	sprite = pygame.image.load('gfx/slash.png').convert_alpha()

	def __init__(self):
		super(Slash, self).__init__()
		self.lifespan = 0.33
		self.life = self.lifespan
		self.position = (0, 0)
		self.velocity = (0, 0)
		self.acceleration = (0, 0)
		self.rect = pygame.Rect((0, 0), (0, self.sprite.get_height()))
		
	def update(self, delta):
		super(Slash, self).update(delta)
		
		self.rect.w = self.sprite.get_width() * min(1.0, delta * (self.lifespan - self.life) * 300)
		
class GoldLoss(Effect):
	sprite = pygame.image.load('gfx/gold.png').convert_alpha()
	
	def __init__(self):
		super(GoldLoss, self).__init__()
		self.lifespan = 0.2 + random.random() * 0.6
		self.life = self.lifespan
		self.position = (random.randrange(-10, 10), random.randrange(-10, 10))
		self.velocity = (random.randrange(-30.0, 30.0), random.randrange(-40.0, -20.0))
		self.acceleration = (0, 50.0)
		#self.rect = pygame.Rect((0, 0), (0, self.sprite.get_height()))
		
class SmokeCloud(Effect):
	sprite = pygame.image.load('gfx/smokecloud.png').convert_alpha()
	
	def __init__(self):
		super(SmokeCloud, self).__init__()
		self.lifespan = 0.6 + random.random() * 0.6
		self.life = self.lifespan
		self.position = (-8, -8)
		self.velocity = (0, -5.0)
		self.acceleration = (0, -5.0)
		#self.rect = pygame.Rect((0, 0), (0, self.sprite.get_height()))