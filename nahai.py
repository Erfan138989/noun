import pygame, sys
from button import Button
import arabic_reshaper
from bidi.algorithm import get_display

# تعریف قسمت‌های مختلف اسکلت و محدوده‌های آنها بر اساس تصویر اصلی (730x1222)
original_skeleton_parts = {
    "جمجمه": (290, 50, 440, 160),
    "ستون فقرات": (345, 160, 385, 500),
    "قفسه سینه": (250, 160, 480, 350),
    "استخوان لگن": (260, 460, 470, 550),
    "بازوی چپ": (100, 250, 250, 500),
    "بازوی راست": (480, 250, 630, 500),
    "پای چپ": (300, 550, 360, 1100),  # تغییر در y2
    "پای راست": (390, 550, 450, 1100),  # تغییر در y2
}

# اطلاعات درباره‌ی قسمت‌های اسکلت
skeleton_info = {
    "جمجمه": "جمجمه شامل ۲۲ استخوان است که از مغز و اجزای داخلی ان محافظت می‌کنند.",
    "ستون فقرات": " ستون فقرات شامل ۳۳ مهره است که به حرکت و پشتیبانی بدن کمک می‌کند و از نخاع محافظت میکند",
    "قفسه سینه": "این قسمت شامل دنده‌ها و استخوان جناغ است که از اندام‌های داخلی به خصوص قلب محافظت می‌کنند.",
    "استخوان لگن": "لگن بخشی از اسکلت است که وزن بدن را تحمل کرده و به حرکت کمک می‌کند.",
    "بازوی چپ": " بازو شامل استخوان‌های بازو، ساعد، و مچ دست است که با ماهیچه ی دوسر و سه سر حرکت میکند",
    "بازوی راست": "بازو شامل استخوان‌های بازو، ساعد، و مچ دست است که با ماهیچه ی دوسر و سه سر حرکت میکند",
    "پای چپ": "پای چپ شامل استخوان ران، درشت‌نی، نازک‌نی و استخوان‌های کف پا است که با ماهیجه ی دوسر و چهارسر حرکت میکند",
    "پای راست": "پای راست شامل استخوان ران، درشت‌نی، نازک‌نی و استخوان‌های کف پا است که با ماهیجه ی دوسر و چهارسر حرکت میکند",
}

# تابع مقیاس‌بندی مختصات
def scale_coordinates(parts, original_width, original_height, new_width, new_height):
    scale_width = new_width / original_width
    scale_height = new_height / original_height
    scaled_parts = {}
    for part, (x1, y1, x2, y2) in parts.items():
        scaled_x1 = int(x1 * scale_width)
        scaled_y1 = int(y1 * scale_height)
        scaled_x2 = int(x2 * scale_width)
        scaled_y2 = int(y2 * scale_height)
        scaled_parts[part] = (scaled_x1, scaled_y1, scaled_x2, scaled_y2)
    return scaled_parts

# مقیاس‌بندی قسمت‌های اسکلت به اندازه 1080x720
skeleton_parts = scale_coordinates(original_skeleton_parts, 730, 1222, 1080, 720)

# تابع برای بارگذاری فونت
def get_font(size, font_name="font.ttf"):
    return pygame.font.Font(f"assets/{font_name}", size)

# تابع منوی اصلی
def main_menu():
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")
    BG = pygame.image.load("assets/Background.png")

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    skeleton_app = SkeletonApp("Skeleton.jpg")  # ایجاد نمونه از کلاس SkeletonApp
                    skeleton_app.run()  # اجرای صفحه اسکلت
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(SCREEN)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# تابع صفحه OPTIONS
def options(SCREEN):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        OPTIONS_TEXT = get_font(45).render("nothiG", True, "Blue")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

# کلاس نمایش اسکلت
class SkeletonApp:
    def __init__(self, image_path):
        self.screen = pygame.display.set_mode((1080, 720))  # تنظیم اندازه پنجره به 1080x720
        pygame.display.set_caption("اسکلت انسان - نمایش تعاملی")
        
        # بارگذاری تصویر اسکلت و مقیاس‌بندی آن به 1080x720
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1080, 720))
        
        # بارگذاری فونت فارسی
        self.font = pygame.font.Font("Vazir.ttf", 20)
        self.tooltip_font = pygame.font.Font("Vazir.ttf", 18)
        self.tooltip_text = ""
        self.tooltip_pos = (0, 0)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.on_mouse_move(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.on_mouse_click(event.pos)

            # پر کردن پس‌زمینه
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.image, (0, 0))

            # نمایش tooltip
            if self.tooltip_text:
                reshaped_text = arabic_reshaper.reshape(self.tooltip_text)
                bidi_text = get_display(reshaped_text)
                tooltip_surface = self.tooltip_font.render(bidi_text, True, (0, 0, 0))
                self.screen.blit(tooltip_surface, self.tooltip_pos)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def on_mouse_move(self, pos):
        """ بررسی می‌کند که آیا ماوس روی یکی از قسمت‌ها قرار دارد یا نه. """
        x, y = pos
        for part, (x1, y1, x2, y2) in skeleton_parts.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.tooltip_text = part
                self.tooltip_pos = (x + 10, y + 10)
                return
        self.tooltip_text = ""

    def on_mouse_click(self, pos):
        """ بررسی کلیک ماوس روی یکی از قسمت‌های اسکلت. """
        x, y = pos
        for part, (x1, y1, x2, y2) in skeleton_parts.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.show_skeleton_info(part)
                return

    def show_skeleton_info(self, part):
        """ نمایش اطلاعات مربوط به بخش انتخاب‌شده. """
        info_text = skeleton_info.get(part, "اطلاعات موجود نیست.")
        reshaped_text = arabic_reshaper.reshape(info_text)
        bidi_text = get_display(reshaped_text)
        info_surface = self.font.render(bidi_text, True, (0, 0, 0))
        info_rect = info_surface.get_rect(center=(550,15 ))
        self.screen.blit(info_surface, info_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

# اجرای برنامه
if __name__ == "__main__":
    main_menu()