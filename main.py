import random

import pgzrun
import pygame
from pgzhelper import *


"""CONFIGURATION"""

WIDTH = 600
HEIGHT = 900

"""VARIABLES"""

ship = Actor("ship")
ship.x = WIDTH / 2
ship.y = HEIGHT - 60
ship.vx = 5
ship.points = 0
ship.lifes = 3
ship.ammunition = 5

asteroids_list = []
lasers_list = []


"""DRAW"""


def draw():
    screen.blit("bg", (0, 0))
    for asteroid in asteroids_list:
        asteroid.draw()

    for laser in lasers_list:
        laser.draw()

    ship.draw()
    screen.draw.text(str(ship.points), center=(
        WIDTH / 2, 20), fontsize=50, color="yellow")
    draw_lifes()
    if ship.lifes <= 0:
        screen.draw.text("GAME OVER", center=(
            WIDTH / 2, HEIGHT / 2), fontsize=90, color="yellow")


def draw_lifes():
    for life_id in range(1, ship.lifes + 1):
        life = Actor("life")
        life.x = life_id * life.width
        life.y = life.height / 2
        life.draw()


"""UPDATE"""


def update():
    if ship.lifes <= 0:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < ship.x:
        ship.x -= ship.vx

    if mouse_x > ship.x:
        ship.x += ship.vx

    if random.random() < 0.02:
        add_asteroid()

    update_asteroids()
    update_lasers()
    update_lasers_hits()


def update_asteroids():
    for asteroid in asteroids_list[:]:
        asteroid.y += asteroid.vy
        if asteroid.y > HEIGHT + 50:
            asteroids_list.remove(asteroid)
        elif asteroid.collide_pixel(ship):
            ship.lifes -= 1
            asteroids_list.remove(asteroid)
            if ship.lifes > 0:
                sounds.shield.play()
            else:
                sounds.explosion.play()


def update_lasers():
    for laser in lasers_list[:]:
        laser.y += laser.vy
        if laser.y < -laser.height:
            lasers_list.remove(laser)


def update_lasers_hits():
    for laser in lasers_list[:]:
        for asteroid in asteroids_list[:]:
            if laser.collide_pixel(asteroid):
                lasers_list.remove(laser)
                asteroids_list.remove(asteroid)
                ship.points += 1
                break


"""HELPERS"""


def add_asteroid():
    image_id = random.randint(1, 4)
    asteroid = Actor("asteroid" + str(image_id))
    asteroid.x = random.randint(20, WIDTH-20)
    asteroid.y = -10
    asteroid.vy = random.randint(2, 10)
    asteroid.scale = random.uniform(0.5, 1.5)
    asteroid.angle = random.randint(0, 360)
    asteroids_list.append(asteroid)


def add_laser():
    laser = Actor("laser")
    laser.pos = ship.pos
    laser.vy = -8
    lasers_list.append(laser)


def regenerate_ammo():
    ship.ammunition += 1


"""EVENTS"""


def on_mouse_down(pos):
    if ship.ammunition <= 0:
        return

    add_laser()
    sounds.laser.play()
    ship.ammunition -= 1
    clock.schedule(regenerate_ammo, 1)


"""INITIALIZATION"""

pygame.mouse.set_visible(False)

music.play("space")
music.set_volume(0.3)

pgzrun.go()
