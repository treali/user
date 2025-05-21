import os
import pygame # For color definitions

# --- 常量定义 ---
INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600
TILE_SIZE = 64  # 您的图片资源的尺寸 (像素)
FPS = 30 # Frames per second

# --- 游戏界面最小尺寸 (setup_level 中使用) ---
MIN_GAME_SCREEN_WIDTH = 400
MIN_GAME_SCREEN_HEIGHT_BASE = 300 # 不包含信息区的高度

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
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# --- 声音资源路径 ---
MOVE_SOUND_PATH = os.path.join(SOUNDS_DIR, "move.wav")
BGM_PATHS = [
    os.path.join(SOUNDS_DIR, "bgm1.ogg"),
    os.path.join(SOUNDS_DIR, "bgm2.ogg"),
    os.path.join(SOUNDS_DIR, "bgm3.ogg")
]

# --- 字体 ---
CHINESE_FONT_NAME = "NotoSansSC-Regular.otf"

# --- UI绘制常量 ---
MENU_BUTTONS_PER_ROW = 5
MENU_BUTTON_WIDTH = 100
MENU_BUTTON_HEIGHT = 70
MENU_BUTTON_PADDING = 20
MENU_BORDER_RADIUS = 8

# --- 游戏状态和数据常量 ---
MAX_HISTORY = 50
