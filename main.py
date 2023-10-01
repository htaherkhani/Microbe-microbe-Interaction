import pandas as pd
import csv
import networkx as nx
import json
import matplotlib.pyplot as plt

def make_graph(growth_rates, similarity=None, correlations=None):
    """ Make a graph of the interaction network.

    Parameters
    ----------
    growth_rates : pandas.DataFrame
        Each element is a path to a single species model file
    similarity : pandas.DataFrame
        Path to output folder where community model JSON file is saved
    correlations : list of tuple
        Each

    Returns
    -------
    networkx.Graph
        Graph representation of interaction network
    """

    # supposedly, width can be an array of floats, add as edge attribute

    # Each node is colored a shade of gray based on the similarity of
    # the OTU to the corresponding NCBI genome.
    node_colors = dict()
    if similarity is not None:
        for index, row in similarity.iterrows():
            if row['SIMILARITY'] >= 99.9:
                node_colors[row['GENOME_ID']] = "#7894C6"
            elif row['SIMILARITY'] >= 99.8:
                node_colors[row['GENOME_ID']] = "#C47FBD"
            elif row['SIMILARITY'] >= 99.7:
                node_colors[row['GENOME_ID']] = "#d1c02a"
            elif row['SIMILARITY'] >= 99.2:
                node_colors[row['GENOME_ID']] = "#C8C46F"
            elif row['SIMILARITY'] >= 98.0:
                node_colors[row['GENOME_ID']] = "#707070"
            elif row['SIMILARITY'] >= 99.8:
                node_colors[row['GENOME_ID']] = "#d1462a"
            elif row['SIMILARITY'] >= 95.0:
                node_colors[row['GENOME_ID']] = "#C8A46F"
            elif row['SIMILARITY'] >= 90.0:
                node_colors[row['GENOME_ID']] = "#56dbcb"
            else:
                node_colors[row['GENOME_ID']] = "#d9d9d9"

    # The thickness of each edge is set based on the correlation between the
    # two OTUs in the pair.
    edge_width = dict()
    if correlations is not None:
        # The similarity data frame is needed to translate OTU IDs to genome IDS.
        if similarity is None:
            raise ValueError('A similarity DataFrame must be provided when correlations are provided')
        for corr in correlations:
            # Translate OTU ID to genome ID.
            a_id = similarity.loc[similarity['OTU_ID'] == corr[0]].iloc[0]['GENOME_ID']
            if a_id not in edge_width:
                edge_width[a_id] = dict()
            b_id = similarity.loc[similarity['OTU_ID'] == corr[1]].iloc[0]['GENOME_ID']
            if b_id not in edge_width:
                edge_width[b_id] = dict()

            # Set width based on correlation value.
            if corr[2] >= 0.995:
                width = 20.0
            elif corr[2] >= 0.85:
                width = 15.5
            elif corr[2] >= 0.70:
                width = 11.0
            elif corr[2] >= 0.65:
                width = 8.5
            elif corr[2] >= 0.50:
                width = 5.0
            elif corr[2] >= -0.10:
                width = 2.5
            elif corr[2] >= -0.50:
                width = 2.0
            elif corr[2] >= -0.70:
                width = 1.5
            else:
                width = 1.0

            # Order of growth rates data frame is non-deterministic so include
            # width value indexed in both orders.
            edge_width[a_id][b_id] = width
            edge_width[b_id][a_id] = width

    # For each interaction, create the nodes and an edge between them.
    graph = nx.Graph()
    for index, row in growth_rates.iterrows():
        # Add a node for the first organism in the pair.
        try:
            color1 = node_colors[row['A_ID']]
        except KeyError:
            color1 = '#e0e0e0'
        # print(row['A_ID'], {'color': color})
        #graph.add_node(row['A_ID'], {'color': color})
        graph.add_node(row['A_ID'], color = color1)

        # Add a node for the second organism in the pair.
        try:
            color1 = node_colors[row['B_ID']]
        except KeyError:
            color1 = '#e0e0e0'
        # graph.add_node(row['B_ID'], {'color': color})
        graph.add_node(row['B_ID'],color = color1)

        # Classify the interaction between the two species to set the color
        # of the edge between the two nodes.
        if row['TYPE'] == 'Mutualism':
            color1 = '#2ca02c'  # Green
        elif row['TYPE'] == 'Parasitism':
            color1 = '#d62728'  # Red
        elif row['TYPE'] == 'Commensalism':
            color1 = '#2ca02c'  # Green
        elif row['TYPE'] == 'Competition':
            color1 = '#d62728'  # Red
        elif row['TYPE'] == 'Neutralism':
            color1 = '#c7c7c7'  # Gray
        elif row['TYPE'] == 'Amensalism':
            color1 = '#d62728'  # Red
        else:
            color1 = '#c7c7c7'  # Gray

        # Set the width of the edge based on the correlation between the
        # two species. A higher correlation gets a thicker edge.
        if len(edge_width) > 0:
            try:
                width1 = edge_width[row['A_ID']][row['B_ID']]
            except KeyError:
                width1 = 2.0
        else:
            width1 = 2.0

        # Add an edge between the two nodes.
        # graph.add_edge(row['A_ID'], row['B_ID'], {'color': color1, 'width': width})
        graph.add_edge(row['A_ID'], row['B_ID'], color= color1, width= width1)

    return graph


def plot_graph(graph):
    """ Plot a graph using a circular layout.

    Parameters
    ----------
    graph : networkx.Graph
        Graph representation of interaction network
    """

    # Draw the graph using circular layout.
    edge_widths = nx.get_edge_attributes(graph, 'width')
    edge_colors = nx.get_edge_attributes(graph, 'color')
    node_colors = nx.get_node_attributes(graph, 'color')
    # for i in range(len(node_colors.keys())):
    #     a = str(i)
    #     node_colors[a] = node_colors.pop(i)
    # a = [i+1 for i in range(len(node_colors.keys()))]
    # print(node_colors.keys())
    # nx.draw_circular(graph, with_labels=True, width=edge_widths.values(),
    #                  edgelist=edge_colors.keys(), edge_color=edge_colors.values(),
    #                  nodelist=node_colors.keys(), node_color=node_colors.values())

    nx.draw_circular(graph, with_labels=True, width=list(edge_widths.values()),
                     edgelist=edge_colors.keys(), edge_color=list(edge_colors.values()),
                     nodelist=node_colors.keys(), node_color=list(node_colors.values()))

    # nx.draw_circular(graph, with_labels=True, width=list(edge_widths.values()),
    #                  edgelist=edge_colors.keys(), edge_color=list(edge_colors.values()),
    #                  nodelist=a, node_color=list(node_colors.values()))   
                  
    plt.show()
    return


# 


growth_rates = pd.read_csv ('growth_rates.csv')
# print (growth_rates.head())
# growth_rates = growth_rates.astype({"A_ID": int, "B_ID": int})
# # pd.to_numeric(growth_rates['A_ID'], downcast='integer')
# print(growth_rates.head())

similarity = pd.read_csv ('similarity.csv')
# print (similarity.head())
correlations = []
with open('correlation.txt', newline = '') as games:                                                                                          
    game_reader = csv.reader(games, delimiter='\t')
    for game in game_reader:
        correlations.append(tuple([float(i) for i in game]))
        # print(correlations)

graph = make_graph(growth_rates, similarity, correlations)
plot_graph(graph)















# with open('correlation.txt','r',newline='') as f:
#     r = csv.reader(f,delimiter='\t')
#     for line in r:
#         print(ascii(line))

# with open('correlation.txt') as f:
#     content = f.read().splitlines()
# f.close
# print(r)

# f = open('correlation.txt','r')
# print(f)
