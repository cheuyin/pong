import pygame
import settings


class Menu:
    def __init__(self, screen: pygame.Surface, title: str, labels: list[str]):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.title = title
        self.labels = labels
        self.selected_index = 0
        self.title_font = settings.LARGE_TEXT
        self.option_font = settings.MEDIUM_TEXT
        self.hint_font = settings.SMALL_TEXT

    def reset(self):
        self.selected_index = 0

    def handle_event(self, event: pygame.event.Event) -> int | None:
        """Return the selected index when Enter is pressed, otherwise None."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.labels)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.labels)
        elif event.key == pygame.K_RETURN:
            return self.selected_index
        return None

    def draw(self):
        self.screen.fill(settings.SCREEN_BG_COLOR)

        title_surface = self.title_font.render(
            self.title, True, settings.WHITE)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 100
        self.screen.blit(title_surface, title_rect)

        y = title_rect.bottom + 60
        for i, label in enumerate(self.labels):
            selected = i == self.selected_index
            color = settings.MENU_SELECTION_COLOR if selected else settings.WHITE
            prefix = "> " if selected else "  "
            surface = self.option_font.render(f"{prefix}{label}", True, color)
            rect = surface.get_rect()
            rect.centerx = self.screen_rect.centerx
            rect.top = y
            self.screen.blit(surface, rect)
            y += rect.height + 20

        hint = self.hint_font.render(
            "Up/Down to choose, Enter to confirm", True, settings.GREY)
        hint_rect = hint.get_rect()
        hint_rect.centerx = self.screen_rect.centerx
        hint_rect.bottom = self.screen_rect.height - 40
        self.screen.blit(hint, hint_rect)
