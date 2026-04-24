import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    running = True

    while running:
        # Process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logical updates here
        # ...

        screen.fill("black")

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
