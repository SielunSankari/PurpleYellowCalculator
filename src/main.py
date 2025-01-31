import customtkinter as ctk
from asteval import Interpreter
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
    """
    The Calculator class is a graphical calculator
    created using the CustomTkinter library.
    It supports basic mathematical operations such as addition,
    subtraction, multiplication, division, squaring,
    and square root extraction.
    """

    def __init__(self):
        """
        Initializes the main application window and configures the interface settings.
        """
        self.window = ctk.CTk()
        self.window.geometry("375x667+4+4")
        self.window.resizable(0, 0)
        self.window.title("Calculator By Batyrzhan (@SielunSankari)")

        # Error message to display when there is an invalid operation
        self.ERROR_MESSAGE = "ERROR (￢_￢;)"

        # Set the path to the calculator icon
        ICON_PATH = os.path.join(os.path.dirname(__file__), "../assets/calculator_icon.ico")
        app_id = "com.batyrzhan.calculator"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)  # Set the app's ID for better taskbar integration
        self.window.iconbitmap(ICON_PATH)  # Apply the icon to the window

        # Initialize with a random emotion to display at the start
        self.current_expression = self.get_random_emotion()
        self.total_expression = ""

        # Create the display frame and labels
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

        # Create the buttons frame and add all the buttons
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
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

    def get_random_emotion(self):
        """
        Returns a random emoticon to display at the start of the application.
        """
        self.emotions = [
            "(¬‿¬)",
            ":>",
            "(≧◡≦)",
            "(^_^)",
            "(｡♥‿♥｡)",
            "(≧ω≦)",
            "(≧∇≦)/",
            ":3",
            "(˘︶˘).｡.:*♡",
            "(✧ω✧)",
            "(,,>﹏<,,)",
            "(˶ᵔ ᵕ ᵔ˶)",
        ]
        return random.choice(self.emotions)

    def is_valid_expression(self):
        """
        Checks if the current expression is valid (not an error message).
        """
        return self.current_expression != self.ERROR_MESSAGE

    def bind_keys(self):
        """
        Binds keyboard keys to the corresponding actions.
        """
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

    def create_special_buttons(self):
        """
        Creates special calculator buttons:
        - CE (Clear Entry)
        - = (Equals)
        - x² (Square)
        - √x (Square Root)
        """
        self.create_clear_entry_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        """
        Creates labels to display the current and total expressions on the calculator screen.
        - total_label: Displays the total expression (e.g., "12 + 17").
        - label: Displays the current value or result.
        """
        total_label = ctk.CTkLabel(self.display_frame, text=self.total_expression, anchor="e", bg_color=LABEL_COLOR, text_color=WHITE, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = ctk.CTkLabel(self.display_frame, text=self.current_expression, anchor="e", bg_color=LABEL_COLOR, text_color=WHITE, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        return total_label, label

    def create_display_frame(self):
        """
        Creates frames for the area of expressions displayed on the calculator.
        This frame contains tags for current and general expressions.
        """
        frame = ctk.CTkFrame(self.window, height=221, fg_color=OFF_WHITE)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        """
        Adds a value (digit or dot) to the current expression.
        If the current expression is a mistake or contains an emotion, it is cleared.
        Checks the correctness of adding a decimal point.
        """
        if self.current_expression in (self.ERROR_MESSAGE, *chain(self.emotions)):
            self.clear()

        if self.current_expression in ("0"):
            if value == "0":
                return
            elif value == ".":
                self.current_expression = "0"
            else:
                self.current_expression = str(value)
                self.update_label()
                return

        if value == ".":
            if not self.current_expression or self.current_expression[-1] in self.operations:
                self.current_expression = "0"
            elif "." in self.current_expression:
                return

        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        """
        Creates buttons for numbers (0-9) and decimal points.
        Each button is associated with the method add_to_expression.
        """
        for digit, grid_values in self.digits.items():
            button = ctk.CTkButton(self.buttons_frame, text=str(digit), fg_color=WHITE, text_color=LABEL_COLOR, font=DIGITS_FONT_STYLE, corner_radius=0, border_width=0, hover_color=OFF_WHITE, command=lambda digit_value=digit: self.add_to_expression(digit_value))
            button.grid(row=grid_values[0], column=grid_values[1], sticky="nsew")

    def append_operator(self, operator):
        """
        Appends an operator to the current expression.
        If the current expression is a mistake or emotion, it is cleared.
        """
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

    def create_operator_buttons(self):
        """
        Creates buttons for operators (+, -, *, /).
        Each button is associated with the method append_operator.
        """
        row_index = 0
        for operator, symbol in self.operations.items():
            button = ctk.CTkButton(self.buttons_frame, text=symbol, fg_color=PURPLE, text_color=WHITE, font=DEFAULT_FONT_STYLE, corner_radius=0, border_width=0, hover_color=LABEL_COLOR, command=lambda operator_symbol=operator: self.append_operator(operator_symbol))
            button.grid(row=row_index, column=4, sticky="nsew")
            row_index += 1

    def clear(self):
        """
        Clears the current expression and total expression.
        Sets the starting value of "0" for the current expression.
        """
        self.current_expression = "0"
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    def clear_entry(self):
        """
        Removes the last character from the current expression.
        If empty, sets the value to "0".
        """
        if len(self.current_expression) > 1 and self.current_expression not in (self.ERROR_MESSAGE, "0", *chain(self.emotions)):
            self.current_expression = self.current_expression[:-1]
        else:
            self.current_expression = "0"

        self.update_label()

    def create_clear_entry_button(self):
        """
        Creates a "CE" (Clear Entry) button to delete the last character.
        """
        button = ctk.CTkButton(self.buttons_frame, text="CE", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.clear_entry)
        button.grid(row=0, column=1, sticky="nsew")

    def square(self):
        """
        Calculates the square of the current expression.
        If the expression is incorrect, an error message is displayed.
        """
        try:
            value = float(self.current_expression)
            self.current_expression = str(round(value**2, 2))
        except ValueError:
            self.current_expression = self.ERROR_MESSAGE
            self.update_label()
        else:
            self.update_label()

    def create_square_button(self):
        """
        Creates the "x²" button to calculate the square of the current value.
        """
        button = ctk.CTkButton(self.buttons_frame, text="x²", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.square)
        button.grid(row=0, column=2, sticky="nsew")

    def sqrt(self):
        """
        Calculates the square root of the current expression.
        If the expression is incorrect or the number is negative, an error message is displayed.
        """
        try:
            value = float(self.current_expression)
            if value < 0:
                raise ValueError("Square root of negative number is not possible")
            self.current_expression = str(round(value**0.5, 2))
        except ValueError as e:
            self.current_expression = self.ERROR_MESSAGE
            self.update_label()
        else:
            self.update_label()

    def create_sqrt_button(self):
        """
        Creates the "√x" button to calculate the square root of the current value.
        """
        button = ctk.CTkButton(self.buttons_frame, text="√x", fg_color=WHITE, text_color=LABEL_COLOR, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=OFF_WHITE, border_width=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky="nsew")

    def evaluate(self):
        """
        Calculates the result of the total expression.
        Uses a safe interpreter to evaluate the expression.
        If the expression is invalid, displays an error message.
        """
        if self.current_expression == self.ERROR_MESSAGE:
            self.clear()
            return

        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            aeval = Interpreter()
            result = aeval(self.total_expression)
            if isinstance(result, (int, float)):
                self.current_expression = str(round(result, 2))
                self.total_expression = ""
            else:
                raise ValueError("Invalid result")
        except Exception:
            self.current_expression = self.ERROR_MESSAGE
        finally:
            self.update_label()

    def create_equals_button(self):
        """
        Creates the "=" (Equal) button to calculate the result of the total expression.
        """
        button = ctk.CTkButton(self.buttons_frame, text="=", fg_color=YELLOW, text_color=WHITE, font=DEFAULT_FONT_STYLE, corner_radius=0, hover_color=LABEL_COLOR, border_width=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky="nsew")

    def create_buttons_frame(self):
        """
        Creates a frame for all the calculator buttons.
        """
        frame = ctk.CTkFrame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        """
        Updates the label with the total expression.
        """
        self.total_label.configure(text=self.total_expression)

    def update_label(self):
        """
        Updates the label with the current expression.
        """
        self.label.configure(text=self.current_expression)

    def run(self):
        """
        Runs the main application window.
        """
        self.window.mainloop()

if __name__ == "__main__":
    """
    Main entry point for the calculator application.
    Creates an instance of the Calculator class and runs the main application window.
    """
    calc = Calculator()
    calc.run()

# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠜⠳⣄
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⠁⠀⠀⠘⢳⡀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠹⣆
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⣠⡀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠒⠒⠋⠋⢹⡟⣦⣴⡄
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡖⠀⠀⠀⢺⡍⠁⠀⢀⡤⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⡧⣦
# ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠷⠆⠀⠴⠯⡄⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢩⣉⠙⠒⠒⠤⢤⣀⡀
# ⠀⠀⠀⠀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⢠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠈⠉⠓⠢⢤⣀
# ⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⢻⣿⣿⣿⣷⣤⣠⡤⠋⢀⠀⠀⣤⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟
# ⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣼⣿⣿⣿⣿⣿⡉⠁⣴⡦⣜⡌⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⢀⡴⠃
# ⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡌⠢⠌⠵⠁⠀⠀⠀⠀⠀⠧⢴⣄⠀⠀⠀⠀⠀⢠⣶⣆⠀⠀⠀⢰⡄⠀⢀⣠⠴⠋
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣽⣿⣿⣿⣿⣿⣿⣄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠹⠿⠟⠀⡀⢀⢸⡆⣸⡏
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣷⣰⣬⢸⣷⠃⠁
# ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠴⢚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠢⠽⢎⠹⣟⠒⠦⣄⡀
# ⠀⠀⠀⠀⠀⠀⡶⠏⠁⠀⠀⠈⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⢀⡸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡷⣎⠁⠀⠀⠉⠷⣆
# ⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⣠⠞⠁⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⡴⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠤⠤⠞⠃⠈⢢⡄
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿
# ⢠⣴⣿⣿⣿⣿⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠚⠛⠉⠙⠳⣀
# ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⢰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⣀⡀ ⠳
# ⠀⠉⠁⠈⠈⠙⢿⣿⣿⣿⣿⣿⣄⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡄⠀⠀⢀⡼⠁⠀⠀⠀⣠⠖⠋⠁⠉⠉
# ⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣆⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⠃⠀⠀⠀⠀⠀⠸⢠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⡾⠁⠀⠀⣠⠞⠁
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡁⠀⠀⣰⠃
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⣰⠃
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢏⡏
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢹⡀⠀⠀⠀⠀⢤⣀⡄⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠋
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⡈⣟⡄⠀⠀⠀⣠⠉⠀⠀⠀⠀⠀⠀⢀⣠⠞⠁
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠻⠿⠿⠿⠟⠛⠛⠻⠿⠟⠛⠉⠙⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠚⠒⠋⠙⠓⠶⠤⠖⠓⠢⠦⠤⠤⠤⠖⠒⠋

# ──────███─█──█─████─█──█─█──█─███────███─████─████────████─███─████─████──███─█──█─████
# ───────█──█──█─█──█─██─█─█─█──█──────█───█──█─█──█────█──█─█───█──█─█──██──█──██─█─█───
# ───────█──████─████─█─██─██───███────███─█──█─████────████─███─████─█──██──█──█─██─█─██
# ───────█──█──█─█──█─█──█─█─█────█────█───█──█─█─█─────█─█──█───█──█─█──██──█──█──█─█──█
# ───────█──█──█─█──█─█──█─█──█─███────█───████─█──█────█──█─███─█──█─████──███─█──█─████