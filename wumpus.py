import pygame
import random
import sys
import time

# ---------------- CONFIG ----------------
CELL_SIZE = 80
FPS = 5

EMPTY = 0
PIT = 1
WUMPUS = 2
GOLD = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
GRAY = (200, 200, 200)
RED = (220, 50, 50)
BLUE = (80, 80, 220)
GREEN = (50, 200, 50)
YELLOW = (240, 220, 70)

# ---------------------------------------

class WumpusWorld:
    def __init__(self, rows, cols):
        """
        Initialize the Wumpus World.
        Students should:
        - Create the grid
        - Place the agent, Wumpus, gold, and pits
        - Initialize game state variables
        """ 
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for each in range(cols)] for _ in range(rows)] #Adding # of columns for each row, creating a 2D grid
        self.place_world()
        self.agent_alive = True
        self.agent_pos = (rows-1,0)
        self.arrow=True
        self.has_gold=False
        self.wumpus_alive=True
        self.prev_position = (0,0) #just to speed up return to exit
        pass

    def place_random(self, item): #placing gold and obstacles into the grid
        x,y = self.random_empty_cell()
        self.grid[x][y] = item


    def place_world(self):
        """
        Randomly place:
        - One Wumpus
        - One Gold
        - Multiple pits
        Ensure the starting cell is safe.
        """
        for i in range(3):
            self.place_random(PIT)
        self.place_random(WUMPUS)
        self.place_random(GOLD)
        pass

    def random_empty_cell(self):
        """
        Return a random (row, col) that is empty and not the start cell.
        """
        while True:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if self.grid[x][y] == EMPTY and (x,y) != (self.rows-1,0):
                return (x,y)


    def neighbors(self):
        """
        Yield valid neighboring cells (up, down, left, right).
        """
        r,c = self.agent_pos
        if self.inBounds(r+1,c): #right
            yield (r+1,c)
        if self.inBounds(r-1,c): #left 
            yield (r-1,c)
        if self.inBounds(r,c+1): #down
            yield (r,c+1)
        if self.inBounds(r,c-1): #up
            yield (r,c-1)

    def getSafeNeighbors(self):
        neighbors = self.neighbors()
        safeNeighbors = []
        for x, y in neighbors:
            if self.grid[x][y] not in [WUMPUS,PIT]:
                safeNeighbors.append((x, y))
        return safeNeighbors
    
    def inBounds(self,r,c): #checks if square is inBounds
        r = r
        c = c
        if (0<=r< self.rows) and (0<=c< self.cols):
            return True
        else:
            return False


    def get_percepts(self):
        """
        Return the agent's current percepts.
        Example:
        (stench, breeze, glitter)
        """
        x,y = self.agent_pos
        percepts = {
            "breeze" : False,
            "stench" : False,
            "glitter" : False,
        }
        if self.grid[x][y] == GOLD:
                percepts["glitter"] = True
        for nx, ny in self.neighbors(): #checks through neighboring squares and changes percepts if needed
            if self.grid[nx][ny] == WUMPUS and self.wumpus_alive:
                percepts["stench"] = True
            if self.grid[nx][ny] == PIT:
                percepts["breeze"] = True
        return  percepts["stench"], percepts["breeze"], percepts["glitter"]
    
    def move_to_exit(self):
        x,y = self.agent_pos
        movesTowardExit = [(x-1,y),(x,y+1)]
        safeOptions = []
        for _ in movesTowardExit:
            if _ in self.getSafeNeighbors() and (_ != self.prev_position):
                safeOptions.append(_)
        if safeOptions:
            return safeOptions
        else:
            return self.getSafeNeighbors()



    def move(self, action):
        """
        Move the agent to a new position.
        Update agent_alive if it falls into a pit or meets the Wumpus.
        """
        #also needs to avoid dying

        # r,c= self.agent_pos
        # self.agent_pos=(r,c)
        if action == "pickup_gold":
            self.pickup_gold()
        elif action == "avoid_and_shoot":
            #avoid
            self.shoot()
            r,c = random.choice(self.getSafeNeighbors())
            self.prev_position = self.agent_pos
            self.agent_pos = (r,c)
            
            
        elif action == "avoid":
            #avoid
            r,c = random.choice(self.getSafeNeighbors())
            self.prev_position = self.agent_pos
            self.agent_pos = (r,c)
            
        elif action == "move_randomly": #avoids danger squares, just change to .neighbors instead of safe to not do this
            r,c = random.choice(self.getSafeNeighbors())
            self.prev_position = self.agent_pos
            self.agent_pos = (r,c)
            if self.grid[r][c]==PIT:
                print("💀 Agent fell into a pit!")
                self.agent_alive=False
            if self.grid[r][c]==WUMPUS and self.wumpus_alive:
                print("💀 Agent eaten by the Wumpus!")
                self.agent_alive = False

        elif action == "move_to_exit":
            moves = self.move_to_exit()
            r,c = random.choice(moves)
            self.prev_position = self.agent_pos
            self.agent_pos = (r,c)
            
            
        pass

    def shoot(self):
        """
        Shoot the arrow into a target cell.
        The agent only has one arrow.
        Print '☠️ Wumpus screamed!' if the Wumpus is killed.
        """
        x,y = self.agent_pos
        points = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        targets = []
        for nx,ny in points:
            if self.inBounds(nx,ny):
                targets.append((nx,ny))
        if not self.arrow:
            return 
        self.arrow=False
        nx,ny = random.choice(targets)
        if self.grid[nx][ny]== WUMPUS and self.wumpus_alive:
            self.wupus_alive=False
            self.grid[nx][ny] = EMPTY
            print("☠️ Wumpus screamed!")
        else:
            print("User missed his ONE AND ONLY arrow!")
        
        

    def pickup_gold(self):
        """
        Pick up gold if the agent is in the same cell.
        """
        r,c=self.agent_pos
        if self.grid[r][c]==GOLD:
            self.has_gold=True
            self.grid[r][c]=EMPTY
            print("✨ Gold picked up!")
        


# ---------------- AGENT ----------------

class SimpleReflexAgent:
    def act(self, world):
        """
        Decide and execute an action based ONLY on current percepts.
        Must implement a simple reflex agent:
        - No memory
        - No planning
        - No inference
        """
        percepts = world.get_percepts() 
        print(percepts)
        action = self.get_action(percepts,world)
        print(action)
        world.move(action)
        pass

    def get_action(self, percepts, world):
        print(percepts)
        if percepts[2]: #glitter
            return "pickup_gold"
        if percepts[0]: #stench
            return "avoid_and_shoot"
        if percepts[1]: #breeze
            return "avoid"
        if world.has_gold:
            return "move_to_exit"
        return "move_randomly"



# ---------------- DRAWING ----------------
# NOTE: you do NOT need to modify this section.

def draw_world(screen, world):
    for r in range(world.rows):
        for c in range(world.cols):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            cell = world.grid[r][c]

            if cell == PIT:
                pygame.draw.circle(screen, BLACK, rect.center, 20)
            if cell == GOLD:
                pygame.draw.circle(screen, YELLOW, rect.center, 15)
            if cell == WUMPUS: # and world.wumpus_alive: Just remove wumpus from board when killed?
                pygame.draw.circle(screen, RED, rect.center, 20)

    # Agent
    ar, ac = world.agent_pos
    agent_rect = pygame.Rect(
        ac * CELL_SIZE + 10,
        ar * CELL_SIZE + 10,
        CELL_SIZE - 20,
        CELL_SIZE - 20
    )
    pygame.draw.rect(screen, BLUE, agent_rect)

    # Percepts (visual hints only)
    stench, breeze, glitter = world.get_percepts() 
    if breeze:
        pygame.draw.circle(screen, GRAY, agent_rect.center, 8)
    if stench:
        pygame.draw.circle(screen, GREEN, agent_rect.center, 5) 


# ---------------- MAIN ----------------

def main():
    pygame.init()

    rows = random.randint(4, 7)
    cols = random.randint(4, 7)

    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Wumpus World - Simple Reflex Agent")

    clock = pygame.time.Clock()

    world = WumpusWorld(rows, cols)
    agent = SimpleReflexAgent()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if world.agent_alive:
            agent.act(world)
        else:
            print("Agent died")
            pygame.quit()
            sys.exit()

        screen.fill(GRAY)
        draw_world(screen, world)
        pygame.display.flip()


if __name__ == "__main__":
    main()
