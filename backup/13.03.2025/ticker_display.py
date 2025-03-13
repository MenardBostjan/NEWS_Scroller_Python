# ticker_display.py
import pygame

class NewsTicker:
    def __init__(self, screen, headlines, settings_button_command):
        pygame.init()
        self.screen = screen
        self.headlines = headlines
        self.settings_button_command = settings_button_command
        self.current_headline_index = 0
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.x_position = self.screen_width
        self.scroll_speed = 150
        self.last_update_time = pygame.time.get_ticks()
        self.headline_surface = None
        self.headline_rect = None
        self.font = None
        self.text_color = (255, 255, 255) # White
        self.shadow_color = (0, 0, 0)     # Black
        self.shadow_offset = 1
        self.settings_button_rect = None

        self.configure_font_and_style()
        self.create_settings_button()
        self.prepare_headlines_text() # Prepare combined headline text with separators
        self.show_next_headline()

    def configure_font_and_style(self):
        self.font = pygame.font.SysFont("Arial", 10) # Arial 10px (slightly larger for better appearance)

    def create_settings_button(self):
        button_text = "[^]" # Settings button text
        button_surface = self.font.render(button_text, True, self.text_color) # Render button text
        self.settings_button_rect = button_surface.get_rect(topright=(self.screen_width - 3, 3)) # Position at top right with 3px padding
        self.settings_button_surface = button_surface # Store the surface for drawing

    def prepare_headlines_text(self):
        """Combines headlines with "***" separators into a single list."""
        headlines_with_separators = []
        for i, headline in enumerate(self.headlines):
            headlines_with_separators.append(headline)
            if i < len(self.headlines) - 1: # No separator after the last headline
                headlines_with_separators.append("   ***   ") # Added separators with spaces for visual separation
        self.combined_headlines = headlines_with_separators

    def show_next_headline(self):
        if not self.combined_headlines:
            return # No headlines to show

        current_headline = self.combined_headlines.pop(0) # Get and remove the first headline/separator

        # Render shadow text first (transparent background)
        shadow_text_surface = self.font.render(current_headline, True, self.shadow_color) # Antialiased, transparent bg by default
        text_surface = self.font.render(current_headline, True, self.text_color)     # Antialiased, transparent bg by default

        # Create a surface large enough for shadow and main text (transparent background)
        combined_width = max(text_surface.get_width(), shadow_text_surface.get_width()) + self.shadow_offset
        combined_height = max(text_surface.get_height(), shadow_text_surface.get_height()) + self.shadow_offset
        self.headline_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA, 32) # SRCALPHA for transparency
        self.headline_surface.fill((0, 0, 0, 0)) # Fill with transparent black

        # Blit shadow then main text onto the combined surface
        self.headline_surface.blit(shadow_text_surface, (self.shadow_offset, self.shadow_offset))
        self.headline_surface.blit(text_surface, (0, 0))

        self.headline_rect = self.headline_surface.get_rect(topleft=(self.x_position, 3)) # Start at top + 3px padding

        self.headline_width = self.headline_rect.width
        if not self.combined_headlines: # Refill headlines if empty
            self.prepare_headlines_text() # Repopulate combined_headlines


    def update_ticker(self):
        current_time = pygame.time.get_ticks()
        time_elapsed_ms = current_time - self.last_update_time
        time_elapsed_seconds = time_elapsed_ms / 1000.0

        distance = self.scroll_speed * time_elapsed_seconds
        self.x_position -= distance
        self.headline_rect.x = int(self.x_position)

        if self.headline_rect.right < 0:
            self.x_position = self.screen_width
            self.headline_rect.x = int(self.x_position)
            self.show_next_headline()

        self.last_update_time = current_time


    def draw(self, screen):
        if self.headline_surface:
            screen.blit(self.headline_surface, self.headline_rect)
        screen.blit(self.settings_button_surface, self.settings_button_rect) # Draw settings button

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.settings_button_rect.collidepoint(event.pos):
                    self.settings_button_command()