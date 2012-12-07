import json, sys, operator, time, curses

mapdata = json.loads(open('../assets/maps/world_map.json', 'r').read())

#print mapdata['layers'][0]['name']

class Pos(tuple):
	def __init__(self, pos):
		self.pos = pos

	def __add__(self, p):
		return self.__class__(tuple(map(operator.add, self, p)))
		#return self.__class__(map(lambda x, y:x + y, self.pos, p))

	def __sub__(self, p):
		return self.__class__(tuple(map(operator.sub, self, p)))

	def __repr__(self):
		return repr(self.pos)

	def x(self):
		return self.pos[0]

	def y(self):
		return self.pos[1]


class MapLayer:
	def __init__(self, data, width, height, opacity, name):
		self.data = data
		self.width = width
		self.height = height
		self.opacity = opacity
		self.name = name

	def get_data_at(self, pos):
		offset = self.pos_to_offset(pos)
		return self.data[offset]

	def pos_to_offset(self, pos):
		#clamp the position
		y = pos.y() % self.height
		x = pos.x() % self.width

		return ((y) * self.width) + (x)

class Map:
	def __init__(self, width, height, layers):
		self.width = width
		self.height = height
		self.layers = layers



map1 = Map(mapdata['width'], mapdata['height'], [
	MapLayer(mapdata['layers'][0]['data'], mapdata['layers'][0]['width'], mapdata['layers'][0]['height'], mapdata['layers'][0]['opacity'], mapdata['layers'][0]['name']),
	MapLayer(mapdata['layers'][1]['data'], mapdata['layers'][1]['width'], mapdata['layers'][1]['height'], mapdata['layers'][1]['opacity'], mapdata['layers'][1]['name']),
	MapLayer(mapdata['layers'][2]['data'], mapdata['layers'][2]['width'], mapdata['layers'][2]['height'], mapdata['layers'][2]['opacity'], mapdata['layers'][2]['name'])
	])
#print ml.pos_to_offset(Pos((33,0)))
#print ml.get_data_at(Pos((45,56)))

#print len(map1.layers)
ml1 = map1.layers[0]

c = Pos((0,50))

def draw_tile(num):
	tile = ''
	if num == 1:
		tile += '\033[94m'
	elif num == 21:
		tile += '\033[92m'
	else:
		tile += '\033[95m'

	tile += '#' + '\033[0m'

	return tile

def tile_color(num):
	if num == 1:
		c = 2
	elif num == 21:
		c = 3
	else:
		c = 1

	return c

for cx in range(0, 50):
	output = ""
	for y in range(0, 8):
		for x in range(0, 16):
			output += draw_tile(ml1.get_data_at(Pos((x, y)) + c))
		output += "\n"


	#sys.stdout.write(output)
	#sys.stdout.write("\b"*(8*16))
	c += Pos((1,0))
	#time.sleep(1)
def draw_map(stdscr, pos, width, height):
	for y in xrange(0, height):
		for x in xrange(0, width):
			stdscr.addstr(y, x, '#', curses.color_pair(tile_color(ml1.get_data_at(Pos((x, y)) + pos))))

def main(stdscr):
	p = Pos((0,50))
	#draw_map(stdscr, p)
	for cx in range(0, 50):
		draw_map(stdscr, p + Pos((cx,0)))
		stdscr.refresh()
		time.sleep(0.1)
		


screen = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

pp = Pos((0, 50))
scrsize = screen.getmaxyx()
#main(screen)
while True:
	scrsize = screen.getmaxyx()
	draw_map(screen, pp, scrsize[1], scrsize[0]-1)
	event = screen.getch()
	if event == ord('q'):
		break
	elif event == curses.KEY_RIGHT:
		pp += Pos((1,0))
	elif event == curses.KEY_LEFT:
		pp -= Pos((1,0))
	elif event == curses.KEY_UP:
		pp -= Pos((0,1))
	elif event == curses.KEY_DOWN:
		pp += Pos((0,1)) 

#screen.addstr(0,0, '#', curses.color_pair(1))
#screen.refresh()
#time.sleep(3)

curses.endwin()
print scrsize[0], scrsize[1]