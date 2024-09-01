import pygame
import requests


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth and Satellite Simulation")

WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)

FONT = pygame.font.SysFont("Consolas", 16)

def draw_earth_and_satellite(earth_data, satellite_data, simulated_time):
    WIN.fill((0, 0, 0))

    earth_x = WIDTH // 2
    earth_y = HEIGHT // 2
    earth_radius = int(earth_data['radius_km'] * 0.02)  
    pygame.draw.circle(WIN, BLUE, (earth_x, earth_y), earth_radius)


    satellite_x = int(satellite_data['x'] * 0.02 + earth_x)
    satellite_y = int(satellite_data['y'] * 0.02 + earth_y)
    pygame.draw.circle(WIN, RED, (satellite_x, satellite_y), 5)

    draw_button(WIN, "Speed Up", 650, 50)
    draw_button(WIN, "Slow Down", 650, 100)

    time_text = FONT.render(simulated_time, True, WHITE)
    WIN.blit(time_text, (10, 10))

    pygame.display.update()

def draw_button(win, text, x, y):
    mouse = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, 120, 40)
    
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(win, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(win, BUTTON_COLOR, button_rect)

    text_surface = FONT.render(text, True, (0, 0, 0))
    win.blit(text_surface, (x + (120 - text_surface.get_width()) // 2, y + (40 - text_surface.get_height()) // 2))

    return button_rect

def set_time_scale(scale):
    response = requests.post(f"http://127.0.0.1:8000/set_time_scale/?scale={scale}")
    print(response.json())

def get_simulated_time():
    response = requests.get("http://127.0.0.1:8000/simulated_time/")
    return response.json()['current_simulated_time']

def main():
    run = True
    clock = pygame.time.Clock()

    time_scale = 1000
    set_time_scale(time_scale)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if speed_up_button.collidepoint(mouse_pos):
                    time_scale *= 2
                    set_time_scale(time_scale)
                elif slow_down_button.collidepoint(mouse_pos):
                    time_scale /= 2
                    set_time_scale(time_scale)

        earth_data = requests.get("http://127.0.0.1:8000/earth_data/").json()
        satellite_data = requests.get("http://127.0.0.1:8000/satellite_position/").json()
        simulated_time = get_simulated_time()

        draw_earth_and_satellite(earth_data, satellite_data, simulated_time)

        speed_up_button = pygame.Rect(650, 50, 120, 40)
        slow_down_button = pygame.Rect(650, 100, 120, 40)

    pygame.quit()

if __name__ == "__main__":
    main()