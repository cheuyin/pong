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
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle.moveup()
        if keys[pygame.K_DOWN]:
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
