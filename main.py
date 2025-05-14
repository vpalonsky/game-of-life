import pygame, copy, random

# Window constants
W_WIDTH = 800
W_HEIGHT = 600
FPS = 30
BACKGROUND_COLOR = "black"

# Text constants
FONT_SIZE = 24
TEXT_COLOR = (255, 255, 255)
TEXT_TOP_MARGIN = 10
TEXT_LEFT_MARGIN = 10
TEXT_SEPARATION = 5

# Cells constants
CELL_COLOR = "white"
BASE_COLOR = "whitesmoke"
LERP_COLOR = "red4"
CELLS_ROWS = 75
CELLS_COLUMNS = 100
CELL_ALIVE = 1
CELL_DEAD = 0
CREATE_CELL = 1
DELETE_CELL = 0
RANDOM_SHAPES_CANT = 20
PATTERN_SHAPES = [
    {
        "size": [0, 1, 0, 1],
        "shape": [(0,0), (0,1), (1,0), (1,1)]
    },
    {
        "size": [-1, 2, -1, 1],
        "shape": [(0, -1), (1, -1), (-1, 0), (2, 0), (0, 1), (1, 1)]
    },
    {
        "size": [-2, 1, -1, 2],
        "shape": [(-1, -1), (0, -1), (-2, 0), (1, 0), (-1, 1), (1, 1), (0, 2)]
    },
    {
        "size": [-1, 2, 0, 1],
        "shape": [(0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1)]
    },
    {
        "size": [-1, 1, -5, 6],
        "shape": [(-1, -5), (0, -5), (1, -5), (0, -4), (0, -3), (-1, -2), (0, -2), (1, -2), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 3), (0, 3), (1, 3), (0, 4), (0, 5), (-1, 6), (0, 6), (1, 6)]
    },
    {
        "size": [-1, 1, -1, 1],
        "shape": [(0, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]
    },
    {
        "size": [-2, 2, -1, 2],
        "shape": [(-2, -1), (1, -1), (2, 0), (-2, 1), (2, 1), (-1, 2), (0, 2), (1, 2), (2, 2)]
    },
    {
        "size": [-2, 3, -2, 2],
        "shape": [(-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (-2, -1), (3, -1), (3, 0), (-2, 1), (2, 1), (0, 2)]
    },
    {
        "size": [-3, 3, -2, 2],
        "shape": [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (-3, -1), (3, -1), (3, 0), (-3, 1), (2, 1), (-1, 2), (0, 2)]
    }
]

# Pygame constants
pygame.init()
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, FONT_SIZE)

# Cells variables
total_cells = CELLS_ROWS*CELLS_COLUMNS
cell_color = pygame.Color(BASE_COLOR)
cell_width = surface.get_width()/CELLS_COLUMNS
cell_height = surface.get_height()/CELLS_ROWS

def draw_cells(cells, live_cells_color):
    population = 0

    for i in range(CELLS_ROWS):
        for j in range(CELLS_COLUMNS):
            cell_state = cells[i][j]
            cell_x = cell_width*j
            cell_y= cell_height*i

            if cell_state==CELL_ALIVE: population+=1
            draw_cell(cell_x, cell_y, cell_state, live_cells_color)

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

def generate_random_cells(cells):
    shape_fits = lambda shape_size, row, col : row >= abs(shape_size[2]) and row <= CELLS_ROWS-shape_size[3]-1 and col >= abs(shape_size[0]) and col <= CELLS_COLUMNS-shape_size[1]-1

    for i in range(RANDOM_SHAPES_CANT):
        random_cell_row = random.randint(0, CELLS_ROWS-1)
        random_cell_col = random.randint(0, CELLS_COLUMNS-1)
        random_shape = PATTERN_SHAPES[random.randint(0, len(PATTERN_SHAPES)-1)]

        if shape_fits(random_shape["size"], random_cell_row, random_cell_col):
            for (relative_col, relative_row) in random_shape["shape"]:
                new_row = random_cell_row+relative_row
                new_col = random_cell_col+relative_col

                cells[new_row][new_col] = CELL_ALIVE

def main():
    cells = [[CELL_DEAD for _ in range(CELLS_COLUMNS)] for _ in range(CELLS_ROWS)]
    running = True
    simulate = False
    generation = 0
    population = 0

    generate_random_cells(cells)

    while running:
        live_cells_color = cell_color.lerp(LERP_COLOR, 1 if population/total_cells>1 else population/(total_cells//5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    simulate = not simulate
                if event.key == pygame.K_r:
                    simulate = False
                    generation = 0
                    cells = [[CELL_DEAD for _ in range(CELLS_COLUMNS)] for _ in range(CELLS_ROWS)]
                    generate_random_cells(cells)
                if event.key == pygame.K_c:
                    simulate = False
                    generation = 0
                    cells = [[CELL_DEAD for _ in range(CELLS_COLUMNS)] for _ in range(CELLS_ROWS)]
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

        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()