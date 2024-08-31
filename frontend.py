import pygame
import requests
import sys

WIDTH, HEIGHT = 800, 600
BACKEND_URL = "http://127.0.0.1:8000/satellite_position/"
EARTH_RADIUS = 200
SATELLITE_RADIUS = 10
CENTER = (WIDTH // 2, HEIGHT // 2)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

def get_satellite_position():
    try:
        response = requests.get(BACKEND_URL)
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
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            CENTER = (WIDTH // 2, HEIGHT // 2)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (0, 0, 255), CENTER, EARTH_RADIUS)

    sat_x, sat_y = get_satellite_position()

    scaled_sat_x = CENTER[0] + (sat_x - EARTH_RADIUS)
    scaled_sat_y = CENTER[1] + (sat_y - EARTH_RADIUS)

    if (scaled_sat_x < 0 or scaled_sat_x > WIDTH or 
        scaled_sat_y < 0 or scaled_sat_y > HEIGHT):
        print("Satellite out of bounds")

    pygame.draw.circle(screen, (255, 0, 0), (int(scaled_sat_x), int(scaled_sat_y)), SATELLITE_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
