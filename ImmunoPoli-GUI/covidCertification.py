
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x500")
window.configure(bg = "#FAF8F5")


canvas = Canvas(
    window,
    bg = "#FAF8F5",
    height = 500,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    289.0,
    104.0,
    anchor="nw",
    text="ImmunoPoli",
    fill="#000000",
    font=("Comfortaa Regular", 20 * -1)
)

canvas.create_text(
    31.0,
    144.0,
    anchor="nw",
    text="Covid Certification",
    fill="#6370FF",
    font=("Comfortaa Bold", 20 * -1)
)

canvas.create_text(
    31.0,
    201.0,
    anchor="nw",
    text="Date:",
    fill="#000000",
    font=("Comfortaa Bold", 16 * -1)
)

canvas.create_text(
    31.0,
    312.0,
    anchor="nw",
    text="Country:",
    fill="#000000",
    font=("Comfortaa Bold", 16 * -1)
)

canvas.create_text(
    181.0,
    312.0,
    anchor="nw",
    text="Italy",
    fill="#000000",
    font=("Comfortaa Regular", 16 * -1)
)

canvas.create_text(
    31.0,
    425.0,
    anchor="nw",
    text="Expiration Date:",
    fill="#000000",
    font=("Comfortaa Bold", 16 * -1)
)

canvas.create_text(
    181.0,
    425.0,
    anchor="nw",
    text="17/12/2021",
    fill="#000000",
    font=("Comfortaa Regular", 16 * -1)
)

canvas.create_text(
    181.0,
    201.0,
    anchor="nw",
    text="17/06/2021",
    fill="#000000",
    font=("Comfortaa Regular", 16 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=493.0,
    y=348.0,
    width=150.0,
    height=50.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=493.0,
    y=416.0,
    width=150.0,
    height=50.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=494.0,
    y=212.0,
    width=150.0,
    height=50.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=494.0,
    y=144.0,
    width=150.0,
    height=50.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=493.0,
    y=280.0,
    width=150.0,
    height=50.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    52.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    359.0,
    315.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()