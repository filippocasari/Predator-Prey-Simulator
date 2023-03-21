import matplotlib.pyplot as plt
import numpy as np
from Wolf import Wolf
from Rabbit import Rabbit
import random
import math
import json
import time
L = int(input("Insert value for L: "))
name_plot=input("Insert name for plot according with the assignment point: ")
#PERC_WOLVES = 0.01
#PERC_RABBITS = 0.09
#L2 = L**2


list_wolves = []
list_rabbits = []
with open('best_params.json', 'r') as f: #best_params.json
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
ITER = params['ITER']
del params
print(f"Number of wolves: {N_W}\n")
print(f"Number of rabbits: {N_R}\n")

N_X = int(L/R_C)
N_Y = int(L/R_C)
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
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
    list_wolves.append(Wolf(x, y, x_cell, y_cell, R_C))
for i in range(N_R):
    x = random.random() * L
    y = random.random() * L
    x_cell = math.ceil(x / R_C)
    y_cell = math.ceil(y / R_C)
    list_rabbits.append(Rabbit(x, y, x_cell, y_cell, T_D_R, R_C))

scatter_wolves = ax.scatter([w.x for w in list_wolves], [
                                w.y for w in list_wolves], c='red')
scatter_rabbits = ax.scatter([r.x for r in list_rabbits], [
                                r.y for r in list_rabbits], c='green')
ax.grid(True)
ax.set_title("Initial condition")
ax.get_figure().savefig(f"output_main/{name_plot}_initial_conition.png")
ax2.grid(True)
plt.draw()
plt.pause(4)



for iter in range(ITER):

    if (N_W < 1 or N_R < 1):
        break

    # past_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]
    index =-1
    for wolf in list_wolves.copy():
        index+=1
        if (wolf.not_eaten_iter >= T_D_W):
            list_wolves.remove(wolf)
            N_W = N_W - 1
            index-=1
            continue

        else:
            list_wolves[index].not_eaten_iter += 1
        step_len = np.random.normal(mu, sigma, 2)
        direction = np.random.randn(2)
        direction/= np.linalg.norm(direction)
        step_len=step_len*direction
        
        dx = step_len[0]
        dy = step_len[1]
        list_wolves[index].move(dx, dy, L)
        

    # new_value = [[list_wolves[i].x, list_wolves[i].y] for i in range(N_W)]
    # print(f"past values: {past_value}")
    # print(f"new value {new_value}")
    add_rabbits = []
    index =-1
    for rabbit in list_rabbits.copy():
        index+=1
        step_len = np.random.normal(mu, sigma, 2)
        direction = np.random.randn(2)
        direction/= np.linalg.norm(direction)
        step_len=step_len*direction
        
        dx = step_len[0]
        dy = step_len[1]
        list_rabbits[index].move(dx, dy, L)
        

        if (rabbit.life_steps >= T_D_R):
            list_rabbits.remove(rabbit)
            N_R = N_R - 1
            index-=1

        else:
            if (random.random() <= P_R_R):
                new_rabbit = Rabbit(rabbit.x, rabbit.y,
                                    rabbit.i, rabbit.j, T_D_R, R_C)
                add_rabbits.append(new_rabbit)
                N_R = N_R + 1

    list_rabbits.extend(add_rabbits)
    # list_num_rabbits.append(N_R)
    added_wolves = []
    # list_wolves=np.array(list_wolves)
    to_remove = []
    for wolf in list_wolves:
        #already_eaten = False
        i = wolf.i
        j = wolf.j
        x, y = wolf.x, wolf.y

        for ii in range(i-1, i+1):
            
            for jj in range(j-1, j+1):
                
                nearby_rabbits = [r for r in list_rabbits if r.i == ii %
                                  N_X and r.j == jj % N_Y and r not in to_remove]
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
                    d = math.sqrt(d_x**2 + d_y**2)
                    if (d <= R_C):
                        # print("Wolf found rabbit")
                        if (random.random() <= P_E_W):
                            to_remove.append(rabbit)
                            wolf.x, wolf.y = rabbit.x, rabbit.y
                            wolf.i, wolf.j = rabbit.i, rabbit.j
                            wolf.eat()
                            #already_eaten = True
                            N_R = N_R - 1
                            if (random.random() <= P_R_W):
                                new_wolf = Wolf(0, 0, 0, 0, R_C)
                                new_wolf.x = wolf.x
                                new_wolf.y = wolf.y
                                new_wolf.i = wolf.i
                                new_wolf.j = wolf.j

                                added_wolves.append(new_wolf)
                                N_W = N_W + 1
                            # print(f"Rabbit eaten by wolf at {rabbit.x}, {rabbit.y}")
                            #break

    list_wolves.extend(added_wolves)
    # list_num_wolves.append(N_W)
    for rabbit in to_remove:
        list_rabbits.remove(rabbit)
    # list_num_rabbits.append(N_R)

    ax.clear()
    scatter_wolves = ax.scatter([w.x for w in list_wolves], [
                                w.y for w in list_wolves], c='red')
    scatter_rabbits = ax.scatter([r.x for r in list_rabbits], [
                                 r.y for r in list_rabbits], c='green')
    
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    
    ax2.set_xlim(0, ITER)
    #ax2.set_ylim([0, max(len(list_num_rabbits), len(list_num_wolves))])
    ax2.plot(list_num_wolves, c='red')
    ax2.plot(list_num_rabbits, c='green')
    ax.grid()
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
if(name_plot!=None):
    fig2.savefig("output_main/"+name_plot+".png")

plt.show()

from matplotlib.animation import FuncAnimation
fig3=plt.figure()

#scatter = ax.scatter([], [])
def animate(n):
    line, = plt.plot(list_num_rabbits[:n], list_num_wolves[:n], color='g')
    plt.xlim([-2, max(list_num_rabbits)+2])
    plt.ylim([-2, max(list_num_wolves)+2])
    if(n==len(list_num_rabbits)-1 and name_plot!=None):
        fig3.savefig(f"output_main/{name_plot}_populations.png", dpi=300, bbox_inches='tight', pad_inches=0, format='png')
    return line,


plt.scatter(list_num_rabbits[0], list_num_wolves[0], c='r', label="Starting point")
plt.scatter(list_num_rabbits[-1], list_num_wolves[-1], c='b', label="End point")
plt.legend()
plt.title("Number of wolves vs number of rabbits")
plt.xlabel("number of rabbits")
plt.ylabel("Number of wolves")
plt.grid(True)
#ax3.plot(,, c='r')
anim = FuncAnimation(fig, animate, frames=len(list_num_rabbits), interval=25, blit=True)
plt.show()
#if (name_plot!=None):
 ##   fig = anim._fig
 #   fig.savefig(f"output_main/{name_plot}_populations.png", dpi=300, bbox_inches='tight', pad_inches=0, format='png', transparent=True)
    #anim.save(f"output_main/{name_plot}_populations.png", writer='imagemagick', fps=10, frame=len(list_num_rabbits)-1)
    


