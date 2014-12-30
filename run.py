import pandas as pd
import os
import Tkinter as Tk
import tkFileDialog
import sys
import time

points =[]
recordID = []
lats = []
longs = []
times = []
dates = []
elevations = []
fileNames =[]

trackptCount = 0
fileCount = 0
percent = 0

df = pd.DataFrame(columns = ['RecordID', 'FileName', 'Lat', 'Long', 'Elevation', 'Date', 'Time'])


# create some lists of flac files and their paths
fullPaths = []
justFileNames = []

def AskForFolderLocation():
    # Request file location from user
    global src
    root = Tk.Tk()
    root.withdraw()
    root.overrideredirect(True)
    root.geometry('0x0+0+0')
    root.deiconify()
    root.lift()
    root.focus_force()
    
    #ask user for file location
    src = tkFileDialog.askdirectory(parent=root)
    root.destroy()

def GetFiles(mySrc):
    # loop time
    for root, dirs, files in os.walk(mySrc, topdown=False):
        for name in files:

            # create a list of the full paths
            fullFilePath = os.path.join(root, name)
            if fullFilePath.endswith('.gpx'):
                fullPaths.append(fullFilePath)

            # create a list of the flac file names
            justFileName = os.path.join(name)
            if justFileName.endswith('.gpx'):
                justFileNames.append(justFileName)


def createLists(myFiles):
	global trackptCount
	global fileCount
	global percent
	for file in myFiles:
		with open(file, 'r') as file:
			temptimes = []
			tempdates = []
			for line in file:
				cleanLine = line.strip()

				if cleanLine[:6] == "<trkpt":
					points.append(cleanLine)
					trackptCount = trackptCount + 1
					recordID.append(trackptCount)

					cleanLat = cleanLine[12:22]
					cleanLat = cleanLat.strip()
					
					cleanLong = cleanLine[29:41]
					cleanLong = cleanLong.strip()
					cleanLong = cleanLong.strip('"')

					lats.append(cleanLat)
					longs.append(cleanLong)

					fileNames.append(str(file)[42:66])


				if cleanLine[:6] == "<time>":
					cleanTime = cleanLine[17:25]
					temptimes.append(cleanTime)
					

				if cleanLine[:6] == "<time>":
					cleanDate = cleanLine[6:16]
					tempdates.append(cleanDate)


				if cleanLine[:5] == "<ele>":
					cleanElevation = cleanLine[5:9]
					cleanElevation = cleanElevation.strip('<')
					elevations.append(cleanElevation)

			sys.stdout.write("\r%d%% complete" % percent)
			sys.stdout.flush()

			temptimes = temptimes[1:]
			for time in temptimes:
				times.append(time)
			
			tempdates = tempdates[1:]
			for date in tempdates:
				dates.append(date)


			fileCount = fileCount + 1
			percent = fileCount/len(fullPaths) * 100


AskForFolderLocation()
GetFiles(src)
createLists(fullPaths)

df['RecordID'] = recordID
df['Lat'] = lats
df['Long'] = longs
df['Time'] = times
df['Date'] = dates
df['Elevation'] = elevations
df['FileName'] = fileNames

writer = pd.ExcelWriter('map.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save


print "RecordID: " + str(len(recordID))
print "Points: " + str(len(points))
print "Lats: " + str(len(lats))
print "Longs: " + str(len(longs))
print "Times: " + str(len(times))
print "Dates: " + str(len(dates))
print "Elevations: " + str(len(elevations))
print "FileNames: " + str(len(fileNames))

print df

if len(recordID) == 0:
	print "\nLooks like something went wrong..."
else: 
	print "\nSuccess!"
