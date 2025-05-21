import pygame
import sys

from constants import (
    PLAYER, FLOOR, GOAL, BOX, WALL, MAX_HISTORY, TILE_SIZE,
    PLAYER_ON_GOAL, BOX_ON_GOAL, MIN_GAME_SCREEN_WIDTH, MIN_GAME_SCREEN_HEIGHT_BASE
)
# Assuming loader.py is in the same directory or accessible via Python path
from loader import levels, move_sound # levels is the list of all level maps

# --- Global variables for game logic state ---
current_level_data = []
player_pos = (0, 0)
history = []

# These will be updated by setup_level and potentially used by drawing functions if they were here.
# For now, setup_level calculates them.
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0


def setup_level(level_idx, screen_surface_from_main, game_state_from_main, current_level_idx_from_main_for_setup):
    """
    Sets up the game board for a given level index.
    Manages screen resizing based on level dimensions.
    Returns:
        tuple: (new_game_state, updated_screen_surface)
               new_game_state can be "playing", "game_complete", "error_no_levels", or "menu_player_not_found".
               updated_screen_surface is the surface returned by pygame.display.set_mode.
    """
    global current_level_data, player_pos, history, SCREEN_WIDTH, SCREEN_HEIGHT
    
    # This variable from main.py (current_level_index) is used by is_original_goal_tile
    # We are passing it around for now. Let's call the parameter current_level_idx_from_main_for_setup
    # to avoid confusion with the level_idx being set up.

    if not (0 <= level_idx < len(levels)):
        new_game_state = "game_complete" if levels else "error_no_levels"
        return new_game_state, screen_surface_from_main # No change to screen if level invalid

    current_level_data = [row[:] for row in levels[level_idx]]
    history = [] # Reset history for the new level
    max_cols = 0
    player_found = False

    for r, row_data in enumerate(current_level_data):
        max_cols = max(max_cols, len(row_data))
        for c, char in enumerate(row_data):
            if char == PLAYER:
                player_pos = (r, c)
                current_level_data[r][c] = FLOOR # Player stands on a floor tile
                player_found = True
            elif char == PLAYER_ON_GOAL:
                player_pos = (r, c)
                current_level_data[r][c] = GOAL # Player stands on a goal tile initially
                player_found = True
    
    if not player_found:
        print(f"错误：关卡 {level_idx + 1} 中未找到玩家初始位置 ('@' 或 '+')。")
        # Instead of calling draw_level_selection_menu here, signal main.py
        return "menu_player_not_found", screen_surface_from_main 

    num_rows = len(current_level_data)
    num_cols = max_cols if max_cols > 0 else 10

    info_area_height = TILE_SIZE * 2 
    new_screen_width = num_cols * TILE_SIZE
    new_screen_height = num_rows * TILE_SIZE + info_area_height

    # Use constants for min screen size
    actual_min_game_screen_height = MIN_GAME_SCREEN_HEIGHT_BASE + info_area_height
    SCREEN_WIDTH = max(new_screen_width, MIN_GAME_SCREEN_WIDTH)
    SCREEN_HEIGHT = max(new_screen_height, actual_min_game_screen_height)

    # Resize the screen
    updated_screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"推箱子 - 关卡 {level_idx + 1}")
    
    save_current_state_to_history() # Save initial state
    return "playing", updated_screen_surface


def get_tile_at(r, c):
    """Gets the tile character at a given row and column."""
    if 0 <= r < len(current_level_data) and 0 <= c < len(current_level_data[r]):
        return current_level_data[r][c]
    return WALL # Treat out-of-bounds as a wall


def set_tile_at(r, c, tile_char):
    """Sets the tile character at a given row and column."""
    if 0 <= r < len(current_level_data) and 0 <= c < len(current_level_data[r]):
        current_level_data[r][c] = tile_char


def is_original_goal_tile(r, c, current_level_idx_from_main):
    """Checks if the tile at (r,c) in the original level map was a goal."""
    if not (0 <= current_level_idx_from_main < len(levels)):
        return False # Should not happen if levels are loaded and index is valid
    original_level_map = levels[current_level_idx_from_main]
    if 0 <= r < len(original_level_map) and 0 <= c < len(original_level_map[r]):
        original_char = original_level_map[r][c]
        return original_char in [GOAL, PLAYER_ON_GOAL, BOX_ON_GOAL]
    return False


def move_player_and_boxes(dr, dc, current_level_idx_from_main):
    """
    Handles player movement and box pushing logic.
    `current_level_idx_from_main` is needed for `is_original_goal_tile`.
    Returns True if the player moved, False otherwise.
    """
    global player_pos # We are modifying player_pos

    cr, cc = player_pos
    nr, nc = cr + dr, cc + dc # Next position for the player

    tile_at_next = get_tile_at(nr, nc)

    if tile_at_next == WALL:
        return False # Can't move into a wall

    # Try to move player or player and box
    if tile_at_next == FLOOR or tile_at_next == GOAL:
        player_pos = (nr, nc)
        save_current_state_to_history()
        if move_sound:
            move_sound.play()
        return True
    
    if tile_at_next == BOX or tile_at_next == BOX_ON_GOAL:
        # Position behind the box
        box_nr, box_nc = nr + dr, nc + dc 
        tile_behind_box = get_tile_at(box_nr, box_nc)

        if tile_behind_box == WALL or tile_behind_box == BOX or tile_behind_box == BOX_ON_GOAL:
            # Box is blocked
            return False

        # Move box
        set_tile_at(box_nr, box_nc, BOX_ON_GOAL if is_original_goal_tile(box_nr, box_nc, current_level_idx_from_main) else BOX)
        # Clear the box's previous spot
        set_tile_at(nr, nc, GOAL if tile_at_next == BOX_ON_GOAL else FLOOR)
        # Move player
        player_pos = (nr, nc)
        save_current_state_to_history()
        if move_sound:
            move_sound.play()
        return True
        
    return False # Should not be reached if logic is exhaustive for WALL, FLOOR, GOAL, BOX, BOX_ON_GOAL


def check_level_win_condition(current_level_idx_from_main):
    """
    Checks if all goals are covered by boxes.
    `current_level_idx_from_main` is needed for `is_original_goal_tile`.
    """
    for r_idx, row in enumerate(current_level_data):
        for c_idx, tile_char in enumerate(row):
            if is_original_goal_tile(r_idx, c_idx, current_level_idx_from_main) and tile_char != BOX_ON_GOAL:
                return False # A goal is not covered
    return True # All goals are covered


def save_current_state_to_history():
    """Saves the current level map and player position to history for undo."""
    global history
    # Deep copy of current_level_data and player_pos
    history.append(([row[:] for row in current_level_data], player_pos))
    if len(history) > MAX_HISTORY:
        history.pop(0) # Keep history size bounded


def undo_last_move():
    """Restores the game state to the previous state in history."""
    global current_level_data, player_pos, history
    if len(history) > 1: # Need at least one state to revert to (initial state is one entry)
        history.pop() # Remove current state
        last_map_state, last_player_pos = history[-1]
        current_level_data = [row[:] for row in last_map_state]
        player_pos = last_player_pos
    elif len(history) == 1:
        # This means we are at the initial state, can't undo further from current logic
        # (or, if initial state wasn't saved first, this means only one state in history)
        print("提示: 已在初始状态或无法撤销。")

if __name__ == '__main__':
    # This block is for basic testing of game_logic.py
    # Requires constants.py and loader.py to be accessible
    # and loader.py should have successfully loaded levels.
    
    print("game_logic.py executed directly. Basic tests:")

    if not levels:
        print("Levels not loaded from loader.py. Cannot run tests.")
        sys.exit()

    # Mock Pygame screen for setup_level
    pygame.init() # Ensure pygame is initialized
    mock_screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT)) # from constants
    
    print(f"Total levels loaded by loader: {len(levels)}")

    test_level_idx = 0
    print(f"\nSetting up level {test_level_idx + 1}...")
    # game_state_from_main would be 'menu' or 'playing', current_level_idx is the one being loaded
    new_state, updated_mock_screen = setup_level(test_level_idx, mock_screen, "menu", test_level_idx)
    print(f"  New game state: {new_state}")
    print(f"  Player position: {player_pos}")
    print(f"  History length: {len(history)}")
    if current_level_data:
        print(f"  Level data rows: {len(current_level_data)}, cols (first row): {len(current_level_data[0]) if current_level_data[0] else 0}")

    if new_state == "playing":
        # Test move
        print("\nAttempting a move (down)...")
        moved = move_player_and_boxes(1, 0, test_level_idx) # dr=1, dc=0 (down)
        print(f"  Player moved: {moved}")
        print(f"  New player position: {player_pos}")
        print(f"  History length: {len(history)}")

        # Test undo
        print("\nAttempting undo...")
        undo_last_move()
        print(f"  Player position after undo: {player_pos}")
        print(f"  History length: {len(history)}") # Should be 1 if initial state was saved

        # Test win condition (likely false on initial setup)
        print("\nChecking win condition...")
        won = check_level_win_condition(test_level_idx)
        print(f"  Level won: {won}")

    pygame.quit()
    sys.exit()
