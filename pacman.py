import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
TILE_SIZE = 30
COLS = 19
ROWS = 21
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + 50

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
SCARED_BLUE = (33, 33, 222)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Original level map
ORIGINAL_LEVEL = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

level = [row[:] for row in ORIGINAL_LEVEL]

class Pacman:
    def __init__(self):
        self.grid_x = 9
        self.grid_y = 15
        self.pixel_x = float(self.grid_x * TILE_SIZE)
        self.pixel_y = float(self.grid_y * TILE_SIZE)
        self.direction = 0
        self.next_direction = 0
        self.speed = 3
        self.mouth_angle = 0
        self.mouth_dir = 1
        self.powered = False
        self.power_timer = 0
        self.moving = False
        
    def get_direction_delta(self, direction):
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return deltas[direction]
        
    def can_move_to(self, grid_x, grid_y):
        if grid_x < 0 or grid_x >= COLS:
            return True
        if grid_y < 0 or grid_y >= ROWS:
            return False
        return level[grid_y][grid_x] != 1
    
    def update(self):
        aligned_x = abs(self.pixel_x - round(self.pixel_x / TILE_SIZE) * TILE_SIZE) < self.speed
        aligned_y = abs(self.pixel_y - round(self.pixel_y / TILE_SIZE) * TILE_SIZE) < self.speed
        
        if aligned_x and aligned_y:
            self.pixel_x = round(self.pixel_x / TILE_SIZE) * TILE_SIZE
            self.pixel_y = round(self.pixel_y / TILE_SIZE) * TILE_SIZE
            self.grid_x = int(self.pixel_x // TILE_SIZE)
            self.grid_y = int(self.pixel_y // TILE_SIZE)
            
            if self.grid_x < 0:
                self.grid_x = COLS - 1
                self.pixel_x = float(self.grid_x * TILE_SIZE)
            elif self.grid_x >= COLS:
                self.grid_x = 0
                self.pixel_x = 0.0
            
            dx, dy = self.get_direction_delta(self.next_direction)
            if self.can_move_to(self.grid_x + dx, self.grid_y + dy):
                self.direction = self.next_direction
            
            dx, dy = self.get_direction_delta(self.direction)
            if self.can_move_to(self.grid_x + dx, self.grid_y + dy):
                self.moving = True
            else:
                self.moving = False
        
        if self.moving:
            dx, dy = self.get_direction_delta(self.direction)
            self.pixel_x += dx * self.speed
            self.pixel_y += dy * self.speed
            
            if self.pixel_x < -TILE_SIZE:
                self.pixel_x = float((COLS - 1) * TILE_SIZE)
            elif self.pixel_x >= COLS * TILE_SIZE:
                self.pixel_x = 0.0
        
        self.mouth_angle += self.mouth_dir * 4
        if self.mouth_angle >= 45:
            self.mouth_dir = -1
        elif self.mouth_angle <= 5:
            self.mouth_dir = 1
            
        if self.powered:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.powered = False
                
    def draw(self):
        center_x = int(self.pixel_x + TILE_SIZE // 2)
        center_y = int(self.pixel_y + TILE_SIZE // 2 + 50)
        
        angles = [0, 270, 180, 90]
        base_angle = angles[self.direction]
        
        start_angle = base_angle + self.mouth_angle
        end_angle = base_angle + 360 - self.mouth_angle
        
        points = [(center_x, center_y)]
        for angle in range(int(start_angle), int(end_angle) + 1, 10):
            rad = math.radians(angle)
            x = center_x + 13 * math.cos(rad)
            y = center_y - 13 * math.sin(rad)
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, YELLOW, points)
            
    def reset(self):
        self.grid_x = 9
        self.grid_y = 15
        self.pixel_x = float(self.grid_x * TILE_SIZE)
        self.pixel_y = float(self.grid_y * TILE_SIZE)
        self.direction = 0
        self.next_direction = 0
        self.moving = False
        self.powered = False
        self.power_timer = 0

class Ghost:
    def __init__(self, grid_x, grid_y, color, scatter_target, delay):
        self.start_x = grid_x
        self.start_y = grid_y
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = float(grid_x * TILE_SIZE)
        self.pixel_y = float(grid_y * TILE_SIZE)
        self.color = color
        self.direction = 3
        self.speed = 2.5
        self.scared = False
        self.scatter_target = scatter_target
        self.mode = "chase"
        self.mode_timer = 0
        self.delay = delay
        self.original_delay = delay
        self.active = delay == 0
        self.blink = False
        self.blink_timer = 0
        
    def get_direction_delta(self, direction):
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return deltas[direction]
        
    def can_move_to(self, grid_x, grid_y):
        if grid_x < 0 or grid_x >= COLS:
            return True
        if grid_y < 0 or grid_y >= ROWS:
            return False
        return level[grid_y][grid_x] != 1
    
    def get_available_directions(self):
        available = []
        opposite = (self.direction + 2) % 4
        
        for d in range(4):
            if d == opposite:
                continue
            dx, dy = self.get_direction_delta(d)
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            if new_x < 0:
                new_x = COLS - 1
            elif new_x >= COLS:
                new_x = 0
                
            if self.can_move_to(new_x, new_y):
                available.append(d)
                
        if not available:
            available.append(opposite)
            
        return available
    
    def choose_direction(self, pacman):
        available = self.get_available_directions()
        if not available:
            return
            
        if self.scared:
            self.direction = random.choice(available)
            return
            
        if self.mode == "scatter":
            target = self.scatter_target
        else:
            target = (pacman.grid_x, pacman.grid_y)
        
        best_dir = available[0]
        best_dist = float('inf')
        
        for d in available:
            dx, dy = self.get_direction_delta(d)
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            dist = (new_x - target[0]) ** 2 + (new_y - target[1]) ** 2
            if dist < best_dist:
                best_dist = dist
                best_dir = d
                
        self.direction = best_dir
        
    def update(self, pacman):
        if not self.active:
            self.delay -= 1
            if self.delay <= 0:
                self.active = True
            return
            
        self.mode_timer += 1
        if self.mode_timer > 420:
            self.mode = "chase" if self.mode == "scatter" else "scatter"
            self.mode_timer = 0
            
        aligned_x = abs(self.pixel_x - round(self.pixel_x / TILE_SIZE) * TILE_SIZE) < self.speed
        aligned_y = abs(self.pixel_y - round(self.pixel_y / TILE_SIZE) * TILE_SIZE) < self.speed
        
        if aligned_x and aligned_y:
            self.pixel_x = round(self.pixel_x / TILE_SIZE) * TILE_SIZE
            self.pixel_y = round(self.pixel_y / TILE_SIZE) * TILE_SIZE
            self.grid_x = int(self.pixel_x // TILE_SIZE)
            self.grid_y = int(self.pixel_y // TILE_SIZE)
            
            if self.grid_x < 0:
                self.grid_x = COLS - 1
                self.pixel_x = float(self.grid_x * TILE_SIZE)
            elif self.grid_x >= COLS:
                self.grid_x = 0
                self.pixel_x = 0.0
            
            self.choose_direction(pacman)
        
        speed = self.speed * 0.5 if self.scared else self.speed
        dx, dy = self.get_direction_delta(self.direction)
        self.pixel_x += dx * speed
        self.pixel_y += dy * speed
        
        if self.pixel_x < -TILE_SIZE:
            self.pixel_x = float((COLS - 1) * TILE_SIZE)
        elif self.pixel_x >= COLS * TILE_SIZE:
            self.pixel_x = 0.0
            
        if self.scared and pacman.power_timer < 120:
            self.blink_timer += 1
            if self.blink_timer > 8:
                self.blink = not self.blink
                self.blink_timer = 0
        else:
            self.blink = False
                
    def draw(self):
        if not self.active:
            return
            
        center_x = int(self.pixel_x + TILE_SIZE // 2)
        center_y = int(self.pixel_y + TILE_SIZE // 2 + 50)
        
        if self.scared:
            color = WHITE if self.blink else SCARED_BLUE
        else:
            color = self.color
            
        pygame.draw.circle(screen, color, (center_x, center_y - 3), 13)
        pygame.draw.rect(screen, color, (center_x - 13, center_y - 3, 26, 13))
        
        wave_y = center_y + 10
        for i in range(4):
            wx = center_x - 10 + i * 7
            pygame.draw.circle(screen, color, (wx, wave_y), 4)
            
        if not self.scared:
            pygame.draw.circle(screen, WHITE, (center_x - 5, center_y - 5), 5)
            pygame.draw.circle(screen, WHITE, (center_x + 5, center_y - 5), 5)
            
            dx, dy = self.get_direction_delta(self.direction)
            pygame.draw.circle(screen, BLUE, (center_x - 5 + dx * 2, center_y - 5 + dy * 2), 2)
            pygame.draw.circle(screen, BLUE, (center_x + 5 + dx * 2, center_y - 5 + dy * 2), 2)
        else:
            pygame.draw.circle(screen, WHITE, (center_x - 4, center_y - 4), 3)
            pygame.draw.circle(screen, WHITE, (center_x + 4, center_y - 4), 3)
            for i in range(4):
                y_off = 2 if i % 2 == 0 else -2
                pygame.draw.line(screen, WHITE, 
                               (center_x - 6 + i * 4, center_y + 4 + y_off), 
                               (center_x - 2 + i * 4, center_y + 4 - y_off), 2)
            
    def reset(self):
        self.grid_x = self.start_x
        self.grid_y = self.start_y
        self.pixel_x = float(self.grid_x * TILE_SIZE)
        self.pixel_y = float(self.grid_y * TILE_SIZE)
        self.direction = 3
        self.scared = False
        self.mode = "chase"
        self.mode_timer = 0
        self.delay = self.original_delay
        self.active = self.delay == 0
        self.blink = False

def draw_level():
    for y in range(ROWS):
        for x in range(COLS):
            tile = level[y][x]
            px = x * TILE_SIZE
            py = y * TILE_SIZE + 50
            
            if tile == 1:
                pygame.draw.rect(screen, BLUE, (px, py, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, DARK_BLUE, (px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4))
            elif tile == 2:
                pygame.draw.circle(screen, WHITE, (px + TILE_SIZE // 2, py + TILE_SIZE // 2), 3)
            elif tile == 3:
                size = 6 + int(2 * abs((pygame.time.get_ticks() % 500) - 250) / 250)
                pygame.draw.circle(screen, WHITE, (px + TILE_SIZE // 2, py + TILE_SIZE // 2), size)

def check_collision(pacman, ghosts):
    px = pacman.pixel_x + TILE_SIZE // 2
    py = pacman.pixel_y + TILE_SIZE // 2
    
    for ghost in ghosts:
        if not ghost.active:
            continue
            
        gx = ghost.pixel_x + TILE_SIZE // 2
        gy = ghost.pixel_y + TILE_SIZE // 2
        
        dist = math.sqrt((px - gx) ** 2 + (py - gy) ** 2)
        
        if dist < TILE_SIZE * 0.7:
            if pacman.powered and ghost.scared:
                ghost.reset()
                ghost.delay = 180
                ghost.active = False
                return 200
            elif not ghost.scared:
                return -1
    return 0

def check_pellet(pacman):
    grid_x = int(round(pacman.pixel_x / TILE_SIZE))
    grid_y = int(round(pacman.pixel_y / TILE_SIZE))
    
    if abs(pacman.pixel_x - grid_x * TILE_SIZE) > 8:
        return 0
    if abs(pacman.pixel_y - grid_y * TILE_SIZE) > 8:
        return 0
    
    if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
        if level[grid_y][grid_x] == 2:
            level[grid_y][grid_x] = 0
            return 10
        elif level[grid_y][grid_x] == 3:
            level[grid_y][grid_x] = 0
            pacman.powered = True
            pacman.power_timer = 480
            return 50
    return 0

def count_pellets():
    count = 0
    for row in level:
        for tile in row:
            if tile in (2, 3):
                count += 1
    return count

def reset_level():
    global level
    level = [row[:] for row in ORIGINAL_LEVEL]

def draw_ui(score, lives, high_score):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 15))
    
    high_text = small_font.render(f"High Score: {high_score}", True, YELLOW)
    screen.blit(high_text, (WIDTH // 2 - 50, 18))
    
    for i in range(lives):
        cx = WIDTH - 25 - i * 28
        pygame.draw.circle(screen, YELLOW, (cx, 25), 10)
        pygame.draw.polygon(screen, BLACK, [(cx, 25), (cx + 10, 22), (cx + 10, 28)])

def main():
    global level
    
    pacman = Pacman()
    
    ghosts = [
        Ghost(9, 7, RED, (COLS - 2, 0), 0),
        Ghost(8, 9, PINK, (2, 0), 90),
        Ghost(10, 9, CYAN, (COLS - 1, ROWS - 1), 180),
        Ghost(9, 9, ORANGE, (0, ROWS - 1), 270),
    ]
    
    score = 0
    high_score = 0
    lives = 3
    game_over = False
    won = False
    paused = False
    start_delay = 90
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pacman.next_direction = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pacman.next_direction = 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pacman.next_direction = 2
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    pacman.next_direction = 3
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    reset_level()
                    pacman = Pacman()
                    ghosts = [
                        Ghost(9, 7, RED, (COLS - 2, 0), 0),
                        Ghost(8, 9, PINK, (2, 0), 90),
                        Ghost(10, 9, CYAN, (COLS - 1, ROWS - 1), 180),
                        Ghost(9, 9, ORANGE, (0, ROWS - 1), 270),
                    ]
                    if score > high_score:
                        high_score = score
                    score = 0
                    lives = 3
                    game_over = False
                    won = False
                    start_delay = 90
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill(BLACK)
        draw_level()
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
        draw_ui(score, lives, high_score)
        
        if start_delay > 0:
            start_delay -= 1
            ready_text = font.render("GET READY!", True, YELLOW)
            screen.blit(ready_text, (WIDTH // 2 - 60, HEIGHT // 2))
            pygame.display.flip()
            clock.tick(60)
            continue
                    
        if not game_over and not won and not paused:
            pacman.update()
            
            for ghost in ghosts:
                ghost.scared = pacman.powered
                ghost.update(pacman)
                
            pellet_score = check_pellet(pacman)
            score += pellet_score
            
            collision = check_collision(pacman, ghosts)
            if collision == -1:
                lives -= 1
                if lives <= 0:
                    game_over = True
                    if score > high_score:
                        high_score = score
                else:
                    pacman.reset()
                    for ghost in ghosts:
                        ghost.reset()
                    start_delay = 60
            elif collision > 0:
                score += collision
                
            if count_pellets() == 0:
                won = True
                if score > high_score:
                    high_score = score
        
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT - 50))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 50))
            pause_text = font.render("PAUSED", True, YELLOW)
            hint_text = small_font.render("Resume: P | Restart: R", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
            screen.blit(hint_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
            
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT - 50))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 50))
            
            game_over_text = font.render("GAME OVER!", True, RED)
            score_text = font.render(f"Score: {score}", True, WHITE)
            restart_text = small_font.render("Restart: R | Quit: ESC", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 40))
            screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - 90, HEIGHT // 2 + 40))
            
        elif won:
            overlay = pygame.Surface((WIDTH, HEIGHT - 50))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 50))
            
            won_text = font.render("YOU WIN!", True, YELLOW)
            score_text = font.render(f"Score: {score}", True, WHITE)
            restart_text = small_font.render("Restart: R | Quit: ESC", True, WHITE)
            
            screen.blit(won_text, (WIDTH // 2 - 55, HEIGHT // 2 - 40))
            screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - 90, HEIGHT // 2 + 40))
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()