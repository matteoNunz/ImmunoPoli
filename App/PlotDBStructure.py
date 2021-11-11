from pyvis.network import Network
import webbrowser
import tkinter as tk
import platform
import os


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
        # Take the dimensions of the screen
        root = tk.Tk()
        width = str(root.winfo_screenwidth()) + "px"
        height = str(root.winfo_screenheight()) + "px"
        root.destroy()

        PlotDBStructure.network = Network(height , width , directed=True)
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
        PlotDBStructure.infectedFamilyAndAppColor = 'red'
        PlotDBStructure.infectedLocationColor = 'green'

    @staticmethod
    def addStructure(listOfNodesAndArcs=None):
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

                # Add Person nodes
                label = node["ID(p)"]
                title = node['p']['name'] + " " + node['p']['surname'] + "," \
                        + node['p']['age'] + "," + node['p']['mail'] + "," \
                        + node['p']['number'] + ",app:" + node['p']['app']
                #title = titleList
                color = PlotDBStructure.personColor
                PlotDBStructure.network.add_node(node["ID(p)"], label=label, title=title, color=color)

            # If Location node
            elif 'l' in node.keys():

                # Add Location node
                if 'rate' in node.keys():
                    label = str(node['ID(l)']) + ", rate: " + str(node['rate']*100) + "%"
                else:
                    label = node['ID(l)']

                title = node['l']['name'] + "," + node['l']['address'] + "," + node['l']['civic_number'] + "," +node['l']['CAP'] + "," + node['l']['city'] + "," + node['l']['province'] + "," +node['l']['type']
                color = PlotDBStructure.locationColor
                PlotDBStructure.network.add_node(node['ID(l)'], label=label, title=title, color=color)

            # If House node
            elif 'h' in node.keys():

                # Add House nodes
                label = node['ID(h)']
                title = node['h']['name']
                color = PlotDBStructure.houseColor
                PlotDBStructure.network.add_node(node['ID(h)'], label=label, title=title, color=color)

            # If Vaccine node
            elif 'v' in node.keys():

                # Add Vaccine nodes
                label = node['ID(v)']
                title = node['v']['name'] + "," + node['v']['producer']
                color = PlotDBStructure.vaccineColor
                PlotDBStructure.network.add_node(node['ID(v)'], label=label, title=title, color=color)

            # If Test node
            elif 't' in node.keys():

                # Add Test nodes
                label = node['ID(t)']
                title = node['t']['name']
                color = PlotDBStructure.testColor
                PlotDBStructure.network.add_node(node['ID(t)'], label=label, title=title, color=color)

            # If it's a relationship
            elif 'r' in node.keys():

                relationship = node  # Just conceptual
                # Take the ids of the nodes
                id1 = relationship['ID(n1)']
                id2 = relationship['ID(n2)']
                # Take the relationship type
                rType = relationship['r'][1]

                if rType == 'LIVE':
                    color = PlotDBStructure.liveColor
                    PlotDBStructure.network.add_edge(id1, id2, title=rType, color=color)
                elif rType == 'APP_CONTACT':
                    if 'r.hour' in relationship.keys():
                        hour = str(relationship['r.hour']).split('.')[0]
                    else:
                        hour = None
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + hour
                    color = PlotDBStructure.appContactColor
                    PlotDBStructure.network.add_edge(id1, id2, title=title, color=color)
                elif rType == 'VISIT':
                    start_hour = str(relationship['r.start_hour']).split('.')[0]
                    end_hour = str(relationship['r.end_hour']).split('.')[0]
                    title = rType + ",date: " + str(relationship['r.date']) + ",start_hour: " \
                            + start_hour + ",end_hour: " + end_hour
                    color = PlotDBStructure.visitColor
                    PlotDBStructure.network.add_edge(id1, id2, title=title, color=color)
                elif rType == 'GET':
                    title = rType + ",date: " + str(relationship['r.date']) + ",expiration_date: " \
                            + str(relationship['r.expirationDate']) + ",country: " + relationship['r.country']
                    color = PlotDBStructure.getVaccineColor
                    PlotDBStructure.network.add_edge(id1, id2, title=title, color=color)
                elif rType == 'MAKE_TEST':
                    hour = str(relationship['r.hour']).split('.')[0]
                    title = rType + ",date: " + str(relationship['r.date']) + ",hour: " + hour \
                            + ",result: " + relationship['r.result']
                    color = PlotDBStructure.makeTestColor
                    PlotDBStructure.network.add_edge(id1, id2, title=title, color=color)
                elif rType == 'COVID_EXPOSURE':
                    title = rType + ",date: " + str(relationship['r.date']) + ",place: " + str(relationship['r.name'])
                    if relationship['r.name'] is None:
                        color = PlotDBStructure.infectedFamilyAndAppColor
                    else:
                        color = PlotDBStructure.infectedLocationColor
                    PlotDBStructure.network.add_edge(id1, id2, title=title, color=color)
                else:
                    pass

    @staticmethod
    def addLiveRelationships(pId, hId):
        """
        Method that adds the relationships LIVE
        :param pId: is the id of the Person
        :param hId: is the id of the House
        """
        color = PlotDBStructure.liveColor
        PlotDBStructure.network.add_edge(pId, hId, title='LIVE', color=color)

    @staticmethod
    def setPersonColor(color='orange'):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.personColor = color

    @staticmethod
    def setHouseColor(color='blue'):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.houseColor = color

    @staticmethod
    def setLocationColor(color='red'):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.locationColor = color

    @staticmethod
    def setVaccineColor(color='gray'):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.vaccineColor = color

    @staticmethod
    def setTestColor(color='green'):
        """
        Method to set the color of the nodes in the graph
        """
        PlotDBStructure.testColor = color

    @staticmethod
    def setLiveColor(color='black'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.liveColor = color

    @staticmethod
    def setVisitColor(color='black'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.visitColor = color

    @staticmethod
    def setAppContactColor(color='orange'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.appContactColor = color

    @staticmethod
    def setGetVaccineColor(color='black'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.getVaccineColor = color

    @staticmethod
    def setMakeTestColor(color='black'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.makeTestColor = color

    @staticmethod
    def setInfectedFamilyAndAppColor(color='red'):
        """
        Method to set the color of the relationships in the graph
        """
        PlotDBStructure.infectedFamilyAndAppColor = color

    @staticmethod
    def setInfectedLocationColor(color='blue'):
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

        if platform.system() == "Darwin":  # check if on OSX
            file_location = "file://" + os.path.abspath('graph.html')
            webbrowser.get().open(file_location, new=1)
        else:
            PlotDBStructure.network.show('graph.html')

