import pygame

from constants import (
    MENU_BACKGROUND_COLOR, RED, MENU_BUTTON_TEXT_COLOR, LEVELS_DIR, MENU_TITLE_COLOR,
    MENU_BUTTON_COLOR, MENU_BUTTON_HOVER_COLOR, MENU_BUTTON_BORDER_COLOR,
    MENU_BUTTON_SELECTED_BORDER_COLOR, MENU_QUIT_BUTTON_COLOR, MENU_QUIT_BUTTON_HOVER_COLOR,
    MENU_BORDER_RADIUS, INITIAL_SCREEN_WIDTH, TILE_SIZE, BLACK, GAME_INFO_BG_COLOR,
    GAME_INFO_TEXT_COLOR, GREEN, WHITE, MENU_BUTTONS_PER_ROW, MENU_BUTTON_WIDTH,
    MENU_BUTTON_HEIGHT, MENU_BUTTON_PADDING
)
# Assuming loader.py is in the same directory or accessible via Python path
from loader import FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_BUTTON, IMAGES, levels


def draw_text(text, font, color, surface, x, y, centered=False):
    """Renders text onto a surface."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect # Return the rect for potential collision detection or positioning


def draw_level_selection_menu(screen_surface, selected_button_idx, current_screen_width, current_screen_height, mouse_pos):
    """
    Draws the level selection menu. Handles screen resizing.
    Returns:
        tuple: (button_rects_list, new_screen_surface, new_screen_width, new_screen_height)
    """
    new_screen_width = current_screen_width
    new_screen_height = current_screen_height
    
    screen_surface.fill(MENU_BACKGROUND_COLOR)

    if not levels: # levels is imported from loader
        # Adjust screen for error message
        target_width, target_height = 700, 350
        if new_screen_width != target_width or new_screen_height != target_height:
            new_screen_width, new_screen_height = target_width, target_height
            screen_surface = pygame.display.set_mode((new_screen_width, new_screen_height))
            # Re-fill after resize
            screen_surface.fill(MENU_BACKGROUND_COLOR)
        
        if FONT_MEDIUM and FONT_SMALL: # Check if fonts loaded
            draw_text("错误：未找到或加载任何关卡！", FONT_MEDIUM, RED, screen_surface, new_screen_width // 2, 80, centered=True)
            draw_text(f"请在 '{LEVELS_DIR}' 目录下", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, new_screen_width // 2, 150, centered=True)
            draw_text("添加有效的关卡文件 (如 level1.txt)。", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, new_screen_width // 2, 180, centered=True)
        else: # Fallback if fonts are not available
            print("ERROR: Fonts not loaded, cannot display level loading error message on screen.")


        quit_btn_rect = pygame.Rect(0, 0, 200, 50)
        quit_btn_rect.center = (new_screen_width // 2, new_screen_height - 70)
        
        is_hovered = quit_btn_rect.collidepoint(mouse_pos)
        btn_color = MENU_QUIT_BUTTON_HOVER_COLOR if is_hovered else MENU_QUIT_BUTTON_COLOR
        pygame.draw.rect(screen_surface, btn_color, quit_btn_rect, border_radius=MENU_BORDER_RADIUS)
        pygame.draw.rect(screen_surface, MENU_BUTTON_BORDER_COLOR, quit_btn_rect, 2, border_radius=MENU_BORDER_RADIUS)
        if FONT_SMALL:
            draw_text("退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, quit_btn_rect.centerx, quit_btn_rect.centery, centered=True)
        return [quit_btn_rect], screen_surface, new_screen_width, new_screen_height

    title_area_height = 100
    if FONT_LARGE:
        draw_text("选择关卡", FONT_LARGE, MENU_TITLE_COLOR, screen_surface, current_screen_width // 2, title_area_height // 2, centered=True)

    num_button_rows = (len(levels) + MENU_BUTTONS_PER_ROW - 1) // MENU_BUTTONS_PER_ROW
    buttons_grid_width = MENU_BUTTONS_PER_ROW * (MENU_BUTTON_WIDTH + MENU_BUTTON_PADDING) - MENU_BUTTON_PADDING
    buttons_grid_height = num_button_rows * (MENU_BUTTON_HEIGHT + MENU_BUTTON_PADDING) - MENU_BUTTON_PADDING

    horizontal_margin = 80
    vertical_margin_bottom = 100 

    # Dynamically adjust screen size
    required_width = max(buttons_grid_width + horizontal_margin * 2, INITIAL_SCREEN_WIDTH) # INITIAL_SCREEN_WIDTH from constants
    required_height = title_area_height + buttons_grid_height + vertical_margin_bottom + 50

    if current_screen_width != required_width or current_screen_height != required_height:
        new_screen_width, new_screen_height = int(required_width), int(required_height)
        screen_surface = pygame.display.set_mode((new_screen_width, new_screen_height))
        screen_surface.fill(MENU_BACKGROUND_COLOR) # Re-fill after resize
        if FONT_LARGE: # Re-draw title if it was drawn
            draw_text("选择关卡", FONT_LARGE, MENU_TITLE_COLOR, screen_surface, new_screen_width // 2, title_area_height // 2, centered=True)

    button_rects = []
    grid_start_x = (new_screen_width - buttons_grid_width) // 2
    grid_start_y = title_area_height + 20

    for i in range(len(levels)):
        row_idx = i // MENU_BUTTONS_PER_ROW
        col_idx = i % MENU_BUTTONS_PER_ROW
        btn_x = grid_start_x + col_idx * (MENU_BUTTON_WIDTH + MENU_BUTTON_PADDING)
        btn_y = grid_start_y + row_idx * (MENU_BUTTON_HEIGHT + MENU_BUTTON_PADDING)
        rect = pygame.Rect(btn_x, btn_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        button_rects.append(rect)

        is_selected_by_kb = (i == selected_button_idx)
        is_hovered_by_mouse = rect.collidepoint(mouse_pos)

        btn_color = MENU_BUTTON_COLOR
        if is_hovered_by_mouse or is_selected_by_kb:
            btn_color = MENU_BUTTON_HOVER_COLOR

        pygame.draw.rect(screen_surface, btn_color, rect, border_radius=MENU_BORDER_RADIUS)
        border_color = MENU_BUTTON_SELECTED_BORDER_COLOR if is_selected_by_kb else MENU_BUTTON_BORDER_COLOR
        pygame.draw.rect(screen_surface, border_color, rect, 2, border_radius=MENU_BORDER_RADIUS)
        if FONT_BUTTON:
            draw_text(str(i + 1), FONT_BUTTON, MENU_BUTTON_TEXT_COLOR, screen_surface, rect.centerx, rect.centery, centered=True)

    quit_btn_width = 220
    quit_btn_height = 50
    quit_btn_rect = pygame.Rect((new_screen_width - quit_btn_width) // 2, new_screen_height - quit_btn_height - 30, quit_btn_width, quit_btn_height)
    button_rects.append(quit_btn_rect)

    is_quit_selected_by_kb = (selected_button_idx == len(levels)) 
    is_quit_hovered_by_mouse = quit_btn_rect.collidepoint(mouse_pos)
    quit_color = MENU_QUIT_BUTTON_COLOR
    if is_quit_hovered_by_mouse or is_quit_selected_by_kb:
        quit_color = MENU_QUIT_BUTTON_HOVER_COLOR

    pygame.draw.rect(screen_surface, quit_color, quit_btn_rect, border_radius=MENU_BORDER_RADIUS)
    quit_border_color = MENU_BUTTON_SELECTED_BORDER_COLOR if is_quit_selected_by_kb else MENU_BUTTON_BORDER_COLOR
    pygame.draw.rect(screen_surface, quit_border_color, quit_btn_rect, 2, border_radius=MENU_BORDER_RADIUS)
    if FONT_SMALL:
        draw_text("退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, quit_btn_rect.centerx, quit_btn_rect.centery, centered=True)

    return button_rects, screen_surface, new_screen_width, new_screen_height


def draw_game_screen(screen_surface, current_level_data_param, player_pos_param, 
                     current_level_index_param, total_levels_param, 
                     screen_width_param, screen_height_param, 
                     game_state_param, is_original_goal_tile_func):
    """Draws the main game screen with level, player, boxes, and info."""
    screen_surface.fill(BLACK) # Background for game area

    # Draw game elements: floor, goals, walls, boxes
    if FONT_SMALL and IMAGES: # Check if resources are loaded
        for r, row in enumerate(current_level_data_param):
            for c, tile_char in enumerate(row):
                draw_pos = (c * TILE_SIZE, r * TILE_SIZE)
                # Draw goal under player/box if original tile was a goal
                if is_original_goal_tile_func(r, c, current_level_index_param):
                    screen_surface.blit(IMAGES["goal"], draw_pos)
                else:
                    screen_surface.blit(IMAGES["floor"], draw_pos)

                if tile_char == WALL: # WALL from constants
                    screen_surface.blit(IMAGES["wall"], draw_pos)
                elif tile_char == BOX: # BOX from constants
                    screen_surface.blit(IMAGES["box"], draw_pos)
                elif tile_char == BOX_ON_GOAL: # BOX_ON_GOAL from constants
                    screen_surface.blit(IMAGES["box_on_goal"], draw_pos)
        
        # Draw player
        pr, pc = player_pos_param
        player_img_key = "player_on_goal" if is_original_goal_tile_func(pr, pc, current_level_index_param) else "player"
        if player_img_key in IMAGES:
             screen_surface.blit(IMAGES[player_img_key], (pc * TILE_SIZE, pr * TILE_SIZE))

        # Draw info area
        info_area_y = len(current_level_data_param) * TILE_SIZE
        pygame.draw.rect(screen_surface, GAME_INFO_BG_COLOR, (0, info_area_y, screen_width_param, screen_height_param - info_area_y))
        
        pad, line_h = 15, 28
        draw_text(f"关卡: {current_level_index_param + 1}/{total_levels_param}", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad, info_area_y + pad)
        draw_text("R: 重玩", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad, info_area_y + pad + line_h)
        draw_text("U: 撤销", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad + 120, info_area_y + pad + line_h)
        draw_text("B/V: 切换bgm", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad + 240, info_area_y + pad + line_h)
        draw_text("Esc: 菜单", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, screen_width_param - 150 - pad, info_area_y + pad)

        if game_state_param == "level_complete":
            overlay = pygame.Surface((screen_width_param, screen_height_param), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Semi-transparent black
            screen_surface.blit(overlay, (0, 0))
            if FONT_LARGE and FONT_MEDIUM:
                draw_text("关卡完成!", FONT_LARGE, GREEN, screen_surface, screen_width_param // 2, screen_height_param // 2 - 40, centered=True)
                draw_text("按 Enter 或 空格 继续", FONT_MEDIUM, WHITE, screen_surface, screen_width_param // 2, screen_height_param // 2 + 20, centered=True)
    else:
        print("ERROR: Fonts or Images not loaded, cannot draw game screen properly.")


def draw_game_completion_screen(screen_surface, current_screen_width, current_screen_height):
    """
    Draws the game completion screen when all levels are finished.
    Handles screen resizing.
    Returns:
        tuple: (new_screen_surface, new_screen_width, new_screen_height)
    """
    new_screen_width = current_screen_width
    new_screen_height = current_screen_height
    
    target_width, target_height = 700, 400
    if new_screen_width != target_width or new_screen_height != target_height:
        new_screen_width, new_screen_height = target_width, target_height
        screen_surface = pygame.display.set_mode((new_screen_width, new_screen_height))

    screen_surface.fill(MENU_BACKGROUND_COLOR)
    if FONT_LARGE and FONT_MEDIUM and FONT_SMALL: # Check if fonts loaded
        draw_text("恭喜你，全部通关!", FONT_LARGE, GREEN, screen_surface, new_screen_width // 2, new_screen_height // 2 - 70, centered=True)
        draw_text("你是推箱子大师！", FONT_MEDIUM, MENU_TITLE_COLOR, screen_surface, new_screen_width // 2, new_screen_height // 2 - 10, centered=True)
        draw_text("按 Esc 返回菜单，或 Q 退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, new_screen_width // 2, new_screen_height // 2 + 50, centered=True)
    else:
        print("ERROR: Fonts not loaded, cannot display game completion screen.")
        
    return screen_surface, new_screen_width, new_screen_height

if __name__ == '__main__':
    # Basic test for ui.py
    # This requires constants.py and loader.py to be available and loader.py to have run its course (fonts/images loaded)
    # It also needs game_logic.py for the is_original_goal_tile function.
    
    pygame.init() # Ensure pygame is initialized for display and font
    
    # Mock necessary components that would normally be provided by other modules
    mock_current_screen_width = INITIAL_SCREEN_WIDTH # from constants
    mock_current_screen_height = INITIAL_SCREEN_HEIGHT # from constants
    mock_screen_surface = pygame.display.set_mode((mock_current_screen_width, mock_current_screen_height))
    pygame.display.set_caption("UI Test")
    
    mock_mouse_pos = (0,0)
    mock_selected_button_idx = 0

    # Test draw_text (implicitly tested by other functions)
    if FONT_SMALL:
        draw_text("UI Test Mode", FONT_SMALL, WHITE, mock_screen_surface, 10, 10)
    else:
        print("FONT_SMALL not loaded, skipping draw_text direct test.")

    # Test draw_level_selection_menu
    print("\nTesting draw_level_selection_menu...")
    if FONT_LARGE and FONT_MEDIUM and FONT_SMALL and FONT_BUTTON: # Ensure fonts are loaded
        button_rects, new_surface, new_w, new_h = draw_level_selection_menu(mock_screen_surface, mock_selected_button_idx, mock_current_screen_width, mock_current_screen_height, mock_mouse_pos)
        print(f"  Returned {len(button_rects)} button rects. New screen: {new_w}x{new_h}")
        mock_screen_surface = new_surface # Update surface if resized
        mock_current_screen_width, mock_current_screen_height = new_w, new_h
    else:
        print("  Skipping draw_level_selection_menu test as fonts are not loaded.")
    
    pygame.display.flip()
    pygame.time.wait(1000)

    # Test draw_game_screen
    print("\nTesting draw_game_screen...")
    # Mock game data (normally from game_logic.py and main.py)
    mock_level_data = [list("####"), list("# @#"), list("#  #"), list("####")] # Player at (1,2)
    mock_player_pos = (1, 2)
    mock_level_idx = 0
    mock_total_levels = 1 # len(levels)
    
    # Mock is_original_goal_tile function (normally from game_logic.py)
    def mock_is_original_goal(r, c, level_idx): return False

    if FONT_SMALL and IMAGES: # Check if resources are loaded
        draw_game_screen(mock_screen_surface, mock_level_data, mock_player_pos, 
                         mock_level_idx, mock_total_levels, 
                         mock_current_screen_width, mock_current_screen_height, 
                         "playing", mock_is_original_goal)
    else:
        print("  Skipping draw_game_screen test as fonts or images are not loaded.")

    pygame.display.flip()
    pygame.time.wait(1000)

    # Test draw_game_completion_screen
    print("\nTesting draw_game_completion_screen...")
    if FONT_LARGE and FONT_MEDIUM and FONT_SMALL: # Ensure fonts are loaded
        new_surface, new_w, new_h = draw_game_completion_screen(mock_screen_surface, mock_current_screen_width, mock_current_screen_height)
        print(f"  New screen: {new_w}x{new_h}")
    else:
        print("  Skipping draw_game_completion_screen test as fonts are not loaded.")

    pygame.display.flip()
    pygame.time.wait(1000)
    
    pygame.quit()
    print("UI tests finished.")
