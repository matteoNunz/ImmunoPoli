from pyvis.network import Network


class PlotDBStructure:
    """
    Utility class called to print the desired structure of the database
    Call the __init__ method to initialize the network attribute -> maybe add some color parameters
    Call the addStructure method to add nodes/relationships
    Call the showGraph method to show the html file
    """
    @staticmethod
    def __init__():
        """
        Method that creates and initialize the network attribute
        """
        PlotDBStructure.network = Network('500px' , '500px' , directed = True)
        PlotDBStructure.personColor = 'orange'
        PlotDBStructure.locationColor = 'red'
        PlotDBStructure.houseColor = 'blue'
        PlotDBStructure.vaccineColor = 'gray'
        PlotDBStructure.testColor = 'green'

        PlotDBStructure.liveColor = 'black'
        PlotDBStructure.visitColor = 'black'
        PlotDBStructure.appContactColor = 'orange'
        PlotDBStructure.getVaccineColor = 'black'
        PlotDBStructure.makeTestColor = 'black'
        PlotDBStructure.infectedFamilyColor = 'red'
        PlotDBStructure.infectedAppColor = 'green'
        PlotDBStructure.infectedLocationColor = 'blue'

    @staticmethod
    def addStructure(listOfNodesAndArcs = None):
        """
        Method that given a list of nodes/relationships adds the corresponding representation in the network
        :param listOfNodesAndArcs: list of nodes or arcs or both
        """
        if listOfNodesAndArcs is None:
            return

        # Create nodes and arcs
        for node in listOfNodesAndArcs:
            # If Person node
            if 'p' in node.keys():
                # print("Person node")
                # Add Person nodes
                label = node["ID(p)"]
                title = node['p']['name'] + " " + node['p']['surname'] + "," \
                        + node['p']['age'] + "," + node['p']['mail'] + "," \
                        + node['p']['number'] + ",app:" + node['p']['app']
                color = PlotDBStructure.personColor
                PlotDBStructure.network.add_node(node["ID(p)"] , label = label , title = title , color = color)

            # If Location node
            elif 'l' in node.keys():
                # print("Location node")
                # Add Location node
                label = node['ID(l)']
                title = node['l']['name'] + "," + node['l']['address'] + "," + node['l']['civic_number'] + "," \
                        + node['l']['CAP'] + "," + node['l']['city'] + "," + node['l']['province'] + "," \
                        + node['l']['type']
                color = PlotDBStructure.locationColor
                PlotDBStructure.network.add_node(node['ID(l)'] , label = label , title = title , color = color)

            # If House node
            elif 'h' in node.keys():
                # print("House node")
                # Add House nodes
                label = node['ID(h)']
                title = node['h']['name']
                color = PlotDBStructure.houseColor
                PlotDBStructure.network.add_node(node['ID(h)'] , label= label , title = title , color = color)

            # If Vaccine node
            elif 'v' in node.keys():
                # print("Vaccine node")
                # Add Vaccine nodes
                label = node['ID(v)']
                title = node['v']['name'] + "," + node['v']['producer']
                color = PlotDBStructure.vaccineColor
                PlotDBStructure.network.add_node(node['ID(v)'] , label = label , title = title , color = color)

            # If Test node
            elif 't' in node.keys():
                # print("Test node")
                # Add Test nodes
                label = node['ID(t)']
                title = node['t']['name']
                color = PlotDBStructure.testColor
                PlotDBStructure.network.add_node(node['ID(t)'] , label = label , title = title , color = color)

            # If it's a relationship
            elif 'r' in node.keys():
                # print("A relationship")
                relationship = node  # Just conceptual
                # Take the ids of the nodes
                id1 = relationship['ID(n1)']
                id2 = relationship['ID(n2)']
                # Take the relationship type
                rType = relationship['r'][1]

                if rType == 'LIVE':
                    color = PlotDBStructure.liveColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = rType , color = color)
                elif rType == 'APP_CONTACT':
                    hour = str(relationship['r.hour']).split('.')[0]
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + hour
                    color = PlotDBStructure.appContactColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                elif rType == 'VISIT':
                    start_hour = str(relationship['r.start_hour']).split('.')[0]
                    end_hour = str(relationship['r.end_hour']).split('.')[0]
                    title = rType + ",date: " + str(relationship['r.date']) + ",start_hour: " \
                            + start_hour + ",end_hour: " + end_hour
                    color = PlotDBStructure.visitColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                elif rType == 'GET':
                    title = rType + ",date: " + str(relationship['r.date']) + ",expiration_date: " \
                            + str(relationship['r.expirationDate']) + ",country: " + relationship['r.country']
                    color = PlotDBStructure.getVaccineColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                elif rType == 'MAKE':
                    hour = str(relationship['r.hour']).split('.')[0]
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + hour \
                            + ",result: " + relationship['r.result']
                    color = PlotDBStructure.makeTestColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                elif rType == 'INFECTED':
                    title = rType + ",date: " + str(relationship['r.date']) + ",place: " + str(relationship['r.name'])
                    if relationship['r.date'] is None:
                        color = PlotDBStructure.infectedFamilyColor
                    elif relationship['r.name'] is None:
                        color = PlotDBStructure.infectedAppColor
                    else:
                        color = PlotDBStructure.infectedLocationColor
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                else:
                    pass

    @staticmethod
    def setPersonColor(color):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.personColor = color

    @staticmethod
    def setHouseColor(color):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.houseColor = color

    @staticmethod
    def setLocationColor(color):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.locationColor = color

    @staticmethod
    def setVaccineColor(color):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.vaccineColor = color

    @staticmethod
    def setTestColor(color):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.testColor = color

    @staticmethod
    def setLiveColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.liveColor = color

    @staticmethod
    def setVisitColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.visitColor = color

    @staticmethod
    def setAppContactColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.appContactColor = color

    @staticmethod
    def setGetVaccineColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.getVaccineColor = color

    @staticmethod
    def setMakeTestColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.makeTestColor = color

    @staticmethod
    def setInfectedFamilyColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.infectedFamilyColor = color

    @staticmethod
    def setInfectedAppColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.infectedAppColor = color

    @staticmethod
    def setInfectedLocationColor(color):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.infectedLocationColor = color

    @staticmethod
    def showGraph():
        """
        Method that shows the network built until now
        Shows the graph only if there is at least one node
        """
        # Show the result
        if len(PlotDBStructure.network.get_nodes()) == 0:
            print("Empty graph: nothing to show!")
            return
        PlotDBStructure.network.set_edge_smooth('dynamic')
        PlotDBStructure.network.show('graph.html')
