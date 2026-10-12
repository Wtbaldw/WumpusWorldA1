# Wumpus World: simple reflex agent

A team project in Python and pygame. A simple reflex agent explores a Wumpus World cave, picks up the gold, and returns to the start. It picks each action from what it senses that turn. See Limitations for two shortcuts.

## How it works

Everything is in `wumpus.py`.

**The world**
- A random grid, 4–7 rows by 4–7 columns.
- 3 pits, 1 Wumpus and 1 gold, each in a random empty cell. Nothing is ever placed on the start cell.
- The agent starts in the bottom-left corner with one arrow.

**Percepts** (checked every turn)
- **Stench:** a living Wumpus is in an adjacent cell (up, down, left or right).
- **Breeze:** a pit is in an adjacent cell.
- **Glitter:** the gold is in the current cell.

**Agent rules** (`SimpleReflexAgent.get_action`, first match wins)
1. Glitter → pick up the gold.
2. Stench → shoot the arrow into a random adjacent cell, then step to a random safe neighbor.
3. Breeze → step to a random safe neighbor.
4. Carrying the gold → head for the exit. It prefers safe moves down or left that don't go straight back to the previous cell.
5. Otherwise → step to a random safe neighbor.

**Shooting**
- The agent has one arrow.
- If the arrow lands on the Wumpus, the Wumpus dies, is removed from the board, and "Wumpus screamed!" is printed. Otherwise it's a miss.

**Ending a run**
- The run ends when the agent is back on the start cell holding the gold.
- Each turn prints the percepts, the chosen action and the new position to the console.
- The pygame window redraws at 5 frames per second: pits black, gold yellow, Wumpus red, agent blue, breeze a gray dot, stench a green dot.

## Run it

```bash
pip install pygame
python wumpus.py
```

Close the window to stop a run early. Each run generates a new random board.

## Project context

- **Team project for a college course assignment**, built by four students: William Baldwin, Madison Montgomery, Mark Carr and Nyree Hamrick (listed in the header of `wumpus.py`).
- **Built from course starter code.** The file started from a template. Its docstrings address "Students", and the drawing code is marked as not needing changes. The team filled in the world setup, percepts, movement, shooting, the win check and the agent.
- **Commit history:** 25 of 28 commits come from William Baldwin's account and 3 from Madison Montgomery's.

## Limitations

- **Not a strictly pure reflex agent.** Two shortcuts:
  - The "safe neighbor" filter reads pit and Wumpus positions straight from the world grid, which a real agent could only infer from percepts.
  - The world remembers the previous cell to steer the trip home.
- **Death checks never trigger.** Moves only go to hazard-free cells, so the pit and Wumpus death branches in `move()` don't fire in practice.
- **Can crash when boxed in.** If every neighbor holds a hazard, `random.choice` gets an empty list and the program stops with an `IndexError`.
- **Gold may be unreachable.** Nothing checks whether hazards wall it off. If they do, the agent wanders until the window is closed.
- **The arrow often misses**, because its direction is random.
- **Odds and ends:**
  - no `requirements.txt`, no random seed and no tests
  - `time` is imported but never used
  - the header date reads 2/5/2025, while the commits run from 2026-01-31 to 2026-02-06

## License

There's no license file, so default copyright applies.
