import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot Trajectory Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Robot trajectory
trajectory = [
    (0, 0), (0, 10), (10, 10), (20, 10), (20, 0),
    (20, 10), (20, 20), (10, 20), (0, 20), (10, 20),
    (20, 20), (10, 20), (10, 10), (10, 0), (10, 10)
]

# Scale factor to fit the trajectory on the screen
scale = 20
offset_x, offset_y = 200, 100

# Font for text
font = pygame.font.Font(None, 24)

# Animation settings
current_step = 0
animation_progress = 0
animation_speed = 0.025  # Halved from the previous value of 0.05

clock = pygame.time.Clock()

def draw_trajectory():
    for i in range(1, len(trajectory)):
        start = trajectory[i-1]
        end = trajectory[i]
        start_pos = (start[0] * scale + offset_x, height - (start[1] * scale + offset_y))
        end_pos = (end[0] * scale + offset_x, height - (end[1] * scale + offset_y))
        pygame.draw.line(screen, BLUE, start_pos, end_pos, 2)

running = True
animation_started = False
animation_completed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not animation_started:
            if event.key == pygame.K_SPACE:
                animation_started = True

    screen.fill(WHITE)

    # Draw grid
    for x in range(0, width, scale):
        pygame.draw.line(screen, (200, 200, 200), (x + offset_x, offset_y), (x + offset_x, height - offset_y))
    for y in range(0, height, scale):
        pygame.draw.line(screen, (200, 200, 200), (offset_x, y + offset_y), (width - offset_x, y + offset_y))

    # Draw heat source
    heat_source_pos = (10 * scale + offset_x, height - (10 * scale + offset_y))
    pygame.draw.circle(screen, GREEN, heat_source_pos, 15)
    heat_text = font.render("Heat Source", True, BLACK)
    screen.blit(heat_text, (heat_source_pos[0] + 20, heat_source_pos[1] - 10))

    # Calculate and draw robot position
    if animation_started:
        if animation_completed:
            robot_pos = trajectory[-1]  # Use the last position in the trajectory
            draw_trajectory()  # Draw the full trajectory at the end
        else:
            prev_pos = trajectory[int(current_step)]
            next_pos = trajectory[min(int(current_step) + 1, len(trajectory) - 1)]
            robot_pos = (
                prev_pos[0] + (next_pos[0] - prev_pos[0]) * animation_progress,
                prev_pos[1] + (next_pos[1] - prev_pos[1]) * animation_progress
            )
        
        robot_x = robot_pos[0] * scale + offset_x
        robot_y = height - (robot_pos[1] * scale + offset_y)
        pygame.draw.circle(screen, RED, (int(robot_x), int(robot_y)), 10)
    else:
        start_text = font.render("Press SPACEBAR to start the animation", True, BLACK)
        screen.blit(start_text, (width // 2 - 150, height // 2))

    # Display "Animation Completed" when the robot reaches the heat source
    if animation_completed:
        complete_text = font.render("Animation Completed - Robot at Heat Source", True, BLACK)
        screen.blit(complete_text, (width // 2 - 150, 50))

    pygame.display.flip()

    # Update animation
    if animation_started and not animation_completed:
        animation_progress += animation_speed
        if animation_progress >= 1:
            current_step += 1
            animation_progress = 0

        if current_step >= len(trajectory) - 1:
            animation_completed = True
            current_step = len(trajectory) - 1
            animation_progress = 1

    clock.tick(60)

pygame.quit()
sys.exit()