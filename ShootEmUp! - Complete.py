# AHMAD KAMAL ABDUL HAFIZ
# STUDENT ID: 3933564
# Software Engineering Coursework 1
# ShootEmUp!

# Below are Python modules used in this program.
# These modules are built into python.
from tkinter import *  # Used to make the GUI window.
import pygame  # Used to make the game.
import random  # Used to help build some functions within the game.
import sys  # Minimal use, used to exit the program.
import os  # Minimal use, used to access the Operating System (OS) functions.
from os import path  # Used to access files.

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Pygame window spawns at the center of the screen.

# Surf - The surface we want the text drawn on.
# Text - What we want to display.
# Size - Size of text.
# xText, yText - The location on screen where text will be displayed.
def displayText(surf, text, size, xText, yText):
    WHITE = (255, 255, 255)  # RGB code colour for white. Stored in a constant.

    fontDIR = path.join(path.dirname(__file__), "FONT")  # Font directory on computer.

    font = pygame.font.Font(os.path.join(fontDIR, 'ARCADE_N.TTF'), size - 10)

    textSurface = font.render(text, True, WHITE)
    textRect = textSurface.get_rect()
    textRect.midtop = (xText, yText)
    surf.blit(textSurface, textRect)


# Function below if called if the "1 Player" button is pressed in the GUI window.
def onePlayer():
    root.withdraw()  # Hides Tkinter window.

    imageDir = path.join(path.dirname(__file__), "IMAGES")  # Directory for images used within the program.
    soundDir = path.join(path.dirname(__file__), "SOUND")  # Directory for sound used within the program.

    WIDTH = 600  # Width of pygame window.
    HEIGHT = 925  # Height of pygame window.
    FPS = 60  # Frames per second. Stored in a constant. How many times per second the loop should happen. The game loop.

    BLACK = (0, 0, 0)  # RGB code colour for black. Stored in a constant.

    pygame.init()  # Initialise pygame. Required to start.
    pygame.mixer.init()  # Enables the use of sound in pygame.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates pygame window screen.
    pygame.display.set_caption("ShootEmUp!")  # Name of displayed pygame window.
    Icon = pygame.image.load("IMAGES/Icon.png")  # Icon loaded from images folder.
    pygame.display.set_icon(Icon)  # Displays icon on pygame window. Top left, left of pygame window name.

    clock = pygame.time.Clock()  # Used later on to make sure game runs on FPS.

    # Function below displays the lives on the screen on the top left.
    def displayLives(surf, xLife, yLife, lives, heartImg):
        for life in range(lives):  # Loops for the amount of lives.
            imgRect = heartImg.get_rect()
            imgRect.x = xLife + 50 * life  # Makes a gap between each heart.
            imgRect.y = yLife  # Draw all hearts on the same line.
            surf.blit(heartImg, imgRect)  # Display the lives onto the screen.

    # Class below allows us to toggle the background music.
    class ToggleMusic(object):  # Defines a new class.
        def __init__(self):  # Defines what code will run whenever a new instance of this class is created.
            self.paused = pygame.mixer.music.get_busy()  # Checks if music is playing or not.

        def toggle(self):  # Function is used whenever the "M" button is pressed when the game is being played.
            if self.paused:  # If music is not playing.
                pygame.mixer.music.unpause()  # Unpause music.
            if not self.paused:  # If music is playing.
                pygame.mixer.music.pause()  # Pause music.
            self.paused = not self.paused

    class Ship(pygame.sprite.Sprite):  # Class creates the ship the  user will interact with, whilst playing the game.
        def __init__(self):  # Defines what code will run whenever a new instance of this class is created.
            pygame.sprite.Sprite.__init__(self)  # Required by pygame.
            self.image = pygame.transform.scale(shipImg, (99, 75))  # Load the ship image and alter the size of it.
            self.image.set_colorkey(BLACK)  # Remove black entities on the loaded ship image.
            self.rect = self.image.get_rect()  # Get object rectangle.
            self.radius = 25  # Hit box for the ship.
            self.rect.centerx = WIDTH / 2  # Places sprite center of the screen, in terms of width.
            self.rect.bottom = HEIGHT - 10  # Places sprite (0,915) on the screen.
            self.speedx = 0  # Keeps track of how fast the player is moving in the x direction.
            self.speedy = 0  # Keeps track of how fast the player is moving in the y direction.
            self.lives = 3  # Set lives.
            self.shootDelay = 200  # How long in milliseconds before next bullet can be shot.
            self.lastShot = pygame.time.get_ticks()  # Keeps track of last bullet being shot.

        def update(self):
            self.speedx = 0  # Sets speedx to 0 for every frame.
            self.speedy = 0  # Sets speedy to 0 for every frame.
            keyState = pygame.key.get_pressed()  # Stores the key that is pressed.
            if keyState[pygame.K_LEFT]:  # If left arrow pressed.
                self.speedx = -8  # Move 8 pixels left.
            if keyState[pygame.K_RIGHT]:  # If right arrow pressed.
                self.speedx = 8  # Move 8 pixels right.
            if keyState[pygame.K_UP]:  # If up arrow pressed.
                self.speedy = -8  # Move 8 pixels up.
            if keyState[pygame.K_DOWN]:  # If down arrow pressed.
                self.speedy = 8  # Move 8 pixels down.
            if keyState[pygame.K_SPACE]:  # If the user presses space.
                self.shoot()  # runs ship shoot() method.

            self.rect.x = self.rect.x + self.speedx  # Allows the ship to move along the x axis.
            self.rect.y = self.rect.y + self.speedy  # Allows the ship to move along the y axis.

            # Ensures the user stays within the screen and does not get off.
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

        # Function below is used whenever the space button is is pressed or held down. A new bullet will spawn from the ship.
        def shoot(self):
            n = pygame.time.get_ticks()  # Get time.
            if n - self.lastShot > self.shootDelay:  # Checks on how much time passed since last bullet was shot.
                self.lastShot = n  # Updates last shot.
                bullet = Bullet(self.rect.centerx, self.rect.top)
                allSprites.add(bullet)  # Add bullet to allSprites group.
                bullets.add(bullet)  # Add bullets to the bullets group.
                shootSound.play()  # Play pew sound when a bullet is shot.

    # Class below creates the alien(s) within the game.
    class Alien(pygame.sprite.Sprite):  # Defines a new class.
        def __init__(self):  # Defines what code will run whenever a new instance of this class is created.
            pygame.sprite.Sprite.__init__(self)  # Required by pygame.
            self.image = random.choice(alienImg)  # Load a random image from the list.
            self.image.set_colorkey(BLACK)  # Remove black entities of the loaded image.
            self.rect = self.image.get_rect()  # Get object rectangle.
            self.radius = int(self.rect.width / 2)  # Hit box for the alien.
            self.rect.x = random.randrange(WIDTH - self.rect.width)  # Alien spawns off screen at an angle.
            self.rect.y = random.randrange(-100, -40)  # Aliens spawns off screen.
            self.speedy = random.randrange(1, 8)  # Alien moves down the screen at varying speeds from, 1 pixel to 8.
            self.speedx = random.randrange(-3, 3)  # Alien moves at angle at varying speeds.

        # Function below respawns the alien to the top off the screen, if it goes off screen.
        def update(self):
            self.rect.x = self.rect.x + self.speedx  # Allows the alien to move along the x axis.
            self.rect.y = self.rect.y + self.speedy  # Allows the alien to move along the y axis.
            # Moves the sprite back to a random position above.
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

    # Class below creates the bullet(s) within the game.
    class Bullet(pygame.sprite.Sprite):  # Defines a new class.
        def __init__(self, xBullet, yBullet):  # xBullet and yBullet ensures that bullet is set to where the player is.
            pygame.sprite.Sprite.__init__(self)  # Required by pygame.
            self.image = pygame.transform.scale(bulletImg, (9, 54))  # Load the bullet image and alter the size of it.
            self.image.set_colorkey(BLACK)  # Remove black entities of the loaded image.
            self.rect = self.image.get_rect()  # Get object rectangle.
            self.rect.bottom = yBullet  # y coordinate of user.
            self.rect.centerx = xBullet  # x coordinate of user.
            self.speedy = -10  # Speed the bullet moves.

        # Function below kills the bullet when it is off the screen and allows the bullet to move across the screen.
        def update(self):
            self.rect.y = self.rect.y + self.speedy  # Allows the bullet to move along the y axis.
            # Kill the bullet if it moves off the top of the screen.
            if self.rect.bottom < 0:  # If the bullet is above the screen.
                self.kill()  # The bullet kills itself.

    # Function below gets the high score for the 1 player mode.
    # Code within this function will create a txt file for the score, called "Scores1.txt".
    def getHighScore():
        score1File = open("Scores1.txt", "a")  # Open text file in append mode.
        score1File.write(str(score) + "\n")  # Append the score to the end of the file on a new line.
        score1File.close()  # Close file.
        score1File = open("Scores1.txt", "r")  # Opens file in read mode.
        with open('Scores1.txt', 'r') as file1:  # Used to clean up data by removing values.
            data1 = [line.strip() for line in file1]  # Gets rid of spaces, new lines, and stores all in a list.
        score1File.close()  # Close file.

        highScore = 0  # Variable used to hold high score.
        for item in range(len(data1)):  # Loops for how many items in the data list.
            currentScore1 = int(data1[
                                    item])  # The variable is equivalent to i, the position of data in the list. The string is converted to integer.
            # Comparison of integers to find out the largest.
            if currentScore1 >= highScore:
                highScore = currentScore1
            else:
                highScore = highScore

        return highScore  # return highScore back to variable

    # Function below displays the game over screen for when the ship lives is equal to 0.
    def gameOverScreen():
        highScore = getHighScore()  # Calls the getHighScore function, gets the high score and stores it in a variable.
        screen.blit(bg, bgRect)  # Draw background onto screen.
        pygame.display.flip()  # Flip display.
        # Display text on the screen so the user can see score and know how to navigate to other parts.
        displayText(screen, "ShootEmUp!", 65, WIDTH / 2 + 20, HEIGHT - 925)
        displayText(screen, "Your Score:", 40, WIDTH / 2, HEIGHT / 4)
        displayText(screen, str(score), 60, WIDTH / 2, HEIGHT / 2)
        displayText(screen, "High Score:" + str(highScore), 40, WIDTH / 2, HEIGHT * 3 / 4)
        displayText(screen, "R - Play Again", 30, WIDTH / 2, HEIGHT - 190)
        displayText(screen, "ESC - Return to menu", 30, WIDTH / 2, HEIGHT - 160)
        displayText(screen, "Q - Quit Game", 30, WIDTH / 2, HEIGHT - 130)
        displayText(screen, "Developed By,", 22, WIDTH / 2, HEIGHT - 69)
        displayText(screen, "Ahmad Kamal Abdul Hafiz.", 22, WIDTH / 2, HEIGHT - 47)
        displayText(screen, "Software Engineering Coursework 1.", 22, WIDTH / 2, HEIGHT - 25)
        pygame.display.flip()  # Flip display back to other side.

        waiting = True
        while waiting:
            pygame.init()  # Initialise pygame.
            for event1p in pygame.event.get():  # Process input.
                if event1p.type == pygame.QUIT:  # If the user clicks the "X" button.
                    exit()  # Quit therefore, game ends.
                elif event1p.type == pygame.KEYDOWN:
                    if event1p.key == pygame.K_ESCAPE:  # If ESC button is pressed.
                        score1Output.config(text="1 Player Hi-Score: " + str(highScore))  # Updates label.
                        root.deiconify()  # Tkinter window is given focus.
                        root.update()  # Update Tkinter window.
                        waiting = False  # Loop ends.
                        pygame.quit()  # Pygame window quits.
                        root.mainloop()  # Tkinter window reappears.
                    if event1p.key == pygame.K_q:  # If Q is pressed.
                        exit()  # Quit therefore, game ends.
                    if event1p.key == pygame.K_r:  # If R is pressed.
                        onePlayer()  # Call the onePlayer function and play again.
                        root.withdraw()  # Hides Tkinter window.

    bg = pygame.image.load(path.join(imageDir, "Background.png")).convert()  # Load the background and store it.
    bgSize = bg.get_size()  # Store the width and height of the background.
    bgRect = bg.get_rect()  # Get rectangle of the background.
    w, h = bgSize  # (x, y), w = x and h = y.
    # Background x and y values. To be used in a scrolling background etc.
    bgX = 0
    bgY = 0
    bgX1 = 0
    bgY1 = -h

    shipImg = pygame.image.load(path.join(imageDir, "SpaceShip1.png")).convert()  # Load the spaceship image.
    bulletImg = pygame.image.load(path.join(imageDir, "Bullet1.png")).convert()  # Load the bullet image.

    alienImg = []  # Create an empty list.
    alienList = ["Alien1.png", "Alien2.png", "Alien3.png", "Alien4.png"]  # Alien images.
    for img in alienList:  # Loop for the amount of images in the list.
        alienImg.append(
            pygame.image.load(path.join(imageDir, img)).convert())  # Convert it and add it to the empty list.

    heart1Img = pygame.image.load(path.join(imageDir, "Heart1.png")).convert()  # Load the heart image.
    heart1Img.set_colorkey(BLACK)  # Get rid of the black entities of the heart.

    shootSound = pygame.mixer.Sound(path.join(soundDir, "Pew.wav"))  # Store pew sound from the sound directory.
    explosionSound = pygame.mixer.Sound(
        path.join(soundDir, "Explosion.wav"))  # Store explosion sound from sound directory.
    pygame.mixer.music.load(path.join(soundDir, "AfterHoursInstrumental.mp3"))  # Load background music.

    pygame.mixer.music.set_volume(1)  # Set volume of music.
    pygame.mixer.Sound.set_volume(shootSound, 0.1)  # Set volume of shoot sound.
    pygame.mixer.Sound.set_volume(explosionSound, 0.1)  # Set volume of explosion sound.

    allSprites = pygame.sprite.Group()  # Hold all sprites in a group. Separate from other groups.
    aliens = pygame.sprite.Group()  # Hold all aliens in a group. Separate from other groups.
    bullets = pygame.sprite.Group()  # Hold all bullets in a group. Separate from other groups.

    ship = Ship()  # Stores the Ship class in a variable.
    allSprites.add(ship)  # Adds ship to the allSprites group.

    # Spawns the mobs (aliens).
    for mobs1P in range(20):  # Increase range more mobs spawn.
        a = Alien()  # Stores the Alien in a variable.
        allSprites.add(a)  # Adds alien to the allSprites group.
        aliens.add(a)  # Adds alien to the aliens group.

    score = 0  # Set score to 0

    pygame.mixer.music.play(loops=-1)  # Infinite loop of music.
    tgMusic = ToggleMusic()  # Instantiate.

    pause = False
    # Game loop, The main loop, constantly run over and over, each loop is called a frame.
    running = True
    while running:
        clock.tick(FPS)  # Keep loop running at the same speed.
        for event in pygame.event.get():  # Process input.
            if event.type == pygame.QUIT:  # If the user clicks the "X" button.
                running = False  # Loop ends therefore, game ends.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # If m is pressed.
                    ToggleMusic.toggle(tgMusic)  # Toggle music.
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:  # If p is pressed.
                    pause = True  # Pause is true

        # Whilst pause nothing is moving on the screen.
        while pause:
            for event in pygame.event.get():  # Process input
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:  # If p is pressed.
                        pause = False  # Pause is false.

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        ToggleMusic.toggle(tgMusic)

        # Scrolling background. Infinite looping background, the background continuously moves.
        bgY1 = bgY1 + 5  # How much the background should move by.
        bgY = bgY + 5  # How much the background should move by.
        screen.blit(bg, (bgX, bgY))  # Draw onto the screen.
        screen.blit(bg, (bgX1, bgY1))  # Draw onto the screen.
        # Causes the background to move.
        if bgY > h:
            bgY = -h
        if bgY1 > h:
            bgY1 = -h

        allSprites.update()  # Update, changes anything that needs to change on the frame.

        # Checks for a collision between a alien and a bullet.
        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)  # Compares the aliens and bullets group.
        for _ in hits:  # groupCollide compare two groups, two lists essentially.
            score = score + 50  # Increase score by 50 each time alien is hit.
            explosionSound.play()  # Play explosion sound when alien is killed.
            # Spawn another alien for each alien hit.
            a = Alien()
            allSprites.add(a)
            aliens.add(a)

        # Checks for a collision between a alien and the ship.
        hits = pygame.sprite.spritecollide(ship, aliens, True,
                                           pygame.sprite.collide_circle)  # Compare aliens group with the ship sprite. Set true so alien disappear.
        for _ in hits:  # spriteCollide is a list of the sprites that were hit. If list not empty, if statement will be true.
            ship.lives = ship.lives - 1  # Everytime the user gets hit subtract 1 from lives.
            # Spawn another alien for each one killed.
            a = Alien()
            allSprites.add(a)
            aliens.add(a)

        if ship.lives == 0:  # If lives is 0 end game.
            gameOverScreen()  # Calls function.
            sys.exit()  # Exit the window, with no errors using systems.

        allSprites.draw(screen)  # Draw everything on the screen.
        displayText(screen, str(score), 30, WIDTH / 2, 10)  # Show score on window.
        displayLives(screen, WIDTH - 600, 5, ship.lives, heart1Img)  # Draw lives onto screen.
        pygame.display.update()  # Update screen.

    pygame.quit()  # Quit pygame.


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

# Function below if called if the "2 Player" button is pressed in the GUI window.
def twoPlayer():
    root.withdraw()

    imageDir = path.join(path.dirname(__file__), "IMAGES")
    soundDir = path.join(path.dirname(__file__), "SOUND")

    WIDTH = 600
    HEIGHT = 925
    FPS = 60

    BLACK = (0, 0, 0)

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ShootEmUp!")
    Icon = pygame.image.load("IMAGES/Icon.png")
    pygame.display.set_icon(Icon)

    clock = pygame.time.Clock()

    def displayLives(surf, xLife, yLife, lives, heartImg):
        for life in range(lives):
            imgRect = heartImg.get_rect()
            imgRect.x = xLife + 50 * life
            imgRect.y = yLife
            surf.blit(heartImg, imgRect)

    class ToggleMusic(object):
        def __init__(self):
            self.paused = pygame.mixer.music.get_busy()

        def toggle(self):
            if self.paused:
                pygame.mixer.music.unpause()
            if not self.paused:
                pygame.mixer.music.pause()
            self.paused = not self.paused

    # Class below creates the first ship the first player will interact with, whilst playing the game.
    class Ship1(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(ship1Img, (99, 75))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 25
            self.rect.centerx = WIDTH * 3 / 4  # Places ship on the right hand side of the screen.
            self.rect.bottom = HEIGHT - 10  # Places sprite (0, 915) on the screen.
            self.speedx = 0
            self.speedy = 0
            self.lives = 3
            self.shootDelay = 200
            self.lastShot = pygame.time.get_ticks()

        def update(self):
            self.speedx = 0
            self.speedy = 0
            keyState = pygame.key.get_pressed()
            if keyState[pygame.K_LEFT]:
                self.speedx = -8
            if keyState[pygame.K_RIGHT]:
                self.speedx = 8
            if keyState[pygame.K_UP]:
                self.speedy = -8
            if keyState[pygame.K_DOWN]:
                self.speedy = 8
            if keyState[pygame.K_SPACE]:
                self.shoot()

            self.rect.x = self.rect.x + self.speedx
            self.rect.y = self.rect.y + self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

        def shoot(self):
            n = pygame.time.get_ticks()
            if n - self.lastShot > self.shootDelay:
                self.lastShot = n
                bullet = Bullet1(self.rect.centerx, self.rect.top)
                allSprites.add(bullet)
                bullets.add(bullet)
                shootSound.play()

    # Class below creates the second ship the second player will interact with, whilst playing the game.
    class Ship2(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(ship2Img, (99, 75))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 25
            self.rect.centerx = WIDTH / 4  # Places ship on the left hand side of the screen.
            self.rect.bottom = HEIGHT - 10  # Places sprite (0,915) on the screen.
            self.speedx = 0
            self.speedy = 0
            self.lives = 3
            self.shootDelay = 200
            self.lastShot = pygame.time.get_ticks()

        def update(self):
            self.speedx = 0
            self.speedy = 0
            keyState = pygame.key.get_pressed()  # Stores the key that is pressed.
            if keyState[pygame.K_a]:  # If a pressed.
                self.speedx = -8  # Move 8 pixels left.
            if keyState[pygame.K_d]:  # If d pressed.
                self.speedx = 8  # Move 8 pixels right.
            if keyState[pygame.K_w]:  # If w pressed.
                self.speedy = -8  # Move 8 pixels up.
            if keyState[pygame.K_s]:  # If s pressed.
                self.speedy = 8  # Move 8 pixels down.
            if keyState[pygame.K_f]:  # If the user presses space.
                self.shoot()  # runs ship shoot() method.

            self.rect.x = self.rect.x + self.speedx
            self.rect.y = self.rect.y + self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

        def shoot(self):
            n = pygame.time.get_ticks()
            if n - self.lastShot > self.shootDelay:
                self.lastShot = n
                bullet = Bullet2(self.rect.centerx, self.rect.top)
                allSprites.add(bullet)
                bullets.add(bullet)
                shootSound.play()

    class Alien(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = random.choice(alienImg)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width / 2)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x = self.rect.x + self.speedx
            self.rect.y = self.rect.y + self.speedy

            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

    class Bullet1(pygame.sprite.Sprite):
        def __init__(self, xBullet, yBullet):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet1Img, (9, 54))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = yBullet
            self.rect.centerx = xBullet
            self.speedy = -10

        def update(self):
            self.rect.y = self.rect.y + self.speedy

            if self.rect.bottom < 0:
                self.kill()

    class Bullet2(pygame.sprite.Sprite):
        def __init__(self, xBullet, yBullet):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet2Img, (9, 54))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = yBullet
            self.rect.centerx = xBullet
            self.speedy = -10

        def update(self):
            self.rect.y = self.rect.y + self.speedy
            if self.rect.bottom < 0:
                self.kill()

    # Function below gets the high score for the 2 player mode.
    # Code within this function will create a txt file for the score, called "Scores2.txt".
    def getHighScore():
        score2File = open("Scores2.txt", "a")
        score2File.write(str(score) + "\n")
        score2File.close()
        with open('Scores2.txt', 'r') as file2:
            data2 = [line.strip() for line in file2]
        score2File.close()

        highScore = 0
        for item in range(len(data2)):
            currentScore2p = int(data2[item])

            if currentScore2p >= highScore:
                highScore = currentScore2p
            else:
                highScore = highScore

        return highScore

    def gameOverScreen():
        highScore = getHighScore()
        screen.blit(bg, bgRect)
        pygame.display.flip()

        displayText(screen, "ShootEmUp!", 65, WIDTH / 2 + 20, HEIGHT - 925)
        displayText(screen, "Your Score:", 40, WIDTH / 2, HEIGHT / 4)
        displayText(screen, str(score), 60, WIDTH / 2, HEIGHT / 2)
        displayText(screen, "High Score:" + str(highScore), 40, WIDTH / 2, HEIGHT * 3 / 4)
        displayText(screen, "R - Play Again", 30, WIDTH / 2, HEIGHT - 190)
        displayText(screen, "ESC - Return to menu", 30, WIDTH / 2, HEIGHT - 160)
        displayText(screen, "Q - Quit Game", 30, WIDTH / 2, HEIGHT - 130)
        displayText(screen, "Developed By,", 22, WIDTH / 2, HEIGHT - 69)
        displayText(screen, "Ahmad Kamal Abdul Hafiz.", 22, WIDTH / 2, HEIGHT - 47)
        displayText(screen, "Software Engineering Coursework 1.", 22, WIDTH / 2, HEIGHT - 25)
        pygame.display.flip()

        waiting = True
        while waiting:
            pygame.init()
            for event2p in pygame.event.get():
                if event2p.type == pygame.QUIT:
                    pygame.quit()
                elif event2p.type == pygame.KEYDOWN:
                    if event2p.key == pygame.K_ESCAPE:
                        score2Output.config(text="2 Player Hi-Score: " + str(highScore))  # Updates label.
                        root.deiconify()
                        root.update()
                        waiting = False
                        pygame.quit()
                        root.mainloop()
                    if event2p.key == pygame.K_q:
                        exit()
                    if event2p.key == pygame.K_r:  # If R is pressed.
                        twoPlayer()  # Call the twoPlayer function and play again.
                        root.withdraw()  # Hides Tkinter window.

    bg = pygame.image.load(path.join(imageDir, "Background.png")).convert()
    bgSize = bg.get_size()
    bgRect = bg.get_rect()
    w, h = bgSize

    bgX = 0
    bgY = 0
    bgX1 = 0
    bgY1 = -h

    ship1Img = pygame.image.load(
        path.join(imageDir, "SpaceShip1.png")).convert()  # Load the first player spaceship image.
    ship2Img = pygame.image.load(
        path.join(imageDir, "SpaceShip2.png")).convert()  # Load the second player spaceship image.

    bullet1Img = pygame.image.load(path.join(imageDir, "Bullet1.png")).convert()  # Load the first player bullet image.
    bullet2Img = pygame.image.load(path.join(imageDir, "Bullet2.png")).convert()  # Load the second player bullet image.

    alienImg = []
    alienList = ["Alien1.png", "Alien2.png", "Alien3.png", "Alien4.png"]
    for img in alienList:
        alienImg.append(pygame.image.load(path.join(imageDir, img)).convert())

    heart1Img = pygame.image.load(path.join(imageDir, "Heart1.png")).convert()  # Load the fist player heart image.
    heart1Img.set_colorkey(BLACK)  # Get rid of the black entities of the heart.
    heart2Img = pygame.image.load(path.join(imageDir, "Heart2.png")).convert()  # Load the second player heart image.
    heart2Img.set_colorkey(BLACK)  # Get rid of the black entities of the heart.

    shootSound = pygame.mixer.Sound(path.join(soundDir, "Pew.wav"))
    explosionSound = pygame.mixer.Sound(path.join(soundDir, "Explosion.wav"))
    pygame.mixer.music.load(path.join(soundDir, "AfterHoursInstrumental.mp3"))

    pygame.mixer.music.set_volume(1)  # Set volume of music.
    pygame.mixer.Sound.set_volume(shootSound, 0.1)  # Set volume of shoot sound.
    pygame.mixer.Sound.set_volume(explosionSound, 0.1)  # Set volume of explosion sound.

    allSprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    ship1 = Ship1()  # Stores the Ship1 class in a variable.
    ship2 = Ship2()  # Stores the Ship2 class in a variable.
    allSprites.add(ship1)  # Adds ship1 to the allSprites group.
    allSprites.add(ship2)  # Adds ship2 to the allSprites group.

    for mobs2P in range(30):
        a = Alien()
        allSprites.add(a)
        aliens.add(a)

    score = 0

    pygame.mixer.music.play(loops=-1)
    tgMusic = ToggleMusic()

    pause = False

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    ToggleMusic.toggle(tgMusic)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        pause = False

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        ToggleMusic.toggle(tgMusic)

        bgY1 = bgY1 + 5
        bgY = bgY + 5
        screen.blit(bg, (bgX, bgY))
        screen.blit(bg, (bgX1, bgY1))
        if bgY > h:
            bgY = -h
        if bgY1 > h:
            bgY1 = -h

        allSprites.update()

        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for _ in hits:
            score = score + 50
            explosionSound.play()
            a = Alien()
            allSprites.add(a)
            aliens.add(a)

        # Checks for a collision between a alien and the first player ship.
        hits = pygame.sprite.spritecollide(ship1, aliens, True, pygame.sprite.collide_circle)
        for _ in hits:
            ship1.lives = ship1.lives - 1

            a = Alien()
            allSprites.add(a)
            aliens.add(a)

        # Checks for a collision between a alien and second player ship.
        hits = pygame.sprite.spritecollide(ship2, aliens, True, pygame.sprite.collide_circle)
        for _ in hits:
            ship2.lives = ship2.lives - 1

            a = Alien()
            allSprites.add(a)
            aliens.add(a)

        if ship1.lives == 0:  # If the fist player ship lives is 0 player dies, shouldn't affect the other ship.
            ship1.rect.bottom = HEIGHT + 50  # Move ship off screen.
            ship1.kill()  # Kills ship.
        if ship2.lives == 0:  # If the second player ship lives is 0 player dies, shouldn't affect the other ship.
            ship2.rect.bottom = HEIGHT + 50  # Move ship off screen.
            ship2.kill()  # Kills ship.

        totalShipLives = ship1.lives + ship2.lives  # Variable holding total ship lives.
        if totalShipLives == 0:  # If both ship are dead then the lives should total to 0 and game ends.
            gameOverScreen()  # Calls function.
            sys.exit()  # Exit the window, with no errors using systems.

        allSprites.draw(screen)
        displayText(screen, str(score), 30, WIDTH / 2, 10)
        displayLives(screen, WIDTH - 600, 5, ship1.lives, heart1Img)  # Draw the first player lives onto screen.
        displayLives(screen, WIDTH - 600, 50, ship2.lives, heart2Img)  # Draw the second players lives onto screen.
        pygame.display.update()

    pygame.quit()


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

def infoControls():  # Called if info/controls button is pressed.
    root.withdraw()  # Hide Tkinter window.

    imageDir = path.join(path.dirname(__file__), "IMAGES")  # Image directory on computer.

    WIDTH = 600  # Width of pygame window.
    HEIGHT = 925  # Height of pygame window.

    pygame.init()  # Initialise pygame. Required to start.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates pygame window screen.
    pygame.display.set_caption("ShootEmUp!")  # Name of displayed pygame window.
    Icon = pygame.image.load("IMAGES/Icon.png")  # Icon loaded from images folder.
    pygame.display.set_icon(Icon)  # Displays icon on pygame window. Top left, left of pygame window name.

    bg = pygame.image.load(path.join(imageDir, "Background.png")).convert()  # Load the background and store it.
    bgRect = bg.get_rect()  # Store the width and height of the background.

    screen.blit(bg, bgRect)  # Draw background onto screen.
    pygame.display.flip()  # Flip display.
    # Display text on the screen so the user can see score and know how to navigate to other parts.
    displayText(screen, "ShootEmUp!", 65, WIDTH / 2 + 20, HEIGHT - 925)
    displayText(screen, "Player 1 Controls", 22, WIDTH / 2, HEIGHT - 830)
    displayText(screen, "Up Arrow - Move Forward", 20, WIDTH / 2, HEIGHT - 810)
    displayText(screen, "Left Arrow - Move Left", 20, WIDTH / 2, HEIGHT - 790)
    displayText(screen, "Down Arrow - Move Backwards", 20, WIDTH / 2, HEIGHT - 770)
    displayText(screen, "Right Arrow - Move Right", 20, WIDTH / 2, HEIGHT - 750)
    displayText(screen, "Space - Shoot", 20, WIDTH / 2, HEIGHT - 730)
    displayText(screen, "Player 2 Controls", 22, WIDTH / 2, HEIGHT - 670)
    displayText(screen, "W - Move Forward", 20, WIDTH / 2, HEIGHT - 650)
    displayText(screen, "A - Move Left", 20, WIDTH / 2, HEIGHT - 630)
    displayText(screen, "S - Move Backwards", 20, WIDTH / 2, HEIGHT - 610)
    displayText(screen, "D - Move Right", 20, WIDTH / 2, HEIGHT - 590)
    displayText(screen, "F - Shoot", 20, WIDTH / 2, HEIGHT - 570)
    displayText(screen, "P - Pause Game", 22, WIDTH / 2, HEIGHT - 510)
    displayText(screen, "M - Toggle Music", 22, WIDTH / 2, HEIGHT - 490)
    displayText(screen, "CREDITS", 22, WIDTH / 2, HEIGHT - 435)
    displayText(screen, "Background from desktopbackground.org", 20, WIDTH / 2, HEIGHT - 415)
    displayText(screen, "Spaceships and bullets by Kenney (www.kenney.n1)", 20, WIDTH / 2, HEIGHT - 395)
    displayText(screen, "Aliens by Kenney (www.kenney.n1)", 20, WIDTH / 2, HEIGHT - 375)
    displayText(screen, "Heart by DontMind8.blogspot.com", 20, WIDTH / 2, HEIGHT - 355)
    displayText(screen, "Music, The Weeknd - After Hours (Instrumental)", 20, WIDTH / 2, HEIGHT - 335)
    displayText(screen, "Press ESC to return to menu.", 22, WIDTH / 2, HEIGHT - 280)
    displayText(screen, "Press Q to quit game", 22, WIDTH / 2, HEIGHT - 258)
    displayText(screen, "Developed By,", 22, WIDTH / 2, HEIGHT - 69)
    displayText(screen, "Ahmad Kamal Abdul Hafiz.", 22, WIDTH / 2, HEIGHT - 47)
    displayText(screen, "Software Engineering Coursework 1.", 22, WIDTH / 2, HEIGHT - 25)
    pygame.display.flip()  # Flip display.
    pygame.display.update()  # Update screen.

    waiting = True
    while waiting:
        pygame.init()  # Initialise pygame.
        for event in pygame.event.get():  # Process input.
            if event.type == pygame.QUIT:  # If the user clicks the "X" button.
                exit()  # Quit therefore, game ends.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # If ESC button is pressed.
                    root.deiconify()  # Tkinter window reappears.
                    root.update()  # Update Tkinter window.
                    waiting = False  # Loop ends.
                    pygame.quit()  # Pygame window quits.
                if event.key == pygame.K_q:  # If Q is pressed.
                    exit()  # Quit therefore, game ends.


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

def ResetScores():  # Called if reset scores button is pressed.
    resetScore1 = open("Scores1.txt", "w+")  # Opens file and overwrites it, emptying its content. Nothing in text file.
    resetScore1.close()  # Close file.
    score1Output.config(text="1 Player Hi-Score: " + "0")  # Updates label so score says 0.
    resetScore2 = open("Scores2.txt", "w+")  # Opens file and overwrites it, emptying its content. Nothing in text file.
    resetScore2.close()  # Close file.
    score2Output.config(text="2 Player Hi-Score: " + "0")  # Updates label so score says 0.


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

def quitGame():  # Called if quit button pressed.
    exit()  # Close all windows in relation to the software.


##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

f = open("Scores1.txt",
         "a")  # If no existing txt file, create a new one, append to ensure that file is not overwritten if program run again.
f.close()  # Close file.
f = open("Scores1.txt", "r")  # Opens file in read mode.
with open('Scores1.txt', 'r') as f1:  # Used to clean up data by removing values.
    data = [line.strip() for line in f1]  # Gets rid of spaces, new lines, and stores all in a list.
f.close()  # Close file.

hScore1 = 0  # Variable used to hold high score for one player mode.
for i in range(len(data)):  # Loops for how many items in the data list.
    x = int(data[
                i])  # The variable is equivalent to i, the position of data in the list. The string is converted to integer.
    # Comparison of integers to find out the largest.
    if x >= hScore1:
        hScore1 = x
    else:
        hScore1 = hScore1

f = open("Scores2.txt",
         "a")  # If no existing txt file, create a new one, "a" to ensure that file is not overwritten if program run again.
f.close()  # Close file.
f = open("Scores2.txt", "r")  # Opens file in read mode.
with open('Scores2.txt', 'r') as f2:  # Used to clean up data by removing values.
    data = [line.strip() for line in f2]  # Gets rid of spaces, new lines, and stores all in a list.
f.close()  # Close file.

hScore2 = 0  # Variable used to hold high score for two player mode.
for i in range(len(data)):  # Loops for how many items in the data list
    x = int(data[
                i])  # The variable is equivalent to i, the position of data in the list. The string is converted to integer.
    # Comparison of integers to find out the largest.
    if x >= hScore2:
        hScore2 = x
    else:
        hScore2 = hScore2

strScore1 = str(hScore1)  # Converts high score into string and stores in a variable.
strScore2 = str(hScore2)  # Converts high score into string and stores in a variable.

root = Tk()  # Create Tkinter class.

root.title("ShootEmUp!")  # Name of tkinter window, the GUI window.
root.geometry("200x200")  # Size of the GUI window.

# Create button. Format: Button(POSITION DISPLAYED, text="YOUR TEXT", fg="COLOUR"(OPTIONAL), command=FUNCTION)
# Once button is clicked it would call the corresponding command, the function.
btn1P = Button(root, text="1 Player", fg="black", command=onePlayer)
btn2P = Button(root, text="2 Player", fg="black", command=twoPlayer)
btnIC = Button(root, text="Info/Controls", fg="black", command=infoControls)
btnQuit = Button(root, text="Quit", fg="black", command=quitGame)
btnReset = Button(root, text="Reset Scores", fg="black", command=ResetScores)

# Create labels. format: Label(POSITION DISPLAYED, text="YOUR TEXT")
title = Label(root, text="ShootEmUp!")
score1Output = Label(root, text="1 Player Hi-Score: " + strScore1)
score2Output = Label(root, text="2 Player Hi-Score: " + strScore2)

# Put content, button and labels in Tkinter window. Pack it into the window.
# Order packed will be order showed on Tkinter window.
title.pack()
btn1P.pack()
btn2P.pack()
btnIC.pack()
btnQuit.pack()
score1Output.pack()
score2Output.pack()
btnReset.pack()

root.mainloop()  # Displays Tkinter window.
