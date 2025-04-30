import asyncio
import pygame.freetype
import sys

# Initialize pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

async def main():
    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Online Pygame Demo")
    clock = pygame.time.Clock()
    
    # Game variables
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 2 * player_size
    enemies = []
    score = 0
    game_over = False
    spawn_timer = 0
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset the game
                    player_x = WIDTH // 2 - player_size // 2
                    player_y = HEIGHT - 2 * player_size
                    enemies = []
                    score = 0
                    game_over = False
        
        if not game_over:
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
                    game_over = True
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw player
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))
        
        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
        
        # Draw score
        font.render_to(screen, (10, 10), f"Score: {score}", WHITE)
        
        # Draw game over screen
        if game_over:
            text = "Game Over! Press SPACE to restart"
            text_rect = font.get_rect(text)
            font.render_to(screen, (WIDTH//2 - text_rect.width//2, HEIGHT//2 - text_rect.height//2), 
                           text, WHITE)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
        
        # Allow other tasks to run (required for asyncio)
        await asyncio.sleep(0)
    
    pygame.quit()
    sys.exit()

# This setup works for both normal pygame and for pygbag
if __name__ == "__main__":
    asyncio.run(main())