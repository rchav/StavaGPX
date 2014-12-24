import pandas as pd

filename = '20130223-233104-Ride.gpx'

points =[]
recordID = []
count = 0
lats = []
longs = []

with open(filename, 'r') as file:
	for line in file:
		cleanLine = line.strip()
		if cleanLine[:6] == "<trkpt":
			points.append(cleanLine)
			count = count + 1
			recordID.append(count)

			cleanLat = cleanLine[12:22]
			cleanLat = cleanLat.strip()
			
			cleanLong = cleanLine[29:41]
			cleanLong = cleanLong.strip()

			lats.append(cleanLat)
			longs.append(cleanLong)

df = pd.DataFrame(columns = ['RecordID', 'Trackpoint', 'Lat', 'Long', 'Elevation', 'Date'])
df['RecordID'] = recordID
df['Trackpoint'] = points
df['Lat'] = lats
df['Long'] = longs

print df
