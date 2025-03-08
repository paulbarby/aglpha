import sys
import pygame
import configparser
from src.engine.game_engine import GameEngine
from src.engine.core_states import GameState

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    screen_width = int(config['Graphics']['screen_width'])
    screen_height = int(config['Graphics']['screen_height'])
    return screen_width, screen_height

def main():
    pygame.init()
    screen_width, screen_height = load_config()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Civ Game")

    engine = GameEngine()
    # Add game_name attribute to store new game name
    engine.game_name = ""
    
    # Set the screen on the engine
    engine.set_screen(screen)
    
    # Initialize UI with screen size
    engine.ui_manager.initialize(engine, (screen_width, screen_height))
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Use the engine's shutdown method to save settings
                engine.shutdown()
                running = False
                continue
            
            # Pass events to both game engine and UI manager
            engine.handle_event(event)
            engine.ui_manager.process_input(event)

        engine.update()

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Call the engine's render method instead of directly rendering UI components
        engine.render(screen)
            
        pygame.display.flip()
        clock.tick(60)

    sys.exit()

if __name__ == '__main__':
    main()
