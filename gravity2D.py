import math
import os
import random
import sys
import time
from math import sqrt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


initial_objects = 150  # Number of initial objects in the simulation
object_list = []
G = 6.67408e-11  # Gravitational constant
time_step = 50000  # How much time has passed between every calculation - (lower more accurate)
frame_rate = 60  # time passed in sim = current time * time_step * frame_rate
minimum_interaction_radius = 50  # A minium gravitiational influence radius to reduce inaccurate integral values
collision_radius = 2  # Distance from object where collision occurs
max_v = 100  # A maximum velocity for objects to minimise inaccurate integrals of velocity
start_time = time.time()


pygame.init()
display = pygame.display.set_mode((1250, 700))
display.fill(pygame.Color("white"))
clock = pygame.time.Clock()


class MassObject:
    def __init__(self, mass, x_pos, y_pos, x_vel, y_vel):
        self.mass = mass
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_vel
        self.y_velocity = y_vel


def main():
    setup(object_list)
    step = 1
    while True:
        pygame.display.set_caption(
            'Gravity Simulation: Step {}  SimulationTime(s): {} RealTime: {}  Objects: {}'.format(str(step), round(
                round(time.time() - start_time, 2) * time_step * frame_rate, 2), round(time.time() - start_time, 2),
                                                                                                  len(object_list)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display.fill(pygame.Color("white"))
        step += 1
        update_pos(object_list)
        check_collisions(object_list)
        draw(object_list)


def setup(object_list):
    for i in range(initial_objects):
        object_list.append(
            MassObject(random.randrange(1, 100), random.randrange(1, 1250), random.randrange(1, 700), 0, 0))


def add_force(object):
    x_acc = y_acc = 0.0
    for other in object_list:
        if sqrt((other.x_pos - object.x_pos) ** 2 + (other.y_pos - object.y_pos) ** 2) > minimum_interaction_radius:
            if other != object and object.x_pos - other.x_pos != 0:
                r = ((other.x_pos - object.x_pos) ** 2) + ((other.y_pos - object.y_pos) ** 2)
                fg = G * object.mass * other.mass / r
                angle = math.atan2((other.y_pos - object.y_pos), (other.x_pos - object.x_pos))
                x_acc += fg * math.cos(angle) / object.mass
                y_acc += fg * math.sin(angle) / object.mass
    return x_acc, y_acc


def update_pos(object_list):
    for object in object_list:
        x_acc, y_acc = add_force(object)
        if max_v > object.x_velocity + (x_acc * time_step) > -max_v:
            object.x_velocity += x_acc * time_step
        elif object.x_velocity + (x_acc * time_step) > max_v:
            object.x_velocity = max_v
        elif object.x_velocity + (x_acc * time_step) < -max_v:
            object.x_velocity = -max_v
        if max_v > object.y_velocity + (y_acc * time_step) > -max_v:
            object.y_velocity += y_acc * time_step
        elif object.y_velocity + (y_acc * time_step) > max_v:
            object.y_velocity = max_v
        elif object.y_velocity + (y_acc * time_step) < -max_v:
            object.y_velocity = -max_v
        object.x_pos += object.x_velocity * time_step
        object.y_pos += object.y_velocity * time_step


def check_collisions(object_list):
    for object in object_list:
        for other in object_list:
            if (object != other) and (collision_radius > other.x_pos - object.x_pos > -collision_radius) and (collision_radius > other.y_pos - object.y_pos > -collision_radius):
                object.x_velocity = (object.x_velocity * object.mass + other.x_velocity * other.mass) / (object.mass + other.mass)
                object.y_velocity = (object.y_velocity * object.mass + other.y_velocity * other.mass) / (object.mass + other.mass)
                object.mass += other.mass
                object_list.remove(other)


def draw(object_list):
    for object in object_list:
        r = 255 // int(object.mass)
        g = int(object.mass) if int(object.mass) < 255 else 255
        b = int(object.mass) if int(object.mass) < 255 else 255
        pygame.draw.circle(display, (r, g, b), (int(object.x_pos), int(object.y_pos)), 2, 0)
        #pygame.draw.circle(display, (255, 255, 255), (int(object.x_pos), int(object.y_pos)), 2, 0)
    pygame.display.update()
    clock.tick(frame_rate)


main()
