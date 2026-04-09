import tkinter as tk

# ---------------- COLORS ----------------
color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "#FFFFFF"

# ---------------- BUTTON LAYOUT ----------------
buttons = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%", "√"]

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Calculator")
window.configure(bg=color_black)
window.resizable(False, False)

# ---------------- DISPLAY ----------------
display = tk.Label(
    window,
    text="0",
    font=("Helvetica", 40),
    bg=color_black,
    fg=color_white,
    anchor="e",
    padx=10
)
display.grid(row=0, column=0, columnspan=4, sticky="we", pady=10)

# ---------------- LOGIC ----------------
A = "0"
operator = None

def clear_all():
    global A, operator
    A = "0"
    operator = None

def format_num(n):
    return str(int(n)) if n % 1 == 0 else str(n)

def click(value):
    global A, operator

    if value in right_symbols:
        if value == "=":
            try:
                B = float(display["text"])
                A_num = float(A)

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
            A = display["text"]
            operator = value
            display["text"] = "0"

    elif value in top_symbols:
        try:
            num = float(display["text"])

            if value == "AC":
                clear_all()
                display["text"] = "0"
            elif value == "+/-":
                display["text"] = format_num(-num)
            elif value == "%":
                display["text"] = format_num(num / 100)
            elif value == "√":
                display["text"] = format_num(num ** 0.5)
        except:
            display["text"] = "Error"

    else:
        if value == ".":
            if "." not in display["text"]:
                display["text"] += "."
        else:
            if display["text"] == "0":
                display["text"] = value
            else:
                display["text"] += value

# ---------------- CUSTOM BUTTON (CANVAS) ----------------
def create_button(row, col, text):

    if text in top_symbols:
        bg = color_light_gray
        fg = color_black
    elif text in right_symbols:
        bg = color_orange
        fg = color_white
    else:
        bg = color_dark_gray
        fg = color_white

    canvas = tk.Canvas(
        window,
        width=80,
        height=80,
        bg=color_black,
        highlightthickness=0
    )

    rect = canvas.create_rectangle(
        5, 5, 75, 75,
        fill=bg,
        outline=bg
    )

    canvas.create_text(
        40, 40,
        text=text,
        fill=fg,
        font=("Helvetica", 20)
    )

    def on_click(event):
        click(text)

    canvas.bind("<Button-1>", on_click)

    canvas.grid(row=row, column=col, padx=5, pady=5)

# ---------------- CREATE BUTTONS ----------------
for r in range(5):
    for c in range(4):
        create_button(r+1, c, buttons[r][c])

# ---------------- CENTER WINDOW ----------------
window.update()
w = window.winfo_width()
h = window.winfo_height()

x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)

window.geometry(f"{w}x{h}+{x}+{y}")

window.mainloop()