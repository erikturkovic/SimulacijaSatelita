import pygame
import requests

INITIAL_WIDTH, INITIAL_HEIGHT = 800, 600
EARTH_DATA_URL = "http://127.0.0.1:8000/earth_data/"
SATELLITE_POSITION_URL = "http://127.0.0.1:8000/satellite_position/"
DESIRED_EARTH_DIAMETER_PIXELS = 200 
SATELLITE_RADIUS = 10

def fetch_earth_data():
    try:
        response = requests.get(EARTH_DATA_URL)
        data = response.json()
        return data['radius_km'], data['mass_kg'], data['gravity']
    except Exception as e:
        print(f"Error fetching Earth data: {e}")
        return 0, 0, 0

def fetch_satellite_position():
    try:
        response = requests.get(SATELLITE_POSITION_URL)
        data = response.json()
        return data['x'], data['y']
    except Exception as e:
        print(f"Error fetching satellite position: {e}")
        return 0, 0

def km_to_pixels(km, scale_factor):
    return km * scale_factor

def main():
    pygame.init()
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    earth_radius_km, _, _ = fetch_earth_data()
    scale_factor = DESIRED_EARTH_DIAMETER_PIXELS / (2 * earth_radius_km) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                scale_factor = DESIRED_EARTH_DIAMETER_PIXELS / (2 * earth_radius_km)

        screen.fill((0, 0, 0))


        WIDTH, HEIGHT = screen.get_size()  
        pygame.draw.circle(screen, (0, 0, 255), (WIDTH // 2, HEIGHT // 2), DESIRED_EARTH_DIAMETER_PIXELS // 2)

        sat_x, sat_y = fetch_satellite_position()

        sat_x_pixels = WIDTH // 2 + km_to_pixels(sat_x, scale_factor)
        sat_y_pixels = HEIGHT // 2 + km_to_pixels(sat_y, scale_factor)

        pygame.draw.circle(screen, (255, 0, 0), (int(sat_x_pixels), int(sat_y_pixels)), SATELLITE_RADIUS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
