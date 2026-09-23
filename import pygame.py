import pygame
import sys
import random
from collections import deque

# ================= CẤU HÌNH BÀN ĐẤU =================
GRID_WIDTH = 30
GRID_HEIGHT = 20
CELL_SIZE = 28
TOP_BAR_HEIGHT = 75

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + TOP_BAR_HEIGHT

# Cấu hình Gameplay
NUM_APPLES = 3              # Số lượng táo luôn duy trì trên sân (BỎ GIỚI HẠN: ăn là sinh mới vô tận)
NUM_OBSTACLES = 8           # Số lượng khối chướng ngại vật cố định trên bản đồ
MAX_LENGTH = 20             # Độ dài tối đa của rắn (thoải mái lớn)

# Bảng màu hiện đại
COLOR_BG = (15, 18, 28)
COLOR_GRID = (24, 29, 44)
COLOR_BAR = (10, 12, 20)
COLOR_TEXT = (240, 245, 255)
COLOR_TEXT_DIM = (140, 150, 175)

# Chướng ngại vật (Khối đá cản trở)
COLOR_OBSTACLE = (55, 65, 90)
COLOR_OBSTACLE_BORDER = (90, 105, 140)

# Rắn 1: Xanh Neon / Emerald
COLOR_S1_HEAD = (0, 245, 160)
COLOR_S1_BODY1 = (0, 200, 130)
COLOR_S1_BODY2 = (14, 116, 144)
COLOR_S1_BADGE = (16, 185, 129)

# Rắn 2: Hồng / Tím Neon
COLOR_S2_HEAD = (255, 60, 130)
COLOR_S2_BODY1 = (225, 29, 72)
COLOR_S2_BODY2 = (168, 85, 247)
COLOR_S2_BADGE = (236, 72, 153)

# Thức ăn
COLOR_APPLE = (255, 190, 0)
COLOR_APPLE_GLOW = (255, 230, 100)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# ================= THUẬT TOÁN TÌM ĐƯỜNG BFS =================
def bfs_path(start, target, obstacles):
    """Tìm đường ngắn nhất từ start tới target tránh toàn bộ vật cản."""
    queue = deque([start])
    parent = {start: None}
    obs_set = set(obstacles)

    while queue:
        curr = queue.popleft()
        if curr == target:
            break
        for dx, dy in DIRECTIONS:
            nxt = (curr[0] + dx, curr[1] + dy)
            if 0 <= nxt[0] < GRID_WIDTH and 0 <= nxt[1] < GRID_HEIGHT:
                if nxt not in obs_set and nxt not in parent:
                    parent[nxt] = curr
                    queue.append(nxt)

    if target not in parent:
        return None

    path = []
    curr = target
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path

def get_competitive_ai_move(my_snake, opp_snake, foods, obstacles):
    """
    AI ĐỐI KHÁNG TRÁNH CHƯỚNG NGẠI VẬT:
    - Coi chướng ngại vật, thân đối thủ và thân mình là vật cản chết người.
    - Tìm đường an toàn nhất tới các quả táo (vô hạn).
    - Nếu bị dồn ép: bám đuôi chính mình để sống sót và chờ đối thủ mắc lỗi.
    """
    my_head = my_snake[0]
    opp_head = opp_snake[0]

    # Toàn bộ vật cản: chướng ngại vật cố định + thân mình + toàn bộ thân đối thủ
    all_obs = set(obstacles) | set(my_snake[:-1]) | set(opp_snake)

    # Vùng nguy hiểm quanh đầu đối thủ (tránh tông trực diện nếu đối thủ dài hơn hoặc bằng)
    danger_cells = set()
    if len(opp_snake) >= len(my_snake):
        for dx, dy in DIRECTIONS:
            danger_cells.add((opp_head[0] + dx, opp_head[1] + dy))

    # 1. Tìm quả táo gần nhất có đường an toàn
    best_path = None
    min_dist = float('inf')

    for food in foods:
        path = bfs_path(my_head, food, all_obs | danger_cells)
        if not path and danger_cells:
            path = bfs_path(my_head, food, all_obs)

        if path and len(path) < min_dist:
            min_dist = len(path)
            best_path = path

    # 2. Kiểm tra an toàn (sau khi ăn táo có còn đường về đuôi không)
    if best_path:
        first_step = best_path[0]
        virtual_body = [first_step] + my_snake[:-1]
        virtual_tail = my_snake[-1]
        if bfs_path(first_step, virtual_tail, all_obs | set(virtual_body[:-1])) is not None:
            return (first_step[0] - my_head[0], first_step[1] - my_head[1])
        elif len(my_snake) < 6:
            return (first_step[0] - my_head[0], first_step[1] - my_head[1])

    # 3. Kế hoạch B: Bám đuôi chính mình (Tail-chasing)
    my_tail = my_snake[-1]
    best_move = None
    max_dist = -1

    for dx, dy in DIRECTIONS:
        nxt = (my_head[0] + dx, my_head[1] + dy)
        if 0 <= nxt[0] < GRID_WIDTH and 0 <= nxt[1] < GRID_HEIGHT:
            if nxt not in all_obs and nxt not in danger_cells:
                virtual_body = [nxt] + my_snake[:-1]
                if bfs_path(nxt, my_tail, all_obs | set(virtual_body[:-1])) is not None:
                    dist = abs(nxt[0] - opp_head[0]) + abs(nxt[1] - opp_head[1])
                    if dist > max_dist:
                        max_dist = dist
                        best_move = (dx, dy)

    # 4. Nước đi sinh tồn bất kỳ ô trống nào
    if best_move is None:
        for dx, dy in DIRECTIONS:
            nxt = (my_head[0] + dx, my_head[1] + dy)
            if 0 <= nxt[0] < GRID_WIDTH and 0 <= nxt[1] < GRID_HEIGHT:
                if nxt not in all_obs:
                    return (dx, dy)

    return best_move

# ================= CLASS GAME ĐỐI KHÁNG CHƯỚNG NGẠI VẬT =================
class ObstacleSnakeDuelGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("⚔️ Snake Duel: Đấu Kháng Chướng Ngại Vật (Táo Vô Hạn)")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_main = pygame.font.SysFont("segoe ui, arial, sans-serif", 18, bold=True)
        self.font_title = pygame.font.SysFont("segoe ui, arial, sans-serif", 22, bold=True)
        self.font_huge = pygame.font.SysFont("segoe ui, arial, sans-serif", 28, bold=True)
        self.font_small = pygame.font.SysFont("segoe ui, arial, sans-serif", 14)

        self.s1_auto = True   # Snake 1 AI (Phím 1)
        self.s2_auto = True   # Snake 2 AI (Phím 2)
        self.fps = 15
        self.paused = False

        self.s1_wins = 0
        self.s2_wins = 0
        self.reset()

    def generate_obstacles(self):
        """Tạo các khối chướng ngại vật phân bố trên sân đấu."""
        obstacles = set()
        safe_zone = set(self.s1) | set(self.s2)
        for dx in range(-2, 5):
            safe_zone.add((self.s1[0][0] + dx, self.s1[0][1]))
            safe_zone.add((self.s2[0][0] - dx, self.s2[0][1]))

        while len(obstacles) < NUM_OBSTACLES:
            ox = random.randint(2, GRID_WIDTH - 3)
            oy = random.randint(2, GRID_HEIGHT - 3)
            if (ox, oy) not in safe_zone:
                obstacles.add((ox, oy))
        return list(obstacles)

    def reset(self):
        mid_y = GRID_HEIGHT // 2

        self.s1 = [(5, mid_y), (4, mid_y), (3, mid_y), (2, mid_y)]
        self.s1_dir = RIGHT
        self.s1_next_dir = RIGHT
        self.s1_score = 0

        self.s2 = [(GRID_WIDTH - 6, mid_y), (GRID_WIDTH - 5, mid_y), (GRID_WIDTH - 4, mid_y), (GRID_WIDTH - 3, mid_y)]
        self.s2_dir = LEFT
        self.s2_next_dir = LEFT
        self.s2_score = 0

        # Tạo chướng ngại vật cố định
        self.obstacles = self.generate_obstacles()

        # Tạo thức ăn vô hạn (luôn duy trì NUM_APPLES quả trên sân)
        self.foods = []
        for _ in range(NUM_APPLES):
            self.spawn_food()

        self.game_over = False
        self.winner_msg = ""
        self.winner_color = COLOR_TEXT

    def spawn_food(self):
        all_occupied = set(self.s1) | set(self.s2) | set(self.obstacles) | set(self.foods)
        empty = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in all_occupied
        ]
        if empty:
            self.foods.append(random.choice(empty))

    def step(self):
        if self.game_over or self.paused:
            return

        # 1. Hướng đi AI / Thủ công
        if self.s1_auto:
            mv1 = get_competitive_ai_move(self.s1, self.s2, self.foods, self.obstacles)
            if mv1: self.s1_dir = mv1
        else:
            self.s1_dir = self.s1_next_dir

        if self.s2_auto:
            mv2 = get_competitive_ai_move(self.s2, self.s1, self.foods, self.obstacles)
            if mv2: self.s2_dir = mv2
        else:
            self.s2_dir = self.s2_next_dir

        # 2. Vị trí đầu mới
        head1 = (self.s1[0][0] + self.s1_dir[0], self.s1[0][1] + self.s1_dir[1])
        head2 = (self.s2[0][0] + self.s2_dir[0], self.s2[0][1] + self.s2_dir[1])

        # 3. Kiểm tra va chạm TƯỜNG
        s1_hit_wall = not (0 <= head1[0] < GRID_WIDTH and 0 <= head1[1] < GRID_HEIGHT)
        s2_hit_wall = not (0 <= head2[0] < GRID_WIDTH and 0 <= head2[1] < GRID_HEIGHT)

        # 4. Kiểm tra va chạm CHƯỚNG NGẠI VẬT CỐ ĐỊNH
        s1_hit_obs = head1 in self.obstacles
        s2_hit_obs = head2 in self.obstacles

        # 5. Kiểm tra TỰ CẮN MÌNH
        s1_hit_self = head1 in self.s1[:-1]
        s2_hit_self = head2 in self.s2[:-1]

        # 6. Kiểm tra va chạm THÂN ĐỐI THỦ (Thân đối thủ là chướng ngại vật!)
        s1_hit_s2 = head1 in self.s2[:-1]
        s2_hit_s1 = head2 in self.s1[:-1]

        # 7. Đối đầu trực diện
        if head1 == head2:
            self.game_over = True
            if len(self.s1) > len(self.s2):
                self.winner_msg = "SNAKE 1 CHIẾN THẮNG! (Dài hơn khi đối đầu)"
                self.winner_color = COLOR_S1_HEAD
                self.s1_wins += 1
            elif len(self.s2) > len(self.s1):
                self.winner_msg = "SNAKE 2 CHIẾN THẮNG! (Dài hơn khi đối đầu)"
                self.winner_color = COLOR_S2_HEAD
                self.s2_wins += 1
            else:
                self.winner_msg = "HÒA NHAU! (Cùng chiều dài khi đâm trực diện)"
                self.winner_color = COLOR_TEXT
            return

        # Phân xử va chạm chướng ngại vật
        s1_dead = s1_hit_wall or s1_hit_obs or s1_hit_self or s1_hit_s2
        s2_dead = s2_hit_wall or s2_hit_obs or s2_hit_self or s2_hit_s1

        if s1_dead and s2_dead:
            self.game_over = True
            self.winner_msg = "HÒA! (Cả 2 cùng đâm chướng ngại vật)"
            self.winner_color = COLOR_TEXT
            return
        elif s1_dead:
            self.game_over = True
            if s1_hit_obs: reason = "đâm vào khối chướng ngại vật"
            elif s1_hit_wall: reason = "đâm vào tường"
            elif s1_hit_s2: reason = "đâm vào thân Snake 2"
            else: reason = "tự cắn vào thân mình"

            self.winner_msg = f"SNAKE 2 CHIẾN THẮNG! (Snake 1 {reason})"
            self.winner_color = COLOR_S2_HEAD
            self.s2_wins += 1
            return
        elif s2_dead:
            self.game_over = True
            if s2_hit_obs: reason = "đâm vào khối chướng ngại vật"
            elif s2_hit_wall: reason = "đâm vào tường"
            elif s2_hit_s1: reason = "đâm vào thân Snake 1"
            else: reason = "tự cắn vào thân mình"

            self.winner_msg = f"SNAKE 1 CHIẾN THẮNG! (Snake 2 {reason})"
            self.winner_color = COLOR_S1_HEAD
            self.s1_wins += 1
            return

        # 8. Di chuyển bước tiến
        self.s1.insert(0, head1)
        self.s2.insert(0, head2)

        # 9. Ăn táo & TỰ ĐỘNG SINH TÁO MỚI (VÔ HẠN)
        if head1 in self.foods:
            self.s1_score += 1
            self.foods.remove(head1)
            self.spawn_food()  # Táo sinh vô tận
            if len(self.s1) > MAX_LENGTH: self.s1.pop()
        else:
            self.s1.pop()

        if head2 in self.foods:
            self.s2_score += 1
            self.foods.remove(head2)
            self.spawn_food()  # Táo sinh vô tận
            if len(self.s2) > MAX_LENGTH: self.s2.pop()
        else:
            self.s2.pop()

    def draw_snake(self, snake, c_head, c_body1, c_body2, direction):
        n = len(snake)
        for i, segment in enumerate(reversed(snake)):
            idx = n - 1 - i
            sx = segment[0] * CELL_SIZE
            sy = segment[1] * CELL_SIZE + TOP_BAR_HEIGHT
            margin = 2
            rect = pygame.Rect(sx + margin, sy + margin, CELL_SIZE - margin * 2, CELL_SIZE - margin * 2)

            if idx == 0:
                pygame.draw.rect(self.screen, c_head, rect, border_radius=8)
                cx, cy = rect.centerx, rect.centery
                dx, dy = direction
                e1 = (cx + 4*dx - 5*dy, cy + 4*dy - 5*dx) if dx != 0 else (cx - 5, cy + 4*dy)
                e2 = (cx + 4*dx + 5*dy, cy + 4*dy + 5*dx) if dx != 0 else (cx + 5, cy + 4*dy)
                pygame.draw.circle(self.screen, (10, 15, 25), e1, 3)
                pygame.draw.circle(self.screen, (10, 15, 25), e2, 3)
            else:
                ratio = idx / max(1, n - 1)
                r = int(c_body1[0] * (1 - ratio) + c_body2[0] * ratio)
                g = int(c_body1[1] * (1 - ratio) + c_body2[1] * ratio)
                b = int(c_body1[2] * (1 - ratio) + c_body2[2] * ratio)
                pygame.draw.rect(self.screen, (r, g, b), rect, border_radius=6)

    def draw_obstacles(self):
        for obs in self.obstacles:
            rx = obs[0] * CELL_SIZE
            ry = obs[1] * CELL_SIZE + TOP_BAR_HEIGHT
            rect = pygame.Rect(rx + 2, ry + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect, border_radius=6)
            pygame.draw.rect(self.screen, COLOR_OBSTACLE_BORDER, rect, width=2, border_radius=6)
            cx, cy = rect.centerx, rect.centery
            pygame.draw.line(self.screen, COLOR_OBSTACLE_BORDER, (cx - 4, cy - 4), (cx + 4, cy + 4), 2)
            pygame.draw.line(self.screen, COLOR_OBSTACLE_BORDER, (cx - 4, cy + 4), (cx + 4, cy - 4), 2)

    def draw(self):
        self.screen.fill(COLOR_BG)

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rx = x * CELL_SIZE
                ry = y * CELL_SIZE + TOP_BAR_HEIGHT
                pygame.draw.rect(self.screen, COLOR_GRID, (rx, ry, CELL_SIZE, CELL_SIZE), 1)

        self.draw_obstacles()

        for food in self.foods:
            fx = food[0] * CELL_SIZE + CELL_SIZE // 2
            fy = food[1] * CELL_SIZE + TOP_BAR_HEIGHT + CELL_SIZE // 2
            rad = CELL_SIZE // 2 - 3
            pygame.draw.circle(self.screen, COLOR_APPLE_GLOW, (fx, fy), rad + 2)
            pygame.draw.circle(self.screen, COLOR_APPLE, (fx, fy), rad)
            pygame.draw.line(self.screen, (120, 220, 90), (fx, fy - rad + 2), (fx + 4, fy - rad - 3), 2)

        self.draw_snake(self.s1, COLOR_S1_HEAD, COLOR_S1_BODY1, COLOR_S1_BODY2, self.s1_dir)
        self.draw_snake(self.s2, COLOR_S2_HEAD, COLOR_S2_BODY1, COLOR_S2_BODY2, self.s2_dir)

        # Top Bar
        pygame.draw.rect(self.screen, COLOR_BAR, (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))
        pygame.draw.line(self.screen, COLOR_GRID, (0, TOP_BAR_HEIGHT - 1), (SCREEN_WIDTH, TOP_BAR_HEIGHT - 1), 2)

        # S1 Info
        s1_tag = "S1 [AI]" if self.s1_auto else "S1 [WASD]"
        s1_badge = pygame.Rect(16, 12, 100, 24)
        pygame.draw.rect(self.screen, COLOR_S1_BADGE, s1_badge, border_radius=6)
        t_s1 = self.font_small.render(s1_tag, True, (255, 255, 255))
        self.screen.blit(t_s1, t_s1.get_rect(center=s1_badge.center))

        s1_txt = self.font_title.render(f"Điểm: {self.s1_score}  (Thắng: {self.s1_wins})", True, COLOR_S1_HEAD)
        self.screen.blit(s1_txt, (16, 42))

        # S2 Info
        s2_tag = "S2 [AI]" if self.s2_auto else "S2 [MŨI TÊN]"
        s2_badge = pygame.Rect(SCREEN_WIDTH - 126, 12, 110, 24)
        pygame.draw.rect(self.screen, COLOR_S2_BADGE, s2_badge, border_radius=6)
        t_s2 = self.font_small.render(s2_tag, True, (255, 255, 255))
        self.screen.blit(t_s2, t_s2.get_rect(center=s2_badge.center))

        s2_str = f"Điểm: {self.s2_score}  (Thắng: {self.s2_wins})"
        s2_txt = self.font_title.render(s2_str, True, COLOR_S2_HEAD)
        self.screen.blit(s2_txt, (SCREEN_WIDTH - s2_txt.get_width() - 16, 42))

        # Trung tâm HUD
        center_info = f"🍎 Táo: Vô hạn ({len(self.foods)} trên sân)  |  🧱 Chướng ngại vật: {NUM_OBSTACLES}"
        c_surf = self.font_small.render(center_info, True, COLOR_TEXT)
        self.screen.blit(c_surf, c_surf.get_rect(center=(SCREEN_WIDTH // 2, 22)))

        guide_txt = self.font_small.render("[1]: AI S1  |  [2]: AI S2  |  [Space]: Dừng  |  [R]: Chơi lại", True, COLOR_TEXT_DIM)
        self.screen.blit(guide_txt, guide_txt.get_rect(center=(SCREEN_WIDTH // 2, 48)))

        # Overlay Kết Thúc
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 185))
            self.screen.blit(overlay, (0, 0))

            win_surf = self.font_huge.render(self.winner_msg, True, self.winner_color)
            self.screen.blit(win_surf, win_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)))

            sub = self.font_main.render("Nhấn [R] để bắt đầu hiệp đấu mới", True, COLOR_TEXT)
            self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)))

        elif self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 130))
            self.screen.blit(overlay, (0, 0))
            p_txt = self.font_huge.render("ĐANG TẠM DỪNG (PAUSED)", True, (255, 215, 0))
            self.screen.blit(p_txt, p_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset()
                    
                    elif event.key in (pygame.K_1, pygame.K_KP1):
                        self.s1_auto = not self.s1_auto
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.s2_auto = not self.s2_auto

                    elif not self.s1_auto:
                        if event.key == pygame.K_w and self.s1_dir != DOWN:
                            self.s1_next_dir = UP
                        elif event.key == pygame.K_s and self.s1_dir != UP:
                            self.s1_next_dir = DOWN
                        elif event.key == pygame.K_a and self.s1_dir != RIGHT:
                            self.s1_next_dir = LEFT
                        elif event.key == pygame.K_d and self.s1_dir != LEFT:
                            self.s1_next_dir = RIGHT

                    elif not self.s2_auto:
                        if event.key == pygame.K_UP and self.s2_dir != DOWN:
                            self.s2_next_dir = UP
                        elif event.key == pygame.K_DOWN and self.s2_dir != UP:
                            self.s2_next_dir = DOWN
                        elif event.key == pygame.K_LEFT and self.s2_dir != RIGHT:
                            self.s2_next_dir = LEFT
                        elif event.key == pygame.K_RIGHT and self.s2_dir != LEFT:
                            self.s2_next_dir = RIGHT

                    if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                        self.fps = min(60, self.fps + 2)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.fps = max(3, self.fps - 2)

            self.step()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ObstacleSnakeDuelGame()
    game.run()
