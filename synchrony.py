from concurrent.futures import process
from os import X_OK
from pycowview import manipulate
from pycowview import data
#import pandas as pd
#import statistics
import csv
import time
import math


def activity_type_to_data_index2(activity_type):
    if ((activity_type >= 0) & (activity_type <= 5)): return activity_type + 3
    if (activity_type == 998): return 9
    if (activity_type == 999): return 10
    else: return -1


def get_sync_data_header2(index):
    if (index == 0): return "Cow1"
    if (index == 1): return "Cow2"
    if (index == 2): return "Total"
    if (index == 3): return "Unknown"
    if (index == 4): return "Standing"
    if (index == 5): return "Walking"
    if (index == 6): return "Sleeping"
    if (index == 7): return "Feeding"
    if (index == 8): return "Drinking"
    if (index == 9): return "???"
    if (index == 10): return "Outside"
    else: return "Undefined"
    


def get_pairs(df, barn):
    """
    Finds and returns all unordered pairs of cow_ids in a given data file.

    Parameters:
        df: the pandas dataframe
        barn: the path to the file containing the barn layout

    Returns:
        An array of 3-tuples, each element in the array representing one pair of cows. 
        The 3-tuple has the following format:
            (cow_id1, cow_id2, same_side)
        where 
            cow_id1: the id of the first cow in the pair
            cow_id2: the id of the second cow in the pair
            same_side: 1 if the cows are on the same side of the barn, otherwise 0
    """

    # Remove inactive tags
    df = manipulate.detect_drop_inactive_tags(df, threshold=1800)
    list_cows = df.tag_id.unique()

    # Separate left cows and right cows
    df_left, df_right = manipulate.left_right(df, barn)

    list_cow_left = df_left.tag_id.unique().tolist()
    list_cow_right = df_right.tag_id.unique().tolist()

    cow_count = len(list_cows)
    pair_count = int((cow_count * (cow_count-1))/2)
    pairs = [(0,0,0)]*pair_count

    k = 0
    for i in range(cow_count):
        for j in range(cow_count-i-1):
            same_side = 0

            if ((list_cow_left.count(list_cows[i])) & (list_cow_left.count(list_cows[i+j+1]))):
                same_side = 1
            elif ((list_cow_right.count(list_cows[i])) & (list_cow_right.count(list_cows[i+j+1]))):
                same_side = 1

            pairs[k] = (list_cows[i], list_cows[i+j+1], same_side)
            k=k+1

    return pairs

def get_synchrony(df, pairs, limit, print_progress=False):
    """
    Calculates and returns a list with the time spent (in milliseconds) in synchrony between all pairs. In synchrony here refers to the time spent performing the same activity.

    Parameters:
        df: the pandas dataframe
        pairs: the list of pairs. Use get_pairs() to generate this list.
        limit: how many pairs in the list we want to use. If 0, all values will be used.
        print_progress: whether we want to print the progress in console or not

    Returns:
        A list of synchrony between every pair of cows. Each row in the list represents a pair, and is an array with the followning structure:
            (cow1, cow2, avg_distance, all_activites, all_activities_u, activity0, activity0_u, ..., activity999, activity999_u, same_side)
        where 
            cow1: the id of the first cow in the pair
            cow2: the id of the second cow in the pair
            avg_distance: the average distance from cow 1 to cow 2
            all_activities: total time spent in synchrony for any activity
            all_activities_u: total time not spent in synchrony for any activity
            activity*: total time spent in synchrony for the activity with id *
            activity*_u: total time not spent in synchrony for the activity with id *
            same_side: 1 if the cows are on the same side of the barn, otherwise 0
    """

   

    # If the limit is 0, set it to all pairs
    if (limit <= 0):
        limit = len(pairs)

    sync_percent = [0]*limit

    # Get synchrony for every pair
    index = 0
    for pair in pairs:
        if (index == limit):
            break
        sync_percent[index] = get_synchrony_for(df, pair)
        index += 1

        # Print progress
        if (print_progress==True & ((index%100)==0)):
            print('Progress: '+str(index)+"/"+str(limit)+" ("+str(100*index/limit)+"%)")

    return sync_percent

def get_synchrony_proximity(df, pairs, proximity_threshold, limit, print_progress=False):
    """
    Calculates and returns a list with the time spent (in milliseconds) in synchrony between all pairs. In synchrony here refers to the time spent performing the same activity and being in proximity.

    Parameters:
        df: the pandas dataframe
        pairs: the list of pairs. Use get_pairs() to generate this list.
        proximity_threshold: the maximum distance between the cows for them to be considered in synchrony
        limit: how many pairs in the list we want to use. If 0, all values will be used.
        print_progress: whether we want to print the progress in console or not

    Returns:
        A list of synchrony between every pair of cows. Each row in the list represents a pair, and is an array with the followning structure:
            (cow1, cow2, avg_distance, all_activites, all_activities_u, activity0, activity0_u, ..., activity999, activity999_u, same_side)
        where 
            cow1: the id of the first cow in the pair
            cow2: the id of the second cow in the pair
            prox_only: total time spent in synchrony (ignoring whether the activities are equal or not)
            prox_only_u: total time not spent in synchrony (ignoring whether the activities are equal or not)
            all_activities: total time spent in synchrony for any activity
            all_activities_u: total time not spent in synchrony for any activity
            activity*: total time spent in synchrony for the activity with id *
            activity*_u: total time not spent in synchrony for the activity with id *
            same_side: 1 if the cows are on the same side of the barn, otherwise 0
    """
    index = 0
    if (limit <= 0):
        limit = len(pairs)

    sync_percent = [0]*limit
    for pair in pairs:
        if (index == limit):
            break
        sync_percent[index] = get_synchrony_proximity_for(df, proximity_threshold, pair)
        index += 1
        if (print_progress==True & ((index%100)==0)):
            print('Progress: '+str(index)+"/"+str(limit)+" ("+str(100*index/limit)+"%)")

    return sync_percent

def get_synchrony_for(df, pair):
    """
    Calculates and returns the time spent in synchrony between two pairs of cows, see get_synchrony().

    Parameters:
        df: the pandas dataframe
        pair: the pair

    Returns:
        An array with the time spend in synchrony between the pair.
    """
    cow_id1 = pair[0]
    cow_id2 = pair[1]

    cow_merge = df.loc[(df['tag_id'] == cow_id1) | (df['tag_id'] == cow_id2)]
    cow_merge = cow_merge.sort_values('start')

    start_time = df['start'][0]
    end_time = 0
  
    activity1 = 0
    activity2 = 0
    synched = 0
    unsynched = 0
    time = start_time
    pos1 = (0,0)
    pos2 = (0,0)

    avg_dist = 0

    synched_specific = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 998: 0, 999: 0}
    unsynched_specific = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 998: 0, 999: 0}

    for index, row in cow_merge.iterrows():

        if (row['tag_id'] == cow_id1):
            delta_time = row['start'] - time
            time = row['start']
            if (activity1 == activity2):
                synched += delta_time
                synched_specific[activity1] += delta_time
            else:
                unsynched += delta_time
                unsynched_specific[activity1] += delta_time

            activity1 = row['activity_type']
            pos1 = (row['x'], row['y'])

        else:
             delta_time = row['start'] - time
             time = row['start']
             if (activity1 == activity2):
                synched += delta_time
                synched_specific[activity2] += delta_time
             else:
                unsynched += delta_time
                unsynched_specific[activity2] += delta_time
             activity2 = row['activity_type']
             pos2 = (row['x'], row['y'])

        dist = math.sqrt((pos1[0]-pos2[0])*(pos1[0]-pos2[0]) + (pos1[1]-pos2[1])*(pos1[1]-pos2[1]))
        avg_dist += dist * delta_time
             
    end_time = row['start']
    avg_dist /= (end_time - start_time)

    return [cow_id1, cow_id2, avg_dist, synched, unsynched, synched_specific[0], unsynched_specific[0], synched_specific[1], unsynched_specific[1], synched_specific[2], unsynched_specific[2], 
        synched_specific[3], unsynched_specific[3], synched_specific[4], unsynched_specific[4], synched_specific[5], unsynched_specific[5], synched_specific[998], unsynched_specific[998], synched_specific[999], unsynched_specific[999], pair[2]]


def get_synchrony_proximity_for(df, proximity_threshold, pair):
    """
    Calculates and returns the time spent in synchrony between two pairs of cows, see get_synchrony_proximity().

    Parameters:
        df: the pandas dataframe
        proximity_threshold: the maximum distance to be considered in synchrony
        pair: the pair

    Returns:
        An array with the time spend in synchrony between the pair.
    """

    cow_id1 = pair[0]
    cow_id2 = pair[1]

    prox_thr2 = proximity_threshold*proximity_threshold

    cow_merge = df.loc[(df['tag_id'] == cow_id1) | (df['tag_id'] == cow_id2)]
    cow_merge = cow_merge.sort_values('start')

    start_time = df['start'][0]
  
    activity1 = 0
    activity2 = 0
    proximity = 0
    not_proximity = 0
    synched = 0
    unsynched = 0
    time = start_time
    pos1 = (-9999,-9999)
    pos2 = (9999,9999)

    synched_specific = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 998: 0, 999: 0}
    unsynched_specific = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 998: 0, 999: 0}

    for index, row in cow_merge.iterrows():

        # Squared distance between the cows
        dist2 = (pos1[0]-pos2[0])*(pos1[0]-pos2[0]) + (pos1[1]-pos2[1])*(pos1[1]-pos2[1])

        if (row['tag_id'] == cow_id1):
            delta_time = row['start'] - time
            time = row['start']
            if ((activity1 == activity2) & (dist2 <= prox_thr2)):
                synched += delta_time
                synched_specific[activity1] += delta_time
            else:
                unsynched += delta_time
                unsynched_specific[activity1] += delta_time

            if (dist2 <= prox_thr2):
                proximity += delta_time
            else:
                not_proximity += delta_time

            activity1 = row['activity_type']
            pos1 = (row['x'], row['y'])

        else:
             delta_time = row['start'] - time
             time = row['start']
             if ((activity1 == activity2) & (dist2 <= prox_thr2)):
                synched += delta_time
                synched_specific[activity2] += delta_time
             else:
                unsynched += delta_time
                unsynched_specific[activity2] += delta_time

             if (dist2 <= prox_thr2):
                proximity += delta_time
             else:
                not_proximity += delta_time
             
             activity2 = row['activity_type']
             pos2 = (row['x'], row['y'])

    return [cow_id1, cow_id2, proximity, not_proximity, synched, unsynched, synched_specific[0], unsynched_specific[0], synched_specific[1], unsynched_specific[1], synched_specific[2], unsynched_specific[2], 
     synched_specific[3], unsynched_specific[3], synched_specific[4], unsynched_specific[4], synched_specific[5], unsynched_specific[5], synched_specific[998], unsynched_specific[998], synched_specific[999], unsynched_specific[999], pair[2]]


def save_csv(sync_data, file_name):
    """
    Saves the synchrony data into a .CSV file.

    Parameters:
        df: the list of synchrony between all pairs of cows
        file_name: the name of the file to save the data to
    """
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sync_data)

def process_file(data_file, barn_file, save_file, proximity_threshold=300, limit=0, benchmark=False, print_progress=False):
    """
    Calculates the synchrony between all pairs of cows and stores it in a file.

    Parameters:
        data_file: the file containing the PA data
        barn_file: the file containing the barn layout
        save_file: the file to save the data to
        proximity_threshold: the maximum distance between the cows for them to be considered in synchrony. If 0, proximity wont be used, only activity
        limit: how many pairs in the list we want to use. If 0, all values will be used.
        benchmark: whether we want to to print the time it took to execute the program
        print_progress: whether we want to print the progress in console or not
    """

    if (print_progress):
        bm = time.time()

    # Load data
    df = data.csv_read_PA(data_file, 0)
    pairs = get_pairs(df, barn_file)

    # Get synchrony
    if (proximity_threshold == 0):
        sync_data = get_synchrony(df, pairs, limit, print_progress)
    else:
        sync_data = get_synchrony_proximity(df, pairs, proximity_threshold, limit, print_progress)

    # Save to file
    save_csv(sync_data, save_file)

    if (print_progress):
        bm = time.time() - bm
        print("Done! Took "+str(bm)+" s.")






