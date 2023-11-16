import numpy as np
import pygame
from pygame_gui.elements import UIButton
from pygame import gfxdraw
from Objects.grid import Grid
import PySimpleGUI as sg
import time as t
import copy as c
import matplotlib.pyplot as plt
import matplotlib.animation as animation


las_dir = {"u":"△", "r":"▷", "d":"▽", "l":"◁"}
mir_dir = {"r":"⟋", "l":"⟍"}
beam_dir = {"u":"▴", "r":"▸", "d":"▾", "l":"◂"}

def create_coordinates_between(coords, n):
    new_coords = []

    for i in range(len(coords) - 1):
        x_start, y_start, z_start = coords[i]
        x_end, y_end, z_end = coords[i + 1]

        x_values = np.linspace(x_start, x_end, num=n+2, endpoint=False)[1:]
        y_values = np.linspace(y_start, y_end, num=n+2, endpoint=False)[1:]
        z_values = np.linspace(z_start, z_end, num=n+2, endpoint=False)[1:]

        new_coords.extend(list(zip(x_values, y_values, z_values)))

    return new_coords

def translate_coord(lst, size):
    new = [((y+1)-0.5, (1+size-(x+1)-0.5), size/2) for x, y in lst]
    return new

def translate_coord_l(lst, size):
    new = [[i[1]+0.5, -1+size-(i[0]+1), size/2, i[2]] for i in lst]
    return new

def translate_coord_m(lst, size):
    new = [[i[1], size-(i[0]+1), size/2, i[2]] for i in lst]
    return new

def sim(lc, ll, lm, size, length, speed, path):
    print(lc)
    print(ll)
    print(lm)
    lc = translate_coord(lc, size)
    ll = translate_coord_l(ll, size)
    lm = translate_coord_m(lm, size)
    lc = create_coordinates_between(lc, length)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_zlim(0, size)

    ll_coordinates = ll[0][:3]
    ll_direction = ll[0][3]
    if ll_direction == 'u':
        ax.quiver(ll_coordinates[0], ll_coordinates[1]+1, ll_coordinates[2], 0, 0, 0.001, color='blue')
    elif ll_direction == 'd':
        ax.quiver(ll_coordinates[0], ll_coordinates[1]+2, ll_coordinates[2], 0, 0, -0.001, color='blue')
    elif ll_direction == 'l':
        ax.quiver(ll_coordinates[0], ll_coordinates[1]+1.5, ll_coordinates[2]-0.001, 0, 0, 0, color='blue')
    elif ll_direction == 'r':
        ax.quiver(ll_coordinates[0], ll_coordinates[1]+1.5, ll_coordinates[2]+0.001, 0, 0, 0, color='blue')

    for lm_coords in lm:
        lm_coordinates = lm_coords[:3]
        lm_direction = lm_coords[3]
        if lm_direction == 'r':
            x = np.array([[lm_coordinates[0], lm_coordinates[0]+1],
                          [lm_coordinates[0], lm_coordinates[0]+1]])
            y = np.array([[lm_coordinates[1], lm_coordinates[1]+1],
                          [lm_coordinates[1], lm_coordinates[1]+1]])
            z = np.array([[lm_coordinates[2]-2, lm_coordinates[2]-2],
                          [lm_coordinates[2]+2, lm_coordinates[2]+2]])
            ax.plot_surface(x, y, z, color='green', alpha=0.9)
        elif lm_direction == 'l':
            x = np.array([[lm_coordinates[0]+1, lm_coordinates[0]],
                          [lm_coordinates[0]+1, lm_coordinates[0]]])
            y = np.array([[lm_coordinates[1], lm_coordinates[1]+1],
                          [lm_coordinates[1], lm_coordinates[1]+1]])
            z = np.array([[lm_coordinates[2]-2, lm_coordinates[2]-2],
                          [lm_coordinates[2]+2, lm_coordinates[2]+2]])
            ax.plot_surface(x, y, z, color='green', alpha=0.9)

    line, = ax.plot([], [], [], color='red')

    def update(frame):
        if frame > 0:
    
            prev_point = lc[frame-1]
            current_point = lc[frame]
            x = np.linspace(prev_point[0], current_point[0], num=10)
            y = np.linspace(prev_point[1], current_point[1], num=10)
            z = np.linspace(prev_point[2], current_point[2], num=10)
            line.set_data(x, y)
            line.set_3d_properties(z)
        return line,

    def update_frame(frame):
        x, y, z = zip(*lc[:frame+1])
        line.set_data(x, y)
        line.set_3d_properties(z)
        return line,

    if not path:
        ani = animation.FuncAnimation(fig, update, frames=len(lc), interval=speed, blit=True)
    else:
        ani = animation.FuncAnimation(fig, update_frame, frames=len(lc), interval=speed, blit=True)

    plt.show()


sg.theme('Dark Grey 12')

start = True
grid_side = 10

layout = [[sg.Push(), sg.Text("Grid Side Length", size=(16, 1), font=("Bahnschrift", 12)), sg.Push()],
          [sg.Push(), sg.Input(size=(5,5), font='Bahnschrift '+str(12), key='len'), sg.Push()],
          [sg.Push(), sg.Button('Select',font=("Bahnschrift", 10), key='select'), sg.Push()]]

window = sg.Window("Choose Grid Size", layout, element_justification='l', resizable=True)

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WINDOW_CLOSED or event == 'exit':
        start = False
        break
    if event == 'select':
        grid_side = int(values['len'])
        break

window.close()

grid = Grid(grid_side, grid_side)

if start:
    pygame.init()
    grid_width = grid.x
    grid_height = grid.y
    if grid_side > 15:
        box_size = 30
        grid_margin = 5
        text_size = 40
        down = 68
        b_text_size = 15
    else:
        box_size = 50
        grid_margin = 5
        text_size = 60
        down = 83
        b_text_size = 24

    window_width = grid_width * (box_size + grid_margin) + grid_margin
    window_height = (grid_height + 1) * (box_size + grid_margin) + grid_margin + 50

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Reflections")

    def is_run_button_clicked(pos):
        run_button_rect = pygame.Rect(grid_margin, window_height - 40, (window_width - 3 * grid_margin) // 2, 30)
        return run_button_rect.collidepoint(pos)

    def is_reset_button_clicked(pos):
        reset_button_rect = pygame.Rect(grid_margin * 2 + (window_width - 3 * grid_margin) // 2, window_height - 40, (window_width - 3 * grid_margin) // 2, 30)
        return reset_button_rect.collidepoint(pos)

    def is_simulate_button_clicked(pos):
        simulate_button_rect = pygame.Rect(grid_margin * 2 + (window_width - 3 * grid_margin) // 2, window_height - 80, (window_width - 3 * grid_margin) // 2, 30)
        return simulate_button_rect.collidepoint(pos)

    ld = "u"
    md = "r"
    running = True
    has_run = False
    
    while running:
        window.fill((255, 255, 255)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ld = "r"
                elif event.key == pygame.K_LEFT:
                    ld = "l"
                elif event.key == pygame.K_UP:
                    ld = "u"
                elif event.key == pygame.K_DOWN:
                    ld = "d"
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    if md == "r":
                        md = "l"
                    else:
                        md = "r"
                if event.y < 0:
                    if md == "r":
                        md = "l"
                    else:
                        md = "r"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: 
                    pos = pygame.mouse.get_pos()
                    if is_run_button_clicked(pos):
                        has_run = True
                        grid.shoot()
                    elif is_reset_button_clicked(pos):
                        grid.reset()
                    elif is_simulate_button_clicked(pos):
                        if has_run:
                            sim(grid.log.log_ord, grid.logpos.log_pos['l'], grid.logpos.log_pos['m'] ,grid.x, 100, 0.01, True)
                        else:
                            print("Not yet run!!")
                    else:
                        col = pos[0] // (box_size + grid_margin)
                        row = pos[1] // (box_size + grid_margin)
                        if 0 <= col < grid_width and 0 <= row < grid_height:
                            print(row, col, ld)
                            grid.pl(row, col, ld)
                elif pygame.mouse.get_pressed()[2]: 
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (box_size + grid_margin)
                    row = pos[1] // (box_size + grid_margin)
                    if 0 <= col < grid_width and 0 <= row < grid_height:
                        print(md)
                        grid.pm(row, col, md)

        for row in range(grid_width):
            for col in range(grid_height):
                if grid.grid[row][col] == 0:
                    gfxdraw.box(window, [
                        grid_margin + col * (box_size + grid_margin),
                        grid_margin + row * (box_size + grid_margin),
                        box_size, box_size
                    ], (0, 0, 0))
                elif grid.grid[row][col].type == "l":
                        font = pygame.font.SysFont("Cambria Math", text_size)
                        text = font.render(las_dir[grid.grid[row][col].direction], True, (0, 0, 0))
                        text_rect = text.get_rect(center=(
                            grid_margin + col * (box_size + grid_margin) + box_size // 2,
                            grid_margin + row * (box_size + grid_margin) + box_size // 2
                        ))
                        window.blit(text, text_rect)
                elif grid.grid[row][col].type == "m":
                    font = pygame.font.SysFont("Cambria Math", text_size)
                    text = font.render(mir_dir[grid.grid[row][col].direction], True, (0, 0, 0))
                    text_rect = text.get_rect(center=(
                        grid_margin + col * (box_size + grid_margin) + box_size // 2,
                        grid_margin + row * (box_size + grid_margin) + box_size // 2
                    ))
                    window.blit(text, text_rect)
                elif grid.grid[row][col].type == "b":
                    font = pygame.font.SysFont("Cambria Math", b_text_size)
                    text = font.render(beam_dir[grid.grid[row][col].direction], True, (0, 0, 0))
                    text_rect = text.get_rect(center=(
                        grid_margin + col * (box_size + grid_margin) + box_size // 2,
                        grid_margin + row * (box_size + grid_margin) + box_size // 2
                    ))
                    window.blit(text, text_rect)

        gfxdraw.box(window, [grid_margin, window_height - 40, (window_width - 3 * grid_margin) // 2, 30], (30, 215, 96))
        font = pygame.font.SysFont('Bahnschrift', 24)
        text = font.render("Run", True, (255, 255, 255))
        text_rect = text.get_rect(center=(window_width // 4, window_height - 22.2))
        window.blit(text, text_rect)

        gfxdraw.box(window, [grid_margin * 2 + (window_width - 3 * grid_margin) // 2, window_height - 40, (window_width - 3 * grid_margin) // 2, 30], (193, 0, 0))
        text = font.render("Reset", True, (255, 255, 255))
        text_rect = text.get_rect(center=(3 * window_width // 4, window_height - 22.2))
        window.blit(text, text_rect)

        gfxdraw.box(window, [grid_margin * 2 + (window_width - 3 * grid_margin) // 2, window_height - 80, (window_width - 3 * grid_margin) // 2, 30], (255, 165, 0))
        text = font.render("Simulate", True, (255, 255, 255))
        text_rect = text.get_rect(center=(3 * window_width // 4, window_height - 62.2))
        window.blit(text, text_rect)
        
        display_text = ""
        display_text += las_dir[ld]
        display_text += " "
        display_text += mir_dir[md]
        display_font = pygame.font.SysFont("Cambria Math", text_size)
        display_text_surface = display_font.render(display_text, True, (0, 0, 0))
        display_text_rect = display_text_surface.get_rect(center=((window_width // 2)/2, window_height - down))
        window.blit(display_text_surface, display_text_rect)

        pygame.display.flip() 

    pygame.quit()


