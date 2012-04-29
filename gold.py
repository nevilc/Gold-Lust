import random

from object import *

class Gold(Object):
	sprite = pygame.image.load('gfx/gold.png').convert_alpha()
	est_value = 1
	
	def __init__(self): 
		super(Gold, self).__init__()
		self.value = 1
		
	def on_player(self, player):
		player.gold += self.value
		player.lust = max(0, player.lust - self.value)
		self.delete = True
		
class GoldPile(Gold):
	sprite = pygame.image.load('gfx/goldpile.png').convert_alpha()
	est_value = 5
	
	def __init__(self):
		super(GoldPile, self).__init__()
		self.value = 5
		
class GoldStacks(Gold):
	sprite = pygame.image.load('gfx/goldstacks.png').convert_alpha()
	
	est_value = 20
	
	def __init__(self):
		super(GoldStacks, self).__init__()
		self.value = random.randrange(15, 31)
		
class GoldBag(Gold):
	sprite = pygame.image.load('gfx/goldbag.png').convert_alpha()
	
	est_value = 75
	
	def __init__(self):
		super(GoldBag, self).__init__()
		self.value = random.randrange(50, 101)
		
class GoldOre(Gold):
	sprite = pygame.image.load('gfx/goldore.png').convert_alpha()
	
	est_value = 250
	
	def __init__(self):
		super(GoldOre, self).__init__()
		self.value = 250
		
class GoldBullion(Gold):
	sprite = pygame.image.load('gfx/goldbullion.png').convert_alpha()
	
	est_value = 500
	
	def __init__(self):
		super(GoldBullion, self).__init__()
		self.value = 500
		
class GoldStatue(Gold):
	sprite = pygame.image.load('gfx/goldstatue.png').convert_alpha()
	
	est_value = 1000
	
	def __init__(self):
		super(GoldStatue, self).__init__()
		self.value = 1000