import java.util.Scanner; //Scanner is used for gathering input from the user during program run

class Global {
	public static int SIZE = 5;
	public static int[] taken_coords;
}

class Board {
	public Board() {
		board = new char[Global.SIZE * Global.SIZE];
		create_board();
	}
	
	//assembles the array into a printable format
	public void print_board() {
		for (int i = 0; i < Global.SIZE; i++) {
			for (int j = 0; j < Global.SIZE; j++) {
				System.out.print(board[i * Global.SIZE + j] + " ");
			}
			System.out.println();
		}
	}
	
	//replaces target coord to input char
	public void replace(int coord, char replacement) {board[coord] = replacement;}
	
	//determines if coord is occupied by a ship
	public boolean is_a_ship(int coord) {
		if (board[coord] == 'S') {return true;}
		else {return false;}
	}
	
	//determines if coord was already tried
	public boolean already_tried(int coord) {
		if (board[coord] == 'X' || board[coord] == '*') {return true;}
		else {return false;}
	}
	
	//determines if coord is on the board
	public boolean is_valid(int coord) {
		if (coord < 0 || coord >= board.length) {return false;}
		else {return true;}
	}
	
	private char[] board;
	
	private void create_board() {
		for (int i = 0; i < board.length; i++) {board[i] = 'O';}
	}
}

class Ship {
	public Ship() {}
	
	//takes over to "initialize" unique parameters of the ship
	public void construct(int ship_length, String ship_name) {
		name = ship_name;
		length = ship_length;
		ship = new int[length];
		populate();
	}
	
	//populate ship indices with "coordinates" (row * Global.SIZE) + col
	public void populate() {
		det_direction();
		det_init_coord();
		ship[0] = init_coord;
		if (horizontal == false) {
			if (init_coord < Global.SIZE * Global.SIZE - (length - 1)) {
				for (int i = 1; i < length; i++) {
					ship[i] = init_coord + Global.SIZE * i;
				}
			}
			else {System.out.println("Something went wrong in populate()");}
		}
		else {
			for (int i = 1; i < length; i++) {ship[i] = init_coord + i;}
		}
	}
	
	public boolean is_empty() {
		if (length == 0) {return true;}
		else {return false;}
	}
	
	//validate created ship
	public boolean is_valid() {
		for (int i = 0; i < length; i++) {
			if (is_occupied(ship[i])) {return false;}
		}
		return true;
	}
	
	//finds the ship that contains target coord
	public boolean matches_coord(int coord) {
		for (int i = 0; i < length; i++) {
			if (ship[i] == coord) {return true;}
		}
		return false;
	}
	
	//adds to list of occupied coordinates
	public void collect_taken() {
		int num = Global.taken_coords.length; //original taken_coords length
		
		//grab what the coords were
		int[] temp = new int[num];
		for (int i = 0; i < num; i++) {temp[i] = Global.taken_coords[i];}
		
		//set the new length of the array to include the new ship
		Global.taken_coords = new int[length + num];
		
		//put back the old values
		for (int i = 0; i < num; i++) {Global.taken_coords[i] = temp[i];}
		
		//add the new values
		for (int i = 0; i < length; i++) {Global.taken_coords[num + i] = ship[i];}
	}
	
	//first use of "collect_taken"
	public void first_taken() {
		Global.taken_coords = new int[length];
		for (int i = 0; i < length; i++) {Global.taken_coords[i] = ship[i];}
	}
	
	//remove damaged part of the ship
	public void damage(int coord) {
		//decrement by one to create new length of damaged ship
		length -= 1;
		
		//only applicable if length is still positive
		if (length > 0) {
			int[] temp = new int[length];
			
			//sets counter to properly set indices of temp
			int count = 0;
			
			//only moves over undamaged parts of the ship to temp
			for (int i = 0; i < (length + 1); i++) {
				if (ship[i] != coord) {
					temp[count] = ship[i];
					count += 1;
				}
			}

			//erases and sets updated length to the ship
			ship = new int[length];
			
			//moves coords back to the ship for future reference
			for (int i = 0; i < length; i++) {ship[i] = temp[i];}
		}
	}
	
	//GET FUNCTIONS
	public int get_coord(int x) {return ship[x];}
	public int[] get_ship() {return ship;}
	public int get_length() {return length;}
	public String get_name() {return name;}
	
	//DEBUGGING FUNCTIONS
	//outputs coordinates for each ship chunk
	public void print_ship() {
		System.out.print("[" + ship[0]);
		for (int i = 1; i < length; i++) {
			System.out.print(", " + ship[i]);
		}
		System.out.print("]");
		System.out.println();
	}
	
	private boolean horizontal;
	private int init_coord;
	private int length;
	private String name;
	private int[] ship;
	
	//horizontal = 0, vertical = 1
	private void det_direction() {
		int num = (int)(Math.random() * 2);
		if (num == 0) {horizontal = true;}
		else {horizontal = false;}
	}
	
	//randomly generates a starting coord for the ship
	private void det_init_coord() {
		int row, col;
		if (horizontal) {
			if (Global.SIZE == length) {
				row = (int)(Math.random() * Global.SIZE);
				col = 0;
			}
			else {
				row = (int)(Math.random() * Global.SIZE);
				col = (int)(Math.random() * (Global.SIZE - length));
			}
		}
		else {
			if (Global.SIZE == length) {
				row = 0;
				col = (int)(Math.random() * Global.SIZE);
			}
			else {
				row = (int)(Math.random() * (Global.SIZE - length));
				col = (int)(Math.random() * Global.SIZE);
			}
		}
		init_coord = (row * Global.SIZE) + col;
	}
	
	//check possible coordinates against occupied space
	private boolean is_occupied(int coord) {
		for (int i = 0; i < Global.taken_coords.length; i++) {
			if (coord == Global.taken_coords[i]) {return true;}
		}
		return false;
	}
}

public class Main {
	public static Ship[] create_ships() {
		Ship[] ships = new Ship[5];
		
		//aircraft carrier
		Ship aircraft_carrier = new Ship();
		aircraft_carrier.construct(5, "Aircraft carrier");
		aircraft_carrier.first_taken();
	
		//battleship
		Ship battleship = new Ship();
		battleship.construct(4, "Battleship");
		while (battleship.is_valid() != true) {battleship.populate();}
		battleship.collect_taken();

		//submarine
		Ship submarine = new Ship();
		submarine.construct(3, "Submarine");
		while (submarine.is_valid() != true) {submarine.populate();}
		submarine.collect_taken();
	
		//destroyer
		Ship destroyer = new Ship();
		destroyer.construct(3, "Destroyer");
		while (destroyer.is_valid() != true) {destroyer.populate();}
		destroyer.collect_taken();

		//patrol boat
		Ship patrol_boat = new Ship();
		patrol_boat.construct(2, "Patrol boat");
		while (patrol_boat.is_valid() != true) {patrol_boat.populate();}
		
		//assemble ships
		ships[0] = aircraft_carrier;
		ships[1] = battleship;
		ships[2] = submarine;
		ships[3] = destroyer;
		ships[4] = patrol_boat;
		
		return ships;
}

	//place ships on boards
	public static void populate_board(Board board, Ship[] ships) {
		for (int i = 0; i < ships.length; i++) {
			for (int j = 0; j < ships[i].get_length(); j++) {
				board.replace(ships[i].get_coord(j), 'S');
			}
		}
	}

	//establishes win condition
	public static boolean player_wins(Ship[] ships) {
		for (int i = 0; i < ships.length; i++) {
			if (ships[i].is_empty() == false) {return false;}
		}
		return true;
	}

	public static boolean player_turn(Board ship_board, Board guess_board, String player_name, Ship[] ships) {
		System.out.println(player_name + "'s turn:");
	
		//status of destroyed ships
		for (int i = 0; i < ships.length; i++) {
			if (ships[i].is_empty()) {
				System.out.println(ships[i].get_name() + " is destroyed!");
			}
		}
	
		//displays the guess board
		guess_board.print_board();
	
		//collect together a guess coord
		int row, col, guess;
		Scanner sc = new Scanner(System.in);
		System.out.print("Guess Row: ");
		row = sc.nextInt();
		System.out.print("Guess Col: ");
		col = sc.nextInt();
		guess = (row - 1) * Global.SIZE + (col - 1);
	
		//verifies that input coords are valid and weren't already chosen
		while (guess_board.is_valid(guess) == false || guess_board.already_tried(guess)) {
			if (guess_board.is_valid(guess) == false) {
				System.out.println("Oops, that's not even in the ocean.");
			}
			else if (guess_board.already_tried(guess)) {
				System.out.println("You guessed that one already.");
			}
			System.out.print("Guess Row: ");
			row = sc.nextInt();
			System.out.print("Guess Col: ");
			col = sc.nextInt();
			guess = (row - 1) * Global.SIZE + (col - 1);
		}
	
		//check if scoring occurs
		//scoring a hit
		if (ship_board.is_a_ship(guess)) {
			System.out.println("You scored a hit!");
			guess_board.replace(guess, '*');
		
			//update ships
			for (int i = 0; i < ships.length; i++) {
				if (ships[i].matches_coord(guess)) {ships[i].damage(guess);}
			}
		
			//win condition
			if (player_wins(ships)) {return true;}
		}
	
		//miss logic
		else {
			System.out.println("You missed my battleship!");
			guess_board.replace(guess, 'X');
		}
		
		//assuming no scoring occurs....
		return false;
	}
	
	public static void main(String[] args) {
		//creates user boards
		Board p1_guess_board = new Board();
		Board p2_guess_board = new Board();
		Board p1_ship_board = new Board();
		Board p2_ship_board = new Board();
	
		//set up Player 1's ships
		Ship[] p1_ships = new Ship[5];
		p1_ships = create_ships();

		//set up Player 2's ships
		Ship[] p2_ships = new Ship[5];
		p2_ships = create_ships();

		populate_board(p1_ship_board, p1_ships);
		populate_board(p2_ship_board, p2_ships);
	
		//get player names
		String player1, player2;
		Scanner sc = new Scanner(System.in);
		System.out.print("What's the first player's name? ");
		player1 = sc.nextLine();
		System.out.print("What's the second player's name? ");
		player2 = sc.nextLine();
		
		boolean has_won = false;
		while (has_won == false) {
			has_won = player_turn(p2_ship_board, p1_guess_board, player1, p2_ships);
			if (has_won) {
				System.out.println("You've destroyed all battleships!");
				System.out.println(player1 + " has won the game!");
			}
			else {
				has_won = player_turn(p1_ship_board, p2_guess_board, player2, p1_ships);
				if (has_won) {
					System.out.println("You've destroyed all battleships!");
					System.out.println(player2 + " has won the game!");
				}
			}
		}
	}
}