"""
Comments:

- Each button is designed with specific images;
- All the elements built inside a canvas can be destroy with " canvas.delete('all') " command
    while entries and buttons must be delete separately

Useful commands:

canvas.create_text : creates a text field
- Entry : creates a text box (expected an input from the customer)
- PhotoImage : loads an image
- Button : creates a button

Abbreviations:

- pi = personal information
- gp = green pass
- ct = covid test
- ce = covid exposure
- p = place
- db = database



Buttons:

- button__1 : user front page
- button_0 : app manager front page

- button_1 : covid exposure
- button_2 : places visited
- button_3 : green pass
- button_4 : pesonal information
- button_5 : covid tests

- button_6 : change personal information
- button_7 : save changes in personal information
- button_8 : cancel changes in personal information

- button_11 : covid trends
- button_22 : database query
- button_33 : add covid results

Person :

personal_information = [ id , name , surname , age , phone , email , address , civic number , city ]
new_field_pi = [ new phone , new email ]
green_pass = [ type, date , country  , expiration day ]
tests = [ [test], [test], ... ]
places = [ [place, date, start h, end h , risk], [place, date, start h, end h , risk], ...  ]

checked id login :
- empty id field
- negative id
- out of range id
- not a number

cheked mail:
- contains @
- contains .

checked phone number:
- it's an integer

checked new ct:
- person exist
- test exist
- format of date
- format of hour

"""

from pathlib import Path
import neo4j as nj
import numpy

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./Images")

BOLT = "bolt://52.87.206.215:7687"
USER = "neo4j"
PASSWORD = "controls-inches-halyard"

"""
list of buttons that don't belong to canvas that have to be delete before building a page 
"""
button_list = []
"""
list of entry that don't belong to canvas that have to be delete before building a page 
"""
entry_list = []

"""
for the following list the format was specified in the comments above 
"""
personal_information = []
new_fields_pi = []
green_pass = []
tests = []
places = []

"""error message"""
error = None


def relative_to_assets(path: str) -> Path:
    """
    Method that rebuilds the path of all the pictures
    :param path: picture name
    :return: complete path
    """
    return ASSETS_PATH / Path(path)


"""CONNECTION MANAGING"""


def open_connection():
    """
    Method that starts a connection with the database
    :return: the driver for the connection
    """
    connection = nj.GraphDatabase.driver(
        BOLT, auth=nj.basic_auth(USER, PASSWORD))
    return connection


def close_connection(connection):
    """
    Method that close a connection
    :param connection: is the connection to terminate
    """
    connection.close()


"""DATABASE QUERIES"""


def find_person_by_ID(tx, ID):
    """
    Method that finds a Person given it's ID
    :param tx: is the transaction
    :param ID: is the ID to find
    :return: all the nodes that have attribute equal to ID
    """
    global personal_information
    personal_information = []

    query = (
        "MATCH (p:Person)-[r:LIVE]->(a:House) "
        "WHERE id(p) = $ID "
        "RETURN p,a"
    )
    result = tx.run(query, ID=ID)

    personal_information.append(ID)

    for node in result:
        personal_information.append(node.data()['p'].get('name'))
        personal_information.append(node.data()['p'].get('surname'))
        personal_information.append(node.data()['p'].get('age'))
        personal_information.append(node.data()['p'].get('number'))
        personal_information.append(node.data()['p'].get('mail'))
        personal_information.append(node.data()['a'].get('address'))
        personal_information.append(node.data()['a'].get('civic_number'))
        personal_information.append(node.data()['a'].get('city'))


def update_information_by_ID(tx, ID):
    """
    Method that queries the database for update some user information
    :param tx: is the transaction
    :param ID: is the ID of the person that decides to update his information
    """
    query = (
        "MATCH (p: Person) "
        "WHERE id(p) = $ID "
        "SET p.mail = $MAIL, p.number = $NUMBER "
        "RETURN p"
    )
    tx.run(query, ID=ID, NUMBER=new_fields_pi[0], MAIL=new_fields_pi[1])


def find_gp_by_ID(tx, ID):
    """
        Method that finds a green pass given the ID of the person
        :param tx: is the transaction
        :param ID: is the ID to find
        :return: all the nodes that have attribute equal to ID
        """
    global green_pass
    green_pass = []

    query = (
        "MATCH(p: Person)-[r: GET]->(v: Vaccine) "
        "WHERE id(p) = $ID "
        "RETURN v.name, r.date, r.country, r.expirationDate "
        "ORDER BY r.date "
        "desc LIMIT 1 "
    )

    result = tx.run(query, ID=ID)
    for relation in result:
        green_pass.append(relation.data()['v.name'])
        green_pass.append(relation.data()['r.date'])
        green_pass.append(relation.data()['r.country'])
        green_pass.append(relation.data()['r.expirationDate'])


def find_covid_tests_by_ID(tx, ID):
    """
    Method that queries the database for collecting tests information
    :param tx: is the transaction
    :param ID: is the ID of the person
    """

    global tests
    tests = []

    query = (
        "MATCH(p: Person)-[r: MAKE]->(n:Test) "
        "WHERE id(p) = $ID "
        "RETURN n.name, r.date, r.hour, r.result"
    )

    result = tx.run(query, ID=ID)

    for relation in result:
        test = [relation.data()['n.name'], relation.data()['r.date']]
        x = relation.data()['r.hour']
        x = str(x)
        x = x[0:8]
        test.append(x)
        test.append(relation.data()['r.result'])
        tests.append(test)


def find_covid_exposures_by_ID(tx, ID):
    """
    Method that queries the database for collecting covid exposures
    :param tx: is the transaction
    :param ID: is the ID of the person
    """
    print("to be make")


def find_place_visited(tx, ID):
    """
    Method that queries the database for collecting covid exposures
    :param tx: is the transaction
    :param ID: is the ID of the person
    """
    global places
    places = []

    query = (
        "MATCH (p:Person)-[r:VISIT]->(l:Location) "
        "WHERE id(p) = $ID  "
        "RETURN r.date, l.name, r.start_hour, r.end_hour"
    )

    result = tx.run(query, ID=ID)

    for relation in result:
        place = []
        z = relation.data()['l.name']
        z = str(z)
        if len(z) > 13:
            z = z[0:13]
            z = z + '-'
        place.append(z)
        place.append(relation.data()['r.date'])
        x = relation.data()['r.start_hour']
        x = str(x)
        x = x[0:8]
        place.append(x)
        y = relation.data()['r.end_hour']
        y = str(y)
        y = y[0:8]
        place.append(y)
        places.append(place)


def add_new_test(tx, ID, testId, date, hour, result):
    """
    Method that adds a new covid test
    :param tx: is the transaction
    :param ID: person id
    :param tesId: test id
    :param date: date of the test
    :param hour: hour of the test
    param result: result of the test -> positive or negative
    """

    query = (
        "MATCH (p:Person) , (t:Test) "
        "WHERE ID(p) = $ID AND ID(t) = $testId "
        "MERGE (p)-[:MAKE{date:date($date) , hour: time($hour) ,result:$result}]->(t); "
    )
    tx.run(query, ID=ID, testId=testId, date=date, hour=hour, result=result)


"""PAGE BUILDER"""


def ct_value_check(date_initial, ID_personal, hour_initial, testId_initial, result):
    """
    Method that checks valitidy of values inserted
    :param ID_personal: person id
    :param testId_initial: test id
    :param date_initial: date of the test
    :param hour_initial: hour of the test
    param result: result of the test -> positive or negative
    """

    global error

    if error is not None:
        canvas.delete(error)

    try:
        ID = int(ID_personal)
    except ValueError:

        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid ID, provide a number ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    try:
        testId = int(testId_initial)
    except ValueError:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid test ID, provide a number ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    """ check if a person or a test exist 
    PERCHè NON FUNZIONA
    query = (
            "MATCH (p: Person), (t:Test) "
            "WHERE id(p) = $ID AND testId=$testId"
            "RETURN count(*) "
    )
    print(query)
    result = session.run(query, ID=ID_personal,testId=testId_initial)
    print(ID_personal, testId_initial)
    for x in result:
        count = x.data()["count(*)"]
        print(x)
        print(count)

    if count == 0:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: person or test doesn't exist ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return
    """

    date_split = date_initial.split("-")
    if len(date_split) != 3 :
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid data range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    try:
        date_split[0] = int(date_split[0])
        date_split[1] = int(date_split[1])
        date_split[2] = int(date_split[2])
    except ValueError:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid data fromat, try with AAA-MM-DD ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    if (1950 > date_split[0] or date_split[0] > 2021) or (
            1 > date_split[1] or date_split[1] > 12) or (
            1 > date_split[2] or date_split[2] > 31):
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid data range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    hour_split = hour_initial.split(":")
    if len(hour_split) != 2 :
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid hour range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    try:
        hour_split[0] = int(hour_split[0])
        hour_split[1] = int(hour_split[1])
    except ValueError:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid hour fromat, try with HH:MM ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    if (0 > hour_split[0] or hour_split[0] > 23) or (0 > hour_split[1] or hour_split[1]> 59):
        print(len(hour_split), hour_split[0], hour_split[1])
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: invalid hour range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    add_new_test(session, ID, testId, date_initial, hour_initial, result)
    create_add_ct()


def save_pi_changes(phone, email):
    """
    Method that catches and checks new entries inserted by user.
    If a field is empty its information will be replaced by older one
    :param phone: new phone
    :param email: new email
    :param address: new address
    """
    global error
    if error is not None:
        canvas.delete(error)

    if (phone == '') and (email == ''):
        create_pi()

    if phone == '':
        int_phone = personal_information[4]
    else:
        try:
            int_phone = int(phone)
        except ValueError:
            error = canvas.create_text(
                338,
                322,
                anchor="nw",
                text="ERROR: \nwrong phone format \nplease insert a number ",
                fill="#CA0000",
                font=("Comfortaa Regular", 10 * -1)
            )
            return

    if email == '':
        email = personal_information[5]
    else:
        if len(email.split("@")) != 2:
            error = canvas.create_text(
                338,
                322,
                anchor="nw",
                text="ERROR: \nwrong email format \n'@' is missing ",
                fill="#CA0000",
                font=("Comfortaa Regular", 10 * -1)
            )
            return
        elif len(email.split(".")) < 2:
            error = canvas.create_text(
                338,
                322,
                anchor="nw",
                text="ERROR: \nwrong email format \n'.' is missing ",
                fill="#CA0000",
                font=("Comfortaa Regular", 10 * -1)
            )
            return

    global new_fields_pi
    new_fields_pi.append(phone)
    new_fields_pi.append(email)
    global session
    update_information_by_ID(session, personal_information[0])
    create_pi()


def collect_app_manager_information(ID_person, subtitle):
    """
    Method that is able to collect data and call personal information page constructor
    :param ID_person: id inserted by the app manager
    """

    # no integer or empty
    try:
        ID = int(ID_person)
    except ValueError:
        canvas.itemconfig(subtitle, text="The following field must be fulfilled with a number", fill="red")
        canvas.coords(subtitle, 160, 363)
        return

    global session

    global personal_information
    find_person_by_ID(session, ID)

    # id is not link to any person (also negative )
    if len(personal_information) < 3:
        canvas.itemconfig(subtitle, text="The following field must be fulfilled with an existing ID", fill="red")
        canvas.coords(subtitle, 140, 363)
        return

    canvas.delete("all")
    global button_list
    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []
    button_list = []

    create_add_ct()


def collect_user_information(ID_person, subtitle):
    """
    Method that is able to collect data and call personal information page constructor
    :param ID_person: id inserted by the user
    """

    # no integer or empty
    try:
        ID = int(ID_person)
    except ValueError:
        canvas.itemconfig(subtitle, text="The following field must be fulfilled with a number", fill="red")
        canvas.coords(subtitle, 160, 363)
        return

    global session

    global personal_information
    find_person_by_ID(session, ID)

    # id is not link to any person (also negative )
    if len(personal_information) < 3:
        canvas.itemconfig(subtitle, text="The following field must be fulfilled with an existing ID", fill="red")
        canvas.coords(subtitle, 140, 363)
        return

    canvas.delete("all")
    global button_list
    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []
    button_list = []

    create_pi()


def user_login(title, subtitle, button__1, button_0):
    """
    Method that builds user login page
    :param title: text field from front page that has to modify
    :param subtitle: text field from front page that has to modify
    :param button__1: button to delete
    :param button_0: button to delete
    :return:
    """

    button__1.destroy()
    button_0.destroy()

    # modify the innter text
    canvas.itemconfig(title, text="Please insert you personal ID")
    # modify the position
    canvas.coords(title, 130, 320)
    canvas.itemconfig(subtitle, text="We remind you to keep it secret ")
    canvas.coords(subtitle, 230, 363)

    # create entries
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
        command=lambda: collect_user_information(entry_1.get(), subtitle),
        relief="flat"
    )
    login.place(
        x=293.0,
        y=442.0,
        width=114.0,
        height=36.0
    )

    global button_list
    button_list = [login]

    global entry_list
    entry_list = [entry_1]

    # update window
    window.mainloop()


def app_manager_login(title, subtitle, button__1, button_0):
    """
       Method that builds app manager login page
       :param title: text field from front page that has to modify
       :param subtitle: text field from front page that has to modify
       :param button__1: button to delete
       :param button_0: button to delete
       :return:
    """

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
        command=lambda: collect_app_manager_information(entry_1.get(), subtitle),
        relief="flat"
    )
    login.place(
        x=293.0,
        y=442.0,
        width=114.0,
        height=36.0
    )

    global button_list
    button_list = [login]

    global entry_list
    entry_list = [entry_1]

    window.mainloop()


def create_add_ct():
    """
    Method that creates the app manager interface for inserting new covid test results
    :return:
    """
    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []

    canvas.create_text(
        22.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",
        font=("Comfortaa Regular", 20 * -1)
    )

    canvas.create_text(
        232.0,
        166.0,
        anchor="nw",
        text="Add Covid Test Results",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        255.0,
        250.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        253.0,
        215.0,
        anchor="nw",
        text="Person ID",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        255.0,
        286.0,
        anchor="nw",
        text="Hour",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        253.0,
        321.0,
        anchor="nw",
        text="Test ID",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        223.0,
        404.0,
        anchor="nw",
        text="Result",
        fill="#000000",
        font=("Comfortaa Bold", 20 * -1)
    )

    entry_1 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_1.place(
        x=355.0,
        y=250.0,
        width=91.0,
        height=17.0
    )

    entry_2 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_2.place(
        x=355.0,
        y=217.0,
        width=91.0,
        height=17.0
    )

    entry_3 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_3.place(
        x=355.0,
        y=286.0,
        width=91.0,
        height=17.0
    )

    entry_4 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_4.place(
        x=355.0,
        y=322.0,
        width=91.0,
        height=17.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_covid_trends(),
        relief="flat"
    )
    button_1.place(
        x=342.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_22.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_db(),
        relief="flat"
    )
    button_2.place(
        x=509.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_33_dark.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=1000,
        highlightthickness=0,
        relief="flat"
    )
    button_3.place(
        x=175.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        83.0,
        61.0,
        image=image_image_1
    )

    negative_image = PhotoImage(
        file=relative_to_assets("negative.png"))
    negative = Button(
        image=negative_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: ct_value_check(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), 'Negative'),
        relief="flat"
    )
    negative.place(
        x=400.0,
        y=382.0,
        width=60.0,
        height=59.090911865234375
    )

    positive_image = PhotoImage(
        file=relative_to_assets("positive.png"))
    positive = Button(
        image=positive_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: ct_value_check(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), 'Positive'),
        relief="flat"
    )
    positive.place(
        x=322.0,
        y=382.0,
        width=60.0,
        height=60.0
    )

    button_list = [positive, negative, button_1, button_2, button_3]


    entry_list = [entry_1, entry_2, entry_3, entry_4]
    window.mainloop()


def create_covid_trends():
    """
    Method that creates app manager page for visualizing covid-19 common trends
    :return:
    """

    canvas.delete("all")
    global button_list
    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []
    button_list = []

    canvas.create_text(
        22.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",
        font=("Comfortaa Regular", 20 * -1)
    )

    canvas.create_text(
        273.0,
        166.0,
        anchor="nw",
        text="Covid Trends",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_11_dark.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        relief="flat"
    )
    button_1.place(
        x=342.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    canvas.create_text(
        25.0,
        14.0,
        anchor="nw",
        text="Trends",
        fill="#FFFFFF",
        font=("Roboto", 18 * -1)
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_22.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_db(),
        relief="flat"
    )
    button_2.place(
        x=509.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_33.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_add_ct(),
        relief="flat"
    )
    button_3.place(
        x=175.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        83.0,
        61.0,
        image=image_image_1
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        438.0,
        176.0,
        image=image_image_3
    )
    button_list = [button_1, button_2, button_3]
    window.mainloop()


def create_db():
    """
    Method that creates app manager page for query the database
    :return:
    """
    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []

    canvas.create_text(
        22.0,
        113.0,
        anchor="nw",
        text="ImmunoPoli",
        fill="#000000",
        font=("Comfortaa Regular", 20 * -1)
    )

    canvas.create_text(
        229.0,
        166.0,
        anchor="nw",
        text="Database Query",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_covid_trends(),
        relief="flat"
    )
    button_1.place(
        x=342.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_22_dark.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=1000,
        highlightthickness=0,
        relief="flat"
    )
    button_2.place(
        x=509.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_33.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_add_ct(),
        relief="flat"
    )
    button_3.place(
        x=175.0,
        y=46.0,
        width=150.0,
        height=50.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        83.0,
        61.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_2 = canvas.create_image(
        437.0,
        172.0,
        image=image_image_2
    )

    button_list = [button_1, button_2, button_3]
    window.mainloop()


def create_pi():
    """
    Method that creates user page for seeing personal information
    """
    find_person_by_ID(session, personal_information[0])

    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []
    button_list = []

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
        text="Age:",
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
        text=personal_information[1],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # surname
    canvas.create_text(
        190.0,
        241.0,
        anchor="nw",
        text=personal_information[2],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # age
    canvas.create_text(
        190.0,
        281.0,
        anchor="nw",
        text=personal_information[3],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # Phone Number
    phone = canvas.create_text(
        190.0,
        321.0,
        anchor="nw",
        text="+39 " + personal_information[4],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # e-mail
    email = canvas.create_text(
        190.0,
        361.0,
        anchor="nw",
        text=personal_information[5],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )

    # address
    address = canvas.create_text(
        190.0,
        401.0,
        anchor="nw",
        text=personal_information[6] + " " + personal_information[7] + ", " + personal_information[8],
        fill="#000000",
        font=("Comfortaa Regular", 16 * -1)
    )
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: create_change_pi(variable_fields),
        relief="flat"
    )
    button_6.place(
        x=224.0,
        y=440.0,
        width=114.0,
        height=36.0
    )
    variable_fields = [phone, email]

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
        command=lambda: create_ct(),
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
    button_list = [button_1, button_2, button_3, button_4, button_5, button_6]
    window.mainloop()


def create_change_pi(list):
    """
    Method that allows user to modify some of his personal infmation
    :param list: list of fields to destroy
    :return:
    """
    global button_list
    for x in button_list:
        x.destroy()

    for x in list:
        canvas.delete(x)

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

    # save
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: save_pi_changes(entry_1.get(), entry_2.get()),
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
        command=lambda: create_pi(),
        relief="flat"
    )
    button_7.place(
        x=269.0,
        y=438.0,
        width=114.0,
        height=36.0
    )

    button_list = [button_7, button_8]

    global entry_list
    entry_list = [entry_1, entry_2]

    window.mainloop()


def create_gp():
    """
    Method that creates user page for seeing his green pass if exist
    :param button_6: button change to destroy
    :return:
    """

    canvas.delete("all")

    global button_list
    for x in button_list:
        x.destroy()

    find_gp_by_ID(session, personal_information[0]);

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

    if len(green_pass) != 4:
        canvas.create_text(
            31.0,
            201.0,
            anchor="nw",
            text="Zero doses of covid vaccine was found",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        button_list = [button_1, button_2, button_3, button_4, button_5]
        window.mainloop()
        return

    canvas.create_text(
        31.0,
        201.0,
        anchor="nw",
        text="Type:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        272.0,
        anchor="nw",
        text="Date:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        31.0,
        342.0,
        anchor="nw",
        text="Country:",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
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
        201.0,
        anchor="nw",
        text=green_pass[0],
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        181.0,
        272.0,
        anchor="nw",
        text=green_pass[1],
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        181.0,
        342.0,
        anchor="nw",
        text=green_pass[2],
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        181.0,
        425.0,
        anchor="nw",
        text=green_pass[3],
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        375.0,
        315.0,
        image=image_image_2
    )
    button_list = [button_1, button_2, button_3, button_4, button_5]
    window.mainloop()


def create_ct():
    """
        Method that creates user page for seeing covid test done
        :param button_6: button change to destroy
        :return
    """
    find_covid_tests_by_ID(session, personal_information[0])

    canvas.delete("all")
    global button_list
    for x in button_list:
        x.destroy()

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
        text="Type",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        143.0,
        187.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        256.0,
        187.0,
        anchor="nw",
        text="Hour",
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

    for i in range(len(tests)):

        delta = 32 * i

        canvas.create_text(
            31.0,
            216.0 + delta,
            anchor="nw",
            text=tests[i][0],
            fill="#000000",
            font=("Comfortaa Regular", 16 * -1)
        )

        canvas.create_text(
            143.0,
            217.0 + delta,
            anchor="nw",
            text=tests[i][1],
            fill="#000000",
            font=("Comfortaa Regular", 16 * -1)
        )

        canvas.create_text(
            256.0,
            217.0 + delta,
            anchor="nw",
            text=tests[i][2],
            fill="#000000",
            font=("Comfortaa Regular", 16 * -1)
        )

        color = "#FF0000"
        if tests[i][3] == 'Positive':
            color = "#CA0000"
        else:
            color = "#039300"
        canvas.create_text(
            372.0,
            217.0 + delta,
            anchor="nw",
            text=tests[i][3],
            fill=color,
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


def create_ce():
    """
        Method that creates user page for seeing possible covid exposure
       :param button_6: button change to destroy
       :return
   """
    find_covid_exposures_by_ID(session, personal_information[0])
    canvas.delete("all")
    global button_list

    for x in button_list:
        x.destroy()

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


def create_p():
    """
        Method that creates user page for seeing places visited recently
        :param button_6: button change to destroy
        :return
    """
    find_place_visited(session, personal_information[0])

    canvas.delete("all")

    global button_list
    for x in button_list:
        x.destroy()

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
        text="Place",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        147.0,
        186.0,
        anchor="nw",
        text="Date",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        250.0,
        186.0,
        anchor="nw",
        text="Start H.",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        334.0,
        186.0,
        anchor="nw",
        text="End H.",
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

    for i in range(len(places)):

        delta = 32 * i

        canvas.create_text(
            29.0,
            214.0 + delta,
            anchor="nw",
            text=places[i][0],
            fill="#000000",
            font=("Comfortaa Bold", 16 * -1)
        )

        canvas.create_text(
            147.0,
            214.0 + delta,
            anchor="nw",
            text=places[i][1],
            fill="#000000",
            font=("Comfortaa Bold", 16 * -1)
        )

        canvas.create_text(
            250.0,
            214.0 + delta,
            anchor="nw",
            text=places[i][2],
            fill="#000000",
            font=("Comfortaa Bold", 16 * -1)
        )

        canvas.create_text(
            334.0,
            214.0 + delta,
            anchor="nw",
            text=places[i][3],
            fill="#000000",
            font=("Comfortaa Bold", 16 * -1)
        )

        # to be calculate
        risk = 0
        color = "#000000"
        if risk < 30:
            color = "#039300"
        elif risk < 65:
            color = "#FF7A00"
        else:
            color = "#CA0000"

        canvas.create_text(
            420.0,
            214.0 + delta,
            anchor="nw",
            text="Risk",
            fill=color,
            font=("Comfortaa Bold", 16 * -1)
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


"""
create the main window, titled it and fixed the position in the center of the screen
"""
window = Tk()
window.title('SMBUD Group 20')
screenPositionRight = int(window.winfo_screenwidth() / 2 - 700 / 2)
screenPositionDown = int(window.winfo_screenheight() / 2 - 500 / 2)
window.geometry("700x500" + "+{}+{}".format(screenPositionRight, screenPositionDown))
window.configure(bg="#FAF8F5")

"""
create the workspace upon the windows and set the background
"""
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
    260.0,
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

# user login button
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

# app manager login button
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

# Open the connection
driver = open_connection()
session = driver.session()

window.mainloop()
