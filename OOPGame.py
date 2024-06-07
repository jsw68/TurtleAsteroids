import turtle
import random
import time
from CheckArea import PolygonArea, PolygonSort
import os
# my second attempt at making Asteroids, this time, OOP style

# setup stuff
screen = turtle.Screen()
screen.tracer(0)
screen.bgcolor('black')
turtle.setundobuffer(1)
turtle.ht()
print()
explosion_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Sounds and Images', 'Explosion2.gif'))
screen.setworldcoordinates(-300, -300, 300, 300)
# makes window fullscreen
screen.setup(width=1.0, height=1.0)
screen.setworldcoordinates(-300, -300, 300, 300)


def draw_black_border():
    # draws a white border around the screen
    draw_border('white', border)


def random_asteroid(asteroid_name):
    # creates random dimensions for the all_asteroids, right now they are 4 sided, anything more sounds much more
    # difficult PolygonArea and PolygonSort are both functions that I found online, they are not essential though,
    # they just reduce the amount of weird/small shapes
    area = 0
    while area < 275:
        x_coords = []
        y_coords = []
        x_coord, y_coord = 0, 0
        # 4 sided rectangle
        for _ in range(4):
            while x_coord == y_coord or x_coord in x_coords or y_coord in y_coords:
                # negative and postive x coordinates that way it looks like a square
                if _ <= 1:
                    x_coord = abs((random.randint(10, 17)))
                else:
                    x_coord = abs((random.randint(10, 17))) * -1
                if _ == 1 or _ == 3:
                    y_coord = abs(random.randint(10, 17))
                else:
                    y_coord = abs(random.randint(10, 17)) * -1
            x_coords.append(x_coord)
            y_coords.append(y_coord)
        coords = [(x_coords[i], y_coords[i]) for i in range(4)]
        # make sure it is of a certain area
        coords = PolygonSort(coords)
        area = PolygonArea(coords)
        # register shape
    screen.register_shape(asteroid_name, (coords[0], coords[1], coords[2], coords[3]))


def set_shapes():
    # registers the three shapes I use, maybe I will incorporate a fancier background
    screen.register_shape(explosion_path)
    screen.register_shape("ship", ((8, -3), (0, 20), (-8, -3)))
    screen.register_shape('bullet', ((0, -8), (-4, -8), (-4, 0), (0, 0)))


def collision_check(turt1, turt2):
    # checks distances between turtles to see if they ahve collided, not perfect, but it works pretty well
    if (turt1.xcor() >= (turt2.xcor() - 14)) and \
            (turt1.xcor() <= (turt2.xcor() + 14)) and \
            (turt1.ycor() >= (turt2.ycor() - 14)) and \
            (turt1.ycor() <= (turt2.ycor() + 14)) and not turt2.shielded:
        return True


def fire():
    # if there are bullets left
    if len(bullets):
        # bullet heading and position is the same as ship, then remove from the list and update text
        bullets[0].setposition(s.position())
        bullets[0].setheading(s.heading())
        bullets[0].st()
        shot.append(bullets[0])
        bullets.remove(bullets[0])
        text = 'Lives: %s Score: %s Ammo: %s' % (s.lives, s.score, len(bullets))
        write(writer, text)


def reset_asteroid(asteroid):
    # this removes asteroids from the game, so when you shoot them they dont respawn immediately
    asteroid.ht()
    asteroids.remove(asteroid)
    asteroid.setposition(20000, 20000)
    # asteroids get faster as the game progresses
    asteroid.speed += 0.2
    # after 5 seconds, the asteroid comes back
    screen.ontimer(asteroid.reset_pos, 5000)
    screen.ontimer(asteroid.return_to_asteroids, 5001)


def write(turt, msg):
    # this function writes the text in the top left corner
    turt.reset()
    turt.speed(0)
    turt.ht()
    turt.penup()
    turt.goto(-295, 275)
    turt.color('white')
    turt.write(msg, font=("Arial", 16, "normal"), align='left')


def draw_border(color, turt):
    # draws a border a certain color
    turt.setposition(-300, 300)
    turt.seth(0)
    turt.pendown()
    turt.pencolor(color)
    for _ in range(4):
        turt.fd(595)
        turt.rt(90)


def start_game():
    global game_started
    game_started = True


class Ship(turtle.Turtle):
    # my ship/player class
    def __init__(self):
        # inherits from turtle.Turtle, allows me to use turtle methods from self
        super().__init__(shape='ship')
        self.color('red')
        self.penup()
        self.ammo = 5
        self.score = 0
        self.shot = []
        self.lives = 3
        self.speed = 15
        self.shielded = False
        self.base_acceleration = 0.3

    def move_forward(self):
        if self.in_bounds_check():
            self.fd(self.speed)

    def rotate_right(self):
        if self.in_bounds_check():
            self.rt(self.speed)

    def rotate_left(self):
        if self.in_bounds_check():
            self.lt(self.speed)

    def move_backward(self):
        if self.in_bounds_check():
            self.backward(self.speed)

    def move_gravity(self):
        # zero-gravity does not work right now
        if self.in_bounds_check():
            self.fd(self.base_acceleration)

    def remove_shield(self):
        # allows ship to be hit again
        self.shielded = False

    def in_bounds_check(self):
        # wrapping borders
        if self.xcor() < -285:
            self.setx(283)
            return False
        elif self.xcor() > 285:
            self.setx(-283)
            return False
        if self.ycor() < -285:
            self.sety(283)
            return False
        elif self.ycor() > 285:
            self.sety(-283)
            return False
        return True


class Asteroid(turtle.Turtle):
    def __init__(self):
        # inherts from turtle.Turtle
        random_asteroid(self)
        super().__init__(shape=self)
        self.penup()
        self.ht()
        self.speed = 0.7
        self.reset_pos()
        self.color('white')

    def reset_pos(self):
        # gives asteroids a random location along the edge, makes sure it is not too close to the ship
        while True:
            if random.choice([True, False]):
                self.setposition((random.choice([-300, 300]), random.randint(-300, 300)))
            else:
                self.setposition((random.randint(-300, 300), random.choice([-300, 300])))
            self.setheading(self.towards(s.position()) + random.randint(-16, 16))
            if self.distance(s) > 20:
                break
        self.st()

    def return_to_asteroids(self):
        # returns the asteroid to the list of asteroids
        asteroids.append(self)

    def move(self):
        # checks if it is in-bounds, if not, it is reset, otherwise it moves
        self.st()
        if abs(self.position()[0]) > 300 or abs(self.position()[1]) > 300:
            # if the asteroid just goes out of bounds as opposed to shot, it does not stay away for 5 seconds,
            # and its speed is not increased
            self.reset_pos()
        self.fd(self.speed)


class Explosion(turtle.Turtle):
    def __init__(self):
        super().__init__(shape=explosion_path)
        self.ht()
        self.penup()

    def goto_collision(self, coord):
        # goes to the site of the explosion
        self.setposition(coord)
        self.st()


class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='bullet')
        self.ht()
        self.penup()
        self.speed = 1
        self.color('green')
        self.shielded = False

    def move(self):
        # if it is out of bounds
        if abs(self.position()[0]) > 300 or abs(self.position()[1]) > 300:
            # return to ammo
            shot.remove(self)
            bullets.append(self)
            self.ht()
            # update text on the top
            text = 'Lives: %s Score: %s Ammo: %s' % (s.lives, s.score, len(bullets))
            write(writer, text)
        else:
            # otherwise, move forward
            self.fd(self.speed)


# create all the objects I will need
writer = turtle.Turtle()
set_shapes()
s = Ship()
border = turtle.Turtle()
border.penup()
border.ht()
border.pensize(5)
draw_black_border()
asteroids = []
shot = []

e = Explosion()
bullets = []
game_started = False
for i in range(5):
    bullet = Bullet()
    bullets.append(bullet)
text = 'Lives: %s Score: %s Ammo: %s' % (s.lives, s.score, len(bullets))
write(writer, text)
# set keybindings, right now it is wasd, but it could use arrows


writer.goto(-50, 0)
writer.write('Welcome to Asteroids!', font=("Arial", 16, "normal"), align='left')
time.sleep(1.5)
writer.reset()
number_of_asteroids = screen.numinput('Asteroids', 'How many asteroids do you want to play with?', minval=3, maxval=100)
for _ in range(int(number_of_asteroids)):
    a = Asteroid()
    asteroids.append(a)
# game loop
screen.onkeypress(s.move_forward, 'w')
screen.onkeypress(s.move_backward, 's')
screen.onkeypress(s.rotate_left, 'a')
screen.onkeypress(s.rotate_right, 'd')
screen.onkeypress(screen.bye, 'q')
screen.onkeypress(fire, 'space')
screen.listen()
while True:
    # update screen
    screen.update()
    # move all asteroids and bullets
    for asteroid in asteroids:
        asteroid.move()
    for bullet in shot:
        bullet.move()
    # s.move_gravity()
    for asteroid in asteroids:
        for bullet in shot:
            # check for collisions between bullets and asteroids
            if collision_check(asteroid, bullet):
                # if they collided, set the explosion
                e.goto_collision(asteroid.position())
                # add 10 to the score
                s.score += 10
                # hide the explosion after 1 second
                screen.ontimer(e.ht, 1000)
                # reset the asteroid
                reset_asteroid(asteroid)
                # update the text
                text = 'Lives: %s Score: %s Ammo: %s' % (s.lives, s.score, len(bullets))
                write(writer, text)
    for asteroid in asteroids:
        if collision_check(asteroid, s):
            # collision check between ship and asteroid
            # draw a red border so the player knows they are hit
            draw_border('red', border)
            # return to a black border after 1 second
            screen.ontimer(draw_black_border, 1000)
            # remove a life and give them a shield for one second
            s.lives -= 1
            s.shielded = True
            screen.ontimer(s.remove_shield, 1000)
            # reset the asteroid and update the text
            reset_asteroid(asteroid)
            text = 'Lives: %s Score: %s Ammo: %s' % (s.lives, s.score, len(bullets))
            write(writer, text)
        if s.lives <= 0:
            # if player loses, tell them and exit. Asking to play again is more difficult than expected.
            '''msg = ''
            while True:
                again = screen.textinput('Play again', f'{msg}Do you want to play again? (y/n)').lower()
                if again == 'y':
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                elif again == 'n':
                    screen.bye()
                else:
                    msg = 'Please enter either y or n. '''
            writer.write('You lose!', font=("Arial", 16, "normal"), align='left')
            time.sleep(1)
            screen.bye()
