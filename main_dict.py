import matplotlib.pyplot as plt
import numpy as np
from Wolf import Wolf
from Rabbit import Rabbit
import random
import math
import matplotlib.ticker as ticker
import time
L = int(input("Insert value for L: "))
name_plot=input("Insert name for plot according with the assignment point: ")
PERC_WOLVES = 0.01
PERC_RABBITS = 0.09
L2 = L**2
#N_R = int(L2*PERC_RABBITS)
#N_W = int(L2*PERC_WOLVES)
N_R = 90
N_W=20
list_wolves = {}
list_rabbits = {}
R_C = 0.1
print(f"Number of wolves: {N_W}\n")
print(f"Number of rabbits: {N_R}\n")
P_E_W = 0.1
P_R_W = 0.3
P_R_R = 0.18
T_D_R = 100
T_D_W = 100
mu = 0.0
sigma = 0.5
N_X = int(L/R_C)
N_Y = int(L/R_C)
fig, ax = plt.subplots()
scatter_wolves = ax.scatter([], [], c='r')
scatter_rabbits = ax.scatter([], [], c='b')
ax.set_xlim([0, L])
ax.set_ylim([0, L])
start = time.time()

list_num_wolves = []
list_num_rabbits = []
for i in range(N_W):
    x = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_wolves[i]=Wolf(x, y, x_cell, y_cell, R_C)
for i in range(N_R):
    x = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_rabbits[i]=Rabbit(x, y, x_cell, y_cell, T_D_R, R_C)


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
        dx = np.random.randint(-1, 2)*step_len/np.sqrt(2)
        dy = np.random.randint(-1, 2)*step_len/np.sqrt(2)
        wolf.move(dx, dy, L)

    # new_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]
    # print(f"past values: {past_value}")
    # print(f"new value {new_value}")
    add_rabbits = {}
    for key, rabbit in list(list_rabbits.items()):
        step_len = np.random.normal(mu, sigma, 2)
        direction = np.random.randn(2)
        direction/= np.linalg.norm(direction)
        step_len=step_len*direction
        
        dx = step_len[0]
        dy = step_len[1]
        rabbit.move(dx, dy, L)

        if (rabbit.life_steps >= T_D_R):
            del list_rabbits[key]
            N_R = N_R - 1

        else:
            if (random.random() < P_R_R):
                new_rabbit = Rabbit(rabbit.x, rabbit.y,
                                    rabbit.i, rabbit.j, T_D_R, R_C)
                add_rabbits[N_R]=new_rabbit
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
        x, y = wolf.x, wolf.y

        for ii in range(i-1, i+1):
            if (already_eaten):
                break
            for jj in range(j-1, j+1):
                if (already_eaten):
                    break
                nearby_rabbits = {r.i: r for r in list_rabbits.values() if r.i == ii % N_X and r.j == jj % N_Y and r not in to_remove.values()}


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
                    d = math.sqrt(d_x**2 + d_y**2)
                    if (d <= R_C):
                        # print("Wolf found rabbit")
                        if (random.random() < P_E_W):
                            list_rabbits = {k: v for k, v in list_rabbits.items() if v != rabbit}
                            N_R = N_R - 1
                            wolf.x, wolf.y = rabbit.x, rabbit.y
                            wolf.i, wolf.j = rabbit.i, rabbit.j
                            wolf.eat()
                            already_eaten = True
                            
                            if (random.random() < P_R_W):
                                new_wolf = Wolf(0, 0, 0, 0, R_C)
                                new_wolf.x = wolf.x
                                new_wolf.y = wolf.y
                                new_wolf.i = wolf.i
                                new_wolf.j = wolf.j

                                added_wolves[N_W]=new_wolf
                                N_W = N_W + 1
                            # print(f"Rabbit eaten by wolf at {rabbit.x}, {rabbit.y}")
                            break

    list_wolves.update(added_wolves)
    # list_num_wolves.append(N_W)
    
    # list_num_rabbits.append(N_R)

    ax.clear()
    scatter_wolves = ax.scatter([w.x for w in list_wolves.values()], [
                                w.y for w in list_wolves.values()], c='red')
    scatter_rabbits = ax.scatter([r.x for r in list_rabbits.values()], [
                                 r.y for r in list_rabbits.values()], c='green')
    plt.grid(True)
    ax.set_xlim([0, L])
    ax.set_ylim([0, L])
    # ax.set_yticks(list(range(0,L, int(R_C))))
    # ax.set_xticks(list(range(0,L, int(R_C))))
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(R_C))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(R_C))
    fig.canvas.draw()
    fig.canvas.flush_events

    # plt.draw()
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
fig2.savefig("output/"+name_plot+".png")
plt.show()

