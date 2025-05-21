import pygame
import sys
import os # Kept for consistency, though not directly used for paths here

from constants import * # Import all constants
import loader
import game_logic
import ui

class Game:
    def __init__(self):
        # Initialize Pygame (mixer is initialized in loader.py)
        pygame.init()

        # Load assets using loader module
        # loader.py already calls pygame.init() and pygame.mixer.init()
        # It also loads fonts, sounds (move_sound, initial BGM) at module level.
        loader.load_all_assets() # This calls load_images and load_levels_from_disk

        if not loader.levels:
            print("Error: No levels loaded. Exiting.")
            pygame.quit()
            sys.exit()

        # Initial screen setup
        self.screen_width = INITIAL_SCREEN_WIDTH
        self.screen_height = INITIAL_SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("推箱子 (Sokoban OOP)")

        # Game state variables
        self.game_state = "menu"
        self.current_level_index = 0
        self.menu_selected_idx = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_menu_buttons = [] # For menu click detection

        # Initial UI setup for menu to correctly size screen and get button rects
        if self.game_state == "menu":
            self.current_menu_buttons, self.screen, self.screen_width, self.screen_height = \
                ui.draw_level_selection_menu(
                    self.screen, self.menu_selected_idx, 
                    self.screen_width, self.screen_height, pygame.mouse.get_pos()
                )
        elif self.game_state == "error_no_levels": # Should be handled if loader.levels is empty
             self.current_menu_buttons, self.screen, self.screen_width, self.screen_height = \
                ui.draw_level_selection_menu(
                    self.screen, -1, 
                    self.screen_width, self.screen_height, pygame.mouse.get_pos()
                )


    def run(self):
        while self.running:
            self.handle_events()
            self.update() # Currently minimal, can be expanded
            self.render()
            self.clock.tick(FPS) # Use FPS from constants.py

        pygame.quit()
        sys.exit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return # Exit event loop

            if self.game_state == "menu":
                if event.type == pygame.MOUSEMOTION:
                    if self.current_menu_buttons:
                        for i, rect in enumerate(self.current_menu_buttons):
                            if rect.collidepoint(mouse_pos):
                                self.menu_selected_idx = i
                                break
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_menu_buttons:
                        for i, rect in enumerate(self.current_menu_buttons):
                            if rect.collidepoint(mouse_pos):
                                if i < len(loader.levels):  # Clicked a level button
                                    self.current_level_index = i
                                    self.menu_selected_idx = i
                                    new_gs, updated_screen = game_logic.setup_level(
                                        self.current_level_index, self.screen, 
                                        self.game_state, self.current_level_index
                                    )
                                    self.game_state = new_gs
                                    if self.screen != updated_screen: self.screen = updated_screen
                                    self.screen_width = game_logic.SCREEN_WIDTH
                                    self.screen_height = game_logic.SCREEN_HEIGHT
                                elif i == len(self.current_menu_buttons) - 1: # Quit button
                                    self.running = False
                                break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b: loader.switch_bgm()
                    elif event.key == pygame.K_v: loader.switch_bgm(next_track=False)
                    else:
                        num_menu_options = len(loader.levels) + 1
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: self.running = False
                        elif event.key == pygame.K_LEFT: self.menu_selected_idx = (self.menu_selected_idx - 1 + num_menu_options) % num_menu_options
                        elif event.key == pygame.K_RIGHT: self.menu_selected_idx = (self.menu_selected_idx + 1) % num_menu_options
                        elif event.key == pygame.K_UP:
                            new_idx = self.menu_selected_idx - MENU_BUTTONS_PER_ROW
                            if new_idx < 0:
                                if self.menu_selected_idx == num_menu_options - 1: new_idx = len(loader.levels) - 1
                                else: new_idx = num_menu_options - 1
                            self.menu_selected_idx = max(0, new_idx)
                        elif event.key == pygame.K_DOWN:
                            new_idx = self.menu_selected_idx + MENU_BUTTONS_PER_ROW
                            if self.menu_selected_idx == num_menu_options - 1: new_idx = 0
                            elif new_idx >= len(loader.levels) and self.menu_selected_idx < len(loader.levels): new_idx = num_menu_options - 1
                            self.menu_selected_idx = min(num_menu_options - 1, new_idx)
                        
                        self.menu_selected_idx = max(0, min(self.menu_selected_idx, num_menu_options - 1))

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if 0 <= self.menu_selected_idx < len(loader.levels):
                                self.current_level_index = self.menu_selected_idx
                                new_gs, updated_screen = game_logic.setup_level(
                                    self.current_level_index, self.screen, 
                                    self.game_state, self.current_level_index
                                )
                                self.game_state = new_gs
                                if self.screen != updated_screen: self.screen = updated_screen
                                self.screen_width = game_logic.SCREEN_WIDTH
                                self.screen_height = game_logic.SCREEN_HEIGHT
                            elif self.menu_selected_idx == len(loader.levels): # Quit
                                self.running = False

            elif self.game_state == "playing":
                moved = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]: moved = game_logic.move_player_and_boxes(-1, 0, self.current_level_index)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]: moved = game_logic.move_player_and_boxes(1, 0, self.current_level_index)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]: moved = game_logic.move_player_and_boxes(0, -1, self.current_level_index)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]: moved = game_logic.move_player_and_boxes(0, 1, self.current_level_index)
                    elif event.key == pygame.K_r:
                        new_gs, updated_screen = game_logic.setup_level(self.current_level_index, self.screen, self.game_state, self.current_level_index)
                        self.game_state = new_gs
                        if self.screen != updated_screen: self.screen = updated_screen
                        self.screen_width = game_logic.SCREEN_WIDTH; self.screen_height = game_logic.SCREEN_HEIGHT
                    elif event.key == pygame.K_u: game_logic.undo_last_move()
                    elif event.key == pygame.K_b: loader.switch_bgm()
                    elif event.key == pygame.K_v: loader.switch_bgm(next_track=False)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.current_menu_buttons, self.screen, self.screen_width, self.screen_height =                             ui.draw_level_selection_menu(self.screen, self.current_level_index if loader.levels else 0, 
                                                          self.screen_width, self.screen_height, mouse_pos)
                    
                    if moved and game_logic.check_level_win_condition(self.current_level_index):
                        self.game_state = "level_complete"

            elif self.game_state == "level_complete":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.current_level_index += 1
                        if self.current_level_index < len(loader.levels):
                            new_gs, updated_screen = game_logic.setup_level(self.current_level_index, self.screen, self.game_state, self.current_level_index)
                            self.game_state = new_gs
                            if self.screen != updated_screen: self.screen = updated_screen
                            self.screen_width = game_logic.SCREEN_WIDTH; self.screen_height = game_logic.SCREEN_HEIGHT
                        else:
                            self.game_state = "game_complete"
                            self.screen, self.screen_width, self.screen_height =                                 ui.draw_game_completion_screen(self.screen, self.screen_width, self.screen_height)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.current_menu_buttons, self.screen, self.screen_width, self.screen_height =                             ui.draw_level_selection_menu(self.screen, self.current_level_index if loader.levels else 0, 
                                                          self.screen_width, self.screen_height, mouse_pos)
            
            elif self.game_state == "game_complete":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"; self.current_level_index = 0; self.menu_selected_idx = 0
                        self.current_menu_buttons, self.screen, self.screen_width, self.screen_height =                             ui.draw_level_selection_menu(self.screen, self.menu_selected_idx, 
                                                          self.screen_width, self.screen_height, mouse_pos)
                    elif event.key == pygame.K_q: self.running = False
            
            elif self.game_state == "error_no_levels":
                if self.current_menu_buttons and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_menu_buttons[0].collidepoint(mouse_pos): self.running = False # Quit
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q, pygame.K_RETURN, pygame.K_SPACE]:
                    self.running = False

    def update(self):
        # Most game logic is event-driven. This could be used for animations or continuous checks.
        # Example: Ensure BGM is playing if it stopped for some reason (though play(-1) should loop)
        # if loader.BGM_PATHS and not pygame.mixer.music.get_busy():
        #    loader.switch_bgm(initial_load=True) # Restart current or default BGM
        pass

    def render(self):
        mouse_pos = pygame.mouse.get_pos() # Get current mouse position for hover effects
        current_display_surface = pygame.display.get_surface() # Should be self.screen

        if self.game_state == "menu" or self.game_state == "error_no_levels":
            temp_idx = self.menu_selected_idx if self.game_state == "menu" else -1
            button_rects, new_s, new_sw, new_sh = ui.draw_level_selection_menu(
                current_display_surface, temp_idx, self.screen_width, self.screen_height, mouse_pos
            )
            if self.screen != new_s: self.screen = new_s
            self.screen_width, self.screen_height = new_sw, new_sh
            self.current_menu_buttons = button_rects
        
        elif self.game_state == "playing" or self.game_state == "level_complete":
            # Game screen uses dimensions set by game_logic.setup_level for the game area
            # but the window size is self.screen_width/height
            ui.draw_game_screen(
                current_display_surface, 
                game_logic.current_level_data, 
                game_logic.player_pos, 
                self.current_level_index, 
                len(loader.levels), 
                self.screen_width, # Current window width
                self.screen_height, # Current window height
                self.game_state, 
                game_logic.is_original_goal_tile 
            )
        
        elif self.game_state == "game_complete":
            new_s, new_sw, new_sh = ui.draw_game_completion_screen(
                current_display_surface, self.screen_width, self.screen_height
            )
            if self.screen != new_s: self.screen = new_s
            self.screen_width, self.screen_height = new_sw, new_sh

        pygame.display.flip()

if __name__ == '__main__':
    game_instance = Game()
    game_instance.run()
