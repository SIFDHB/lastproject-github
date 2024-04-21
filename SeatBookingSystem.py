import random
import string
import os
os.system("") # Enables ANSI color codes in the terminal.

# Constants
ANSI_ESCAPE = "\033[39m" # ANSI code to reset to default text color.

# ANSI escape codes of Minecraft colors
TEXT_COLORS = {
    'black': "\033[30m", 'dark_blue': "\033[34m", 'dark_green': "\033[32m", 'dark_aqua': "\033[36m",
    'dark_red': "\033[31m", 'dark_purple': "\033[35m", 'gold': "\033[33m", 'gray': "\033[37m",
    'dark_gray': "\033[90m", 'blue': "\033[94m", 'green': "\033[92m", 'aqua': "\033[96m",
    'red': "\033[91m", 'light_purple': "\033[95m", 'yellow': "\033[93m", 'white': "\033[97m",
}

def TextColor(text="", color="white", continuous=True):
    """
    Apply ANSI color coding to text for terminal display.

    Parameters:
    - text (str): The text to be colored.
    - color (str): The name of the color to apply. Must be a key in TEXT_COLORS.
    - continuous (bool): If False, do not reset color after the text. Default is True.

    Returns:
    - str: The text wrapped in ANSI escape sequences for the specified color.

    Raises:
    - ValueError: If an invalid color name is provided.
    """
    if color in TEXT_COLORS:
        return f"{TEXT_COLORS[color]}{text}{ANSI_ESCAPE if continuous else ''}"
    else:
        raise ValueError(f"Invalid color name: {color}")

class SeatBookingSystem:
    """
    A simple seat booking system for Apache Airlines.

    This system allows for checking seat availability, booking seats with customer details,
    freeing booked seats, and displaying the current booking state with color-coded output.
    """
    def __init__(self):
        # Initialize a simplified seat layout
        self.seating = [['F' for _ in range(4)] for _ in range(7)]
        self.seating[3] = ['X', 'X', 'X', 'X']  # Mark the middle row as an aisle
        self.seating[5:7] = [['F', 'F', 'S', 'S']] * 2  # Last rows with storage spaces
        self.bookings = {}  # Stores booking references and associated customer details
        # Map actions to their corresponding methods
        self.actions = {
            '1': self.check_availability,
            '2': self.book_seat,
            '3': self.free_seat,
            '4': self.show_booking_state
        }

    def generate_unique_booking_reference(self):
        """
        Generate a unique 8-character alphanumeric booking reference.

        Returns:
        - str: A unique booking reference.
        """
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            # Checks if there are no matching references
            if reference not in self.bookings:
                return reference

    def is_seat_valid(self, row:int = None, column:int = None, seat:str = None):
        """
        Check if a seat selection is valid (not an aisle or out of bounds).

        Parameters:
        - row (int): Row number of the seat.
        - column (int): Column number of the seat.
        - seat (str): Direct seat value (optional alternative to row/column).

        Returns:
        - bool: True if the seat is valid, False otherwise.
        """

        # Guard Clause #1
        # Seat-only.
        if seat is not None:
            return seat not in ('X', 'S')

        # Guard Clause #2
        # Row and Column check
        if row is None or column is None :
            raise Exception("Row and column must have a number!")

        # Finally, we check if the rows and columns are valid.
        try:
            return self.seating[row][column] not in ('X', 'S')
        except IndexError:
            return False

    def check_availability(self, row, column):
        """
        Check and return the availability of a specified seat.

        Parameters:
        - row (int): Row number of the seat.
        - column (int): Column number of the seat.

        Returns:
        - str: A message indicating whether the seat is available or not.
        """

        if not self.is_seat_valid(row, column):
            return TextColor("Invalid seat selection.", "red")

        # Check if the seat is free, reserved, or not bookable
        seat = self.seating[row][column]
        if seat == "F":
            return TextColor('Seat is available', 'green')
        else:
            # Seat is taken, show booking details
            return (TextColor('Seat is taken.\n---INFO---', 'yellow', False) +
                        ("\nReference Number: " + seat +
                         "\nPassport Number: " + self.bookings[seat]["passport_number"] +
                         "\nFirst Name: " + self.bookings[seat]["first_name"] +
                         "\nLast Name: " + self.bookings[seat]["last_name"]
                         ) + TextColor(continuous=True))

    def book_seat(self, row, column, passport_number, first_name, last_name):
        """
        Book a seat for a customer with the provided details.

        Parameters:
        - row (int): Row number of the seat.
        - column (int): Column number of the seat.
        - passport_number (str): Customer's passport number.
        - first_name (str): Customer's first name.
        - last_name (str): Customer's last name.

        Returns:
        - str: A message indicating the result of the booking attempt.
        """

        # Check if the seat is valid and available
        if not self.is_seat_valid(row, column) or self.seating[row][column] != 'F':
            return TextColor("Seat cannot be booked.", "red")

        # Generate booking reference and update system
        booking_reference = self.generate_unique_booking_reference()
        self.seating[row][column] = booking_reference
        self.bookings[booking_reference] = {
            'passport_number': passport_number,
            'first_name': first_name,
            'last_name': last_name,
            'seat_row': row,
            'seat_column': column
        }
        return TextColor(f"Seat booked successfully with reference {booking_reference}.", "green")

    def free_seat(self, row, column):
        """
        Free a previously booked seat.

        Parameters:
        - row (int): Row number of the seat.
        - column (int): Column number of the seat.

        Returns:
        - str: A message indicating whether the seat was successfully freed.
        """

        # Check if the seat is valid and available
        if not self.is_seat_valid(row, column) or self.seating[row][column] == 'F':
            return TextColor("Seat is already free or cannot be freed.", "yellow")

        # Free the seat and remove booking details
        booking_reference = self.seating[row][column]
        if booking_reference in self.bookings:
            del self.bookings[booking_reference]
            self.seating[row][column] = 'F'
            return TextColor("Seat has been freed.", "green")

        return TextColor("Booking reference not found.", "red")

    def show_booking_state(self):
        """
        Display the current booking state of all seats with color-coded output.
        """
        # Iterate through each seat to display its status
        for i, row in enumerate(self.seating):
            row_line = ""
            for x in row:
                x = "R" if self.is_seat_valid(seat=x) and x != "F" else x
                row_line += TextColor(x, "white" if x != "F" else "yellow", continuous=False) + " "
            print(row_line + TextColor(f" Row {i+1}", "white", True))

        print("F = Free, X = Aisle, S = Storage, R = Booked")

    def run(self):
        """
        Run the seat booking system, providing a menu for user interaction.
        """
        while True:
            # Display the main menu
            print(TextColor("---------- SBS CLI ----------", "yellow") + "\n1. Check seat availability\n2. Book a seat\n3. Free a seat\n4. Show booking state\n5. Exit")
            choice = input("Select an option: ")
            if choice == '5':
                break # Exit the loop and program

            # Handle the selected action based on user input
            if choice in self.actions:
                if choice in ('1', '2', '3'):

                    # Shared row-column variable getters
                    row = input("Enter row number: ")
                    column = input("Enter column number: ")
                    # Guard clause: Input validation
                    if not row.isdigit() or not column.isdigit():
                        print(TextColor("Invalid input. Row and column must be integers.", "red"))
                        continue
                    # Return the real row and column variables
                    row, column = int(row) - 1, int(column) - 1

                    if choice == '2':
                        passport_number = input("Enter passport number (1234...): ")
                        first_name = input("Enter first name: ")
                        last_name = input("Enter last name: ")
                        print(self.actions[choice](row, column, passport_number, first_name, last_name))
                    else:
                        print(self.actions[choice](row, column))

                elif choice == '4':
                    self.actions[choice]()
                input(TextColor("Press enter to continue..."))
            else:
                print(TextColor("Invalid option. Please try again.", "red"))

if __name__ == "__main__":
    booking_system = SeatBookingSystem()
    booking_system.run()