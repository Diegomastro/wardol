import random
import time

import pygame
import sys

import wordlist
from square import Square

# Initialize Pygame
pygame.init()

# Constants
WORD_LEN = 5
font = pygame.font.Font(None, 36)  # You can adjust the font size

WIDTH, HEIGHT = 600, 810
FPS = 60

SMALL_SQUARE_X_OFFSET = 80
SMALL_SQUARE_Y_OFFSET = 580

# Colors
BLACK = (43, 43, 43)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WARDOL")
clock = pygame.time.Clock()


def send_word(word):
    print(word)


def receive_states():
    res = [random.choice(("gray", "green", "yellow")) for i in range(WORD_LEN)]
    return res


# Function to draw squares with different colors


def main():
    current_try = 0
    this_word_index = 0

    # initialize squares
    squares = [Square(x, y, "blank") for y in range(6) for x in range(5)]

    # initialize small squares (the keyboard below)
    small_squares = []
    small_squares.extend(
        [Square(x, 0, "blank", SMALL_SQUARE_X_OFFSET, SMALL_SQUARE_Y_OFFSET, 40, 60) for x in range(10)])
    small_squares.extend(
        [Square(x, 1, "blank", SMALL_SQUARE_X_OFFSET + 20, SMALL_SQUARE_Y_OFFSET + 2, 40, 60) for x in range(9)])
    small_squares.extend(
        [Square(x, 2, "blank", SMALL_SQUARE_X_OFFSET + 66, SMALL_SQUARE_Y_OFFSET + 4, 40, 60) for x in range(7)])

    # put a letter to every small square, and create a lookup dict
    small_squares_by_letter = {}
    for sq, let in zip(small_squares, "QWERTYUIOPASDFGHJKLZXCVBNM"):
        sq.letter = let
        small_squares_by_letter[let] = sq

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if current_try < 6:  # IF game isn't finished

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
                            word = "".join([squares[i].letter for i in range(first_index, first_index + WORD_LEN)])
                            print(word)

                            if word in wordlist.allowed_words:
                                this_word_index = 0
                                current_try += 1

                                # Send to the server for processing
                                send_word(word)

                                # Paint the squares according to the received states
                                states = receive_states()
                                for i in range(WORD_LEN):
                                    this_square = squares[first_index + i]
                                    this_square.color = states[i]

                                    small_squares_by_letter[this_square.letter].keep_max_color(states[i])

        # Clear the screen
        screen.fill(BLACK)

        # Draw squares
        for i in squares:
            if i.color == "blank":
                pygame.draw.rect(screen, i.rgb, i.pygame_object, width=1)
            else:
                pygame.draw.rect(screen, i.rgb, i.pygame_object)

            if i.letter:
                text = font.render(i.letter, True, (255, 255, 255))  # White color
                text_rect = text.get_rect(center=i.pygame_object.center)
                screen.blit(text, text_rect)

        # Draw small squares
        for i in small_squares:
            pygame.draw.rect(screen, i.rgb, i.pygame_object, border_radius=3)

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
