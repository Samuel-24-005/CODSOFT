import pygame
import random
import os

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# ---------------- ANIMATION ----------------
anim_scale = 0
anim_speed = 5
animating = False

# ---------------- COUNTDOWN ----------------
counting = False
count_steps = ["1", "2", "3", "SHOOT!"]
count_index = 0
count_text = ""
last_update = 0
count_delay = 500

# ---------------- SCORE SYSTEM ----------------
def load_score():
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as f:
            data = f.read().split(",")
            return int(data[0]), int(data[1]), int(data[2])
    return 0, 0, 0

def save_score(w, l, d):
    with open("score.txt", "w") as f:
        f.write(f"{w},{l},{d}")

wins, losses, draws = load_score()

# ---------------- LOAD IMAGES ----------------
def load_image(name):
    img = pygame.image.load(f"assets/{name}")
    return pygame.transform.scale(img, (120, 120))

rock = load_image("rock.png")
paper = load_image("paper.png")
scissors = load_image("scissor.png")

images = {
    "rock": rock,
    "paper": paper,
    "scissors": scissors
}

choices = ["rock", "paper", "scissors"]

# ---------------- GAME STATE ----------------
user_choice = None
comp_choice = None
result = ""

font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)

# ---------------- GAME LOOP ----------------
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((10, 15, 30))

    # -------- INPUT --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                user_choice = "rock"
            elif event.key == pygame.K_p:
                user_choice = "paper"
            elif event.key == pygame.K_s:
                user_choice = "scissors"
            elif event.key == pygame.K_SPACE:
                # RESET GAME
                user_choice = None
                comp_choice = None
                result = ""
                anim_scale = 0
                animating = False
                counting = False
                count_index = 0
                count_text = ""
                wins, losses, draws = 0, 0, 0
                save_score(wins, losses, draws)

            if user_choice:
                comp_choice = random.choice(choices)

                counting = True
                count_index = 0
                count_text = count_steps[count_index]
                last_update = pygame.time.get_ticks()

                animating = False
                anim_scale = 0
                result = ""

    # -------- COUNTDOWN --------
    if counting:
        now = pygame.time.get_ticks()

        if now - last_update > count_delay:
            count_index += 1
            last_update = now

            if count_index < len(count_steps):
                count_text = count_steps[count_index]
            else:
                counting = False
                animating = True
                anim_scale = 0

                # RESULT LOGIC
                if user_choice == comp_choice:
                    result = "Draw!"
                    draws += 1
                elif (user_choice == "rock" and comp_choice == "scissors") or \
                     (user_choice == "scissors" and comp_choice == "paper") or \
                     (user_choice == "paper" and comp_choice == "rock"):
                    result = "You Win!"
                    wins += 1
                else:
                    result = "Computer Wins!"
                    losses += 1

                save_score(wins, losses, draws)

    # -------- ANIMATION --------
    if animating:
        anim_scale += anim_speed
        if anim_scale >= 120:
            anim_scale = 120
            animating = False

    # -------- DRAW --------
    title = font.render("Press R (Rock) / P (Paper) / S (Scissors)", True, (255,255,255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    play_again = small_font.render("Press SPACE to Play Again", True, (200,200,200))
    screen.blit(play_again, (WIDTH//2 - play_again.get_width()//2, 70))

    # Labels
    user_label = small_font.render("You", True, (255,255,255))
    comp_label = small_font.render("Computer", True, (255,255,255))
    screen.blit(user_label, (140, 170))
    screen.blit(comp_label, (380, 170))

    # Countdown
    if counting:
        text = font.render(count_text, True, (255,255,255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

    # Images
    if not counting and user_choice and comp_choice and anim_scale > 0:
        user_img = pygame.transform.scale(images[user_choice], (anim_scale, anim_scale))
        comp_img = pygame.transform.scale(images[comp_choice], (anim_scale, anim_scale))

        screen.blit(user_img, (120, 200))
        screen.blit(comp_img, (360, 200))

    # Result with colors
    if result:
        if result == "You Win!":
            color = (0, 255, 0)
        elif result == "Computer Wins!":
            color = (255, 0, 0)
        else:
            color = (255, 255, 0)

        result_text = font.render(result, True, color)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT - 80))

    # Scoreboard
    score_text = small_font.render(f"W: {wins}  L: {losses}  D: {draws}", True, (200,200,200))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT - 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()