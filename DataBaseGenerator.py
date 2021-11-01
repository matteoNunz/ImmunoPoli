"""
Date: 28/10/2021
First sketch for a generator of data base structure for Neo4J

Problem: if in the file there are empty lines at the end ---> error
"""

import neo4j as nj
import graphistry
from random import randint , random
from enum import IntEnum


MAX_NUMBER_OF_FAMILY_MEMBER = 5
NUMBER_OF_FAMILY = 10

MAX_NUMBER_OF_CONTACT_PER_DAY = 5  # For new contact relationships

MAX_NUMBER_OF_VISIT_PER_DAY = 5  # For new visit relationships

MAX_CIVIC_NUMBER = 100

PHONE_NUMBER_LENGTH = 10

PROBABILITY_TO_HAVE_APP = 0.5


class PersonAttribute(IntEnum):
    """
    Class enum for the attribute of a Person Node
    """
    NAME = 0
    SURNAME = 1
    AGE = 2
    MAIL = 3
    NUMBER = 4
    APP = 5
    # And so on...

    @classmethod
    def numberOfAttribute(cls):
        numAttribute = 0
        for _ in PersonAttribute:
            numAttribute += 1
        return numAttribute


class LocationAttribute(IntEnum):
    """
    Class enum for the attribute of a Location
    """
    TYPE = 0
    NAME = 1
    ADDRESS = 2
    CIVIC_NUMBER = 3
    CAP = 4
    CITY = 5
    PROVINCE = 6
    # and so on ...

    @classmethod
    def numberOfAttribute(cls):
        numAttribute = 0
        for _ in LocationAttribute:
            numAttribute += 1
        return numAttribute


class HouseAttribute(IntEnum):
    """
    Class enum for the creation of the House
    """
    ADDRESS = 0
    CAP = 1
    CITY = 2
    PROVINCE = 3

    @classmethod
    def numberOfAttribute(cls):
        numAttribute = 0
        for _ in HouseAttribute:
            numAttribute += 1
        return numAttribute


def openConnection():
    """
    Method that starts a connection with the database
    :return: the driver for the connection
    """
    connection = nj.GraphDatabase.driver(
        "bolt://18.207.228.214:7687",
        auth=nj.basic_auth("neo4j", "can-alcoholic-writing"))
    return connection


def closeConnection(connection):
    """
    Method that close a connection
    :param connection: is the connection to terminate
    """
    connection.close()


def createPerson(tx, name, age):
    """
    Method that create a new Person node
    :param tx: is the transaction
    :param name: it the name of the new node
    :param age: is the age of the new node
    :return: nothing
    """
    query = (
        "CREATE (p:Person {name: $name , age: $age})"
    )

    tx.run(query, name=name, age=age)


def createFriendOf(tx, name, friend):
    """
    Method that create a friend
    :param tx: it the transaction
    :param name: it the Person that knows a new other Person
    :param friend: is the new Friend of name
    :return: nothing
    """
    query = (
        "MATCH (a:Person) WHERE a.name = $name "
        "CREATE (a)-[:KNOWS]->(:Person {name: $friend})"
    )

    tx.run(query, name=name, friend=friend)


def deleteAll(tx):
    """
    Method that deletes every node and every link
    :param tx: is the transaction
    :return: nothing
    """
    query = (
        "MATCH (n) "
        "DETACH DELETE n"
    )

    tx.run(query)


def deletePerson(tx, name):
    """
    Method that deleted a specific person
    :param tx: is the transaction
    :param name: is the specific node to delete
    :return: nothing
    """
    query = (
        "MATCH (n:Person {name: $name})"
        "DETACH DELETE n"
    )

    tx.run(query, name=name)


def deleteRelationship(tx, relationship, name=None):
    """
    Method that deletes relationships
    :param tx: is the transaction
    :param relationship: is the relationship to delete
    :param name: is None delete all the relationship, delete just the relationship
                    from nodes with name equal to name
    :return: nothing
    """
    if name is None:
        query = (
            "MATCH ()-[r:$relationship]->() "
            "DELETE r"
        )
        tx.run(query, relationship=relationship)
    else:
        query = (
            "MATCH (n:Person {name: $name})-[r:$relationship]->()"
            "DELETE r"
        )
        tx.run(query, name=name, relationship=relationship)


def countAll(tx):
    """
    Method that count the number of Nodes
    :param tx: is the transaction
    :return: the number of Nodes
    """
    query = (
        "MATCH (n) "
        "RETURN COUNT(n) AS count "
        "LIMIT $limit"
    )

    result = tx.run(query, limit=10)
    return [record["count"] for record in result]


def findAll(tx):
    """
    Methods that fins the whole structure of the database
    :param tx: is the transaction
    :return: the whole structure
    """
    query = (
        "MATCH (n1)-[r]->(n2) "
        "RETURN n1 AS node1 , r AS relationship , n2 AS node2 "
    )

    result = tx.run(query)
    return [(record["node1"], record["relationship"], record["node2"]) for record in result]


def findAllPerson(tx):
    """
    Method that finds all the nodes in the data base
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
    Method that finds all the nodes in the data base
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
    Method that finds all the nodes in the data base
    :param tx: is the transaction
    :return: a list of nodes
    """
    query = (
        "MATCH (l:Location) "
        "RETURN l , ID(l);"
    )
    results = tx.run(query).data()
    return results


def findAllRelationships(tx):
    """
    Method that finds all the relationships in the data base
    :param tx: is the transaction
    :return: a list of relationships
    """
    query = (
        "MATCH (n1)-[r]-(n2) "
        "RETURN ID(n1) , r , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def getFriendsOf(tx, name):
    """
    Method that retrieves the friends of a specified Person
    :param tx: is the transaction
    :param name: is the Person we want the friends
    :return: a list of friends
    """
    friends = []

    result = tx.run(
        "MATCH (a:Person)-[:KNOWS]->(f) "
        "WHERE a.name = $name "
        "RETURN f.name AS friend",
        name=name
    )

    for record in result:
        friends.append(record["friend"])
    return friends


def findPerson(tx, name, age=None):
    """
    Method that finds a Person given it's name and ,optionally, his age
    :param tx: is the transaction
    :param name: is the name to find
    :param age: is the age
    :return: all the nodes that have attribute equal to name (and age)
    """
    if age is None:
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, name=name)
        return [record["name"] for record in result]
    else:
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $name ANS p.age = $age"
            "RETURN p.name AS name , p.age AS age"
        )
        result = tx.run(query, name=name, age=age)
        return [(record["name"], record["age"]) for record in result]


def exampleFunction():
    # Open a connection
    driver = openConnection()

    # Create a node Person
    # createPerson("Matteo" , 22)

    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    with driver.session() as session:
        session.write_transaction(createPerson, "Matteo", 22)

    with driver.session() as session:
        session.write_transaction(createFriendOf, "Matteo", "Marco")

    # Verify the node is been added
    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    # Get the friends of Matteo
    with driver.session() as session:
        numberOfNodes = session.read_transaction(getFriendsOf, "Matteo")
    print("Friends of Matteo are: " + str(numberOfNodes))

    # Get the whole structure
    with driver.session() as session:
        graph = session.read_transaction(findAll)
    print("The structure is: ")
    print(graph)

    #with driver.session() as session:
    #    session.write_transaction(randomMatch)

    # Get the whole structure
    with driver.session() as session:
        graph = session.read_transaction(findAll)
    print("The structure is: ")
    print(graph)

    # Delete all the nodes
    with driver.session() as session:
        session.write_transaction(deleteAll)

    # Verify the all the nodes are been removed
    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    # Close the connection
    closeConnection(driver)


def readHours():
    """
    Method that reads the possible hours from a file
    :return: a list containing the hours
    """
    hoursRead = []
    with open("Files/Hours.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            if line is "\n":
                continue
            hoursRead.append(line.rstrip('\n'))
    f.close()
    return hoursRead


def readNames():
    """
    Method that reads the possible names from a file
    :return: a list containing the names
    """
    namesRead = []
    with open("Files/Names.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            if line is "\n":
                continue
            namesRead.append(line.rstrip('\n'))
    f.close()
    return namesRead


def readSurnames():
    """
    Method that reads the possible surnames from a file
    :return: a list containing the surnames
    """
    surnamesRead = []
    with open("Files/Surnames.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            if line is "\n":
                continue
            surnamesRead.append(line.rstrip('\n'))
    f.close()
    return surnamesRead


def readLocations():
    """
    Method that reads the possible locations from a file
    :return: a list containing the locations
    """
    locationsRead = []

    # Parallel reading from address_file and locations_file
    with open("Files/PublicPlaces.txt", 'r', encoding='utf8') as locations_file, \
            open("Files/Addresses.txt", 'r', encoding='utf8') as addresses_file:
        for (location_line, address_line) in zip(locations_file, addresses_file):
            if location_line is "\n" and address_line is "\n":
                continue
            locationDetails = location_line.split(",")
            addressDetails = address_line.split(",")
            details = []
            for locationDetail in locationDetails:
                details.append(locationDetail.lstrip().rstrip().rstrip('\n'))
            for addressDetail in addressDetails:
                details.append(addressDetail.lstrip().rstrip('\n'))
            locationsRead.append(details)

    locations_file.close()
    addresses_file.close()
    return locationsRead


def readHouseAddresses():
    """
    Method that reads different addresses from a file
    :return: a list of addresses
    """
    addressesRead = []
    with open("Files/HouseAddresses.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            if line is "\n":
                continue
            details = line.split(",")
            address = []
            for detail in details:
                address.append(detail)
            addressesRead.append(address)
    f.close()
    return addressesRead


def readDates():
    """
    Method that reads dates from a file
    :return: a list of dates
    """
    datesList = []
    with open("Files/Dates.txt"  , 'r', encoding = 'utf8') as f:
        for line in f:
            if line is "\n":
                continue
            datesList.append(line.rstrip('\n'))
    f.close()
    return datesList


def createFamilies(namesList , surnamesList):
    """
    Method that initialize a list of all the family relationships
    :return: a list of list (a list of family)
    """
    familiesList = []
    surnameIndex = 0
    for _ in range(0 , NUMBER_OF_FAMILY):
        # Choose a size for the family
        numberOfMembers = randint(1 , MAX_NUMBER_OF_FAMILY_MEMBER)
        # Family will contain the name in pos 0 and the surname in pos 1
        familyEl = [None] * numberOfMembers
        casualFamily = False
        for j in range(0 , len(familyEl)):
            familyEl[j] = [None] * PersonAttribute.numberOfAttribute()
            # Append a random name
            name = str(namesList[randint(0 , len(names) - 1)])
            familyEl[j][int(PersonAttribute.NAME)] = name
            # Append the next surname
            surname = str(surnamesList[surnameIndex])
            familyEl[j][int(PersonAttribute.SURNAME)] = surname
            # Append a random age
            if j == 0:
                age = randint(18 , 99)
            else:
                age = randint(1 , 99)
            familyEl[j][int(PersonAttribute.AGE)] = age
            # Append the mail
            mail = name + "." + surname + str(age) + "@immunoPoli.it"
            familyEl[j][int(PersonAttribute.MAIL)] = mail
            # Append the phone number
            number = 0
            for i in range(1 , PHONE_NUMBER_LENGTH + 1):
                number += i * randint(0 , 9)
            familyEl[j][int(PersonAttribute.NUMBER)] = number
            # Append the app attribute
            if random() < PROBABILITY_TO_HAVE_APP:
                app = "True"
            else:
                app = "False"
            familyEl[j][int(PersonAttribute.APP)] = app

            # In every family there will be at least 2 surnames
            # In case of friends living together there is a probability of 30% to have more than 2 surnames in a family
            if j == 0 and randint(0 , 100) < 30:  # Family of not familiar
                casualFamily = True
            if j == 0 or (numberOfMembers > 2 and casualFamily):
                surnameIndex += 1
                if surnameIndex >= len(surnames):
                    surnameIndex = 0
        familiesList.append(familyEl)
        surnameIndex += 1
        if surnameIndex >= len(surnames):
            surnameIndex = 0
    return familiesList


def createNodesFamily(familiesList , houseAddressesList):
    """
    Method that append some command to the general query
    :param houseAddressesList: is the list containing addresses ofr houses
    :param familiesList: is the list of families
    :return: nothing
    """
    creationQuery = []       # Query that will contains all the queries for the node creation
    relationshipsQuery = []  # Query that will contains all the queries for the relationship creation
    for familyEl in familiesList:
        for memberEl in familyEl:
            currentQuery = (
                "CREATE (p:Person {name: \"" + str(memberEl[int(PersonAttribute.NAME)]) + "\" , surname: \"" +
                str(memberEl[int(PersonAttribute.SURNAME)]) + "\" , age: \"" + str(memberEl[int(PersonAttribute.AGE)]) +
                "\" , mail: \"" + str(memberEl[int(PersonAttribute.MAIL)]) + "\" , number: \"" +
                str(memberEl[int(PersonAttribute.NUMBER)]) + "\" , app: \"" +
                str(memberEl[int(PersonAttribute.APP)]) + "\"}); "
            )
            creationQuery.append(currentQuery)
        # Create the name of the house
        memberFamily = familyEl[0]
        familyName = memberFamily[PersonAttribute.NAME] + " " + memberFamily[PersonAttribute.SURNAME] + " house"
        addressIndex = randint(0 , len(houseAddressesList) - 1)
        address = houseAddressesList[addressIndex]
        civicNumber = randint(0 , MAX_CIVIC_NUMBER)
        currentQuery = (
            "CREATE (h:House {name: \"" + str(familyName) + "\" , address: \"" + str(address[HouseAttribute.ADDRESS]) +
            "\",  civic_number: \"" + str(civicNumber) + "\" , CAP: \"" + str(address[HouseAttribute.CAP]) +
            "\", city:  \"" + str(address[HouseAttribute.CITY]) + "\" , province: \""
            + str(address[HouseAttribute.PROVINCE]) + "\"}); "
        )
        creationQuery.append(currentQuery)

        # Create the LIVE relationships
        for memberEl in familyEl:
            currentQuery = (
                "MATCH (p:Person) , (h:House) "
                "WHERE p.name = \"" + str(memberEl[int(PersonAttribute.NAME)]) +
                "\" AND p.surname = \"" + str(memberEl[int(PersonAttribute.SURNAME)]) + "\" AND p.age= \"" +
                str(memberEl[int(PersonAttribute.AGE)]) + "\" AND h.name = \"" + str(familyName) +
                "\" AND h.address = \"" + str(address[HouseAttribute.ADDRESS]) + "\" AND h.civic_number = \"" +
                str(civicNumber) + "\" AND h.CAP = \"" + str(address[HouseAttribute.CAP]) +
                "\" AND h.city = \"" + str(address[HouseAttribute.CITY]) + "\" AND h.province = \"" +
                str(address[HouseAttribute.PROVINCE]) + "\" "
                "CREATE (p)-[:LIVE]->(h);"
            )
            relationshipsQuery.append(currentQuery)

    return creationQuery , relationshipsQuery


def createNodeLocations(locationsList):
    """
    Method that creates the query for the creation of the public places
    :param locationsList: is a list containing all the locations
    :return: a query
    """
    locationsQuery = []
    for locationEl in locationsList:
        currentQuery = (
            "CREATE (l:Location {name: \"" + str(locationEl[int(LocationAttribute.NAME)]) + "\" , type: \"" +
            str(locationEl[int(LocationAttribute.TYPE)]) + "\" , address: \"" +
            str(locationEl[int(LocationAttribute.ADDRESS)]) + "\" , civic_number: \"" +
            str(locationEl[int(LocationAttribute.CIVIC_NUMBER)]) + "\", CAP: \"" +
            str(locationEl[int(LocationAttribute.CAP)]) + "\" , city: \"" +
            str(locationEl[int(LocationAttribute.CITY)]) + "\" , province: \"" +
            str(locationEl[int(LocationAttribute.PROVINCE)]) + "\"}); "
        )
        locationsQuery.append(currentQuery)
    return locationsQuery


def createRelationshipsAppContact(d , pIds , datesList , hoursList):
    """
    Method that creates random relationship
    :param hoursList: list of possible hours
    :param datesList: list of possible dates
    :param d: is the connection (driver)
    :param pIds: list of Person ids
    :return: nothing
    """
    # Create the number of app contact for the day
    numOfContact = randint(1 , MAX_NUMBER_OF_CONTACT_PER_DAY)

    for _ in range(0 , numOfContact):
        # Choose two random people
        randomIndex = randint(0 , len(pIds) - 1)
        pId1 = pIds[randomIndex]
        randomIndex = randint(0 , len(pIds) - 1)
        pId2 = pIds[randomIndex]
        # Choose the hour/date
        dateIndex = randint(0 , len(datesList) - 1)
        date = datesList[dateIndex]
        hourIndex = randint(0 , len(hoursList) - 1)
        hour = hoursList[hourIndex]
        # Verify if it's the same node
        if pId1 == pId2:
            continue
        query = (
            "MATCH (p1:Person) , (p2:Person) "
            "WHERE ID(p1) = $pId1 AND ID(p2) = $pId2 "
            "MERGE (p1)-[:APP_CONTACT { hour: $hour , date: $date}]-(p2)"
        )
        # Execute the query
        with d.session() as s:
            s.write_transaction(createContact , query , pId1 , pId2 , hour , date)


def createRelationshipsVisit(d , pIds , lIds , datesList , hoursList):
    """
    Method that creates VISIT relationships
    :param hoursList: list of possible hours
    :param datesList: list of possible dates
    :param d: is the connection (driver)
    :param pIds: is a list of Person ids
    :param lIds: is a list of Location ids
    :return: nothing
    """
    # Choose how many new visit relationships
    numberOfVisits = randint(1  , MAX_NUMBER_OF_VISIT_PER_DAY)

    for _ in range(0 , numberOfVisits):
        lIndex = randint(0 , len(lIds) - 1)
        locationId = lIds[lIndex]
        pIndex = randint(0 , len(pIds) - 1)
        personId = pIds[pIndex]
        # Choose the hour/date
        dateIndex = randint(0 , len(datesList) - 1)
        date = datesList[dateIndex]
        startHourIndex = randint(0 , len(hoursList) - 1)
        if startHourIndex == len(hoursList) - 1:
            startHourIndex = len(hoursList) - 2
        startHour = hoursList[startHourIndex]
        endHourIndex = randint(startHourIndex , len(hoursList) - 1)
        endHour = hoursList[endHourIndex]
        # For the future: here check if in case of more than 1 relationship already present it has a different hour/date
        # Maybe this can be avoided with MERGE instead of CREATE
        query = (
            "MATCH (p:Person) , (l:Location) "
            "WHERE ID(p) = $personId AND ID(l) = $locationId "
            "MERGE (p)-[:VISIT {date: $date , start_hour: $startHour , end_hour: $endHour}]->(l); "
        )
        # Execute the query
        with d.session() as s:
            s.write_transaction(createVisit , query , personId , locationId , date , startHour , endHour)


def createVisit(tx , query , personId , locationId , date , startHour , endHour):
    """
    Method that executes the query to create a VISIT relationship
    :param endHour: ending time of the visit
    :param startHour: starting time of the visit
    :param date: date of the visit
    :param tx: is the transaction
    :param query: is the query to create a visit relationship
    :param personId: is the id of the Person
    :param locationId: is the id of the Location
    :return: nothing
    """
    tx.run(query , personId = personId , locationId = locationId , date = date , startHour = startHour ,
           endHour = endHour)


def createContact(tx , query , pId1 , pId2 , hour , date):
    """
    Method that executes the query to create a CONTACT_APP relationship
    :param date: the date of the contact
    :param hour: the hour of the contact
    :param tx: is the transaction
    :param query: is the query to perform
    :param pId1: is the id of the first Person
    :param pId2: is the id of the second Person
    :return: nothing
    """
    tx.run(query , pId1 = pId1 , pId2 = pId2 , hour = hour , date = date)


def getPersonIds(withApp = False):
    """
    Method that retrieves all the ids of Person Node
    :param withApp: if True, retrieve the id of person with app = True
    :return: a list of integer corresponding to the person ids
    """
    with driver.session() as s:
        ids = s.write_transaction(getPersonId , withApp)
    print(ids)

    pIds = []
    for idEl in ids:
        pIds.append(idEl["ID(p)"])
    print(pIds)

    return pIds


def getPersonId(tx , withApp):
    """
    Method that retrieves the ids of Person in the data base
    :param tx: is the transaction
    :param withApp: if True, retrieve the id of person with app = True
    :return: a list of ids
    """
    if not withApp:
        query = (
            "MATCH (p:Person) "
            "RETURN ID(p);"
        )
    else:
        query = (
            "MATCH (p:Person) "
            "WHERE p.app = \"True\" "
            "RETURN ID(p);"
        )

    idsList = tx.run(query).data()
    return idsList


def getLocationsIds():
    """
    Method that retrieves all the ids of Location Node
    :return: a list of integer corresponding to the location ids
    """
    with driver.session() as s:
        ids = s.write_transaction(getLocationsId)
    print(ids)

    lIds = []
    for idEl in ids:
        lIds.append(idEl["ID(l)"])
    print(lIds)

    return lIds


def getLocationsId(tx):
    """
    Method that retrieve a list of location ids
    :param tx: is the transaction
    :return: a list of ids
    """
    query = (
        "MATCH (l:Location)"
        "RETURN ID(l)"
    )

    idsList = tx.run(query).data()
    return idsList


def runQuery(tx , query , isReturn = False):
    """
    Method that runs a generic query
    :param tx: is the transaction
    :param query: is the query to perform
    :param isReturn: if True return the results, return nothing otherwise
    """
    result = tx.run(query)

    if isReturn:
        return result


def runQueryWrite(d , queryList):
    """
    Method that run a generic query
    :param d: is the connection to the database (driver)
    :param queryList: is the query to run -> it's already completed
    :return: nothing
    """
    for query in queryList:
        print("Executing query: ")
        print(query)
        with d.session() as s:
            s.write_transaction(runQuery , query)


def runQueryRead(d , query):
    """
    Method that run a generic query
    :param d: is the connection to the database
    :param query: is the query to run -> it's already completed
    :return: nothing
    """
    with d.session() as s:
        results = s.read_transaction(runQuery , query , True)
    return results


def print_database():
    """
    Method that prints the whole database inside a predefined
    browser tab.
    """
    NEO4J_CREDS = {'uri': "bolt://18.207.228.214:7687",
                   'auth': ("neo4j", "can-alcoholic-writing")}
    graphistry.register(bolt=NEO4J_CREDS, api=3, protocol="https", server="hub.graphistry.com",
                        username="PieroRendina", password="acmilan01")
    graphistry.cypher("MATCH (a)-[r]->(b) RETURN *").plot()


if __name__ == '__main__':
    # Read hours from the file
    hours = readHours()
    print("Hours read")
    # Read names from the file
    names = readNames()
    print("Names read")
    # Read surnames from the file
    surnames = readSurnames()
    print("Surnames read")
    # Read locations
    locations = readLocations()
    print("Locations read")
    # Read house addresses
    houseAddresses = readHouseAddresses()
    print("House addresses read")
    # Read dates
    dates = readDates()
    print("Dates read")

    """
    print("Hours are: " + str(hours))
    print("Locations are: " + str(locations))
    print("Number of hours is: " + str(len(hours)))
    print("Number of names is: " + str(len(names)))
    print("Number of surnames is: " + str(len(surnames)))
    print("Number of locations is: " + str(len(locations)))
    print("Number of dates is: " + str(len(dates)))
    """

    # Create the family list
    families = createFamilies(names , surnames)
    print("Families created")

    """
    i = 0
    for family in families:
        print("Family number " + str(i))
        for member in family:
            print(member[int(PersonAttribute.NAME)] + " " + member[int(PersonAttribute.SURNAME)])
        i += 1
    """

    # Query is an attribute that will contain the whole query to instantiate the database
    generalQuery = []

    # Generate all the Person Nodes and the family relationships
    cQuery , rQuery = createNodesFamily(families , houseAddresses)
    # Generate the locations node
    lQuery = createNodeLocations(locations)
    for subQuery in cQuery:
        generalQuery.append(subQuery)
    for subQuery in lQuery:
        generalQuery.append(subQuery)
    for subQuery in rQuery:
        generalQuery.append(subQuery)

    print("The final query is: ")
    print(generalQuery)

    # Open the connection
    driver = openConnection()

    # Delete the nodes already present
    with driver.session() as session:
        numberOfNodes = session.write_transaction(deleteAll)

    # Generate the structure performing the families creation
    runQueryWrite(driver , generalQuery)

    # Generate random contacts with app tracing
    # Take Person ids of people with app attribute equal to True)
    personIds = getPersonIds(True)
    # Generate the relationships
    createRelationshipsAppContact(driver , personIds , dates , hours)

    # Generate random visits
    # Take Location ids
    locationIds = getLocationsIds()
    # Generate the relationship
    createRelationshipsVisit(driver , personIds , locationIds , dates , hours)

    # Verify the nodes are been created
    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    # Get the whole structure
    with driver.session() as session:
        graph = session.read_transaction(findAll)
    print("The structure is: ")
    print_database()
