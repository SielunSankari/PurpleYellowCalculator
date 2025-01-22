import customtkinter as ctk
import random
from itertools import chain
import ctypes
import os

# Color Palette for the Application
PURPLE = "#9966CC"
YELLOW = "#FFCF40"
LABEL_COLOR = "#141414"
WHITE = "#FFFFFF"
OFF_WHITE = "#DCDCDC"

# Font Styles for the Application
SMALL_FONT_STYLE = ("Arial", 18)
LARGE_FONT_STYLE = ("Arial", 40)
DIGITS_FONT_STYLE = ("Arial", 25, "bold")
DEFAULT_FONT_STYLE = ("Arial", 25,  "bold")

class Calculator:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator By Batyrzhan (@SielunSankari)")

        # Error message to display when there is an invalid operation
        self.ERROR_MESSAGE = "ERROR (￢_￢;)"

        # Set the path to the calculator icon
        ICON_PATH = os.path.join(os.path.dirname(__file__), "../assets/calculator_icon.ico")
        # Create the full path to the icon file located in the 'assets' folder

        # Set the application ID for Windows taskbar icon grouping
        app_id = "com.batyrzhan.calculator"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)  # Set the app's ID for better taskbar integration

        # Set the window icon for the calculator using the icon path
        self.window.iconbitmap(ICON_PATH)  # Apply the icon to the window

        # Initialize with a random emotion to display at the start
        self.current_expression = self.get_random_emotion()

        self.total_expression = ""
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        # Dictionary to map digits and the decimal point to grid positions on the calculator
        self.digits = {
            7: (1, 1),  8: (1, 2),  9: (1, 3),
            4: (2, 1),  5: (2, 2),  6: (2, 3),
            1: (3, 1),  2: (3, 2),  3: (3, 3),
            0: (4, 2),  '.': (4, 1),
        }

        # Dictionary to map operation symbols to their Unicode equivalents
        self.operations = {
            "/": "\u00F7",  # Division symbol (÷)
            "*": "\u00D7",  # Multiplication symbol (×)
            "+": "+",
            "-": "-",
        }

       # Create the frame that will hold the calculator buttons
        self.buttons_frame = self.create_buttons_frame()

        # Configure the first row to expand equally when the window is resized
        self.buttons_frame.rowconfigure(0, weight=1)

        # Loop through rows and columns to configure the grid layout of buttons
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)  # Allow rows 1 to 4 to expand equally
            self.buttons_frame.columnconfigure(x, weight=1)  # Allow columns 1 to 4 to expand equally

        # Create digit buttons (0-9)
        self.create_digit_buttons()

        # Create operator buttons (+, -, *, /)
        self.create_operator_buttons()

        # Create special buttons (e.g., clear, equals, etc.)
        self.create_special_buttons()

        # Bind keyboard keys for easy input using the keyboard
        self.bind_keys()

    # Returns a random emotion from the list
    def get_random_emotion(self):
        self.emotions = [
            "(¬‿¬)",
            "(:>)",
            "(≧◡≦)",
            "(^_^)",
            "(｡♥‿♥｡)",
            "(≧ω≦)",
            "(❁´◡`❁)",
            "(≧∇≦)/",
            "(｡•́‿•̀｡)",
            "(･ω･)",
            "(˘︶˘).｡.:*♡",
            "(´∩｡• ᵕ •｡∩`)",
            "(✧ω✧)",
        ]
        return random.choice(self.emotions)

    # Checks if the current expression is valid (not an error message)
    def is_valid_expression(self):
        return self.current_expression != self.ERROR_MESSAGE

    def bind_keys(self):
        # Binding for the Enter key to evaluate the expression
        self.window.bind("<Return>", lambda event: self.evaluate() if self.is_valid_expression() else self.clear())

        # Binding for the digits
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit) if self.is_valid_expression() else self.clear())

        # Binding for the operators (+-×÷)
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator) if self.is_valid_expression() else self.clear())

        # Binding for the "CE" (Backspace) key
        self.window.bind("<BackSpace>", lambda event: self.clear_entry() if self.is_valid_expression() else self.clear())

        # Binding for the "C" (Escape) key
        self.window.bind("<Escape>", lambda event: self.clear())

    # Create special buttons like Clear, Equals, Square, and Square Root
    def create_special_buttons(self):
        self.create_clear_entry_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    # Create the labels to display the total and current expressions on the calculator screen
    def create_display_labels(self):
        total_label = ctk.CTkLabel(self.display_frame, text=self.total_expression, anchor="e", bg_color=LABEL_COLOR, text_color=WHITE, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = ctk.CTkLabel(self.display_frame, text=self.current_expression, anchor="e", bg_color=LABEL_COLOR, text_color=WHITE, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        return total_label, label

    # Create the frame that holds the display area of the calculator
    def create_display_frame(self):
        frame = ctk.CTkFrame(self.window, height=221, fg_color=OFF_WHITE)
        frame.pack(expand=True, fill="both")
        return frame

    # Add a value to the current expression and update the display
    def add_to_expression(self, value):
        if self.current_expression in (self.ERROR_MESSAGE, "0.0", "0", *chain(self.emotions)):
            self.clear()
        if self.current_expression in ("0.0", "0", *chain(self.emotions)):
            self.current_expression = ""
        self.current_expression += str(value)
        self.update_label()

    # Create digit buttons (0-9 and '.')
    def create_digit_buttons(self):
        for digit, grid_values in self.digits.items():
            button = ctk.CTkButton(self.buttons_frame, text=str(digit), fg_color=WHITE, text_color=LABEL_COLOR, font=DIGITS_FONT_STYLE, corner_radius=0, border_width=0, hover_color=OFF_WHITE, command=lambda digit_value=digit: self.add_to_expression(digit_value))
            button.grid(row=grid_values[0], column=grid_values[1], sticky="nsew")

    # Append the operator to the expression and update the display
    def append_operator(self, operator):
        if self.current_expression in (self.ERROR_MESSAGE, *chain(self.emotions)):
            self.current_expression = "0"
            self.clear()
        if not self.current_expression and not self.total_expression:
            return
        if not self.current_expression and self.total_expression[-1] in self.operations:
            self.total_expression = self.total_expression[:-1] + operator
        else:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # Create operator buttons (+, -, *, /)
    def create_operator_buttons(self):
        row_index = 0
        for operator, symbol in self.operations.items():
            button = ctk.CTkButton(self.buttons_frame, text=symbol, fg_color=PURPLE, text_color=WHITE, font=DEFAULT_FONT_STYLE, corner_radius=0, border_width=0, hover_color=LABEL_COLOR, command=lambda operator_symbol=operator: self.append_operator(operator_symbol))
            button.grid(row=row_index, column=4, sticky="nsew")
            row_index += 1

    # Clears the current and total expressions and updates the display
    def clear(self):
        self.current_expression = "0.0"
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    # Clears the last entry in the current expression
    def clear_entry(self):
        if len(self.current_expression) > 1 and self.current_expression not in (self.ERROR_MESSAGE, "0.0", "0", *chain(self.emotions)):
            self.current_expression = self.current_expression[:-1]
        else:
            self.current_expression = "0.0"
        self.update_label()

    def create_clear_entry_button(self):
        button = ctk.CTkButton(self.buttons_frame, text="CE", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.clear_entry)
        button.grid(row=0, column=1, sticky="nsew")

    # Squares the current expression value
    def square(self):
        try:
            value = float(self.current_expression)
            self.current_expression = str(round(value**2, 4))
        except ValueError:
            self.current_expression = self.ERROR_MESSAGE
            self.update_label()
            self.wait_for_key_press()
        else:
            self.update_label()

    def create_square_button(self):
        button = ctk.CTkButton(self.buttons_frame, text="x²", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.square)
        button.grid(row=0, column=2, sticky="nsew")

    # Calculates the square root of the current expression value
    def sqrt(self):
        try:
            value = float(self.current_expression)
            if value < 0:
                raise ValueError("Square root of negative number is not possible")
            self.current_expression = str(round(value**0.5, 4))
        except ValueError as e:
            self.current_expression = self.ERROR_MESSAGE
            self.update_label()
            self.wait_for_key_press()
        else:
            self.update_label()

    def create_sqrt_button(self):
        button = ctk.CTkButton(self.buttons_frame, text="√x", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky="nsew")

    # Evaluates the total expression and updates the result or shows error if invalid
    def evaluate(self):
        if self.current_expression == self.ERROR_MESSAGE:
            self.clear()

        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            result = eval(self.total_expression)
            self.current_expression = str(round(result, 4))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = self.ERROR_MESSAGE
            self.update_label()
            self.wait_for_key_press()
        else:
            self.update_label()

    # Creates the "=" button to trigger evaluation
    def create_equals_button(self):
        button = ctk.CTkButton(self.buttons_frame, text="=", fg_color=YELLOW, text_color=WHITE, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=LABEL_COLOR, border_width=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky="nsew")

    # Creates the frame for all the calculator buttons
    def create_buttons_frame(self):
        frame = ctk.CTkFrame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # Updates the total expression label with the current total expression
    def update_total_label(self):
        self.total_label.configure(text=self.total_expression)

    # Updates the current expression label with the current expression (up to 14 characters)
    def update_label(self):
        self.label.configure(text=self.current_expression[:14])

    # Run the calculator app
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
