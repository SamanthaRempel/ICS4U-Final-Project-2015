import pygame, sys, random

(height, width) = (800, 1300)  # screen height and width

# colours!!!!
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (240, 150, 50)
yellow = (250, 250, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (200, 50, 200)
pink = (255, 0, 150)

colours = [red, orange, yellow, green, blue, purple, pink]

clock = pygame.time.Clock()

# the window
window = pygame.display.set_mode((width, height))  # the window that contains the size
pygame.display.set_caption("Snake")  # create a title for the screen
window.fill(white)  # creates the colour of the window


def down(points):
    '''
    if they press the down key
    :param points: y variable
    :return: new y postion
    '''
    y = points[1]
    if y < 790:
        y += 10
    else:
        y = 790
    points[1] = y
    return points


def up(points):
    '''
    if they press the up key
    :param points: y variable
    :return: new y postion
    '''
    y = points[1]
    if y > 0:
        y -= 10
    else:
        y = 0
    points[1] = y
    return points


def left(points):
    '''
    if they press the left key
    :param points: x variable
    :return: new x postion
    '''
    x = points[0]
    if x > 0:
        x -= 10
    else:
        x = 0
    points[0] = x
    return points


def right(points):
    '''
    if they press the right key
    :param points: x variable
    :return: new x postion
    '''
    x = points[0]
    if x < 1290:
        x += 10
    else:
        x = 1290
    points[0] = x
    return points


def grow(keyPressed, coords, colour):
    '''
    Create new coords in the coord list for the tail when the snake eats food
    :param keyPressed: The key that was just pressed
    :param coords: list of snake tail coords
    :param colour: The colour of the food
    :return: new coords list
    '''

    x = coords[-3]  # the very last x coord in the list (tail end)
    y = coords[-2]  # the very last y coord in the list (tail end)
    for i in range(1):
        if keyPressed[pygame.K_UP]:
            y += (length + i)
        elif keyPressed[pygame.K_DOWN]:
            y -= (length + i)
        elif keyPressed[pygame.K_LEFT]:
            x += (length + i)
        elif keyPressed[pygame.K_RIGHT]:
            x -= (length + i)
        coords.append(x)  # Add the new x and y coords
        coords.append(y)
        coords.append(colour)  # Add the food colour
    return coords


def coordChange(coords):
    '''
    Changing the coords of the snakes tail
    :param coords: the list of coords for the snake's tail
    :return: the new list of coords
    '''

    coords = coords[::-1]  # flip the list so you can work from the back to change the coords

    for i in range(1, 3):
        for j in range(i, len(coords) - 3,
                       3):  # go through all the x' and y's in a step 3, but not the snake head coords
            coords[j] = coords[j + 3]  # replace the current x or y with the x or y infront of it

    coords = coords[::-1]  # reflip the list so thre coords are in  the right order
    return coords


def hitDetect(coords, keyPressed, direction):
    '''
    Will check to see if the snake head hits the snake body
    :param coords: the list of coords in the snake body
    :param keyPressed: the key that was just hit
    :return: boolean True or False
    '''
    headX = coords[0]
    headY = coords[1]
    checkCoords = coords[3:]
    for i in range (1, len(checkCoords), 3):
        if checkCoords[i] == headX:
            if checkCoords[i+1] == headY:
                return True
    else:
        return False


length = 0


def main(length):
    '''
    Main loop of the game that runs the animation and will break when the player collides with anything other that food
    :param length: The length of the snake/player score
    :return: the players score/length
    '''

    coords = [650, 400, black]
    food = (random.randint(10, 1290), random.randint(10, 790), 10, 10)  # rng'd co-ords for the food
    foodColour = colours[random.randint(0, 6)]  # rng'd colour of the food
    direction = "up"  # set initial direction for the snake to travel

    while True:  # Infinite loop that will close the screen from user input

        x = coords[0]  # the snake's head x
        y = coords[1]  # the snake's head y

        for event in pygame.event.get():  # looks for user input to cancel game
            if event.type == pygame.QUIT:  # QUIT is a pygame action that is the cancel button on the screen
                sys.exit()  # exits if the user say

        window.fill(white)  # will remove the last thing drawn to replace with new drawing

        for c in range(0, len(coords) - 1, 3):  # draw the snakes tail
            pygame.draw.ellipse(window, coords[c + 2], (coords[c], coords[c + 1], 10, 10))

        pygame.draw.rect(window, foodColour, (food))  # draw the food
        clock.tick(30)
        pygame.display.update()  # like refresh it updates the screen with whats been drawn

        # This MUST be outside the event loop otherwise it needs mouse movement to work
        keyPressed = pygame.key.get_pressed()  # variable for when a key is held down

        # collision with itself detection
        if len(coords) > 3:
            hit = hitDetect(coords, keyPressed, direction)
            if hit == True:
                return length
                break

        # collision with sides detection
        if x != 0 and x != 1290 and y != 0 and y != 790:
            if keyPressed[pygame.K_DOWN]:  # if the press the down button
                if len(coords) > 3 and keyPressed:  # if there's a snake tail
                    coords = coordChange(coords)  # change the tail coords
                direction = "down"
                coords = down(coords)

            elif keyPressed[pygame.K_UP]:  # if the press the up button
                if len(coords) > 3 and keyPressed:  # if there's a snake tail
                    coords = coordChange(coords)  # change the tail coords
                direction = "up"
                coords = up(coords)  # change snake head coords

            elif keyPressed[pygame.K_LEFT]:  # if they press the left button
                if len(coords) > 3 and keyPressed:  # if there's a snake tail
                    coords = coordChange(coords)  # change the tail coords
                direction = "left"
                coords = left(coords)

            elif keyPressed[pygame.K_RIGHT]:  # if they press the right button
                if len(coords) > 3 and keyPressed:  # if there's a snake tail
                    coords = coordChange(coords)  # change the tail coords
                direction = "right"
                coords = right(coords)

            elif "1" not in keyPressed:  # the palyer isn't pressing a key
                if len(coords) > 3 and keyPressed:  # if there's a snake tail
                    coords = coordChange(coords)  # change the tail coords
                if direction == "up":
                    coords = up(coords)
                elif direction == "down":
                    coords = down(coords)
                elif direction == "left":
                    coords = left(coords)
                elif direction == "right":
                    coords = right(coords)

            # if the snake head is within 10 pixels of the food on any side
            if coords[0] in range(food[0] - 10, food[0] + 10):
                if coords[1] in range(food[1] - 10, food[1] + 10):
                    coords = grow(keyPressed, coords, foodColour)  # add new tail length
                    foodColour = colours[random.randint(0, 6)]  # rng'd colour of the new food
                    food = (random.randint(10, 1290), random.randint(10, 790), 10, 10)  # rng'd co-ords for the new food
                    length += 1  # add to the player's score

        else:  # when collision occurs
            return length
            break


def end():
    '''
    fonts: swiss721extended, swiss721extended, swiss721blackcondensed, swiss721black
    If they hit the sides or themselves then the game over loop runs
    :return: No return
    '''
    while True:  # infinite loop or until person hits quit
        for event in pygame.event.get():  # looks for user input to cancel game
            if event.type == pygame.QUIT:  # QUIT is a pygame action that is the cancel button on the screen
                sys.exit()  # exits if the user say

        pygame.init()  # intialize fonts

        # create the GAME OVER text
        gameOver = ("GAME OVER")  # my txt
        gameOverFont = pygame.font.SysFont("swiss721extended", 45, bold=True)  # font name, font size, bolded
        gameOverText = gameOverFont.render(gameOver, 1, (black))  # actually creates the text

        # create the score text
        score = ("Score: " + str(length))  # player's score
        playerScoreFont = pygame.font.SysFont("swiss721extended", 35, bold=True)  # font name, font size, bolded
        playerScoreText = playerScoreFont.render(score, 1, (black))
        window.blit(gameOverText, (490, 330))  # prints the text at these coords
        window.blit(playerScoreText, (560, 380))
        pygame.display.update()  # update the screen with the new text


length = main(length)  # run the main game loop
window.fill(white)  # get rid of the snake on the screen
pygame.display.update()  # refresh
end()  # GAME OVER
