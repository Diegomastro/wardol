import random
import time

import pygame
import sys
from square import Square

# Initialize Pygame
pygame.init()

# Constants
WORD_LEN = 5
font = pygame.font.Font(None, 36)  # You can adjust the font size

WIDTH, HEIGHT = 600, 800
FPS = 60

# Colors
BLACK = (24, 20, 20)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WARDOL")
clock = pygame.time.Clock()


def send_word(word):
    print(word)


def receive_states():
    res = [random.choice(("gray", "green", "yellow")) for i in range(WORD_LEN)]
    print(res)
    return res


# Function to draw squares with different colors
def draw_squares(color_sequence):
    square_size = WIDTH // len(color_sequence)
    for i, color in enumerate(color_sequence):
        pygame.draw.rect(screen, color, (i * square_size, 0, square_size, HEIGHT))


# Main game loop
def main():
    squares = [Square(x, y, "blank") for y in range(6) for x in range(5)]
    current_try = 0
    this_word_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if current_try < 6: # IF game isn't finished

                    # if word isn't fully typed then type letter on the same row
                    if pygame.K_a <= event.key <= pygame.K_z:
                        if this_word_index < WORD_LEN:
                            squares[current_try * WORD_LEN + this_word_index].letter = chr(event.key).upper()
                            this_word_index += 1

                    # if word isn't empty then erase one position
                    if event.key == pygame.K_BACKSPACE:
                        if this_word_index > 0:
                            this_word_index -= 1
                            squares[current_try * WORD_LEN + this_word_index].letter = " "

                    # if word is fully typed then send it to the server
                    if event.key == pygame.K_RETURN:
                        if this_word_index == WORD_LEN:
                            first_index = current_try * WORD_LEN
                            send_word("".join([squares[i].letter for i in range(first_index, first_index + WORD_LEN)]))
                            states = receive_states()
                            this_word_index = 0
                            current_try += 1

                            for i in range(WORD_LEN):
                                squares[first_index + i].color = states[i]

        # Clear the screen
        screen.fill(BLACK)

        # Draw squares
        for i in squares:
            pygame.draw.rect(screen, i.rgb, i.pygame_object)

            if i.letter:
                text = font.render(i.letter, True, (255, 255, 255))  # White color
                text_rect = text.get_rect(center=i.pygame_object.center)
                screen.blit(text, text_rect)

        # DEBUG DRAWS
        text_this_word_index = font.render(str(this_word_index), True, (255, 255, 255))  # White color
        text_rect = text_this_word_index.get_rect(center=(10, 10))
        screen.blit(text_this_word_index, text_rect)

        text_current_try = font.render(str(current_try), True, (255, 255, 255))  # White color
        text_rect = text_current_try.get_rect(center=(10, 50))
        screen.blit(text_current_try, text_rect)


        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
