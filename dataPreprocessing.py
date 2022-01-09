# -*- coding: utf-8 -*-


import pandas as pd
import csv
import time
from os import listdir
from os.path import isfile, join
from calendar import timegm

#               0         1         2           3          4      5   6   7       8          9
# colnames=['dataType','tagID','tagString','startTime','endTime','x','y','z','activity','distance']

def find(dataArray, tagID): #finds all the indeces for a tagID in an array
    return [i for i, index in enumerate(dataArray) if index == tagID]

def syncTagsWithCows(inputData,cowPath): #function for syncing tagID and cowID with eachother so we operate with cows instead of tags
    colNames= ['CowID','Tag','From','To','Lactation','firstdate','lastdate','unclearTag','unclearCow']
    cowData = pd.read_csv(cowPath,names=colNames,skiprows=1,header=None,sep=';') #read the data to a variable
    
    cowTagCombinations = []
    cowInfo=[]
    outputData=[]
    
    for yee,row in cowData.iterrows(): #We change the time data in the cow-tag-sync information to milli epochs.
        try: #if the tag has been removed from the cow this works
            cowInfo.append([row['CowID'],row['Tag'],timegm(time.strptime(row['From'],'%Y-%m-%d')),timegm(time.strptime(row['To'],'%Y-%m-%d'))])
        except: #if the try doesn't work it will throw an exception because the cow is still wearing the tag. In that case we set the date to today seeing as we need an end date and the data is probably not from the future.
            cowInfo.append([row['CowID'],row['Tag'],timegm(time.strptime(row['From'],'%Y-%m-%d')),round(time.time()*1000)])
    
    for x in cowInfo: #Here we take out the relevant information and put it into a more workable array
        cowTagCombinations.append(x[0]) #cowid
        cowTagCombinations.append(x[1]) #tag
        cowTagCombinations.append(x[2]) #from
        cowTagCombinations.append(x[3]) #to
    
    for row in inputData: 
        try:
            indexes = find(cowTagCombinations,row[2]) #for each point of data we find all indeces for that tagID in the cowTagCombinations array
            for i in indexes: #for each index we check if the activity is performed within the timespan that the cow wore the tag.
                if cowTagCombinations[i+1] <= row[3] <=cowTagCombinations[i+2]: #If the tag was worn by the cow within said timespan we write the data into an array with the tagID changed to the relevant cowID.
                    outputData.append([row[0],int(cowTagCombinations[i-1]),row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]])
        except: #if the find function can't find any indeces with that tagID it's going to throw a fit. So we let it pass and go to the next tagID since the last tagID wasn't associated with a cow.
            pass
    return outputData

def smoothData(inputData,timeThreshold):
    aktivitet = [1,2,3,4,999]
    sparadeAktiviteter = [] #to know the latest activity
    heldActivities = [] #Keeping activities until we have an activity to change
    outputData = []
    for row in inputData: #iterate over the data array row for row
        if row[4]-row[3] < timeThreshold: #if the activity time is under a preset threshold
            if [row[1],1] in sparadeAktiviteter or [row[1],2] in sparadeAktiviteter or [row[1],3] in sparadeAktiviteter or [row[1],4] in sparadeAktiviteter or [row[1],999] in sparadeAktiviteter: #if the tagID is in sparadeAktiviteter with any activity
                for e in aktivitet: #This tries to find the current activity through brute force by trying each activity. Not elegant but effective
                    try:
                        outputData.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],sparadeAktiviteter[sparadeAktiviteter.index([row[1],e])][1],row[9]])#write a row in new datafile with the previous activity
                    except:
                        pass
            else: #if we have no previous activities to set the short activity to we hold it until we have a longer activity that we can use to attribute it to
                heldActivities.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]])
        else: #if the activity is longer than the time threshold we write it into the new csv file
            outputData.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]])
            if [row[1],1] in sparadeAktiviteter or [row[1],2] in sparadeAktiviteter or [row[1],3] in sparadeAktiviteter or [row[1],4] in sparadeAktiviteter or [row[1],999] in sparadeAktiviteter: #if the current tagID is in sparadeaktiviteter we write over the old with the new activity
                for e in aktivitet:
                    try:
                        tmpIndex = sparadeAktiviteter.index([row[1],e])
                    except:
                        pass
                sparadeAktiviteter[tmpIndex] = [row[1],row[8]]
            else: #If the tagID is not in sparadeaktiviteter we append it to the list
                sparadeAktiviteter.append([row[1],row[8]])
                if len(heldActivities)>0:#check if we've held any activities
                    removeIndex = []
                    for i in range(len(heldActivities)):#Then we check if we've held any activities with this tagID and if so we write it to the csv with the new activity
                        if row[1] in heldActivities[i]:
                            heldActivities[i][8] = row[8]
                            outputData.append(heldActivities[i])
                            removeIndex.append(i)
                    for i in reversed(removeIndex): #We remove the written heldactivities in reverse order to preserve the indexing
                        del heldActivities[i]
    return outputData

def removeInactiveTags(inputData,distanceThreshold): #Function to remove inactive tags based on a minimum threshold for total distance travelled in the y direction.
    susTagID = [[1,2,10]] #System works by adding up distance until a tag is considered active. Must start the list of not verified tags with a value for the function to work proper.
    safeTagID = []
    outputData = []
    for row in inputData: 
        if row[1] not in safeTagID: #for each row in the data, check if the tag is considered active.
            for i in range(len(susTagID)):
                if row[1] in susTagID[i]: #for each value in the not verified pool, check if the tag is in the pool.
                    susTagID[i][2] = abs(susTagID[i][1] - row[6]) #if yes, safe the distance it's travelled for this data node
                    if susTagID[i][2] > distanceThreshold: #if the tag is now over a threshold we add it to the safe tag list and remove it from the non verified list.
                        safeTagID.append(row[1])
                        del susTagID[i]
                    else:
                        susTagID[i][1] = row[6]
                    break #break the loop since it's surved it's purpose
                elif i == len(susTagID)-1: #if the loop has gone all the way to the end and still hasn't found the tag in the non verified tags(and of course not in the safe tags), add it to the non verified list.
                    susTagID.append([row[1],row[6],0])
    for row in inputData: #Write all the safe tag ids data into the output array
        if row[1] in safeTagID:
            outputData.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]])
    return outputData

def combineWalkingStanding(inputData): #function to combine two activities. Hardcoded to combine walking and standing
    activityToBeCombinedTo = 2
    activityToBeCombinedFrom = 1
    outputData = []
    for row in inputData: #for each row check if the activity is the one we want to merge into another. If so write the data with the other activity. Else write the data as it was into the output data array.
        if row[8] == activityToBeCombinedFrom:
            outputData.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],activityToBeCombinedTo,row[9]])
        else:
            outputData.append(row)
    return outputData

def readFile(path): #function to read the data from the file and put it into an array, making it easier to work with.
    colnames=['dataType','tagID','tagString','startTime','endTime','x','y','z','activity','distance']
    rawData = pd.read_csv(path,names=colnames,header=None)
    data=[]
    for yee, row in rawData.iterrows(): #iterate for each row and append the data to the array
        data.append([row['dataType'],row['tagID'],row['tagString'],row['startTime'],row['endTime'],row['x'],row['y'],row['z'],row['activity'],row['distance']])
    return data
    
def oneFunctionToRuleThemAll(ansSyncCowTag,pathCowTagCSV,ansMultiFile,inPath,outPath,anssmoothData,timeThreshold,anscombineWalkingStanding,ansremoveInactiveTags,distanceThreshold):
    if ansMultiFile: #if we have multiple files to process, find all files in the directory and send them to selected functions to be processed.
        fileNames = [f for f in listdir(inPath) if isfile(join(inPath,f))]
        for fileName in fileNames:
            print('Now processing file: ',fileName) #progress update
            data = readFile(inPath+fileName)
            if ansSyncCowTag:
                data = syncTagsWithCows(data,pathCowTagCSV)
            if ansremoveInactiveTags:
                data = removeInactiveTags(data, distanceThreshold)
            if anssmoothData:
                data = smoothData(data,timeThreshold)
            if anscombineWalkingStanding:
                data = combineWalkingStanding(data)
                
            #Open a new file to write the data to, then loop the resultant data to write it into the file
            f = open(outPath+fileName,'w')
            writer = csv.writer(f,lineterminator = '\n')
            for row in data:
                writer.writerow(row)
            f.close()   
    else:#if we only have a single file to process, read the selected file and send data to selected functions to be processed.
        data = readFile(inPath)
        if ansSyncCowTag:
            data = syncTagsWithCows(data,pathCowTagCSV)
        if ansremoveInactiveTags:
            data = removeInactiveTags(data, distanceThreshold)
        if anssmoothData:
            data = smoothData(data,timeThreshold)
        if anscombineWalkingStanding:
            data = combineWalkingStanding(data)
            
        #Open a new file to write the data to, then loop the resultant data to write it into the file
        f = open(outPath,'w')
        writer = csv.writer(f,lineterminator = '\n')
        for row in data:
            writer.writerow(row)
        f.close()
        
def main():
    if 1:#If manual entry select if 1: for entry with pre-choice select if 0
        answerIndex = []
        
        answerTagSync = input('Sync tagID with cowID?(Y/N):')
        if answerTagSync == 'Y':
            syncPath = input('Path to sync file(ex. syncData/cowTagMap.csv)')
            answerIndex.append(1)
            answerIndex.append(syncPath)
        elif answerTagSync == 'N':
            answerIndex.append(0)
            answerIndex.append(0)
        
        answerMultipleFiles = input('Multiple data files to handle(Y/N):')
        if answerMultipleFiles == 'Y':
            inputDataPath = input('Path to input data files(ex. data/2020/august/): ')  
            outputDataPath = input('Path for output data files(ex. data/agregateddata/2020/august): ')
            answerIndex.append(1)
            answerIndex.append(inputDataPath)
            answerIndex.append(outputDataPath)
        elif answerMultipleFiles == 'N':
            inputDataPath = input('Path to input data file(ex. data/PA_20201017T000000UTC.csv): ')
            outputDataPath = input('Path for output data file(ex. data/agregateddata/2020/august): ')
            answerIndex.append(0)
            answerIndex.append(inputDataPath)
            answerIndex.append(outputDataPath)
            
        answerSmooth = input('Smooth the data?(Y/N):')
        if answerSmooth == 'Y':
            timeThreshold = input('Smooth the data with what time threshold in seconds(default 10s)?:')
            answerIndex.append(1)
            answerIndex.append(int(timeThreshold)*1000)
        elif answerSmooth == 'N':
            answerIndex.append(0)
            answerIndex.append(0)
            
        
        answerCombineWalkingStanding = input('Combine Standing and Walking activity?(Y/N):')
        if answerCombineWalkingStanding == 'Y':
            answerIndex.append(1)
        elif answerCombineWalkingStanding == 'N':
            answerIndex.append(0)
        
        answerThreshold = input('Remove cows that havent moved a certain distance threshold in Y direction?(Y/N): ')
        if answerThreshold == 'Y':
            distanceThreshold = input('How big should the distance threshold be in meters(default 18m)?')
            answerIndex.append(1)
            answerIndex.append(int(distanceThreshold)*100)
        elif answerThreshold == 'N':
            answerIndex.append(0)
            answerIndex.append(0)
        
    else:
        #[sync cows and tags?, cowtagsyncpath?,multiple files?, input path?, output path?, smooth?, timethreshold?, combine standing/walking?,remove inactive tags?, distancethreshold?]
        answerIndex = [1,'cowTagMap.csv',1, 'data/', 'agregeradData/', 1, 10000, 0, 1, 1800]
        
    oneFunctionToRuleThemAll(answerIndex[0],answerIndex[1],answerIndex[2],answerIndex[3],answerIndex[4],answerIndex[5],answerIndex[6],answerIndex[7],answerIndex[8],answerIndex[9])
    
    
if __name__ == "__main__":
    main()