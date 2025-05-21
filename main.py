import pygame
import os
import sys

# --- 常量定义 ---
INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600
TILE_SIZE = 64  # 您的图片资源的尺寸 (像素)

# --- 颜色定义 (新的UI颜色方案) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)  # 鲜绿色，用于成功提示
RED = (200, 0, 0)  # 深红色，用于错误提示
BLUE = (0, 0, 255)  # 基本蓝色

# 菜单界面颜色
MENU_BACKGROUND_COLOR = (60, 60, 80)  # 深蓝灰色背景
MENU_TITLE_COLOR = (220, 220, 255)  # 淡紫色标题
MENU_BUTTON_COLOR = (90, 90, 120)  # 按钮常规颜色 (偏蓝紫)
MENU_BUTTON_HOVER_COLOR = (130, 130, 170)  # 按钮悬停颜色
MENU_BUTTON_TEXT_COLOR = (230, 230, 230)  # 按钮文字颜色 (亮灰色)
MENU_BUTTON_BORDER_COLOR = (40, 40, 60)  # 按钮边框颜色
MENU_BUTTON_SELECTED_BORDER_COLOR = (200, 200, 255)  # 选中按钮的边框（键盘选中时）

MENU_QUIT_BUTTON_COLOR = (180, 80, 80)  # 退出按钮颜色 (偏红)
MENU_QUIT_BUTTON_HOVER_COLOR = (220, 100, 100)  # 退出按钮悬停颜色

# 游戏内信息区颜色
GAME_INFO_BG_COLOR = (40, 40, 50)
GAME_INFO_TEXT_COLOR = (200, 200, 200)

# 游戏元素字符映射
WALL = '#'
FLOOR = ' '
PLAYER = '@'
BOX = '$'
GOAL = '.'
BOX_ON_GOAL = '*'
PLAYER_ON_GOAL = '+'

# --- 资源路径 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEVELS_DIR = os.path.join(BASE_DIR, "levels")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")


# 初始化 Pygame 和音效系统
pygame.init()
pygame.mixer.init()

# 背景音乐路径

# --- 声音资源路径 ---
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# --- 加载声音资源 ---
MOVE_SOUND_PATH = os.path.join(SOUNDS_DIR, "move.wav")

try:
    move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)
except pygame.error as e:
    print(f"警告：移动音效加载失败：{e}")
    move_sound = None
# 在声音资源路径后添加以下内容
BGM_PATHS = [
    os.path.join(SOUNDS_DIR, "bgm1.ogg"),
    os.path.join(SOUNDS_DIR, "bgm2.ogg"),  # 添加更多BGM文件
    os.path.join(SOUNDS_DIR, "bgm3.ogg")
]
current_bgm_index = 0  # 当前播放的BGM索引

# 修改switch_bgm函数定义
def switch_bgm(next=True, initial=False):
    """切换背景音乐
    :param next: 是否切换下一首
    :param initial: 是否是初始化调用
    """
    global current_bgm_index
    try:
        pygame.mixer.music.stop()
        if not initial:  # 非初始化调用才修改索引
            if next:
                current_bgm_index = (current_bgm_index + 1) % len(BGM_PATHS)
            else:
                current_bgm_index = (current_bgm_index - 1) % len(BGM_PATHS)
        pygame.mixer.music.load(BGM_PATHS[current_bgm_index])
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"切换BGM失败: {e}")

# 修改初始化调用方式（约第110行附近）
try:
    # 初始直接播放current_bgm_index对应的音乐（不修改索引）
    pygame.mixer.music.load(BGM_PATHS[current_bgm_index])
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"警告：背景音乐加载失败：{e}")
# 在游戏事件处理部分添加切换检测（找到KEYDOWN事件处理部分）

# !!! 关键修复：在加载任何资源前设置显示模式 !!!
# 使用初始尺寸，后续会被动态调整
screen = pygame.display.set_mode((INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT))
SCREEN_WIDTH = INITIAL_SCREEN_WIDTH
SCREEN_HEIGHT = INITIAL_SCREEN_HEIGHT
pygame.display.set_caption("推箱子")  # 初始标题

# --- 加载资源 ---
# 字体
CHINESE_FONT_NAME = "NotoSansSC-Regular.otf"  # 请确保此字体文件在 assets/fonts/
CHINESE_FONT_PATH = os.path.join(FONTS_DIR, CHINESE_FONT_NAME)

if not os.path.exists(CHINESE_FONT_PATH):
    print(f"错误：找不到字体文件 {CHINESE_FONT_PATH}")
    print(f"请将 '{CHINESE_FONT_NAME}' (或其他中文字体) 放置于 '{FONTS_DIR}' 目录下。")
    fallback_font = pygame.font.match_font("simhei,microsoftyahei,arialunicodems")  # 增加arialunicodeMS
    if fallback_font:
        CHINESE_FONT_PATH = fallback_font
        print(f"警告：将使用系统字体 '{CHINESE_FONT_PATH}'。")
    else:
        CHINESE_FONT_PATH = pygame.font.get_default_font()
        print(f"警告：将使用默认字体 '{CHINESE_FONT_PATH}'，可能不支持中文。")
try:
    FONT_LARGE = pygame.font.Font(CHINESE_FONT_PATH, 48)
    FONT_MEDIUM = pygame.font.Font(CHINESE_FONT_PATH, 32)  # 调整了中号字体大小
    FONT_SMALL = pygame.font.Font(CHINESE_FONT_PATH, 22)  # 调整了小号字体大小
    FONT_BUTTON = pygame.font.Font(CHINESE_FONT_PATH, 28)  # 按钮专用字体
except pygame.error as e:
    print(f"加载字体失败: {e}. 游戏无法继续。")
    pygame.quit()
    sys.exit()

# 图片
IMAGES = {}
IMAGE_FILES = {
    "wall": "wall.png", "floor": "floor.png", "player": "player.png",
    "box": "box.png", "goal": "goal.png", "box_on_goal": "box_on_goal.png",
    "player_on_goal": "player_on_goal.png"
}


def load_images():
    global TILE_SIZE
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
        print("\n由于一个或多个图片资源加载失败，游戏无法启动。请检查以上错误信息。")
        pygame.quit()
        sys.exit()
    if not IMAGES:
        print("错误：没有任何图片被加载。")
        pygame.quit()
        sys.exit()


# --- 游戏状态和数据 ---
game_state = "menu"
current_level_index = 0
levels = []
current_level_data = []
player_pos = (0, 0)
history = []
MAX_HISTORY = 50


# --- 辅助函数 (与上一版基本相同，细节微调) ---
def load_levels_from_disk():
    global levels
    levels = []
    if not os.path.exists(LEVELS_DIR):
        print(f"错误：关卡目录 '{LEVELS_DIR}' 未找到。")
        return False
    level_files_found = False
    for i in range(1, 100):
        level_file_path = os.path.join(LEVELS_DIR, f"level{i}.txt")
        if os.path.exists(level_file_path):
            level_files_found = True
            try:
                with open(level_file_path, 'r', encoding='utf-8') as f:
                    level_map = [list(line.rstrip('\n')) for line in f.readlines() if line.strip()]
                if not level_map or not any(row for row in level_map):  # 确保关卡不是完全空的
                    print(f"警告：关卡文件 '{level_file_path}' 为空或格式不正确。已跳过。")
                    continue
                levels.append(level_map)
                # print(f"成功: 关卡 {i} 从 '{level_file_path}' 加载。")
            except Exception as e:
                print(f"错误: 加载关卡文件 '{level_file_path}' 失败: {e}")
        elif level_files_found:  # 如果之前找到过文件，但现在这个序号的找不到了，说明结束了
            break
        elif i > 5 and not level_files_found:  # 尝试了5个还没找到level1，可能就没有
            break
    if not levels:
        print("错误：在 'levels' 文件夹中没有成功加载任何关卡文件。")
        return False
    print(f"成功加载 {len(levels)} 个关卡。")
    return True


def setup_level(level_idx):
    global current_level_data, player_pos, game_state, history, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    if not (0 <= level_idx < len(levels)):
        game_state = "game_complete" if levels else "error_no_levels"
        return

    current_level_data = [row[:] for row in levels[level_idx]]
    history = []
    max_cols = 0
    player_found = False
    for r, row_data in enumerate(current_level_data):
        max_cols = max(max_cols, len(row_data))
        for c, char in enumerate(row_data):
            if char == PLAYER:
                player_pos = (r, c)
                current_level_data[r][c] = FLOOR
                player_found = True
            elif char == PLAYER_ON_GOAL:
                player_pos = (r, c)
                current_level_data[r][c] = GOAL
                player_found = True
    if not player_found:
        print(f"错误：关卡 {level_idx + 1} 中未找到玩家初始位置 ('@' 或 '+')。将返回菜单。")
        game_state = "menu"
        # 确保在返回菜单时，屏幕尺寸适合菜单
        _ = draw_level_selection_menu(screen, current_level_index if levels else 0)
        return

    num_rows = len(current_level_data)
    num_cols = max_cols if max_cols > 0 else 10  # 默认列数，防止0

    info_area_height = TILE_SIZE * 2
    new_screen_width = num_cols * TILE_SIZE
    new_screen_height = num_rows * TILE_SIZE + info_area_height

    MIN_GAME_SCREEN_WIDTH = 400  # 游戏界面最小宽度
    MIN_GAME_SCREEN_HEIGHT = 300 + info_area_height
    SCREEN_WIDTH = max(new_screen_width, MIN_GAME_SCREEN_WIDTH)
    SCREEN_HEIGHT = max(new_screen_height, MIN_GAME_SCREEN_HEIGHT)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"推箱子 - 关卡 {level_idx + 1}")
    game_state = "playing"
    save_current_state_to_history()


def get_tile_at(r, c):
    if 0 <= r < len(current_level_data) and 0 <= c < len(current_level_data[r]):
        return current_level_data[r][c]
    return WALL


def set_tile_at(r, c, tile_char):
    if 0 <= r < len(current_level_data) and 0 <= c < len(current_level_data[r]):
        current_level_data[r][c] = tile_char


def is_original_goal_tile(r, c):
    if 0 <= current_level_index < len(levels) and \
            0 <= r < len(levels[current_level_index]) and \
            0 <= c < len(levels[current_level_index][r]):
        original_char = levels[current_level_index][r][c]
        return original_char in [GOAL, PLAYER_ON_GOAL, BOX_ON_GOAL]
    return False


def move_player_and_boxes(dr, dc):
    global player_pos
    cr, cc = player_pos
    nr, nc = cr + dr, cc + dc
    tile_at_next = get_tile_at(nr, nc)

    if tile_at_next == WALL:
        return False
    if tile_at_next == FLOOR or tile_at_next == GOAL:
        player_pos = (nr, nc)
        save_current_state_to_history()
        if move_sound:
            move_sound.play()
        return True
    if tile_at_next == BOX or tile_at_next == BOX_ON_GOAL:
        box_nr, box_nc = nr + dr, nc + dc
        tile_behind_box = get_tile_at(box_nr, box_nc)
        if tile_behind_box == WALL or tile_behind_box == BOX or tile_behind_box == BOX_ON_GOAL:
            return False
        set_tile_at(box_nr, box_nc, BOX_ON_GOAL if is_original_goal_tile(box_nr, box_nc) else BOX)
        set_tile_at(nr, nc, GOAL if tile_at_next == BOX_ON_GOAL else FLOOR)
        player_pos = (nr, nc)
        save_current_state_to_history()
        if move_sound:
            move_sound.play()
        return True
    return False



def check_level_win_condition():
    for r, row in enumerate(current_level_data):
        for c, tile in enumerate(row):
            if is_original_goal_tile(r, c) and tile != BOX_ON_GOAL:
                return False
    return True


def save_current_state_to_history():
    history.append(([row[:] for row in current_level_data], player_pos))
    if len(history) > MAX_HISTORY: history.pop(0)


def undo_last_move():
    global current_level_data, player_pos
    if len(history) > 1:
        history.pop()
        last_map_state, last_player_pos = history[-1]
        current_level_data = [row[:] for row in last_map_state]
        player_pos = last_player_pos
    elif len(history) == 1:
        print("提示: 已在初始状态。")


def draw_text(text, font, color, surface, x, y, centered=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


# --- UI绘制函数 ---
MENU_BUTTONS_PER_ROW = 5
MENU_BUTTON_WIDTH = 100  # 按钮宽度
MENU_BUTTON_HEIGHT = 70  # 按钮高度
MENU_BUTTON_PADDING = 20
MENU_BORDER_RADIUS = 8


def draw_level_selection_menu(screen_surface, selected_button_idx):
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen

    screen_surface.fill(MENU_BACKGROUND_COLOR)

    if not levels:
        # 调整屏幕适应错误消息
        current_caption = pygame.display.get_caption()
        SCREEN_WIDTH, SCREEN_HEIGHT = 700, 350
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if current_caption: pygame.display.set_caption(current_caption[0])  # 恢复标题

        screen_surface.fill(MENU_BACKGROUND_COLOR)  # 重新填充新尺寸的屏幕
        draw_text("错误：未找到或加载任何关卡！", FONT_MEDIUM, RED, screen_surface, SCREEN_WIDTH // 2, 80, centered=True)
        draw_text(f"请在 '{LEVELS_DIR}' 目录下", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, SCREEN_WIDTH // 2,
                  150, centered=True)
        draw_text("添加有效的关卡文件 (如 level1.txt)。", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface,
                  SCREEN_WIDTH // 2, 180, centered=True)

        quit_btn_rect = pygame.Rect(0, 0, 200, 50)
        quit_btn_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
        is_hovered = quit_btn_rect.collidepoint(pygame.mouse.get_pos())
        btn_color = MENU_QUIT_BUTTON_HOVER_COLOR if is_hovered else MENU_QUIT_BUTTON_COLOR
        pygame.draw.rect(screen_surface, btn_color, quit_btn_rect, border_radius=MENU_BORDER_RADIUS)
        pygame.draw.rect(screen_surface, MENU_BUTTON_BORDER_COLOR, quit_btn_rect, 2, border_radius=MENU_BORDER_RADIUS)
        draw_text("退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, quit_btn_rect.centerx,
                  quit_btn_rect.centery, centered=True)
        return [quit_btn_rect]

    title_area_height = 100
    draw_text("选择关卡", FONT_LARGE, MENU_TITLE_COLOR, screen_surface, SCREEN_WIDTH // 2, title_area_height // 2,
              centered=True)

    num_button_rows = (len(levels) + MENU_BUTTONS_PER_ROW - 1) // MENU_BUTTONS_PER_ROW
    buttons_grid_width = MENU_BUTTONS_PER_ROW * (MENU_BUTTON_WIDTH + MENU_BUTTON_PADDING) - MENU_BUTTON_PADDING
    buttons_grid_height = num_button_rows * (MENU_BUTTON_HEIGHT + MENU_BUTTON_PADDING) - MENU_BUTTON_PADDING

    horizontal_margin = 80
    vertical_margin_bottom = 100  # 为退出按钮留空间

    # 动态调整屏幕尺寸
    new_screen_width = max(buttons_grid_width + horizontal_margin * 2, INITIAL_SCREEN_WIDTH * 1)
    new_screen_height = title_area_height + buttons_grid_height + vertical_margin_bottom + 50  # 增加一些额外空间

    if SCREEN_WIDTH != new_screen_width or SCREEN_HEIGHT != new_screen_height:
        SCREEN_WIDTH, SCREEN_HEIGHT = int(new_screen_width), int(new_screen_height)
        current_caption = pygame.display.get_caption()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if current_caption: pygame.display.set_caption(current_caption[0])
        screen_surface.fill(MENU_BACKGROUND_COLOR)  # 重新填充
        draw_text("选择关卡", FONT_LARGE, MENU_TITLE_COLOR, screen_surface, SCREEN_WIDTH // 2, title_area_height // 2,
                  centered=True)  # 重绘标题

    button_rects = []
    grid_start_x = (SCREEN_WIDTH - buttons_grid_width) // 2
    grid_start_y = title_area_height + 20

    mouse_pos = pygame.mouse.get_pos()

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
        draw_text(str(i + 1), FONT_BUTTON, MENU_BUTTON_TEXT_COLOR, screen_surface, rect.centerx, rect.centery,
                  centered=True)

    # 退出按钮
    quit_btn_width = 220
    quit_btn_height = 50
    quit_btn_rect = pygame.Rect((SCREEN_WIDTH - quit_btn_width) // 2, SCREEN_HEIGHT - quit_btn_height - 30,
                                quit_btn_width, quit_btn_height)
    button_rects.append(quit_btn_rect)

    is_quit_selected_by_kb = (selected_button_idx == len(levels))  # 退出按钮是最后一个"虚拟"索引
    is_quit_hovered_by_mouse = quit_btn_rect.collidepoint(mouse_pos)
    quit_color = MENU_QUIT_BUTTON_COLOR
    if is_quit_hovered_by_mouse or is_quit_selected_by_kb:
        quit_color = MENU_QUIT_BUTTON_HOVER_COLOR

    pygame.draw.rect(screen_surface, quit_color, quit_btn_rect, border_radius=MENU_BORDER_RADIUS)
    quit_border_color = MENU_BUTTON_SELECTED_BORDER_COLOR if is_quit_selected_by_kb else MENU_BUTTON_BORDER_COLOR
    pygame.draw.rect(screen_surface, quit_border_color, quit_btn_rect, 2, border_radius=MENU_BORDER_RADIUS)
    draw_text("退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, quit_btn_rect.centerx,
              quit_btn_rect.centery, centered=True)

    return button_rects


def draw_game_screen(screen_surface):
    screen_surface.fill(BLACK)  # 游戏区域背景色
    for r, row in enumerate(current_level_data):
        for c, tile_id in enumerate(row):
            draw_pos = (c * TILE_SIZE, r * TILE_SIZE)
            if is_original_goal_tile(r, c):
                screen_surface.blit(IMAGES["goal"], draw_pos)
            else:
                screen_surface.blit(IMAGES["floor"], draw_pos)

            if tile_id == WALL:
                screen_surface.blit(IMAGES["wall"], draw_pos)
            elif tile_id == BOX:
                screen_surface.blit(IMAGES["box"], draw_pos)
            elif tile_id == BOX_ON_GOAL:
                screen_surface.blit(IMAGES["box_on_goal"], draw_pos)

    pr, pc = player_pos
    player_img_key = "player_on_goal" if "player_on_goal" in IMAGES and is_original_goal_tile(pr, pc) else "player"
    screen_surface.blit(IMAGES[player_img_key], (pc * TILE_SIZE, pr * TILE_SIZE))

    info_area_y = len(current_level_data) * TILE_SIZE
    pygame.draw.rect(screen_surface, GAME_INFO_BG_COLOR, (0, info_area_y, SCREEN_WIDTH, SCREEN_HEIGHT - info_area_y))
    pad, line_h = 15, 28
    draw_text(f"关卡: {current_level_index + 1}/{len(levels)}", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad,
              info_area_y + pad)
    draw_text("R: 重玩", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad, info_area_y + pad + line_h)
    draw_text("U: 撤销", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad + 120, info_area_y + pad + line_h)
    draw_text("B/V: 切换bgm", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, pad + 240, info_area_y + pad + line_h)
    draw_text("Esc: 菜单", FONT_SMALL, GAME_INFO_TEXT_COLOR, screen_surface, SCREEN_WIDTH - 150 - pad,
              info_area_y + pad)

    if game_state == "level_complete":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen_surface.blit(overlay, (0, 0))
        draw_text("关卡完成!", FONT_LARGE, GREEN, screen_surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40,
                  centered=True)
        draw_text("按 Enter 或 空格 继续", FONT_MEDIUM, WHITE, screen_surface, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 + 20, centered=True)


def draw_game_completion_screen(screen_surface):
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen  # 允许修改全局 screen
    # 固定通关界面尺寸
    target_width, target_height = 700, 400
    if SCREEN_WIDTH != target_width or SCREEN_HEIGHT != target_height:
        SCREEN_WIDTH, SCREEN_HEIGHT = target_width, target_height
        current_caption = pygame.display.get_caption()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if current_caption: pygame.display.set_caption(current_caption[0])

    screen_surface.fill(MENU_BACKGROUND_COLOR)  # 使用菜单背景色
    draw_text("恭喜你，全部通关!", FONT_LARGE, GREEN, screen_surface, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70,
              centered=True)
    draw_text("你是推箱子大师！", FONT_MEDIUM, MENU_TITLE_COLOR, screen_surface, SCREEN_WIDTH // 2,
              SCREEN_HEIGHT // 2 - 10, centered=True)
    draw_text("按 Esc 返回菜单，或 Q 退出游戏", FONT_SMALL, MENU_BUTTON_TEXT_COLOR, screen_surface, SCREEN_WIDTH // 2,
              SCREEN_HEIGHT // 2 + 50, centered=True)


# --- 主程序 ---
def main():
    global game_state, current_level_index, screen, SCREEN_WIDTH, SCREEN_HEIGHT

    load_images()  # 现在这个函数在 screen 初始化之后调用
    if not load_levels_from_disk():
        game_state = "error_no_levels"

    pygame.display.set_caption("推箱子")  # 确保标题被设置

    clock = pygame.time.Clock()
    running = True
    menu_selected_idx = 0

    # 确保首次进入菜单时，屏幕尺寸是为菜单优化的
    if game_state == "menu" or game_state == "error_no_levels":
        _ = draw_level_selection_menu(screen, menu_selected_idx)

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            if game_state == "menu":
                current_menu_buttons = draw_level_selection_menu(screen, menu_selected_idx)  # 获取按钮

            #鼠标悬停更新 selected_idx (仅用于视觉，不触发动作)
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(current_menu_buttons):
                        if rect.collidepoint(mouse_pos):
                            menu_selected_idx = i # 这样会导致键盘选择被鼠标覆盖
                            break
                           #else: menu_selected_idx = -1 # 取消悬停高亮

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(current_menu_buttons):
                        if rect.collidepoint(mouse_pos):
                            if i < len(levels):  # 点击关卡按钮
                                current_level_index = i
                                menu_selected_idx = i  # 更新键盘焦点
                                setup_level(current_level_index)
                            elif i == len(current_menu_buttons) - 1:  # 点击退出按钮
                                running = False
                            break
                if event.type == pygame.KEYDOWN:
                    if game_state == "menu":
                        if event.type == pygame.KEYDOWN:
                            # 添加音乐切换检测 ↓↓↓
                            if event.key == pygame.K_b:
                                switch_bgm()
                                continue  # 阻止后续处理
                            elif event.key == pygame.K_v:
                                switch_bgm(next=False)
                                continue
                    if not levels and game_state == "error_no_levels":  # 无关卡时
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: running = False
                        continue

                    num_menu_options = len(levels) + 1  # 关卡数 + 退出按钮
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        menu_selected_idx = (menu_selected_idx - 1 + num_menu_options) % num_menu_options
                    elif event.key == pygame.K_RIGHT:
                        menu_selected_idx = (menu_selected_idx + 1) % num_menu_options
                    elif event.key == pygame.K_UP:
                        new_idx = menu_selected_idx - MENU_BUTTONS_PER_ROW
                        if new_idx < 0:  # 如果已经在最顶行或退出按钮，尝试跳到最后一行的对应列或最后一个关卡
                            if menu_selected_idx == num_menu_options - 1:  # 是退出按钮
                                new_idx = len(levels) - 1  # 跳到最后一个关卡
                            else:  # 在第一行
                                new_idx = num_menu_options - 1  # 跳到退出按钮
                        menu_selected_idx = max(0, new_idx)

                    elif event.key == pygame.K_DOWN:
                        new_idx = menu_selected_idx + MENU_BUTTONS_PER_ROW
                        if menu_selected_idx == num_menu_options - 1:  # 是退出按钮
                            new_idx = 0  # 跳到第一个关卡
                        elif new_idx >= len(levels) and menu_selected_idx < len(levels):  # 从关卡按钮向下超出了
                            new_idx = num_menu_options - 1  # 跳到退出按钮
                        menu_selected_idx = min(num_menu_options - 1, new_idx)

                    menu_selected_idx = max(0, min(menu_selected_idx, num_menu_options - 1))  # 确保在范围内

                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if 0 <= menu_selected_idx < len(levels):
                            current_level_index = menu_selected_idx
                            setup_level(current_level_index)
                        elif menu_selected_idx == len(levels):  # 选中退出按钮
                            running = False

            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        moved = move_player_and_boxes(-1, 0)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        moved = move_player_and_boxes(1, 0)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        moved = move_player_and_boxes(0, -1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        moved = move_player_and_boxes(0, 1)
                    elif event.key == pygame.K_r:
                        setup_level(current_level_index)
                    elif event.key == pygame.K_u:
                        undo_last_move()
                    elif event.key == pygame.K_b:  # 按B键切换下一首
                        switch_bgm()
                    elif event.key == pygame.K_v:  # 按V键切换上一首
                        switch_bgm(next=False)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                        _ = draw_level_selection_menu(screen, current_level_index if levels else 0)  # 适应菜单屏幕
                    if moved and check_level_win_condition(): game_state = "level_complete"

            elif game_state == "level_complete":
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        current_level_index += 1
                        if current_level_index < len(levels):
                            setup_level(current_level_index)
                        else:
                            game_state = "game_complete"
                            _ = draw_game_completion_screen(screen)  # 适应通关屏幕
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                        _ = draw_level_selection_menu(screen, current_level_index if levels else 0)

            elif game_state == "game_complete":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                        current_level_index = 0
                        menu_selected_idx = 0
                        _ = draw_level_selection_menu(screen, menu_selected_idx)
                    elif event.key == pygame.K_q:
                        running = False

            elif game_state == "error_no_levels":  # 主要通过draw函数显示，事件只处理退出
                current_menu_buttons = draw_level_selection_menu(screen, -1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if current_menu_buttons and current_menu_buttons[0].collidepoint(mouse_pos): running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q, pygame.K_RETURN, pygame.K_SPACE]: running = False

        # --- 绘制 ---
        current_display_surface = pygame.display.get_surface()  # 获取当前有效的surface
        if game_state == "menu" or game_state == "error_no_levels":
            draw_level_selection_menu(current_display_surface, menu_selected_idx if game_state == "menu" else -1)
        elif game_state == "playing" or game_state == "level_complete":
            draw_game_screen(current_display_surface)
        elif game_state == "game_complete":
            draw_game_completion_screen(current_display_surface)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()