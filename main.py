import asyncio
import pygame.freetype
import sys
import os
import platform

# Initialize pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5

# Enemy settings
enemy_size = 50
enemy_speed = 3
enemies = []

# Score
score = 0
pygame.freetype.init()
font = pygame.freetype.SysFont(None, 36)

# Debug flag to help with development
DEBUG = os.environ.get('PYGBAG_DEBUG', '0') == '1'

# Detect if we're running in browser or locally
RUNNING_IN_BROWSER = platform.system() == 'Emscripten'

# Game state
GAME_STATE_START_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
game_state = GAME_STATE_START_MENU

def print_debug(message):
    """Print debug messages if debug mode is on"""
    if DEBUG:
        print(f"[DEBUG] {message}")

# Button class to create interactive buttons
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)  # Button border
        
        # Draw text
        text_rect = font.get_rect(self.text)
        font.render_to(screen, 
                     (self.rect.centerx - text_rect.width//2, 
                      self.rect.centery - text_rect.height//2), 
                     self.text, WHITE)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

async def main():
    print_debug("Game starting...")
    
    # Create the screen with appropriate flags
    flags = pygame.SRCALPHA
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Online Pygame Demo")
    clock = pygame.time.Clock()
    
    # Create start button
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50, "START GAME", BLUE, GREEN)
    restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "RESTART", BLUE, GREEN)
    
    # Game variables
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 2 * player_size
    enemies = []
    score = 0
    spawn_timer = 0
    
    # Main game loop
    running = True
    game_state = GAME_STATE_START_MENU
    
    # For Pygbag web version - this indicates the game has loaded
    print("PYGAME RUNNING")
    
    print_debug(f"Running in browser: {RUNNING_IN_BROWSER}")
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and game_state == GAME_STATE_GAME_OVER:
                    # Reset the game
                    player_x = WIDTH // 2 - player_size // 2
                    player_y = HEIGHT - 2 * player_size
                    enemies = []
                    score = 0
                    game_state = GAME_STATE_PLAYING
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GAME_STATE_START_MENU and start_button.is_hovered(mouse_pos):
                    game_state = GAME_STATE_PLAYING
                    print_debug("Game started!")
                elif game_state == GAME_STATE_GAME_OVER and restart_button.is_hovered(mouse_pos):
                    # Reset the game
                    player_x = WIDTH // 2 - player_size // 2
                    player_y = HEIGHT - 2 * player_size
                    enemies = []
                    score = 0
                    game_state = GAME_STATE_PLAYING
        
        # Clear screen first
        screen.fill(BLACK)
        
        if game_state == GAME_STATE_START_MENU:
            # Draw title
            title_text = "DODGE THE BLOCKS"
            title_rect = font.get_rect(title_text)
            font.render_to(screen, (WIDTH//2 - title_rect.width//2, HEIGHT//4), 
                        title_text, WHITE)
            
            # Draw instructions
            inst_text = "Use LEFT/RIGHT arrows to move"
            inst_rect = font.get_rect(inst_text)
            font.render_to(screen, (WIDTH//2 - inst_rect.width//2, HEIGHT//4 + 50), 
                        inst_text, WHITE)
            
            # Draw click instruction for clarity
            click_text = "Click the button below to start"
            click_rect = font.get_rect(click_text)
            font.render_to(screen, (WIDTH//2 - click_rect.width//2, HEIGHT//4 + 100), 
                        click_text, WHITE)
            
            # Update and draw start button
            start_button.update(mouse_pos)
            start_button.draw(screen)
            
        elif game_state == GAME_STATE_PLAYING:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
                player_x += player_speed
            
            # Spawn enemies
            spawn_timer += 1
            if spawn_timer >= FPS:
                import random
                enemy_x = random.randint(0, WIDTH - enemy_size)
                enemy_y = -enemy_size
                enemies.append([enemy_x, enemy_y])
                spawn_timer = 0
            
            # Move enemies
            for enemy in enemies[:]:
                enemy[1] += enemy_speed
                if enemy[1] > HEIGHT:
                    enemies.remove(enemy)
                    score += 1
                
                # Check for collision with player
                if (player_x < enemy[0] + enemy_size and
                    player_x + player_size > enemy[0] and
                    player_y < enemy[1] + enemy_size and
                    player_y + player_size > enemy[1]):
                    game_state = GAME_STATE_GAME_OVER
            
            # Draw player
            pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))
            
            # Draw enemies
            for enemy in enemies:
                pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
            
        elif game_state == GAME_STATE_GAME_OVER:
            # Draw game over message
            game_over_text = "GAME OVER!"
            game_over_rect = font.get_rect(game_over_text)
            font.render_to(screen, (WIDTH//2 - game_over_rect.width//2, HEIGHT//3), 
                         game_over_text, RED)
            
            # Draw final score
            final_score_text = f"Final Score: {score}"
            final_score_rect = font.get_rect(final_score_text)
            font.render_to(screen, (WIDTH//2 - final_score_rect.width//2, HEIGHT//3 + 50), 
                         final_score_text, WHITE)
            
            # Draw instruction to restart
            space_text = "Press SPACE or click button to restart"
            space_rect = font.get_rect(space_text)
            font.render_to(screen, (WIDTH//2 - space_rect.width//2, HEIGHT//3 + 90), 
                         space_text, WHITE)
            
            # Update and draw restart button
            restart_button.update(mouse_pos)
            restart_button.draw(screen)
            
        # Always draw score if playing or game over
        if game_state != GAME_STATE_START_MENU:
            font.render_to(screen, (10, 10), f"Score: {score}", WHITE)
        
        # Draw debug info if enabled
        if DEBUG:
            font.render_to(screen, (WIDTH - 150, 10), "DEBUG MODE", BLUE)
            font.render_to(screen, (WIDTH - 150, 40), f"FPS: {int(clock.get_fps())}", GREEN)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
        
        # Allow other tasks to run (required for asyncio)
        await asyncio.sleep(0)
    
    print_debug("Game exiting...")
    pygame.quit()
    sys.exit()

# This setup works for both normal pygame and for pygbag
if __name__ == "__main__":
    print_debug("Starting game...")
    asyncio.run(main())