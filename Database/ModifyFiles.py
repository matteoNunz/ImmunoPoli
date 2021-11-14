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


def readLocationsAndAddress():
    """
    Method that read all the locations with their attributes
    :return: a list of locations
    """
    locationsRead = []
    # Parallel reading from address_file and locations_file
    with open("Files/PublicPlaces.txt", 'r', encoding='utf8') as locations_file, \
            open("Files/Addresses.txt", 'r', encoding='utf8') as addresses_file:
        for (location_line, address_line) in zip(locations_file, addresses_file):
            if location_line == "\n" and address_line == "\n":
                continue

            details = location_line.rstrip("\n") + " , " + address_line.rstrip("\n")
            locationsRead.append(details)

    locations_file.close()
    addresses_file.close()
    return locationsRead


def textNewNames(lowerNames):
    f = open("Files/Names.txt" , "w" , encoding = 'utf8')
    for name in lowerNames:
        upperName = name[0].upper() + name[1:len(name)]
        f.write(upperName + "\n")


def textLocations(locationToText):
    f = open("Files/PublicPlaces.txt", "w", encoding='utf8')
    for location in locationToText:
        f.write(str(location) + "\n")


if __name__  == "__main__":
    #names = readNames()
    #textNewNames(names)
    locations = readLocationsAndAddress()
    textLocations(locations)
