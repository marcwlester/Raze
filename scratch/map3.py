import sys, json, pygame
sys.path.append("/home/marc/Work/Raze/raze")
import maptools

class TileSet():
	def __init__(self, src, width, height, twidth, theight):
		self.src = src
		self.width = width
		self.height = height
		self.tile_width = twidth
		self.tile_height = theight

	def get_tilexy(self, offset):
		cols = self.width / self.tile_width
		rows = self.height / self.tile_height
		x = ((offset % cols) - 1) * self.tile_width
		y = ((offset / cols) * self.tile_height)
		return (x, y)



mapdata = json.loads(open('../assets/maps/world_map.json', 'r').read())

map1 = maptools.Map(mapdata['width'], mapdata['height'], [
	maptools.MapLayer(mapdata['layers'][0]['data'], mapdata['layers'][0]['width'], mapdata['layers'][0]['height'], mapdata['layers'][0]['opacity'], mapdata['layers'][0]['name'])
	,maptools.MapLayer(mapdata['layers'][1]['data'], mapdata['layers'][1]['width'], mapdata['layers'][1]['height'], mapdata['layers'][1]['opacity'], mapdata['layers'][1]['name'])
	])

def get_imgrect(tileset, tilenum):
	offset = tileset.get_tilexy(tilenum)
	rect = pygame.Rect(offset, (tileset.tile_width, tileset.tile_height))
	return rect






pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)	
tileset = TileSet(mapdata['tilesets'][0]['image'], mapdata['tilesets'][0]['imagewidth'], mapdata['tilesets'][0]['imageheight'], 32, 32)
tilesetimg = pygame.image.load('../assets/maps/' + mapdata['tilesets'][0]['image']).convert()
screen_tile_width = 26
screen_tile_height = 20
pos = maptools.Pos((50,80))
moving = {'up': False, 'down': False, 'left': False, 'right': False}
quit = False
clock = pygame.time.Clock()

while not quit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_ESCAPE):
				quit = True
			if (event.key == pygame.K_DOWN):
				moving['down'] = True
			if (event.key == pygame.K_UP):
				moving['up'] = True
			if (event.key == pygame.K_LEFT):
				moving['left'] = True
			if (event.key == pygame.K_RIGHT):
				moving['right'] = True
		if event.type == pygame.KEYUP:
			if (event.key == pygame.K_DOWN):
				moving['down'] = False
			if (event.key == pygame.K_UP):
				moving['up'] = False
			if (event.key == pygame.K_LEFT):
				moving['left'] = False
			if (event.key == pygame.K_RIGHT):
				moving['right'] = False

	move = maptools.Pos((0,0))
	if moving['up'] == True:
		move += maptools.Pos((0, -1))
	if moving['down'] == True:
		move += maptools.Pos((0, 1))
	if moving['left'] == True:
		move += maptools.Pos((-1, 0))
	if moving['right'] == True:
		move += maptools.Pos((1, 0))

	pos += move

	for layer in map1.layers:
		mapslice = layer.slice(maptools.Pos(pos), screen_tile_width, screen_tile_height)
		for y in xrange(0, screen_tile_height - 1):
			for x in xrange(0, screen_tile_width - 1):
				tile = mapslice[y][x]
				if (tile > 0):
					screen.blit(tilesetimg, (x*tileset.tile_width,y*tileset.tile_height), get_imgrect(tileset, tile))

	pygame.display.update()
	clock.tick()
	print clock.get_fps()


pygame.quit()