class Wolf:
    def __init__(self, x, y,z, i, j,k, r_c):
        # Constructor method to create a new Wolf object
        self.x = x
        self.y = y
        self.z=z
        self.i = i
        self.j = j
        self.k=k
        self.not_eaten_iter = 0
        self.R_C = r_c

    def move(self, dx, dy,dz, L):
        # Method to move the wolf by a given amount
        self.x = (self.x + dx) % L
        self.y = (self.y + dy) % L
        self.z = (self.z + dz) % L
        self.i = int(self.x/self.R_C) 
        self.j = int(self.y/self.R_C)
        self.k = int(self.z/self.R_C)

    def eat(self):
        
        self.not_eaten_iter = 0

    def disp(self):
        # Method to display information about the wolf
        print(f'Wolf position: ({self.x}, {self.y})')
        print(f'Cell location: ({self.i}, {self.j})')
