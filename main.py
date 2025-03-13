# main.py
import pygame
import os # Import os module
from news_fetcher import fetch_headlines
from ticker_display import NewsTicker
from settings_menu import SettingsMenu

if __name__ == "__main__":
    pygame.init()

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    ticker_height = 17

    # Set window position to top-left (0,0) - already default with NOFRAME, but explicit for clarity
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0" # Set window position at top-left

    screen = pygame.display.set_mode((screen_width, ticker_height), pygame.NOFRAME | pygame.SRCALPHA | pygame.HWSURFACE) # HWSURFACE for potential performance
    pygame.display.set_caption("Google News Ticker")
    pygame.mouse.set_visible(False)

    # Attempt to make window always on top (OS-dependent and may not always work reliably with Pygame NOFRAME)
    try:
        import pygame._sdl2 as sdl2 # Try importing SDL2 bindings
        sdl2.window.Window.from_display_module().set_always_on_top(True) # Set always on top if SDL2 available
        print("Attempted to set window always on top (SDL2 method)")
    except ImportError:
        print("SDL2 bindings not found, 'always on top' may not be available.")
    except Exception as e:
        print(f"Error setting 'always on top': {e}")


    screen.fill((0, 0, 0, 0))

    headlines = fetch_headlines()

    settings_menu = SettingsMenu(screen)

    def open_settings_menu_func():
        settings_menu.open_menu()

    ticker = NewsTicker(screen, headlines, open_settings_menu_func)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif not settings_menu.is_open:
                ticker.handle_event(event)
            else:
                settings_menu.handle_event(event)

        if not settings_menu.is_open:
            ticker.update_ticker()

            screen.fill((0, 0, 0, 0))
            ticker.draw(screen)

            pygame.display.flip()

        elif settings_menu.is_open: # Draw settings menu if open
            settings_menu.draw(screen)

        pygame.time.delay(20)

    pygame.quit()