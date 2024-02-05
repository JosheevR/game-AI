import pygame
import module

# Global variables
BACKGROUND_COLOR = (200, 200, 200)
SCREEN_SIZE = [1280,720]
MAX_FRUITS = 5
INIT_PITS = 4
FRUIT = True
PIT = False

# Game State
state = [True, False, False]

# Leaderboard
high_score = 0
high_time = 0

# Initialize game
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
ending = pygame.font.Font(None, 50)
score = 0
prevscore = -1
start_time = 0

# Run until the user asks to quit
running = True
while running:
    
    # Framerate = 60fps
    clock.tick(60)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill(BACKGROUND_COLOR)
    
    key = pygame.key.get_pressed()

    if state[0] == True:
        # Press Enter to Begin Game
        if key[pygame.K_RETURN] and not return_key_pressed:
            state[0] = False
            state[1] = True
            return_key_pressed = True
            player_rect = module.createNewPlayer(SCREEN_SIZE)
            
            # Initialize Game Attributes
            score = 0
            current_time = 0
            fruit_size = 10
            pit_size = 50
            fruits = []
            pits = []
            start_time = pygame.time.get_ticks()
            current_run_start_time = pygame.time.get_ticks()
            current_time = 0

            for i in range(MAX_FRUITS):
                module.add_new_rect(SCREEN_SIZE, fruit_size, fruits, pit_size, pits, player_rect, FRUIT)
            for i in range(INIT_PITS):
                module.add_new_rect(SCREEN_SIZE, fruit_size, fruits, pit_size, pits, player_rect, PIT)
            
            num_fruits = len(fruits)
            num_pits = len(pits)

        elif not key[pygame.K_RETURN]:
            return_key_pressed = False

        text = "Welcome! Press Enter to Start"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        screen.blit(text_surface, text_rect)


    elif state[1] == True:

        # Keep track of score on screen
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        total_time = pygame.time.get_ticks() - start_time
        total_seconds = total_time // 1000
        total_minutes = total_seconds // 60

        remaining_seconds = total_seconds % 60
        remaining_minutes = total_minutes % 60

        # Display the timer in the top right corner
        timer_text = font.render(f'Time: {remaining_minutes:02d}:{remaining_seconds:02d}', True, (0, 0, 0))
        screen.blit(timer_text, (SCREEN_SIZE[0] - 150, 10))

        if score % 10 == 0 and prevscore % 10 != 0:
            module.add_new_rect(SCREEN_SIZE, fruit_size, fruits, pit_size, pits, player_rect, PIT)

        prevscore = score

        # Draw pits
        for deadly_rect in pits:
            pygame.draw.rect(screen, (90, 15, 20), deadly_rect)

        # Draw fruits
        for fruit_rect in fruits:
            pygame.draw.rect(screen, (150, 150, 150), fruit_rect)

        # Player rectangle
        pygame.draw.rect(screen, (0, 0, 0), player_rect)
        module.moveRect(key, player_rect)

        for fruit_rect in fruits:
            if player_rect.colliderect(fruit_rect):
                fruits.remove(fruit_rect)
                module.add_new_rect(SCREEN_SIZE, fruit_size, fruits, pit_size, pits, player_rect, FRUIT)
                score += 1

        state = module.checkWallCollision(player_rect, SCREEN_SIZE, state)

        for deadly_rect in pits:
            if player_rect.colliderect(deadly_rect):
                state[1] = False
                state[2] = True

        current_time = total_time + 0
        high_score, high_time = module.checkHighScore(high_score, high_time, score, total_time)

    elif state[2] == True:
        # Press Enter to Restart Game
        if key[pygame.K_RETURN] and not return_key_pressed:
            state[2] = False
            state[0] = True
            return_key_pressed = True
        elif not key[pygame.K_RETURN]:
            return_key_pressed = False
        
        text = "Game Over"
        text_surface = ending.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - 100)
        screen.blit(text_surface, text_rect)

        # Keep track of score on screen
        score_text = font.render(f'High Score: {high_score}', True, (0, 0, 0))

        total_time = high_time
        total_seconds = total_time // 1000
        total_minutes = total_seconds // 60

        remaining_seconds = total_seconds % 60
        remaining_minutes = total_minutes % 60

        high_score_text = font.render(f'High Score: {high_score}         Time: {remaining_minutes:02d}:{remaining_seconds:02d}', True, (0, 0, 0))
        screen.blit(high_score_text, (SCREEN_SIZE[0]/2 - 175, SCREEN_SIZE[1]/2))

        # Calculate current attempt time
        current_attempt_time = current_time

        # Calculate minutes and seconds for the current attempt time
        current_minutes = (current_attempt_time // 1000) // 60
        current_seconds = (current_attempt_time // 1000) % 60

        # Display the timer for the current attempt on the end screen
        current_score_text = font.render(f'Current Score: {score}         Time: {current_minutes:02d}:{current_seconds:02d}', True, (90, 15, 20))
        screen.blit(current_score_text, (SCREEN_SIZE[0]/2 - 210, SCREEN_SIZE[1]/2 + 50))
    

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
