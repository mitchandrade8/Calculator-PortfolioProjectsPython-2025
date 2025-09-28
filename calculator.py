import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    """
    A professional-looking GUI calculator application using Tkinter,
    now using a high-contrast, light theme for maximum visibility.
    """
    def __init__(self, master):
        self.master = master
        master.title("Python Pro Calculator")
        
        # Disable resizing for a fixed, clean calculator layout
        master.resizable(False, False)
        
        # --- High-Contrast Light Color Palette ---
        self.light_bg = '#FFFFFF'     # Main background (Pure White)
        self.display_bg = '#444444'  # Display area background (Dark Slate)
        self.num_btn_color = '#F0F0F0' # Number button color (Very light gray)
        self.op_btn_color = '#4CAF50'  # Operator button color (Green accent)
        self.eq_btn_color = '#FF9800'  # Equals button color (Orange accent)
        self.text_color_dark = 'black' # Text color for light backgrounds
        self.text_color_light = 'white' # Text color for dark backgrounds
        
        master.configure(bg=self.light_bg)

        # State variable for the calculator display
        self.current_expression = ""
        self.display_text = tk.StringVar(master, value="0")

        # --- Display Setup ---
        self.display = tk.Entry(
            master, 
            textvariable=self.display_text, 
            font=('Inter', 30, 'bold'), 
            bd=0, 
            bg=self.display_bg, 
            fg=self.text_color_light, # White text on dark display
            justify='right',
            relief='flat'
        )
        # Span the display across all 4 columns at the top
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", ipadx=8, ipady=10, padx=10, pady=(10, 5))

        # --- Button Layout Definition ---
        buttons = [
            # Row 1 (Clear and Parenthesis use light text on dark colors)
            ('C', 1, 0, self.eq_btn_color), ('(', 1, 1, self.op_btn_color), (')', 1, 2, self.op_btn_color), ('/', 1, 3, self.op_btn_color),
            # Row 2 (Numbers use dark text on light color)
            ('7', 2, 0, self.num_btn_color), ('8', 2, 1, self.num_btn_color), ('9', 2, 2, self.num_btn_color), ('*', 2, 3, self.op_btn_color),
            # Row 3
            ('4', 3, 0, self.num_btn_color), ('5', 3, 1, self.num_btn_color), ('6', 3, 2, self.num_btn_color), ('-', 3, 3, self.op_btn_color),
            # Row 4
            ('1', 4, 0, self.num_btn_color), ('2', 4, 1, self.num_btn_color), ('3', 4, 2, self.num_btn_color), ('+', 4, 3, self.op_btn_color),
            # Row 5
            ('0', 5, 0, self.num_btn_color), ('.', 5, 1, self.num_btn_color), ('=', 5, 2, self.eq_btn_color, 2) # Equals spans 2 columns
        ]

        # --- Button Creation Loop ---
        for (text, r, c, color, span) in [(t[0], t[1], t[2], t[3], t[4] if len(t) > 4 else 1) for t in buttons]:
            self.create_button(text, r, c, color, span)

        # Ensure columns and rows expand nicely
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(1, 6):
            master.grid_rowconfigure(i, weight=1)

    def create_button(self, text, row, col, color, colspan=1):
        """Helper function to create and place buttons with consistent styling."""
        
        # 1. Determine Foreground (Text) Color based on button type
        # Numbers and decimal point get dark text on light background
        if text.isdigit() or text == '.':
            fg_color = self.text_color_dark 
        else:
            # Operators, 'C', '(', ')', and '=' get light text on dark background
            fg_color = self.text_color_light
            
        action = lambda t=text: self.button_click(t)

        # Special action mapping
        if text == 'C':
            action = self.clear_display
        elif text == '=':
            action = self.calculate

        button = tk.Button(
            self.master, 
            text=text, 
            padx=20, 
            pady=20, 
            font=('Inter', 18, 'bold'), 
            bg=color, 
            fg=fg_color, 
            activebackground=color,
            activeforeground=fg_color, 
            command=action, 
            relief='flat',
            bd=0,
            cursor="hand2" # Change cursor on hover
        )
        
        button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
        
        # Add a subtle hover effect (visual feedback is key for professional apps)
        button.bind("<Enter>", lambda e: e.widget.config(bg=self.shade_color(color, 0.9)))
        button.bind("<Leave>", lambda e: e.widget.config(bg=color))

    def shade_color(self, hex_color, factor):
        """Slightly lightens or darkens a hex color for hover effect."""
        try:
            # Convert hex to RGB
            rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
            # Apply shading factor
            shaded = [min(255, max(0, int(c * factor))) for c in rgb]
            # Convert RGB back to hex
            return f'#{shaded[0]:02x}{shaded[1]:02x}{shaded[2]:02x}'
        except:
            return hex_color # Return original if shading fails

    def button_click(self, item):
        """Appends the clicked button's value to the current expression."""
        if self.display_text.get() == "0" and item not in ('(', '.', '/', '*', '+', '-'):
            self.current_expression = str(item)
        else:
            self.current_expression += str(item)
        self.display_text.set(self.current_expression)

    def clear_display(self):
        """Clears the current expression and resets the display to '0'."""
        self.current_expression = ""
        self.display_text.set("0")

    def calculate(self):
        """Evaluates the current expression and updates the display."""
        try:
            # Use Python's built-in eval for expression evaluation
            safe_expression = self.current_expression.replace('x', '*').replace('÷', '/')
            
            result = str(eval(safe_expression))
            
            # Format large numbers to avoid scientific notation
            if '.' in result and len(result.split('.')[-1]) > 10:
                result = f"{float(result):.10f}"
                
            self.display_text.set(result)
            self.current_expression = result # Set result as start of next calculation
        
        except ZeroDivisionError:
            self.display_text.set("Error: Div by Zero")
            self.current_expression = ""
            
        except Exception:
            self.display_text.set("Error: Invalid Input")
            self.current_expression = ""

# Standard Python idiom to run the main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
