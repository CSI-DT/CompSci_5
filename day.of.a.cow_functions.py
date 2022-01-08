import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import time

#   This script consists of funcitons i used and then main fuctions which should be ready to run. All that is needed is to manually enter the paths...
#   in the function called "download_data".

# One thing worth knowing is what is called "act". Here that is a 14x4 matrix where each row is how much the cow spent on each of the 4 activities for that day.
# so [0, 0, 0, 24] would mean that it spent all day eating. 14 of these hours spent matrices make up the "act" short for "activities" matrices.

def csv_read_PA(filename, nrows): # Reads the file
    if nrows == 0:
        df = pd.read_csv(filename, header=None)
    else:
        df = pd.read_csv(filename, nrows=nrows, header=None)
    df.columns = ['data_entity', 'tag_id', 'tag_string', 'start', 'end', 'x', 'y', 'z', 'activity_type', 'distance']
    return df

def fday(a, length, activities, tagid): # downloads data for creates a 4 slot array with average values for a specific cow for a specific day
    for i in range(0,length):
        if(a['tag_id'][i]==tagid):
            if(a['activity_type'][i]==1):
                activities[0] = activities[0] + a['end'][i] - a['start'][i]
            if(a['activity_type'][i]==2):
                activities[1] = activities[1] + a['end'][i] - a['start'][i]  
            if(a['activity_type'][i]==3):
                activities[2] = activities[2] + a['end'][i] - a['start'][i]
            if(a['activity_type'][i]==4):
                activities[3] = activities[3] + a['end'][i] - a['start'][i]
    for i in range(0,4):
        activities[i] = activities[i]/1000/60/60
    print('.', end='')

def pront(activities): #plots out the data for 4 activities
    names = ['Standing', 'Walking', 'in Cubicle', 'At feed']
    fig = plt.figure(figsize = (10, 4))
    plt.bar(names, activities) 
    plt.xlabel("Courses offered")
    plt.ylabel("Number of seconds")
    plt.title("Activity distribution of one cow one day")
    plt.show()

def printex(a): #test to print out an activity array
    print(a)
    print(print(a['distance'][1]))

def sumtime(activities): #sums up activity time, help check if they add up to 24h
    sum = activities[0] + activities[1] + activities[2] + activities[3]
    print("SUM ",  sum)

def download_data(id_current): # calls fday to go trough each day and donload data. Pleas note that file-paths have to be entered manually
    print("Getting data for cow-id ", end="")
    act = []
    act1 = [0,0,0,0]
    path1 = '/Users/samuel/Documents/python/project/PA/PA_20201016T000000UTC.csv'  
    a1 = csv_read_PA(path1, 387630)
    act.append(act1)
    fday(a1, 387630, act1, id_current)

    # print(a1)

    act2 = [0,0,0,0]
    path2 = '/Users/samuel/Documents/python/project/PA/PA_20201017T000000UTC.csv'
    a2 = csv_read_PA(path2, 407205)
    act.append(act2)
    fday(a2, 407205, act2, id_current)

    act3 = [0,0,0,0]
    a3 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201018T000000UTC.csv', 415105)
    fday(a3, 415105, act3, id_current)
    act.append(act3)


    act4 = [0,0,0,0]
    a4 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201019T000000UTC.csv', 404736)
    fday(a4, 404736, act4, id_current)
    act.append(act4)

    act5 = [0,0,0,0]
    a5 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201020T000000UTC.csv', 381498)
    fday(a5, 381498, act5, id_current)
    act.append(act5)

    act6 = [0,0,0,0]
    a6 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201021T000000UTC.csv', 394454)
    fday(a6, 394454, act6, id_current)
    act.append(act6)

    act7 = [0,0,0,0]
    a7 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201022T000000UTC.csv', 391122)
    fday(a7, 391122, act7, id_current)
    act.append(act7)

    act8 = [0,0,0,0]
    a8 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201023T000000UTC.csv', 387146)
    fday(a8, 387146, act8, id_current)
    act.append(act8)


    act9 = [0,0,0,0]
    a9 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201024T000000UTC.csv', 375912)
    fday(a9, 375912, act9, id_current)
    act.append(act9)

    act10 = [0,0,0,0]
    a10 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201025T000000UTC.csv', 388549)
    fday(a10, 388549, act10, id_current)
    act.append(act10)

    act11 = [0,0,0,0]
    a11 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201026T000000UTC.csv', 379473)
    fday(a11, 379473, act11, id_current)
    act.append(act11)

    act12 = [0,0,0,0]
    a12 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201027T000000UTC.csv', 384718)
    fday(a12, 384718, act12, id_current)
    act.append(act12)

    act13 = [0,0,0,0]
    a13 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201028T000000UTC.csv', 392246)
    fday(a13, 392246, act13, id_current)
    act.append(act13)

    act14 = [0,0,0,0]
    a14 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201029T000000UTC.csv', 386824)
    fday(a14, 386824, act14, id_current)
    act.append(act14)
    print("  Done ")
    return act

def avg_time(act):  #finds the average time spent on each activity for a cow
    act_avg = [0,0,0,0]
    for i in range(0,4):
        for j in range(0,14):
            act_avg[i] += act[j][i]
    
    for i in range(0,4):
        act_avg[i] /= 14
    return act_avg

def dev_avg(act_avg, act): # finds the deviation in hours from what the cow normally spends
    deviation = np.zeros((14, 4))
    for i in range(0,14):
        deviation[i] -= act_avg

    for i in range (0,4):
        for j in range(0,14):
            deviation[j][i] += act[j][i]

    return deviation

def plot_deviation(deviation):
    N = 4
    ind = np.arange(N) 
    width = 0.05
    bar1 = plt.bar(ind, deviation[0], width)
    bar2 = plt.bar(ind+width, deviation[1], width)
    bar3 = plt.bar(ind+width*2, deviation[2], width)
    bar4 = plt.bar(ind+width*3, deviation[3], width)
    bar5 = plt.bar(ind+width*4, deviation[4], width)
    bar6 = plt.bar(ind+width*5, deviation[5], width)
    bar7 = plt.bar(ind+width*6, deviation[6], width)
    bar8 = plt.bar(ind+width*7, deviation[7], width)
    bar9 = plt.bar(ind+width*8, deviation[8], width)
    bar10 = plt.bar(ind+width*9, deviation[9], width)
    bar11 = plt.bar(ind+width*10, deviation[10], width)
    bar12 = plt.bar(ind+width*11, deviation[11], width)
    bar13 = plt.bar(ind+width*12, deviation[12], width)
    bar14 = plt.bar(ind+width*13, deviation[13], width)
    #plt.xlabel("Dates")
    plt.ylabel('Hours Spent')
    plt.title("Deviation from average day in hours")
    plt.xticks(ind+width,['Standing', 'Walking', 'in Cubicle', 'At feed'])
    plt.legend( (bar1, bar2, bar3, bar4), ('Day 1', 'Day 2', 'Day 3', 'And so on...') )
    plt.show()

def plot_daily(act):
    N = 4
    ind = np.arange(N) 
    width = 0.05
    bar1 = plt.bar(ind, act[0], width)
    bar2 = plt.bar(ind+width, act[1], width)
    bar3 = plt.bar(ind+width*2, act[2], width)
    bar4 = plt.bar(ind+width*3, act[3], width)
    bar5 = plt.bar(ind+width*4, act[4], width)
    bar6 = plt.bar(ind+width*5, act[5], width)
    bar7 = plt.bar(ind+width*6, act[6], width)
    bar8 = plt.bar(ind+width*7, act[7], width)
    bar9 = plt.bar(ind+width*8, act[8], width)
    bar10 = plt.bar(ind+width*9, act[9], width)
    bar11 = plt.bar(ind+width*10, act[10], width)
    bar12 = plt.bar(ind+width*11, act[11], width)
    bar13 = plt.bar(ind+width*12, act[12], width)
    bar14 = plt.bar(ind+width*13, act[13], width)
    #plt.xlabel("Dates")
    plt.ylabel('Hours Spent')
    plt.title("Hours spent on each activity per day")

    plt.xticks(ind+width,['Standing', 'Walking', 'in Cubicle', 'At feed'])
    plt.legend( (bar1, bar2, bar3, bar4), ('Day 1', 'Day 2', 'Day 3', 'And so on...') )
    plt.show()

def plot_array(values, xaxis, yaxis, titletext): #plots an array for given size
    title = []
    for i in range(0,len(values)):
        title.append(i)

    fig = plt.figure(figsize = (10, 5))

    plt.bar(title, values, color ='green', width = 0.4)
    plt.xlabel(xaxis)
    #plt.xticks(0.1,['Standing', 'Walking', 'in Cubicle', 'At feed'])
    plt.ylabel(yaxis)
    plt.title(titletext)
    plt.show()

def printa(a): #prints out a 14x4 matrix with activity times for easy viewing
    for i in range(0,14):
        for j in range(0,4):
            print(math.floor(a[i][j]), "    ", end='')
        sum = 0 
        for x in range(0,4):
            sum += a[i][x]
        print("{:.1f}".format(sum))

def correlate(a1, a2):  # finds correlation between two cows
    correlation = []
    for i in range(0,len(a1)):
        correlation.append(np.corrcoef(a1[i],a2[i])[0][1])
    return correlation

def plot4(deviation): #plots correlation between two cows on time spent on each of the 4 activities
    N = 4
    ind = np.arange(N) 
    width = 0.3
    bar1 = plt.bar(0, deviation[0], width)
    bar2 = plt.bar(1, deviation[1], width)
    bar3 = plt.bar(2, deviation[2], width)
    bar4 = plt.bar(3, deviation[3], width)
    plt.xlabel("Activity")
    plt.ylabel('Correlation')
    plt.title("Correlation of the activities between two cows")
    plt.xticks(ind+width,['Standing', 'Walking', 'in Cubicle', 'At feed'])
    #plt.legend( (bar1, bar2, bar3, bar4), ('Day 1', 'Day 2', 'Day 3', 'And so on...') )
    plt.show()

def correlate_activity(a1, a2, activity_number): #finds correlation between two cows on a specific activity
    correlation = []
    b1 = []
    b2 = [] 
    for i in range(0, len(a1)):
        b1.append(a1[i][activity_number])
        b2.append(a2[i][activity_number])
    out = np.corrcoef(b1, b2)[0][1]
    return (out)

def main_plot4_corrs(): #plots the correlation between two cows for each activity
    a1 = download_data(2421804)
    a2 = download_data(2428348)
    corri = []
    corri.append(correlate_activity(a1,a2,0))
    corri.append(correlate_activity(a1,a2,1))
    corri.append(correlate_activity(a1,a2,2))
    corri.append(correlate_activity(a1,a2,3))
    print(corri)
    plot4(corri)

def summarize_correlation(a1, a2): #summarize the correlation into a single number
    #a1 = download_data(id1)
    #a2 = download_data(id2)
    abc = correlate(a1, a2)
    sum = 0
    for i in range(0,14):
        sum +=abc[i]
    return sum/14 #divide by 14 to normalize to 1

def make_correlation_matrix(list_of_ids): #creates the correlation matrix
    mx = np.zeros((len(list_of_ids), len(list_of_ids)))

    a = 0
    b = 0
    for i in list_of_ids:
        b = 0
        for j in list_of_ids:
            if(i==j):
                mx[a][b] = 1
            else:
                mx[a][b] = summarize_correlation(i,j)
            b +=1
            print("i is now: ", i)
            print("j is now: ", j)
        a +=1
    return mx

def plot_matrix(mx, title):
    print(mx)
    [m,n] = np.shape(mx)
    #Colour Map using Matrix
    plt.figure()
    plt.imshow(mx, alpha=0.8)
    plt.xticks(np.arange(n))
    plt.yticks(np.arange(m))
    plt.colorbar()
    # plt.xlabel('Numbers')
    # plt.ylabel('Value')
    plt.title(title)
    plt.show()

def c414(act1, act2): #return the correlation of all activites between a pair of cows
    sum = 0
    for i in range(0,14):
        sum += np.corrcoef(act1[i], act2[i])[0][1]
    return(sum/14)

def make_activities(list_of_ids): #creates a list of 14x4 activity matrices
    act_arrays = []
    index = 0
    for i in list_of_ids:
        print("@ id = ", i, "index: ", index) #prints out how far we have come
        index = index + 1
        act = download_data(i)
        act_arrays.append(act)
    return act_arrays

def time_check(list_of_ids): #print out the time spent for list of cows (can be used to detect errors in data)
    ll = make_activities(list_of_ids)
    for q in range(0,len(ll)):
        for i in range(0,14):
            for j in range(0,4):
                act = ll[q]
                print("  ", "{:.1f}".format(act[i][j]), end='')
            print(" ")
        print("")
        print("Next cow:")
        print("")

def c414b(act1, act2, x): #calculated correlation for one activity x=0 means activity standing x=1 means walking x=2 is sleeping and x=3 is eating
    list1 = []
    list2 = []
    for i in range(0,14):
        list1.append(act1[i][x])
        list2.append(act2[i][x])
    sum = np.corrcoef(list1, list2)[0][1]
    print("SUM HERE:    ", sum)
    return sum

def sort_matrix(m): # this function is used in main 4,5,6 to sort the matrices before plotting
    a = len(m)
    arr = []
    for i in range(0,a):
        arr.append(0)
    for i in range(0,a):
        for j in range(0,a):
            arr[i] += m[j][i]
    
    plot_matrix(m, "Befor sorting")

    for i in range(0,a):
        for j in range(0,a):
            if(arr[i] > arr[j]):
                #swap the arrray
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                #also swap the corresponding matrix
                for x in range(0,a):
                    temp2 = m[x][i]
                    m[x][i] = m[x][j]
                    m[x][j] = temp2

    arr = []
    for i in range(0,a):
        arr.append(0)
    for i in range(0,a):
        for j in range(0,a):
            arr[i] += m[i][j]

    for i in range(0,a):
        for j in range(0,a):
            if(arr[i] > arr[j]):
                #swap the arrray
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                #also swap the corresponding matrix
                for x in range(0,a):
                    temp2 = m[i][x]
                    m[i][x] = m[j][x]
                    m[j][x] = temp2


############################################################################# This section checks which id:s seem valid. (In order to get the 101 list.)

def not_in_list(list, element): #checks if an id is not already in the list to prevent doubles
    for i in range(0, len(list)):
        if(list[i]==element):
            return 0
    return 1

def listcows(a, legth): # looks at one day and adds all cow id:s
    # Reads in all
    list = []
    for i in range(0,legth):
        list.append(a['tag_id'][i])
    #sort part
    list2 = []
    list2.append(list[0])
    for i in range(0,len(list)):
        if(not_in_list(list2, list[i])):
            list2.append(list[i])
    list2.sort()
    list = list2
    #sort part
    return list

def sort_cow(id_current): #sorts out which cow ids seems to not be broken or who dont provide bad data
    act = download_data(id_current)
    printa(act) #prints out the activity matrix so if it is not addedwe can easily se what went wrong
    for i in range(0,14):
        sum = 0
        for j in range(0,4):
            sum += act[i][j]
        if (sum < 23.9 or sum > 24.1): #if total time spent per day deviates too much dont include the id
            print("Removed: ", id_current)
            return 0

    for i in range(0,14): # if more then 23 hours or less then 1 hour is spent on an activity something probably is wrong
        for j in range(0,4): #some cows may only spend one hour on activity x every day but i wanted to be extra safe not to include bad data
            if(act[i][j] > 23 or act[i][j] < 1):
                print("Removed: ", id_current)
                return 0

    print("Addedd: ", id_current)
    return id_current

def print_list_of_valid_ids():
    a1 = csv_read_PA('/Users/samuel/Documents/python/project/PA/PA_20201016T000000UTC.csv', 387630)
    list = listcows(a1, 387630) # creates a list of all cows id:s from 20201016

    # for i in range(0,len(list)):  #length = 231  in case we want to quickly print the list to see it, 
    #     print(list[i])
    #     print("Length of list: ", len(list))

    list_corrected = [] #to this list we will only add the id:s that there seems to be nothing wrong with
    index = 0
    for i in list:
        print("index: ", index)
        if(sort_cow(i)):
            list_corrected.append(i)
        index += 1  # printing this out to see how long we have come 
    print("Following is the list of id:s where each day adds up to 24h: ")
    for i in list_corrected:
        print(i)

#############################################################################


# MAIN PROGRAMS

def main1(id_current): #plots out hours spent and deviation for one cow
    act = download_data(id_current)
    act_avg = avg_time(act)
    deviation = dev_avg(act_avg, act)
    plot_deviation(deviation)
    plot_daily(act)
    # plot_ds(deviation)  ##Bonus function 

def main2(id1, id2): # plots correlation btw all activities each day for 2 cows
    a1 = download_data(id1)
    a2 = download_data(id2)
    cor = correlate(a1, a2)
    x_axis = 'Day'
    y_axis = 'Correlation'
    title = 'Correlation between two cowids over 14 days'
    plot_array(cor, x_axis, y_axis, title)

def main3(id1, id2): # Plot out corrrelation for the 4 activities
    a1 = download_data(id1)
    a2 = download_data(id2)
    corri = []
    corri.append(correlate_activity(a1,a2,0))
    corri.append(correlate_activity(a1,a2,1))
    corri.append(correlate_activity(a1,a2,2))
    corri.append(correlate_activity(a1,a2,3))
    print("Numbers of plot printed out: ", corri)
    plot4(corri)

def main4(list_of_ids): # plots correlation matrix 
    lngth = len(list_of_ids)
    ll = make_activities(list_of_ids)  # creates a list where each element is a 4x14 matrix with the activity times
    m = np.zeros((lngth,lngth)) #Matrix with the correct size we ant to plot
    for i in range(0,lngth):
        for j in range(0,lngth):
            m[i][j] = c414(ll[i], ll[j])
        print("")
    sort_matrix(m) ##SORT
    print(m)
    plot_matrix(m, 'Pairwise correlation of activities for list of cows')

def main5(list_of_ids, x): # plots correlation matrix for one activity
    lngth = len(list_of_ids)
    ll = make_activities(list_of_ids)
    m = np.zeros((lngth,lngth))
    print("CHECK............")
    for i in range(0,lngth):
        for j in range(0,lngth):
            m[i][j] = c414b(ll[i], ll[j], x)
        print("")
    print(m)
    plot_matrix(m, 'Pairwise correlation between time spent on given activity for given list of cows')

def main6(list_of_ids): # List of cow correlation to average
    lngth = len(list_of_ids)
    ll = make_activities(list_of_ids)
    avg = np.zeros((14,4))
    for c in range(0,lngth):
        act = ll[c]
        for i in range(0,14):
            for j in range(0,4):
                avg[i][j] += act[i][j]
    
    for i in range(0,14):
        for j in range(0,4):
            avg[i][j] = avg[i][j]/14          

    m = []
    for i in range(0,lngth):
        m.append(c414(ll[i], avg))
    
    matrixx = np.zeros((len(m),len(m)))
    
    for i in range(0,len(m)):
        for j in range(0,len(m)):
            matrixx[i][j] = m[j]

    sort_matrix(matrixx)
    plot_matrix(matrixx, 'How well the cows synchronize with the group on average')

    # print(m)
    # plot_array(m, 'Cow Number', 'Correlation', 'Correlation between how a cow spends its time relative to the average of all cows ')

def main_main():
    complete_list = [2417175, 2417195, 2420450, 2421765, 2421773, 2421788, 2421804, 2421834, 2421869, 2421874, 2423344, 2423349, 2423364, 2423378, 2426244, 2426245, 2426253, 2426262, 2426270, 2426271, 2426290, 2427443, 2427445, 2427458, 2427465, 2427540, 2427555, 2427562,2427564, 2427565, 2427567, 2427590, 2427599, 2427608, 2427703, 2427728, 2427729, 2427737,2427898, 2427905, 2428056, 2428062, 2428068, 2428071, 2428072, 2428080, 2428091, 2428094,2428176, 2428289, 2428292, 2428315, 2428323, 2428331, 2428364, 2428385, 2428398, 2428709,2428711, 2428714, 2428724, 2428732, 2428739, 2428744, 2428745, 2428760, 2428764, 2428776,2428778, 2428782, 2428788, 2428789, 2428793, 2428796, 2428861, 2428863, 2428865, 2428876,2428877, 2428879, 2428880, 2428893, 2428894, 2428902, 2428905, 2428906, 2432025, 2432098,2432127, 2432129, 2432152, 2432652, 2432668, 2432674, 2432680, 2433119, 2433132, 2433142,2433145, 2433148 ,2433164]
    print("What would you like to test?")
    print("Enter 1 for looking at graphs for time spent each day for one cow")
    print("Enter 2 for looking at correlation between all activities for 2 cows")
    print("Enter 3 to look at correlation  between all 4 activities individually between 2 cows")
    print("Enter 4 to get an overview of cow each pair of cows correlate on all activities")
    print("Enter 5 to get an overview of cow each pair of cows correlate on one activity")
    print("Enter 6 to get an overview of cow each cow correlates on all activities to the average")
    print("Enter 7 for a listing of the 101 cow:id deemed non-corrupt (! long runtime) ... ")
    x = input("Enter number: ")
    x = int(x)
    if(x==1):
        index = input("Choose a number between 0 and 100 (each number = unique cow): ")
        index = int(index)
        chosen_id =  complete_list[index]
        main1(chosen_id)
    if(x==2):
        index1 = input("Choose a number between 0 and 100 (each number = unique cow): for the first cow ")
        index1 = int(index1)
        chosen_id1 = complete_list[index1]
        index2 = input("Choose a number between 0 and 100 (each number = unique cow): for the socond cow ")
        index2 = int(index2)
        chosen_id2 = complete_list[index2]
        main2(chosen_id1, chosen_id2) 
    if(x==3):
        index1 = input("Choose a number between 0 and 100 (each number = unique cow): for the first cow ")
        index1 = int(index1)
        chosen_id1 = complete_list[index1]
        index2 = input("Choose a number between 0 and 100 (each number = unique cow): for the socond cow ")
        index2 = int(index2)
        chosen_id2 = complete_list[index2]
        main3(chosen_id1, chosen_id2)
    if(x==4):
        choice = int(input("For a pre-determined list enter 1, to choose your own cow-id:s enter 2  "))
        listy = []
        if(choice == 1):
            length = int(input("How many id:e do you want? (101 = max)  "))
            for i in range(0,length):
                listy.append(complete_list[i])
        if(choice == 2):
            listy = []
            numba = 1
            while(numba < 101 or numba >= 0):
                numba = int(input("Enter cow number (0-100 you wish to enter) [enter any number above 100 when done]  "))
                numba 
                if(numba < 0 or numba > 100):
                    print("done")
                    break
                if (numba <= 100):
                    print("Cow with number: ", numba, " and with cow:id = ", complete_list[numba], "  is now added")
                    listy.append(complete_list[numba])
        main4(listy)
    if(x==5):
        choice = int(input("For a pre-determined list enter 1, to choose your own cow-id:s enter 2  "))
        listy = []
        if(choice == 1):
            length = int(input("How many id:e do you want? (101 = max)"))
            for i in range(0,length):
                listy.append(complete_list[i])
        if(choice == 2):
            numba = 1
            while(numba < 101 or numba >= 0):
                numba = int(input("Enter cow number (0-100 you wish to enter) [enter any number above 100 when done]  "))
                if(numba < 0 or numba > 100):
                    print("done")
                    break
                if (numba <= 100):
                    print("Cow with number: ", numba, " and with cow:id = ", complete_list[numba], "  is now added")
                    listy.append(complete_list[numba])
        x = int(input("Finally let us know which activity you want to look at. (0=standing, 1 = walking, 3 = sleeping and 4 = eating  "))
        main5(listy, x)
    if(x==6):
        choice = int(input("For a pre-determined list enter 1, to choose your own cow-id:s enter 2  "))
        listy = []
        if(choice == 1):
            length = int(input("How many id:e do you want? (101 = max)  "))
            for i in range(0,length):
                listy.append(complete_list[i])
        if(choice == 2):
            listy = []
            numba = 1
            while(numba < 101 or numba >= 0):
                numba = int(input("Enter cow number (0-100 you wish to enter) [enter any number above 100 when done]  "))
                if(numba < 0 or numba > 100):
                    print("done")
                    break
                if (numba <= 100):
                    print("Cow with number: ", numba, " and with cow:id = ", complete_list[numba], "  is now added ")
                    listy.append(complete_list[numba])
        main6(listy)
    if(x==7):
        print_list_of_valid_ids()

main_main()

print("#########################################################################################################################################################")
print("# End of program         ", datetime.now().strftime("%H:%M:%S"))
print("#########################################################################################################################################################")

