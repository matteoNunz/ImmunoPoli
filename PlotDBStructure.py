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
                print("Person node")
                print("Mail: " , node['p']['mail'])
                # Add Person nodes
                label = node["ID(p)"]
                title = node['p']['name'] + " " + node['p']['surname'] + "," \
                        + node['p']['age'] + "," + node['p']['mail'] + "," \
                        + node['p']['number'] + ",app:" + node['p']['app']
                PlotDBStructure.network.add_node(node["ID(p)"] , label = label , title = title , color = 'orange')

            # If Location node
            elif 'l' in node.keys():
                print("Location node")
                # Add Location node
                label = node['ID(l)']
                title = node['l']['name'] + "," + node['l']['address'] + "," + node['l']['civic_number'] + "," \
                        + node['l']['CAP'] + "," + node['l']['city'] + "," + node['l']['province'] + "," \
                        + node['l']['type']
                PlotDBStructure.network.add_node(node['ID(l)'] , label = label , title = title , color = 'red')

            # If House node
            elif 'h' in node.keys():
                print("House node")
                # Add House nodes
                label = node['ID(h)']
                title = node['h']['name']
                PlotDBStructure.network.add_node(node['ID(h)'] , label= label , title = title , color = 'blue')

            # If Vaccine node
            elif 'v' in node.keys():
                print("Vaccine node")
                # Add Vaccine nodes
                label = node['ID(v)']
                title = node['v']['name'] + "," + node['v']['producer']
                PlotDBStructure.network.add_node(node['ID(v)'] , label = node , title = title , color = 'gray')

            # If Test node
            elif 't' in node.keys():
                print("Test node")
                # Add Test nodes
                label = node['ID(t)']
                title = node['t']['name']
                PlotDBStructure.network.add_node(node['ID(t)'] , label = label , title = title , color='green')

            # If it's a relationship
            elif 'r' in node.keys():
                print("A relationship")
                relationship = node  # Just conceptual
                # Take the ids of the nodes
                id1 = relationship['ID(n1)']
                id2 = relationship['ID(n2)']
                # Take the relationship type
                rType = relationship['r'][1]

                if rType == 'LIVE':
                    PlotDBStructure.network.add_edge(id1 , id2 , title = rType , color = 'black')
                elif rType == 'APP_CONTACT':
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + str(relationship['r.hour'])
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = 'black')
                elif rType == 'VISIT':
                    title = rType + ",date: " + str(relationship['r.date']) + ",start_hour: " \
                            + str(relationship['r.start_hour']) + ",end_hour: " + str(relationship['r.end_hour'])
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color='black')
                elif rType == 'GET':
                    title = rType + ",date: " + str(relationship['r.date']) + ",expiration_date: " \
                            + str(relationship['r.expirationDate']) + ",country: " + relationship['r.country']
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = 'black')
                elif rType == 'MAKE':
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + str(relationship['r.hour']) \
                            + ",result: " + relationship['r.result']
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = 'black')
                elif rType == 'INFECTED':
                    if relationship['r.name'] is not None:
                        color = 'blue'
                    elif relationship['r.date'] is not None:
                        color = 'green'
                    else:
                        color = 'red'
                    title = rType + ",date: " + str(relationship['r.date']) + ",place: " + str(relationship['r.name'])
                    PlotDBStructure.network.add_edge(id1 , id2 , title = title , color = color)
                else:
                    pass

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
