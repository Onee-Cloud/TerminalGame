import curses
from curses import wrapper
from settings import *

class World:

    def __init__(self, stdscr, map_path, world_map, width, height):
        self.stdscr = stdscr
        self.map_path = map_path
        self.world_map = world_map
        self.width = width
        self.height = height

    def read_map(self):
        try:
            with open(self.map_path, 'r') as file:
                for y, line in enumerate(file):
                    for x, char in enumerate(line.strip()):
                        if x < self.width and y < self.height:
                            self.world_map[y][x] = char
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

class Editor:
    def __init__(self, stdscr, current_color_id, current_mouse_pos_x, current_mouse_pos_y):
        self.stdscr = stdscr
        self.current_color_id = current_color_id
        self.current_mouse_pos_x = current_mouse_pos_x
        self.current_mouse_pos_y = current_mouse_pos_y
    
    def init_colors(self):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)#Трава
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)#Пісок
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)#Вода
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)#Службовий бар'єр
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)#Ворог
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_WHITE)#Гравець

    def draw_ui(self):
        self.stdscr.addstr(25, 5, "Щоб обрати колір для малювання натисніть одну з цих клавіш: 1 (Земля), 2 (Пісок), 3 (Вода)")

    def get_current_mouse_pos(self):
        _, self.current_mouse_pos_x, self.current_mouse_pos_y, _, _ = curses.getmouse()
    
    def edit_map(self, world):
        if (self.current_mouse_pos_x > 0 and self.current_mouse_pos_x < 119) and (self.current_mouse_pos_y > 0 and self.current_mouse_pos_y < 20):
            world.world_map[self.current_mouse_pos_y][self.current_mouse_pos_x] = str(self.current_color_id)
            self.stdscr.addstr(self.current_mouse_pos_y, self.current_mouse_pos_x, str(self.current_color_id), curses.color_pair(int(self.current_color_id)))

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
        self.stdscr.addstr(self.y, self.x, '@', curses.color_pair(6))
    
    def move(self, dir, world):
        if dir == "UP":
            if self.y > 0:
                if int(world.world_map[self.y-1][self.x]) not in CANT_WALK:
                    self.y -= 1
        elif dir == "DOWN":
            if int(world.world_map[self.y+1][self.x]) not in CANT_WALK:
                    self.y += 1
        elif dir == "LEFT":
            if self.x > 0:
                if int(world.world_map[self.y][self.x-1]) not in CANT_WALK:
                    self.x -= 1
        elif dir == "RIGHT":
            if self.x + 1 < world.width:
                if int(world.world_map[self.y][self.x+1]) not in CANT_WALK:
                    self.x += 1
        
        world.draw_map()
        self.set_player_pos(self.x, self.y)

def main(stdscr):

    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.clear()
    world = World(stdscr, map_path="map.txt", world_map=[['4'] * 120 for _ in range(21)], width=120, height=21)
    world.read_map()
    world.draw_map()
    editor = Editor(stdscr, current_color_id=1, current_mouse_pos_x=0, current_mouse_pos_y=0)
    editor.init_colors()
    player = Player(stdscr, player_path="player.txt", speed=1, x=1, y=1)
    player.read_pos()
    player.set_player_pos(player.x, player.y)
    editor.draw_ui()
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()

        if key in QUIT:
            world.save_map()
            player.save_pos()
            break

        if key in UP:
            player.move("UP", world)
        
        if key in DOWN:
            player.move("DOWN", world)
        
        if key in LEFT:
            player.move("LEFT", world)
        
        if key in RIGHT:
            player.move("RIGHT", world)

        if key in GREEN:
            editor.current_color_id = 1
        
        if key in YELLOW:
            editor.current_color_id = 2
        
        if key in BLUE:
            editor.current_color_id = 3
        
        if key in BLACK:
            editor.current_color_id = 4

        if key == curses.KEY_MOUSE:
            editor.get_current_mouse_pos()
            editor.edit_map(world)
            stdscr.addstr(21, 20, f"Курсор миші: ({editor.current_mouse_pos_x}, {editor.current_mouse_pos_y})")
            stdscr.refresh()  

wrapper(main)