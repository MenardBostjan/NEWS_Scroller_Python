# settings_menu.py
import pygame

class SettingsMenu:
    def __init__(self, parent_screen):
        pygame.init()
        self.parent_screen = parent_screen
        self.settings_window = None
        self.is_open = False
        self.setting_modules = []
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.background_color = (240, 240, 240, 5) # Light gray with 75% transparency (alpha = 191)
        self.button_color = (200, 200, 200)
        self.button_hover_color = (220, 220, 220)
        self.text_color = (0, 0, 0)
        self.close_button_rect = None
        self.menu_y_position = -pygame.display.Info().current_h # Start off-screen above
        self.slide_speed = 1 # Pixels per frame for sliding
        self.is_animating = False # Flag to indicate if animation is in progress


    def setup_ui(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.settings_window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SRCALPHA) # SRCALPHA for menu transparency
        pygame.display.set_caption("Settings Menu")

        # Create background surface with transparency
        self.background_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, 255)
        self.background_surface.fill(self.background_color) # Fill with transparent background color

        # Title
        title_text_surface = self.title_font.render("Settings", True, self.text_color)
        title_rect = title_text_surface.get_rect(center=(screen_width // 2, 50))
        self.title_rect = title_rect # Store for drawing

        # Placeholder Content Area
        content_rect = pygame.Rect(50, 100, screen_width - 100, screen_height - 200)
        self.content_rect = content_rect # Store for drawing
        placeholder_text_surface = self.font.render("Settings Modules will be loaded here...", True, self.text_color)
        placeholder_rect = placeholder_text_surface.get_rect(center=content_rect.center)
        self.placeholder_rect = placeholder_rect # Store for drawing

        # Close Button
        button_width = 150
        button_height = 40
        button_x = (screen_width - button_width) // 2
        button_y = screen_height - 80
        self.close_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.close_button_text_surface = self.font.render("Close Settings", True, self.text_color) # Store surface
        self.close_button_text_rect = self.close_button_text_surface.get_rect(center=self.close_button_rect.center) # Store rect


    def add_setting_module(self, module_class):
        self.setting_modules.append(module_class)
        print(f"Setting module '{module_class.__name__}' added (integration not fully implemented yet).")


    def open_menu(self):
        if not self.is_open:
            self.setup_ui()
            self.is_open = True
            self.menu_y_position = -pygame.display.Info().current_h # Reset position for animation start
            self.is_animating = True # Start animation flag
        pygame.mouse.set_visible(True)


    def close_menu(self):
        if self.is_open:
            self.is_open = False
            self.is_animating = False # Stop animation if running
            self.menu_y_position = -pygame.display.Info().current_h # Reset for next open animation
            pygame.display.quit()
            pygame.init()
            self.settings_window = None
        pygame.mouse.set_visible(False)


    def handle_event(self, event):
        if not self.is_open:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.close_button_rect.collidepoint(event.pos):
                    self.close_menu()
                    return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_menu()
                return True
        return True

    def update_menu_position(self):
        if self.is_animating:
            if self.menu_y_position < 0:
                self.menu_y_position += self.slide_speed
                if self.menu_y_position > 0: # Overshot, set to 0 to stop at top
                    self.menu_y_position = 0
                    self.is_animating = False # Stop animating when at top
            else:
                self.is_animating = False # Already fully open

    def draw(self, screen):
        if self.is_open:
            self.update_menu_position() # Update menu Y position for sliding

            self.settings_window.fill((0,0,0,0)) # Clear with transparent
            self.settings_window.blit(self.background_surface, (0, self.menu_y_position)) # Blit background with transparency, animated Y
            self.settings_window.blit(self.background_surface, (0, self.menu_y_position)) # Blit background

            pygame.draw.rect(self.settings_window, (220, 220, 220), self.content_rect.move(0, self.menu_y_position), 0) # Content area, move with menu
            self.settings_window.blit(self.placeholder_rect.move(0, self.menu_y_position), self.placeholder_rect.move(0, self.menu_y_position)) # Placeholder text
            self.settings_window.blit(self.title_rect.move(0, self.menu_y_position), self.title_rect.move(0, self.menu_y_position)) # Title
            pygame.draw.rect(self.settings_window, self.button_color, self.close_button_rect.move(0, self.menu_y_position)) # Close button
            self.settings_window.blit(self.close_button_text_surface, self.close_button_text_rect.move(0, self.menu_y_position)) # Close button text

            pygame.display.flip()