import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pycowview import manipulate, data


def is_right_side(cow_id, cow_list):

    if (cow_id in cow_list.tag_id.unique()):
        return 1
    else:
        return 0

def get_right_side_cows(PA_data_file, barn_file):
    df = data.csv_read_PA('C:/Users/Marcus/Desktop/Studier/Projekt/correctid/PA_20201016T000000UTC.csv', 0)
    df_left, df_right = manipulate.left_right(df, 'C:/Users/Marcus/Desktop/Studier/Projekt/CowDistance-Project/data/barn.csv')
    return df_right

def graph(synchrony_data_file, raw_data_file, barn_file, uses_proximity, activity, threshold):
    """
    Plots a graph where each node represents a cow, and the color of the node represents which side of the barn it's on.
    Each edge between two nodes represents a synchrony of those two cows that exceeds the given threshold value.

    Parameters:
        synchrony_data_file: file containing the synchrony data
        raw: file containing the raw data which the synchrony data was generated from
        barn_data_file: file containing the barn layout
        uses_proximity: if True, the synchrony data uses proximity. It is important that this is set correctly.
        activity: which activity to use, allowed values are
            all
            proximity_only
            unknown
            standing
            walking
            in_cubicle
            feeding
            drinking
            outside
        threshold: the value which the synchrony has to exceed for an edge to be rendered
    """

    df = pd.read_csv(synchrony_data_file, skiprows = 0, sep = ',', header=0)
    if (uses_proximity):
        df.columns = ['cow1','cow2','proximity_only','proximity_only_u','all','all_u','unknown','unknown_u','standing','standing_u','walking','walking_u','in_cubicle','in_cubicle_u','feeding','feeding_u','drinking','drinking_u','null','null_u','outside','outside_u','same_side']
    else:
        df.columns = ['cow1','cow2','avgdist','all','all_u','unknown','unknown_u','standing','standing_u','walking','walking_u','in_cubicle','in_cubicle_u','feeding','feeding_u','drinking','drinking_u','null','null_u','outside','outside_u','same_side']

    cow_ids = df.cow1.unique()

    col = df[activity]
    col_u = df[activity+"_u"]

    # Sort out all pairs below the threshold and above 95% (considered invalid)
    df = df[((col/(col + col_u)) > threshold) & ((col/(col + col_u)) < 0.95)]

    # Use networkx to create graph
    G = nx.from_pandas_edgelist(df, 'cow1', 'cow2')
    degrees = dict(G.degree)

    # Get the list of cows on the right side of the barn. This is so we can plot the cows with a different color depending on which side on the barn they are.
    # Preferably, we'd want to re-write this someohow to avoid using the original raw data.
    right_cows = get_right_side_cows(raw_data_file, barn_file)
    
    colors = [is_right_side(node, right_cows) for node in G.nodes()]

    fig = plt.figure(1, figsize=(15, 10), dpi=60)

    nx.draw_networkx(G, nodelist=degrees.keys(), node_size=[5*(v+2) for v in degrees.values()], node_color=colors, with_labels=False, font_size=14, cmap=plt.cm.winter)

    fig.suptitle('Pairwise synchrony, activity='+str(activity)+', threshold='+str(threshold*100)+'%', fontsize=30)

    plt.tight_layout()
    plt.show()

def histogram(synchrony_data_file, uses_proximity, activity, log_scale=True):
    """
    Plots a histogram over the synchrony values for each pair

    Parameters:
        synchrony_data_file: file containing the synchrony data
        uses_proximity: if True, the synchrony data uses proximity. It is important that this is set correctly.
        activity: which activity to use, allowed values are
            all
            proximity_only
            unknown
            standing
            walking
            in_cubicle
            feeding
            drinking
            outside
        log_scale: If True, the plot will use log scale on the y-axis
    """
    df = pd.read_csv(synchrony_data_file, skiprows = 0, sep = ',', header=0)
    if (uses_proximity):
        df.columns = ['cow1','cow2','proximity_only','proximity_only_u','all','all_u','unknown','unknown_u','standing','standing_u','walking','walking_u','in_cubicle','in_cubicle_u','feeding','feeding_u','drinking','drinking_u','null','null_u','outside','outside_u','same_side']
    else:
        df.columns = ['cow1','cow2','avgdist','all','all_u','unknown','unknown_u','standing','standing_u','walking','walking_u','in_cubicle','in_cubicle_u','feeding','feeding_u','drinking','drinking_u','null','null_u','outside','outside_u','same_side']

    cow_ids = df.cow1.unique()


    col = df[activity]
    col_u = df[activity+"_u"]

    
    df = df[((col/(col + col_u)) < 0.95)]

    col = df[activity]
    col_u = df[activity+"_u"]

    fig = plt.figure(1, figsize=(15, 10), dpi=60)

    fig.suptitle("Pairwise synchrony histogram", fontsize=30)

    plt.ylabel("Pairs", fontsize=20)
    plt.xlabel("Pairwise synchrony", fontsize=20)

    col_log = (col/(col + col_u))

    plt.hist(col_log, bins=200)

    if (log_scale):
        plt.yscale('log')

    plt.tight_layout()
    plt.show()

    
    
#graph("synchronicity_data_prox.csv", 'C:/Users/Marcus/Desktop/Studier/Projekt/correctid/PA_20201016T000000UTC.csv', 'C:/Users/Marcus/Desktop/Studier/Projekt/CowDistance-Project/data/barn.csv', uses_proximity=True, activity="all", threshold=0.1)

histogram("synchronicity_data_prox.csv", uses_proximity=True, activity="all")

#'C:/Users/Marcus/Desktop/Studier/Projekt/correctid/PA_20201016T000000UTC.csv', 'C:/Users/Marcus/Desktop/Studier/Projekt/CowDistance-Project/data/barn.csv'