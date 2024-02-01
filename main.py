# pygame window and main loop
import pygame
from elements import PolyLine

# Define the screen resolution
SCREEN_RESOLUTION = (600, 600)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("PolyPy")
    clock = pygame.time.Clock()
    running = True

    # Initialize Pygame mixer and load sound file
    pygame.mixer.init(size=-8, channels=2)
    sonido1 = pygame.mixer.Sound("sound1.wav")

    # Create instances of PolyLine with different parameters
    line0 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 15, SCREEN_RESOLUTION[1] / 2 - 80],
        2,
        130,
        [sonido1],
        (0, 148, 255),
        5,
    )
    line1 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 15, SCREEN_RESOLUTION[1] / 2 - 40],
        3,
        180,
        [sonido1],
        (0, 20, 255),
        5,
    )
    line2 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 15, SCREEN_RESOLUTION[1] / 2 - 40],
        4,
        250,
        [sonido1],
        (107, 0, 255),
        5,
    )
    line3 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 15, SCREEN_RESOLUTION[1] / 2 - 40],
        5,
        250,
        [sonido1],
        (235, 0, 255),
        5,
    )
    line4 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 15, SCREEN_RESOLUTION[1] / 2 - 40],
        6,
        250,
        [sonido1],
        (255, 0, 148),
        5,
    )

    # List of PolyLine objects to be drawn and moved
    figures = [
        line0,
        # # line1,
        # # line2,
        # line3,
        # line4
    ]

    # Main game loop
    while running:
        # Set the frame rate
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("space")

        # Clear the screen
        screen.fill((0, 0, 0))

        # Move and draw each PolyLine in the figures list
        for figure in figures:
            figure.move()
            figure.draw(screen)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
