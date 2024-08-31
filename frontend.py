import pygame
import requests
import math


WIDTH, HEIGHT = 800, 600
EARTH_RADIUS = 50
SATELLITE_RADIUS = 10
ORBIT_RADIUS = 150
CENTER = (WIDTH // 2, HEIGHT // 2)
BACKEND_URL = "http://127.0.0.1:8000/satellite_position/"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def get_satellite_position():
    try:
        response = requests.post(BACKEND_URL)
        data = response.json()
        return data['x'], data['y']
    except Exception as e:
        print(f"Error fetching satellite position: {e}")
        return 0, 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (0, 0, 255), CENTER, EARTH_RADIUS)

    sat_x, sat_y = get_satellite_position()

    sat_pos = (CENTER[0] + sat_x, CENTER[1] + sat_y)
    pygame.draw.circle(screen, (255, 0, 0), (int(sat_pos[0]), int(sat_pos[1])), SATELLITE_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
