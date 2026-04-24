import pygame

from sprites.paddle import Paddle


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    running = True

    player1 = Paddle(screen, "left")
    player2 = Paddle(screen, "right")

    while running:
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player2.moveup()
        if keys[pygame.K_DOWN]:
            player2.movedown()
        if keys[pygame.K_w]:
            player1.moveup()
        if keys[pygame.K_s]:
            player1.movedown()

        # Reset Screen
        screen.fill("black")

        # Draw Sprites
        player1.draw()
        player2.draw()

        # Update Screen
        pygame.display.flip()

        # 60 fps Clock Tick
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
