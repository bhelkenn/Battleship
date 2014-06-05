from random import randint

#creates the board and defines how to print it
board = []
size = 6
for x in range(size):
    board.append(["O"] * size)
def print_board(board):
    for row in board:
        print " ".join(row)

#defines how to generate a random coordinate
def random_row(board):
    return randint(0, len(board) - 1)
def random_col(board):
    return randint(0, len(board[0]) - 1)

#define 2x1 patrol boat
def create_2x1():
    ship_2x1 = []
    
    #0 = horizontal, 1 = vertical
    length_dimension = randint(0, 1)
    
    #establish starting point for the "tracing" of the ship
    row_coordinate = random_row(board)
    col_coordinate = random_col(board)
    
    #ensure that the ship won't go off the board
    ship_2x1.append([row_coordinate, col_coordinate])
    if length_dimension == 0 and row_coordinate <= len(board) - 2:
        ship_2x1.append([row_coordinate + 1, col_coordinate])
    elif length_dimension == 0 and row_coordinate > len(board) - 2:
        ship_2x1.append([row_coordinate - 1, col_coordinate])
    elif length_dimension == 1 and col_coordinate <= len(board) - 2:
        ship_2x1.append([row_coordinate, col_coordinate + 1])
    elif length_dimension == 1 and col_coordinate > len(board) - 2:
        ship_2x1.append([row_coordinate, col_coordinate - 1])
    
    return ship_2x1
    
#define 3x1 destroyer and submarine
def create_3x1():
    ship_3x1 = []
    
    #0 = horizontal, 1 = vertical
    length_dimension = randint(0, 1)
    
    #establish starting point for the "tracing" of the ship
    row_coordinate = random_row(board)
    col_coordinate = random_col(board)

    #ensure that the ship won't go off the board
    ship_3x1.append([row_coordinate, col_coordinate])
    if length_dimension == 0 and row_coordinate <= len(board) - 3:
        ship_3x1.append([row_coordinate + 1, col_coordinate])
        ship_3x1.append([row_coordinate + 2, col_coordinate])
    elif length_dimension == 0 and row_coordinate > len(board) - 3:
        ship_3x1.append([row_coordinate - 1, col_coordinate])
        ship_3x1.append([row_coordinate - 2, col_coordinate])
    elif length_dimension == 1 and col_coordinate <= len(board) - 3:
        ship_3x1.append([row_coordinate, col_coordinate + 1])
        ship_3x1.append([row_coordinate, col_coordinate + 2])
    elif length_dimension == 1 and col_coordinate > len(board) - 3:
        ship_3x1.append([row_coordinate, col_coordinate - 1])
        ship_3x1.append([row_coordinate, col_coordinate - 2])
    
    return ship_3x1
    
#define 4x1 battleship
def create_4x1():
    ship_4x1 = []
    
    #0 = horizontal, 1 = vertical
    length_dimension = randint(0, 1)
    
    #establish starting point for the "tracing" of the ship
    row_coordinate = random_row(board)
    col_coordinate = random_col(board)

    #ensure that the ship won't go off the board
    ship_4x1.append([row_coordinate, col_coordinate])
    if length_dimension == 0 and row_coordinate <= len(board) - 4:
        ship_4x1.append([row_coordinate + 1, col_coordinate])
        ship_4x1.append([row_coordinate + 2, col_coordinate])
        ship_4x1.append([row_coordinate + 3, col_coordinate])
    elif length_dimension == 0 and row_coordinate > len(board) - 4:
        ship_4x1.append([row_coordinate - 1, col_coordinate])
        ship_4x1.append([row_coordinate - 2, col_coordinate])
        ship_4x1.append([row_coordinate - 3, col_coordinate])
    elif length_dimension == 1 and col_coordinate <= len(board) - 4:
        ship_4x1.append([row_coordinate, col_coordinate + 1])
        ship_4x1.append([row_coordinate, col_coordinate + 2])
        ship_4x1.append([row_coordinate, col_coordinate + 3])
    elif length_dimension == 1 and col_coordinate > len(board) - 4:
        ship_4x1.append([row_coordinate, col_coordinate - 1])
        ship_4x1.append([row_coordinate, col_coordinate - 2])
        ship_4x1.append([row_coordinate, col_coordinate - 3])
    
    return ship_4x1

#define 5x1 aircraft carrier
def create_5x1():
    ship_5x1 = []
    
    #0 = horizontal, 1 = vertical
    length_dimension = randint(0, 1)
    
    #establish starting point for the "tracing" of the ship
    row_coordinate = random_row(board)
    col_coordinate = random_col(board)

    #ensure that the ship won't go off the board
    ship_5x1.append([row_coordinate, col_coordinate])
    if length_dimension == 0 and row_coordinate <= len(board) - 5:
        ship_5x1.append([row_coordinate + 1, col_coordinate])
        ship_5x1.append([row_coordinate + 2, col_coordinate])
        ship_5x1.append([row_coordinate + 3, col_coordinate])
        ship_5x1.append([row_coordinate + 4, col_coordinate])
    elif length_dimension == 0 and row_coordinate > len(board) - 5:
        ship_5x1.append([row_coordinate - 1, col_coordinate])
        ship_5x1.append([row_coordinate - 2, col_coordinate])
        ship_5x1.append([row_coordinate - 3, col_coordinate])
        ship_5x1.append([row_coordinate - 4, col_coordinate])
    elif length_dimension == 1 and col_coordinate <= len(board) - 5:
        ship_5x1.append([row_coordinate, col_coordinate + 1])
        ship_5x1.append([row_coordinate, col_coordinate + 2])
        ship_5x1.append([row_coordinate, col_coordinate + 3])
        ship_5x1.append([row_coordinate, col_coordinate + 4])
    elif length_dimension == 1 and col_coordinate > len(board) - 5:
        ship_5x1.append([row_coordinate, col_coordinate - 1])
        ship_5x1.append([row_coordinate, col_coordinate - 2])
        ship_5x1.append([row_coordinate, col_coordinate - 3])
        ship_5x1.append([row_coordinate, col_coordinate - 4])
    
    return ship_5x1

#error-check to make sure that ships aren't overlapping
def collect_taken_coordinates(lst, taken):
    for hit in lst:
        taken.append(hit)
    return taken
    
#check possible coordinates against occupied space
def is_occupied(coord, taken):
    for i in range(0, len(taken)):
        if coord == taken[i]:
            return True
        else:
            occupied = False
    return occupied

#check if ship is off the board
def is_off(coord):
    if coord[0] < 0 or coord[1] < 0:
        return True
    else:
        off = False
    return off

#validate created ship
def validate(lst, taken):
    for hit in lst:
        if is_occupied(hit, taken) or is_off(hit):
            for i in range(0, len(lst)):
                del(lst[0])
    return lst

#create ships
def assemble_ships():
    #defines occupied coordinates on the board
    taken_coordinates = []
    
    patrol_boat = create_2x1()
    taken_coordinates = collect_taken_coordinates(patrol_boat, taken_coordinates)
    
    #debugging
    #print "occupied coordinates are " + str(taken_coordinates) + " after creating a patrol boat"
    
    destroyer = []
    while destroyer == []:
        destroyer = create_3x1()
        destroyer = validate(destroyer, taken_coordinates)
    
    taken_coordinates = collect_taken_coordinates(destroyer, taken_coordinates)
    
    #debugging
    #print "occupied coordinates are " + str(taken_coordinates) + " after creating a destroyer"
    
    submarine = []
    while submarine == []:
        submarine = create_3x1()
        submarine = validate(submarine, taken_coordinates)
    
    taken_coordinates = collect_taken_coordinates(submarine, taken_coordinates)
    
    #debugging
    #print "occupied coordinates are " + str(taken_coordinates) + " after creating a submarine"
    
    battleship = []
    while battleship == []:
        battleship = create_4x1()
        battleship = validate(battleship, taken_coordinates)
    
    taken_coordinates = collect_taken_coordinates(battleship, taken_coordinates)
    
    #debugging
    #print "occupied coordinates are " + str(taken_coordinates) + " after creating a battleship"
    
    aircraft_carrier = []
    while aircraft_carrier == []:
        aircraft_carrier = create_5x1()
        aircraft_carrier = validate(aircraft_carrier, taken_coordinates)
    
    taken_coordinates = collect_taken_coordinates(aircraft_carrier, taken_coordinates)
    
    #debugging
    #print "occupied coordinates are " + str(taken_coordinates) + " after creating a aircraft carrier"
    
    #makes determining a hit easier
    ships = [patrol_boat, destroyer, submarine, battleship, aircraft_carrier]
    return ships

ships = assemble_ships()

#debugging

print "Let's play Battleship!"

turn = 0
while ships[0] != [] or ships[1] != [] or ships[2] != [] or ships[3] != [] or ships[4] != []:
    """need to reset "scored" to False if the miss logic is going to work."""
    """Once a score is detected, "scored" is set to True until the beginning of the next turn"""
    scored = False
    print "Turn: " + str(turn + 1)
    #print "remaining ship coordinates are: " + str(ships)
    #status of destroyed ships
    if ships[0] == []:
        print "The patrol boat has been destroyed!"
    if ships[1] == []:
        print "The destroyer has been destroyed!"
    if ships[2] == []:
        print "The submarine has been destroyed!"
    if ships[3] == []:
        print "The battleship has been destroyed!"
    if ships[4] == []:
        print "The aircraft carrier has been destroyed!"

    print_board(board)
    guess_row = int(raw_input("Guess Row:")) - 1
    guess_col = int(raw_input("Guess Col:")) - 1
    guess = [guess_row, guess_col]
    
    #scoring a hit
    for i in range(len(ships)):
        for hit in ships[i]:
            if guess == hit:
                print "You scored a hit!"
                board[guess_row][guess_col] = "*"
                ships[i].remove(guess)
                scored = True
    if scored == False:
        #invalid coordinates entered
        if (guess_row < 0 or guess_row > len(board) - 1) or (guess_col < 0 or guess_col > len(board) - 1):
            print "Oops, that's not even in the ocean."
        #already tried coordinates
        elif(board[guess_row][guess_col] == "X" or board[guess_row][guess_col] == "*"):
            print "You guessed that one already."
        #straight up missed
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "X"
    turn += 1

#win condition
print "You've destroyed all battleships!"