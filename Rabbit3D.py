import random
class Rabbit:
    def __init__(self, x, y,z, i, j,k, t_d_r, r_c):
        # Constructor method to create a new Rabbit object
        self.x = x
        self.y = y
        self.z=z
        self.i = i
        self.j = j
        self.k=k
        self.life_steps = random.randint(1, t_d_r)
        self.R_C = r_c

    def move(self, dx, dy,dz, L):
        # Method to move the rabbit by a given amount
        self.x = (self.x + dx) % L
        self.y = (self.y + dy) % L
        self.z=(self.z+dz)%L
        self.i = int(self.x/self.R_C) 
        self.j = int(self.y/self.R_C)
        self.k = int(self.z/self.R_C)
        self.life_steps += 1

    def disp(self):
        # Method to display information about the rabbit
        print(f'Rabbit position: ({self.x}, {self.y})')
        print(f'Cell location: ({self.i}, {self.j})')
