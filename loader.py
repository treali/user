import os
import sys
import pygame

# Attempt to import constants. If this module is run directly, this might fail
# if constants.py is not in the Python path. For now, assume it's accessible.
from constants import (
    TILE_SIZE, IMAGES_DIR, LEVELS_DIR, SOUNDS_DIR, FONTS_DIR,
    CHINESE_FONT_NAME, MOVE_SOUND_PATH, BGM_PATHS
)

# --- Global variables for loaded assets ---
IMAGES = {}
IMAGE_FILES = { # This was part of main.py, closely tied to load_images
    "wall": "wall.png", "floor": "floor.png", "player": "player.png",
    "box": "box.png", "goal": "goal.png", "box_on_goal": "box_on_goal.png",
    "player_on_goal": "player_on_goal.png"
}
levels = []
move_sound = None
current_bgm_index = 0

# Font related globals
CHINESE_FONT_PATH = "" # Determined by logic below
FONT_LARGE = None
FONT_MEDIUM = None
FONT_SMALL = None
FONT_BUTTON = None

# --- Initialization ---
# It's good practice to initialize pygame modules if this loader is meant to be somewhat standalone
# or if its functions are called before main.py's own pygame.init().
pygame.init() # General pygame init
pygame.mixer.init() # Explicitly init mixer for sounds
# pygame.font.init() # Explicitly init font if needed, pygame.init() usually covers it.

# --- Image Loading ---
def load_images():
    """Loads all game images and scales them to TILE_SIZE."""
    global IMAGES, TILE_SIZE # Ensure TILE_SIZE from constants is used
    all_images_loaded_successfully = True
    for name, filename in IMAGE_FILES.items():
        path = os.path.join(IMAGES_DIR, filename)
        if not os.path.exists(path):
            print(f"错误：图片文件未找到 '{path}'。")
            all_images_loaded_successfully = False
            continue
        try:
            image = pygame.image.load(path)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
            IMAGES[name] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            print(f"成功: 图片 '{filename}' 已加载。")
        except pygame.error as e:
            print(f"错误：加载或转换图片 '{path}' 失败: {e}")
            all_images_loaded_successfully = False
    
    if not all_images_loaded_successfully:
        print("\n由于一个或多个图片资源加载失败，游戏可能无法正常启动。请检查以上错误信息。")
        # In a real scenario, might raise an exception or have main.py handle this
        # For now, just printing error as in original main.py
        # pygame.quit()
        # sys.exit() # Exiting here might be too abrupt for a library module
    if not IMAGES:
        print("错误：没有任何图片被加载。")
        # pygame.quit()
        # sys.exit()

# --- Level Loading ---
def load_levels_from_disk():
    """Loads all level files from the LEVELS_DIR."""
    global levels # To populate the global levels list
    levels = []
    if not os.path.exists(LEVELS_DIR):
        print(f"错误：关卡目录 '{LEVELS_DIR}' 未找到。")
        return False # Indicate failure
    level_files_found = False
    for i in range(1, 100): # Assuming max 99 levels
        level_file_path = os.path.join(LEVELS_DIR, f"level{i}.txt")
        if os.path.exists(level_file_path):
            level_files_found = True
            try:
                with open(level_file_path, 'r', encoding='utf-8') as f:
                    level_map = [list(line.rstrip('\n')) for line in f.readlines() if line.strip()]
                if not level_map or not any(row for row in level_map):
                    print(f"警告：关卡文件 '{level_file_path}' 为空或格式不正确。已跳过。")
                    continue
                levels.append(level_map)
            except Exception as e:
                print(f"错误: 加载关卡文件 '{level_file_path}' 失败: {e}")
        elif level_files_found:
            break 
        elif i > 5 and not level_files_found: # Optimization from original
            break
            
    if not levels:
        print("错误：在 'levels' 文件夹中没有成功加载任何关卡文件。")
        return False # Indicate failure
    print(f"成功加载 {len(levels)} 个关卡。")
    return True # Indicate success

# --- Sound Loading ---
try:
    move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)
except pygame.error as e:
    print(f"警告：移动音效加载失败：{e}")
    move_sound = None # Ensure it's None if loading failed

def switch_bgm(next_track=True, initial_load=False):
    """切换背景音乐 or loads initial BGM."""
    global current_bgm_index
    try:
        pygame.mixer.music.stop()
        if not initial_load:
            if next_track:
                current_bgm_index = (current_bgm_index + 1) % len(BGM_PATHS)
            else:
                current_bgm_index = (current_bgm_index - 1 + len(BGM_PATHS)) % len(BGM_PATHS)
        
        if 0 <= current_bgm_index < len(BGM_PATHS):
            pygame.mixer.music.load(BGM_PATHS[current_bgm_index])
            pygame.mixer.music.play(-1) # Loop indefinitely
        else:
            print(f"警告: BGM索引 {current_bgm_index} 超出范围。BGM数量: {len(BGM_PATHS)}")

    except pygame.error as e:
        print(f"切换/加载BGM失败: {e}")

# Initial BGM load
if BGM_PATHS: # Check if there are any BGM paths defined
    switch_bgm(initial_load=True)
else:
    print("警告: BGM_PATHS为空，不加载背景音乐。")


# --- Font Loading ---
# Logic for CHINESE_FONT_PATH selection
original_chinese_font_path = os.path.join(FONTS_DIR, CHINESE_FONT_NAME)
if not os.path.exists(original_chinese_font_path):
    print(f"错误：找不到字体文件 {original_chinese_font_path}")
    print(f"请将 '{CHINESE_FONT_NAME}' (或其他中文字体) 放置于 '{FONTS_DIR}' 目录下。")
    fallback_font = pygame.font.match_font("simhei,microsoftyahei,arialunicodems")
    if fallback_font:
        CHINESE_FONT_PATH = fallback_font
        print(f"警告：将使用系统字体 '{CHINESE_FONT_PATH}'。")
    else:
        CHINESE_FONT_PATH = pygame.font.get_default_font()
        print(f"警告：将使用默认字体 '{CHINESE_FONT_PATH}'，可能不支持中文。")
else:
    CHINESE_FONT_PATH = original_chinese_font_path

# Actual font object loading
try:
    if not CHINESE_FONT_PATH: # Should not happen if logic above is correct
        raise pygame.error("Chinese font path not set.")
    FONT_LARGE = pygame.font.Font(CHINESE_FONT_PATH, 48)
    FONT_MEDIUM = pygame.font.Font(CHINESE_FONT_PATH, 32)
    FONT_SMALL = pygame.font.Font(CHINESE_FONT_PATH, 22)
    FONT_BUTTON = pygame.font.Font(CHINESE_FONT_PATH, 28)
except pygame.error as e:
    print(f"加载字体失败: {e}. 游戏可能无法正确显示文本。")
    # In a real app, might need more robust error handling or fallback to default font for all sizes
    # For now, font objects might remain None if this fails.
    # pygame.quit()
    # sys.exit() # Exiting here might be too abrupt for a library module

# --- Optional: Function to load all assets ---
def load_all_assets():
    """Calls all asset loading functions."""
    print("--- 开始加载所有资源 ---")
    load_images()
    load_levels_from_disk()
    # Sounds and fonts are loaded at module import time due to current structure
    # If preferred, their loading blocks can be wrapped in functions and called here.
    # For example, move_sound loading, initial BGM, and font object loading.
    # For now, they load when loader.py is imported.
    print("--- 所有资源加载尝试完毕 ---")

if __name__ == '__main__':
    # This block can be used for testing the loader module independently
    print("loader.py executed directly. Attempting to load all assets...")
    load_all_assets()
    
    print("\n--- 测试加载结果 ---")
    print(f"图片数量: {len(IMAGES)}")
    if IMAGES:
        print(f"  示例图片 'wall': {IMAGES.get('wall')}")
    print(f"关卡数量: {len(levels)}")
    if levels:
        print(f"  示例关卡1 (行数): {len(levels[0]) if levels[0] else 0}")
    print(f"移动音效: {move_sound}")
    print(f"当前BGM索引: {current_bgm_index}")
    if BGM_PATHS and 0 <= current_bgm_index < len(BGM_PATHS):
         print(f"  当前BGM路径: {BGM_PATHS[current_bgm_index]}")
    print(f"中文字体路径: {CHINESE_FONT_PATH}")
    print(f"大号字体: {FONT_LARGE}")
    print(f"中号字体: {FONT_MEDIUM}")
    print(f"小号字体: {FONT_SMALL}")
    print(f"按钮字体: {FONT_BUTTON}")

    # Example of how to use switch_bgm (would require pygame display to be active for music)
    # print("\n尝试切换BGM...")
    # if pygame.display.get_init(): # Music usually needs an active display
    #    switch_bgm(next_track=True)
    #    print(f"BGM切换后索引: {current_bgm_index}")
    # else:
    #    print("Pygame display not initialized, skipping BGM switch test.")
    
    pygame.quit() # Clean up pygame if it was initialized here
    sys.exit()
