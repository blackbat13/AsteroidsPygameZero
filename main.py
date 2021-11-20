import pgzrun
import random
import pygame
import shelve

WIDTH = 600
HEIGHT = 900

statek = Actor("statek")
statek.x = WIDTH / 2
statek.y = HEIGHT - 60
statek.px = 5
statek.zycia = 3
statek.strzaly = 1
statek.punkty = 0

meteory = []

lasery = []

zycia = []

wyniki = shelve.open("wyniki")
if "highscore" not in wyniki:
    wyniki["highscore"] = 0
wyniki.close()

def draw():
    screen.blit("tlo", (0, 0))
    draw_meteory()
    draw_lasery()
    statek.draw()
    draw_punkty()
    draw_zycia()

    if statek.zycia == 0:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2), fontsize=90)

        wyniki = shelve.open("wyniki")
        highscore = wyniki["highscore"]
        wyniki.close()

        screen.draw.text("Best: " + str(highscore), center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize = 90, color="yellow")


def draw_punkty():
    screen.draw.text(str(statek.punkty), center=(WIDTH / 2, 20), fontsize=50, color="yellow")


def draw_zycia():
    for st in zycia:
        st.draw()


def draw_meteory():
    for met in meteory:
        met.draw()


def draw_lasery():
    for las in lasery:
        las.draw()


def update():
    if statek.zycia == 0:
        return

    mysz_x, mysz_y = pygame.mouse.get_pos()
    if mysz_x < statek.x:
        statek.x -= statek.px
    if mysz_x > statek.x:
        statek.x += statek.px

    if random.randint(0, 250) <= 1:
        dodaj_meteor()

    update_meteory()
    update_lasery()
    update_trafienia()


def update_meteory():
    for met in meteory[:]:
        met.y += met.py
        met.angle += met.pa
        if met.y > HEIGHT + 50:
            meteory.remove(met)

        if met.colliderect(statek):
            statek.zycia -= 1
            zycia.pop()
            meteory.remove(met)
            if statek.zycia > 0:
                sounds.tarcza.play()
            else:
                sounds.eksplozja.play()
                sounds.game_over.play()
                music.fadeout(1)

                wyniki = shelve.open("wyniki")
                if statek.punkty > wyniki["highscore"]:
                    wyniki["highscore"] = statek.punkty
                wyniki.close()


def update_lasery():
    for las in lasery[:]:
        las.y += las.py

        if las.y < -las.height:
            lasery.remove(las)


def update_trafienia():
    for las in lasery[:]:
        for met in meteory[:]:
            if las.colliderect(met):
                lasery.remove(las)
                meteory.remove(met)
                statek.punkty += 10
                sounds.trafienie.play()
                break


def on_mouse_down():
    if statek.strzaly > 0:
        dodaj_laser()
        statek.strzaly -= 1
        clock.schedule(dodaj_strzal, 1)
        sounds.laser.play()


def dodaj_laser():
    laser = Actor("laser")
    laser.x = statek.x
    laser.y = statek.y
    laser.py = -8
    lasery.append(laser)


def dodaj_meteor():
    grafika = random.choice(["meteor1", "meteor2", "meteor3", "meteor4"])
    met = Actor(grafika)
    met.x = random.randint(20, WIDTH - 20)
    met.y = -10
    met.py = random.randint(2, 10)
    met.pa = random.randint(-5, 5)
    meteory.append(met)


def dodaj_strzal():
    statek.strzaly += 1


def utworz_zycia():
    for i in range(statek.zycia):
        st = Actor("zycie")
        st.x = st.width / 2 + i * st.width
        st.y = st.height / 2
        zycia.append(st)


pygame.mouse.set_visible(False)
utworz_zycia()

music.play("space")
music.set_volume(0.3)

pgzrun.go()
