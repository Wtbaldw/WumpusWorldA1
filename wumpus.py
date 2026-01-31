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
        self.grid = [["EMPTY" for each in range(cols)] for _ in range(rows)] #Adding # of columns for each row, creating a 2D grid
        self.place_world()
        self.agent_alive = True
        self.agent_pos = (0,0)
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
            if self.grid[x][y] == "EMPTY" and (x,y) != (0,0):
                return (x,y)


    def neighbors(self, r, c):
        """
        Yield valid neighboring cells (up, down, left, right).
        """
        r = r
        c = c
        neighbors = []
        if self.inBounds(r+1,c):
            neighbors.append((r+1,c))
        if self.inBounds(r-1,c):
            neighbors.append((r-1,c))
        if self.inBounds(r,c+1):
            neighbors.append((r,c+1))
        if self.inBounds(r,c-1):
            neighbors.append((r,c-1))
        return neighbors
    
    def inBounds(self,r,c):
        r = r
        c = c
        if (0<r< self.rows) and (0<c< self.cols):
            return True
        else:
            False


    def get_percepts(self):
        x,y = self.agent_pos
        percepts = {
            "breeze" : False,
            "stench" : False,
            "safe" : True,
            "glitter" : True,
        }
        for neighbor in self.neighbors(x,y):
            nx,ny = neighbor
            if self.grid[nx][ny] == WUMPUS:
                percepts["stench"] = True
            if self.grid[nx][ny] == PIT:
                percepts["breeze"] = True
            if self.grid[x][y] == GOLD:
                percepts["glitter"] == True
            if percepts["stench"] or percepts["breeze"]:
                percepts["safe"] == False
        return percepts
        """
        Return the agent's current percepts.
        Example:
        (stench, breeze, glitter)
        """
        pass

    def move(self, pos):
        """
        Move the agent to a new position.
        Update agent_alive if it falls into a pit or meets the Wumpus.
        """
        pass

    def shoot(self, target):
        """
        Shoot the arrow into a target cell.
        The agent only has one arrow.
        Print '☠️ Wumpus screamed!' if the Wumpus is killed.
        """
        pass

    def pickup_gold(self):
        """
        Pick up gold if the agent is in the same cell.
        """
        pass


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
        pass


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

    """# Percepts (visual hints only)
     stench, breeze, glitter = world.percepts() 
    if breeze:
        pygame.draw.circle(screen, GRAY, agent_rect.center, 8)
    if stench:
        pygame.draw.circle(screen, GREEN, agent_rect.center, 5) """


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
            # percepts = world.get_Percepts()
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