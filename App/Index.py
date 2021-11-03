from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./Images")

button_list=[]

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def user_login(title, subtitle, button__1, button_0):
    button__1.destroy()
    button_0.destroy()

    canvas.itemconfig(title, text="Please insert you personal ID")
    canvas.coords(title, 130, 320)
    canvas.itemconfig(subtitle, text="We remind you to keep it secret ")
    canvas.coords(subtitle, 230, 363)
    entry_1 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_1.place(
        x=219.0,
        y=402.0,
        width=262.0,
        height=28.0
    )

    login_image = PhotoImage(
        file=relative_to_assets("login.png"))
    login = Button(
        image=login_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_user(login, entry_1),
        relief="flat"
    )
    login.place(
        x=293.0,
        y=442.0,
        width=114.0,
        height=36.0
    )
    window.mainloop()


def create_user(login, entry_1):
    canvas.delete('all')
    login.destroy()
    entry_1.destroy()

    create_pi()


def app_manager_login(title, subtitle, button__1, button_0):
    button__1.destroy()
    button_0.destroy()

    canvas.itemconfig(title, text="Please insert you personal ID")
    canvas.coords(title, 130, 320)
    canvas.itemconfig(subtitle, text="We remind you to keep it secret ")
    canvas.coords(subtitle, 230, 363)
    entry_1 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_1.place(
        x=219.0,
        y=402.0,
        width=262.0,
        height=28.0
    )

    login_image = PhotoImage(
        file=relative_to_assets("login.png"))
    login = Button(
        image=login_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    login.place(
        x=293.0,
        y=442.0,
        width=114.0,
        height=36.0
    )
    window.mainloop()


def create_pi(button_6 = None, button_7= None, button_8= None, entry_1 = None, entry_2 = None, entry_3=None):

    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()
    if button_6 != None:
        button_6.destroy()
    if button_7 != None:
        button_7.destroy()
    if button_8 != None:
        button_8.destroy()


    canvas.create_text(
        31.0,
        144.0,
        anchor="nw",
        text="Personal Information",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        31.0,
        201.0,
        anchor="nw",
        text="Name: ",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        241.0,
        anchor="nw",
        text="Surname:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        281.0,
        anchor="nw",
        text="Fiscal Code:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        321.0,
        anchor="nw",
        text="Phone Number:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        361.0,
        anchor="nw",
        text="E-mail:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        401.0,
        anchor="nw",
        text="Address:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    # name
    canvas.create_text(
        190.0,
        201.0,
        anchor="nw",
        text="... ",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # surname
    canvas.create_text(
        190.0,
        241.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # fiscal code
    canvas.create_text(
        190.0,
        281.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # Phone Number
    phone = canvas.create_text(
        190.0,
        321.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # e-mail
    email = canvas.create_text(
        190.0,
        361.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # address
    address = canvas.create_text(
        190.0,
        401.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_change_pi(variable_fields, button_6),
        relief="flat"
    )
    button_6.place(
        x=224.0,
        y=440.0,
        width=114.0,
        height=36.0
    )
    variable_fields = [phone, email, address]

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ce(button_6),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_p( button_6),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_gp(button_6),
        relief="flat"
    )
    button_3.place(
        x=494.0,
        y=212.0,
        width=150.0,
        height=50.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4_dark.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=1000,
        highlightthickness=0,
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ct(button_6),
        relief="flat"
    )
    button_5.place(
        x=493.0,
        y=280.0,
        width=150.0,
        height=50.0
    )
    canvas.create_text(
        289.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",
        font=("Comfortaa Regular", 20 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        61.0,
        image=image_image_1
    )
    button_list = [button_1,button_2,button_3,button_4,button_5]

    if entry_1 != None:
        entry_1.destroy()
    if entry_2 != None:
        entry_2.destroy()
    if entry_3 != None:
        entry_3.destroy()
    window.mainloop()


def create_change_pi(list, button_6):

    for x in button_list:
        x.destroy()

    for x in list:
        canvas.delete(x)

    button_6.destroy()

    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_1.place(
        x=190.0,
        y=321.0,
        width=136.0,
        height=23.0
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_2.place(
        x=190.0,
        y=361.0,
        width=136.0,
        height=23.0
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_3.place(
        x=190.0,
        y=401.0,
        width=136.0,
        height=23.0
    )

    # save
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi( None, button_8, button_7, entry_1, entry_2, entry_3),
        relief="flat"
    )
    button_8.place(
        x=117.0,
        y=438.0,
        width=114.0,
        height=36.0
    )

    # delete
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi( None, button_8, button_7, entry_1, entry_2, entry_3),
        relief="flat"
    )
    button_7.place(
        x=269.0,
        y=438.0,
        width=114.0,
        height=36.0
    )
    window.mainloop()


def cancel_pi(button_8, button_7, entry_1, entry_2, entry_3):
    # Phone Number
    phone = canvas.create_text(
        190.0,
        321.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # e-mail
    email = canvas.create_text(
        190.0,
        361.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # address
    address = canvas.create_text(
        190.0,
        401.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    list = [phone, email, address]

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_change_pi(list, button_6),
        relief="flat"
    )
    button_6.place(
        x=224.0,
        y=440.0,
        width=114.0,
        height=36.0
    )

    button_7.destroy()
    button_8.destroy()
    entry_1.destroy()
    entry_2.destroy()
    entry_3.destroy()

    create_pi()


def save_pi(button_8, button_7, entry_1, entry_2, entry_3):
    # Phone Number
    phone = canvas.create_text(
        190.0,
        321.0,
        anchor="nw",
        text=entry_1.get(),
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # e-mail
    email = canvas.create_text(
        190.0,
        361.0,
        anchor="nw",
        text=entry_2.get(),
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # address
    address = canvas.create_text(
        190.0,
        401.0,
        anchor="nw",
        text=entry_3.get(),
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    list = [phone, email, address]

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_change_pi(list, button_6),
        relief="flat"
    )
    button_6.place(
        x=224.0,
        y=440.0,
        width=114.0,
        height=36.0
    )

    button_7.destroy()
    button_8.destroy()
    entry_1.destroy()
    entry_2.destroy()
    entry_3.destroy()
    create_pi()


def create_gp(button_6 = None):
    canvas.delete("all")

    global button_list
    for x in button_list:
        x.destroy()
    if button_6 != None:
        button_6.destroy()

    canvas.create_text(
        289.0,
        113.0,
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

    # place
    canvas.create_text(
        181.0,
        312.0,
        anchor="nw",
        text="...",
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

    # date
    canvas.create_text(
        181.0,
        425.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # Expiration
    canvas.create_text(
        181.0,
        201.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ce(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_p(),
        relief="flat"
    )
    button_2.place(
        x=494.0,
        y=416.0,
        width=150.0,
        height=50.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3_dark.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=1000,
        highlightthickness=0,
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ct(),
        relief="flat"
    )
    button_5.place(
        x=494.0,
        y=280.0,
        width=150.0,
        height=50.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        61.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        359.0,
        315.0,
        image=image_image_2
    )
    button_list = [button_1, button_2, button_3, button_4, button_5]
    window.mainloop()


def create_ct(button_6 = None, button_7= None, button_8= None):
    canvas.delete("all")
    global button_list
    for x in button_list:
        x.destroy()
    if button_6 != None:
        button_6.destroy()
    if button_7 != None:
        button_7.destroy()
    if button_8 != None:
        button_8.destroy()

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        61.0,
        image=image_image_1
    )

    canvas.create_text(
        289.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",

        font=("Comfortaa Regular", 20 * -1)
    )


    canvas.create_text(
        31.0,
        144.0,
        anchor="nw",
        text="Covid Tests",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        31.0,
        186.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        143.0,
        187.0,
        anchor="nw",
        text="Hour",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        256.0,
        187.0,
        anchor="nw",
        text="Type",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        372.0,
        187.0,
        anchor="nw",
        text="Result",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    # date
    canvas.create_text(
        31.0,
        216.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # time
    canvas.create_text(
        143.0,
        217.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # type
    canvas.create_text(
        256.0,
        217.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # result
    canvas.create_text(
        372.0,
        217.0,
        anchor="nw",
        text="...",
        fill="#FF0000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # date example distance
    canvas.create_text(
        31.0,
        248.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ce(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_p(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_gp(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi(),
        relief="flat"
    )
    button_4.place(
        x=494.0,
        y=144.0,
        width=150.0,
        height=50.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5_dark.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=1000,
        highlightthickness=0,
        relief="flat"
    )
    button_5.place(
        x=493.0,
        y=280.0,
        width=150.0,
        height=50.0
    )
    button_list = [button_1, button_2, button_3, button_4, button_5]
    window.mainloop()


def create_ce(button_6 = None):

    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()

    if button_6 != None:
        button_6.destroy()

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        61.0,
        image=image_image_1
    )

    canvas.create_text(
        289.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",

        font=("Comfortaa Regular", 20 * -1)
    )

    canvas.create_text(
        31.0,
        144.0,
        anchor="nw",
        text="Covid Exposure",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        31.0,
        186.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        143.0,
        187.0,
        anchor="nw",
        text="Place",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        317.0,
        188.0,
        anchor="nw",
        text="Risk Level",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    # date
    canvas.create_text(
        31.0,
        216.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # place
    canvas.create_text(
        143.0,
        217.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # risk
    canvas.create_text(
        317.0,
        218.0,
        anchor="nw",
        text="...",
        fill="#2CAB00",
        font=("Comfortaa Regular", 16 * -1)
    )

    # date_2
    canvas.create_text(
        31.0,
        248.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1_dark.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_p(),
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
        borderwidth=1000,
        highlightthickness=0,

        command=lambda: create_gp(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ct(),
        relief="flat"
    )
    button_5.place(
        x=493.0,
        y=280.0,
        width=150.0,
        height=50.0
    )


    button_list = [button_1, button_2, button_3, button_4, button_5]
    window.mainloop()


def create_p(button_6 = None):
    canvas.delete("all")

    global button_list
    for x in button_list:
        x.destroy()

    if button_6 != None:
        button_6.destroy()

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        349.0,
        61.0,
        image=image_image_1
    )

    canvas.create_text(
        289.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",

        font=("Comfortaa Regular", 20 * -1)
    )

    canvas.create_text(
        31.0,
        144.0,
        anchor="nw",
        text="Place Visited",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        31.0,
        186.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        110.0,
        187.0,
        anchor="nw",
        text="Place",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        420.0,
        186.0,
        anchor="nw",
        text="Risk",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        214.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    canvas.create_text(
        110.0,
        215.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    canvas.create_text(
        420.0,
        214.0,
        anchor="nw",
        text="...",
        fill="#2CAB00",
        font=("Comfortaa Regular", 16 * -1)
    )

    canvas.create_text(
        31.0,
        246.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    canvas.create_text(
        259.0,
        185.0,
        anchor="nw",
        text="Start H.",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        264.0,
        217.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    canvas.create_text(
        341.0,
        185.0,
        anchor="nw",
        text="End H.",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        341.0,
        213.0,
        anchor="nw",
        text="...",
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ce(),
        relief="flat"
    )
    button_1.place(
        x=493.0,
        y=348.0,
        width=150.0,
        height=50.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2_dark.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=1000,
        highlightthickness=0,
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_gp(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_pi(),
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
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_ct(),
        relief="flat"
    )
    button_5.place(
        x=493.0,
        y=280.0,
        width=150.0,
        height=50.0
    )


    button_list = [button_1, button_2, button_3, button_4, button_5]
    window.mainloop()

window = Tk()
window.title('SMBUD Group 20')
screenPositionRight = int(window.winfo_screenwidth() / 2 - 700 / 2)
screenPositionDown = int(window.winfo_screenheight() / 2 - 500 / 2)
window.geometry("700x500" + "+{}+{}".format(screenPositionRight, screenPositionDown))
window.configure(bg="#FAF8F5")

canvas = Canvas(
    window,
    bg="#FAF8F5",
    height=500,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

title = canvas.create_text(
    240.0,
    317.0,
    anchor="nw",
    text="ImmunoPoli",
    fill="#000000",
    font=("Comfortaa Regular", 34 * -1)
)

subtitle = canvas.create_text(
    195.0,
    363.0,
    anchor="nw",
    text="Welcome to COVID-19 information portal",
    fill="#000000",
    font=("Poppins Regular", 16 * -1)
)

# user login
button_image_0 = PhotoImage(
    file=relative_to_assets("button_0.png"))
button_0 = Button(
    image=button_image_0,
    borderwidth=1000,
    highlightthickness=0,
    command=lambda: user_login(title, subtitle, button__1, button_0),
    relief="flat"
)
button_0.place(
    x=414.0,
    y=405.0,
    width=200.0,
    height=60.0
)

# app manager login
button_image__1 = PhotoImage(
    file=relative_to_assets("button_-1.png"))
button__1 = Button(
    image=button_image__1,
    borderwidth=1000,
    highlightthickness=0,
    command=lambda: app_manager_login(title, subtitle, button__1, button_0),
    relief="flat"
)

button__1.place(
    x=85.0,
    y=405.0,
    width=200.0,
    height=60.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("logo.png"))
image_1 = canvas.create_image(
    350.0,
    164.0,
    image=image_image_1
)

window.resizable(False, False)
window.mainloop()
