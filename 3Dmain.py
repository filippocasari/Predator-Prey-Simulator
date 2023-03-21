import matplotlib.pyplot as plt
import numpy as np
from Wolf3D import Wolf
from Rabbit3D import Rabbit
import random
import math
import time
import json
import os
L = int(input("Insert value for L: "))
name_plot = input("Insert name for plot according with the assignment point: ")
PERC_WOLVES = 0.01
PERC_RABBITS = 0.09
L2 = L**2
# N_R = int(L2*PERC_RABBITS)
# N_W = int(L2*PERC_WOLVES)

list_wolves = []
list_rabbits = []
with open('params3D.json', 'r') as f:
    # Load the contents of the file into a dictionary
    params = json.load(f)

N_R = params['N_R']
N_W = params['N_W']
R_C = params['R_C']
P_E_W = params['P_E_W']
P_R_W = params['P_R_W']
P_R_R = params['P_R_R']
T_D_R = params['T_D_R']
T_D_W = params['T_D_W']
mu = params['mu']
sigma = params['sigma']
move_when_eat = params['move_when_eat']
print("MOVE THE WOLF IF IT EATS: ", move_when_eat)
del params
print(f"Number of wolves: {N_W}\n")
print(f"Number of rabbits: {N_R}\n")
N_X = int(L/R_C)
N_Y = int(L/R_C)
N_Z = int(L/R_C)
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)
ax.set_xlim([0, L])
ax.set_ylim([0, L])
ax.set_zlim([0, L])
scatter_wolves = ax.scatter([w.x for w in list_wolves], [
    w.y for w in list_wolves], [
    w.z for w in list_wolves], c='red')
scatter_rabbits = ax.scatter([r.x for r in list_rabbits], [
    r.y for r in list_rabbits], [r.z for r in list_rabbits], c='green')
fig.canvas.draw()
fig.canvas.flush_events()
plt.pause(4)

start = time.time()

list_num_wolves = []
list_num_rabbits = []
for i in range(N_W):
    x = random.random() * L
    z = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    z_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_wolves.append(Wolf(x, y, z, x_cell, y_cell, z_cell, R_C))
for i in range(N_R):
    x = random.random() * L
    z = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    z_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_rabbits.append(Rabbit(x, y, z, x_cell, y_cell, z_cell, T_D_R, R_C))


for iter in range(1000):

    if (N_W < 1 or N_R < 1):
        break

    # past_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]

    index = -1
    for wolf in list_wolves.copy():
        index += 1
        if (wolf.not_eaten_iter >= T_D_W):
            list_wolves.remove(wolf)
            N_W = N_W - 1
            index -= 1
            continue

        else:
            list_wolves[index].not_eaten_iter += 1

        step_len = np.random.normal(mu, sigma, 3)
        direction = np.random.randn(3)
        direction /= np.linalg.norm(direction)
        step_len = step_len*direction

        dx = step_len[0]
        dy = step_len[1]
        dz = step_len[2]
        list_wolves[index].move(dx, dy, dz, L)

    # new_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]
    # print(f"past values: {past_value}")
    # print(f"new value {new_value}")
    add_rabbits = []
    index = -1
    for rabbit in list_rabbits.copy():
        index += 1
        step_len = np.random.normal(mu, sigma, 3)
        direction = np.random.randn(3)
        direction /= np.linalg.norm(direction)
        step_len = step_len*direction

        dx = step_len[0]
        dy = step_len[1]
        dz = step_len[2]
        list_rabbits[index].move(dx, dy, dz, L)

        if (rabbit.life_steps >= T_D_R):
            list_rabbits.remove(rabbit)

            index -= 1

        else:
            if (random.random() <= P_R_R):
                new_rabbit = Rabbit(rabbit.x, rabbit.y, rabbit.z,
                                    rabbit.i, rabbit.j, rabbit.k, T_D_R, R_C)
                add_rabbits.append(new_rabbit)

    list_rabbits.extend(add_rabbits)
    # list_num_rabbits.append(N_R)
    added_wolves = []
    # list_wolves=np.array(list_wolves)
    to_remove = []
    for wolf in list_wolves:
        # already_eaten = False
        i = wolf.i
        j = wolf.j
        k = wolf.k
        # x, y, z = wolf.x, wolf.y, wolf.z

        for ii in range(i-1, i+1):

            for jj in range(j-1, j+1):
                for kk in range(k-1, k+1):
                    nearby_rabbits = [r for r in list_rabbits if r.i == ii %
                                      N_X and r.j == jj % N_Y and r.k == kk % N_Z and r not in to_remove]
                    # print(f"Nearby rabbits: {nearby_rabbits}")

                    for rabbit in nearby_rabbits:
                        d_x = x-rabbit.x
                        if (d_x > L/2):
                            d_x = d_x-L
                        elif (d_x <= -L/2):
                            d_x = d_x+L
                        d_y = y-rabbit.y
                        if (d_y > L/2):
                            d_y = d_y-L
                        if (d_y <= -L/2):
                            d_y = d_y+L
                        d_z = z-rabbit.z
                        if (d_z > L/2):
                            d_z = d_z-L
                        if (d_z <= -L/2):
                            d_z = d_z+L
                        d = math.sqrt(d_x**2 + d_y**2 + d_z**2)
                        if (d <= R_C):

                            if (random.random() <= P_E_W):
                                to_remove.append(rabbit)
                                list_rabbits.remove(rabbit)
                                wolf.eat()

                                if (random.random() <= P_R_W):
                                    new_wolf = Wolf(
                                        wolf.x, wolf.y, wolf.z, wolf.i, wolf.j, wolf.k, R_C)

                                    added_wolves.append(new_wolf)

    list_wolves.extend(added_wolves)
    # list_num_wolves.append(N_W)
    # for rabbit in to_remove:
    #    list_rabbits.remove(rabbit)
    # list_num_wolves.append(N_W)

    # list_num_rabbits.append(N_R)

    ax.clear()
    scatter_wolves = ax.scatter([w.x for w in list_wolves], [
                                w.y for w in list_wolves], [
                                w.z for w in list_wolves], c='red')
    scatter_rabbits = ax.scatter([r.x for r in list_rabbits], [
                                 r.y for r in list_rabbits], [r.z for r in list_rabbits], c='green')
    plt.grid(True)
    ax.set_xlim([0, L])
    ax.set_ylim([0, L])
    ax.set_zlim([0, L])

    plt.grid(True)
    ax2.set_xlim([0, 1000])
    ax2.plot(list_num_wolves, c='red')
    ax2.plot(list_num_rabbits, c='green')
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.00001)

    # ax.set_yticks(list(range(0,L, int(R_C))))
    # ax.set_xticks(list(range(0,L, int(R_C))))
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(R_C))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(R_C))

    N_W = len(list_wolves)
    N_R = len(list_rabbits)
    list_num_rabbits.append(N_R)
    list_num_wolves.append(N_W)
print("Simulation time: ", time.time()-start)
print("Iterations: ", max(len(list_num_rabbits), len(list_num_wolves)))
fig2, ax2 = plt.subplots()
ax2.plot(list_num_wolves, label="Wolves", c='r')
ax2.plot(list_num_rabbits, label="Rabbits", c='b')
plt.legend()
ax2.set_title("Number of wolves and rabbits over time")
ax2.set_xlabel("Iterations")
ax2.grid(True)
if (name_plot != None and os.path.exists("output3D")):
    fig2.savefig("output3D/"+name_plot+"_first.png")

plt.show()
fig3, ax3 = plt.subplots()
minimum = min(len(list_num_wolves), len(list_num_rabbits))

ax3.scatter(list_num_wolves[0], list_num_rabbits[0],
            c='r', label="Starting point")
ax3.plot(list_num_wolves[:minimum], list_num_rabbits[:minimum], c='r')
ax3.scatter(list_num_wolves[minimum-1],
            list_num_rabbits[minimum-1], c='b', label="End point")
ax3.legend()
ax3.set_title("Number of wolves vs number of rabbits")
ax3.set_ylabel("number of rabbits")
ax3.set_xlabel("Number of wolves")
ax3.grid(True)
if (name_plot != None and os.path.exists("output3D")):
    fig3.savefig("output3D/"+name_plot+"second.png")
plt.show()
