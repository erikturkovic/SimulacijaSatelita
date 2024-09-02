import pygame
import requests
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Earth and Satellite Simulation")

WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
INSTANCE_BUTTON_COLOR = (200, 200, 200)

FONT = pygame.font.SysFont("Consolas", 16)

VIEW_DISTANCE = 1
DEFAULT_TIME_SCALE = 1
DEFAULT_EARTH_SCALE = 1.0
MIN_EARTH_SCALE = 0.1

satellite_colors = {}
backend_ports = range(8001, 8006)

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def fetch_from_backend(endpoint):
    for port in backend_ports:
        try:
            response = requests.get(f"http://127.0.0.1:{port}/{endpoint}")
            response.raise_for_status()
            return response.json(), port
        except requests.RequestException as e:
            print(f"Error fetching data from port {port}: {e}")
    return None, None

def draw_earth_and_satellites(earth_image, earth_data, all_satellites_data, simulated_time, buttons, earth_scale, time_scale):
    global WIDTH, HEIGHT
    WIN.fill((0, 0, 0))

    earth_x = WIDTH // 2
    earth_y = HEIGHT // 2

    actual_earth_radius = earth_data['radius_km']
    scaled_earth_radius = actual_earth_radius * earth_scale
    display_earth_radius = int(scaled_earth_radius * 0.02)

    image_size = int(display_earth_radius * 2)
    scaled_image = pygame.transform.scale(earth_image, (image_size, image_size))

    pygame.draw.circle(WIN, BLUE, (earth_x, earth_y), display_earth_radius)
    image_rect = scaled_image.get_rect(center=(earth_x, earth_y))
    WIN.blit(scaled_image, image_rect)

    displayed_satellites = set()

    for satellites_data in all_satellites_data:
        for satellite_data in satellites_data:
            name = satellite_data['name']

            if name in displayed_satellites:
                continue

            x = satellite_data['x']
            y = satellite_data['y']
            z = satellite_data['z']

            if name not in satellite_colors:
                satellite_colors[name] = get_random_color()

            color = satellite_colors[name]

            scale = VIEW_DISTANCE / (VIEW_DISTANCE + z)
            satellite_screen_x = int(earth_x + x * scale * 0.02 * earth_scale)
            satellite_screen_y = int(earth_y - y * scale * 0.02 * earth_scale)

            pygame.draw.circle(WIN, color, (satellite_screen_x, satellite_screen_y), 5)

            displayed_satellites.add(name)

    time_text = FONT.render(f"Simulated Time: {simulated_time}", True, WHITE)
    scale_text = FONT.render(f"Earth Radius: {scaled_earth_radius:.2f} km", True, WHITE)
    speed_text = FONT.render(f"Time Scale: {time_scale:.2f}", True, WHITE)

    text_x = 10
    text_y = 10
    WIN.blit(time_text, (text_x, text_y))
    WIN.blit(scale_text, (text_x, text_y + 20))
    WIN.blit(speed_text, (text_x, text_y + 40))

    list_x = WIDTH - 200
    list_y = 10
    title_text = FONT.render("Satellites:", True, WHITE)
    WIN.blit(title_text, (list_x, list_y))
    list_y += 30

    for satellite_name in displayed_satellites:
        color = satellite_colors[satellite_name]
        pygame.draw.circle(WIN, color, (list_x - 20, list_y + 10), 5)
        name_text = FONT.render(satellite_name, True, WHITE)
        WIN.blit(name_text, (list_x, list_y))
        list_y += 20

    for button in buttons:
        draw_button(WIN, button['text'], button['rect'], button['color'])

    pygame.display.update()

def draw_button(win, text, button_rect, color):
    mouse = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(win, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(win, color, button_rect)

    text_surface = FONT.render(text, True, (0, 0, 0))
    win.blit(text_surface, (button_rect.x + (button_rect.width - text_surface.get_width()) // 2,
                            button_rect.y + (button_rect.height - text_surface.get_height()) // 2))

def set_time_scale(scale):
    for port in backend_ports:
        try:
            response = requests.post(f"http://127.0.0.1:{port}/set_time_scale/?scale={scale}")
            response.raise_for_status()
            print(f"Time scale set on port {port}")
        except requests.RequestException as e:
            print(f"Error setting time scale on port {port}: {e}")

def main():
    global WIDTH, HEIGHT
    run = True
    clock = pygame.time.Clock()

    time_scale = DEFAULT_TIME_SCALE
    earth_scale = DEFAULT_EARTH_SCALE
    set_time_scale(time_scale)

    earth_image = pygame.image.load("pngs/earth.png") 
    earth_image = pygame.transform.scale(earth_image, (640, 640))

    buttons = [
        {"text": "Speed Up", "rect": pygame.Rect(10, 100, 120, 40), "color": BUTTON_COLOR},
        {"text": "Slow Down", "rect": pygame.Rect(10, 150, 120, 40), "color": BUTTON_COLOR},
        {"text": "Real Time", "rect": pygame.Rect(10, 200, 120, 40), "color": BUTTON_COLOR},
        {"text": "Increase Size", "rect": pygame.Rect(10, 250, 120, 40), "color": BUTTON_COLOR},
        {"text": "Decrease Size", "rect": pygame.Rect(10, 300, 120, 40), "color": BUTTON_COLOR},
    ]

    instance_buttons = [
        {"text": "1", "rect": pygame.Rect(10, HEIGHT - 60, 40, 40), "color": INSTANCE_BUTTON_COLOR},
        {"text": "2", "rect": pygame.Rect(60, HEIGHT - 60, 40, 40), "color": INSTANCE_BUTTON_COLOR},
        {"text": "3", "rect": pygame.Rect(110, HEIGHT - 60, 40, 40), "color": INSTANCE_BUTTON_COLOR},
        {"text": "4", "rect": pygame.Rect(160, HEIGHT - 60, 40, 40), "color": INSTANCE_BUTTON_COLOR},
        {"text": "5", "rect": pygame.Rect(210, HEIGHT - 60, 40, 40), "color": INSTANCE_BUTTON_COLOR},
    ]

    buttons.extend(instance_buttons)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                for i, button in enumerate(instance_buttons):
                    button['rect'].y = HEIGHT - 60
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        if button['text'] == "Speed Up":
                            time_scale *= 2
                            set_time_scale(time_scale)
                        elif button['text'] == "Slow Down":
                            time_scale /= 2
                            set_time_scale(time_scale)
                        elif button['text'] == "Real Time":
                            time_scale = DEFAULT_TIME_SCALE
                            set_time_scale(time_scale)
                        elif button['text'] == "Increase Size":
                            earth_scale += 0.1
                        elif button['text'] == "Decrease Size":
                            earth_scale = max(earth_scale - 0.1, MIN_EARTH_SCALE)
                        elif button['text'] in {"1", "2", "3", "4", "5"}:
                            button['color'] = (100, 100, 100)
                            print(f"Instance {button['text']} button clicked.")

        try:
            earth_data, _ = fetch_from_backend("earth_data/")
            all_satellites_data = []
            for port in backend_ports:
                satellites_data, _ = fetch_from_backend(f"satellite_positions/")
                if satellites_data:
                    all_satellites_data.append(satellites_data)

            simulated_time, _ = fetch_from_backend("simulated_time/")
            simulated_time = simulated_time['current_simulated_time']
        except Exception as e:
            print(f"Error: {e}")
            earth_data = {"radius_km": 6371}
            all_satellites_data = [[{"name": "Unknown", "x": 0, "y": 0, "z": 0}]]
            simulated_time = "Error"

        draw_earth_and_satellites(earth_image, earth_data, all_satellites_data, simulated_time, buttons, earth_scale, time_scale)

    pygame.quit()

if __name__ == "__main__":
    main()
