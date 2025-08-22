import pygame
import serial
import time

# Try to connect to Arduino
try:
    ser = serial.Serial('COM5', 9600, timeout=1)  # Change COM port if needed!
    time.sleep(2)  # Wait for connection
    print("Connected to Arduino on COM5")
except:
    ser = None
    print("No Arduino found, running keyboard mode only")

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joystick Game")

circleX, circleY = WIDTH // 2, HEIGHT // 2
radius = 20
speed = 3

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))  # Clear screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ser:  # If Arduino connected
        line = ser.readline().decode().strip()
        if line:
            try:
                xValue, yValue, buttonState = map(int, line.split(","))
                
                # Map joystick values
                moveX = (xValue - 512) / 512 * speed
                moveY = (yValue - 512) / 512 * speed

                circleX += moveX
                circleY += moveY

                # Reset position if button pressed
                if buttonState == 0:
                    circleX, circleY = WIDTH // 2, HEIGHT // 2

            except:
                pass
    else:
        # Keyboard fallback mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            circleX -= speed
        if keys[pygame.K_RIGHT]:
            circleX += speed
        if keys[pygame.K_UP]:
            circleY -= speed
        if keys[pygame.K_DOWN]:
            circleY += speed
        if keys[pygame.K_SPACE]:
            circleX, circleY = WIDTH // 2, HEIGHT // 2

    # Keep circle inside screen
    circleX = max(radius, min(WIDTH - radius, circleX))
    circleY = max(radius, min(HEIGHT - radius, circleY))

    # Draw circle
    pygame.draw.circle(screen, (255, 0, 0), (int(circleX), int(circleY)), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
