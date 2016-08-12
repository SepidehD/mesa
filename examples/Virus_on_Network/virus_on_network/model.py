import networkx as nx

from decimal import Decimal
from random import choice

from mesa import Agent, Model
from mesa.time import RandomActivation


class VirusAgent(Agent):
    def __init__(self, unique_id, infected=0):
        self.unique_id = unique_id
        self.infected = infected

    def __str__(self):
        return "%s, %s" % (str(self.unique_id), self.infected)


class VirusModel(Model):
    """A model with some number of agents"""

    def __init__(self, N=150, width=500, height=500, avg_node_degree=3,
                 initial_outbreak_size=3,):

        self.num_agents = N
        self.avg_node_degree = Decimal(avg_node_degree)
        self.schedule = RandomActivation(self)
        self.graph = self._create_graph()
        self.initial_outbreak_size = initial_outbreak_size

        self.running = True

        self._infect_nodes(self.initial_outbreak_size)

    def _create_graph(self):
        G = nx.Graph()

        num_links = round(self.avg_node_degree * self.num_agents / 2)
        G = nx.dense_gnm_random_graph(self.num_agents, num_links)

        # Assign agents to the nodes in the graph
        for i in G.nodes():
            G.node[i]['agent'] = VirusAgent(i).__dict__
            # self.schedule.add(agent)

        # TODO: Rewrite node selection to do the following...
        # "The network that is created is based on proximity
        # (Euclidean distance) between nodes. A node is randomly chosen and
        # connected to the nearest node that it is not already connected
        # to. This process is repeated until the network has the correct
        # number of links to give the specified average node degree."

        # From:
        # Stonedahl, F. and Wilensky, U. (2008). NetLogo Virus on a Network
        # model.

        # There maybe an easy way to do it using one of the graphs from
        # this page:
        # https://networkx.github.io/documentation/networkx-1.10/reference/generators.html

        return G

    def _infect_nodes(self, N):
        G = self.graph
        for i in range(N):
            node = choice(G.nodes())
            G.node[node]['agent'] = 1
        self.graph = G

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
