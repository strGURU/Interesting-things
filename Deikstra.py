import pygame as pg

pg.init()

clock = pg.time.Clock()

BLOCK_SIZE = 50
width = 1000
height = 750

colorPalitre = {"RED": (255, 0, 0),
                "GRAY": (50, 50, 50),
                "YELLOW": (255, 255, 0),
                "BLACK": (0, 0, 0),
                "GREEN": (0, 255, 0)}


screen = pg.display.set_mode((width, height))
pg.display.set_caption("Find shortest way")

map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player_x = 9
player_y = 8
CanGo = True
i = 0

enemy_x = 2
enemy_y = 1
EnCanGo = True
ei = 0
EnSide = "0"

inf = float("inf")

GRAPH = {}
GRAPH["player"] = {}
COSTS = {}
COSTS["player"] = None
PARENTS = {}
PARENTS["player"] = None
PROCESSED = []


sides = ["UP", "DOWN", "LEFT", "RIGHT"]

sidesLR = {"UP": ["LEFT", "RIGHT"],
           "DOWN": ["LEFT", "RIGHT"],
           "LEFT": ["UP", "DOWN"],
           "RIGHT": ["UP", "DOWN"]}

def IDKHowNameOfThisFunction(map_data, x, y):
    START = (x, y)
    STARTLR = [x, y]
    FINDING = True
    counter = 0
    reserv = []
    FINDINGLR = True
    counterLR = 0
    reservLR = []

    for side in sides:
        while FINDING:
            reserv = [x, y]
            if side == "UP":
                y -= 1
            elif side == "DOWN":
                y += 1
            elif side == "LEFT":
                x -= 1
            elif side == "RIGHT":
                x += 1
            STARTLR = [x, y]
            for sideLR in sidesLR[side]:
                while FINDINGLR:
                    reservLR = [x, y]
                    if sideLR == "UP":
                        y -= 1
                    elif sideLR == "DOWN":
                        y += 1
                    elif sideLR == "LEFT":
                        x -= 1
                    elif sideLR == "RIGHT":
                        x += 1
                    result = can_move(x, y)
                    counterLR += 1

                    if not result:
                        if counterLR > 2 and map_data[reservLR[1]][reservLR[0]] != 3:
                            map_data[reservLR[1]][reservLR[0]] = 3
                            IDKHowNameOfThisFunction(map_data, reservLR[0], reservLR[1])
                            map_data[STARTLR[1]][STARTLR[0]] = 3
                            IDKHowNameOfThisFunction(map_data, STARTLR[0], STARTLR[1])
                            FINDINGLR = False
                        else:
                            FINDINGLR = False
                FINDINGLR = True
                counterLR = 0
                x, y = STARTLR
            result = can_move(x, y)
            counter += 1

            if not result:
                if counter > 2 and map_data[reserv[1]][reserv[0]] != 3:
                    map_data[reserv[1]][reserv[0]] = 3
                    IDKHowNameOfThisFunction(map_data, reserv[0], reserv[1])
                    FINDING = False
                else:
                    FINDING = False
        FINDING = True
        counter = 0
        x, y = START

def draw_map(map_data):
    global COMPLETED
    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            if map_data[y][x] == 1:
                color = colorPalitre["GRAY"]
            elif y == enemy_y and x == enemy_x:
                color = colorPalitre["RED"]
            elif y == player_y and x == player_x:
                color = colorPalitre["YELLOW"]
            elif map_data[y][x] == 3:
                color = colorPalitre["BLACK"]
                makeTransitions(x, y)
            else:
                color = colorPalitre["BLACK"]
            pg.draw.rect(screen, color, (x * 50, y * 50, BLOCK_SIZE, BLOCK_SIZE))

def can_move(x, y):
    global gameRunning
    try:
        if map[y][x] == 3:
            return 3
        if map[y][x] != 1:
            return True
    except:
        print("Об'єкт імовірно за межами карти, програму зупинено")
        gameRunning = False
    return False

def makeTransitions(x, y):
    global GRAPH
    index = (x, y)
    GRAPH[index] = {}
    COSTS[index] = inf
    PARENTS[index] = None
    counter = 0
    FINDING = True


    for side in sides:
        while FINDING:
            if side == "UP":
                y -= 1
            elif side == "DOWN":
                y += 1
            elif side == "LEFT":
                x -= 1
            elif side == "RIGHT":
                x += 1
            result = can_move(x, y)
            counter += 1

            if not result:
                FINDING = False
            elif x == player_x and y == player_y:
                GRAPH[index]["player"] = (counter, side)
                FINDING = False
            elif result == 3:
                GRAPH[index][(x, y)] = (counter, side)
                FINDING = False

        counter = 0
        x, y = index
        FINDING = True

def find_lowest_cost_node(costs):
    lowest_cost = float("inf")
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in PROCESSED:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def enemyFind():
    global GRAPH
    global enemy_x
    global enemy_y
    global EnCanGo
    global EnSide
    global ei

    counter = 0
    FINDING = True
    PlayerСlose = False
    x = enemy_x
    y = enemy_y
    GRAPH["start"] = {}
    IsLocked = []

    for side in sides:
        while FINDING:
            if side == "UP":
                y -= 1
            elif side == "DOWN":
                y += 1
            elif side == "LEFT":
                x -= 1
            elif side == "RIGHT":
                x += 1
            result = can_move(x, y)
            counter += 1

            if not result:
                FINDING = False
            elif x == player_x and y == player_y:
                GRAPH["start"]["player"] = (counter, side)
                FINDING = False
                PlayerСlose = True
                EnSide = side
            elif result == 3:
                GRAPH["start"][(x, y)] = (counter, side)
                COSTS[(x, y)] = counter
                PARENTS[(x, y)] = "start"
                IsLocked.append((x, y))
                FINDING = False

        counter = 0
        FINDING = True
        x = enemy_x
        y = enemy_y

    for c in COSTS.keys():
        if c not in IsLocked:
            COSTS[c] = inf
            PARENTS[c] = None

    if not PlayerСlose:
        node = find_lowest_cost_node(COSTS)
        while node is not None:
            cost = COSTS[node]
            neighbors = GRAPH[node]
            for n in neighbors.keys():
                new_cost = cost + neighbors[n][0]

                if COSTS[n] > new_cost:
                    COSTS[n] = new_cost
                    PARENTS[n] = node
            PROCESSED.append(node)
            node = find_lowest_cost_node(COSTS)
        PROCESSED.clear()

        son = PARENTS["player"]
        try:
            while son != "start":
                reserv = son
                son = PARENTS[son]

            EnSide = GRAPH["start"][reserv][1]
        except:
            print("Не вдалося знайти гравця")
            EnSide = 0

    if player_x == enemy_x and player_y == enemy_y:
        EnSide = 0

    if EnSide == "LEFT" and EnCanGo:
        enemy_x -= 1
        EnCanGo = False
    if EnSide == "RIGHT" and EnCanGo:
        enemy_x += 1
        EnCanGo = False
    if EnSide == "UP" and EnCanGo:
        enemy_y -= 1
        EnCanGo = False
    if EnSide == "DOWN" and EnCanGo:
        enemy_y += 1
        EnCanGo = False

    if not EnCanGo:
        ei += 1
        if ei > 15:
            EnCanGo = True
            ei = 0

IDKHowNameOfThisFunction(map, enemy_x, enemy_y)

draw_map(map)

gameRunning = True
while gameRunning:

    draw_map(map)

    enemyFind()

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        if can_move(player_x - 1, player_y) and CanGo:
            player_x -= 1
            CanGo = False
    if keys[pg.K_RIGHT]:
        if can_move(player_x + 1, player_y) and CanGo:
            player_x += 1
            CanGo = False
    if keys[pg.K_UP]:
        if can_move(player_x, player_y - 1) and CanGo:
            player_y -= 1
            CanGo = False
    if keys[pg.K_DOWN]:
        if can_move(player_x, player_y + 1) and CanGo:
            player_y += 1
            CanGo = False

    if not CanGo:
        i += 1
        if i > 10:
            CanGo = True
            i = 0

    pg.display.update()
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False
            pg.quit()
