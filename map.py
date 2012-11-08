from util import *

import pygame

import random
import math
import copy

from gold import *
from stair import *
from barrel import *
from goblin import *
from leprechaun import *

class Tile(object):
	def __init__(self):
		self.sprite = None
		self.solid = True
		
	def draw(self, surface, offset):
		surface.blit(self.sprite, offset) 
		

tile_null = Tile()
tile_null.sprite = pygame.image.load('gfx/tile_null.png').convert_alpha()

tile_cave_floor = Tile()
tile_cave_floor.solid = False
tile_cave_floor.sprite = pygame.image.load('gfx/tile_cave_floor.png').convert_alpha()


class AreaType(object):
	# sizes
	tiny = 0
	small = 1
	medium = 2
	large = 3
	huge = 4
	
	# environments
	cave = 0
	dungeon = 1
	tunnels = 2
	building = 3
		

	def __init__(self):
		self.treasure_level = 0
		self.monster_level = 0
		self.size = AreaType.tiny
		self.environment = AreaType.cave
		self.stairup = False
		self.stairdown = False





class Room(object):
	__size = {
		AreaType.tiny: 		(4, 	7),
		AreaType.small: 	(8, 	11),
		AreaType.medium: 	(10, 	17),
		AreaType.large:		(18, 	25),
		AreaType.huge:		(30, 	37)
		}
		
	__gold = {
		0: (0, 1),
		1: (0, 4),
		2: (1, 11),
		3: (10, 31),
		4: (40, 61),
		5: (75, 101),
		6: (100, 201),
		7: (250, 501),
		8: (500, 1001),
		9: (1000, 2000)
		}
		
	__monster = {
		0: (0, 1, 0, 1),
		1: (0, 1, 0, 1),
		2: (1, 2, 0, 1),
		3: (1, 3, 0, 2),
		4: (1, 5, 0, 2),
		5: (2, 5, 0, 2),
		6: (2, 7, 0, 2),
		7: (2, 9, 0, 2),
		8: (2, 9, 0, 3),
		9: (2, 9, 1, 3)
		}
		

	def __init__(self, type):
		self.generate(type)
	
	def fill(self, tile):
		self.tile[int(self.w / 2)][int(self.h / 2)] = tile_null
		self.subfill(tile, (self.w / 2, self.h / 2))
		
	def subfill(self, tile, pos):
		x = int(pos[0])
		y = int(pos[1])
		if x < 0 or y < 0 or x >= self.w or y >= self.h or self.tile[x][y] != tile_null:
			return
		
		self.tile[x][y] = tile
		self.subfill(tile, (x + 1, y))
		self.subfill(tile, (x - 1, y))
		self.subfill(tile, (x, y + 1))
		self.subfill(tile, (x, y - 1))
		
	
		
		
	def add_obj(self, pos, obj):	
		if pos in self.objs:
			self.objs[pos].append(obj)
		else:
			self.objs[pos] = [obj]
		
	def include_obj(self, obj, force_empty = False):
		failures = 0
		failures_allowed = 20
		while failures < failures_allowed:
			failures += 1
			x = random.randrange(0, self.w)
			y = random.randrange(0, self.h)
			
			if self.tile[x][y].solid:
				continue
			if force_empty and (x, y) in self.objs:
				continue
			self.add_obj((x, y), obj)
			return (x, y)
		return None
		
	def generate(self, type):
		self.w = random.randrange(self.__size[type.size][0], self.__size[type.size][1])
		self.h = random.randrange(self.__size[type.size][0], self.__size[type.size][1])
		
		
		self.tile = [[tile_null for i in range(self.h)] for j in range(self.w)]
		
		self.objs = {}
	
		self.exit_points = []
	
		if (type.environment == AreaType.cave):
			N = (random.randrange(round(self.w / 4), round(self.w * 3 / 4)), 0)
			W = (0, random.randrange(round(self.h / 4), round(self.h * 3 / 4)))
			S = (random.randrange(round(self.w / 4), round(self.w * 3 / 4)), self.h - 1)
			E = (self.w - 1, random.randrange(round(self.h / 4), round(self.h * 3 / 4)))
			
			self.exit_points = [N, W, S, E]
			
			pos = W
			for goal, pull in zip((N, E, S, W), ((0, 0), (self.w, 0), (self.w, self.h), (0, self.h))):
				target = (round((goal[0] + pull[0]) / 2), round((goal[1] + pull[1]) / 2))
				dist = math.sqrt((pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2)
				switch_dist = random.triangular(0.0, dist, dist / 2)
				did_switch = False
				while (pos != goal):
					self.tile[pos[0]][pos[1]] = tile_cave_floor
					
					if not did_switch and math.sqrt((pos[0] - target[0]) ** 2 + (pos[1] - target[1]) ** 2) <= switch_dist:
						did_switch = True
						target = goal
					
					xdiff = goal[0] - pos[0]
					ydiff = goal[1] - pos[1]
					
					# x/y forward (toward target)
					xf = math.fabs(xdiff) / (math.fabs(xdiff) + math.fabs(ydiff))
					yf = math.fabs(ydiff) / (math.fabs(xdiff) + math.fabs(ydiff))
					
					# x/y backward
					xb = xf * yf * yf
					yb = xf * xf * yf
		
					rx = random.random()
					ry = random.random()
					if rx - xf <= 0:
						pos = (int(max(0, min(self.w - 1, pos[0] + math.copysign(1, xdiff)))), pos[1])
					elif rx - xf - xb <= 0:
						pos = (int(max(0, min(self.w - 1, pos[0] - math.copysign(1, xdiff)))), pos[1])
					
					if ry - yf <= 0:
						pos = (pos[0], int(max(0, min(self.h - 1, pos[1] + math.copysign(1, ydiff)))))
					elif ry - yf - yb <= 0:
						pos = (pos[0], int(max(0, min(self.h - 1, pos[1] - math.copysign(1, ydiff)))))
						
			self.fill(tile_cave_floor)
	
			g = random.randrange(self.__gold[type.treasure_level][0], self.__gold[type.treasure_level][1])
			
			while g > 0:
				obj = None
				sum = 0
				for i in (Gold(), GoldPile(), GoldStacks(), GoldBag(), GoldOre(), GoldBullion(), GoldStatue()):
					if g >= i.est_value:
						sum += int(math.sqrt(i.est_value))
				val = random.randrange(0, sum + 1)
				for i in (Gold(), GoldPile(), GoldStacks(), GoldBag(), GoldOre(), GoldBullion(), GoldStatue()):
					val -= int(math.sqrt(i.est_value))
					if val <= 0:
						self.include_obj(i, False)
						g -= i.est_value
						break
			
			

			while random.random() <= 0.45:
				self.include_obj(Barrel(), True)
				
			for i in range(random.randrange(self.__monster[type.monster_level][0], self.__monster[type.monster_level][1])):
				self.include_obj(Goblin(), True)
				
			for i in range(random.randrange(self.__monster[type.monster_level][2], self.__monster[type.monster_level][3])):
				self.include_obj(Leprechaun(), True)
		

class Map(object):
	tile_size = 16
	
	deepest = 0

	# tile min, tile max, room min, room max
	__size = {
		AreaType.tiny: 		(12, 	16, 	1, 	3),
		AreaType.small: 	(20, 	30, 	2,	4),
		AreaType.medium: 	(36, 	48,		3,  6),
		AreaType.large:		(64, 	80, 	5,	9),
		AreaType.huge:		(128, 	160,	10,	13)
		}
	

	def __init__(self, type):
		self.level = self.deepest
		self.deepest += 1
		
		self.player_xy = (0, 0)
	
		self.prev = None
		self.next = None
	
		self.generate(type)
		
		
		
		
		
	def add_room(self, pos, room):
		for x in range(room.w):
			for y in range(room.h):
				self.tile[pos[0] + x][pos[1] + y] = room.tile[x][y]
				#self.obj[pos[0] + x][pos[1] + y].extend(room.tile[x][y])
		objs_new = {(k[0] + pos[0], k[1] + pos[1]): v for k, v in room.objs.items()}
		self.objs = merge_dict(self.objs, objs_new)
				
		self.rooms.append((pos, room))
		
	
		
		
	def generate(self, type):
		self.w = random.randrange(self.__size[type.size][0], self.__size[type.size][1])
		self.h = random.randrange(self.__size[type.size][0], self.__size[type.size][1])
		
		self.tile = [[tile_null for i in range(self.h)] for j in range(self.w)]
		self.objs = {}
		self.objs_temp = {}
		self.objs_lock = False
		
		self.rooms = []
		
		self.type = type
		
		
		if (type.environment == type.cave):
			failures = 0
			
			failures_allowed = 5
			
			while len(self.rooms) < 2 or failures < failures_allowed:
				r = Room(type)
				x = random.randrange(0, self.w - r.w + 1)
				y = random.randrange(0, self.h - r.h + 1)
				w = r.w
				h = r.h
				
				rect = pygame.Rect((x, y), (w, h))
				
				collide = False
				
				for t in self.rooms:
					x2 = t[0][0]
					y2 = t[0][1]
					r2 = t[1]
					w2 = r2.w
					h2 = r2.h
					rect2 = pygame.Rect((x2, y2), (w2, h2))
					if (rect.colliderect(rect2)):
						collide = True
						break
				
				if collide:
					failures = failures + 1
					continue
					
				if type.stairup:
					self.player_xy = r.include_obj(StairUp(), True)
					self.player_xy = (self.player_xy[0] + x, self.player_xy[1] + y)
					type.stairup = False
				elif type.stairdown:
					r.include_obj(StairDown(), True)
					type.stairdown = False
				
				self.add_room((x, y), r)
				
			# connect rooms
			r = random.choice(self.rooms)
			rcon = [r]
			runcon = [x for x in self.rooms if x != r]
			tuples = []
			
			while len(runcon) != 0:
				r = random.choice(rcon)
				t1 = r[1].exit_points[random.randrange(0, 4)]
				t1 = (t1[0] + r[0][0], t1[1] + r[0][1])
				r2 = random.choice(runcon)
				t2 = r2[1].exit_points[random.randrange(0, 4)]
				t2 = (t2[0] + r2[0][0], t2[1] + r2[0][1])
				
				tuples.append((t1, t2))
				
				rcon.append(r2)
				runcon = [x for x in runcon if x != r2]
				
			for t in tuples:
				x = t[0][0]
				y = t[0][1]
				x2 = t[1][0]
				y2 = t[1][1]
				
				px = x
				py = y
				
				while (px, py) != (x2, y2):
					self.tile[px][py] = tile_cave_floor
					rand = random.random()
					if rand <= .35:
						px += int(math.copysign(1, x2 - px))
					elif rand <= .70:
						py += int(math.copysign(1, y2 - py))
					elif rand <= .85:
						px -= int(math.copysign(1, x2 - px))
					else:
						py -= int(math.copysign(1, y2 - py))
					px = max(0, min(self.w - 1, px))
					py = max(0, min(self.h - 1, py))
	
	def merge_objs(self):
		if self.objs_lock:
			print('objs_lock error')
		else:
			self.objs = merge_dict(self.objs, self.objs_temp)
			self.objs_temp = {}
	
	def add_obj(self, pos, obj):
		if self.objs_lock:
			if pos in self.objs_temp:
				self.objs_temp[pos].append(obj)
			else:
				self.objs_temp[pos] = [obj]
		else:
			if pos in self.objs:
				self.objs[pos].append(obj)
			else:
				self.objs[pos] = [obj]
			
	def move_obj(self, pos, obj):
		self.objs = {k: [x for x in self.objs[k] if x != obj] for k in self.objs.keys()}
		self.add_obj(pos, obj)
	
	def draw(self, surface, offset):
		for x in range(self.w):
			for y in range(self.h):
				self.tile[x][y].draw(surface, addt(offset, (x * self.tile_size, y * self.tile_size)))
		for pos, objs in self.objs.items():
			for obj in objs:
				obj.draw(surface, (pos[0] * self.tile_size, pos[1] * self.tile_size))
			