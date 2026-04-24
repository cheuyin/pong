import pygame

from sprites.paddle import Paddle


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    running = True

    paddle = Paddle(screen)

    while running:
        # Process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddle.moveup()
                elif event.key == pygame.K_DOWN:
                    paddle.movedown()

        # Reset Screen
        screen.fill("black")

        # Draw Sprites
        paddle.draw()

        # Update Screen
        pygame.display.flip()

        # 60 fps Clock Tick
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
