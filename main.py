import pgzrun
import random
import pygame


""" CONFIGURATION """

WIDTH = 600
HEIGHT = 900

""" VARIABLES """

player = Actor("ship")
player.x = WIDTH / 2
player.y = HEIGHT - 60
player.vx = 5
player.lifes = 3
player.ammo = 1
player.points = 0

meteors_list = []

lasers_list = []

lifes_list = []


""" DRAW """


def draw():
    screen.blit("bg", (0, 0))

    draw_actors_list(meteors_list)
    draw_actors_list(lasers_list)
    draw_actors_list(lifes_list)

    player.draw()

    screen.draw.text(str(player.points), center=(
        WIDTH / 2, 20), fontsize=50, color="yellow")

    if player.lifes == 0:
        screen.draw.text("Game Over", center=(
            WIDTH / 2, HEIGHT / 2), fontsize=90)


def draw_actors_list(actors_list):
    for actor in actors_list:
        actor.draw()


""" UPDATE """


def update():
    if player.lifes == 0:
        return

    if random.randint(0, 250) <= 1:
        add_meteor()

    update_player()
    update_meteors()
    update_lasers()
    update_hits()


def update_player():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_x < player.x:
        player.x -= player.vx

    if mouse_x > player.x:
        player.x += player.vx


def update_meteors():
    for meteor in meteors_list[:]:
        meteor.y += meteor.vy
        meteor.angle += meteor.va

        if meteor.y > HEIGHT + 50:
            meteors_list.remove(meteor)

        if meteor.colliderect(player):
            player.lifes -= 1
            lifes_list.pop()
            meteors_list.remove(meteor)
            if player.lifes > 0:
                sounds.shield.play()
            else:
                sounds.explosion.play()
                sounds.game_over.play()
                music.fadeout(1)


def update_lasers():
    for laser in lasers_list[:]:
        laser.y += laser.vy

        if laser.y < -laser.height:
            lasers_list.remove(laser)


def update_hits():
    for laser in lasers_list[:]:
        for meteor in meteors_list[:]:
            if laser.colliderect(meteor):
                lasers_list.remove(laser)
                meteors_list.remove(meteor)
                player.points += 10
                sounds.hit.play()
                return


""" EVENTS """


def on_mouse_down():
    if player.ammo > 0:
        add_laser()
        player.ammo -= 1
        clock.schedule(add_ammo, 1)
        sounds.laser.play()


""" HELPERS """


def add_laser():
    laser = Actor("laser")
    laser.x = player.x
    laser.y = player.y
    laser.vy = -8
    lasers_list.append(laser)


def add_meteor():
    image = random.choice(["meteor1", "meteor2", "meteor3", "meteor4"])
    meteor = Actor(image)
    meteor.x = random.randint(20, WIDTH - 20)
    meteor.y = -10
    meteor.vy = random.randint(2, 10)
    meteor.va = random.randint(-5, 5)
    meteors_list.append(meteor)


def add_ammo():
    player.ammo += 1


""" INITIALIZATION """


def init_lifes():
    for i in range(player.lifes):
        life = Actor("life")
        life.x = life.width / 2 + i * life.width
        life.y = life.height / 2
        lifes_list.append(life)


pygame.mouse.set_visible(False)
init_lifes()

music.play("space")
music.set_volume(0.3)

pgzrun.go()
