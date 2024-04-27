import curses
from curses import wrapper

world_map = []

class Player:
    def __init__(self, speed, x, y):
        self.speed = speed
        self.x = x
        self.y = y
    
    def read_pos(self):
        try:
            with open("player.txt", 'r') as file:
                position = file.readline().strip().split(' ')
                self.x = int(position[0])
                self.y = int(position[1])
        except FileNotFoundError:
            print(f"Файл player.txt не знайдено.")
        except Exception as e:
            print(f"Помилка: {e}")

def read_map():
    with open("map.txt", 'r') as file:
        for line in file:
            row = []
            for char in line.strip():
                row.append(char)
            world_map.append(row)

def init_colors(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)#Трава
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)#Багнюка
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)#Вода
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)#Ворог
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)#Гравець

def draw_map(stdscr):
    for y in range(len(world_map)):
        for x in range(len(world_map[y])):
            stdscr.addstr(y,x, str(world_map[y][x]), curses.color_pair(int(world_map[y][x])))

def main(stdscr):
    init_colors(stdscr)
    read_map()
    stdscr.clear()
    draw_map(stdscr)
    stdscr.refresh()
    
    player = Player(speed=1,x=1,y=1)
    player.read_pos()
    stdscr.addstr(player.x, player.y, '@', curses.color_pair(5))
    curses.curs_set(0)
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        

wrapper(main)