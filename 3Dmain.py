import matplotlib.pyplot as plt
import numpy as np
from Wolf3D import Wolf
from Rabbit3D import Rabbit
import random
import math
import time
import json
from mpl_toolkits.mplot3d import Axes3D
L = int(input("Insert value for L: "))
name_plot = input("Insert name for plot according with the assignment point: ")
PERC_WOLVES = 0.01
PERC_RABBITS = 0.09
L2 = L**2
# N_R = int(L2*PERC_RABBITS)
# N_W = int(L2*PERC_WOLVES)

list_wolves = {}
list_rabbits = {}
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
del params
print(f"Number of wolves: {N_W}\n")
print(f"Number of rabbits: {N_R}\n")
N_X = int(L/R_C)
N_Y = int(L/R_C)
N_Z = int(L/R_C)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([0, L])
ax.set_ylim([0, L])
ax.set_zlim([0, L])
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
    list_wolves[i] = Wolf(x, y, z, x_cell, y_cell, z_cell, R_C)
for i in range(N_R):
    x = random.random() * L
    z = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    z_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_rabbits[i] = Rabbit(x, y, z, x_cell, y_cell, z_cell, T_D_R, R_C)


for iter in range(1000):

    if (N_W < 1 or N_R < 1):
        break

    # past_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]

    for key, wolf in list(list_wolves.items()):
        if (wolf.not_eaten_iter >= T_D_W):
            del list_wolves[key]
            N_W = N_W - 1

        else:
            wolf.not_eaten_iter += 1
        step_len = np.random.normal(mu, sigma)
        step_len = np.random.normal(mu, sigma, 3)
        direction = np.random.randn(3)
        direction /= np.linalg.norm(direction)
        step_len = step_len*direction

        dx = step_len[0]
        dy = step_len[1]
        dz = step_len[2]
        wolf.move(dx, dy, dz, L)

    # new_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]
    # print(f"past values: {past_value}")
    # print(f"new value {new_value}")
    add_rabbits = {}
    for key, rabbit in list(list_rabbits.items()):
        step_len = np.random.normal(mu, sigma, 3)
        direction = np.random.randn(3)
        direction /= np.linalg.norm(direction)
        step_len = step_len*direction

        dx = step_len[0]
        dy = step_len[1]
        dz = step_len[2]
        rabbit.move(dx, dy, dz, L)

        if (rabbit.life_steps >= T_D_R):
            del list_rabbits[key]
            N_R = N_R - 1

        else:
            if (random.random() < P_R_R):
                new_rabbit = Rabbit(rabbit.x, rabbit.y, rabbit.z,
                                    rabbit.i, rabbit.j, rabbit.k, T_D_R, R_C)
                add_rabbits[N_R] = new_rabbit
                N_R = N_R + 1

    list_rabbits.update(add_rabbits)
    # list_num_rabbits.append(N_R)
    added_wolves = {}
    # list_wolves=np.array(list_wolves)
    to_remove = {}
    for k_w, wolf in list(list_wolves.items()):
        already_eaten = False
        i = wolf.i
        j = wolf.j
        k = wolf.k
        x, y, z = wolf.x, wolf.y, wolf.z

        for ii in range(i-1, i+1):
            if (already_eaten):
                break
            for jj in range(j-1, j+1):
                if (already_eaten):
                    break
                for kk in range(k-1, k+1):
                    nearby_rabbits = {r.i: r for r in list_rabbits.values(
                    ) if r.k == kk % N_Z and r.i == ii % N_X and r.j == jj % N_Y}

                    # print(f"Nearby rabbits: {nearby_rabbits}")

                    for k_r, rabbit in list(nearby_rabbits.items()):
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
                        d = math.sqrt(d_x**2 + d_y**2+d_z**2)
                        if (d <= R_C):
                            # print("Wolf found rabbit")
                            if (random.random() < P_E_W):
                                list_rabbits = {
                                    k: v for k, v in list_rabbits.items() if v != rabbit}
                                N_R = N_R - 1
                                if (move_when_eat):
                                    wolf.x, wolf.y, wolf.z = rabbit.x, rabbit.y, rabbit.z
                                    wolf.i, wolf.j, wolf.k = rabbit.i, rabbit.j, rabbit.k
                                wolf.eat()
                                already_eaten = True

                                if (random.random() < P_R_W):
                                    new_wolf = Wolf(wolf.x, wolf.y, wolf.z, wolf.i, wolf.j,  wolf.k, R_C)

                                    added_wolves[N_W] = new_wolf
                                    N_W = N_W + 1
                                # print(f"Rabbit eaten by wolf at {rabbit.x}, {rabbit.y}")
                                break

    list_wolves.update(added_wolves)
    # list_num_wolves.append(N_W)

    # list_num_rabbits.append(N_R)

    ax.clear()
    scatter_wolves = ax.scatter([w.x for w in list_wolves.values()], [
                                w.y for w in list_wolves.values()], [
                                w.z for w in list_wolves.values()], c='red')
    scatter_rabbits = ax.scatter([r.x for r in list_rabbits.values()], [
                                 r.y for r in list_rabbits.values()], [r.z for r in list_rabbits.values()], c='green')
    plt.grid(True)
    ax.set_xlim([0, L])
    ax.set_ylim([0, L])
    ax.set_zlim([0, L])
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.00001)
    # ax.set_yticks(list(range(0,L, int(R_C))))
    # ax.set_xticks(list(range(0,L, int(R_C))))
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(R_C))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(R_C))
    plt.pause(0.00001)
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
if (name_plot != None):
    fig2.savefig("output/"+name_plot+".png")

plt.show()
fig3, ax3 = plt.subplots()
minimum = min(len(list_num_wolves), len(list_num_rabbits))

ax3.scatter(list_num_wolves[0],list_num_rabbits[0], c='r', label="Starting point")
ax3.plot(list_num_wolves[:minimum],list_num_rabbits[:minimum], c='r')
ax3.scatter(list_num_wolves[minimum-1],list_num_rabbits[minimum-1], c='b', label="End point")
ax3.legend()
ax3.set_title("Number of wolves vs number of rabbits")
ax3.set_ylabel("number of rabbits")
ax3.set_xlabel("Number of wolves")
ax3.grid(True)

plt.show()

