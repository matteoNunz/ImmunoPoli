"""
Date: 28/10/2021
First sketch for a generator of data base structure for Neo4J

Problem: there is a problem where name/surname are made by 2 words
"""

import neo4j as nj
from random import randint
from enum import IntEnum
import pandas as pd

MAX_NUMBER_OF_FAMILY_MEMBER = 5
NUMBER_OF_FAMILY = 5


class PersonAttribute(IntEnum):
    """
    class enum for the attribute of a Person Node
    """
    NAME = 0
    SURNAME = 1
    # And so on...

    @classmethod
    def numberOfAttribute(cls):
        numAttribute = 0
        for attribute in PersonAttribute:
            numAttribute += 1
        return numAttribute


def openConnection():
    """
    Method that starts a connection with the database
    :return: the driver for the connection
    """
    connection = nj.GraphDatabase.driver(
        "bolt://18.204.42.164:7687",
        auth=nj.basic_auth("neo4j", "oxygen-wishes-knives"))
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


def randomMatch(tx):
    """
    Method that creates random relationship
    :param tx: is the transaction
    :return: nothing
    """
    query = (
        "MATCH (p1:Person) , (p2:Person) "
        "WITH p1 , p2 "
        "WHERE rand() < 1 AND p1 <> p2"
        "MERGE (p1)-[:KILL]->(p2)"
    )

    tx.run(query)


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

    with driver.session() as session:
        session.write_transaction(randomMatch)

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
            surnamesRead.append(line.rstrip('\n'))
    f.close()
    return surnamesRead


def readLocations():
    """
    Method that reads the possible locations from a file
    :return: a list containing the locations
    """
    locationsRead = []
    with open("Files/PublicPlaces.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            locationDetails = line.split(",")
            details = []
            for locationDetail in locationDetails:
                details.append(locationDetail.rstrip('\n'))
            locationsRead.append(details)
    f.close()
    return locationsRead


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
        print("Number extracted is: " + str(numberOfMembers))
        # Family will contain the name in pos 0 and the surname in pos 1
        familyEl = [None] * numberOfMembers
        casualFamily = False
        for j in range(0 , len(familyEl)):
            familyEl[j] = [None] * PersonAttribute.numberOfAttribute()
            # Append a random name
            familyEl[j][int(PersonAttribute.NAME)] = str(namesList[randint(0 , len(names) - 1)])
            # Append the next surname
            familyEl[j][int(PersonAttribute.SURNAME)] = str(surnamesList[surnameIndex])
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


def createNodesFamily(familiesList):
    """
    Method that append some command to the general query
    :param familiesList: is the list of families
    :return: nothing
    """
    creationQuery = []       # Query that will contains all the queries for the node creation
    relationshipsQuery = []  # Query that will contains all the queries for the relationship creation
    for familyEl in familiesList:
        for memberEl in familyEl:
            currentQuery = (
                "CREATE (p:Person {name: '" + str(memberEl[int(PersonAttribute.NAME)]) + "' , surname: '" +
                str(memberEl[int(PersonAttribute.SURNAME)]) + "'}); "
            )
            creationQuery.append(currentQuery)
        # Create the name of the house
        memberFamily = familyEl[0]
        familyName = memberFamily[PersonAttribute.NAME] + " " + memberFamily[PersonAttribute.SURNAME] + " house"
        currentQuery = (
            "CREATE (l:Location {name: '" + str(familyName) + "'}); "
        )
        creationQuery.append(currentQuery)

        # Create the LIVE relationships
        for memberEl in familyEl:
            currentQuery = (
                "MATCH (p:Person) , (l:Location) "
                "WHERE p.name = '" + str(memberEl[int(PersonAttribute.NAME)]) +
                "' AND p.surname = '" + str(memberEl[int(PersonAttribute.SURNAME)]) + "' AND l.name = '"
                + str(familyName) + "' "
                "CREATE (p)-[:LIVE]->(l);"
            )
            relationshipsQuery.append(currentQuery)

    return creationQuery , relationshipsQuery


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


def runQueryWrite(driver , queryList):
    """
    Method that run a generic query
    :param driver: is the connection to the database
    :param query: is the query to run -> it's already completed
    :return: nothing
    """
    for query in queryList:
        print("Executing query: ")
        print(query)
        print("Query length is: " + str(len(query)))  # toDo: that's the problem
        with driver.session() as s:
            s.write_transaction(runQuery , query)


def runQueryRead(driver , query):
    """
    Method that run a generic query
    :param driver: is the connection to the database
    :param query: is the query to run -> it's already completed
    :return: nothing
    """
    with driver.session() as session:
        results = session.read_transaction(runQuery , query , True)
    return results


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

    """
    print("Hours are: " + str(hours))
    print("Locations are: " + str(locations))
    print("Number of hours is: " + str(len(hours)))
    print("Number of names is: " + str(len(names)))
    print("Number of surnames is: " + str(len(surnames)))
    print("Number of locations is: " + str(len(locations)))
    """

    # Create the family list
    families = createFamilies(names , surnames)
    print("Families created")
    print("Families are: ")

    i = 0
    for family in families:
        print("Family number " + str(i))
        for member in family:
            print(member[int(PersonAttribute.NAME)] + " " + member[int(PersonAttribute.SURNAME)])
        i += 1

    # query is an attribute that will contain the whole query to instantiate the database
    generalQuery = []

    # Generate all the Person Nodes and the family relationships
    cQuery , rQuery = createNodesFamily(families)
    for subQuery in cQuery:
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

    # Verify the nodes are been created
    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    # Get the whole structure
    with driver.session() as session:
        graph = session.read_transaction(findAll)
    print("The structure is: ")
    print(graph)
