import pygame


class Square:

    def __init__(self, xpos=0, ypos=0, color="gray", xoffset=60, yoffset=100, side_size=75):
        # constants
        self.possible_colors = {
            "blank": (96, 96, 96),
            "yellow": (193, 174, 95),
            "green": (84, 139, 76),
            "gray": (150, 150, 150)
        }

        # vars
        self.color = color
        self.side_size = side_size
        self.padding = 6
        self.rgb = self.possible_colors[self.color]
        self.xpos = xpos
        self.ypos = ypos
        self.x = self.xpos * (self.side_size + self.padding) + self.side_size + xoffset
        self.y = self.ypos * (self.side_size + self.padding) + self.side_size + yoffset
        self.letter = " "

    @property
    def pygame_object(self):
        return pygame.Rect(self.x, self.y, self.side_size, self.side_size)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value not in self.possible_colors:
            raise ValueError(f"Invalid color, must be one of {self.possible_colors.keys()}")
        self.rgb = self.possible_colors[value]
        self._color = value
