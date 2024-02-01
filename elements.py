import numpy as np
import pygame

from constants import COLOR, quarter


class Circle:
    """
    Class representing a circle with optional growing shadow circles.
    """

    def __init__(self, pos, direction, speed) -> None:
        """
        Initialize the Circle object.

        Parameters:
        - pos (list): Initial position of the circle [x, y].
        - direction (list): Initial direction of movement [dx, dy].
        - speed (float): Speed of the circle.
        """
        self.circle_width = 20
        self.pos = pos
        self.delta_speed = speed
        self.circle_shadow = []
        self.change_dir(direction)

    def change_dir(self, new_dir):
        """
        Change the direction of movement.

        Parameters:
        - new_dir (list): New direction of movement [dx, dy].
        """
        self.speed = [
            new_dir[0] * self.delta_speed,
            new_dir[1] * self.delta_speed,
        ]

    def grow(self):
        """Add a growing shadow circle to the circle's shadow list."""
        self.circle_shadow.append(CircleGrow(self.pos, self.speed, 1))

    def move(self):
        """Move the circle and its shadow circles."""
        self.pos = [
            self.pos[0] + self.speed[0],
            self.pos[1] + self.speed[1],
        ]
        for circle in self.circle_shadow:
            circle.move()
            if circle.circle_width > 50:
                self.circle_shadow.remove(circle)

    def draw(self, screen):
        """Draw the circle and its shadow circles on the screen."""
        for circle in self.circle_shadow:
            circle.draw(screen)
        pygame.draw.circle(screen, COLOR, self.pos, self.circle_width, 5)


class CircleGrow(Circle):
    """
    Class representing a growing shadow circle.
    """

    def __init__(self, pos, direction, speed) -> None:
        """
        Initialize the CircleGrow object.

        Parameters:
        - pos (list): Initial position of the circle [x, y].
        - direction (list): Initial direction of movement [dx, dy].
        - speed (float): Speed of the circle growth.
        """
        self.circle_width = 25
        self.pos = pos
        self.delta_speed = speed
        self.change_dir(direction)

    def move(self):
        """Increase the circle's width to simulate growth."""
        self.circle_width += self.delta_speed

    def draw(self, screen):
        """Draw the growing circle on the screen."""
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.circle_width, 0)


class PolyLine:
    """
    Class representing a polyline with an associated moving circle.
    """

    def __init__(self, pos, vertex, size, notes, color=(255, 255, 255), width=5):
        """
        Parameters:
        - pos (list): Center position of the polyline [x, y].
        - vertex (int): Number of vertices in the polyline.
        - size (int): Size of the polyline.
        - notes (list): List of sound notes associated with collisions.
        - color (tuple): RGB color of the polyline.
        - width (int): Width of the polyline.
        """
        self.pos = pos
        self.vertex = vertex
        self.size = size
        self.next_point = 1
        self.notes = notes
        self.color = color
        self.width = width

        # Initialize the polyline and the associated circle
        self.calculate_points_and_direction()
        self.note = notes[0]
        self.circle = Circle(self.points[0], self.circle_speed, 0.03)

    def calculate_points_and_direction(self):
        """Calculate the vertices of the polyline and the initial direction of the associated circle."""
        angle_increment = 2 * np.pi / self.vertex
        current_angle = -np.pi / 2  # Start at -pi/2 to make the polyline start at the top position
        self.points = []

        for _ in range(self.vertex):
            x = self.pos[0] + self.size * np.cos(current_angle)
            y = self.pos[1] + self.size * np.sin(current_angle)

            self.points.append([int(x), int(y)])
            current_angle += angle_increment  # Increment the angle to move in the opposite direction of the clock hands

        # Add the first point at the end to close the geometric shape
        self.points.append(self.points[0])

        # Set the initial direction of the circle
        self.circle_speed = [
            self.points[1][0] - self.points[0][0],
            self.points[1][1] - self.points[0][1],
        ]

    def move(self):
        """Move the polyline and handle collisions with the associated circle."""
        current_point = np.array(self.points[self.next_point])
        circle_position = np.array(self.circle.pos)

        distance = np.linalg.norm(current_point - circle_position)
        if distance < 10:
            self.handle_collision()

        self.circle.move()

    def handle_collision(self):
        """Handle collisions between the polyline and the associated circle."""
        for sound in self.notes:
            sound.play(int(quarter / 2))
            self.circle.grow()

        self.next_point += 1
        if self.next_point >= len(self.points):
            self.next_point = 0

        new_dir = [
            self.points[self.next_point][0] - self.points[self.next_point - 1][0],
            self.points[self.next_point][1] - self.points[self.next_point - 1][1],
        ]
        self.circle.change_dir(new_dir)

    def draw(self, screen):
        """Draw the polyline and the associated circle on the screen."""
        pygame.draw.lines(screen, self.color, False, self.points, self.width)
        self.circle.draw(screen)
