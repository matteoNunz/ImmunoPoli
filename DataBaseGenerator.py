"""
Date: 28/10/2021
Neo4J generator for ImmunoPoli project
"""

import neo4j as nj
import PlotDBStructure as ps

from random import randint, random
from enum import IntEnum
import datetime

MAX_NUMBER_OF_FAMILY_MEMBER = 5
NUMBER_OF_FAMILY = 50

MAX_NUMBER_OF_CONTACT_PER_DAY = 50  # For new contact relationships

MAX_NUMBER_OF_VISIT_PER_DAY = 300  # For new visit relationships

MAX_CIVIC_NUMBER = 100

PHONE_NUMBER_LENGTH = 10

PROBABILITY_TO_HAVE_APP = 0.5
PROBABILITY_TO_BE_POSITIVE = 0.5
PROBABILITY_TO_BE_TESTED_AFTER_INFECTED = 0.8

MAX_NUMBER_OF_VACCINE_PER_DAY = 50  # For new get vaccinated relationships

MAX_NUMBER_OF_TEST_PER_DAY = 50  # For new make test relationships


# BOLT = "bolt://localhost:7687"
# PASSWORD = "991437"

"""BOLT = "bolt://3.91.213.132:7687"
PASSWORD = "blocks-company-calendar"""
USER = "neo4j"
PASSWORD = "cJhfqi7RhIHR4I8ocQtc5pFPSEhIHDVJBCps3ULNzbA"
URI = "neo4j+s://057f4a80.databases.neo4j.io"


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


class VaccineAttribute(IntEnum):
    """
    Class enum for the attribute of a Location
    """
    NAME = 0
    PRODUCER = 1

    # and so on ...

    @classmethod
    def numberOfAttribute(cls):
        numAttribute = 0
        for _ in VaccineAttribute:
            numAttribute += 1
        return numAttribute


def openConnection():
    """
    Method that starts a connection with the database
    :return: the driver for the connection
    """
    connection = nj.GraphDatabase.driver(
        uri=URI, auth=nj.basic_auth(USER, PASSWORD))
    return connection


def closeConnection(connection):
    """
    Method that close a connection
    :param connection: is the connection to terminate
    """
    connection.close()


def readNames():
    """
    Method that reads the possible names from a file
    :return: a list containing the names
    """
    namesRead = []
    with open("Files/Names.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            namesRead.append(line.rstrip('\n').rstrip().lstrip())
    f.close()
    return namesRead


def readSurnames():
    """
    Method that reads the possible surnames from a file
    :return: a list containing the surnames
    """
    surnamesRead = []
    with open("Files/Surnames.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            surnamesRead.append(line.rstrip('\n').rstrip().lstrip())
    f.close()
    return surnamesRead


def readLocations():
    """
    Method that reads the possible locations from a file
    :return: a list containing the locations
    """
    locationsRead = []

    # Parallel reading from address_file and locations_file
    with open("Files/PublicPlaces.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            details = line.split(",")
            address = []
            for detail in details:
                address.append(detail.rstrip('\n').rstrip().lstrip())
            locationsRead.append(address)
        f.close()
    return locationsRead


def readHouseAddresses():
    """
    Method that reads different addresses from a file
    :return: a list of addresses
    """
    addressesRead = []
    with open("Files/HouseAddresses.txt" , 'r', encoding = 'utf8') as f:
        for line in f:
            if line == "\n":
                continue
            details = line.split(",")
            address = []
            for detail in details:
                address.append(detail.rstrip('\n').rstrip().lstrip())
            addressesRead.append(address)
    f.close()
    return addressesRead


def readVaccines():
    """
    Method that reads the possible vaccines from a file
    :return: a list containing the vaccines
    """
    vaccinesRead = []

    with open("Files/Vaccines.txt", 'r', encoding='utf8') as vaccine_file:
        for vaccine_lines in vaccine_file:
            vaccineDetails = vaccine_lines.split(",")
            details = []
            for vaccineDetail in vaccineDetails:
                details.append(vaccineDetail.lstrip().rstrip().rstrip('\n'))
            vaccinesRead.append(details)

    vaccine_file.close()
    return vaccinesRead


def readTests():
    """
    Method that reads the possible locations from a file
    :return: a list containing the locations
    """
    testsList = []

    with open("Files/Tests.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            testsList.append(line.rstrip('\n').rstrip().lstrip())
    f.close()
    return testsList


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
        "MATCH (n1:Person)-[r:GET]->(n2:Vaccine) "
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
        "MATCH (n1:Person)-[r:MAKE]->(n2:Test) "
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
        "MATCH (n1:Person)-[r:INFECTED]->(n2:Person) "
        "RETURN ID(n1) , r , r.date , r.name , ID(n2);"
    )
    results = tx.run(query).data()
    return results


def createFamilies(namesList, surnamesList):
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
            mail = name.lower() + "." + surname.lower() + str(age) + "@immunoPoli.it"

            familyEl[j][int(PersonAttribute.MAIL)] = mail
            # Append the phone number
            number = 0
            for i in range(0 , PHONE_NUMBER_LENGTH):
                number += randint(0 , 9) * 10 ** i
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


def createNodeVaccines(vaccinesList):
    """
    Method that creates the query for the creation of the vaccines node
    :param vaccinesList: is a list containing all the vaccines
    :return: a query
    """
    vaccinesQuery = []
    for vaccineEl in vaccinesList:
        currentQuery = (
                "CREATE (v:Vaccine {name: \"" + str(vaccineEl[int(VaccineAttribute.NAME)]) + "\" , producer: \"" +
                str(vaccineEl[int(VaccineAttribute.PRODUCER)]) + "\"}); "
        )
        vaccinesQuery.append(currentQuery)
    return vaccinesQuery


def createNodeTests(testsList):
    """
    Method that creates the query for the creation of the tests
    :param testsList: is a list containing all the possible type of tests
    :return: a query
    """
    testsQuery = []
    for testEl in testsList:
        currentQuery = (
                "CREATE (t:Test {name: \"" + str(testEl) + "\"}); "
        )
        testsQuery.append(currentQuery)
    return testsQuery


def createRelationshipsAppContact(d , pIds):
    """
    Method that creates random relationship
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
        # Verify if it's the same node
        if pId1 == pId2:
            return
        date = datetime.date.today() - datetime.timedelta(days=randint(0, 9))
        date = date.strftime("%Y-%m-%d")
        h = randint(0, 23)
        minutes = randint(0, 59)
        if minutes < 10:
            minutes = "0" + str(minutes)
        hour = str(h) + ":" + str(minutes) + ":00"
        n = 0
        while (validateDate(d, date, pId1, hour) == False or validateDate(d, date, pId2, hour)==False) and n < 5:

            date = datetime.date.today() - datetime.timedelta(days=randint(0, 9))
            date = date.strftime("%Y-%m-%d")
            h = randint(0, 23)
            minutes = randint(0, 59)
            if minutes < 10:
                minutes = "0" + str(minutes)
            hour = str(h) + ":" + str(minutes) + ":00"
            n = n + 1
        if n == 5:
            return


        query = (
            "MATCH (p1:Person) , (p2:Person) "
            "WHERE ID(p1) = $pId1 AND ID(p2) = $pId2 "
            "MERGE (p1)-[:APP_CONTACT { hour: time($hour) , date: date($date)}]->(p2) "
            "MERGE (p1)<-[:APP_CONTACT { hour: time($hour) , date: date($date)}]-(p2)"
        )
        # Execute the query
        with d.session() as s:
            s.write_transaction(createContact , query , pId1 , pId2 , hour , date)


def createRelationshipsVisit(d , pIds , lIds):
    """
    Method that creates VISIT relationships
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

        date = datetime.date.today() - datetime.timedelta(days=randint(0, 7))
        date = date.strftime("%Y-%m-%d")
        h = randint(0, 22)
        minutes = randint(0, 59)
        if minutes < 10:
            minutes = "0" + str(minutes)
        startHour = str(h) + ":" + str(minutes)
        h = randint(h, 23)
        minutes = randint(0, 59)
        if minutes < 10:
            minutes = "0" + str(minutes)
        endHour = str(h) + ":" + str(minutes)
        n = 0
        while validateDate(d, date, personId, endHour) == False and n < 5:
            date = datetime.date.today() - datetime.timedelta(days=randint(0, 7))
            date = date.strftime("%Y-%m-%d")
            h = randint(0, 22)
            minutes = randint(0, 59)
            if minutes < 10:
                minutes = "0" + str(minutes)
            startHour = str(h) + ":" + str(minutes)
            h = randint(h, 23)
            minutes = randint(0, 59)
            if minutes < 10:
                minutes = "0" + str(minutes)
            endHour = str(h) + ":" + str(minutes)
            n = n + 1
        if n == 5:
            return
        # For the future: here check if in case of more than 1 relationship already present it has a different hour/date
        # Maybe this can be avoided with MERGE instead of CREATE
        query = (
            "MATCH (p:Person) , (l:Location) "
            "WHERE ID(p) = $personId AND ID(l) = $locationId "
            "MERGE (p)-[:VISIT {date: date($date) , start_hour: time($startHour) , end_hour: time($endHour)}]->(l); "
        )
        # Execute the query

        with d.session() as s:
            s.write_transaction(createVisit , query , personId , locationId , date , startHour , endHour)


def validateDate(d, date, personId, hour):
    """
       Method that validate the date,if the last test before the date is positive return false
       :param d: driver
       :param date: date to check
       :param personId: person to check
       :param hour: hour to check
       :return: true if it's valid
       """
    query = (
        "MATCH (p:Person)-[r:MAKE_TEST]->(:Test) "
        "WHERE ID(p) = $personId AND (date($date)>r.date OR(date($date)=r.date AND time($hour)>r.hour)) "
        "RETURN r.date as date,r.result as result,r.hour as hour "
        "ORDER BY date DESC "
        "LIMIT 1 ")
    # Execute the query

    with d.session() as s:
        precDates = s.read_transaction(checkDate, query, personId, date, hour)

    if precDates is None or len(precDates) == 0 or precDates[0]["result"] == "Negative":
        return True
    else:
        return False


def createRelationshipsGetVaccine(d, pIds, vIds):
    """
    Method that creates GET vaccine relationships
    :param d: is the connection (driver)
    :param pIds: is a list of Person ids
    :param vIds: is a list of Vaccine ids
    :return: nothing
    """
    # Choose how many new visit relationships
    numberOfVaccines = randint(0,MAX_NUMBER_OF_VACCINE_PER_DAY)

    for _ in range(0, numberOfVaccines):
        vIndex = randint(0, len(vIds) - 1)
        vaccineId = vIds[vIndex]
        pIndex = randint(0, len(pIds) - 1)
        personId = pIds[pIndex]
        date = datetime.date.today() - datetime.timedelta(days=randint(0, 60))
        country = "Italy"
        # For the future: maybe do a random country
        # Ask to  neo4j server how many vaccines the user did
        query = (
            "MATCH (p:Person)-[r]->(v:Vaccine) "
            "WHERE ID(p) = $personId AND type(r)='GET_VACCINE'"
            "RETURN count(p) as count,ID(v) as vaccineID,r.expirationDate as date"
        )
        with d.session() as s:
            datas = s.read_transaction(gettingNumberVaccines, query, personId)

        # if no vaccines do one, else make the second vaccine
        if len(datas) == 0:
            expDate = date + datetime.timedelta(days=28)
        else:
            if len(datas) == 1:
                string1 = datas[0]["date"].split("-")
                date = datetime.date(int(string1[0]), int(string1[1]), int(string1[2].split(",")[0]))
                expDate = date + datetime.timedelta(days=365)
                vaccineId = datas[0]["vaccineID"]
            else:
                return
        date = date.strftime("%Y-%m-%d")
        expDate = expDate.strftime("%Y-%m-%d,%H:%M")

        query = (
            "MATCH (p:Person) , (v:Vaccine) "
            "WHERE ID(p) = $personId AND ID(v) = $vaccineId "
            "MERGE (p)-[:GET{date:date($date),country:$country,expirationDate:$expDate}]->(v); "
        )

        # Execute the query
        with d.session() as s:
            s.write_transaction(createGettingVaccine, query, personId, vaccineId, date, country, expDate)


def createRelationshipsMakeTest(d, pIds, tIds):
    """
    Method that creates MAKE test relationships
    :param d: is the connection (driver)
    :param pIds: is a list of Person ids
    :param tIds: is a list of Test ids
    :return: nothing
    """
    # Choose how many new visit relationships
    numberOfTest = randint(0,MAX_NUMBER_OF_TEST_PER_DAY)

    for _ in range(0, numberOfTest):
        probability = random()
        tIndex = randint(0, len(tIds) - 1)
        testId = tIds[tIndex]
        pIndex = randint(0, len(pIds) - 1)
        personId = pIds[pIndex]
        date = datetime.date.today() - datetime.timedelta(days=randint(0, 9))
        h = randint(0, 23)
        minutes = randint(0, 59)
        if minutes < 10:
            minutes = "0" + str(minutes)
        string_date = date.strftime("%Y-%m-%d")
        hour = str(h) + ":" + str(minutes)

        if probability < PROBABILITY_TO_BE_POSITIVE:
            result = "Positive"
        else:
            result = "Negative"

        query = (
            "MATCH (p:Person) , (t:Test) "
            "WHERE ID(p) = $personId AND ID(t) = $testId "
            "MERGE (p)-[:MAKE_TEST{date:date($date) , hour: time($hour) ,result:$result}]->(t); "
        )

        # If negative, all infections have to be neglected
        if probability >= PROBABILITY_TO_BE_POSITIVE:
            # Check whether or not I have been infected by someone
            delete_possible_infection_command = (
                "MATCH ()-[i:INFECTED]->(p:Person)"
                "WHERE ID(p) = $personId AND (i.date < date($date) OR "
                "i.date = date($date) AND i.hour < time($hour))"
                "DELETE i"
            )
            with d.session() as s:
                s.write_transaction(delete_possible_infection, delete_possible_infection_command, personId, string_date,
                                    hour)
        # Positive, create possible infections
        else:
            """I'm now passing the date of the test and we have to check up to 7 days"""
            # --- maybe we should change 7
            createRelationshipsInfect(personId, date, 7)
        # Execute the query
        with d.session() as s:
            s.write_transaction(createMakingTest, query, personId, testId, string_date,hour, result)


def delete_possible_infection(tx, command, personId, date, hour):
    """
    Method
    :param command: delete infection command to be performed
    :param personId: person whose infection is deleted
    :param date: date of the test
    :param hour: hour of the test
    """
    tx.run(command, personId = personId, date = date, hour = hour)


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


def createGettingVaccine(tx, query, personId, vaccineId, date, country, expDate):
    """
    Method that executes the query to create a VISIT relationship
    :param tx: is the transaction
    :param query: is the query to create a visit relationship
    :param personId: is the id of the Person
    :param vaccineId: is the id of the Vaccine
    :param date: date of the vaccine
    :param country: country
    :param expDate: expiration date of the vaccine
    :return: nothing
    """
    tx.run(query, personId=personId, vaccineId=vaccineId, date=date, country=country, expDate=expDate)


def gettingNumberVaccines(tx, query, personId):
    """
    Method that executes the query to create a GET vaccinated relationship
    :param tx: is the transaction
    :param query: is the query to create a visit relationship
    :param personId: is the id of the Person
    :return:  a list of the vaccines already administered to the Person
    """
    return tx.run(query, personId=personId).data()


def createMakingTest(tx, query, personId, testId, date, hour , result):
    """
    Method that executes the query to create a VISIT relationship
    :param tx: is the transaction
    :param query: is the query to create a visit relationship
    :param personId: is the id of the Person
    :param testId: is the id of the Test
    :param date: date of the vaccine
    :param hour: hour of the test
    :param result: result of the test
    :return: nothing
    """
    tx.run(query, personId=personId, testId=testId, date=date, hour=hour , result=result)


def findAllPositivePerson():
    """
    Method that finds all the positive person
    :return: a list of positive ids
    """
    query = (
        "MATCH (p:Person)-[r:MAKE]->(t:Test) "
        "WHERE r.result = \"Positive\" "
        "RETURN DISTINCT ID(p);"
    )

    positiveIdsFounds = runQueryRead(driver, query)
    return positiveIdsFounds


def checkDate(tx, query, personId, date, hour):
    """
    Method that executes the query to return the last test before the date
    :param date: hypothetical date of the visit
    :param tx: is the transaction
    :param query: is the query to get the test
    :return: date of the precedent test
    """
    return tx.run(query, personId=personId, date=date, hour=hour).data()


def createRelationshipsInfect(id, test_date, daysBack):
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
        "WHERE ID(pp) = $id AND r1.date > date($date) AND NOT "
        "(pp)-[:COVID_EXPOSURE{date: r1.date}]->(ip)"
        "RETURN DISTINCT ID(ip) , r1.date;"
    )
    locationContactQuery = (
        "MATCH (pp:Person)-[r1:VISIT]->(l:Location)<-[r2:VISIT]-(ip:Person) "
        "WHERE ID(pp) = $id AND ip <> pp AND r1.date > date($date) AND r2.date = r1.date AND "
        "((r1.star_hour < r2.start_hour AND r1.end_hour > r2.start_hour) OR "
        "(r2.start_hour < r1.start_hour AND r2.end_hour > r1.start_hour)) AND NOT "
        "(pp)-[:COVID_EXPOSURE{name: l.name , date: r1.date}]->(ip)"
        "RETURN DISTINCT ID(ip) , r1.date , l.name;"
    )

    # date = datetime.date.today() - datetime.timedelta(daysBack)
    """
    date is referred to date test - daysback 
    """
    date = test_date - datetime.timedelta(daysBack)
    infectedIds = []
    with driver.session() as s:
        familyInfected = s.read_transaction(findInfectInFamily, familyQuery, id)
        appInfected = s.read_transaction(findInfect, appContactQuery, id, date)
        locationInfected = s.read_transaction(findInfect, locationContactQuery, id, date)
        print(familyInfected)
        for el in familyInfected, appInfected, locationInfected:
            if len(el) > 0:
                # Take just the id
                infectedIds.append(el[0]['ID(ip)'])
        print("Family infected by " + str(id))
        print(familyInfected)
        print("App infected by " + str(id))
        print(appInfected)
        print("Location infected by " + str(id))
        print(locationInfected)

        infectedIds = []
        for el in familyInfected:
            print("Person is: ", el['ID(ip)'])
            infectedIds.append(el['ID(ip)'])
        print("Family infected by ", str(id))
        print(infectedIds)

        for infectedId in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:INFECTED{date:date($date)}]->(ip);"
            )
            s.write_transaction(createInfectFamily , query , id , infectedId, date.strftime("%Y-%m-%d"))

        infectedIds = []
        for el in appInfected:
            details = []
            details.append(el['ID(ip)'])
            details.append(el['r1.date'])
            infectedIds.append(details)
        print("App infected by " + str(id))
        print(infectedIds)

        for infectedId , infectedDate in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:INFECTED{date: date($date)}]->(ip);"
            )
            s.write_transaction(createInfectApp , query , id , infectedId , infectedDate)

        infectedIds = []
        print(locationInfected)
        for el in locationInfected:
            details = []
            details.append(el['ID(ip)'])
            details.append(el['r1.date'])
            details.append(el['l.name'])
            infectedIds.append(details)
        print("Location infected by " + str(id))
        print(infectedIds)

        for infectedId , infectedDate , infectedPlace in infectedIds:
            query = (
                "MATCH (pp:Person) , (ip:Person) "
                "WHERE ID(pp) = $id AND ID(ip) = $ipid "
                "CREATE (pp)-[:INFECTED{date: date($date) , name: $name}]->(ip);"
            )
            s.write_transaction(createInfectLocation , query , id , infectedId , infectedDate , infectedPlace)


def createInfectFamily(tx , query , id , ipid, date):
    """
    Method that create the relationship Infect
    """
    tx.run(query , id = id , ipid = ipid, date = date)


def createInfectApp(tx , query , id , ipid , date):
    """
    Method that create the relationship Infect
    """
    tx.run(query , id = id , ipid = ipid , date  = date)


def createInfectLocation(tx , query , id , ipid , date , name):
    """
    Method that create the relationship Infect
    """
    tx.run(query , id = id , ipid = ipid , date = date , name = name)


def findInfectInFamily(tx , query , id):
    """
    Method that executes the query to find the infected member of a family
    :param tx: is the transaction
    :param query: is the query to execute
    :param id: is the id of the positive Person
    """
    result = tx.run(query , id = id).data()
    return result


def findInfect(tx , query , id , date):
    """
    Method that executes the query to find the Person infected by other Persons
    :param tx: is the transaction
    :param query: is the query to execute
    :param id: is the id of the positive Person
    :param date: is the date from wich start the tracking
    """
    result = tx.run(query , id = id , date = date).data()
    return result


def createContact(tx, query, pId1, pId2 , hour , date):
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


def getVaccinesId(tx):
    """
    Method that retrieve a list of location ids
    :param tx: is the transaction
    :return: a list of ids
    """
    query = (
        "MATCH (v:Vaccine)"
        "RETURN ID(v)"
    )

    idsList = tx.run(query).data()
    return idsList


def getVaccinesIds():
    """
    Method that retrieves all the ids of Vaccine Node
    :return: a list of integer corresponding to the vaccine ids
    """
    with driver.session() as s:
        ids = s.write_transaction(getVaccinesId)
    print(ids)

    vIds = []
    for idEl in ids:
        vIds.append(idEl["ID(v)"])
    print(vIds)

    return vIds


def getTestsIds():
    """
    Method that retrieves all the ids of test Node
    :return: a list of integer corresponding to the test ids
    """
    with driver.session() as s:
        ids = s.write_transaction(getTestsId)
    print(ids)

    tIds = []
    for idEl in ids:
        tIds.append(idEl["ID(t)"])
    print(tIds)

    return tIds


def getTestsId(tx):
    """
    Method that retrieve a list of location ids
    :param tx: is the transaction
    :return: a list of ids
    """
    query = (
        "MATCH (t:Test)"
        "RETURN ID(t)"
    )

    idsList = tx.run(query).data()
    return idsList


def runQuery(tx, query, isReturn=False):
    """
    Method that runs a generic query
    :param tx: is the transaction
    :param query: is the query to perform
    :param isReturn: if True return the results, return nothing otherwise
    """
    result = tx.run(query)

    if isReturn:
        return result.data()


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


def printDatabase():
    """
    Method use to print the database structure using PlotDBStructure module
    :return: nothing
    """
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

        # Initialize the network attribute
        ps.PlotDBStructure.__init__()

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

        # Show the graph structure
        ps.PlotDBStructure.showGraph()
        return


if __name__ == '__main__':

    # Open the connection
    driver = openConnection()

    # Only read from the graph
    """printDatabase()

    # Close the connection
    closeConnection(driver)
    exit()"""

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
    vaccines = readVaccines()
    print("Vaccines read")
    tests = readTests()
    print("Tests read")

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

    # Query is an attribute that will contain the whole query to instantiate the database
    generalQuery = []

    # Generate all the Person Nodes and the family relationships
    cQuery, rQuery = createNodesFamily(families, houseAddresses)
    # Generate the locations node
    lQuery = createNodeLocations(locations)
    # Generate the vaccines nodes
    vQuery = createNodeVaccines(vaccines)
    # Generate the tests nodes
    tQuery = createNodeTests(tests)

    # Adds the creation node queries to the generalQuery
    for subQuery in cQuery:
        generalQuery.append(subQuery)
    for subQuery in lQuery:
        generalQuery.append(subQuery)
    for subQuery in vQuery:
        generalQuery.append(subQuery)
    for subQuery in tQuery:
        generalQuery.append(subQuery)
    # Adds the relation queries to the generalQuery
    for subQuery in rQuery:
        generalQuery.append(subQuery)

    print("The final query is: ")
    print(generalQuery)

    """
    # Find all the positive Person
    positiveIds = findAllPositivePerson()
    print("Positive are:")
    print(positiveIds)
    # Search all the infected Person tracked
    trackedPersonIds = []
    for positiveId in positiveIds:
        print(positiveId['ID(p)'])
        createRelationshipsInfect(positiveId['ID(p)'] , 7)

    # Print the whole structure
    print_database_with_pyvis()
    exit()
    """

    # Delete the nodes already present
    with driver.session() as session:
        numberOfNodes = session.write_transaction(deleteAll)

    # Generate the structure performing the node and relationship creation
    runQueryWrite(driver, generalQuery)

    # Generate random tests
    # Take tests ids
    testsIds = getTestsIds()
    personIds = getPersonIds()
    # Generate the relationship
    createRelationshipsMakeTest(driver, personIds, testsIds)

    # Generate random contacts with app tracing
    # Take Person ids of people with app attribute equal to True)
    personIds = getPersonIds(True)
    # Generate the relationships
    createRelationshipsAppContact(driver, personIds)

    # Generate random visits
    # Take Location ids
    locationIds = getLocationsIds()
    personId = getPersonIds()
    # Generate the relationship
    createRelationshipsVisit(driver , personIds, locationIds)

    # Generate random vaccines
    # Take vaccines ids
    vaccineIds = getVaccinesIds()
    # Generate the relationship
    createRelationshipsGetVaccine(driver, personIds, vaccineIds)

    # Verify the nodes are been created
    with driver.session() as session:
        numberOfNodes = session.read_transaction(countAll)
    print("Number of nodes: " + str(numberOfNodes))

    # Find all the positive Person
    positiveIds = findAllPositivePerson()
    print("Positive are:")
    print(positiveIds)
    # Search all the infected Person tracked
    trackedPersonIds = []

    """Commented because we create infection after a positive test"""
    """for positiveId in positiveIds:
        print(positiveId['ID(p)'])
        createRelationshipsInfect(positiveId['ID(p)'], 7)
        if random() < PROBABILITY_TO_BE_TESTED_AFTER_INFECTED:
            createRelationshipsMakeTest(driver, positiveIds, testsIds)
    """
    # Print the whole structure
    printDatabase()

    # Close the connection
    closeConnection(driver)
