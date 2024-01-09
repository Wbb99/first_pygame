import pygame
pygame.init()

# Initialize the game window
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")

# Load player images
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

# Set up game clock
clock = pygame.time.Clock()

# Load game sounds and music
bullet_sound = pygame.mixer.Sound('bullet.mp3')
hit_sound = pygame.mixer.Sound('hit.mp3')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# Initialize score
score = 0

# Player class definition
class player(object):
    # Initialize player attributes
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    # Draw player on the window
    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not(self.standing):
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x,self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x,self.y))
                self.walk_count +=1
        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    # Handle player getting hit
    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        self.x = 100
        self.y = 410
        self.walk_count = 0
        font1 = pygame.font.SysFont('comicsans', 75)
        text = font1.render("-5", 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                

# Projectile class definition
class projectile(object):
    # Initialize projectile attributes
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    # Draw projectile on the window
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

# Enemy class definition
# Load in enemy pictures
class enemy(object):
    walk_right = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walk_left = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    # Initialize enemy attributes
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    # Draw enemy on the window
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0:
                win.blit(self.walk_right[self.walk_count //3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count //3], (self.x, self.y))
                self.walk_count += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    # Move enemy back and forth
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    # Handle enemy getting hit
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")

        
# Function to redraw the game window
def redrawGameWindow():
    # Draw background, score, player, enemy, and bullets on the window
    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (340, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()


# Main game loop
font = pygame.font.SysFont('comicsans', 25, True)
man = player(200, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 450)
shoot_loop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    # Collision detection between player and enemy
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update bullet positions    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hit_sound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))     
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Handle player input
    keys = pygame.key.get_pressed()

    # Handle player key space bar input
    if keys[pygame.K_SPACE] and shoot_loop == 0:
        bullet_sound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

        shoot_loop = 1

    # Handle player key left input
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    # Handle player key right input
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walk_count = 0
        
    # Handle player key up input
    if not(man.is_jump):
        if keys[pygame.K_UP]:
            man.is_jump = True
            man.right = False
            man.left = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10
            
    # Update and redraw the game window
    redrawGameWindow()

# Quit pygame
pygame.quit()