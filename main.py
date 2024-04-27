import curses
from curses import wrapper
from settings import *




class World:

    def __init__(self, stdscr, map_path, world_map):
        self.stdscr = stdscr
        self.map_path = map_path
        self.world_map = world_map

    def read_map(self):
        try:
            with open(self.map_path, 'r') as file:
                for line in file:
                    row = []
                    for char in line.strip():
                        row.append(char)
                    self.world_map.append(row)
        except FileNotFoundError:
            print(f"Файл {self.map_path} не знайдено.")
        except Exception as e:
            print(f"Помилка: {e}")
    
    def save_map(self):
        try:
            with open(self.map_path, 'w') as file:
                for row in self.world_map:
                    file.write(''.join(row) + '\n')
            print(f"Дані збережено у файлі {self.map_path}")
        except Exception as e:
            print(f"Помилка при збереженні даних у файл: {e}")

    def draw_map(self):
        for y in range(len(self.world_map)):
            for x in range(len(self.world_map[y])):
                self.stdscr.addstr(y,x, str(self.world_map[y][x]), curses.color_pair(int(self.world_map[y][x])))
    
class Player():

    def __init__(self, stdscr, player_path, speed, x, y):
        self.speed = speed
        self.player_path = player_path
        self.x = x
        self.y = y
        self.stdscr = stdscr
    
    def read_pos(self):
        try:
            with open(self.player_path, 'r') as file:
                position = file.readline().strip().split(' ')
                self.x = int(position[0])
                self.y = int(position[1])
        except FileNotFoundError:
            print(f"Файл {self.player_path} не знайдено.")
        except Exception as e:
            print(f"Помилка: {e}")
    
    def save_pos(self):
        try:
            with open(self.player_path, 'w') as file:
                file.write(f"{self.x} {self.y}")
            print(f"Позицію гравця збережено у файлі {self.player_path}")
        except Exception as e:
            print(f"Помилка при збереженні позиції гравця у файл: {e}")

    def set_player_pos(self, x, y):
        self.x = x
        self.y = y
        self.stdscr.addstr(self.y, self.x, '@', curses.color_pair(5))
    
    def move(self, dir):
        if dir == "UP":
            if self.y > 0:
                self.y -= 1
        elif dir == "DOWN":
            self.y += 1
        elif dir == "LEFT":
            if self.x > 0:
                self.x -= 1
        elif dir == "RIGHT":
            self.x += 1

def init_colors(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)#Трава
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)#Багнюка
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)#Вода
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)#Ворог
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)#Гравець

def main(stdscr):

    curses.curs_set(0)
    stdscr.clear()
    init_colors(stdscr)
    world = World(stdscr, map_path="map.txt", world_map=[])
    world.read_map()
    world.draw_map()
    stdscr.refresh()
    player = Player(stdscr, player_path="player.txt", speed=1, x=1, y=1)
    player.read_pos()
    player.set_player_pos(player.x, player.y)

    
    while True:
        key = stdscr.getch()
        if key in QUIT:
            world.save_map()
            player.save_pos()
            break

        if key in UP:
            player.move("UP")
            world.draw_map()
            player.set_player_pos(player.x, player.y)
        
        if key in DOWN:
            player.move("DOWN")
            world.draw_map()
            player.set_player_pos(player.x, player.y)
        
        if key in LEFT:
            player.move("LEFT")
            world.draw_map()
            player.set_player_pos(player.x, player.y)
        
        if key in RIGHT:
            player.move("RIGHT")
            world.draw_map()
            player.set_player_pos(player.x, player.y)
        

wrapper(main)