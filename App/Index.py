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
- lm = location manager

Buttons:

- button__1 : user front page
- button_0 : app manager front page

- button_1 : covid exposure
- button_2 : places visited
- button_3 : green pass
- button_4 : personal information
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
exposure = [ [date, place], [date, place], ... ]

checked id login :
- empty id field
- negative id
- out of range id
- not a number

checked mail:
- contains @
- contains .
- no spaces
- no comma

checked phone number:
- it's an integer

checked new ct:
- person exist
- test exist
- format of date
- format of hour

"""

from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, OptionMenu, END
from pandas import DataFrame
import PlotDBStructure as ps
import neo4j as nj
import datetime

import tkinter
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./Images")

QUERY_OPTIONS = [
    "1 - All contacts registered via the app",
    "2 - All covid exposures registered",
    "3 - All people who result positive after direct contact with a positive",
    "4 - All people who result positive after a vaccine dose",
    "5 - All people that live in a house with at least a positive now",
    "6 - Worst case of tree of exposures caused by a person",
    "7 - The first ten places visited with a higher risk rate",
    "8 - All people had contact with a positive and haven't done the test yet",
    "9 - All people that haven't gotten the vaccine yet",
    "10 - All people with just one dose of vaccine",
    "11 - All people with two doses of vaccine",
    "12 - All positive people",
    "13 - All visit relationships",
    "14 - Show the entire database"
]

QUERY_OPTIONS_TRENDS = [
    "1 - The average age of actual positives",
    "2 - The number of tests done for each month",
    "3 - The number of positives for each month",
    "4 - The number of vaccines done for each month",
    "5 - The number of people that received a vaccine for each CAP",
    "6 - The number of contacts registered via app for at most 10 person",
    "7 - The rate of vaccinated people who result positive"
]

USER = "neo4j"
PASSWORD = "cJhfqi7RhIHR4I8ocQtc5pFPSEhIHDVJBCps3ULNzbA"
URI = "neo4j+s://057f4a80.databases.neo4j.io"

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
location_information = []
new_fields_pi = []
green_pass = []
tests = []
places = []
exposures = []

"""error message"""
error = None

label = None

plot = None


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
        uri=URI, auth=nj.basic_auth(USER, PASSWORD))
    return connection


def close_connection(connection):
    """
    Method that close a connection
    :param connection: is the connection to terminate
    """
    connection.close()


"""DATABASE QUERIES"""


def app_contacts(tx):
    """
    Method that queries the database for collecting all people who directly or indirectly had a contact
    :param tx: session
    :return nodes of person
    """
    query = (
        "MATCH (n1:Person)-[r:APP_CONTACT]->(n2:Person) "
        "RETURN n1 , ID(n1) , n2 , ID(n2) , r , r.date , r.hour"
    )
    result = tx.run(query).data()
    return result


def covid_exposures(tx):
    """
    Method that queries the database for collecting all covid exposures
    :param tx: session
    :return nodes of person
    """
    query = (
        "MATCH (n1:Person)-[r:COVID_EXPOSURE]->(n2:Person) "
        "RETURN n1 , ID(n1) , n2 , ID(n2) , r , r.date , r.name"
    )
    result = tx.run(query).data()
    return result


def positive_after_contact(tx):
    """
        Method that queries the database for collecting all people that result positive after a contact
        :param tx: session
        :return: nodes of person
    """
    query = (
        "MATCH (i:Person)-[inf:COVID_EXPOSURE]->(p:Person)-[m:MAKE_TEST{result: \"Positive\"}]->(Test) "
        "WHERE m.date > inf.date + duration({days: 1}) "
        "RETURN p, ID(p)"
    )
    result = tx.run(query).data()
    return result


def positive_after_one_dose(tx):
    """
         Method that queries the database for collecting all people that result positive after a dose of vaccine
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH(t:Test)<-[m:MAKE_TEST{result: \"Positive\"}]-(p:Person)-[g: GET_VACCINE]->(v:Vaccine) "
        "WHERE NOT (()<-[:GET_VACCINE]-(p)-[:GET_VACCINE]->()) AND m.date > g.date "
        "RETURN p , ID(p)"
    )
    result = tx.run(query).data()
    return result


def people_live_in_positive_house(tx):
    """
         Method that queries the database for collecting all people that live in a house with a positive
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH (p:Person)-[:LIVE]->(h:House)<-[:LIVE]-(pp:Person)-[r:MAKE_TEST{result: \"Positive\"}]->() "
        "WHERE r.date >= date() - duration({days: 10}) "
        "RETURN pp , ID(pp) , COLLECT(p), COLLECT(ID(p)) , h , ID(h)"
    )
    result = tx.run(query).data()
    return result


def tree_of_exposures(tx , id):
    """
         Method that queries the database for collecting all the exposure generated by a Person
         :param tx: session
         :param id: the person that started the contagious
         :return nodes of person
    """
    query = (
        """
        MATCH g1 = (p1:Person)-[relationship1:COVID_EXPOSURE*1..2]->(p2:Person)
        WHERE ID(p1) = $id AND 
            ALL ( idx in range(1 , size(relationships(g1)) - 1) 
            WHERE (relationships(g1))[idx - 1].date <= (relationships(g1))[idx].date
            )

        MATCH g2 = (p2)-[relationship2:COVID_EXPOSURE*0..2]->(p5:Person)
        WHERE 
            ALL (idx in range(1 , size(relationships(g2)) - 1) 
            WHERE (relationships(g2))[idx - 1].date <= (relationships(g2))[idx].date
            )

        MATCH ()<-[t1:MAKE_TEST{result: "Positive"}]-(p3:Person)-[ce:COVID_EXPOSURE]->(p4:Person)-[t2:MAKE_TEST{result: "Positive"}]->()
        WHERE t1.date <= t2.date AND ce.date <= t1.date AND (ce IN relationships(g1) OR ce IN relationships(g2))
        RETURN DISTINCT p3 , ID(p3) , ce , ce.name , ce.date , p4 , ID(p4)
        """
    )

    result = tx.run(query , id = id).data()
    return result


def ten_risk_location(tx):
    """
         Method that queries the database for collecting 10 locations with the highest risk
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH (p:Person)-[v:VISIT]->(l1:Location), (p)-[m:MAKE_TEST {result: \"Positive\"}]->(t:Test) "
        "WHERE v.date <= m.date <= v.date + duration({Days: 10}) AND v.date >= date() - duration({Days: 30}) "
        "with (COUNT(DISTINCT(p)))*1.0 as num, id(l1) as i "

        "MATCH (p1:Person)-[v1:VISIT]->(l:Location) "
        "WHERE v1.date >= date() - duration({Days: 30}) and id(l) = i "
        "with (COUNT(DISTINCT(p1))) as den, num, l "

        "return num/den as rate, l , ID(l) ORDER BY rate DESC LIMIT 10"
    )
    result = tx.run(query).data()
    return result


def people_at_risk_without_test(tx):
    """
         Method that queries the database for collecting all people that appeared in a covid exposure but haven't done
         the test yet
         :param tx: session
         :return nodes of person
     """

    query = (
        "MATCH(i:Person)-[inf: COVID_EXPOSURE]->(p:Person) "
        "WHERE NOT EXISTS { MATCH (i)-[inf: COVID_EXPOSURE]->(p), (p3:Person)-[m: MAKE_TEST]->(:Test) "
        "WHERE m.date >= inf.date AND id(p) = id(p3) } "
        "RETURN p , ID(p)"
    )
    result = tx.run(query).data()
    return result


def people_with_no_vaccine(tx):
    """
         Method that queries the database for collecting all people that hasn't gotten the vaccine yet
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH (p:Person) "
        "WHERE NOT ((p)-[:GET_VACCINE]->()) "
        "RETURN p , ID(p)"
    )
    result = tx.run(query).data()
    return result


def people_with_one_dose(tx):
    """
         Method that queries the database for collecting all people that has just a dose of vaccine
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH (n1:Person)-[r:GET_VACCINE]->(n2:Vaccine) "
        "WHERE NOT (()<-[:GET_VACCINE]-(n1)-[:GET_VACCINE]->()) "
        "RETURN n1 , ID(n1) , r , r.date , r.country , r.expirationDate , n2 , ID(n2)"
    )
    result = tx.run(query).data()
    return result


def people_with_two_dose(tx):
    """
         Method that queries the database for collecting all people that has two doses of vaccine
         :param tx: session
         :return nodes of person
     """
    query = (
        "MATCH (n2:Vaccine)<-[r1:GET_VACCINE]-(n1:Person)-[r2:GET_VACCINE]->(n3:Vaccine) "
        "WHERE r1 <> r2 AND r1.date < r2.date "
        "RETURN n1 , ID(n1) , r1 , r1.date , r1.country , r1.expirationDate , n2 , ID(n2) , "
        "r2 , r2.date , r2.country , r2.expirationDate , n3 , ID(n3)"
    )
    result = tx.run(query).data()
    return result


def positive_with_vaccine(tx):
    """
      Method that queries the database to calculate how many people who are vaccinated results positive to a covid test
      :param tx: session
      """
    query = (
        "MATCH (v:Vaccine)<-[g:GET_VACCINE]-(p:Person)-[m:MAKE_TEST{result: \"Positive\"}]->(t:Test) "
        "MATCH (v)<-[g1:GET_VACCINE]-(p1: Person) "
        "WHERE m.date > g.date "
        "RETURN (COUNT(DISTINCT(p)))*100/COUNT(DISTINCT(p1)) AS rate, v.name"
    )

    rate = []
    vaccine = []

    result = tx.run(query)

    for x in result:
        rate.append(x.data()["rate"])
        vaccine.append(x.data()["v.name"])

    return [vaccine, rate]


def find_positive(tx):
    """
      Method that queries the database to find all positive Person
      :param tx: session
      :return: nodes of Person
    """
    query = (
        """
        MATCH (p:Person)-[t:MAKE_TEST{result: \"Positive\"}]->()
        WHERE NOT EXISTS {
            MATCH (p)-[t2:MAKE_TEST{result: \"Negative\"}]->()
            WHERE t2.date > t.date
        }
        RETURN distinct p , ID(p)
        """
    )

    result = tx.run(query).data()
    return result


def find_all_visit(tx):
    """
      Method that queries the database to find all VISIT relationships
      :param tx: session
      :return: nodes of Person , Location
    """
    query = (
        """
        MATCH (p:Person)-[r:VISIT]->(l:Location)
        RETURN p , ID(p) , r , r.start_hour , r.end_hour , r.date , l , ID(l)
        """
    )
    result = tx.run(query).data()
    return result


def findAllPerson(tx):
    """
    Method that finds all the nodes Person in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (p:Person) "
        "RETURN p , ID(p);"
    )
    results = tx.run(query).data()
    return results


def findAllHome(tx):
    """
    Method that finds all the nodes House in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (h:House) "
        "RETURN h , ID(h);"
    )
    results = tx.run(query).data()
    return results


def findAllLocation(tx):
    """
    Method that finds all the nodes Location in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (l:Location) "
        "RETURN l , ID(l);"
    )
    results = tx.run(query).data()
    return results


def findAllVaccine(tx):
    """
    Method that finds all the nodes Vaccine in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (v:Vaccine) "
        "RETURN v , ID(v);"
    )
    results = tx.run(query).data()
    return results


def findAllTest(tx):
    """
    Method that finds all the nodes Test in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (t:Test) "
        "RETURN t , ID(t);"
    )
    results = tx.run(query).data()
    return results


def findAllLiveRelationships(tx):
    """
    Method that finds all Live relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:LIVE]->(n2:House) "
        "RETURN ID(n1) , r , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def findAllAppContactRelationships(tx):
    """
    Method that finds all App_Contact relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:APP_CONTACT]->(n2:Person) "
        "RETURN ID(n1) , r , r.date , r.hour, ID(n2);"
    )
    results = tx.run(query).data()
    return results


def findAllVisitRelationships(tx):
    """
    Method that finds all VISIT relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:VISIT]->(n2:Location) "
        "RETURN ID(n1) , r , r.date , r.start_hour , r.end_hour , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def findAllGetVaccineRelationships(tx):
    """
    Method that finds all GET (a vaccine) relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:GET_VACCINE]->(n2:Vaccine) "
        "RETURN ID(n1) , r , r.date , r.country , r.expirationDate , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def findAllMakeTestRelationships(tx):
    """
    Method that finds all MAKE (a test) relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:MAKE_TEST]->(n2:Test) "
        "RETURN ID(n1) , r , r.date , r.hour , r.result , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def findAllInfectedRelationships(tx):
    """
    Method that finds all INFECTED relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1:Person)-[r:COVID_EXPOSURE]->(n2:Person) "
        "RETURN ID(n1) , r , r.date , r.name , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def find_vaccinated_for_CAP(tx):
    """
    Method that queries the database to calculate how many people are vaccinated in each CAP
    :param tx: session
    """
    query = (
        "MATCH(p:Person)-[g:GET_VACCINE]->(v:Vaccine), (p)-[l:LIVE]->(h:House) "
        "WITH h AS house, p AS person "
        "RETURN COUNT(DISTINCT(person)) AS vaccinated, house.CAP ORDER BY vaccinated DESC"
    )

    cap = []
    vaccinated = []

    result = tx.run(query)

    for x in result:
        cap.append(x.data()["house.CAP"])
        vaccinated.append(x.data()["vaccinated"])

    return [cap, vaccinated]


def find_contacts_for_person(tx):
    """
    Method that queries the database to calculate how many contacts had a person
    :param tx: session
    """
    query = (
        "MATCH(p:Person)-[a:APP_CONTACT]->(:Person) "
        "RETURN COUNT(a), p.name LIMIT 10"
    )

    count = []
    person = []

    result = tx.run(query)

    for x in result:
        count.append(x.data()["COUNT(a)"])
        person.append(x.data()["p.name"])

    return [count, person]


def find_test_for_month(tx):
    """
    Method that queries the database to calculate how many tests were done each month
    :param tx: session
    """
    query = (
        "MATCH(p: Person)-[m: MAKE_TEST]->(t:Test) "
        "RETURN COUNT(m), m.date.month"
    )

    result = tx.run(query)
    months = np.zeros(12)
    for x in result:
        months[x.data()["m.date.month"] - 1] = x.data()["COUNT(m)"]

    return months


def find_positive_for_month(tx):
    """
    Method that queries the database to calculate how many positives there were each month
    :param tx: session
    """
    query = (
        "MATCH (p:Person)-[m:MAKE_TEST{result:\"Positive\"}]->(t:Test) "
        "RETURN COUNT(m), m.date.month"
    )

    result = tx.run(query)
    months = np.zeros(12)
    for x in result:
        months[x.data()["m.date.month"] - 1] = x.data()["COUNT(m)"]

    return months


def find_vaccine_for_month(tx):
    """
    Method that queries the database to calculate how many vaccines were made each month
    :param tx: session
    """
    query = (
        "MATCH (p:Person)-[g:GET_VACCINE]->(v:Vaccine) "
        "RETURN COUNT(g), g.date.month "
    )

    result = tx.run(query)
    months = np.zeros(12)
    for x in result:
        months[x.data()["g.date.month"] - 1] = x.data()["COUNT(g)"]

    return months


def positive_age_average(tx):
    """
    Method that queries the database to understand the average age of actual positive
    :param tx: session
    """
    query = (
        "MATCH (pp:Person)-[r:MAKE_TEST]->(t:Test) "
        "WHERE r.result = \"Positive\" AND r.date >= date() - duration({days: 10}) "
        "RETURN AVG(toFloat(pp.age)) AS average"
    )

    result = tx.run(query).data()
    average = result[0]['average']
    if average is not None:
        average = round(average, 2)
    return average


def find_location_by_ID(tx, ID):
    """
    Method that finds a location given it's ID
    :param tx: is the transaction
    :param ID: is the ID to find
    :return: all the nodes that have attribute equal to ID
    """
    global location_information
    location_information = []

    query = (
        "MATCH (l:Location) "
        "WHERE id(l) = $ID "
        "RETURN l.name "
    )
    result = tx.run(query, ID=ID)

    location_information.append(ID)

    for node in result:
        location_information.append(node.data()['l.name'])


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
        "MATCH(p: Person)-[r:GET_VACCINE]->(v: Vaccine) "
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
        "MATCH(p: Person)-[r:MAKE_TEST]->(n:Test) "
        "WHERE id(p) = $ID "
        "RETURN n.name, r.date, r.hour, r.result "
        "ORDER BY r.date DESC "
        "LIMIT 10"
    )

    result = tx.run(query, ID=ID)

    for relation in result:
        name = relation.data()['n.name'].split(" ")
        test = [name[0], relation.data()['r.date']]
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
    query = (
        "MATCH (p: Person)-[i:COVID_EXPOSURE]->(p1:Person) "
        "WHERE id(p1) = $ID "
        "RETURN i.date, i.name "
        "ORDER BY i.date DESC "
        "LIMIT 10"
    )

    global exposures
    exposures = []

    result = tx.run(query, ID=ID)
    for data in result:
        exposure = [data.data()['i.date'], data.data()['i.name']]
        exposures.append(exposure)


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
        "RETURN r.date, l.name, r.start_hour, r.end_hour, id(l) "
        "ORDER BY r.date DESC "
        "LIMIT 10"
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
        location_id = relation.data()['id(l)']
        risk_query = (
            "MATCH (p:Person)-[v:VISIT]->(l:Location), (p)-[m:MAKE_TEST {result: \"Positive\"}]->(t:Test) "
            "WHERE v.date <= m.date <= v.date + duration({Days: 10}) AND v.date >= date() - duration({Days: 30}) and "
            "id(l)= $ID "
            "with (COUNT(DISTINCT(p)))*1.0 as num, id(l) as i "

            "MATCH (p1:Person)-[v1:VISIT]->(l)  "
            "WHERE  v1.date >= date() - duration({Days: 30}) and id(l) = i "
            "with (COUNT(DISTINCT(p1))) as den, num  "

            "return num/den as rate "
        )

        risk_rate = tx.run(risk_query, ID=location_id)

        risk = 0
        result = risk_rate.data()
        if len(result) != 0:
            risk = result[0]['rate'] * 100
        risk_formatted = round(risk, 2)
        place.append(risk_formatted)
        places.append(place)


def check_if_person_exist(tx, ID):
    """
    Method that queries the database for understand if a person node exist
    :param tx: is the transaction
    :param ID: is the ID of the person
     :return TRUE OR FALSE
    """
    query = (
        "MATCH (p:Person) "
        "WHERE id(p) = $ID "
        "RETURN p"
    )

    result = tx.run(query, ID=ID)
    count = 0
    for node in result:
        count = count + 1

    return count


def check_if_test_exist(tx, ID):
    """
       Method that queries the database for understand if a test node exist
       :param tx: is the transaction
       :param ID: is the ID of the test
       :return TRUE OR FALSE
    """
    query = (
        "MATCH (t:Test) "
        "WHERE id(t) = $ID "
        "RETURN t"
    )

    result = tx.run(query, ID=ID)
    count = 0
    for node in result:
        count = count + 1

    return count


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
        "MERGE (p)-[:MAKE_TEST{date:date($date) , hour: time($hour) ,result:$result}]->(t); "
    )
    tx.run(query, ID=ID, testId=testId, date=date, hour=hour, result=result)


def delete_contact_exposure(tx, ID):
    """
    Method that update database after a negative test insert --> delete the entry
    :param tx: session
    """
    query = (
        "MATCH (p:Person) - [inf:COVID_EXPOSURE]-> (i:Person) - [m: MAKE_TEST{result: \"Negative\"}]->(:Test) "
        "WHERE m.date >= inf.date + duration({days: 7}) and id(i) = $id "
        "DELETE inf "
    )
    tx.run(query, id=ID)


def createRelationshipsInfect(id, test_date, test_hour, daysBack):
    """
    Method that finds all the contacts of a positive person
    :param daysBack: is the number of days to look in the past
    :param id: is the id of the positive person
    :return: a list of people who got in contact with the positive person
    """
    familyQuery = (
        "MATCH (pp:Person)-[:LIVE]->(h:House)<-[:LIVE]-(ip:Person) "
        "WHERE ID(pp) = $id AND ip <> pp AND NOT (ip)<-[:COVID_EXPOSURE]-(pp)"
        "RETURN DISTINCT ID(ip);"
    )
    appContactQuery = (
        "MATCH (pp:Person)-[r1:APP_CONTACT]->(ip:Person) "
        "WHERE ID(pp) = $id AND (r1.date > date($date) OR (r1.date = date($date) AND r1.hour >= time($hour))) "
        "AND (r1.date < date($date) + duration({days:7}) OR (r1.date = date($date)+duration({days:7}) AND "
        "r1.hour <= time($hour))) "
        "AND NOT "
        "(pp)-[:COVID_EXPOSURE{date: r1.date}]->(ip)"
        "RETURN DISTINCT ID(ip) , r1.date;"
    )
    locationContactQuery = (
        "MATCH (pp:Person)-[r1:VISIT]->(l:Location)<-[r2:VISIT]-(ip:Person) "
        "WHERE ID(pp) = $id AND ip <> pp AND (r1.date > date($date) OR (r1.date = date($date) AND r1.start_hour >= time($hour))) "
        "AND (r1.date < date($date) + duration({days:7}) OR (r1.date = date($date)+duration({days:7}) AND "
        "r1.end_hour <= time($hour))) AND r2.date = r1.date AND "
        "((r1.start_hour < r2.start_hour AND r1.end_hour > r2.start_hour) OR "
        "(r2.start_hour < r1.start_hour AND r2.end_hour > r1.start_hour)) AND NOT "
        "(pp)-[:COVID_EXPOSURE{name: l.name , date: r1.date}]->(ip)"
        "RETURN DISTINCT ID(ip) , r1.date , l.name;"
    )

    # date = datetime.date.today() - datetime.timedelta(daysBack)
    """
    date is referred to date test - daysback 
    """
    date = datetime.datetime.strptime(test_date, "%Y-%m-%d") - datetime.timedelta(daysBack)
    infectedIds = []
    with driver.session() as s:
        familyInfected = s.read_transaction(findInfectInFamily, familyQuery, id)
        appInfected = s.read_transaction(findInfect, appContactQuery, id, date, test_hour)
        locationInfected = s.read_transaction(findInfect, locationContactQuery, id, date, test_hour)

        for el in familyInfected, appInfected, locationInfected:
            if len(el) > 0:
                # Take just the id
                infectedIds.append(el[0]['ID(ip)'])

        infectedIds = []
        for el in familyInfected:
            infectedIds.append(el['ID(ip)'])

        for infectedId in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:COVID_EXPOSURE{date:date($date)}]->(ip);"
            )
            s.write_transaction(createInfectFamily, query, id, infectedId, date.strftime("%Y-%m-%d"))

        infectedIds = []
        for el in appInfected:
            details = []
            details.append(el['ID(ip)'])
            details.append(el['r1.date'])
            infectedIds.append(details)

        for infectedId, infectedDate in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:COVID_EXPOSURE{date: date($date)}]->(ip);"
            )
            s.write_transaction(createInfectApp, query, id, infectedId, infectedDate)

        infectedIds = []

        for el in locationInfected:
            details = []
            details.append(el['ID(ip)'])
            details.append(el['r1.date'])
            details.append(el['l.name'])
            infectedIds.append(details)

        for infectedId, infectedDate, infectedPlace in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:COVID_EXPOSURE{date: date($date) , name: $name}]->(ip);"
            )
            s.write_transaction(createInfectLocation, query, id, infectedId, infectedDate, infectedPlace)


def findInfectInFamily(tx, query, id):
    """
    Method that executes the query to find the infected member of a family
    :param tx: is the transaction
    :param query: is the query to execute
    :param id: is the id of the positive Person
    """
    result = tx.run(query, id=id).data()
    return result


def findInfect(tx, query, id, date, hour):
    """
    Method that executes the query to find the Person infected by other Persons
    :param tx: is the transaction
    :param query: is the query to execute
    :param id: is the id of the positive Person
    :param date: is the date from wich start the tracking
    """
    result = tx.run(query, id=id, date=date, hour=hour).data()
    return result


def createInfectFamily(tx, query, id, ipid, date):
    """
    Method that create the relationship Infect
    """
    tx.run(query, id=id, ipid=ipid, date=date)


def createInfectApp(tx, query, id, ipid, date):
    """
    Method that create the relationship Infect
    """
    tx.run(query, id=id, ipid=ipid, date=date)


def createInfectLocation(tx, query, id, ipid, date, name):
    """
    Method that create the relationship Infect
    """
    tx.run(query, id=id, ipid=ipid, date=date, name=name)


def check_if_mail_exist(tx, email):
    """
       Method that queries the database for understand if a person with given email exist
       :param tx: is the transaction
       :param ID: is the ID of the person
        :return TRUE OR FALSE
       """
    query = (
        "MATCH (p:Person) "
        "WHERE p.mail = $mail "
        "RETURN p"
    )

    result = tx.run(query, mail=email).data()
    count = 0

    for node in result:
        count = count + 1

    return count


def create_visit(tx, email, shour, ehour, date):
    """
    Create a new visit
    """

    query = (
        "MATCH (p:Person) , (l:Location) "
        "WHERE p.mail = $mail AND id(l) = $locationId "
        "MERGE (p)-[:VISIT {date: date($date) , start_hour: time($startHour) , end_hour: time($endHour)}]->(l); "

    )

    tx.run(query, mail=email, locationId=location_information[0], date=date, startHour=shour, endHour=ehour)


"""VALUES MANAGING"""


def return_to_main(button_exit):
    # clear all

    button_exit.destroy()

    global plot
    global button_list
    global entry_list

    if plot is not None:
        plot.destroy()
    plot = None

    for x in button_list:
        x.destroy()
    button_list = []

    for x in entry_list:
        x.destroy()
    entry_list = []

    global personal_information
    personal_information = []

    global new_fields_pi
    new_fields_pi = []

    global green_pass
    green_pass = []

    global tests
    tests = []

    global places
    places = []

    global exposures
    exposures = []

    global error
    if error is not None:
        canvas.delete(error)

    error = None

    global label
    if label is not None:
        canvas.delete(label)
    label = None

    # build main

    canvas.delete("all")

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
        command=lambda: user_login(title, subtitle, button__1, button_0, location),
        relief="flat"
    )
    button_0.place(
        x=465.0,
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
        command=lambda: app_manager_login(title, subtitle, button__1, button_0, location),
        relief="flat"
    )

    button__1.place(
        x=35.0,
        y=405.0,
        width=200.0,
        height=60.0
    )

    location_image = PhotoImage(
        file=relative_to_assets("location.png"))
    location = Button(
        image=location_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: location_manager_login(title, subtitle, button__1, button_0, location),
        relief="flat"
    )

    location.place(
        x=250.0,
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

    image_image_1 = PhotoImage(
        file=relative_to_assets("logo.png"))
    image_1 = canvas.create_image(
        350.0,
        164.0,
        image=image_image_1
    )

    window.mainloop()


def perform_trend(choice):
    global label

    if label is not None:
        canvas.delete(label)

    global plot
    if plot is not None:
        plot.destroy()

    plot = None

    choice = variable.get()
    choice_number = choice.split(" ")

    if choice_number[0] == "1":
        average = positive_age_average(session)
        x = 325.0
        y = 240.0
        if average is None:
            average = "Nobody is positive :)"
            x = 273.0
        label = canvas.create_text(
            x,
            y,
            anchor="nw",
            text=average,
            fill="#000000",
            font=("Comfortaa Bold", 20 * -1)
        )

    elif choice_number[0] == "2":
        test_month = find_test_for_month(session)

        data = {'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'Test': test_month
                }

        df = DataFrame(data, columns=['Month', 'Test'])

        figure = plt.Figure(figsize=(5, 4), dpi=60)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, window)
        line.get_tk_widget().pack()
        line.get_tk_widget().place(x=200, y=240)
        df = df[['Month', 'Test']].groupby('Month').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)

        plot = line.get_tk_widget()

    elif choice_number[0] == "3":
        positives = find_positive_for_month(session)

        data = {'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'Positives': positives
                }

        df = DataFrame(data, columns=['Month', 'Positives'])

        figure = plt.Figure(figsize=(5, 4), dpi=60)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, window)
        line.get_tk_widget().pack()
        line.get_tk_widget().place(x=200, y=240)
        df = df[['Month', 'Positives']].groupby('Month').sum()
        df.plot(kind='line', legend=True, ax=ax, color='g', marker='o', fontsize=10)

        plot = line.get_tk_widget()

    elif choice_number[0] == "4":
        vaccines = find_vaccine_for_month(session)

        data = {'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'Vaccine': vaccines
                }

        df = DataFrame(data, columns=['Month', 'Vaccine'])

        figure = plt.Figure(figsize=(5, 4), dpi=60)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, window)
        line.get_tk_widget().pack()
        line.get_tk_widget().place(x=200, y=240)
        df = df[['Month', 'Vaccine']].groupby('Month').sum()
        df.plot(kind='line', legend=True, ax=ax, color='y', marker='o', fontsize=10)

        plot = line.get_tk_widget()

    elif choice_number[0] == "5":
        result = find_vaccinated_for_CAP(session)

        cap = result[0]
        vaccinated = result[1]

        if len(result[0]) != 0:
            data = {'CAP': cap,
                    'Vaccinated': vaccinated
                    }

            df = DataFrame(data, columns=['CAP', 'Vaccinated'])

            figure = plt.Figure(figsize=(5, 4), dpi=60)
            ax = figure.add_subplot(111)
            bar = FigureCanvasTkAgg(figure, window)
            bar.get_tk_widget().pack()
            bar.get_tk_widget().place(x=200, y=240)
            df = df[['CAP', 'Vaccinated']].groupby('CAP').sum()
            df.plot(kind='barh', legend=True, ax=ax, color='m')

            plot = bar.get_tk_widget()

        else:
            label = canvas.create_text(
                273.0,
                240.0,
                anchor="nw",
                text="No data to show",
                fill="#000000",
                font=("Comfortaa Bold", 20 * -1)
            )

    elif choice_number[0] == "6":

        result = find_contacts_for_person(session)
        count = result[0]
        person = result[1]

        if len(result[0]) != 0:

            data = {'Person': person,
                    'Count': count
                    }

            df = DataFrame(data, columns=['Person', 'Count'])

            figure = plt.Figure(figsize=(7, 4), dpi=60)
            ax = figure.add_subplot(111)
            bar = FigureCanvasTkAgg(figure, window)
            bar.get_tk_widget().pack()
            bar.get_tk_widget().place(x=180, y=240)
            df = df[['Person', 'Count']].groupby('Person').sum()
            df.plot(kind='barh', legend=True, ax=ax)

            plot = bar.get_tk_widget()

        else:

            label = canvas.create_text(
                273.0,
                240.0,
                anchor="nw",
                text="No data to show",
                fill="#000000",
                font=("Comfortaa Bold", 20 * -1)
            )

    elif choice_number[0] == "7":

        result = positive_with_vaccine(session)
        vaccine = result[0]
        rate = result[1]

        if len(result[0]) != 0:

            data = {'Vaccine': vaccine,
                    'Rate': rate
                    }

            df = DataFrame(data, columns=['Vaccine', 'Rate'])

            figure = plt.Figure(figsize=(7, 4), dpi=60)
            ax = figure.add_subplot(111)
            bar = FigureCanvasTkAgg(figure, window)
            bar.get_tk_widget().pack()
            bar.get_tk_widget().place(x=180, y=240)
            df = df[['Vaccine', 'Rate']].groupby('Vaccine').sum()
            df.plot(kind='barh', legend=True, ax=ax, color='c')

            plot = bar.get_tk_widget()
        else:

            label = canvas.create_text(
                273.0,
                240.0,
                anchor="nw",
                text="No data to show",
                fill="#000000",
                font=("Comfortaa Bold", 20 * -1)
            )


def perform_query(choice):
    choice = variable.get()
    choice_number = choice.split(" ")

    # Initialize the network for the graph
    ps.PlotDBStructure.__init__()

    if choice_number[0] == "1":
        with driver.session() as s:
            result = s.read_transaction(app_contacts)

            # Create all the nodes
            nodesToPrint = []
            for element in result:
                elementDict = {'p': element['n1'], 'ID(p)': element['ID(n1)']}
                nodesToPrint.append(elementDict)
                elementDict = {'p': element['n2'], 'ID(p)': element['ID(n2)']}
                nodesToPrint.append(elementDict)

            ps.PlotDBStructure.setPersonColor('green')
            ps.PlotDBStructure.addStructure(nodesToPrint)
            ps.PlotDBStructure.addStructure(result)
            ps.PlotDBStructure.network.get_nodes()

    elif choice_number[0] == "2":
        with driver.session() as s:
            result = s.read_transaction(covid_exposures)

            # Create all the nodes
            nodesToPrint = []
            for element in result:
                elementDict = {'p': element['n1'], 'ID(p)': element['ID(n1)']}
                nodesToPrint.append(elementDict)
                elementDict = {'p': element['n2'], 'ID(p)': element['ID(n2)']}
                nodesToPrint.append(elementDict)

            ps.PlotDBStructure.setPersonColor('blue')
            ps.PlotDBStructure.addStructure(nodesToPrint)
            ps.PlotDBStructure.addStructure(result)
            ps.PlotDBStructure.network.get_nodes()

    elif choice_number[0] == "3":
        with driver.session() as s:
            result = s.read_transaction(positive_after_contact)
            ps.PlotDBStructure.addStructure(result)

    elif choice_number[0] == "4":
        with driver.session() as s:
            result = s.read_transaction(positive_after_one_dose)
            ps.PlotDBStructure.addStructure(result)

    elif choice_number[0] == "5":
        # All people that live in a house with at least a positive now
        with driver.session() as s:
            result = s.read_transaction(people_live_in_positive_house)
            # Set color = 'red' to better identify the positive member
            ps.PlotDBStructure.setPersonColor('red')
            listOfNodes = []
            for element in result:
                # Add the positive Person in the network
                elementDict = {'p': element['pp'], 'ID(p)': element['ID(pp)']}
                listOfNodes.append(elementDict)
            ps.PlotDBStructure.addStructure(listOfNodes)
            # Set the Person nodes color to the default one
            ps.PlotDBStructure.setPersonColor()

            for element in result:
                nodesToPrint = []
                # Add the House in the network
                elementDict = {'h': element['h'], 'ID(h)': element['ID(h)']}
                nodesToPrint.append(elementDict)
                ps.PlotDBStructure.addStructure(nodesToPrint)

                present = False
                for r in ps.PlotDBStructure.network.get_edges():
                    if element['ID(pp)'] == r['from'] and element['ID(h)'] == r['to']:
                        present = True
                        break
                if not present:
                    # Add the LIVE relationships to the positive Person
                    ps.PlotDBStructure.addLiveRelationships(element['ID(pp)'], element['ID(h)'])

                # Add the other members of the families
                for i in range(len(element['COLLECT(p)']) - 1):
                    elementDict = {'p': element['COLLECT(p)'][i], 'ID(p)': element['COLLECT(ID(p))'][i]}
                    personToPrint = [elementDict]
                    ps.PlotDBStructure.addStructure(personToPrint)

                    # if the LIVE relationships is already present, don't add it
                    present = False
                    for r in ps.PlotDBStructure.network.get_edges():
                        if element['COLLECT(ID(p))'][i] == r['from'] and element['ID(h)'] == r['to']:
                            present = True
                            break
                    if not present:
                        ps.PlotDBStructure.addLiveRelationships(element['COLLECT(ID(p))'][i], element['ID(h)'])

    elif choice_number[0] == "6":
        with driver.session() as s:
            # Take all the positive Person
            result = s.read_transaction(find_positive)
            idMax = result[0]['ID(p)']
            maxNumOfEl = 0
            for el in result:
                resultOfId = s.read_transaction(tree_of_exposures , el['ID(p)'])
                if len(resultOfId) > maxNumOfEl:
                    maxNumOfEl = len(resultOfId)
                    idMax = el['ID(p)']



            result = s.read_transaction(tree_of_exposures , idMax)
            nodeToPrint = []
            for element in result:
                elementDict = {'p': element['p3'], 'ID(p)': element['ID(p3)']}
                # If it's the root
                if element['ID(p3)'] == idMax:
                    ps.PlotDBStructure.setPersonColor('red')
                    ps.PlotDBStructure.addStructure([elementDict])
                    ps.PlotDBStructure.setPersonColor()
                else:
                    nodeToPrint.append(elementDict)
                elementDict = {'p': element['p4'], 'ID(p)': element['ID(p4)']}
                nodeToPrint.append(elementDict)
                ps.PlotDBStructure.addStructure(nodeToPrint)

                # To avoid auto-relationships
                if element['ID(p3)'] == element['ID(p4)']:
                    continue

                present = False
                for r in ps.PlotDBStructure.network.get_edges():
                    if element['ID(p3)'] == r['from'] and element['ID(p4)'] == r['to']:
                        present = True
                        break
                if not present:
                    ps.PlotDBStructure.addCovidExposureRelationships(element['ID(p3)'] , element['ID(p4)'] ,
                                                                 element['ce.date'] , element['ce.name'])

    elif choice_number[0] == "7":
        with driver.session() as s:
            result = s.read_transaction(ten_risk_location)
            ps.PlotDBStructure.addStructure(result)

    elif choice_number[0] == "8":
        with driver.session() as s:
            result = s.read_transaction(people_at_risk_without_test)
            ps.PlotDBStructure.addStructure(result)

    elif choice_number[0] == "9":
        with driver.session() as s:
            result = s.read_transaction(people_with_no_vaccine)
            nodesToPrint = []
            for node in result:
                nodesToPrint.append(node)
            ps.PlotDBStructure.addStructure(nodesToPrint)

    elif choice_number[0] == "10":
        with driver.session() as s:
            result = s.read_transaction(people_with_one_dose)

            nodesToPrint = []
            relationshipsToPrint = []
            for element in result:
                elementDict = {'p': element['n1'], 'ID(p)': element['ID(n1)']}
                nodesToPrint.append(elementDict)
                elementDict = {'v': element['n2'], 'ID(v)': element['ID(n2)']}
                nodesToPrint.append(elementDict)
                elementDict = {'r': element['r'], 'r.date': element['r.date'] ,
                               'r.expirationDate': element['r.expirationDate'] , 'r.country': element['r.country'] ,
                               'ID(n1)': element['ID(n1)'] , 'ID(n2)': element['ID(n2)']}
                relationshipsToPrint.append(elementDict)
            # Add the nodes and the relationships
            ps.PlotDBStructure.addStructure(nodesToPrint)
            ps.PlotDBStructure.addStructure(relationshipsToPrint)

    elif choice_number[0] == "11":
        with driver.session() as s:
            result = s.read_transaction(people_with_two_dose)

            nodesToPrint = []
            relationshipsToPrint = []
            for element in result:
                elementDict = {'p': element['n1'], 'ID(p)': element['ID(n1)']}
                nodesToPrint.append(elementDict)
                elementDict = {'v': element['n2'], 'ID(v)': element['ID(n2)']}
                nodesToPrint.append(elementDict)
                elementDict = {'v': element['n3'], 'ID(v)': element['ID(n3)']}
                nodesToPrint.append(elementDict)
                elementDict = {'r': element['r1'], 'r.date': element['r1.date'] ,
                               'r.expirationDate': element['r1.expirationDate'] , 'r.country': element['r1.country'] ,
                               'ID(n1)': element['ID(n1)'] , 'ID(n2)': element['ID(n2)']}
                relationshipsToPrint.append(elementDict)
                elementDict = {'r': element['r2'], 'r.date': element['r2.date'] ,
                               'r.expirationDate': element['r2.expirationDate'] , 'r.country': element['r2.country'] ,
                               'ID(n1)': element['ID(n1)'] , 'ID(n2)': element['ID(n2)']}
                relationshipsToPrint.append(elementDict)
            # Add the nodes and the relationships
            ps.PlotDBStructure.addStructure(nodesToPrint)
            ps.PlotDBStructure.addStructure(relationshipsToPrint)

    elif choice_number[0] == "12":
        with driver.session() as s:
            result = s.read_transaction(find_positive)
            ps.PlotDBStructure.addStructure(result)

    elif choice_number[0] == "13":
        with driver.session() as s:
            result = s.read_transaction(find_all_visit)

            nodesToPrint = []
            relationshipsToPrint = []
            for element in result:
                elementDict = {'p': element['p'] , 'ID(p)': element['ID(p)']}
                nodesToPrint.append(elementDict)
                elementDict = {'l': element['l'] , 'ID(l)': element['ID(l)']}
                nodesToPrint.append(elementDict)
                elementDict = {'r': element['r'] , 'ID(n1)': element['ID(p)'] , 'ID(n2)': element['ID(l)'],
                               'r.date': element['r.date'] , 'r.start_hour': element['r.start_hour'] ,
                               'r.end_hour': element['r.end_hour']}
                relationshipsToPrint.append(elementDict)
            ps.PlotDBStructure.addStructure(nodesToPrint)
            ps.PlotDBStructure.addStructure(relationshipsToPrint)

    elif choice_number[0] == "14":
        with driver.session() as s:
            personNodes = s.read_transaction(findAllPerson)
            houseNodes = s.read_transaction(findAllHome)
            locationNodes = s.read_transaction(findAllLocation)
            vaccineNodes = s.read_transaction(findAllVaccine)
            testNodes = s.read_transaction(findAllTest)
            liveRelationships = s.read_transaction(findAllLiveRelationships)
            visitRelationships = s.read_transaction(findAllVisitRelationships)
            appContactRelationships = s.read_transaction(findAllAppContactRelationships)
            getRelationships = s.read_transaction(findAllGetVaccineRelationships)
            makeRelationships = s.read_transaction(findAllMakeTestRelationships)
            infectRelationships = s.read_transaction(findAllInfectedRelationships)

            # Add nodes
            ps.PlotDBStructure.addStructure(personNodes)
            ps.PlotDBStructure.addStructure(houseNodes)
            ps.PlotDBStructure.addStructure(locationNodes)
            ps.PlotDBStructure.addStructure(vaccineNodes)
            ps.PlotDBStructure.addStructure(testNodes)

            # Add relationships
            ps.PlotDBStructure.addStructure(liveRelationships)
            ps.PlotDBStructure.addStructure(visitRelationships)
            ps.PlotDBStructure.addStructure(appContactRelationships)
            ps.PlotDBStructure.addStructure(makeRelationships)
            ps.PlotDBStructure.addStructure(getRelationships)
            ps.PlotDBStructure.addStructure(infectRelationships)

    else:
        pass

    # Show the graph built
    ps.PlotDBStructure.showGraph()


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

    n_person = check_if_person_exist(session, ID)
    if n_person == 0:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: person doesn't exist ",
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

    n_test = check_if_test_exist(session, testId)

    if n_test == 0:
        error = canvas.create_text(
            175.0,
            455.0,
            anchor="nw",
            text="ERROR: test type doesn't exist ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    date_split = date_initial.split("-")
    if len(date_split) != 3:
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
    if len(hour_split) != 2:
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

    if (0 > hour_split[0] or hour_split[0] > 23) or (0 > hour_split[1] or hour_split[1] > 59):

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
    if result == "Negative":
        delete_contact_exposure(session, ID)

    elif result == "Positive":
        createRelationshipsInfect(ID, date_initial, hour_initial,10)

    create_add_ct()


def save_pi_changes(phone, email):
    """
    Method that catches and checks new entries inserted by user.
    If a field is empty its information will be replaced by older one
    :param phone: new phone
    :param email: new email
    :param address: new address
    """
    global error, new_fields_pi
    new_fields_pi = []

    if error is not None:
        canvas.delete(error)

    if (phone == '') and (email == ''):
        create_pi()

    if phone == '':
        phone = personal_information[4]
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
        elif (" " in email) or ("," in email):
            error = canvas.create_text(
                338,
                322,
                anchor="nw",
                text="ERROR: \nwrong email format \navoid using spaces and commas  ",
                fill="#CA0000",
                font=("Comfortaa Regular", 10 * -1)
            )
            return
        else:
            count = check_if_mail_exist(session, email)
            if count > 0:
                error = canvas.create_text(
                    338,
                    322,
                    anchor="nw",
                    text="ERROR: \nemail exists yet ",
                    fill="#CA0000",
                    font=("Comfortaa Regular", 10 * -1)
                )
                return

    new_fields_pi.append(phone)
    new_fields_pi.append(email)

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


def collect_location_information(ID_location, subtitle):
    """
    Method that is able to collect data and call personal information page constructor
    :param ID_person: id inserted by the user
    """

    # no integer or empty
    try:
        ID = int(ID_location)
    except ValueError:
        canvas.itemconfig(subtitle, text="The following field must be fulfilled with a number", fill="red")
        canvas.coords(subtitle, 160, 363)
        return

    global session

    global personal_information
    find_location_by_ID(session, ID)

    # id is not link to any person (also negative )
    if len(location_information) < 2:
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

    create_lm()


def location_cancel(entry_1, entry_2, entry_3):
    """
    Method that clears all entry in the page
    """
    global error

    if error is not None:
        canvas.delete(error)

    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)


def location_done(email, shour, ehour):
    """
    Method that checks if all fiels are filled rightly and calls the method that performs the query
    """

    global error

    if error is not None:
        canvas.delete(error)

    if email == '':
        email = personal_information[5]
    else:
        if len(email.split("@")) != 2:
            error = canvas.create_text(
                170.0,
                372.0,
                anchor="nw",
                text="ERROR: wrong email format '@' is missing ",
                fill="#CA0000",
                font=("Comfortaa Regular", 16 * -1)
            )
            return
        elif len(email.split(".")) < 2:
            error = canvas.create_text(
                170.0,
                372.0,
                anchor="nw",
                text="ERROR: wrong email format '.' is missing ",
                fill="#CA0000",
                font=("Comfortaa Regular", 16 * -1)
            )
            return
        elif (" " in email) or ("," in email):
            error = canvas.create_text(
                170.0,
                372.0,
                anchor="nw",
                text="ERROR: wrong email format avoid using spaces and commas  ",
                fill="#CA0000",
                font=("Comfortaa Regular", 16 * -1)
            )
            return

    count = check_if_mail_exist(session, email)
    if count != 1:
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: email does not exist  ",
            fill="#CA0000",
            font=("Comfortaa Regular", 16 * -1)
        )
        return

    hour_split = shour.split(":")
    if len(hour_split) != 2:
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid format of start hour, try with HH:MM",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    try:
        hour_split[0] = int(hour_split[0])
        hour_split[1] = int(hour_split[1])
    except ValueError:
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid start hour format, try with HH:MM ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    if (0 > hour_split[0] or hour_split[0] > 23) or (0 > hour_split[1] or hour_split[1] > 59):
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid start hour range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    hour_split_e = ehour.split(":")
    if len(hour_split_e) != 2:
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid format of end hour, try with HH:MM",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    try:
        hour_split_e[0] = int(hour_split_e[0])
        hour_split_e[1] = int(hour_split_e[1])
    except ValueError:
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid end hour format, try with HH:MM ",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    if (0 > hour_split_e[0] or hour_split_e[0] > 23) or (0 > hour_split_e[1] or hour_split_e[1] > 59):
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid end hour range",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    # if is provided a range
    if (hour_split_e[0] < hour_split[0]) or (hour_split_e[0] == hour_split[0] and hour_split_e[1] < hour_split[1]):
        error = canvas.create_text(
            170.0,
            372.0,
            anchor="nw",
            text="ERROR: invalid hour range, start hour must be before the end",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        return

    date = datetime.date.today().strftime('%Y-%m-%d')
    create_visit(session, email, shour, ehour, date)

    create_lm()


"""PAGE BUILDER"""


def create_lm():
    """
       Method that creates the location manager interface for registering new client that visit his location
       :return: nothing
    """
    canvas.delete("all")
    global button_list

    global plot
    if plot is not None:
        plot.destroy()
    plot = None

    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    entry_list = []

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

    canvas.create_text(
        160.0,
        166.0,
        anchor="nw",
        text="Register clients that today visit your location:",
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        160.0,
        206.0,
        anchor="nw",
        text=location_information[1],
        fill="#6370FF",
        font=("Comfortaa Bold", 20 * -1)
    )

    canvas.create_text(
        170.0,
        258.0,
        anchor="nw",
        text="Client Mail",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )
    canvas.create_text(
        170.0,
        298.0,
        anchor="nw",
        text="Start Hour",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        170.0,
        338.0,
        anchor="nw",
        text="End Hour",
        fill="#000000",
        font=("Comfortaa Bold", 16 * -1)
    )

    canvas.create_text(
        400.0,
        318.0,
        anchor="nw",
        text="HH:MM",
        fill="#000000",
        font=("Comfortaa Bold", 12 * -1)
    )

    entry_1 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_1.place(
        x=295.0,
        y=258.0,
        width=200.0,
        height=17.0
    )

    entry_2 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_2.place(
        x=295.0,
        y=297.0,
        width=91.0,
        height=17.0
    )

    entry_3 = Entry(
        bd=0,
        bg="#ffffff",
        highlightthickness=0
    )
    entry_3.place(
        x=295.0,
        y=338.0,
        width=91.0,
        height=17.0
    )

    close_image = PhotoImage(
        file=relative_to_assets("close.png"))
    close = Button(
        image=close_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: location_cancel(entry_1, entry_2, entry_3),
        relief="flat"
    )
    close.place(
        x=383.0,
        y=410.0,
        width=68.0,
        height=68.0
    )

    check_image = PhotoImage(
        file=relative_to_assets("check.png"))
    check = Button(
        image=check_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: location_done(entry_1.get(), entry_2.get(), entry_3.get()),
        relief="flat"
    )
    check.place(
        x=266.0,
        y=410.0,
        width=68.0,
        height=68.0
    )

    button_list = [check, close]

    entry_list = [entry_1, entry_2, entry_3]

    window.mainloop()


def user_login(title, subtitle, button__1, button_0, location):
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
    location.destroy()

    # modify the innter text
    canvas.itemconfig(title, text="Please insert your personal ID")
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

    button_image = PhotoImage(
        file=relative_to_assets("exit.png"))
    button_exit = Button(
        image=button_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: return_to_main(button_exit),
        relief="flat"
    )
    button_exit.place(
        x=610.0,
        y=40.0,
        width=55.0,
        height=60.0)

    # update window
    window.mainloop()


def app_manager_login(title, subtitle, button__1, button_0, location):
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
    location.destroy()

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

    button_image = PhotoImage(
        file=relative_to_assets("exit.png"))
    button_exit = Button(
        image=button_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: return_to_main(button_exit),
        relief="flat"
    )
    button_exit.place(
        x=620.0,
        y=421.0,
        width=55.0,
        height=60.0)

    window.mainloop()


def location_manager_login(title, subtitle, button__1, button_0, location):
    """
          Method that builds location manager login page
          :param title: text field from front page that has to modify
          :param subtitle: text field from front page that has to modify
          :param button__1: button to delete
          :param button_0: button to delete
          :param location: button to delete
          :return:
       """

    button__1.destroy()
    button_0.destroy()
    location.destroy()

    canvas.itemconfig(title, text="Please insert the ID of your location")
    canvas.coords(title, 100, 320)
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
        command=lambda: collect_location_information(entry_1.get(), subtitle),
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

    button_image = PhotoImage(
        file=relative_to_assets("exit.png"))
    button_exit = Button(
        image=button_image,
        borderwidth=1000,
        highlightthickness=0,
        command=lambda: return_to_main(button_exit),
        relief="flat"
    )
    button_exit.place(
        x=620.0,
        y=421.0,
        width=55.0,
        height=60.0)

    window.mainloop()


def create_add_ct():
    """
    Method that creates the app manager interface for inserting new covid test results
    :return:
    """
    canvas.delete("all")
    global button_list

    global plot
    if plot is not None:
        plot.destroy()
    plot = None

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
        470.0,
        250.0,
        anchor="nw",
        text="AAAA-MM-DD",
        fill="#000000",
        font=("Comfortaa Bold", 12 * -1)
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
        470.0,
        286.0,
        anchor="nw",
        text="HH:MM",
        fill="#000000",
        font=("Comfortaa Bold", 12 * -1)
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
        width=68.0,
        height=68.0
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
        width=68.0,
        height=68.0
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

    variable.set("Show...")

    opt = OptionMenu(window, variable, *QUERY_OPTIONS_TRENDS, command=perform_trend)
    opt.pack()
    opt.place(x=229, y=210)

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
    button_list = [button_1, button_2, button_3, opt]
    window.mainloop()


def create_db():
    """
    Method that creates app manager page for query the database
    :return:
    """
    canvas.delete("all")
    global button_list

    global plot
    if plot is not None:
        plot.destroy()
    plot = None

    for x in button_list:
        x.destroy()

    global entry_list

    for x in entry_list:
        x.destroy()

    button_list = []
    entry_list = []

    variable.set("Show...")

    opt = OptionMenu(window, variable, *QUERY_OPTIONS, command=perform_query)
    opt.pack()
    opt.place(x=229, y=210)

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

    canvas.create_text(
        130.0,
        300.0,
        anchor="nw",
        text="If the result is not empty, it is displayed in a browser window",
        fill="#000000",
        font=("Comfortaa ", 16 * -1)
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

    button_list = [button_1, button_2, button_3, opt]
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

    find_gp_by_ID(session, personal_information[0])

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
            text="No doses of covid vaccine were found",
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
    global plot
    if plot is not None:
        plot.destroy()

    plot = None

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

    if len(tests) == 0:
        canvas.create_text(
            31.0,
            201.0,
            anchor="nw",
            text="No covid tests were found",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        button_list = [button_1, button_2, button_3, button_4, button_5]
        window.mainloop()
        return

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

    if len(exposures) == 0:
        canvas.create_text(
            31.0,
            201.0,
            anchor="nw",
            text="No cases of covid exposure were found",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        button_list = [button_1, button_2, button_3, button_4, button_5]
        window.mainloop()
        return

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

    for i in range(len(exposures)):

        delta = 32 * i

        canvas.create_text(
            31.0,
            216.0 + delta,
            anchor="nw",
            text=exposures[i][0],
            fill="#000000",
            font=("Comfortaa Regular", 16 * -1)
        )

        if exposures[i][1] is None:

            canvas.create_text(
                143.0,
                216.0 + delta,
                anchor="nw",
                text=" - ",
                fill="#000000",
                font=("Comfortaa Regular", 16 * -1)
            )
        else:
            canvas.create_text(
                143.0,
                216.0 + delta,
                anchor="nw",
                text=exposures[i][1],
                fill="#000000",
                font=("Comfortaa Regular", 16 * -1)
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

    if len(places) == 0:
        canvas.create_text(
            31.0,
            201.0,
            anchor="nw",
            text="No places recently visited were found",
            fill="#CA0000",
            font=("Comfortaa Bold", 16 * -1)
        )
        button_list = [button_1, button_2, button_3, button_4, button_5]
        window.mainloop()
        return

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
        risk = places[i][4]
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
            text=str(risk) + "%",
            fill=color,
            font=("Comfortaa Bold", 16 * -1)
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
    command=lambda: user_login(title, subtitle, button__1, button_0, location),
    relief="flat"
)
button_0.place(
    x=465.0,
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
    command=lambda: app_manager_login(title, subtitle, button__1, button_0, location),
    relief="flat"
)

button__1.place(
    x=35.0,
    y=405.0,
    width=200.0,
    height=60.0
)

location_image = PhotoImage(
    file=relative_to_assets("location.png"))
location = Button(
    image=location_image,
    borderwidth=1000,
    highlightthickness=0,
    command=lambda: location_manager_login(title, subtitle, button__1, button_0, location),
    relief="flat"
)

location.place(
    x=250.0,
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

variable = StringVar(window)

window.mainloop()

# Close the connection
close_connection(driver)
