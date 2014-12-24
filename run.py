import pandas as pd
import os

src = 'C:\Projects\StravaGPX\gpx_files'

points =[]
recordID = []
lats = []
longs = []
times = []
dates = []
elevations = []
fileNames =[]

trackptCount = 0

df = pd.DataFrame(columns = ['RecordID', 'FileName', 'Trackpoint', 'Lat', 'Long', 'Elevation', 'Date', 'Time'])


# create some lists of flac files and their paths
fullPaths = []
justFileNames = []


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

					lats.append(cleanLat)
					longs.append(cleanLong)

					fileNames.append(file)


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

				print str(trackptCount) + " of " + str(len(fullPaths))

			temptimes = temptimes[1:]
			for time in temptimes:
				times.append(times)
			
			tempdates = tempdates[1:]
			for date in tempdates:
				dates.append(dates)


GetFiles(src)
createLists(fullPaths)

df['RecordID'] = recordID
df['Trackpoint'] = points
df['Lat'] = lats
df['Long'] = longs
df['Time'] = times
df['Date'] = dates
df['Elevation'] = elevations
df['FileName'] = fileNames

df.to_csv("map.csv", index=False)


# print len(recordID)
# print len(points)
# print len(lats)
# print len(longs)
# print len(times)
# print len(dates)
# print len(elevations)
# print len(fileNames)

print "success"
