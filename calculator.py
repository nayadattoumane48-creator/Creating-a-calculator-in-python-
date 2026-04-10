import tkinter as tk

# ================== COLORS ==================
# These define the colors used in the calculator
color_light_gray = "#D4D4D2"   # top buttons (AC, %, etc.)
color_black = "#1C1C1C"        # background + display
color_dark_gray = "#505050"    # number buttons
color_orange = "#FF9500"       # operators (+, -, ×, ÷, =)
color_white = "#FFFFFF"        # text color

# ================== BUTTON LAYOUT ==================
# This is the visual layout of the calculator buttons
buttons = [
    ["AC","DEL", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

# Buttons grouped by function
right_symbols = ["÷", "×", "-", "+", "="]   # operators
top_symbols = ["AC","DEL", "+/-", "%", "√"]       # special functions

# ================== WINDOW SETUP ==================
window = tk.Tk()                      # create main window
window.title("Calculator")           # window title
window.configure(bg=color_black)     # background color
window.resizable(False, False)       # prevent resizing

# Prevent grid cells from expanding (fixes button stretching)
for i in range(6):                   # 1 display row + 5 button rows
    window.grid_rowconfigure(i, weight=0)

for j in range(4):                   # 4 columns
    window.grid_columnconfigure(j, weight=0)

# ================== DISPLAY SCREEN ==================
# This is the screen where numbers/results appear
display = tk.Label(
    window,
    text="0",                        # starting value
    font=("Helvetica", 40),
    bg=color_black,
    fg=color_white,
    anchor="e",                      # align text to the right
    padx=10,
    width=10
)

# Place display at the top spanning all columns
display.grid(row=0, column=0, columnspan=4, pady=10)

# ================== CALCULATOR LOGIC ==================
A = "0"          # first number
operator = None  # selected operation (+, -, etc.)

# Reset everything
def clear_all():
    global A, operator
    A = "0"
    operator = None

# Remove unnecessary ".0" from numbers (e.g., 5.0 → 5)
def format_num(n):
    return str(int(n)) if n % 1 == 0 else str(n)

# This function runs when any button is clicked
def click(value):
    global A, operator

    # ---------- OPERATOR BUTTONS ----------
    if value in right_symbols:
        if value == "=":
            try:
                B = float(display["text"])   # second number
                A_num = float(A)

                # Perform calculation
                if operator == "+":
                    result = A_num + B
                elif operator == "-":
                    result = A_num - B
                elif operator == "×":
                    result = A_num * B
                elif operator == "÷":
                    result = A_num / B

                display["text"] = format_num(result)

            except:
                display["text"] = "Error"

            clear_all()

        else:
            # Store first number and operator
            A = display["text"]
            operator = value
            display["text"] = "0"

    # ---------- TOP FUNCTION BUTTONS ----------
    elif value in top_symbols:
        try:
            num = float(display["text"])

            if value == "AC":
                clear_all()
                display["text"] = "0"
            
            elif value == "DEL":
                current = display["text"]

                # Remove last character
                if len(current) > 1:
                    display["text"] = current[:-1]
                else:
                    display["text"] = "0"

            elif value == "+/-":
                display["text"] = format_num(-num)

            elif value == "%":
                display["text"] = format_num(num / 100)

            elif value == "√":
                display["text"] = format_num(num ** 0.5)

        except:
            display["text"] = "Error"

    # ---------- NUMBER & DECIMAL BUTTONS ----------
    else:
        if value == ".":
            # Prevent multiple decimals
            if "." not in display["text"]:
                display["text"] += "."
        else:
            # Replace 0 or append number
            if display["text"] == "0":
                display["text"] = value
            else:
                display["text"] += value

# ================== CUSTOM BUTTON (CANVAS) ==================
# We use Canvas instead of Button to fix macOS color issues
def create_button(row, col, text):

    # Decide button color based on type
    if text in top_symbols:
        bg = color_light_gray
        fg = color_black
    elif text in right_symbols:
        bg = color_orange
        fg = color_white
    else:
        bg = color_dark_gray
        fg = color_white

    # Create a square canvas (acts like a button)
    canvas = tk.Canvas(
        window,
        width=80,
        height=80,
        bg=color_black,
        highlightthickness=0
    )

    # Draw the button background
    canvas.create_rectangle(5, 5, 75, 75, fill=bg, outline=bg)

    # Draw the button text
    canvas.create_text(
        40, 40,
        text=text,
        fill=fg,
        font=("Helvetica", 20)
    )

    # Detect click
    canvas.bind("<Button-1>", lambda e: click(text))

    # Place button in grid
    canvas.grid(row=row, column=col, padx=5, pady=5)

# ================== CREATE ALL BUTTONS ==================
for r in range(5):           # rows
    for c in range(4):       # columns
        create_button(r+1, c, buttons[r][c])

# ================== CENTER WINDOW ==================
window.update()

w = window.winfo_width()
h = window.winfo_height()

x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)

window.geometry(f"{w}x{h}+{x}+{y}")

# ================== RUN APP ==================
window.mainloop()