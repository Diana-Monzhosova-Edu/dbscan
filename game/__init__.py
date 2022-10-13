import numpy as np
import pandas as pd
import pygame

if __name__ == '__main__':
    WIDTH = 500
    HEIGHT = 500
    FPS = 30
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    EPS = 40
    MIN_PTS = 7
    POINT_RADIUS = 5

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DBSCAN")
    clock = pygame.time.Clock()
    screen.fill(WHITE)
    pygame.display.flip()

    running = True
    points = pd.DataFrame(columns=['x', 'y', 'color'])
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                pygame.draw.circle(screen, BLACK, (x, y), POINT_RADIUS)
                pygame.display.flip()

                new_point = pd.DataFrame({'x': [x],
                                          'y': [y],
                                          'color': [BLACK]})

                points = pd.concat([points, new_point], ignore_index=True, axis=0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    blacks = []
                    for i in range(len(points)):
                        neighbors = []
                        point = points.iloc[i]
                        if point['color'] == BLACK or point['color'] == RED:
                            for j in range(len(points)):
                                if i != j:
                                    neigh_point = points.iloc[j]
                                    dist = np.sqrt(
                                        (point['x'] - neigh_point['x']) ** 2 + (point['y'] - neigh_point['y']) ** 2)
                                    if dist < EPS + POINT_RADIUS:
                                        neighbors.append(j)
                            if len(neighbors) >= MIN_PTS:
                                pygame.draw.circle(screen, BLACK, (points.iloc[i]['x'],
                                                                   points.iloc[i]['y']), EPS, 1)
                                points.at[i, 'color'] = GREEN
                                pygame.draw.circle(screen, GREEN, (points.iloc[i]['x'], points.iloc[i]['y']),
                                                   POINT_RADIUS)
                            else:
                                if point['color'] == BLACK:
                                    blacks.append(i)
                    for i in blacks:
                        for j in range(len(points)):
                            if points.iloc[j]['color'] == GREEN and i != j:
                                dist = np.sqrt(
                                    (points.iloc[i]['x'] - points.iloc[j]['x']) ** 2 + (points.iloc[i]['y'] - points.iloc[j]['y']) ** 2
                                )
                                if dist < EPS + POINT_RADIUS:
                                    points.at[i, 'color'] = RED
                                    pygame.draw.circle(screen, RED, (points.iloc[i]['x'],
                                                                       points.iloc[i]['y']), POINT_RADIUS)
                    pygame.display.flip()
