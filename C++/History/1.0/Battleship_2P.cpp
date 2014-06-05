#include<iostream>
#include<string>
#include<time.h>
using namespace std;
bool DEBUG = false;

//needs to be global in order to work properly
int *taken_coords;
const int SIZE = 8;

class Board {
public:
	Board() {
		board = new char[SIZE * SIZE];
		create_board();
	}
	
	//assembles the array into a printable format
	void print_board() {
		for (int i = 0; i < SIZE; i++) {
			for (int j = 0; j < SIZE; j++) {
				cout << board[i * SIZE + j] << " ";
			}
			cout << endl;
		}
	}
	
	//replaces target coord to input char
	void replace(int coord, char replacement) {
		board[coord] = replacement;
	}
	
	//determines if coord is occupied by a ship
	bool is_a_ship(int coord) {
		if (board[coord] == 'S') {return true;}
		else {return false;}
	}
	
	//determines if coord was already tried
	bool already_tried(int coord) {
		if (board[coord] == 'X' || board[coord] == '*') {return true;}
		else {return false;}
	}
	
	//determines if coord is on the board
	bool is_valid(int coord) {
		if (coord < 0 || coord >= SIZE * SIZE) {return false;}
		else {return true;}
	}
	
private:
	char *board;

	//fills in the board array with O's
	void create_board() {
		for (int i = 0; i < (SIZE * SIZE); i++) {
			board[i] = 'O';
		}
	}
};

class Ship {
public:
	//constructor needs to be empty for "new" to work	
	Ship() {}
	
	//takes over to "initialize unique parameters of the ship
	void construct(int ship_length, string ship_name) {
		name = ship_name;
		if (DEBUG) {cout << "\nname == " << name << endl;}
		length = ship_length;
		ship = new int[length];
		populate();
	}
	
	//checks if the ship is zeroed out
	bool is_empty() {
		if (length == 0) {return true;}
		else {return false;}
	}
	
	//remove damaged part of the ship
	void damage(int coord) {
		//decrement by one to create new length of damaged ship
		length--;
		
		//only applicable if length is still positive
		if (length > 0) {
			//establishes correct size of new_array
			int *new_array = new int[length];
			
			//sets counter to properly set indices of new_array
			int count = 0;
			
			//only moves over undamaged parts of the ship to new_array
			for (int i = 0; i < (length + 1); i++) {
				if (ship[i] != coord) {
					new_array[count] = ship[i];
					count++;
				}
			}

			//erases and sets updated length to the ship
			ship = new int[length];
			
			//moves coords back to the ship for future reference
			for (int i = 0; i < length; i++) {ship[i] = new_array[i];}
			
			//clears new_array
			delete[] new_array;
			new_array = 0;
		}
	}
	
	//populate ship indices with "coordinates" (row * SIZE) + col
	void populate() {
		det_length_direction();
		det_init_coord();
		ship[0] = init_coord;
		if (horizontal == false) {
			if (init_coord < SIZE * SIZE - (length - 1)) {
				for (int i = 1; i < length; i++) {
					ship[i] = init_coord + SIZE * i;
				}
				if (DEBUG) {
					cout << "Ship coords are: ";
					print_ship();
				}
			}
			else {
				cout << "Something went wrong in populate()" << endl;
			}
		}
		else {
			for (int i = 1; i < length; i++) {
				ship[i] = init_coord + i;
			}
			if (DEBUG) {
				cout << "Ship coords are: ";
				print_ship();
			}
		}
	}
	
	//adds to list of occupied coordinates
	void collect_taken(int num) {
		//grab what the coords were
		int *temp = new int[num];
		for (int i = 0; i < num; i++) {
			temp[i] = taken_coords[i];
		}
		//set the new length of the array to include the new ship
		taken_coords = new int[length + num];
		
		//put back the old values
		for (int i = 0; i < num; i++) {
			taken_coords[i] = temp[i];
		}
		
		//deletes "temp" to prevent memory leak
		delete[] temp;
		temp = 0;
		
		//add the new values
		for (int i = 0; i < length; i++) {
			taken_coords[num + i] = ship[i];
		}
	}
	
	//finds the ship that contains target coord
	bool matches_coord(int coord) {
		for (int i = 0; i < length; i++) {
			if (ship[i] == coord) {
				return true;
			}
		}
		return false;
	}
	
	//increment count
	int inc_count(int num) {
		num += length;
		return num;
	}

	//validate created ship
	bool is_valid(int num) {
		for (int i = 0; i < length; i++) {
			if (is_occupied(ship[i], num)) {
				return false;
			}
		}
		if (DEBUG) {cout << "Is valid" << endl;}
		return true;
	}
	
	//return ship length
	int get_length() {return length;}

	//return coord of a ship part
	int get_coord(int x) {return ship[x];}
	
	//returns the ship for help in assembly
	int* get_ship() {return ship;}

	//returns the display name of the ship
	string get_name() {return name;}

	//DEBUGGING FUNCTIONS
	//outputs coordinates for each ship chunk
	void print_ship() {
		cout << "[" << ship[0];
		for (int i = 1; i < length; i++) {
			cout << ", " << ship[i];
		}
		cout << "]" << endl;
	}

private:
	bool horizontal;
	int init_coord;
	int length;
	string name;
	int *ship;

	//horizontal = 0, vertical = 1
	void det_length_direction() {
		int num = rand() % 2;
		if (num == 0) {horizontal = true;}
		else {horizontal = false;}
	}
	
	//randomly generates a starting coord for the ship
	void det_init_coord() {
		int row, col;
		if (horizontal) {
			if (SIZE == length) {
				row = rand() % SIZE;
				col = 0;
			}
			else {
				row = rand() % SIZE;
				col = rand() % (SIZE - length);
			}
		}
		else {
			if (SIZE == length) {
				row = 0;
				col = rand() % SIZE;
			}
			else {
				row = rand() % (SIZE - length);
				col = rand() % SIZE;
			}
		}
		init_coord = (row * SIZE) + col;
	}

	//check possible coordinates against occupied space
	bool is_occupied(int coord, int num) {
		for (int i = 0; i < num; i++) {
			if (coord == taken_coords[i]) {return true;}
		}
		return false;
	}
};

Ship* create_ships() {
	//for index position/count of taken_coords
	int count = 0;
	int temp;
	Ship *ships;
	ships = new Ship[5];
	//aircraft carrier
	Ship aircraft_carrier;
	aircraft_carrier.construct(5, "Aircraft carrier");
	aircraft_carrier.collect_taken(count);
	temp = aircraft_carrier.inc_count(count);
	count = temp;

	//battleship
	Ship battleship;
	battleship.construct(4, "Battleship");
	while (battleship.is_valid(count) != true) {
		battleship.populate();
	}
	battleship.collect_taken(count);
	temp = battleship.inc_count(count);
	count = temp;

	//submarine
	Ship submarine;
	submarine.construct(3, "Submarine");
	while (submarine.is_valid(count) != true) {
		submarine.populate();
	}
	submarine.collect_taken(count);
	temp = submarine.inc_count(count);
	count = temp;

	//destroyer
	Ship destroyer;
	destroyer.construct(3, "Destroyer");
	while (destroyer.is_valid(count) != true) {
		destroyer.populate();
	}
	destroyer.collect_taken(count);
	temp = destroyer.inc_count(count);
	count = temp;

	//patrol boat
	Ship patrol_boat;
	patrol_boat.construct(2, "Patrol boat");
	while (patrol_boat.is_valid(count) != true) {
		patrol_boat.populate();
	}
	
	//delete "taken_coords"
	delete[] taken_coords;
	taken_coords = 0;
	
	//assemble ships
	ships[0] = aircraft_carrier;
	ships[1] = battleship;
	ships[2] = submarine;
	ships[3] = destroyer;
	ships[4] = patrol_boat;
	
	if (DEBUG) {cout << "\nShips assembled" << endl << endl;}
	
	return ships;
}

//test ships - DEBUGGING FUNCTION
void test_ships(Ship *ships) {
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < ships[i].get_length(); j++) {
			cout << "ships[" << i << "].get_coord(" << j
			<< ") == " << ships[i].get_coord(j) << endl;
		}
	}
}

//place ships on boards
void populate_board(Board board, Ship *ships) {
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < ships[i].get_length(); j++) {
			board.replace(ships[i].get_coord(j), 'S');
		}
	}
}

//establishes win condition
bool player_wins(Ship *ships) {
	for (int i = 0; i < 5; i++) {
		if (ships[i].is_empty() == false) {
			return false;
		}
	}
	return true;
}

bool player_turn(Board ship_board, Board guess_board, string player_name, Ship *ships) {
	cout << player_name << "'s turn:" << endl;
	
	//status of destroyed ships
	for (int i = 0; i < 5; i++) {
		if (ships[i].is_empty()) {
			cout << ships[i].get_name() << " is destroyed!" << endl;
		}
	}
	
	//displays the guess board
	guess_board.print_board();
	
	//collect together a guess coord
	int row, col, guess;
	cout << "Guess Row: ";
	cin >> row;
	cout << "Guess Col: ";
	cin >> col;
	guess = (row - 1) * SIZE + (col - 1);
	
	//verifies that input coords are valid and weren't already chosen
	while (guess_board.is_valid(guess) == false || guess_board.already_tried(guess)) {
		if (guess_board.is_valid(guess) == false) {
			cout << "Oops, that's not even in the ocean." << endl;
		}
		else if (guess_board.already_tried(guess)) {
			cout << "You guessed that one already." << endl;
		}
		cout << "Guess Row: ";
		cin >> row;
		cout << "Guess Col: ";
		cin >> col;
		guess = (row - 1) * SIZE + (col - 1);
	}
	
	//check if scoring occurs
	//scoring a hit
	if (ship_board.is_a_ship(guess)) {
		cout << "You scored a hit!" << endl;
		guess_board.replace(guess, '*');
		
		//update ships
		for (int i = 0; i < 5; i++) {
			if (ships[i].matches_coord(guess)) {
				if (DEBUG) {cout << ships[i].get_name() << " is hit!" << endl;}
				ships[i].damage(guess);
			}
		}
		
		//win condition
		if (player_wins(ships)) {return true;}
	}
	
	//miss logic
	else {
		cout << "You missed my battleship!" << endl;
		guess_board.replace(guess, 'X');
	}
	
	//assuming no scoring occurs....
	return false;
}

//main program
int main() {
	//required to generate a different random number
	//each time the function runs
	srand(time(0));
	
	//creates user boards
	Board p1_guess_board;
	Board p2_guess_board;
	Board p1_ship_board;
	Board p2_ship_board;
	
	//set up Player 1's ships
	Ship *p1_ships = create_ships();
	if (DEBUG) {test_ships(p1_ships);}
	
	//set up Player 2's ships
	Ship *p2_ships = create_ships();
	if (DEBUG) {test_ships(p2_ships);}

	populate_board(p1_ship_board, p1_ships);
	populate_board(p2_ship_board, p2_ships);
	
	if (DEBUG) {
		cout << "\nShip board for Player 1: " << endl;
		p1_ship_board.print_board();
		cout << "\nShip board for PLayer 2: " << endl;
		p2_ship_board.print_board();
	}

	//Get player names
	string player1, player2;
	cout << "What's the first player's name? ";
	cin >> player1;
	cout << "What's the second player's name? ";
	cin >> player2;

	bool has_won = false;
	while (has_won == false) {
		has_won = player_turn(p2_ship_board, p1_guess_board, player1, p2_ships);
		if (has_won) {
			cout << "You've destroyed all battleships!" << endl;
			cout << player1 << " has won the game!" << endl;
		}
		else {
			has_won = player_turn(p1_ship_board, p2_guess_board, player2, p1_ships);
			if (has_won) {
				cout << "You've destroyed all battleships!" << endl;
				cout << player2 << " has won the game!" << endl;
			}
		}
	}
	return 0;
}