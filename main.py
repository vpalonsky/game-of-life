import pygame
import copy

W_WIDTH = 800
W_HEIGHT = 600
FONT_SIZE=24
TEXT_COLOR = (255, 255, 255)
TEXT_TOP_MARGIN = 10
TEXT_LEFT_MARGIN = 10
TEXT_SEPARATION = 5
FRAMERATE = 30
BACKGROUND_COLOR = "black"
CELL_COLOR = "white"
BASE_COLOR = "whitesmoke"
LERP_COLOR = "red4"
CELLS_ROWS = 75
CELLS_COLUMNS = 100
CELL_ALIVE = 1
CELL_DEAD = 0
CREATE_CELL = 1
DELETE_CELL = 0

pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, FONT_SIZE)
cell_color = pygame.Color(BASE_COLOR)

cell_width = surface.get_width()/CELLS_COLUMNS
cell_height = surface.get_height()/CELLS_ROWS
total_cells = CELLS_ROWS*CELLS_COLUMNS

def draw_cells(cells, live_cells_color):
    population = 0

    for i in range(CELLS_ROWS):
        for j in range(CELLS_COLUMNS):
            cell_state = cells[i][j]
            cell_x = cell_width*j
            cell_y= cell_height*i

            live_cell = cell_state==CELL_ALIVE
            if live_cell: population+=1
            cell_color = live_cells_color if live_cell else BACKGROUND_COLOR
            pygame.draw.rect(surface, cell_color, pygame.Rect(cell_x, cell_y, cell_width, cell_height))

    return population

def draw_cell(cell_x, cell_y, cell_state, live_cells_color):
    cell_color = live_cells_color if cell_state==CELL_ALIVE else BACKGROUND_COLOR
    pygame.draw.rect(surface, cell_color, pygame.Rect(cell_x, cell_y, cell_width, cell_height))

def simulate_evolution(cells):
    next_cells = copy.deepcopy(cells)

    for i in range(1, CELLS_ROWS-1):
        for j in range(1, CELLS_COLUMNS-1):
            next_cell = cells[i][j]
            cell_alive_neigbours = 0

            for r in range(i-1, i+2):
                for c in range(j-1, j+2):
                    if r!=i or c!=j:
                        if cells[r][c]==CELL_ALIVE:
                            cell_alive_neigbours+=1

            if next_cell==CELL_ALIVE:
                if cell_alive_neigbours<2:
                    next_cell = CELL_DEAD
                elif cell_alive_neigbours>3:
                    next_cell = CELL_DEAD
            else:
                if cell_alive_neigbours==3:
                    next_cell = CELL_ALIVE

            next_cells[i][j] = next_cell

    for i in range(CELLS_ROWS):
        for j in range(CELLS_COLUMNS):
            cells[i][j] = next_cells[i][j]

def mouse_interaction(pos, edit_mode, cells, live_cells_color):
    (mouse_x, mouse_y) = pos
    cell_row = mouse_y//int(cell_height)
    cell_col = mouse_x//int(cell_width)

    cell_state = CELL_ALIVE if edit_mode==CREATE_CELL else CELL_DEAD

    cells[cell_row][cell_col] = cell_state
    draw_cell(cell_row, cell_col, cell_state, live_cells_color)

def main():
    cells = [[CELL_DEAD for _ in range(CELLS_COLUMNS)] for _ in range(CELLS_ROWS)]

    cells_mid_row = CELLS_ROWS//2
    cells_mid_col = CELLS_COLUMNS//2
    cells[cells_mid_row][cells_mid_col] = 1
    cells[cells_mid_row-1][cells_mid_col] = 1
    cells[cells_mid_row+1][cells_mid_col] = 1
    cells[cells_mid_row][cells_mid_col-1] = 1
    cells[cells_mid_row+1][cells_mid_col+1] = 1

    running = True
    simulate = False
    generation = 0
    population = 0

    while running:
        live_cells_color = cell_color.lerp(LERP_COLOR, 1 if population/(total_cells//5)>1 else population/(total_cells//5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    simulate = not simulate
            if event.type == pygame.MOUSEMOTION:
                (button1, _, button3) = event.buttons
                if not button1 and not button3: continue

                edit_mode = CREATE_CELL if button1 else DELETE_CELL

                mouse_interaction(event.pos, edit_mode, cells, live_cells_color)

        surface.fill(BACKGROUND_COLOR)

        population = draw_cells(cells, live_cells_color)

        if (simulate):
            simulate_evolution(cells)
            generation+=1

        generation_text_surface = my_font.render('Generation %d' % generation, False, TEXT_COLOR)
        population_text_surface = my_font.render('Population: %d' % population, False, TEXT_COLOR)

        surface.blit(generation_text_surface, (TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN))
        surface.blit(population_text_surface, (TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN+generation_text_surface.get_height()+TEXT_SEPARATION))


        pygame.display.flip()

        clock.tick(FRAMERATE)

    pygame.quit()

if __name__ == '__main__':
    main()