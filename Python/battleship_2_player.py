from random import randint

#size of the battleship grid
board_size = 5
class Board(object):
    board = []

    def __init__(self, size):
        self.size = size
        self.board = self.create_board()

    def create_board(self):
        board = []
        for x in range(self.size):
            board.append(['O'] * self.size)
        return board

    def print_board(self):
        s = ''
        for row in self.board:
            s += ' '.join(row) + '\n'
        print s

    #replaces target coord to input char
    def replace(self, coord, char):
        self.board[coord[0]][coord[1]] = char
		
    #determines if coord is occupied by a ship
    def is_a_ship(self, coord):
        if self.board[coord[0]][coord[1]] == 'S':
            return True
        else:
            return False

    #determines if coord was already tried
    def already_tried(self, coord):
        if self.board[coord[0]][coord[1]] == 'X':
            return True
        elif self.board[coord[0]][coord[1]] == '*':
            return True
        else:
            return False
			
    #determines if coord is on the board
    def is_valid(self, coord):
        for each in coord:
            if each < 0 or each >= self.size:
                return False
        return True

class Ship(object):
    horizontal = True
    init_coord = []
    ship = []
    
    def __init__(self, length, name):
        self.length = length
        self.det_length_direction()
        self.ship = self.create()
        self.name = name
    
    def det_length_direction(self):
        num = randint(0, 1)
        if num == 1:
            self.horizontal = False
        return self.horizontal
    
    def is_horizontal(self):
        return self.horizontal
    
    def det_init_coord(self):
        self.init_coord = []
        self.init_coord.append(randint(0, board_size - 1))
        self.init_coord.append(randint(0, board_size - 1))
        return self.init_coord
    
    def print_ship(self):
        return str(self.ship)
    
    def create(self):
        self.init_coord = self.det_init_coord()
        ship = []
        if self.is_horizontal() == True:
            if self.init_coord[0] <= board_size - self.length:
                for i in range(self.length):
                    ship.append([self.init_coord[0] + i, self.init_coord[1]])
            else:
                for i in range(self.length):
                    ship.append([self.init_coord[0] - i, self.init_coord[1]])
            return ship
        else:
            if self.init_coord[1] <= board_size - self.length:
                for i in range(self.length):
                    ship.append([self.init_coord[0], self.init_coord[1] + i])
            else:
                for i in range(self.length):
                    ship.append([self.init_coord[0], self.init_coord[1] - i])
            return ship

    #check possible coordinates against occupied space
    def is_occupied(self, coord, taken):
        for i in range(len(taken)):
            if coord == taken[i]:
                return True
        return False

    #validate created ship
    def is_valid(self, taken):
        for hit in self.ship:
            if self.is_occupied(hit, taken) or self.is_off(hit):
                return False
        return True
    
    #checks if the ship is emptied
    def is_empty(self):
        if self.print_ship() == '[]':
            return True
        else:
            return False
	
    #delete invalid ship
    def delete(self):
        for i in range(self.length):
            del(self.ship[0])

    #adds to list of occupied coordinates
    def collect_taken_coordinates(self, taken):
        for coord in self.ship:
            taken.append(coord)
        return taken

    #check if ship is off the board
    def is_off(self, coord):
        if coord[0] < 0 or coord[1] < 0:
            return True
        else:
            return False

    #matches a coord against specified ship index
    def matches_coord(self, coord):
        for i in range(len(self.ship)):
            if self.ship[i] == coord:
                return True
        return False

    #remove damaged part of the ship
    def damage(self, coord):
        self.ship.remove(coord)

    #returns the name of the ship
    def print_name(self):
        return str(self.name)

#creates user boards
p1_board_for_guesses = Board(board_size)
p2_board_for_guesses = Board(board_size)
p1_board_with_ships = Board(board_size)
p2_board_with_ships = Board(board_size)

#creates ships
def create_ships():
    taken_coords = []

    #aircraft carrier
    aircraft_carrier = Ship(0, "Aircraft carrier")
    while aircraft_carrier.is_empty():
        aircraft_carrier = Ship(5, "Aircraft carrier")
        if aircraft_carrier.is_valid(taken_coords) != True:
            aircraft_carrier.delete()
    taken_coords = aircraft_carrier.collect_taken_coordinates(taken_coords)

    #battleship
    battleship = Ship(0, "Battleship")
    while battleship.is_empty():
        battleship = Ship(4, "Battleship")
        if battleship.is_valid(taken_coords) != True:
            battleship.delete()
    taken_coords = battleship.collect_taken_coordinates(taken_coords)

    #submarine
    submarine = Ship(0, "Submarine")
    while submarine.is_empty():
        submarine = Ship(3, "Submarine")
        if submarine.is_valid(taken_coords) != True:
            submarine.delete()
    taken_coords = submarine.collect_taken_coordinates(taken_coords)

    #destroyer
    destroyer = Ship(0, "Destroyer")
    while destroyer.is_empty():
        destroyer = Ship(3, "Destroyer")
        if destroyer.is_valid(taken_coords) != True:
            destroyer.delete()
    taken_coords = destroyer.collect_taken_coordinates(taken_coords)

    #patrol boat
    patrol_boat = Ship(0, "Patrol boat")
    while patrol_boat.is_empty():
        patrol_boat = Ship(2, "Patrol boat")
        if patrol_boat.is_valid(taken_coords) != True:
            patrol_boat.delete()
    taken_coords = patrol_boat.collect_taken_coordinates(taken_coords)

    #assemble ships
    ships = [patrol_boat, destroyer, submarine, battleship, aircraft_carrier]
    return ships

	
#set ships for each player
p1_ships = create_ships()
p2_ships = create_ships()

def populate_board(board, ships):
    lst = []
    for i in range(len(ships)):
        lst.append(ships[i].ship)
    for each in lst:
        for coord in each:
            board.replace(coord, 'S')
    return board

p1_board_with_ships = populate_board(p1_board_with_ships, p1_ships)
p2_board_with_ships = populate_board(p2_board_with_ships, p2_ships)

player1 = raw_input("What's the first player's name?")
player2 = raw_input("What's the second player's name?")

def player_wins(ships):
    for i in range(len(ships)):
        if ships[i].is_empty() == False:
            return False
    return True

def player_turn(ship_board, guess_board, player_name, ships):
    '''need to reset "scored" to False to make 'miss' logic work'''
    '''Once a score is detected, "scored" is set to True'''

    print player_name + "'s turn:" + '\n'

    #status of destroyed ships
    for i in range(len(ships)):
        if ships[i].is_empty():
            print ships[i].print_name() + " is destroyed!"

    #print board
    guess_board.print_board()
	
    guess_row = int(raw_input("Guess Row:")) - 1
    guess_col = int(raw_input("Guess Col:")) - 1
    guess = [guess_row, guess_col]
    
    #verifies that input coords are valid and weren't already chosen
    while guess_board.is_valid(guess) == False or guess_board.already_tried(guess):
        if guess_board.is_valid(guess) == False:
            print "Oops, that's not even in the ocean."
        elif guess_board.already_tried(guess):
            print "You guessed that one already."
        guess_row = int(raw_input("Guess Row:")) - 1
        guess_col = int(raw_input("Guess Col:")) - 1
        guess = [guess_row, guess_col]

    #check if scoring occurs
    #scoring a hit
    if ship_board.is_a_ship(guess):
        print "You scored a hit!"
        guess_board.replace(guess, '*')

        #update ships
        for i in range(len(ships)):
            if ships[i].matches_coord(guess):
                ships[i].damage(guess)

        #win condition
        if player_wins(ships):
            return True

    #miss logic
    else:
        print "You missed my battleship!"
        guess_board.replace(guess, 'X')

    return False

#end-loop logic is in player_turn
has_won = False
while has_won == False:
    has_won = player_turn(p2_board_with_ships, p1_board_for_guesses, player1, p2_ships)
    if has_won:
        print "You've destroyed all battleships!"
        print player1 + " has won the game!"
    else:
        has_won = player_turn(p1_board_with_ships, p2_board_for_guesses, player2, p1_ships)
        if has_won:
            print "You've destroyed all battleships!"
            print player2 + " has won the game!"