"""
Name: Zebenai Melaku    		ID: kkw2jg
Partner: Eiman Sherzada 		ID: vdx8fg

TITLE: Capybara Shootout!! #CutenessOverload 

Description of your game
In this multiplayer, capybara shoot-out game, the players must avoid one anothers flower bullets. Each hit results in depletion of their health. (idk how many times they get shot until they die) To restore their health, there will be boosters such as hearts for the capybaras to collect as they glide up and down the screen. 

List of the 3 basic features and how you will incorporate each one

USER INPUT:Users are going to use their keyboard in order to navigate their character, to collect boosters, and avoid being hit by one another. 
GAME OVER:The game is over when one of the users has gotten hit over a certain amount of times. Doing so will result in a game over screen. 
GRAPHICS/IMAGES:  Images such as a meadow, Capybaras, flower bullets, hearts, and other tiny details will be used to bring the game to life.
. 

List of 4 additional features and how you will incorporate each one
HEALTH BAR: the bar shrinks each time a player gets hit by a bullet. When the bar of one of the players fully depletes, the game terminates. However, the bar replenishes and extends to its maximum length when a capybara is able to obtain a booster. 
MULTIPLAYER/ENEMIES: Since the game is between two players, the enemies are one another.
COLLECTABLES: there will be boosters in the form of hearts to replenish their health. 
SPRITE ANIMATION: 2D Animation is used to showcase the capybara turning its back, left and right, as well as dying. 


CHANGES: The overall changes made is the type of game we are creating as previously we made a single player, maze-like game. 

INSTRUCTIONS: 
WASD keys for player 1
Arrow keys for player 2 
must move up and down to avoid the other player 
move up and down in order to obtain collectables 
game over when one of the players dies

"""

import uvage
import random

playerOneHealth = 100
playerTwoHealth = 100
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

#effect notices, purposley placed out of bounds
poisonAppleNotice_p1 = uvage.from_text(1000, 900, "POISON APPLE ACTIVE!!!", 30, "blue")
goldenAppleNotice_p1 = uvage.from_text(1000, 900, "GOLDEN APPLE ACTIVE!!!", 30, "red")

poisonAppleNotice_p2 = uvage.from_text(1000, 900, "POISON APPLE ACTIVE!!!", 30, "blue")
goldenAppleNotice_p2 = uvage.from_text(1000, 900, "GOLDEN APPLE ACTIVE!!!", 30, "red")

# box barriers
barrierLeft = uvage.from_color(-20, 300, "white", 50, 650)  # left wall
barrierRight = uvage.from_color(820, 300, "white", 50, 650)  # right wall
barrierTop = uvage.from_color(400, -25, "white", 850, 50)  # top wall
barrierBottom = uvage.from_color(400, 625, "white", 850, 50)  # bottom wall
barrierMiddle = uvage.from_color(400, 300, "white", 5, 600)  # middle wall

walls = [barrierLeft, barrierRight, barrierBottom, barrierMiddle, barrierTop]

players_sprite_sheet = uvage.load_sprite_sheet("217235346/playerImages2.png", 4, 7)

background2 = uvage.from_image(400, 300, "217235346/background_yay.png")
background2.width = 800

# player sprites and beams
playerOne = uvage.from_image(200, 475, players_sprite_sheet[10])
playerOne.scale_by(0.75)  # make sprites smaller due to game dimensions (.75 of its origninal size)

playerTwo = uvage.from_image(600, 100, players_sprite_sheet[10])
playerTwo.scale_by(0.75)  # make sprites smaller due to game dimensions
playerTwo.flip()  # make player2 sprite face the correct direction (players operate on opposite sides)

p1Beam = uvage.from_image(playerOne.x + 50, playerOne.y ,"217235346/flower.png")
p1Beam.scale_by(.03)
p2Beam = uvage.from_image(playerTwo.x + 50, playerTwo.y ,"217235346/Flower2.png")
p2Beam.scale_by(.065)

playerBeams = [p1Beam, p2Beam]
#obstacle sprites and powerups
speedSprite = uvage.from_image(1500, 900, "217235346/apple.png")
speedSprite.scale_by(.1)
broken_heartSprite = uvage.from_image(1500, 900, "217235346/broken_heart.png")
broken_heartSprite.scale_by(0.2)
poisonAppleSprite = uvage.from_image(1500, 900, "217235346/rotten_apple.png")
poisonAppleSprite.scale_by(.1)
heartSprite = uvage.from_image(1500, 900, "217235346/heart.png")
heartSprite.scale_by(0.2)

obstacle_sprites = [speedSprite, broken_heartSprite, poisonAppleSprite, heartSprite]

#obstacle sprites spawn points
leftSpawn_dLocations = [[-5,150],[100,-5],[250,-5]] # downward slope spawn locations from left
rightSpawn_dLocations = [[805,150],[700,-5],[650,-5]] # downward slope spawn locations from right

downSlopes = [leftSpawn_dLocations, rightSpawn_dLocations] # list of downward slopes

leftSpawn_uLocations = [[-5,450], [100,605], [250,605]] # upward slope spawn locations from left
rightSpawn_uLocations = [[805,450], [700, 605], [650, 605]] # upward slope spawn locations from right

upSlopes = [leftSpawn_uLocations, rightSpawn_uLocations] # list of upward slopes

up_down_Slopes = [upSlopes, downSlopes] # both up and down

#conditions for effects

slope = bool # decides upward or downward slope for obstacle sprites
side =  bool

beamSpeed_p1 = 12 # beam for player 1 speed
beamSpeed_p2 = 12 # beam for player 2 speed

goldenApple_p1 = False #tracks whether golden Apple/poison Apple effect is on and changes sprites for players (lines 119-123)
goldenApple_p2 = False

poisonApple_p1 = False
poisonApple_p2 = False

goldenAppleActive_p1 = False # tracks whether or not golden Apple or speed is active (lines 125-129)
poisonAppleActive_p1 = False

goldenAppleActive_p2 = False
poisonAppleActive_p2 = False

#tick timer counts
spriteSpawnCount = 0 # count for random sprite spawns
effectTimerCount_p1 = 0 # count for effect timer
effectTimerCount_p2 = 0 # count for effect timer

def draw_health_bar(health, x, y):
  ratio = health / 100
  
   
  health_bar = uvage.from_color(x, y, "pink", 200, 30)
  current_health = uvage.from_color(x , y, "white ", 200 * ratio, 30)

  

  
  camera.draw(health_bar)
  camera.draw(current_health)

def setup():
    global playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    global speedSprite, broken_heartSprite, heartSprite, poisonAppleSprite
    background2 = uvage.from_image(400, 300, "217235346/background_yay.png")
    background2.width = 1000
    camera.draw(background2)
    camera.draw(uvage.from_text(150, 60, "Player One Health: " + str(int(playerOneHealth)), 30, "red"))
    camera.draw(uvage.from_text(550, 60, "Player Two Health: " + str(int(playerTwoHealth)), 30, "red"))
  
    camera.draw(speedSprite)
    camera.draw(poisonAppleSprite)
    camera.draw(broken_heartSprite)
    camera.draw(heartSprite)
    createBeams()


def playerOneMovement():
    global walls
    global goldenApple_p1, poisonApple_p1, goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2

    for wall in walls:  # makes barriers solid when hitting player
        playerOne.move_to_stop_overlapping(wall)

    if uvage.is_pressing("a"):  # left arrow (backwards)
        if goldenApple_p1:
            playerOne.speedx -= .5
        elif poisonApple_p1:
            playerOne.speedx -= .25
        else:
            playerOne.speedx -= .35
        playerOne.image = players_sprite_sheet[10]

    if uvage.is_pressing("d"):  # right arrow (forward facing)
        if goldenApple_p1:
            playerOne.speedx += 1
            playerOne.image = players_sprite_sheet[0]  # double engine for golden Apple
        elif poisonApple_p1:
            playerOne.speedx += .25
            playerOne.image = players_sprite_sheet[10]
        else:
            playerOne.speedx += .5
            playerOne.image = players_sprite_sheet[1]

    if uvage.is_pressing("w"):  # up arrow
        if goldenApple_p1:
            playerOne.speedy -= 1
            playerOne.image = players_sprite_sheet[9]  # double engine for goldenApple
        elif poisonApple_p1:
            playerOne.speedy -= .25
            playerOne.image = players_sprite_sheet[15]
        else:
            playerOne.speedy -= .5
            playerOne.image = players_sprite_sheet[6]

    if uvage.is_pressing("s"):  # down arrow
        if goldenApple_p1:
            playerOne.speedy += 1
            playerOne.image = players_sprite_sheet[14]  # double engine for golden Apple
        elif poisonApple_p1:
            playerOne.speedy += .25
            playerOne.image = players_sprite_sheet[12]
        else:
            playerOne.speedy += .5
            playerOne.image = players_sprite_sheet[3]
    playerOne.move_speed()


def playerTwoMovement():
    global walls
    global goldenApple_p2, poisonApple_p2, goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2

    for wall in walls:  # makes barriers solid when hitting player 
        playerTwo.move_to_stop_overlapping(wall)

    if uvage.is_pressing('right arrow'):  # (going backwards) no engine sprites
        if goldenApple_p2:
            playerTwo.speedx += .5
        elif poisonApple_p2:
            playerTwo.speedx += .25
        else:
            playerTwo.speedx += .35
        playerTwo.image = players_sprite_sheet[10]

    if uvage.is_pressing('left arrow'):  # forward Facing
        if goldenApple_p2:
            playerTwo.speedx -= 1
            playerTwo.image = players_sprite_sheet[0]  # double engine for golden Apple
        elif poisonApple_p2:
            playerTwo.speedx -= .25
            playerTwo.image = players_sprite_sheet[10]  # no engine for poisonAppleSprite
        else:
            playerTwo.speedx -= .5
            playerTwo.image = players_sprite_sheet[1]

    if uvage.is_pressing('up arrow'):
        if goldenApple_p2:
            playerTwo.speedy -= 1
            playerTwo.image = players_sprite_sheet[9]  # double engine for golden Apple
        elif poisonApple_p2:
            playerTwo.speedy -= .25
            playerTwo.image = players_sprite_sheet[15]  # no engine for poisonAppleSprite
        else:
            playerTwo.speedy -= .5
            playerTwo.image = players_sprite_sheet[6]
    if uvage.is_pressing('down arrow'):
        if goldenApple_p2:
            playerTwo.speedy += 1
            playerTwo.image = players_sprite_sheet[14]  # double engine for golden Apple
        elif poisonApple_p2:
            playerTwo.speedy += .25
            playerTwo.image = players_sprite_sheet[12]  # no engine for poisonAppleSprite
        else:
            playerTwo.speedy += .5
            playerTwo.image = players_sprite_sheet[3]
    playerTwo.move_speed()


def createBeams():
    global p1Beam, p2Beam
    camera.draw(p1Beam)
    camera.draw(p2Beam)


def handle_beams(): # keeps beam speed consisten but move in opposite directions
    global p1Beam, p2Beam
    p1Beam.speedx = beamSpeed_p1
    p2Beam.speedx = -(beamSpeed_p2)

    p1Beam.move_speed()
    p2Beam.move_speed()


def outOfBounds_p1Beam():
    return p1Beam.x > 800


def outOfBounds_p2Beam():
    return p2Beam.x < 0


def reload_p1Beam():
    global p1Beam
    p1Beam  = uvage.from_image(playerOne.x + 50, playerOne.y ,"217235346/flower.png")
    p1Beam.scale_by(.03)
    # moves beam back in front of player


def reload_p2Beam():
    global p2Beam
    p2Beam  = uvage.from_image(playerTwo.x + 50, playerTwo.y ,"217235346/Flower2.png")
    p2Beam.scale_by(.065)
    # moves beam back in front of player

def set_spawnPoints():
    global leftSpawn_dLocations, rightSpawn_dLocations, slope, side
    global leftSpawn_uLocations, rightSpawn_uLocations, upSlopes, downSlopes, up_down_Slopes
    up_or_down = random.randint(0,1)
    left_or_right = random.randint(0,1)
    coordinates = random.randint(0,2)

    x = up_down_Slopes[up_or_down][left_or_right][coordinates][0] # gets x coordinate
    y = up_down_Slopes[up_or_down][left_or_right][coordinates][1] # gets y coordinate


    slope = up_or_down == 0
    #stores slope as True aka upwards if 0 
    #stores slope as False aka downwards if 1
    side = left_or_right == 0 
    #stores side as True aka left if 0 
    #stores side as False aka right if 1

    return x, y
    # returns a tuple containing...
    # (x coordinate, y coordinate)

def speed():
    # increases this speed when hitting this buff
    # Uses "apple.png"
    global speedSprite, playerOne, playerTwo, goldenApple_p1, goldenApple_p2, poisonApple_p1, poisonApple_p2
    global goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2
    x, y = set_spawnPoints()
    speedSprite = uvage.from_image(x, y, "217235346/apple.png")
    speedSprite.scale_by(.1)



def speedMove():
    global speedSprite, playerOne, playerTwo, goldenApple_p1, goldenApple_p2, poisonApple_p1, poisonApple_p2
    global goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2
    global effectTimerCount_p1, effectTimerCount_p2, slope, walls, side
    if speedSprite.touches(playerOne): 
    #when the sprite touches player this function activates the golden Apple effect,
    #changing the player character sprite and setting off the effect timer
        speedSprite = uvage.from_image(1500, 900, "217235346/apple.png") # moves sprite out of bounds
        speedSprite.scale_by(.1)
        goldenApple_p1 = True # turns on golden Apple effect and changes sprite
        poisonApple_p1 = False # turns off poison apple effect if active
        goldenAppleActive_p1 = True # sets off effect timer for golden Apple
        poisonAppleActive_p1 = False # if poison apple is active it turns off
        effectTimerCount_p1 = 0 # sets timer to zero for reassurance
        #every move function for speed/poison apple sprites follow the same patter but for its specific
        #player/effect

    if speedSprite.touches(playerTwo):
        speedSprite = uvage.from_image(1500, 900, "217235346/apple.png") # moves sprite out of bounds
        speedSprite.scale_by(.1)
        goldenApple_p2 = True
        poisonApple_p2 = False
        goldenAppleActive_p2 = True
        poisonAppleActive_p2 = False
        effectTimerCount_p2 = 0
    #this if statement spawns the sprite at a random location preset above and changes 
    #its movement appropriately with the spawn point
    # every move function for an obstacle sprite works the same way
    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            speedSprite.speedy = -5
            speedSprite.speedx = 5
        elif not side: # if right side condiiton 
            speedSprite.speedy = -5
            speedSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            speedSprite.speedy = 5
            speedSprite.speedx = 5
        elif not side: # if right side condiiton 
            speedSprite.speedy = 5
            speedSprite.speedx = -5
    speedSprite.move_speed()

def speedReduce():
    # reduces speed when hitting this debuff
    # uses "rotten_apple.png" sprite
    global poisonAppleSprite, playerOne, playerTwo, goldenApple_p1, goldenApple_p2, poisonApple_p1, poisonApple_p2
    global goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2
    x, y = set_spawnPoints() #sets x and y to the return values
    poisonAppleSprite = uvage.from_image(x,y, "217235346/rotten_apple.png")
    poisonAppleSprite.scale_by(.1)

def speedReduceMove():
    global poisonAppleSprite, playerOne, playerTwo, goldenApple_p1, goldenApple_p2, poisonApple_p1, poisonApple_p2
    global goldenAppleActive_p1 , poisonAppleActive_p1, goldenAppleActive_p2 , poisonAppleActive_p2, slope, walls, side
    global effectTimerCount_p1, effectTimerCount_p2

    if poisonAppleSprite.touches(playerOne):
        poisonAppleSprite = uvage.from_image(1500, 900, "217235346/rotten_apple.png") #moves sprite out of bounds
        poisonAppleSprite.scale_by(.1)
        poisonApple_p1 = True
        goldenApple_p1 = False
        goldenAppleActive_p1 = False
        poisonAppleActive_p1 = True
        effectTimerCount_p1 = 0
    if poisonAppleSprite.touches(playerTwo):
        poisonAppleSprite= uvage.from_image(1500, 900, "217235346/rotten_apple.png") # moves sprite out of bounds
        poisonAppleSprite.scale_by(.1)
        poisonApple_p2 = True
        goldenApple_p2 = False
        goldenAppleActive_p2 = False
        poisonAppleActive_p2 = True
        effectTimerCount_p2 = 0

    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            poisonAppleSprite.speedy = -5
            poisonAppleSprite.speedx = 5
        elif not side: # if right side condiiton 
            poisonAppleSprite.speedy = -5
            poisonAppleSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            poisonAppleSprite.speedy = 5
            poisonAppleSprite.speedx = 5
        elif not side: # if right side condiiton 
            poisonAppleSprite.speedy = 5
            poisonAppleSprite.speedx = -5

    poisonAppleSprite.move_speed()


def healthIncrease():
    # adds health to player when hitting this buff
    # uses "heart.png" sprite
    global heartSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth
    x, y = set_spawnPoints()
    heartSprite = uvage.from_image(x, y, "217235346/heart.png")
    heartSprite.scale_by(0.2)

def healthIncreaseMove():
    global heartSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth, slope, side, walls
    if heartSprite.touches(playerOne):
    #because heartsprite/broken_heartsprite dont have an effect it simple adds or removes heart depending
    #on effect and player
        heartSprite = uvage.from_image(1500, 900, "217235346/heart.png") # moves sprite out of bounds
        heartSprite.scale_by(0.2)
        if playerOneHealth <= 90: # if the health is greater than or equal to 90, we can add 10
            playerOneHealth += 10
        else:
            playerOneHealth = 100 # other wise set it to 100 to avoid going above limit of 100

    if heartSprite.touches(playerTwo):
        heartSprite = uvage.from_image(1500, 900, "217235346/heart.png") # moves sprite out of bounds
        heartSprite.scale_by(0.2)
        if playerTwoHealth <= 90:
            playerTwoHealth += 10
        else:
            playerTwoHealth = 100

    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            heartSprite.speedy = -5
            heartSprite.speedx = 5
        elif not side: # if right side condiiton 
            heartSprite.speedy = -5
            heartSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            heartSprite.speedy = 5
            heartSprite.speedx = 5
        elif not side: # if right side condiiton 
            heartSprite.speedy = 5
            heartSprite.speedx = -5

    heartSprite.move_speed()


def broken_heart():
    # player takes more broken heart when hitting this debuff+ str(int(playerTwoHealth)))
    # uses "broken_heart.png" sprite
    global broken_heartSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth
    x, y = set_spawnPoints()
    broken_heartSprite = uvage.from_image(x , y , "217235346/broken_heart.png")
    broken_heartSprite.scale_by(0.2)  

def broken_heartMove():
    global broken_heartSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth, slope, side, walls

    if broken_heartSprite.touches(playerOne):
        broken_heartSprite = uvage.from_image(1500, 900, "217235346/broken_heart.png") # moves sprite out of bounds
        broken_heartSprite.scale_by(0.2)
        if playerOneHealth >= 10:
            playerOneHealth -= 10
        else:
            playerOneHealth = 0
    if broken_heartSprite.touches(playerTwo):
        broken_heartSprite = uvage.from_image(1500, 900, "217235346/broken_heart.png") # moves sprite out of bounds
        broken_heartSprite.scale_by(0.2)
        if playerTwoHealth >= 10:
            playerTwoHealth -= 10
        else:
            playerTwoHealth = 0

    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            broken_heartSprite.speedy = -5
            broken_heartSprite.speedx = 5
        elif not side: # if right side condiiton 
            broken_heartSprite.speedy = -5
            broken_heartSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            broken_heartSprite.speedy = 5
            broken_heartSprite.speedx = 5
        elif not side: # if right side condiiton 
            broken_heartSprite.speedy = 5
            broken_heartSprite.speedx = -5

    broken_heartSprite.move_speed()

def handle_health():
    global playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    # as the player touches a beam they lose one health
    if p2Beam.touches(playerOne): 
        playerOneHealth -= 1
    if p1Beam.touches(playerTwo):
        playerTwoHealth -= 1

def gameOver(): #ends the game after game over message is displayed
    if playerOneHealth == -1: # set at -1 because game quits at health value 1 (lines 509, 511, 603, 608)
        return True
    elif playerTwoHealth == -1:
        return True  # player 1 wins
    return False


def tick():
    global walls, playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    global p1_Health, p2_Health, rand_num, spriteSpawnCount, effectTimerCount_p1, effectTimerCount_p2
    global goldenApple_p1, goldenApple_p2, poisonApple_p1, poisonApple_p2 
    global poisonAppleNotice_p1, poisonAppleNotice_p2, goldenAppleNotice_p1, goldenAppleNotice_p2
    camera.clear('black')
    setup() # creates beams, player health notices, and sprites

    if gameOver():
        return

    handle_health()

    spriteSpawnCount +=1

    playerOneMovement() # sets all the movements in order
    playerTwoMovement()
    speedMove()
    speedReduceMove()
    healthIncreaseMove()
    broken_heartMove()
    handle_beams()

    if spriteSpawnCount == 90: # every 3 seconds a sprite spawns
        random_effect = random.randint(0,4) # randomly selects an obstacle sprite
        if random_effect == 0:
            speed()
        elif random_effect == 1:
            speedReduce()
        elif random_effect == 2:
            healthIncrease()
        elif random_effect == 3:
            broken_heart()
        spriteSpawnCount = 0

    # in the following 4 if statments, the variable that displays the current effect moves into view
    # when said effects are applied
    if goldenAppleActive_p1: # 10 second timer golden Apple on player 1
        effectTimerCount_p1 +=1 # starts the timer
        goldenAppleNotice_p1 = uvage.from_text(150, 95, "GOLDEN APPLE ACTIVE!!!", 30, "red")

        if effectTimerCount_p1 == 300:#when it hits 300/10 seconds it cancels effect
            goldenApple_p1 = False
            effectTimerCount_p1 = 0 #resets the effect timer

    if goldenAppleActive_p2: # 10 second timer for golden Apple on player 2
        effectTimerCount_p2 +=1
        goldenAppleNotice_p2 = uvage.from_text(550, 95, "GOLDEN APPLE ACTIVE!!!", 30, "red")

        if effectTimerCount_p2 == 300: #when it hits 300 it cancels effect
            goldenAppleNotice_p2 = uvage.from_text(1000, 900, "GOLDEN APPLE ACTIVE!!!", 30, "red")
            goldenApple_p2 = False
            effectTimerCount_p2 = 0

    if poisonAppleActive_p1: # 10 second timer for poison apple on player 1
        effectTimerCount_p1 +=1
        poisonAppleNotice_p1 = uvage.from_text(150, 95, "POISON APPLE ACTIVE!!!", 30, "blue")

        if effectTimerCount_p1 == 300:#when it hits 300 it cancels effect
            poisonApple_p1 = False
            effectTimerCount_p1 = 0

    if poisonAppleActive_p2: # 10 second timer for posion apple on player 2
        effectTimerCount_p2 +=1
        poisonAppleNotice_p2 = uvage.from_text(550, 95, "POISON APPLE ACTIVE!!!", 30, "blue")

        if effectTimerCount_p2 == 300:#when it hits 300 it cancels effect
            poisonApple_p2 = False
            effectTimerCount_p2 = 0

    # when effect is up, it moves the messages back out of view
    if not poisonApple_p1:
        poisonAppleNotice_p1 = uvage.from_text(1000, 900, "SPOISON APPLE ACTIVE!!!", 30, "blue")
    if not poisonApple_p2:
        poisonAppleNotice_p2 = uvage.from_text(1000, 900, "POISON APPLE ACTIVE!!!", 30, "blue")
    if not goldenApple_p1:
        goldenAppleNotice_p1 = uvage.from_text(1000, 900, "POISON APPLE ACTIVE!!!", 30, "blue")
    if not goldenApple_p2:
        goldenAppleNotice_p2 = uvage.from_text(1000, 900, "POISON APPLE ACTIVE!!!", 30, "blue")

    if outOfBounds_p1Beam():  
        # reshoots player 1 beam when it goes out of bounds by moving it back in front of the player
        reload_p1Beam()
    if outOfBounds_p2Beam():  
        # reshoots player 2 beam when it goes out of bounds by moving it back in front of the player
        reload_p2Beam()

    if playerOneHealth <= -1:  # if player 2 wins
        for i in range(21, 28):  
        # ship explosion animation is created in this loop and the next for the appropriate players
            playerOne.image = players_sprite_sheet[i]
        camera.draw(uvage.from_text(360, 300, "GAME OVER!! PLAYER 2 WINS", 50, "red"))
    if playerTwoHealth <= -2:  # if player 1 wins
        for i in range(21, 28):
            playerTwo.image = players_sprite_sheet[i]
        camera.draw(uvage.from_text(360, 300, "GAME OVER!! PLAYER 1 WINS", 50, "red"))

    draw_health_bar(playerOneHealth, 150, 20)
    draw_health_bar(playerTwoHealth, 560, 20)
    camera.draw(playerOne)
    camera.draw(playerTwo)
    if playerOneHealth <= -1:  # if player 2 wins
      for i in range(21, 28):  
      # ship explosion animation is created in this loop and the next for the appropriate players
          playerOne.image = players_sprite_sheet[i]
      camera.draw(uvage.from_text(360, 300, "GAME OVER!! PLAYER 2 WINS", 50, "yellow"))

  
    if playerTwoHealth <= -1:  # if player 1 wins
      for i in range(21, 28):
          playerTwo.image = players_sprite_sheet[i]
      camera.draw(uvage.from_text(360, 300, "GAME OVER!! PLAYER 1 WINS", 50, "yellow"))

  
    camera.draw(goldenAppleNotice_p1) 
    camera.draw(goldenAppleNotice_p2)
    camera.draw(poisonAppleNotice_p1)
    camera.draw(poisonAppleNotice_p2)
    
    camera.display()
    

uvage.timer_loop(30, tick)